"""L5 guard — block autonomous repair/eat while operator/user escalations are pending."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_ESCALATION_FM = re.compile(r"^escalation_active:\s*true\b", re.MULTILINE | re.IGNORECASE)
_REVIEWED_FM = re.compile(r"^user_reviewed:\s*true\b", re.MULTILINE | re.IGNORECASE)
_NO_GAIN_SUPPRESS = frozenset(
    {
        "no_gain_pending_user_gates",
        "explicit_skip_stall",
    }
)


def _scan_agent_output_escalations(vault_root: Path) -> list[str]:
    out_dir = vault_root / "Ingest" / "Agent-Output"
    if not out_dir.is_dir():
        return []
    pending: list[str] = []
    for path in sorted(out_dir.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if _ESCALATION_FM.search(text) and not _REVIEWED_FM.search(text):
            pending.append(str(path.relative_to(vault_root)))
    return pending


def _scan_queue_continuation_no_gain(vault_root: Path, *, max_files: int = 12) -> list[str]:
    tech = vault_root / ".technical"
    if not tech.is_dir():
        return []
    hits: list[str] = []
    paths = list(tech.rglob("queue-continuation.jsonl"))[:max_files]
    for qpath in paths:
        try:
            lines = qpath.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line in lines[-20:]:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(row, dict):
                continue
            suppress = str(row.get("suppress_reason") or "")
            if suppress in _NO_GAIN_SUPPRESS:
                hits.append(f"{qpath.relative_to(vault_root)}:{suppress}")
    return hits


def user_escalation_pending(vault_root: Path) -> tuple[bool, dict[str, Any]]:
    """
    True when autonomous L5 repair/eat must not run (would mask human gates).

    Audit/board refresh may still run.
    """
    vault_root = vault_root.resolve()
    inbox = _scan_agent_output_escalations(vault_root)
    no_gain = _scan_queue_continuation_no_gain(vault_root)
    blocked = bool(inbox or no_gain)
    return blocked, {
        "operator_inbox_pending": inbox,
        "queue_continuation_gates": no_gain,
        "reason": "user_escalation_pending" if blocked else "clear",
    }
