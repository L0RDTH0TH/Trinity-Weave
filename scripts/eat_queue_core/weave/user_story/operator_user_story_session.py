"""Post-session operator hook for user story (mirrors operator_playtest_session)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .operator_user_story_confirm import catalog_is_signed
from .user_story_brief import brief_dir
from .user_story_feedback import list_pending_user_story_confirmations
from .user_story_session_ingest import ingest_user_story_session


@dataclass(frozen=True)
class OperatorUserStorySessionResult:
    ok: bool
    ingest: dict[str, Any]
    pending: list[dict[str, Any]]
    catalog_signed: bool
    latest_brief: str | None
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "ingest": self.ingest,
            "pending": self.pending,
            "catalog_signed": self.catalog_signed,
            "latest_brief": self.latest_brief,
            "detail": self.detail,
        }


def run_operator_user_story_session(
    vault_root: Path,
    *,
    project_id: str,
    session_path: Path | None = None,
) -> OperatorUserStorySessionResult:
    vault_root = vault_root.resolve()
    ingest = ingest_user_story_session(
        vault_root, project_id=project_id, session_path=session_path
    )
    pending = list_pending_user_story_confirmations(vault_root, project_id)
    signed = catalog_is_signed(vault_root, project_id)
    latest = brief_dir(vault_root, project_id) / "latest.md"
    latest_rel = str(latest.relative_to(vault_root)) if latest.is_file() else None

    ok = ingest.ok or ingest.detail == "no_user_story_session"
    detail = "operator_user_story_session_complete"
    if ingest.detail == "no_user_story_session":
        detail = "no_session_optional"

    return OperatorUserStorySessionResult(
        ok=ok,
        ingest=ingest.to_dict(),
        pending=pending,
        catalog_signed=signed,
        latest_brief=latest_rel,
        detail=detail,
    )
