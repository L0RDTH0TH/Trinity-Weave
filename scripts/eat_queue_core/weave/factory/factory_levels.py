"""Factory depth-level satisfaction — Half B overnight stop signal."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..user_story.catalog_io import load_json, user_story_paths
from ..user_story.playtest_manual_gate import playtest_manual_gate_matched
from ..user_story.product_factory_state import FACTORY_CELL_COMPLETE, load_product_factory


def factory_levels_satisfied(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """
    True when every slice-depth-budget row has current_depth >= target_depth.

    Weld receipt on budget rows — not an authoring control.
    """
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    rows = budget.get("rows") or []
    if not rows:
        return False, "no_budget_rows"

    incomplete: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        rid = str(row.get("row_id") or "")
        target = int(row.get("target_depth") or 0)
        current = int(row.get("current_depth") or 0)
        if not rid:
            continue
        if target <= 0:
            incomplete.append(f"{rid}:no_target_depth")
        elif current < target:
            incomplete.append(f"{rid}:d{current}<t{target}")

    if incomplete:
        return False, ";".join(incomplete[:8])
    return True, "all_budget_rows_at_target_depth"


def factory_done_when_matched(
    vault_root: Path,
    packet: dict[str, Any],
    *,
    project_id: str | None = None,
) -> tuple[bool, str]:
    """Match goal packet done_when strings for implementation factory overnight."""
    vault_root = vault_root.resolve()
    pid = project_id or str(packet.get("project_id") or "")
    criteria = packet.get("done_when") or []
    if not isinstance(criteria, list):
        return False, ""

    for raw in criteria:
        key = str(raw or "").strip().lower().replace(" ", "_")
        if not key:
            continue
        if key in ("all_budget_rows_at_target_depth", "factory_levels_satisfied"):
            ok, _reason = factory_levels_satisfied(vault_root, pid)
            if ok:
                return True, key
        if key in ("factory_cell_complete", "cell_complete"):
            pf = load_product_factory(vault_root, pid)
            completed = pf.get("completed_phases") or []
            if FACTORY_CELL_COMPLETE in completed:
                return True, key
            cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
            if str(cell.get("phase") or "") == "cell_complete":
                return True, key
        matched, match_reason = playtest_manual_gate_matched(
            vault_root, packet, project_id=pid
        )
        if matched and key in (
            "playtest_manual_gate",
            "playtest_gate",
            "operator_playtest_pending",
            "playtest_pending_sign_off",
        ):
            return True, match_reason or key

    return False, ""


def implementation_factory_overnight(packet: dict[str, Any]) -> bool:
    """Half B overnight — implementation track without roadmap implementation_gate stop."""
    from ...architect_pq_planner import implementation_track_active

    return implementation_track_active(packet)
