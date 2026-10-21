"""Lane dispatch packets — checklists from Prefer/job only; no baked slice map."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .lane_charters import load_lane_charter


@dataclass(frozen=True)
class LaneDispatchJob:
    lane_id: str
    factory_name: str
    primary_artifact: str
    slice_id: str
    zone_write: tuple[str, ...]
    agent_mode: str
    checklist_ids: tuple[str, ...]
    game_repo_rel: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "lane_id": self.lane_id,
            "factory_name": self.factory_name,
            "primary_artifact": self.primary_artifact,
            "slice_id": self.slice_id,
            "zone_write": list(self.zone_write),
            "agent_mode": self.agent_mode,
            "checklist_ids": list(self.checklist_ids),
            "game_repo_rel": self.game_repo_rel,
        }


def enrich_job_from_charter(vault_root: Path, job: dict[str, Any]) -> dict[str, Any]:
    lane_id = str(job.get("lane_id") or "")
    charter = load_lane_charter(vault_root, lane_id)
    if charter is None:
        return job
    raw = yaml.safe_load(charter.path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        return job
    for key in (
        "depends_on_drops",
        "blocks_parallel_lanes",
        "pinned_drop_receipt_ids",
        "shared_surface_locks",
        "target_files",
        "drb_ref",
        "review_passes",
        "requires_adc",
        "requires_tac",
        "requires_cdc",
        "requires_pdc",
        "requires_audc",
        "interpretation_required",
        "host_touch_budget",
    ):
        if key in raw and key not in job:
            job[key] = raw[key]
    return job


def build_lane_job(
    vault_root: Path,
    *,
    lane_id: str,
    slice_id: str,
    game_repo_rel: str,
) -> LaneDispatchJob | None:
    charter = load_lane_charter(vault_root, lane_id)
    if charter is None:
        return None
    zone_write: tuple[str, ...] = ()
    raw = yaml.safe_load(charter.path.read_text(encoding="utf-8")) or {}
    zw = raw.get("zone_write") or []
    if isinstance(zw, list):
        zone_write = tuple(str(z) for z in zw)
    # Checklists: Prefer/job only — never a baked slice→lane map.
    return LaneDispatchJob(
        lane_id=lane_id,
        factory_name=charter.factory_name,
        primary_artifact=charter.primary_artifact,
        slice_id=slice_id,
        zone_write=zone_write,
        agent_mode="IMPLEMENT_SLICE",
        checklist_ids=(),
        game_repo_rel=game_repo_rel,
    )


def dispatch_slice_lanes(
    vault_root: Path,
    *,
    slice_id: str,
    lane_ids: tuple[str, ...],
    game_repo_rel: str,
) -> list[LaneDispatchJob]:
    jobs: list[LaneDispatchJob] = []
    for lid in lane_ids:
        job = build_lane_job(
            vault_root, lane_id=lid, slice_id=slice_id, game_repo_rel=game_repo_rel
        )
        if job is not None:
            jobs.append(job)
    return jobs
