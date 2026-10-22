"""Six Implementation Factory lane agents — distinct produce paths inside the factory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .drop_contract_base import DROP_CONTRACTS, LANE_DROP_TYPE
from .lane_charters import load_lane_charter

import yaml


@dataclass(frozen=True)
class LaneAgentSpec:
    lane_id: str
    factory_name: str
    engine_adapter: str
    mcp_adapter: str
    drop_contract: str
    produces: str
    consumes: tuple[str, ...]
    verify_steps: tuple[str, ...]
    default_review_passes: tuple[str, ...]

    def handoff(
        self,
        vault_root: Path,
        *,
        queue_lane: str,
        slice_id: str,
        repo_rel: str,
        job: dict[str, Any],
        goal_packet: dict[str, Any] | None,
    ) -> str:
        """Keys-only handoff — does not invent method from baked produces."""
        del self, repo_rel, slice_id
        from ..implementation_handoff import build_implementation_handoff

        entry = {"params": dict(job) if isinstance(job, dict) else {}}
        return build_implementation_handoff(
            vault_root,
            lane=queue_lane or "implementation",
            entry=entry,
            charter={},
            goal_packet=goal_packet,
        )


LANE_AGENTS: dict[str, LaneAgentSpec] = {}


def get_lane_agent(lane_id: str) -> LaneAgentSpec | None:
    return LANE_AGENTS.get(lane_id.strip().lower())


def enrich_job_from_charter(vault_root: Path, job: dict[str, Any]) -> dict[str, Any]:
    lane_id = str(job.get("lane_id") or "")
    agent = get_lane_agent(lane_id)
    charter = load_lane_charter(vault_root, lane_id)
    if charter is not None:
        raw = yaml.safe_load(charter.path.read_text(encoding="utf-8")) or {}
        if isinstance(raw, dict):
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
                "zone_write",
                "primary_artifact",
            ):
                if key in raw and key not in job:
                    job[key] = raw[key]
            if not job.get("factory_name"):
                job["factory_name"] = raw.get("factory_name") or charter.factory_name
    if agent and not job.get("drop_contract"):
        job["drop_contract"] = agent.drop_contract
    if agent and not job.get("mcp_adapter"):
        job["mcp_adapter"] = agent.mcp_adapter
    return job


def build_lane_agent_handoff(
    vault_root: Path,
    *,
    queue_lane: str,
    job: dict[str, Any],
    goal_packet: dict[str, Any] | None,
) -> str:
    lane_id = str(job.get("lane_id") or "")
    agent = get_lane_agent(lane_id)
    if agent is None:
        from ..implementation_handoff import build_factory_lane_handoff

        return build_factory_lane_handoff(
            vault_root,
            lane=queue_lane,
            entry={"params": job},
            goal_packet=goal_packet,
        )
    hints = (goal_packet or {}).get("planner_hints") or {}
    repo_rel = str(job.get("repo_path") or hints.get("repo_path") or "")
    slice_id = str(job.get("slice_id") or "")
    params = dict(job)
    if not params.get("slice_brief_path") and job.get("slice_brief_path"):
        params["slice_brief_path"] = job.get("slice_brief_path")
    return agent.handoff(
        vault_root,
        queue_lane=queue_lane,
        slice_id=slice_id,
        repo_rel=repo_rel,
        job=params,
        goal_packet=goal_packet,
    )


def lane_review_passes(job: dict[str, Any]) -> list[str]:
    from .prefer_authorship_contract import slice_requires_prefer_authorship

    lane_id = str(job.get("lane_id") or "")
    agent = get_lane_agent(lane_id)
    from_charter = job.get("review_passes") or []
    if from_charter:
        passes = [str(x) for x in from_charter]
    elif agent:
        passes = list(agent.default_review_passes)
    else:
        passes = ["structure_pass", "interpretation_pass"]
    # Product Prefer authorship seat — every Prefer worldgen/terrain3d_feed weld.
    if slice_requires_prefer_authorship(str(job.get("slice_id") or ""), job):
        if "prefer_authorship_pass" not in passes:
            passes.append("prefer_authorship_pass")
    return passes
