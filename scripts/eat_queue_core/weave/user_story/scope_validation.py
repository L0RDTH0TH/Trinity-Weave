"""Loop 2 operator scope level attestation (L5 down through target_depth)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .user_story_feedback import (
    load_user_story_feedback,
    row_scope_files_missing,
    row_target_depth,
    save_user_story_feedback,
    scope_levels_for_validation,
)


@dataclass(frozen=True)
class ScopeValidationResult:
    ok: bool
    row_id: str
    target_depth: int
    levels_attested: list[int]
    missing_scope_files: list[int]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "row_id": self.row_id,
            "target_depth": self.target_depth,
            "levels_attested": self.levels_attested,
            "missing_scope_files": self.missing_scope_files,
            "detail": self.detail,
        }


def list_scope_validation_status(
    vault_root: Path,
    *,
    project_id: str,
    row_ids: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Per-row scope attestation status for operator review."""
    from .product_factory_budget import budget_row_ids

    ids = row_ids or budget_row_ids(vault_root, project_id)
    by_id = {r.row_id: r for r in load_user_story_feedback(vault_root, project_id)}
    out: list[dict[str, Any]] = []
    for rid in ids:
        td = row_target_depth(vault_root, project_id, rid)
        missing = row_scope_files_missing(vault_root, project_id, rid, target_depth=td)
        row = by_id.get(rid)
        out.append(
            {
                "row_id": rid,
                "target_depth": td,
                "levels_required": scope_levels_for_validation(td),
                "scopes_validated": bool(row and row.scopes_validated),
                "missing_scope_files": missing,
                "ready_for_attestation": not missing,
            }
        )
    return out


def confirm_scopes_validated(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    notes: str = "",
) -> ScopeValidationResult:
    """Operator attests L5..target_depth scope files match intent (loop 2)."""
    td = row_target_depth(vault_root, project_id, row_id)
    missing = row_scope_files_missing(vault_root, project_id, row_id, target_depth=td)
    levels = scope_levels_for_validation(td)
    if missing:
        return ScopeValidationResult(
            False,
            row_id,
            td,
            levels,
            missing,
            f"missing_scope_files:{missing}",
        )

    rows = [r.to_dict() for r in load_user_story_feedback(vault_root, project_id)]
    found = False
    for row in rows:
        if str(row.get("row_id")) == row_id:
            row["scopes_validated"] = True
            row["source"] = "operator"
            if notes:
                row["notes"] = notes
            found = True
            break
    if not found:
        rows.append(
            {
                "row_id": row_id,
                "beat_ref": "",
                "experiential_pass": None,
                "operator_confirmed": False,
                "scopes_validated": True,
                "notes": notes,
                "source": "operator",
            }
        )
    save_user_story_feedback(vault_root, project_id, rows)
    return ScopeValidationResult(
        True,
        row_id,
        td,
        levels,
        [],
        f"scopes_validated:{row_id}",
    )
