"""Factory lane recovery — replay seats, find agent logs, manual machine turn-over."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...lane_bundle import bundle_dir_for_lane
from .factory_machine_state import (
    find_entry_in_pq,
    load_machine_state,
    save_machine_state,
)


def find_latest_agent_log(
    vault_root: Path,
    queue_lane: str,
    *,
    factory_lane: str | None = None,
    slice_id: str | None = None,
) -> Path | None:
    """Most recent factory-lane telemetry log for queue_lane (+ optional lane/slice filter)."""
    vault_root = vault_root.resolve()
    telem = vault_root / ".technical" / "Run-Telemetry" / queue_lane.strip().lower()
    if not telem.is_dir():
        return None
    pattern = "factory-lane-"
    if factory_lane and slice_id:
        pattern = f"factory-lane-{factory_lane}-{slice_id}-"
    elif factory_lane:
        pattern = f"factory-lane-{factory_lane}-"

    candidates = sorted(
        (p for p in telem.glob(f"{pattern}*.log") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def resolve_agent_log_path(
    vault_root: Path,
    *,
    entry_id: str,
    queue_lane: str,
    agent_log_path: str | None = None,
    factory_lane: str | None = None,
    slice_id: str | None = None,
) -> str | None:
    if agent_log_path:
        p = vault_root / agent_log_path
        if p.is_file():
            return str(p.relative_to(vault_root))
        if Path(agent_log_path).is_file():
            return agent_log_path
    state = load_machine_state(vault_root, entry_id)
    if state and state.get("agent_log_path"):
        rel = str(state["agent_log_path"])
        if (vault_root / rel).is_file():
            return rel
    latest = find_latest_agent_log(
        vault_root, queue_lane, factory_lane=factory_lane, slice_id=slice_id
    )
    if latest:
        return str(latest.relative_to(vault_root))
    return None


def replay_factory_lane_seats(
    vault_root: Path,
    queue_lane: str,
    entry: dict[str, Any],
    *,
    agent_log_path: str | None = None,
    complete_if_ok: bool = True,
    parent_run_id: str | None = None,
) -> dict[str, Any]:
    """
    Re-run lane seats (and optionally complete path) without re-invoking the agent.

    Use when agent artifacts exist but post-agent seats jammed (lint evidence, etc.).
    """
    from .factory_lane_runner import run_factory_lane_job

    eid = str(entry.get("id") or "")
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    log_rel = resolve_agent_log_path(
        vault_root,
        entry_id=eid,
        queue_lane=queue_lane,
        agent_log_path=agent_log_path,
        factory_lane=str(params.get("lane_id") or ""),
        slice_id=str(params.get("slice_id") or ""),
    )
    if not log_rel:
        return {
            "ok": False,
            "id": eid,
            "error": "no_agent_log_for_replay",
            "detail": "Provide --agent-log or ensure Run-Telemetry factory-lane log exists",
            "segment": "REPLAY_SEATS",
        }

    result = run_factory_lane_job(
        vault_root,
        queue_lane,
        entry,
        params=params,
        parent_run_id=parent_run_id,
        skip_agent=True,
        skip_preflight=True,
        agent_log_path=log_rel,
        resume_from="seats",
        complete_pipeline=complete_if_ok,
    )
    if result.get("ok") and complete_if_ok:
        from ...full_cycle import apply_queue_cleanup
        from ...lane_bundle import bundle_dir_for_lane

        pq = bundle_dir_for_lane(vault_root, queue_lane) / "prompt-queue.jsonl"
        if pq.is_file():
            apply_queue_cleanup(pq.resolve(), {eid})
    return result


def replay_factory_lane_by_job_id(
    vault_root: Path,
    queue_lane: str,
    job_id: str,
    *,
    agent_log_path: str | None = None,
    complete_if_ok: bool = True,
) -> dict[str, Any]:
    entry = find_entry_in_pq(vault_root, queue_lane, job_id)
    if entry is None:
        state = load_machine_state(vault_root, job_id)
        if state:
            return {
                "ok": False,
                "id": job_id,
                "error": "job_not_on_pq",
                "machine_state": state,
                "detail": "PQ line consumed or missing; restore from dispatch or re-stage",
                "segment": "REPLAY_SEATS",
            }
        return {
            "ok": False,
            "id": job_id,
            "error": "job_not_found",
            "segment": "REPLAY_SEATS",
        }
    return replay_factory_lane_seats(
        vault_root,
        queue_lane,
        entry,
        agent_log_path=agent_log_path,
        complete_if_ok=complete_if_ok,
    )


def persist_replay_outcome(vault_root: Path, result: dict[str, Any]) -> None:
    """Update machine state after replay attempt."""
    eid = str(result.get("id") or "")
    if not eid:
        return
    from .factory_machine_state import load_machine_state, mark_complete_state, mark_jam, init_machine_state

    state = load_machine_state(vault_root, eid)
    if state is None:
        state = init_machine_state(
            entry_id=eid,
            slice_id=str(result.get("slice_id") or ""),
            lane_id=str(result.get("lane_id") or ""),
            queue_lane="godot",
            run_id=result.get("run_id"),
            chain_id=result.get("chain_id"),
        )
    if result.get("ok"):
        state = mark_complete_state(state)
        state["agent_log_path"] = result.get("agent", {}).get("log_path") or state.get("agent_log_path")
        state["changed_paths"] = result.get("changed_paths") or state.get("changed_paths")
        state["receipt_id"] = (result.get("receipt") or {}).get("receipt_id")
    else:
        state = mark_jam(
            state,
            machine="seats",
            error=str(result.get("error") or "replay_failed"),
            agent_log_path=(result.get("agent") or {}).get("log_path"),
            changed_paths=result.get("changed_paths"),
            lane_seats=result.get("lane_seats"),
        )
    save_machine_state(vault_root, state)
