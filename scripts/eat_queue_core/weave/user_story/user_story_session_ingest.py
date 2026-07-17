"""Ingest operator user-story marks from session JSONL (mirrors playtest_session_ingest)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .user_story_feedback import load_user_story_feedback, save_user_story_feedback


@dataclass(frozen=True)
class UserStoryIngestResult:
    ok: bool
    rows_updated: int
    detail: str
    session_path: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "rows_updated": self.rows_updated,
            "detail": self.detail,
            "session_path": self.session_path,
        }


def _parse_mark(row: dict[str, Any]) -> dict[str, Any] | None:
    verdict = row.get("verdict") or row.get("experiential_pass")
    row_id = row.get("row_id") or row.get("catalog_row_id")
    if not row_id:
        return None
    if verdict in ("pass", "true", True):
        ep: bool | None = True
    elif verdict in ("fail", "false", False):
        ep = False
    elif verdict == "skip":
        return None
    else:
        ep = None
    return {
        "row_id": str(row_id),
        "beat_ref": str(row.get("beat_ref") or ""),
        "experiential_pass": ep,
        "operator_confirmed": False,
        "notes": str(row.get("note") or row.get("notes") or ""),
        "source": "user_story_mark",
    }


def ingest_user_story_session(
    vault_root: Path,
    *,
    project_id: str,
    session_path: Path | None = None,
    write_feedback: bool = True,
) -> UserStoryIngestResult:
    """
    Ingest JSONL session with user_story_mark rows.

    Operator marks override prior ingest suggestions; never auto-set operator_confirmed.
    """
    vault_root = vault_root.resolve()
    sess = session_path
    if sess is None:
        cand = (
            vault_root
            / "1-Projects"
            / project_id
            / "Factory-DRB"
            / "operator-feedback"
            / "user-story-sessions"
        )
        if cand.is_dir():
            files = sorted(cand.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
            sess = files[0] if files else None

    if sess is None or not sess.is_file():
        return UserStoryIngestResult(False, 0, "no_user_story_session", None)

    marks_by_row: dict[str, dict[str, Any]] = {}
    for line in sess.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        if row.get("type") not in ("user_story_mark", "operator_mark", None):
            if row.get("verdict") is None and row.get("experiential_pass") is None:
                continue
        parsed = _parse_mark(row)
        if parsed:
            marks_by_row[parsed["row_id"]] = parsed

    if not marks_by_row:
        return UserStoryIngestResult(
            True, 0, "no_marks_in_session", str(sess.relative_to(vault_root))
        )

    existing = {r.row_id: r.to_dict() for r in load_user_story_feedback(vault_root, project_id)}
    updated = 0
    for row_id, mark in marks_by_row.items():
        prev = existing.get(row_id, {})
        merged = {**prev, **mark}
        merged["operator_confirmed"] = prev.get("operator_confirmed", False)
        existing[row_id] = merged
        updated += 1

    if write_feedback:
        save_user_story_feedback(vault_root, project_id, list(existing.values()))

    return UserStoryIngestResult(
        True,
        updated,
        "user_story_session_ingested",
        str(sess.relative_to(vault_root)),
    )
