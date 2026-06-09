"""Structured corps repair audit log (Grok F) — hash before/after, repair typing."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .governance import ensure_weave_paths

AUDIT_REL = Path(".technical/weave/corps-repair-audit.jsonl")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def corps_repair_audit_path(vault_root: Path) -> Path:
    return vault_root.resolve() / AUDIT_REL


def card_content_hash(card: dict[str, Any] | None) -> str:
    if not card:
        return ""
    blob = json.dumps(card, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def append_corps_repair_audit(vault_root: Path, row: dict[str, Any]) -> None:
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    path = corps_repair_audit_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"ts": _now_iso(), **row}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def audit_card_repair(
    vault_root: Path,
    *,
    trinity_id: str,
    repair_type: str,
    disconnect_kind: str | None = None,
    before_card: dict[str, Any] | None = None,
    after_card: dict[str, Any] | None = None,
    lap: int | None = None,
    changed: bool | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    """Standard audit row for conduct/shape/semantic repairs."""
    row: dict[str, Any] = {
        "event": "corps_repair",
        "trinity_id": trinity_id,
        "repair_type": repair_type,
        "disconnect_kind": disconnect_kind or "",
        "before_hash": card_content_hash(before_card),
        "after_hash": card_content_hash(after_card),
        "changed": changed,
    }
    if lap is not None:
        row["lap"] = lap
    if extra:
        row.update(extra)
    append_corps_repair_audit(vault_root, row)


def read_recent_repair_metrics(vault_root: Path, *, max_rows: int = 200) -> dict[str, Any]:
    """Summarize last repair-loop metrics from audit + metrics.jsonl."""
    vault_root = vault_root.resolve()
    laps: list[dict[str, Any]] = []
    path = corps_repair_audit_path(vault_root)
    if path.is_file():
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-max_rows:]
        for ln in lines:
            try:
                row = json.loads(ln)
            except json.JSONDecodeError:
                continue
            if row.get("event") == "repair_loop_lap":
                laps.append(row)
    if not laps:
        return {"lap_count": 0, "repair_convergence": None, "last_stop_reason": None}
    last = laps[-1]
    changed = int(last.get("changed_count") or 0)
    lap_n = int(last.get("lap") or 1)
    return {
        "lap_count": len(laps),
        "repair_convergence": round(changed / max(1, lap_n), 3),
        "last_stop_reason": last.get("stop_reason"),
        "last_changed_count": changed,
    }
