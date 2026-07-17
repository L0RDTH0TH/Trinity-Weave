"""Depth slicer harness — L5 complete vision → L4..L1 scope files (top-down)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .depth_scope import slice_all_catalog_rows, slice_l5_to_levels


@dataclass(frozen=True)
class DepthSlicerResult:
    ok: bool
    row_id: str | None
    written: tuple[str, ...]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "row_id": self.row_id,
            "written": list(self.written),
            "detail": self.detail,
        }


def run_depth_slicer(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str | None = None,
    row_ids: list[str] | None = None,
    bootstrap_l5: bool = True,
) -> dict[str, Any]:
    """Slice L5 into level scopes for one row or many."""
    vault_root = vault_root.resolve()
    if row_id:
        out = slice_l5_to_levels(
            vault_root, project_id=project_id, row_id=row_id, bootstrap=bootstrap_l5
        )
        return out
    return slice_all_catalog_rows(vault_root, project_id=project_id, row_ids=row_ids)
