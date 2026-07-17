"""Update current_depth on slice-depth-budget after Trinity/factory weld."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog_io import load_json, save_json, user_story_paths
from .work_order_translate import FEED_VAULT_ROADMAP


def bump_row_current_depth(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    new_depth: int,
) -> dict[str, Any]:
    """Set current_depth for row_id in slice-depth-budget.json."""
    vault_root = vault_root.resolve()
    path = user_story_paths(vault_root, project_id)["budget"]
    if not path.is_file():
        return {"ok": False, "detail": "budget_missing", "path": str(path)}

    budget = load_json(path)
    rows = budget.get("rows") or []
    if not isinstance(rows, list):
        return {"ok": False, "detail": "budget_rows_invalid"}

    updated = False
    for row in rows:
        if isinstance(row, dict) and str(row.get("row_id")) == row_id:
            row["current_depth"] = int(new_depth)
            updated = True
            break

    if not updated:
        return {"ok": False, "detail": f"row_not_found:{row_id}"}

    budget["schema_version"] = budget.get("schema_version") or 1
    save_json(path, budget)
    return {
        "ok": True,
        "path": str(path.relative_to(vault_root)),
        "row_id": row_id,
        "current_depth": new_depth,
    }


def try_weld_depth_bump_after_slice(
    vault_root: Path,
    *,
    project_id: str,
    params: dict[str, Any],
    slice_id: str,
    all_lanes_done: bool,
    honesty_ok: bool,
    session_run_id: str | None = None,
    packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Bump budget current_depth when vault-feed row slice completes all lanes."""
    feed = str(params.get("feed_authority") or "")
    row_id = str(params.get("catalog_row_id") or "")
    if not row_id or not all_lanes_done or not honesty_ok:
        return {"skipped": True, "reason": "preconditions"}
    if feed != FEED_VAULT_ROADMAP and not slice_id.startswith("row_"):
        return {"skipped": True, "reason": "not_vault_feed"}

    from ..factory.playtest_gate_policy import should_block_depth_bump_same_run
    from ..factory.weld_beat_ready import playtest_exit_honestly_eligible, weld_beat_ready

    pid = str(project_id or "").strip()
    if playtest_exit_honestly_eligible(vault_root, pid):
        blocked, block_reason = should_block_depth_bump_same_run(
            vault_root,
            pid,
            session_run_id=session_run_id,
            packet=packet,
        )
        if blocked:
            return {"skipped": True, "reason": block_reason}
        beat_ok, beat_reason = weld_beat_ready(vault_root, pid, slice_id=slice_id)
        if not beat_ok:
            return {"skipped": True, "reason": beat_reason}

    target = params.get("dispatch_depth")
    if target is None:
        target = params.get("target_depth")
    if target is None:
        return {"skipped": True, "reason": "no_target_depth"}

    return bump_row_current_depth(
        vault_root,
        project_id=project_id,
        row_id=row_id,
        new_depth=int(target),
    )
