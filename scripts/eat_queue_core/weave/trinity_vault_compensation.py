"""Phase 8 — vault compensation: stamp maintenance core, deploy D tunnels, re-tier harness cards."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .governance import append_metric_row, ensure_weave_paths
from .trinity_card import get_conceptual, get_rules, normalize_card
from .trinity_card_generate import build_provisional_bridge_stub
from .trinity_card_paths import (
    component_proposals_dir,
    components_dir,
    load_trinity_card,
    write_trinity_card,
)
from .trinity_dual_lock import (
    apply_lock_kind_to_card,
    load_maintenance_core_policy,
    operator_mutation_ctx,
)
from .trinity_partition import load_maintenance_trinity_ids

CORE_FORBIDDEN_SHORT = (
    "System must not auto-mutate this maintenance-core card "
    "(operator --operator-mutation only)."
)
DUAL_LOCK_PRECEDENCE = (
    "policy: Phase 8 dual-lock — automation read/align/gate only; "
    "YAML edits operator-only; provisional bridge D must tunnel_via locked bridge B, not core A."
)

PHASE8_FORBIDDEN_STRIP_MARKERS = (
    "System automation MUST NOT",
    "Provisional bridge tunnels (D)",
    "Corps cards MUST NOT",
    "System MUST NOT write maintenance-core",
    "Upgrade integration work MUST",
    "Provisional upgrade tunnels",
    "System must not auto-mutate this maintenance-core",
)

BRIDGE_DOCTRINE: dict[str, dict[str, Any]] = {
    "trinity_spine_maintenance": {
        "conceptual_append": (
            " **Dual-lock (Phase 8):** This card is bridge **B** between frozen core **A** "
            "(maintenance components) and corps **C** (provisionals). "
            "New harness wiring lives on provisional bridge **D** with `tunnel_via: trinity_spine_maintenance` — "
            "never direct `tunnel_via` on core **A**. "
            "`TRINITY_SPINE_CATCHUP` sweeps mutable non-core only; core is read-only for automation."
        ),
        "rules_append_precedence": (
            "Catch-up MUST NOT write maintenance-core component YAML; hash-only gate reconcile on core allowed.",
        ),
    },
    "trinity_upgrade_integration": {
        "conceptual_append": (
            " **Dual-lock (Phase 8):** Upgrade compensators and predesign load live on provisional bridge **D** "
            "with `tunnel_via: trinity_upgrade_integration` (this bridge **B**), not by editing core **A** Touch legs. "
            "Operator owns Conceptual on core targets; corps curates D Touch/Rules only."
        ),
        "rules_append_precedence": (
            "Upgrade integration MUST tunnel via this bridge (B) — no direct corps mutation of core component cards.",
        ),
    },
}

PHASE8_D_STUBS: tuple[dict[str, Any], ...] = (
    {
        "trinity_id": "catchup_corpus_tunnel",
        "tunnel_via": "trinity_spine_maintenance",
        "outcome": (
            "Provisional bridge D for catch-up / corpus harness paths; "
            "tunnels via trinity_spine_maintenance (B) without editing core A YAML."
        ),
        "primary_paths": [
            "scripts/eat_queue_core/weave/trinity_catchup_sweep.py",
            "scripts/eat_queue_core/harness.py",
        ],
    },
    {
        "trinity_id": "upgrade_compensator_tunnel",
        "tunnel_via": "trinity_upgrade_integration",
        "outcome": (
            "Provisional bridge D for upgrade compensator / predesign wiring; "
            "tunnels via trinity_upgrade_integration (B) without editing core A YAML."
        ),
        "primary_paths": [
            "scripts/eat_queue_core/weave/trinity_boundary_audit.py",
            "scripts/eat_queue_core/weave/trinity_bridge_consolidate.py",
        ],
    },
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _append_unique_lines(existing: list[Any], lines: tuple[str, ...]) -> list[str]:
    out = [str(x).strip() for x in existing if str(x).strip()]
    seen = set(out)
    for line in lines:
        if line not in seen:
            out.append(line)
            seen.add(line)
    return out


def _strip_phase8_forbidden(forbidden: list[Any]) -> list[str]:
    out: list[str] = []
    for raw in forbidden:
        s = str(raw).strip()
        if not s:
            continue
        if any(m in s for m in PHASE8_FORBIDDEN_STRIP_MARKERS):
            continue
        out.append(s)
    return out


def _touch_guard_test_count(card: dict[str, Any]) -> int:
    from .trinity_card import get_touch

    touch = get_touch(card)
    signals = touch.get("behavior_signals") or []
    return sum(1 for s in signals if str(s).strip().startswith("test_"))


def stamp_maintenance_core_card(
    card: dict[str, Any],
    *,
    trinity_id: str,
    now_iso: str | None = None,
    apply_bridge_doctrine: bool = True,
) -> dict[str, Any]:
    """Apply maintenance_core meta + dual-lock doctrine (forbidden if room, else precedence)."""
    now = now_iso or _now_iso()
    out = apply_lock_kind_to_card(card, "maintenance_core", now_iso=now)
    rules = out.setdefault("rules", {})
    if not isinstance(rules, dict):
        rules = {}
        out["rules"] = rules

    forbidden = _strip_phase8_forbidden(list(rules.get("forbidden") or []))
    precedence = _append_unique_lines(
        list(rules.get("precedence") or []),
        (DUAL_LOCK_PRECEDENCE,),
    )
    tests = _touch_guard_test_count(out)
    if tests > 0 and len(forbidden) < tests:
        forbidden = _append_unique_lines(forbidden, (CORE_FORBIDDEN_SHORT,))
    rules["forbidden"] = forbidden
    rules["precedence"] = precedence

    if apply_bridge_doctrine and trinity_id in BRIDGE_DOCTRINE:
        doc = BRIDGE_DOCTRINE[trinity_id]
        conc = out.setdefault("conceptual", {})
        if not isinstance(conc, dict):
            conc = {}
            out["conceptual"] = conc
        summary = str(conc.get("summary") or "").strip()
        append = doc["conceptual_append"]
        if append.strip() not in summary:
            conc["summary"] = (summary + append).strip()
        rules["precedence"] = _append_unique_lines(
            list(rules.get("precedence") or []),
            tuple(doc.get("rules_append_precedence") or ()),
        )
    return normalize_card(out)


def run_trinity_stamp_core_cards(
    vault_root: Path,
    *,
    trinity_ids: list[str] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Stamp all maintenance core YAMLs with lock_kind + system_mutable false."""
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    policy = load_maintenance_core_policy(vault_root)
    ids = trinity_ids or sorted(policy.ids)
    now = _now_iso()
    stamped: list[str] = []
    missing: list[str] = []
    errors: list[dict[str, str]] = []

    token = operator_mutation_ctx.set(True)
    try:
        for tid in ids:
            path = components_dir(vault_root) / f"{tid}.yaml"
            if not path.is_file():
                missing.append(tid)
                continue
            try:
                card = load_trinity_card(vault_root, tid, prefer="locked")
                updated = stamp_maintenance_core_card(
                    card, trinity_id=tid, now_iso=now
                )
                if dry_run:
                    stamped.append(tid)
                    continue
                write_trinity_card(
                    vault_root,
                    tid,
                    updated,
                    tier="locked",
                    mutation_action="stamp_maintenance_core",
                    operator_override=True,
                )
                stamped.append(tid)
            except (OSError, ValueError) as e:
                errors.append({"trinity_id": tid, "error": str(e)})
    finally:
        operator_mutation_ctx.reset(token)

    ok = not missing and not errors
    report = {
        "ok": ok,
        "dry_run": dry_run,
        "stamped": stamped,
        "missing": missing,
        "errors": errors,
        "count": len(stamped),
        "expected": len(ids),
    }
    if not dry_run and stamped:
        append_metric_row(
            vault_root,
            {
                "metric_type": "trinity_stamp_core_cards",
                "ok": ok,
                "count": len(stamped),
            },
        )
    return report


