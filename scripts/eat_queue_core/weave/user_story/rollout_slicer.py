"""Operator rollout depth budget + dependency warnings."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_json, load_yaml, save_json, user_story_paths
from .beat_auto_generate import run_beat_auto_generate


@dataclass(frozen=True)
class RolloutSlicerResult:
    ok: bool
    budget_path: str
    rollout_version: int
    rows_written: int
    dependency_warnings: tuple[str, ...]
    beats: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "budget_path": self.budget_path,
            "rollout_version": self.rollout_version,
            "rows_written": self.rows_written,
            "dependency_warnings": list(self.dependency_warnings),
            "beats": self.beats,
        }


def _dependency_warnings(
    catalog_by_id: dict[str, dict[str, Any]],
    assignments: list[dict[str, Any]],
) -> list[str]:
    warnings: list[str] = []
    depth_by_row = {str(a["row_id"]): int(a["target_depth"]) for a in assignments}
    for row_id, target in depth_by_row.items():
        row = catalog_by_id.get(row_id) or {}
        deps = row.get("depends_on") or []
        if not isinstance(deps, list):
            continue
        for dep in deps:
            dep_id = str(dep.get("row_id") if isinstance(dep, dict) else dep)
            min_depth = int(dep.get("min_depth", 1) if isinstance(dep, dict) else 1)
            dep_depth = depth_by_row.get(dep_id)
            if dep_id in depth_by_row and dep_depth is not None and dep_depth < min_depth:
                warnings.append(
                    f"depends_on_warn:{row_id} needs {dep_id}>={min_depth} but assigned {dep_depth}"
                )
            if dep_id not in catalog_by_id:
                warnings.append(f"depends_on_unknown:{row_id}:{dep_id}")
    return warnings


def run_rollout_slicer(
    vault_root: Path,
    *,
    project_id: str,
    rollout_version: int | None = None,
    row_assignments: list[dict[str, Any]],
    generate_beats: bool = True,
) -> RolloutSlicerResult:
    """Persist operator depth budget; optional beat auto-gen."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    catalog_by_id = catalog_rows_by_id(catalog)
    existing = load_json(paths["budget"])

    rv = int(rollout_version if rollout_version is not None else existing.get("rollout_version") or 1)
    warnings = _dependency_warnings(catalog_by_id, row_assignments)

    rows_out: list[dict[str, Any]] = []
    for item in row_assignments:
        row_id = str(item.get("row_id") or "")
        if not row_id:
            continue
        target = int(item.get("target_depth") or 0)
        prior = 0
        for old in existing.get("rows") or []:
            if isinstance(old, dict) and str(old.get("row_id")) == row_id:
                prior = int(old.get("current_depth") or 0)
                break
        rows_out.append(
            {
                "row_id": row_id,
                "target_depth": target,
                "current_depth": prior,
            }
        )

    budget = {
        "schema_version": 1,
        "rollout_version": rv,
        "rows": rows_out,
    }
    save_json(paths["budget"], budget)

    beats_result: dict[str, Any] = {"skipped": True}
    if generate_beats:
        beats_result = run_beat_auto_generate(vault_root, project_id=project_id)

    return RolloutSlicerResult(
        ok=True,
        budget_path=str(paths["budget"].relative_to(vault_root)),
        rollout_version=rv,
        rows_written=len(rows_out),
        dependency_warnings=tuple(warnings),
        beats=beats_result,
    )
