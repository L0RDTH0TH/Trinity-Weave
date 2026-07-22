"""Sync goal-authority.json from product factory / vault_roadmap (not legacy alpha queue)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ...goal_authority_io import goal_authority_path_for_lane
from ..user_story.catalog_io import load_json, user_story_paths
from ..user_story.product_factory_state import load_product_factory


def sync_goal_authority_from_vault_feed(
    vault_root: Path,
    queue_lane: str,
    advance: dict[str, Any],
    *,
    project_id: str | None = None,
) -> dict[str, Any]:
    """
    Mirror budget row + active_slice into goal packet planner_hints.

  ``closed_alpha`` is never written as a scheduling rail — optional user_release_label only.
    """
    vault_root = vault_root.resolve()
    queue_lane = queue_lane.strip().lower()

    path = goal_authority_path_for_lane(vault_root, queue_lane)
    if not path.is_file():
        return {"ok": False, "error": "goal_authority_missing", "path": str(path)}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return {"ok": False, "error": f"goal_authority_read_failed:{e}"}

    if not isinstance(data, dict):
        return {"ok": False, "error": "goal_authority_invalid"}

    pid = project_id or str(data.get("project_id") or "genesis-mythos-master")
    pf = load_product_factory(vault_root, pid)
    active = pf.get("active_slice") if isinstance(pf.get("active_slice"), dict) else {}
    row_ids = [str(x) for x in (active.get("row_ids") or []) if x]
    if not row_ids and advance.get("catalog_row_id"):
        row_ids = [str(advance["catalog_row_id"])]
    dispatch_depth = active.get("dispatch_depth")

    budget = load_json(user_story_paths(vault_root, pid)["budget"])
    rows = budget.get("rows") or []
    by_id = {str(r.get("row_id")): r for r in rows if isinstance(r, dict) and r.get("row_id")}

    hints: dict[str, Any] = dict(data.get("planner_hints") or {})
    updated: list[str] = []

    if row_ids:
        hints["active_row_ids"] = row_ids
        hints["active_row_id"] = row_ids[0]
        updated.extend(["active_row_ids", "active_row_id"])
    if dispatch_depth is not None:
        hints["dispatch_depth"] = int(dispatch_depth)
        updated.append("dispatch_depth")

    for rid in row_ids:
        br = by_id.get(rid) or {}
        hints["target_depth"] = int(br.get("target_depth") or hints.get("target_depth") or 0)
        hints["current_depth"] = int(br.get("current_depth") or 0)
        updated.extend(["target_depth", "current_depth"])
        break

    if advance.get("loop_3_reopened"):
        hints["loop_3_reopened"] = True
        updated.append("loop_3_reopened")

    if advance.get("completed_slice") or advance.get("catalog_row_id"):
        hints["last_completed_factory_slice"] = str(
            advance.get("completed_slice") or advance.get("catalog_row_id") or ""
        )
        updated.append("last_completed_factory_slice")

    hints["feed_authority"] = "vault_roadmap"
    hints.setdefault("user_release_label", "closed_alpha")
    updated.append("feed_authority")

    for legacy_key in (
        "closed_alpha_slice",
        "closed_alpha_release_slice",
        "closed_alpha_slice1_status",
        "closed_alpha_slice2_status",
        "closed_alpha_slice3_status",
        "closed_alpha_slice4_status",
        "closed_alpha_ship_rollup_status",
        "closed_alpha_build_order_authority",
        "closed_alpha_slice_order",
        "alpha_factory_queue_ref",
        "post_alpha_focus",
    ):
        if legacy_key in hints:
            hints.pop(legacy_key, None)
            updated.append(f"removed:{legacy_key}")

    data["planner_hints"] = hints
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    return {
        "ok": True,
        "path": str(path),
        "updated_keys": sorted(set(updated)),
        "vault_feed": True,
        "advance": {k: advance.get(k) for k in ("loop_3_reopened", "catalog_row_id", "reason")},
    }


def sync_goal_authority_on_factory_advance(
    vault_root: Path,
    queue_lane: str,
    advance: dict[str, Any],
    *,
    queue_rel: str = "",
) -> dict[str, Any]:
    """Post-advance goal packet sync — vault_roadmap primary; legacy alpha queue ignored."""
    if advance.get("vault_feed"):
        return sync_goal_authority_from_vault_feed(vault_root, queue_lane, advance)

    if not advance.get("advanced"):
        return {"ok": True, "skipped": True, "reason": str(advance.get("reason") or "no_advance")}

    return {
        "ok": True,
        "skipped": True,
        "reason": "legacy_alpha_queue_deprecated_use_vault_roadmap",
        "detail": "Scheduling rail is product_factory + slice-depth-budget; alpha-factory-queue is archival",
    }
