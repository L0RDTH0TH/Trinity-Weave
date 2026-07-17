"""Enqueue Slice Producer agent beats on lane PQ (Half B PM persona)."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from ...lane_queue_io import append_lane_queue_entry
from .work_order_translate import assemble_pillar_packet


def enqueue_slice_producer_compose(
    vault_root: Path,
    *,
    lane: str,
    project_id: str,
    run_id: str,
    active_slice: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Pre-assemble pillar packet; enqueue SLICE_PRODUCER_COMPOSE for PM agent."""
    vault_root = vault_root.resolve()
    producer_run_id = f"sp-{run_id[:8]}-{uuid.uuid4().hex[:6]}"
    packet = assemble_pillar_packet(
        vault_root,
        project_id=project_id,
        producer_run_id=producer_run_id,
        active_slice=active_slice,
    )
    if packet is None:
        return {"ok": False, "error": "assemble_pillar_packet_failed"}

    slice_id = str(packet.get("slice_id") or "")
    tech_rel = f".technical/factory/slice-briefs/{slice_id}/pillar-packet.json"
    packet_path = vault_root / tech_rel
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    import json

    packet_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")

    eid = f"sp-compose-{uuid.uuid4().hex[:10]}"
    return append_lane_queue_entry(
        vault_root,
        lane=lane.strip().lower(),
        mode="SLICE_PRODUCER_COMPOSE",
        params={
            "project_id": project_id,
            "slice_id": slice_id,
            "producer_run_id": producer_run_id,
            "pillar_packet_path": tech_rel,
            "product_factory_run_id": run_id,
            "queue_next": True,
            "agent_mode": "compose",
        },
        entry_id=eid,
        source="product_factory_conductor",
        fingerprint=f"slice-producer-compose:{run_id}:{slice_id}",
    )


def enqueue_slice_producer_review(
    vault_root: Path,
    *,
    lane: str,
    project_id: str,
    run_id: str,
    slice_id: str,
    wave: int = 1,
) -> dict[str, Any]:
    """Enqueue SLICE_PRODUCER_REVIEW after wave lanes complete."""
    eid = f"sp-review-{uuid.uuid4().hex[:10]}"
    return append_lane_queue_entry(
        vault_root,
        lane=lane.strip().lower(),
        mode="SLICE_PRODUCER_REVIEW",
        params={
            "project_id": project_id,
            "slice_id": slice_id,
            "wave": wave,
            "queue_lane": lane.strip().lower(),
            "product_factory_run_id": run_id,
            "queue_next": True,
            "agent_mode": "review",
        },
        entry_id=eid,
        source="factory_lane_runner",
        fingerprint=f"slice-producer-review:{run_id}:{slice_id}:w{wave}",
    )
