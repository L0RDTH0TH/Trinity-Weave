"""Roadmap (Half A) → Implementation (Half B) handoff after factory_staged."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ...lane_bundle import bundle_dir_for_lane
from ...lane_queue_io import append_lane_queue_entry, pq_relative_for_lane
from .product_factory_state import FACTORY_STAGED, load_product_factory


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def count_pending_factory_lane_jobs(vault_root: Path, lane: str) -> int:
    """Count IMPLEMENT_SLICE factory_lane lines still on lane PQ."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    pq = bundle_dir_for_lane(vault_root, lane) / "prompt-queue.jsonl"
    if not pq.is_file():
        return 0
    count = 0
    for line in pq.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        mode = str(row.get("mode") or "").upper().replace("-", "_")
        if mode != "IMPLEMENT_SLICE":
            continue
        params = row.get("params") if isinstance(row.get("params"), dict) else {}
        if str(params.get("action") or "").lower() == "factory_lane":
            count += 1
    return count


def append_factory_eat_handoff(
    vault_root: Path,
    *,
    lane: str,
    project_id: str,
    run_id: str,
    slice_id: str,
    wave: int = 1,
    lane_job_count: int = 0,
    trigger_source: str = "factory_staged",
) -> dict[str, Any]:
    """
    Append PRODUCT_FACTORY_CONTINUE with action eat_factory_lanes.

    Normative: appended after stage_factory_dispatch_to_pq succeeds. Operator
    runs EAT-QUEUE (or headless_eat) to drain IMPLEMENT_SLICE lines already on PQ.
    """
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    eid = f"pfh-{uuid.uuid4().hex[:12]}"
    fp = f"factory-eat-handoff:{run_id}:{slice_id}:w{int(wave)}"
    params: dict[str, Any] = {
        "project_id": project_id,
        "product_factory_run_id": run_id,
        "action": "eat_factory_lanes",
        "slice_id": slice_id,
        "wave": int(wave),
        "lane_job_count": int(lane_job_count),
        "trigger_source": trigger_source,
        "handoff_at": _utc_iso(),
    }
    return append_lane_queue_entry(
        vault_root,
        lane=lane,
        mode="PRODUCT_FACTORY_CONTINUE",
        params=params,
        entry_id=eid,
        source="factory_eat_handoff",
        fingerprint=fp,
    )


def handle_factory_eat_handoff(
    vault_root: Path,
    entry: dict[str, Any],
    *,
    harness_context: bool = False,
) -> dict[str, Any]:
    """Half B handoff — ack in IDE queue context; drain IMPLEMENT_SLICE in harness context."""
    vault_root = vault_root.resolve()
    eid = str(entry.get("id") or "")
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    harness_context = harness_context or bool(params.get("harness_context"))
    project_id = str(entry.get("project_id") or params.get("project_id") or "")
    lane = str(entry.get("queue_lane") or params.get("queue_lane") or "godot").strip().lower()

    pf = load_product_factory(vault_root, project_id) if project_id else {}
    completed = pf.get("completed_phases") or []
    has_staged = isinstance(completed, list) and FACTORY_STAGED in completed
    cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
    phase = str(cell.get("phase") or "")

    pending = count_pending_factory_lane_jobs(vault_root, lane)
    expected = int(params.get("lane_job_count") or 0)

    if not has_staged and phase not in ("lanes_running", "pm_review", "composed"):
        return {
            "ok": False,
            "id": eid,
            "mode": "PRODUCT_FACTORY_CONTINUE",
            "detail": "handoff_premature",
            "message": "factory_staged not recorded — complete Roadmap factory_stage before eating lanes",
        }

    pq_rel = pq_relative_for_lane(vault_root, lane)

    if harness_context and pending > 0:
        from ...layer1_implementation import (
            FACTORY_LANE_MAX_PER_PASS,
            filter_implementation_entries,
            resolve_implementation_batch_size,
            run_layer1_implementation_pass,
        )
        from ...plan import load_queue_file

        pq_path = bundle_dir_for_lane(vault_root, lane) / "prompt-queue.jsonl"
        entries = load_queue_file(pq_path) if pq_path.is_file() else []
        impl_entries = filter_implementation_entries(entries)
        max_impl = resolve_implementation_batch_size(
            impl_entries, FACTORY_LANE_MAX_PER_PASS
        )
        impl_out = run_layer1_implementation_pass(
            vault_root,
            lane,
            max_entries=max_impl,
            dry_run=False,
            emit_watcher=True,
        )
        remaining = count_pending_factory_lane_jobs(vault_root, lane)
        return {
            "ok": bool(impl_out.get("ok")),
            "id": eid,
            "mode": "PRODUCT_FACTORY_CONTINUE",
            "detail": "factory_eat_handoff_drained",
            "message": (
                f"Harness drained {impl_out.get('processed', 0)} IMPLEMENT_SLICE job(s) on {pq_rel}; "
                f"{remaining} pending."
            ),
            "pending_lane_jobs": remaining,
            "expected_lane_jobs": expected,
            "implementation_processed": impl_out.get("processed", 0),
            "slice_id": params.get("slice_id"),
            "wave": params.get("wave"),
            "pq_path": pq_rel,
            "next_step": "headless_eat" if remaining else "continue",
        }

    return {
        "ok": True,
        "id": eid,
        "mode": "PRODUCT_FACTORY_CONTINUE",
        "detail": "factory_eat_handoff_ack",
        "message": (
            f"Implementation factory owns the queue: {pending} IMPLEMENT_SLICE lane job(s) on {pq_rel}. "
            "Run EAT-QUEUE (laptop) or harness headless_eat for this lane."
        ),
        "pending_lane_jobs": pending,
        "expected_lane_jobs": expected,
        "slice_id": params.get("slice_id"),
        "wave": params.get("wave"),
        "pq_path": pq_rel,
        "next_step": "EAT-QUEUE",
    }
