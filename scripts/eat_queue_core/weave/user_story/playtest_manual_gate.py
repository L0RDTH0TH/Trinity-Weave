"""Playtest manual gate — Half B overnight exit between sessions (Option B)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..factory.operator_feedback import FeedbackRow, load_operator_feedback

PLAYTEST_DONE_WHEN_TOKENS: frozenset[str] = frozenset(
    {
        "playtest_manual_gate",
        "playtest_gate",
        "operator_playtest_pending",
        "playtest_pending_sign_off",
    }
)


def _normalize_token(raw: Any) -> str:
    return str(raw or "").strip().lower().replace(" ", "_").replace("-", "_")


def done_when_requests_playtest_gate(packet: dict[str, Any]) -> bool:
    criteria = packet.get("done_when") or []
    if not isinstance(criteria, list):
        return False
    for raw in criteria:
        key = _normalize_token(raw)
        if key in PLAYTEST_DONE_WHEN_TOKENS:
            return True
        if "playtest" in key and ("gate" in key or "manual" in key or "pending" in key):
            return True
    return False


def _feedback_rel(project_id: str) -> str:
    return (
        f"1-Projects/{project_id}/Factory-DRB/operator-feedback/"
        f"godot-closed-alpha-kinesthetic.yaml"
    )


def _brief_dir(vault_root: Path, project_id: str) -> Path:
    return (
        vault_root
        / "1-Projects"
        / project_id
        / "Factory-DRB"
        / "operator-feedback"
        / "playtest-briefs"
    )


def latest_playtest_brief(vault_root: Path, project_id: str) -> Path | None:
    brief_dir = _brief_dir(vault_root, project_id)
    if not brief_dir.is_dir():
        return None
    matches = sorted(brief_dir.glob("playtest-brief-*.md"), reverse=True)
    return matches[0] if matches else None


def playtest_feedback_pending(
    vault_root: Path,
    project_id: str,
    *,
    feedback_rel: str | None = None,
) -> tuple[bool, list[str]]:
    rel = feedback_rel or _feedback_rel(project_id)
    rows = load_operator_feedback(vault_root, rel)
    if not rows:
        return True, ["no_feedback_rows"]
    pending_ids: list[str] = []
    for row in rows:
        if not isinstance(row, FeedbackRow):
            continue
        if not row.kinesthetic:
            continue
        if row.operator_confirmed and row.pass_ is not None:
            continue
        if row.pass_ is None or not row.operator_confirmed:
            pending_ids.append(row.checklist_id)
    return bool(pending_ids), pending_ids


def playtest_gate_surface_ready(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """
    Machine playtest surface exists; operator sign-off pending between sessions.

    Mirrors loop-2 gate semantics for Half B.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return False, "no_project_id"

    brief = latest_playtest_brief(vault_root, pid)
    if brief is None:
        return False, "no_playtest_brief"

    pending, pending_ids = playtest_feedback_pending(vault_root, pid)
    if pending:
        detail = pending_ids[0] if pending_ids else "pending"
        return True, f"playtest_pending:{detail}"

    return False, "playtest_feedback_complete"


def playtest_manual_gate_matched(
    vault_root: Path,
    packet: dict[str, Any],
    *,
    project_id: str | None = None,
) -> tuple[bool, str]:
    if not done_when_requests_playtest_gate(packet):
        return False, ""
    pid = str(project_id or packet.get("project_id") or "").strip()
    if not pid:
        return False, "no_project_id"
    ok, reason = playtest_gate_surface_ready(vault_root, pid)
    if not ok:
        return False, reason
    token = ""
    for raw in packet.get("done_when") or []:
        key = _normalize_token(raw)
        if key:
            token = key
            break
    return True, token or "playtest_manual_gate"
