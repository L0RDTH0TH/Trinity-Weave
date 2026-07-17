"""Factory run correlation — per-lane factory-run.jsonl + gate log."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def factory_run_log_path(vault_root: Path, lane: str) -> Path:
    lane = lane.strip().lower()
    return vault_root / ".technical" / "parallel" / lane / "factory-run.jsonl"


def gate_log_path(vault_root: Path) -> Path:
    return vault_root / ".technical" / "factory" / "gate-log.jsonl"


@dataclass(frozen=True)
class FactoryRunContext:
    """Correlation spine for one factory_lane job."""

    run_id: str
    chain_id: str
    queue_lane: str
    entry_id: str
    slice_id: str
    factory_lane: str

    @classmethod
    def from_entry(
        cls,
        entry: dict[str, Any],
        params: dict[str, Any],
        *,
        queue_lane: str,
        parent_run_id: str | None = None,
    ) -> FactoryRunContext:
        eid = str(entry.get("id") or "")
        slice_id = str(params.get("slice_id") or "")
        lane_id = str(params.get("lane_id") or "")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_id = f"factory-{slice_id}-{lane_id}-{stamp}"
        chain_id = str(
            parent_run_id
            or entry.get("architect_orchestration_run_id")
            or params.get("factory_dispatch_run_id")
            or eid
        )
        return cls(
            run_id=run_id,
            chain_id=chain_id,
            queue_lane=queue_lane.strip().lower(),
            entry_id=eid,
            slice_id=slice_id,
            factory_lane=lane_id,
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "run_id": self.run_id,
            "chain_id": self.chain_id,
            "queue_lane": self.queue_lane,
            "entry_id": self.entry_id,
            "slice_id": self.slice_id,
            "factory_lane": self.factory_lane,
        }


def append_factory_event(
    vault_root: Path,
    lane: str,
    event: str,
    *,
    run_id: str | None = None,
    chain_id: str | None = None,
    parent_run_id: str | None = None,
    factory_lane: str | None = None,
    slice_id: str | None = None,
    status: str = "ok",
    receipt_id: str | None = None,
    message: str = "",
    extra: dict[str, Any] | None = None,
) -> Path:
    vault_root = vault_root.resolve()
    path = factory_run_log_path(vault_root, lane)
    path.parent.mkdir(parents=True, exist_ok=True)
    row: dict[str, Any] = {
        "ts": _utc_iso(),
        "event": event,
        "lane": lane.strip().lower(),
        "status": status,
        "message": message,
    }
    if run_id:
        row["run_id"] = run_id
    if chain_id:
        row["chain_id"] = chain_id
    if parent_run_id:
        row["parent_run_id"] = parent_run_id
    if factory_lane:
        row["factory_lane"] = factory_lane
    if slice_id:
        row["slice_id"] = slice_id
    if receipt_id:
        row["receipt_id"] = receipt_id
    if extra:
        row.update(extra)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def factory_escalation_path(vault_root: Path) -> Path:
    return vault_root / ".technical" / "factory" / "factory_run_escalation.jsonl"


def append_factory_escalation(
    vault_root: Path,
    *,
    failure_class: str,
    slice_id: str,
    project_id: str,
    message: str = "",
    extra: dict[str, Any] | None = None,
) -> Path:
    path = factory_escalation_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    row: dict[str, Any] = {
        "ts": _utc_iso(),
        "failure_class": failure_class,
        "slice_id": slice_id,
        "project_id": project_id,
        "message": message,
    }
    if extra:
        row.update(extra)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def append_gate_log(
    vault_root: Path,
    pass_name: str,
    *,
    ok: bool,
    run_id: str | None = None,
    chain_id: str | None = None,
    slice_id: str | None = None,
    lane_id: str | None = None,
    violations: list[str] | None = None,
) -> Path:
    path = gate_log_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": _utc_iso(),
        "pass_name": pass_name,
        "ok": ok,
        "run_id": run_id,
        "chain_id": chain_id,
        "slice_id": slice_id,
        "lane_id": lane_id,
        "violations": violations or [],
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path
