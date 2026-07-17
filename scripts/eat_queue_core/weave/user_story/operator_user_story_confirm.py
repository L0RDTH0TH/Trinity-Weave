"""Operator confirm for user-story rows and catalog sign-off."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .catalog_io import parse_state_frontmatter, user_story_paths
from .user_story_feedback import load_user_story_feedback, save_user_story_feedback


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True)
class UserStoryConfirmResult:
    ok: bool
    rows_updated: int
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "rows_updated": self.rows_updated,
            "detail": self.detail,
        }


def confirm_catalog_sign(vault_root: Path, *, project_id: str) -> UserStoryConfirmResult:
    """Set catalog_signed_at on user-story-state.md (operator gate)."""
    vault_root = vault_root.resolve()
    state_path = user_story_paths(vault_root, project_id)["state"]
    if not state_path.is_file():
        return UserStoryConfirmResult(False, 0, "user_story_state_missing")

    text = state_path.read_text(encoding="utf-8")
    stamp = _utc_iso()
    if text.startswith("---"):
        end = text.find("\n---", 4)
        if end >= 0:
            fm_block = text[4:end]
            import yaml

            fm = yaml.safe_load(fm_block) or {}
            if not isinstance(fm, dict):
                fm = {}
            fm["catalog_signed_at"] = stamp
            fm["roadmap_track"] = fm.get("roadmap_track") or "user_story"
            new_fm = yaml.dump(fm, sort_keys=False, allow_unicode=True).strip()
            body = text[end + 4 :].lstrip("\n")
            state_path.write_text(f"---\n{new_fm}\n---\n\n{body}", encoding="utf-8")
            return UserStoryConfirmResult(True, 1, "catalog_signed")

    return UserStoryConfirmResult(False, 0, "invalid_state_frontmatter")


def confirm_user_story_row(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    pass_: bool,
    notes: str = "",
    operator_confirmed: bool = True,
) -> UserStoryConfirmResult:
    rows = [r.to_dict() for r in load_user_story_feedback(vault_root, project_id)]
    found = False
    for row in rows:
        if str(row.get("row_id")) == row_id:
            row["experiential_pass"] = bool(pass_)
            row["operator_confirmed"] = operator_confirmed
            if notes:
                row["notes"] = notes
            row["source"] = "operator"
            found = True
            break
    if not found:
        rows.append(
            {
                "row_id": row_id,
                "beat_ref": "",
                "experiential_pass": bool(pass_),
                "operator_confirmed": operator_confirmed,
                "notes": notes,
                "source": "operator",
            }
        )
    save_user_story_feedback(vault_root, project_id, rows)
    return UserStoryConfirmResult(True, 1, f"row_confirmed:{row_id}")


def catalog_is_signed(vault_root: Path, project_id: str) -> bool:
    state = parse_state_frontmatter(user_story_paths(vault_root, project_id)["state"])
    return bool(state.get("catalog_signed_at"))
