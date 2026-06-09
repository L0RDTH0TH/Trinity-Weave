"""Governance file contracts for Phase 0/1 weave."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def weave_dir(vault_root: Path) -> Path:
    return vault_root / ".technical" / "weave"


def governance_record_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "governance_reviews.jsonl"


def lane_board_snapshot_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "lane_board_snapshot.json"


def metrics_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "metrics.jsonl"


def ensure_weave_paths(vault_root: Path) -> dict[str, str]:
    base = weave_dir(vault_root)
    base.mkdir(parents=True, exist_ok=True)

    for target in (governance_record_path(vault_root), metrics_path(vault_root)):
        if not target.exists():
            target.write_text("", encoding="utf-8")

    snap = lane_board_snapshot_path(vault_root)
    if not snap.exists():
        snap.write_text(
            json.dumps(
                {
                    "timestamp": _now_iso(),
                    "content_hash": "",
                    "lanes": [],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    return {
        "weave_dir": str(base),
        "governance_reviews": str(governance_record_path(vault_root)),
        "lane_board_snapshot": str(snap),
        "metrics": str(metrics_path(vault_root)),
    }


def write_governance_review_record(vault_root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    ensure_weave_paths(vault_root)
    target = governance_record_path(vault_root)

    row = {
        "timestamp": payload.get("timestamp") or _now_iso(),
        "review_type": "governance_review",
        "items_cleared": payload.get("items_cleared") or [],
        "counselor_hash": payload.get("counselor_hash") or "manual",
        "operator_pulse": payload.get("operator_pulse") or "neutral",
        "manual_ghost_stale_noticed": bool(payload.get("manual_ghost_stale_noticed", False)),
        "notes": payload.get("notes") or "",
    }

    line = json.dumps(row, ensure_ascii=False)
    prev = target.read_text(encoding="utf-8") if target.is_file() else ""
    target.write_text((prev.rstrip("\n") + "\n" if prev.strip() else "") + line + "\n", encoding="utf-8")
    return row


def append_metric_row(vault_root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    ensure_weave_paths(vault_root)
    target = metrics_path(vault_root)
    row = {"timestamp": payload.get("timestamp") or _now_iso(), **payload}
    line = json.dumps(row, ensure_ascii=False)
    prev = target.read_text(encoding="utf-8") if target.is_file() else ""
    target.write_text((prev.rstrip("\n") + "\n" if prev.strip() else "") + line + "\n", encoding="utf-8")
    return row


def latest_governance_review(vault_root: Path) -> dict[str, Any] | None:
    target = governance_record_path(vault_root)
    if not target.is_file():
        return None
    rows = [ln.strip() for ln in target.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    for line in reversed(rows):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            return row
    return None
