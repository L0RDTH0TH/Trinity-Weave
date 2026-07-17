"""Half A roadmap factory artifact ledger — structural manifest append + drift reconcile."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ledger_path(vault_root: Path, project_id: str) -> Path:
    return (
        vault_root
        / "1-Projects"
        / project_id
        / "Factory-DRB"
        / "roadmap-factory-artifact-ledger.jsonl"
    )


def _file_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exists": False}
    data = path.read_bytes()
    return {
        "exists": True,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
        "mtime": path.stat().st_mtime,
    }


def append_roadmap_ledger_event(
    vault_root: Path,
    project_id: str,
    event: dict[str, Any],
) -> Path:
    """Append one structural ledger line (harness-only v1)."""
    vault_root = vault_root.resolve()
    path = ledger_path(vault_root, project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {**event, "recorded_at": _utc_iso(), "ledger": "roadmap_factory"}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def record_artifact(
    vault_root: Path,
    project_id: str,
    *,
    artifact_path: str,
    event_type: str,
    persona_id: str = "",
    product_factory_run_id: str = "",
    goal_authority_run_id: str = "",
    authoring_mode: str = "harness",
) -> dict[str, Any]:
    rel = artifact_path.lstrip("/")
    full = vault_root / rel
    manifest = _file_manifest(full)
    event = {
        "event_type": event_type,
        "artifact_path": rel,
        "persona_id": persona_id,
        "product_factory_run_id": product_factory_run_id,
        "goal_authority_run_id": goal_authority_run_id,
        "authoring_mode": authoring_mode,
        **manifest,
    }
    append_roadmap_ledger_event(vault_root, project_id, event)
    return event


@dataclass
class LedgerDriftResult:
    ok: bool
    drift_codes: list[str] = field(default_factory=list)
    last_event: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "drift_codes": list(self.drift_codes),
            "last_event": self.last_event,
        }


def reconcile_ledger_drift(
    vault_root: Path,
    project_id: str,
    *,
    max_lines: int = 50,
) -> LedgerDriftResult:
    """Compare last ledger entries to on-disk artifacts."""
    vault_root = vault_root.resolve()
    path = ledger_path(vault_root, project_id)
    if not path.is_file():
        return LedgerDriftResult(True)

    lines = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    recent = lines[-max_lines:] if lines else []
    drift: list[str] = []
    last: dict[str, Any] | None = None

    for raw in recent:
        try:
            row = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        last = row
        rel = str(row.get("artifact_path") or "")
        if not rel:
            continue
        full = vault_root / rel
        if not full.is_file():
            drift.append(f"missing:{rel}")
            continue
        if row.get("exists") and row.get("sha256"):
            current = _file_manifest(full)
            if current.get("sha256") != row.get("sha256"):
                drift.append(f"unexpected_mtime_or_content:{rel}")

    return LedgerDriftResult(ok=len(drift) == 0, drift_codes=drift, last_event=last)
