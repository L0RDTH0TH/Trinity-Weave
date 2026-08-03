"""Data-driven thin L5 moment floor (not hardcoded-only gate lists)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog_io import load_yaml, user_story_paths

_DEFAULT = {
    "min_moments": 4,
    "row_ids": [
        "ux_combat_play_surface",
        "ux_collaborative_table_agency",
        "ux_player_character_creation",
        "ux_mental_stat_interpretation",
    ],
}


def thin_parents_template_path(vault_root: Path) -> Path:
    return vault_root / "Templates" / "Roadmap" / "User-Story" / "l5-thin-parents.yaml"


def thin_parents_project_path(vault_root: Path, project_id: str) -> Path:
    paths = user_story_paths(vault_root, project_id)
    return paths["scopes_dir"].parent / "l5-thin-parents.yaml"


def load_thin_l5_moment_floor(vault_root: Path, project_id: str) -> dict[str, Any]:
    """Merge template defaults with optional project overlay."""
    vault_root = vault_root.resolve()
    merged = {
        "min_moments": int(_DEFAULT["min_moments"]),
        "row_ids": list(_DEFAULT["row_ids"]),
    }
    for path in (
        thin_parents_template_path(vault_root),
        thin_parents_project_path(vault_root, project_id),
    ):
        if not path.is_file():
            continue
        doc = load_yaml(path)
        floor = doc.get("thin_l5_moment_floor") if isinstance(doc, dict) else None
        if not isinstance(floor, dict):
            continue
        if floor.get("min_moments") is not None:
            try:
                merged["min_moments"] = max(1, int(floor["min_moments"]))
            except (TypeError, ValueError):
                pass
        ids = floor.get("row_ids")
        if isinstance(ids, list) and ids:
            merged["row_ids"] = [str(x).strip() for x in ids if str(x).strip()]
    try:
        from .ux_mint_backlog import load_mint_backlog

        bl = load_mint_backlog(vault_root, project_id)
        fm_ids = bl.get("thin_l5_moment_floor_row_ids")
        if isinstance(fm_ids, list) and fm_ids:
            merged["row_ids"] = [str(x).strip() for x in fm_ids if str(x).strip()]
        if bl.get("thin_l5_min_moments") is not None:
            merged["min_moments"] = max(1, int(bl["thin_l5_min_moments"]))
    except Exception:
        pass
    return merged


def is_thin_l5_parent(vault_root: Path, project_id: str, row_id: str) -> bool:
    floor = load_thin_l5_moment_floor(vault_root, project_id)
    return str(row_id).strip() in set(floor.get("row_ids") or [])


def thin_min_moments(vault_root: Path, project_id: str, row_id: str) -> int:
    floor = load_thin_l5_moment_floor(vault_root, project_id)
    if str(row_id).strip() not in set(floor.get("row_ids") or []):
        return 0
    return int(floor.get("min_moments") or 4)
