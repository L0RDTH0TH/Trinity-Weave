"""Shared budget row helpers for product factory."""

from __future__ import annotations

from pathlib import Path

from .catalog_io import catalog_rows_by_id, load_json, load_yaml, user_story_paths


def budget_row_ids(vault_root: Path, project_id: str) -> list[str]:
    paths = user_story_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    ids: list[str] = []
    for row in budget.get("rows") or []:
        if isinstance(row, dict) and row.get("row_id"):
            ids.append(str(row["row_id"]))
    if ids:
        return ids
    catalog = load_yaml(paths["catalog"])
    return [rid for rid, r in catalog_rows_by_id(catalog).items() if r.get("planned")]
