"""Shared budget row helpers for product factory."""

from __future__ import annotations

from pathlib import Path

from .catalog_io import catalog_rows_by_id, load_json, load_yaml, user_story_paths


def budget_row_ids(vault_root: Path, project_id: str) -> list[str]:
    """Rows in scope for Loop 2 / pin wire / coverage.

    When ``release_plan_feed`` is on: active-wave package catalog rows (planner).
    Else: slice-depth-budget rows, falling back to all planned catalog rows.
    """
    from .release_plan import (
        load_release_plan,
        packages_for_wave,
        release_plan_feed_enabled,
    )

    if release_plan_feed_enabled(vault_root, project_id):
        plan = load_release_plan(vault_root, project_id)
        active = str(plan.get("active_wave") or "")
        ids: list[str] = []
        for pkg in packages_for_wave(plan, active):
            ids.extend(pkg.catalog_row_ids)
        # Preserve order, dedupe
        seen: set[str] = set()
        out: list[str] = []
        for rid in ids:
            if rid not in seen:
                seen.add(rid)
                out.append(rid)
        if out:
            return out

    paths = user_story_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    ids = []
    for row in budget.get("rows") or []:
        if isinstance(row, dict) and row.get("row_id"):
            ids.append(str(row["row_id"]))
    if ids:
        return ids
    catalog = load_yaml(paths["catalog"])
    return [rid for rid, r in catalog_rows_by_id(catalog).items() if r.get("planned")]
