"""Per-job factory machine state — jam points and recovery checkpoints."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MACHINE_STATE_DIR_REL = ".technical/factory/machine-state"

MACHINES = (
    "interpretation",
    "preflight",
    "agent",
    "post_preflight",
    "receipt",
    "seats",
    "slice_rollup",
    "complete",
)

RESUME_FROM_CHOICES = ("interpretation", "preflight", "agent", "seats", "complete")


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def machine_state_dir(vault_root: Path) -> Path:
    return vault_root / MACHINE_STATE_DIR_REL


def machine_state_path(vault_root: Path, entry_id: str) -> Path:
    safe = entry_id.replace("/", "_")
    return machine_state_dir(vault_root) / f"{safe}.json"


def load_machine_state(vault_root: Path, entry_id: str) -> dict[str, Any] | None:
    path = machine_state_path(vault_root, entry_id)
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def save_machine_state(vault_root: Path, state: dict[str, Any]) -> Path:
    vault_root = vault_root.resolve()
    eid = str(state.get("entry_id") or "")
    if not eid:
        raise ValueError("machine_state requires entry_id")
    state = {**state, "updated_at": _utc_iso()}
    path = machine_state_path(vault_root, eid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return path


def init_machine_state(
    *,
    entry_id: str,
    slice_id: str,
    lane_id: str,
    queue_lane: str,
    run_id: str | None = None,
    chain_id: str | None = None,
) -> dict[str, Any]:
    return {
        "entry_id": entry_id,
        "slice_id": slice_id,
        "lane_id": lane_id,
        "queue_lane": queue_lane,
        "run_id": run_id,
        "chain_id": chain_id,
        "status": "running",
        "jam_at": None,
        "resume_from": None,
        "machines": {m: {"status": "pending", "detail": ""} for m in MACHINES},
        "agent_log_path": None,
        "changed_paths": [],
        "receipt_id": None,
        "last_error": None,
        "lane_seats": {},
    }


def set_machine(
    state: dict[str, Any],
    name: str,
    *,
    status: str,
    detail: str = "",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    machines = dict(state.get("machines") or {})
    row: dict[str, Any] = {"status": status, "detail": detail, "ts": _utc_iso()}
    if extra:
        row.update(extra)
    machines[name] = row
    out = {**state, "machines": machines}
    if status == "fail":
        out["status"] = "jammed"
        out["jam_at"] = name
        out["resume_from"] = _suggest_resume_from(name)
    elif status == "ok" and out.get("status") == "running":
        pass
    return out


def _suggest_resume_from(failed_machine: str) -> str:
    if failed_machine in ("interpretation",):
        return "interpretation"
    if failed_machine in ("preflight", "agent", "post_preflight", "receipt"):
        return "agent"
    if failed_machine in ("seats",):
        return "seats"
    return "seats"


def mark_jam(
    state: dict[str, Any],
    *,
    machine: str,
    error: str,
    agent_log_path: str | None = None,
    changed_paths: list[str] | None = None,
    lane_seats: dict[str, Any] | None = None,
) -> dict[str, Any]:
    out = set_machine(state, machine, status="fail", detail=error)
    out["last_error"] = error
    if agent_log_path:
        out["agent_log_path"] = agent_log_path
    if changed_paths is not None:
        out["changed_paths"] = list(changed_paths)
    if lane_seats is not None:
        out["lane_seats"] = lane_seats
    return out


def mark_complete_state(state: dict[str, Any]) -> dict[str, Any]:
    out = {**state, "status": "complete", "jam_at": None, "resume_from": None}
    out = set_machine(out, "complete", status="ok", detail="lane_job_complete")
    return out


def list_machine_states(vault_root: Path, *, jammed_only: bool = False) -> list[dict[str, Any]]:
    d = machine_state_dir(vault_root)
    if not d.is_dir():
        return []
    rows: list[dict[str, Any]] = []
    for path in sorted(d.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        if jammed_only and data.get("status") != "jammed":
            continue
        rows.append(data)
    return rows


def find_entry_in_pq(vault_root: Path, queue_lane: str, entry_id: str) -> dict[str, Any] | None:
    from ...lane_bundle import bundle_dir_for_lane
    from ...plan import load_queue_file

    pq = bundle_dir_for_lane(vault_root, queue_lane) / "prompt-queue.jsonl"
    if not pq.is_file():
        return None
    for e in load_queue_file(pq):
        raw = e.model_dump(mode="json")
        if str(raw.get("id")) == entry_id:
            return raw
    return None
