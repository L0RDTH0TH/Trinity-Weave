"""Parallel race merge barrier — ordering, drop deps, shared surface locks."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .drop_contract_base import check_depends_on_drops
from .lane_charters import load_lane_charter

BARRIER_STATE_REL = ".technical/factory/merge-barrier-state.json"


@dataclass(frozen=True)
class MergeBarrierResult:
    ok: bool
    allowed: bool
    violations: tuple[str, ...]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "allowed": self.allowed,
            "violations": list(self.violations),
            "detail": self.detail,
        }


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _barrier_path(vault_root: Path) -> Path:
    return vault_root / BARRIER_STATE_REL


def load_barrier_state(vault_root: Path) -> dict[str, Any]:
    path = _barrier_path(vault_root)
    if not path.is_file():
        return {"active_lanes": [], "completed_lane_jobs": [], "shared_locks": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save_barrier_state(vault_root: Path, state: dict[str, Any]) -> None:
    path = _barrier_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _charter_fields(vault_root: Path, lane_id: str) -> dict[str, Any]:
    ch = load_lane_charter(vault_root, lane_id)
    if ch is None:
        return {}
    raw = yaml.safe_load(ch.path.read_text(encoding="utf-8")) or {}
    return raw if isinstance(raw, dict) else {}


def _target_overlap(a: list[str], b: list[str]) -> list[str]:
    return [p for p in a if p in b]


def check_job_allowed(
    vault_root: Path,
    job: dict[str, Any],
    *,
    game_repo_rel: str,
    parallel_enabled: bool = False,
) -> MergeBarrierResult:
    vault_root = vault_root.resolve()
    lane_id = str(job.get("lane_id") or "")
    slice_id = str(job.get("slice_id") or "")
    fields = _charter_fields(vault_root, lane_id)
    state = load_barrier_state(vault_root)
    violations: list[str] = []

    active = [str(x) for x in state.get("active_lanes") or []]
    completed = state.get("completed_lane_jobs") or []
    completed_keys = {
        (str(r.get("slice_id")), str(r.get("lane_id")))
        for r in completed
        if isinstance(r, dict)
    }

    if (slice_id, lane_id) in completed_keys:
        violations.append("lane_job_already_completed")

    blocks = [str(x) for x in fields.get("blocks_parallel_lanes") or []]
    for blocker in blocks:
        if blocker in active and blocker != lane_id:
            violations.append(f"merge_blocked:blocks_parallel_lanes:{blocker}")

    if not parallel_enabled and active and lane_id not in active:
        violations.append(f"merge_blocked:serialize_single_lane:active={active}")

    depends = [str(x) for x in fields.get("depends_on_drops") or job.get("depends_on_drops") or []]
    if depends:
        repo = vault_root / game_repo_rel.strip("/")
        ok_deps, dep_v = check_depends_on_drops(
            repo,
            depends,
            pinned_receipt_ids=[str(x) for x in fields.get("pinned_drop_receipt_ids") or []],
        )
        if not ok_deps:
            violations.extend([f"depends_on_drops:{v}" for v in dep_v])

    shared_locks = [str(x) for x in fields.get("shared_surface_locks") or []]
    held = [str(x) for x in state.get("shared_locks") or []]
    for lock in shared_locks:
        if lock in held and lane_id not in active:
            violations.append(f"merge_blocked:shared_surface_lock:{lock}")

    target_files = [str(x) for x in fields.get("target_files") or []]
    for other_lane in active:
        if other_lane == lane_id:
            continue
        other_fields = _charter_fields(vault_root, other_lane)
        overlap = _target_overlap(target_files, [str(x) for x in other_fields.get("target_files") or []])
        if overlap:
            violations.append(f"merge_blocked:target_files_overlap:{other_lane}:{overlap}")

    allowed = len(violations) == 0
    detail = "merge_allowed" if allowed else "; ".join(violations)
    return MergeBarrierResult(ok=True, allowed=allowed, violations=tuple(violations), detail=detail)


def acquire_lane_job(vault_root: Path, job: dict[str, Any]) -> None:
    state = load_barrier_state(vault_root)
    lane_id = str(job.get("lane_id") or "")
    slice_id = str(job.get("slice_id") or "")
    active = list(state.get("active_lanes") or [])
    if lane_id and lane_id not in active:
        active.append(lane_id)
    state["active_lanes"] = active
    state["current_slice_id"] = slice_id
    fields = _charter_fields(vault_root, lane_id)
    locks = list(state.get("shared_locks") or [])
    for lock in fields.get("shared_surface_locks") or []:
        if str(lock) not in locks:
            locks.append(str(lock))
    state["shared_locks"] = locks
    state["updated_at"] = _utc_iso()
    save_barrier_state(vault_root, state)


def release_lane_job(vault_root: Path, job: dict[str, Any], *, ok: bool) -> dict[str, Any]:
    state = load_barrier_state(vault_root)
    lane_id = str(job.get("lane_id") or "")
    slice_id = str(job.get("slice_id") or "")
    active = [x for x in (state.get("active_lanes") or []) if str(x) != lane_id]
    state["active_lanes"] = active
    if ok:
        completed = list(state.get("completed_lane_jobs") or [])
        completed.append(
            {
                "slice_id": slice_id,
                "lane_id": lane_id,
                "completed_at": _utc_iso(),
            }
        )
        state["completed_lane_jobs"] = completed
    fields = _charter_fields(vault_root, lane_id)
    locks = list(state.get("shared_locks") or [])
    for lock in fields.get("shared_surface_locks") or []:
        lock_s = str(lock)
        if lock_s in locks:
            locks.remove(lock_s)
    state["shared_locks"] = locks
    state["updated_at"] = _utc_iso()
    save_barrier_state(vault_root, state)
    return state


def filter_dispatch_jobs(
    vault_root: Path,
    jobs: list[dict[str, Any]],
    *,
    game_repo_rel: str,
    parallel_enabled: bool = False,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    allowed_jobs: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    for job in jobs:
        result = check_job_allowed(
            vault_root, job, game_repo_rel=game_repo_rel, parallel_enabled=parallel_enabled
        )
        if result.allowed:
            allowed_jobs.append(job)
        else:
            blocked.append({**job, "merge_barrier": result.to_dict()})
    return allowed_jobs, blocked


def reset_slice_barrier(vault_root: Path, slice_id: str) -> None:
    state = load_barrier_state(vault_root)
    completed = [
        r
        for r in (state.get("completed_lane_jobs") or [])
        if isinstance(r, dict) and str(r.get("slice_id")) != slice_id
    ]
    state["completed_lane_jobs"] = completed
    state["active_lanes"] = []
    state["shared_locks"] = []
    state["current_slice_id"] = slice_id
    state["updated_at"] = _utc_iso()
    save_barrier_state(vault_root, state)