def deploy_phase8_bridge_stubs(
    vault_root: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    """Write provisional D stubs tunnel_via bridge B (not core A)."""
    vault_root = vault_root.resolve()
    prop_dir = component_proposals_dir(vault_root)
    prop_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    skipped: list[str] = []

    for spec in PHASE8_D_STUBS:
        tid = str(spec["trinity_id"])
        dest = prop_dir / f"{tid}.yaml"
        if dest.is_file() and not force:
            skipped.append(tid)
            continue
        card = build_provisional_bridge_stub(
            tid,
            tunnel_via=str(spec["tunnel_via"]),
            outcome=str(spec["outcome"]),
        )
        touch = card.setdefault("touch", {})
        if isinstance(touch, dict):
            paths = spec.get("primary_paths") or []
            touch["primary_paths"] = list(paths)
        meta = card.setdefault("meta", {})
        if isinstance(meta, dict):
            meta["phase8_deployed"] = True
            meta["deployed_at"] = _now_iso()
        if dry_run:
            written.append(tid)
            continue
        import yaml  # type: ignore[import-untyped]

        dest.write_text(
            yaml.dump(normalize_card(card), sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        written.append(tid)

    return {
        "ok": True,
        "dry_run": dry_run,
        "written": written,
        "skipped": skipped,
    }


def retier_harness_cards_to_proposals(
    vault_root: Path,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Move harness_* from components/ → component-proposals/ (not maintenance core)."""
    vault_root = vault_root.resolve()
    policy = load_maintenance_core_policy(vault_root)
    comp = components_dir(vault_root)
    prop = component_proposals_dir(vault_root)
    prop.mkdir(parents=True, exist_ok=True)
    moved: list[str] = []
    skipped: list[str] = []

    for path in sorted(comp.glob("harness_*.yaml")):
        tid = path.stem
        if tid in policy.ids:
            skipped.append(tid)
            continue
        dest = prop / path.name
        if dry_run:
            moved.append(tid)
            continue
        if dest.is_file():
            dest.unlink()
        shutil.move(str(path), str(dest))
        try:
            card = load_trinity_card(vault_root, tid, prefer="provisional")
            meta = card.setdefault("meta", {})
            if isinstance(meta, dict):
                meta["provisional"] = True
                meta["promotion_tier"] = "provisional"
                meta["card_class"] = "promoted_provisional"
                meta["retiered_from"] = "components"
                meta["retiered_at"] = _now_iso()
                meta.pop("lock_kind", None)
                meta.pop("system_mutable", None)
            import yaml  # type: ignore[import-untyped]

            dest.write_text(
                yaml.dump(normalize_card(card), sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
        except (OSError, ValueError):
            pass
        moved.append(tid)

    return {"ok": True, "dry_run": dry_run, "moved": moved, "skipped": skipped}


def write_provisional_bridge_template(vault_root: Path) -> Path:
    """Refresh A/B/C/D template with tunnel_via → bridge B."""
    vault_root = vault_root.resolve()
    tpl_dir = vault_root / ".technical" / "weave" / "templates"
    tpl_dir.mkdir(parents=True, exist_ok=True)
    path = tpl_dir / "trinity-provisional-bridge.yaml"
    content = """# Provisional bridge stub (Phase 8 — D tunnels via B, not core A)
#
# A = maintenance core component (frozen, operator-only)
# B = locked bridge (e.g. trinity_spine_maintenance, trinity_upgrade_integration)
# C = corps target the bridge already serves (provisionals, corpus)
# D = this card — new harness wiring; maintenance corps may curate Touch/Rules
#
# WRONG: tunnel_via: lane_status_board  (direct core A)
# RIGHT: tunnel_via: trinity_spine_maintenance  (bridge B)

id: example_bridge_D_via_B
meta:
  anatomy: bridge
  provisional: true
  promotion_tier: provisional
  card_class: provisional_bridge
  schema_version: "1"
touch:
  bridge_scope: true
  tunnel_via: trinity_spine_maintenance
  pairs_with:
    - trinity_spine_maintenance
  primary_paths: []
conceptual:
  outcome: "Bridge D piggybacks on locked bridge B to reach core A read-only"
  summary: "Do not set tunnel_via to a maintenance-core component id (A)"
rules:
  forbidden:
    - "Do not mutate maintenance-core component YAML from this bridge card"
    - "Do not set tunnel_via or pairs_with to maintenance-core component ids (A)"
  precedence: []
  acceptance: []
"""
    path.write_text(content, encoding="utf-8")
    return path


def run_phase8_vault_compensation(
    vault_root: Path,
    *,
    dry_run: bool = False,
    skip_touch_refresh: bool = False,
    skip_board_smoke: bool = False,
) -> dict[str, Any]:
    """Full Phase 8 pass: stamp, stubs, retier, template, touch refresh, board smoke."""
    vault_root = vault_root.resolve()
    out: dict[str, Any] = {"ok": True, "phase": 8, "dry_run": dry_run}

    out["stamp"] = run_trinity_stamp_core_cards(vault_root, dry_run=dry_run)
    out["bridge_stubs"] = deploy_phase8_bridge_stubs(vault_root, dry_run=dry_run)
    out["harness_retier"] = retier_harness_cards_to_proposals(
        vault_root, dry_run=dry_run
    )
    if not dry_run:
        tpl = write_provisional_bridge_template(vault_root)
        out["template_path"] = str(tpl.relative_to(vault_root))
    else:
        out["template_path"] = ".technical/weave/templates/trinity-provisional-bridge.yaml"

    if dry_run or skip_touch_refresh:
        out["touch_refresh"] = {"skipped": True, "reason": "dry_run or skip_touch_refresh"}
    else:
        from .trinity_touch_refresh import run_trinity_touch_refresh

        bundle = load_maintenance_trinity_ids(vault_root)
        token = operator_mutation_ctx.set(True)
        try:
            out["touch_refresh"] = run_trinity_touch_refresh(
                vault_root,
                trinity_ids=list(bundle.all),
                pilot_only=False,
                dry_run=False,
                apply_behavior_signals=False,
            )
        finally:
            operator_mutation_ctx.reset(token)

    if dry_run or skip_board_smoke:
        out["board_smoke"] = {"skipped": True}
    else:
        from ..lane_status_board import write_lane_status_board

        try:
            board = write_lane_status_board(vault_root)
            out["board_smoke"] = {
                "ok": board.get("ok"),
                "integrity_ok": board.get("integrity_ok"),
                "trinity_align": board.get("trinity_align"),
            }
            if not board.get("integrity_ok"):
                out["ok"] = False
        except (OSError, ValueError) as e:
            out["board_smoke"] = {"ok": False, "error": str(e)}
            out["ok"] = False

    if not dry_run:
        val_dir = vault_root / ".technical" / "weave" / "validation"
        val_dir.mkdir(parents=True, exist_ok=True)
        report_path = val_dir / f"phase8-vault-compensation-{_stamp()}.json"
        report_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        out["report_path"] = str(report_path)

    if out["stamp"].get("errors") or out["stamp"].get("missing"):
        out["ok"] = False
    return out
