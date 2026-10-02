"""Append PRODUCT_FACTORY_CONTINUE after agent beats (Half B queue-layer1)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from pathlib import Path

from ...lane_queue_io import append_lane_queue_entry
from ...models import QueueEntry


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_mode(mode: str) -> str:
    return str(mode or "").strip().upper().replace(" ", "_").replace("-", "_")


CONTINUE_TRIGGER_MODES = frozenset(
    {
        "RESUME_ROADMAP",
        "RESEARCH_AGENT",
        "RESEARCH_GAPS",
        "SLICE_PRODUCER_COMPOSE",
        "SLICE_PRODUCER_REVIEW",
    }
)


def entry_triggers_product_factory_continue(entry: dict[str, Any] | QueueEntry) -> bool:
    """True when a successful agent beat should schedule conductor tick."""
    if isinstance(entry, QueueEntry):
        row = entry.model_dump(mode="json")
    else:
        row = dict(entry)
    mode = _normalize_mode(str(row.get("mode") or ""))
    if mode not in CONTINUE_TRIGGER_MODES:
        return False
    params = row.get("params") if isinstance(row.get("params"), dict) else {}
    if not params.get("product_factory_run_id"):
        return False
    if mode == "RESUME_ROADMAP":
        action = str(params.get("action") or "").lower()
        if action == "bootstrap-execution-track":
            return False
        return params.get("queue_next", True) is not False
    if mode in ("RESEARCH_AGENT", "RESEARCH_GAPS"):
        return params.get("queue_next", True) is not False
    return True


def _agent_phase_from_entry(entry: dict[str, Any]) -> str | None:
    """Map consumed PQ entry to conductor phase completed by agent beat."""
    mode = str(entry.get("mode") or "").upper().replace("-", "_")
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    if mode != "RESUME_ROADMAP":
        return None
    action = str(params.get("action") or "").lower()
    if action == "bootstrap-execution-track":
        return "execution_bootstrap"
    track = str(params.get("roadmap_track") or "").lower()
    if track == "conceptual":
        # One deepen beat ≠ conceptual leg complete — tick() gates on conceptual_track_ready.
        return None
    return None


def append_product_factory_continue(
    vault_root: Path,
    *,
    lane: str,
    project_id: str,
    run_id: str,
    trigger_entry_id: str | None = None,
    source: str = "product_factory_continue",
    agent_phase_complete: str | None = None,
    prefer_product_seats_met: bool | None = None,
    cell_complete: bool | None = None,
    force: bool = False,
) -> dict[str, Any]:
    """Single helper — append one PRODUCT_FACTORY_CONTINUE line to lane PQ.

    Suppresses spurious continues when Prefer product seats unmet or cell not complete
    (unless ``force``). Dedupe: skip when an identical open continue already sits on PQ.
    """
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    from .done_when_eval import loop2_exit_honestly_eligible
    from .product_factory_state import load_product_factory

    if loop2_exit_honestly_eligible(vault_root, project_id):
        return {
            "ok": True,
            "skipped": True,
            "reason": "loop2_exit_eligible",
            "project_id": project_id,
        }

    if not force:
        if prefer_product_seats_met is False:
            return {
                "ok": True,
                "skipped": True,
                "reason": "prefer_product_seats_unmet",
                "project_id": project_id,
                "run_id": run_id,
            }
        pf = load_product_factory(vault_root, project_id) if project_id else {}
        cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
        phase = str(cell.get("phase") or "")
        completed = pf.get("completed_phases") or []
        if cell_complete is False:
            return {
                "ok": True,
                "skipped": True,
                "reason": "cell_not_complete",
                "project_id": project_id,
                "run_id": run_id,
            }
        # Spurious continue after failed Prefer — cell still lanes_running / pm_review blocked.
        if phase in ("lanes_running", "blocked", "jammed") and source in (
            "depth_bump",
            "factory_lane_success_theater",
        ):
            return {
                "ok": True,
                "skipped": True,
                "reason": f"cell_phase_blocks_continue:{phase}",
                "project_id": project_id,
                "run_id": run_id,
            }
        if isinstance(completed, list) and "factory_cell_complete" not in completed:
            if source == "depth_bump" and prefer_product_seats_met is False:
                return {
                    "ok": True,
                    "skipped": True,
                    "reason": "factory_cell_incomplete_prefer_unmet",
                    "project_id": project_id,
                }

    # Dedupe open continues for same run on PQ.
    from ...lane_bundle import bundle_dir_for_lane
    import json

    pq = bundle_dir_for_lane(vault_root, lane) / "prompt-queue.jsonl"
    if pq.is_file():
        for line in pq.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            mode = str(row.get("mode") or "").upper().replace("-", "_")
            if mode != "PRODUCT_FACTORY_CONTINUE":
                continue
            params = row.get("params") if isinstance(row.get("params"), dict) else {}
            if str(params.get("product_factory_run_id") or "") == run_id:
                return {
                    "ok": True,
                    "skipped": True,
                    "reason": "continue_already_queued",
                    "project_id": project_id,
                    "run_id": run_id,
                    "existing_id": row.get("id"),
                }

    eid = f"pfc-{uuid.uuid4().hex[:12]}"
    fp = f"product-factory-continue:{run_id}:{trigger_entry_id or eid}"
    params: dict[str, Any] = {
        "project_id": project_id,
        "product_factory_run_id": run_id,
        "trigger_entry_id": trigger_entry_id,
        "continued_at": _utc_iso(),
    }
    if agent_phase_complete:
        params["agent_phase_complete"] = agent_phase_complete
    return append_lane_queue_entry(
        vault_root,
        lane=lane,
        mode="PRODUCT_FACTORY_CONTINUE",
        params=params,
        entry_id=eid,
        source=source,
        fingerprint=fp,
    )


def maybe_append_continues_for_consumed_entries(
    vault_root: Path,
    *,
    lane: str | None,
    consumed_entries: list[QueueEntry],
) -> list[dict[str, Any]]:
    """After successful Layer 1 consume — append continue for product-factory agent beats."""
    if not lane:
        return []
    written: list[dict[str, Any]] = []
    seen_run: set[str] = set()
    for entry in consumed_entries:
        row = entry.model_dump(mode="json")
        if not entry_triggers_product_factory_continue(row):
            continue
        params = row.get("params") if isinstance(row.get("params"), dict) else {}
        run_id = str(params.get("product_factory_run_id") or "")
        project_id = str(
            entry.project_id or params.get("project_id") or "genesis-mythos-master"
        )
        dedupe = f"{run_id}:{entry.id}"
        if dedupe in seen_run:
            continue
        seen_run.add(dedupe)
        phase_complete = _agent_phase_from_entry(row)
        out = append_product_factory_continue(
            vault_root,
            lane=lane,
            project_id=project_id,
            run_id=run_id,
            trigger_entry_id=str(entry.id),
            agent_phase_complete=phase_complete,
        )
        written.append(out)
    return written
