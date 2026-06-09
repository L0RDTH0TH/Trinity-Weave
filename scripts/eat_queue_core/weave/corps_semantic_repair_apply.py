"""Phase 10c-B — host apply from conceptual regen pack (Task/agent CLI).

10c-A writes the regen pack and heuristic fallback; this module invokes the local
Cursor ``agent -p`` hand-off (or applies parsed YAML from stdout) to patch only
the ``conceptual:`` block on provisional cards.
"""

from __future__ import annotations

import copy
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from ..agent_cli import find_agent_cli
from .config import load_trinity_config
from .corps_repair_audit import append_corps_repair_audit
from .governance import append_metric_row
from .trinity_card import get_conceptual
from .trinity_card_paths import load_trinity_card, resolve_trinity_card_path, write_trinity_card
from .trinity_conceptual_doctrine import (
    conceptual_has_meta_contamination,
    conceptual_has_machine_voice,
)

PACK_DIR_REL = Path(".technical/weave/semantic-regen-packs")
TRIAL_BACKUP_DIR_REL = Path(".technical/weave/validation/semantic-trial-backups")

_YAML_FENCE = re.compile(r"```(?:yaml)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)

REQUIRED_CONCEPTUAL_FIELDS = ("outcome", "summary", "primary_case")

FORBIDDEN_HOST_APPLY = (
    "patch_touch",
    "patch_rules",
    "patch_contract",
    "patch_meta",
    "promote_to_locked",
    "delete_card",
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def semantic_host_apply_enabled(cfg: Any) -> bool:
    """Global host apply or bounded trial (global flag stays off during trial)."""
    if getattr(cfg, "corps_llm_repair_host_apply_enabled", False):
        return True
    if getattr(cfg, "corps_llm_repair_host_apply_trial_enabled", False):
        return True
    return False


def write_semantic_regen_pack(
    vault_root: Path,
    trinity_id: str,
    markdown: str,
    *,
    timestamp: str | None = None,
) -> Path:
    """Persist pack markdown under ``.technical/weave/semantic-regen-packs/``."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    ts = timestamp or _stamp()
    out_dir = vault_root / PACK_DIR_REL
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{tid}-{ts}.md"
    path.write_text(markdown, encoding="utf-8")
    return path


def write_semantic_regen_pack_json(
    vault_root: Path,
    trinity_id: str,
    *,
    pack_md_path: Path,
    write_scope: str = "conceptual_only",
    timestamp: str | None = None,
) -> Path:
    """Machine-readable sidecar for Task/host apply."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    ts = timestamp or pack_md_path.stem.split("-")[-1] if "-" in pack_md_path.stem else _stamp()
    path = pack_md_path.with_suffix(".json")
    payload = {
        "trinity_id": tid,
        "timestamp": ts,
        "write_scope": write_scope,
        "forbidden": list(FORBIDDEN_HOST_APPLY),
        "pack_md": str(pack_md_path.relative_to(vault_root)),
        "provisional_tier_only": True,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def parse_conceptual_yaml_from_text(text: str) -> dict[str, Any] | None:
    """Extract conceptual mapping from agent stdout (fenced YAML blocks)."""
    for m in _YAML_FENCE.finditer(text):
        try:
            data = yaml.safe_load(m.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        if "conceptual" in data and isinstance(data["conceptual"], dict):
            return dict(data["conceptual"])
        if any(k in data for k in REQUIRED_CONCEPTUAL_FIELDS):
            return dict(data)
    return None


def validate_conceptual_patch(patch: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate proposed conceptual block before write."""
    issues: list[str] = []
    for field in REQUIRED_CONCEPTUAL_FIELDS:
        if not str(patch.get(field) or "").strip():
            issues.append(f"conceptual.{field} empty")
    probe = {"conceptual": patch}
    if conceptual_has_machine_voice(probe):
        issues.append("machine_voice_detected")
    if conceptual_has_meta_contamination(probe):
        issues.append("meta_contamination_detected")
    return len(issues) == 0, issues


def build_semantic_host_apply_handoff(
    vault_root: Path,
    trinity_id: str,
    *,
    pack_path: Path,
    card_path: Path,
) -> str:
    return (
        f"You are Trinity **10c-B semantic repair** (host apply from regen pack).\n\n"
        f"Vault root: `{vault_root}`\n"
        f"Trinity id: `{trinity_id}`\n"
        f"Provisional card path: `{card_path}`\n"
        f"Regen pack: `{pack_path}`\n\n"
        "**Task:** Read the regen pack. Edit **only** the `conceptual:` block in the "
        "provisional YAML at the card path above.\n\n"
        "**Hard stops:** Do NOT change `touch`, `rules`, `contract`, or `meta`. "
        "Do NOT promote to locked/components. Do NOT delete the card.\n\n"
        "Follow the pack STRICT STYLE (outcome = claim, summary = principle, "
        "primary_case = user story; no meta-framework words).\n\n"
        "**YAML safety:** Quote any scalar containing `:` with double quotes.\n\n"
        "After editing the file on disk, respond with **only** a fenced ```yaml block "
        "containing the `conceptual:` mapping you applied (for audit).\n"
    )


def apply_conceptual_patch_to_card(
    vault_root: Path,
    trinity_id: str,
    conceptual_patch: dict[str, Any],
    *,
    dry_run: bool = False,
    operator_override: bool = False,
) -> dict[str, Any]:
    """Merge validated conceptual patch into provisional card."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    rec: dict[str, Any] = {"trinity_id": tid, "changed": False}
    ok, issues = validate_conceptual_patch(conceptual_patch)
    if not ok:
        rec["validation_ok"] = False
        rec["validation_issues"] = issues
        return rec

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError) as e:
        rec["error"] = str(e)
        return rec

    before = get_conceptual(card)
    working = copy.deepcopy(card)
    new_conceptual = dict(get_conceptual(working))
    for key, val in conceptual_patch.items():
        if key in ("outcome", "summary", "primary_case", "edge_cases", "misread_risks", "frame_anchor"):
            new_conceptual[key] = val
    for key in ("spine_ordinal", "set", "operator_memory_hook", "refs", "pairs_with", "polar_pair"):
        if before.get(key) is not None and key not in new_conceptual:
            new_conceptual[key] = before[key]
    working["conceptual"] = new_conceptual

    if dry_run:
        rec["validation_ok"] = True
        rec["would_change"] = new_conceptual != before
        return rec

    try:
        write_trinity_card(
            vault_root,
            tid,
            working,
            tier="provisional",
            operator_override=operator_override,
        )
        rec["changed"] = new_conceptual != before
        rec["validation_ok"] = True
    except (OSError, ValueError) as e:
        rec["error"] = str(e)
    return rec


def invoke_host_apply_agent(
    vault_root: Path,
    trinity_id: str,
    *,
    pack_path: Path,
    timeout_sec: int = 300,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run ``agent -p --force`` with regen pack hand-off."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    rec: dict[str, Any] = {"trinity_id": tid, "phase": "semantic_host_apply_10c"}

    if dry_run:
        rec["dry_run"] = True
        rec["skipped"] = "dry_run"
        return rec

    try:
        card_path, tier = resolve_trinity_card_path(vault_root, tid, prefer="provisional")
    except FileNotFoundError as e:
        rec["error"] = str(e)
        return rec

    if tier != "provisional":
        rec["error"] = "not_provisional"
        return rec

    handoff = build_semantic_host_apply_handoff(
        vault_root, tid, pack_path=pack_path, card_path=card_path
    )
    cli = find_agent_cli()
    if not cli:
        rec["error"] = "cursor_or_agent_cli_not_found"
        return rec

    log_dir = vault_root / ".technical/weave/validation/host-apply-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{tid}-{_stamp()}.log"
    cmd = [*cli, "-p", "--force", "--model", "auto", handoff]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(vault_root / "scripts")

    before_conceptual = get_conceptual(load_trinity_card(vault_root, tid, prefer="provisional"))

    try:
        with log_path.open("w", encoding="utf-8") as logf:
            logf.write(f"# semantic host apply trinity_id={tid}\n")
            r = subprocess.run(
                cmd,
                cwd=str(vault_root),
                stdout=logf,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout_sec,
                env=env,
            )
        raw = log_path.read_text(encoding="utf-8", errors="replace")
        rec["exit_code"] = r.returncode
        rec["log_path"] = str(log_path.relative_to(vault_root))
        rec["implementation_path"] = "agent_p"
    except subprocess.TimeoutExpired:
        rec["error"] = "agent_timeout"
        rec["log_path"] = str(log_path.relative_to(vault_root))
        return rec
    except OSError as e:
        rec["error"] = str(e)
        return rec

    try:
        after_card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, yaml.YAMLError) as e:
        rec["error"] = f"post_apply_load_failed: {e}"
        rec["changed"] = False
        rec["ok"] = False
        return rec

    after_conceptual = get_conceptual(after_card)
    file_changed = after_conceptual != before_conceptual
    rec["file_changed"] = file_changed

    parsed = parse_conceptual_yaml_from_text(raw)
    if parsed and not file_changed:
        apply_rec = apply_conceptual_patch_to_card(vault_root, tid, parsed, dry_run=False)
        rec["stdout_apply"] = apply_rec
        rec["changed"] = bool(apply_rec.get("changed"))
    else:
        rec["changed"] = file_changed
        if file_changed:
            ok, issues = validate_conceptual_patch(after_conceptual)
            rec["validation_ok"] = ok
            if not ok:
                rec["validation_issues"] = issues

    rec["ok"] = bool(rec.get("changed")) and rec.get("validation_ok", True) is not False
    return rec


def apply_semantic_regen_pack(
    vault_root: Path,
    trinity_id: str,
    *,
    pack_path: Path | None = None,
    pack_md: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Apply conceptual regen pack via host agent (10c-B)."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    cfg = load_trinity_config(vault_root)
    rec: dict[str, Any] = {
        "trinity_id": tid,
        "phase": "semantic_regen_apply_10c",
        "changed": False,
    }

    if not semantic_host_apply_enabled(cfg):
        rec["skipped"] = True
        rec["reason"] = "corps_llm_repair_host_apply_disabled"
        return rec

    if pack_path is None and pack_md:
        pack_path = write_semantic_regen_pack(vault_root, tid, pack_md)
    if pack_path is None or not pack_path.is_file():
        rec["error"] = "pack_missing"
        return rec

    timeout = int(getattr(cfg, "corps_llm_repair_host_apply_timeout_sec", 300))
    host_rec = invoke_host_apply_agent(
        vault_root, tid, pack_path=pack_path, timeout_sec=timeout, dry_run=dry_run
    )
    rec["host_apply"] = host_rec
    rec["changed"] = bool(host_rec.get("changed"))
    rec["pack_path"] = str(pack_path.relative_to(vault_root))

    if not dry_run and rec.get("changed"):
        append_corps_repair_audit(
            vault_root,
            {
                "event": "semantic_regen_apply_10c",
                "trinity_id": tid,
                "at": _now_iso(),
                "pack_path": rec["pack_path"],
                "log_path": host_rec.get("log_path"),
                "validation_ok": host_rec.get("validation_ok", True),
            },
        )
        append_metric_row(
            vault_root,
            {
                "metric_type": "llm_patch_host_applied",
                "trinity_id": tid,
                "validation_ok": host_rec.get("validation_ok", True),
            },
        )

    return rec


def trial_weaken_backup_path(vault_root: Path, trinity_id: str) -> Path:
    return vault_root / TRIAL_BACKUP_DIR_REL / f"{trinity_id}-conceptual.json"


def weaken_conceptual_for_trial(
    vault_root: Path,
    trinity_id: str,
    *,
    mode: str = "empty_primary_case",
) -> dict[str, Any]:
    """Intentionally break T1 semantic for trial — backs up conceptual first."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    rec: dict[str, Any] = {"trinity_id": tid, "weakened": False}

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError) as e:
        rec["error"] = str(e)
        return rec

    backup_path = trial_weaken_backup_path(vault_root, tid)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    conceptual = get_conceptual(card)
    backup_path.write_text(json.dumps(conceptual, indent=2) + "\n", encoding="utf-8")
    rec["backup_path"] = str(backup_path.relative_to(vault_root))

    working = copy.deepcopy(card)
    c = dict(get_conceptual(working))
    if mode == "meta_contamination":
        c["summary"] = (
            "This card explains the Trinity weave segment and primary paths for the LLM agent."
        )
        c["primary_case"] = "The operator reads the conceptual leg to understand blast radius."
    else:
        c["primary_case"] = ""
    working["conceptual"] = c
    write_trinity_card(
        vault_root,
        tid,
        working,
        tier="provisional",
        mutation_action="corps_semantic_trial_weaken",
        operator_override=True,
    )
    rec["weakened"] = True
    rec["mode"] = mode
    return rec


def restore_conceptual_from_trial_backup(
    vault_root: Path,
    trinity_id: str,
) -> dict[str, Any]:
    """Restore conceptual from trial backup if present."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    backup_path = trial_weaken_backup_path(vault_root, tid)
    rec: dict[str, Any] = {"trinity_id": tid, "restored": False}
    if not backup_path.is_file():
        rec["skipped"] = "no_backup"
        return rec
    try:
        conceptual = json.loads(backup_path.read_text(encoding="utf-8"))
        try:
            card = load_trinity_card(vault_root, tid, prefer="provisional")
            working = copy.deepcopy(card)
        except (OSError, ValueError, yaml.YAMLError):
            source = load_trinity_card(vault_root, "harness_snapshot", prefer="provisional")
            working = copy.deepcopy(source)
            working["id"] = tid
            rec["restored_via"] = "backup_on_corrupt_rebuild"
        working["conceptual"] = conceptual
        write_trinity_card(
            vault_root,
            tid,
            working,
            tier="provisional",
            mutation_action="corps_semantic_trial_restore",
            operator_override=True,
        )
        rec["restored"] = True
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as e:
        rec["error"] = str(e)
    return rec


def ensure_semantic_trial_fixture(
    vault_root: Path,
    *,
    source_id: str = "harness_snapshot",
    fixture_id: str = "harness_llm_repair_trial",
) -> dict[str, Any]:
    """Clone a harness card as dedicated 10c trial fixture (semantic-weak)."""
    vault_root = vault_root.resolve()
    rec: dict[str, Any] = {"fixture_id": fixture_id, "source_id": source_id}
    try:
        source = load_trinity_card(vault_root, source_id, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError) as e:
        rec["error"] = str(e)
        return rec

    fixture = copy.deepcopy(source)
    fixture["id"] = fixture_id
    meta = dict(fixture.get("meta") or {})
    meta["provisional"] = True
    meta["trial_fixture"] = "10c_semantic"
    fixture["meta"] = meta
    c = dict(get_conceptual(fixture))
    c["primary_case"] = ""
    c["summary"] = "Backward extrapolation stub — trial fixture awaiting 10c-B host apply."
    fixture["conceptual"] = c
    write_trinity_card(
        vault_root,
        fixture_id,
        fixture,
        tier="provisional",
        mutation_action="corps_semantic_trial_fixture",
        operator_override=True,
    )
    rec["created"] = True
    weaken = weaken_conceptual_for_trial(vault_root, fixture_id, mode="empty_primary_case")
    rec["weaken"] = weaken
    return rec
