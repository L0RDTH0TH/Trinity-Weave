"""Phase 10g apply — bounded deterministic test repair after conduct repair pack.

Pack builder (10g) writes the hand-off; this module applies proof-path-only fixes
without editing card YAML. Config-gated (default off); re-runs behavior proofs after.
"""

from __future__ import annotations

import os
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .corps_repair_audit import append_corps_repair_audit
from .trinity_behavior_proof import run_card_behavior_proofs
from .trinity_card import get_touch
from .trinity_card_paths import load_trinity_card
from .trinity_provisional_corps_sweep import _wire_tests_if_missing

_IMPORT_ERR_RE = re.compile(
    r"(?:ModuleNotFoundError|ImportError):\s*No module named ['\"]([^'\"]+)['\"]",
    re.IGNORECASE,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_conduct_repair_pack_json(
    vault_root: Path,
    trinity_id: str,
    *,
    proof_paths: list[str],
    failed_proofs: list[dict[str, Any]],
    write_scope: str,
    pack_md_path: Path,
    timestamp: str | None = None,
) -> Path:
    """Machine-readable sidecar for Task/host or deterministic apply."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    ts = timestamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = pack_md_path.with_suffix(".json")
    payload = {
        "trinity_id": tid,
        "timestamp": ts,
        "write_scope": write_scope,
        "proof_paths": proof_paths,
        "failed_proofs": failed_proofs[:12],
        "forbidden": [
            "patch_card_yaml",
            "weaken_asserts_to_green",
            "delete_tests_to_skip",
        ],
        "pack_md": str(pack_md_path.relative_to(vault_root)),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _run_pytest(vault_root: Path, proof_rel: str) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    script = vault_root / "scripts"
    cmd = [
        "python3",
        "-m",
        "pytest",
        proof_rel,
        "-q",
        "--tb=short",
    ]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(vault_root),
            env={"PYTHONPATH": str(script), **os.environ},
            capture_output=True,
            text=True,
            timeout=120,
        )
        return {
            "proof_path": proof_rel,
            "exit_code": proc.returncode,
            "stdout": (proc.stdout or "")[-2000:],
            "stderr": (proc.stderr or "")[-4000:],
            "ok": proc.returncode == 0,
        }
    except subprocess.TimeoutExpired as e:
        return {
            "proof_path": proof_rel,
            "exit_code": -1,
            "stderr": str(e),
            "ok": False,
            "timeout": True,
        }


def _module_import_from_primary(primary: str) -> str:
    rel = str(primary).strip().replace("\\", "/")
    if rel.endswith(".py"):
        rel = rel[:-3]
    return rel.replace("/", ".")


def _ensure_minimal_proof_stub(
    vault_root: Path,
    proof_rel: str,
    *,
    primary_path: str,
) -> bool:
    """Create a minimal import smoke test when proof file is missing."""
    path = vault_root / proof_rel
    if path.is_file():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    mod = _module_import_from_primary(primary_path)
    body = f'''"""Minimal conduct-repair stub (10g apply)."""

import importlib
import unittest


class TestConductRepairStub(unittest.TestCase):
    def test_target_importable(self) -> None:
        importlib.import_module("{mod}")
'''
    path.write_text(body, encoding="utf-8")
    return True


def _try_fix_import_in_test(vault_root: Path, proof_rel: str, stderr: str) -> bool:
    """One bounded import-line fix when pytest reports ModuleNotFoundError."""
    m = _IMPORT_ERR_RE.search(stderr or "")
    if not m:
        return False
    path = vault_root / proof_rel
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = m.group(1).split(".")[0]
    if f"import {missing}" in text or f"importlib.import_module" in text:
        return False
    prefix = (
        "import sys\nfrom pathlib import Path\n"
        "sys.path.insert(0, str(Path(__file__).resolve().parents[2]))\n\n"
    )
    if not text.startswith("import sys"):
        path.write_text(prefix + text, encoding="utf-8")
        return True
    return False


def conduct_apply_enabled(cfg: Any) -> bool:
    """Global auto-apply or bounded trial (global flag stays off during trial)."""
    if getattr(cfg, "corps_conduct_repair_auto_apply_enabled", False):
        return True
    if getattr(cfg, "corps_conduct_repair_auto_apply_trial_enabled", False):
        return True
    return False


def apply_conduct_repair_pack(
    vault_root: Path,
    trinity_id: str,
    *,
    pack_path: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Apply bounded proof-path repairs; card YAML remains read-only."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    rec: dict[str, Any] = {
        "trinity_id": tid,
        "phase": "conduct_repair_apply_10g",
        "applied": [],
        "changed": False,
        "proofs_ok": None,
    }

    cfg = load_trinity_config(vault_root)
    if not conduct_apply_enabled(cfg):
        rec["skipped"] = True
        rec["reason"] = "corps_conduct_repair_auto_apply_disabled"
        return rec

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError) as e:
        rec["error"] = str(e)
        return rec

    contract = card.get("contract") or {}
    proof_paths = [
        str(p).strip()
        for p in (contract.get("proof") or [])
        if str(p).strip()
    ]
    touch = get_touch(card)
    primary = (touch.get("primary_paths") or ["scripts/eat_queue_core"])[0]

    if not dry_run:
        wired = _wire_tests_if_missing(vault_root, card)
        if wired != card:
            rec["applied"].append("wire_missing_smoke_tests")

    for proof_rel in proof_paths:
        full = vault_root / proof_rel
        if not full.is_file() and not dry_run:
            if _ensure_minimal_proof_stub(vault_root, proof_rel, primary_path=str(primary)):
                from .stub_honesty import append_stub_trace, stub_trace_entry_from_repair

                append_stub_trace(
                    vault_root,
                    stub_trace_entry_from_repair(
                        proof_rel=proof_rel,
                        trinity_id=tid,
                    ),
                )
                rec["applied"].append(f"stub_created:{proof_rel}")
                rec["provisional_stub_only"] = True
                rec["conduct_repair_stub_as_complete"] = False
                rec["changed"] = True

    if dry_run:
        rec["skipped_writes"] = True
        rec["would_proof_paths"] = proof_paths
        return rec

    pytest_runs: list[dict[str, Any]] = []
    for proof_rel in proof_paths:
        run = _run_pytest(vault_root, proof_rel)
        pytest_runs.append(run)
        if not run.get("ok") and _try_fix_import_in_test(
            vault_root, proof_rel, run.get("stderr") or ""
        ):
            rec["applied"].append(f"import_path_fix:{proof_rel}")
            rec["changed"] = True
            pytest_runs.append(_run_pytest(vault_root, proof_rel))

    rec["pytest_runs"] = pytest_runs[:8]

    proofs = run_card_behavior_proofs(vault_root, card)
    failed = [p for p in proofs if not p.ok]
    rec["proof_results"] = [p.to_dict() for p in proofs]
    rec["proofs_ok"] = len(failed) == 0
    if rec.get("provisional_stub_only"):
        rec["proofs_ok"] = False
        rec["proofs_ok_reason"] = "conduct_repair_import_stub_not_structural"
    rec["proofs_failed"] = [p.test_name for p in failed][:8]

    if pack_path and pack_path.is_file():
        rec["pack_path"] = str(pack_path.relative_to(vault_root))

    if rec.get("changed") or rec.get("proofs_ok"):
        append_corps_repair_audit(
            vault_root,
            {
                "event": "conduct_repair_apply_10g",
                "trinity_id": tid,
                "at": _now_iso(),
                "applied": rec.get("applied"),
                "proofs_ok": rec.get("proofs_ok"),
                "proofs_failed": rec.get("proofs_failed"),
            },
        )

    return rec


PACK_DIR_REL = Path(".technical/weave/conduct-repair-packs")


def run_conduct_repair_apply_trial(
    vault_root: Path,
    *,
    trinity_id: str | None = None,
    max_apply: int | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Bounded 10g apply trial — scans conduct-repair packs or targets one id."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not conduct_apply_enabled(cfg):
        return {
            "ok": False,
            "error": "conduct_apply_disabled",
            "hint": "Enable trinity_corps_conduct_repair_auto_apply_trial_enabled",
        }

    cap = max_apply
    if cap is None:
        cap = int(getattr(cfg, "corps_conduct_repair_auto_apply_trial_max_per_run", 3))

    pack_dir = vault_root / PACK_DIR_REL
    targets: list[str] = []
    if trinity_id:
        targets = [str(trinity_id).strip()]
    elif pack_dir.is_dir():
        for path in sorted(pack_dir.glob("*.md"), reverse=True):
            stem = path.stem.split("-")[0]
            if stem and stem not in targets:
                targets.append(stem)
            if len(targets) >= cap:
                break

    applied: list[dict[str, Any]] = []
    for tid in targets[:cap]:
        pack_path = None
        if pack_dir.is_dir():
            matches = sorted(pack_dir.glob(f"{tid}-*.md"), reverse=True)
            if matches:
                pack_path = matches[0]
        rec = apply_conduct_repair_pack(
            vault_root,
            tid,
            pack_path=pack_path,
            dry_run=dry_run,
        )
        applied.append(rec)

    return {
        "ok": True,
        "trial": True,
        "attempted": len(applied),
        "applied": applied,
        "dry_run": dry_run,
    }
