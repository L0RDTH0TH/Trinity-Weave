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
        vault_root = vault_root.resolve()
        from ..implementation_handoff import _mission_first_block

        hints = (goal_packet or {}).get("planner_hints") or {}
        zone_write = job.get("zone_write") or []
        checklists = job.get("checklist_ids") or []
        drb_ref = str(job.get("drb_ref") or "")
        drop_manifest = DROP_CONTRACTS.get(self.drop_contract, "")
        mission_block = _mission_first_block(vault_root, job)
        zone_block = (
            "\n".join(f"- `{repo_rel.rstrip('/')}/{z}`" for z in zone_write)
            if zone_write
            else f"- Only paths under `{repo_rel}` matching lane `{self.lane_id}` zone"
        )
        checklist_block = (
            "\n".join(f"- `{c}`" for c in checklists) if checklists else "- (usability DRB checklist IDs)"
        )
        consume_block = (
            "\n".join(f"- `{c}` drop contract must exist before you integrate" for c in self.consumes)
            if self.consumes
            else "- No upstream drop required for this lane"
        )
        verify_block = "\n".join(f"- `{v}`" for v in self.verify_steps)

        return (
            f"# Implementation Factory — **{self.factory_name}** lane agent\n\n"
            f"You are agent **`{self.lane_id}`** inside the **Implementation Factory** "
            f"(not a roadmap item — a factory worker).\n\n"
            f"| Field | Value |\n|-------|-------|\n"
            f"| Vault | `{vault_root}` |\n"
            f"| Queue lane | `{queue_lane}` |\n"
            f"| Factory lane | `{self.lane_id}` |\n"
            f"| Slice | `{slice_id}` |\n"
            f"| MCP adapter | `{self.mcp_adapter}` |\n"
            f"| Engine | `{self.engine_adapter}` |\n"
            f"| Drop contract | `{self.drop_contract.upper()}` → `{repo_rel}/{drop_manifest}` |\n\n"
            f"{mission_block}"
            f"## Produce\n{self.produces}\n\n"
            f"## Consume (drops only — no cross-zone edits)\n{consume_block}\n\n"
            f"## Zone write (ONLY these paths)\n{zone_block}\n\n"
            f"## DRB\n`{drb_ref or 'see lane charter'}`\n\n"
            f"## Kinesthetic checklist IDs (operator confirms — you design for them)\n{checklist_block}\n\n"
            f"## Post-work verification (factory will run)\n{verify_block}\n\n"
            f"## Hard rules\n"
            f"- **No** claiming Success without real artifacts in zone + drop manifest update\n"
            f"- **No** Q3 graybox / demo acceptance copy on play path\n"
            f"- **No** `.cursor/rules/**` edits\n"
            f"- **No** RESUME_ROADMAP / roadmap deepen\n"
            f"- Module lane: integrate via drops only — never rewrite `assets/` or `content/` roots\n"
            f"- Launch path: `{hints.get('launch_scene', 'LaunchShell.tscn')}` → PlayRegion\n"
            f"- `dotnet build` must pass when this lane touches C#\n\n"
            f"## Runtime logging (factory bus)\n"
            f"- Generated C# **must** call `AlphaFactoryLog.Emit` on state transitions, checklist boundaries, and degradation callbacks\n"
            f"- **Forbidden:** seat-critical events via raw `GD.Print` only (`Degrade_FailVisible` anti-pattern)\n"
            f"- Map touched checklist IDs to explicit log emissions at boundaries\n\n"
            f"## Report on finish\n"
            f"List every file changed (repo-relative), drop IDs registered, and build result."
        )


LANE_AGENTS: dict[str, LaneAgentSpec] = {
    "asset": LaneAgentSpec(
        lane_id="asset",
        factory_name="AssetContent",
        engine_adapter="blender_mcp",
        mcp_adapter="blender :9876",
        drop_contract="adc",
        produces="Meshes, rigs, GLTF exports, env kit scenes under assets/; register ADC manifest rows.",
        consumes=(),
        verify_steps=("adc_manifest_has_drops", "structure_pass", "compliance_pass"),
        default_review_passes=("structure_pass", "compliance_pass", "art_direction_pass"),
    ),
    "techart": LaneAgentSpec(
        lane_id="techart",
        factory_name="TechArt",
        engine_adapter="godot_4_6_3_dotnet",
        mcp_adapter="godot materials/shaders",
        drop_contract="tac",
        produces="Materials, shaders, LOD rules, import presets under assets/_techart/; TAC manifest.",
        consumes=("adc",),
        verify_steps=("tac_manifest_has_drops", "depends_on_adc", "structure_pass"),
        default_review_passes=("structure_pass", "art_direction_pass", "compliance_pass"),
    ),
    "content": LaneAgentSpec(
        lane_id="content",
        factory_name="Content",
        engine_adapter="vault_only",
        mcp_adapter="vault_only",
        drop_contract="cdc",
        produces="World/sim/narrative data, menu-tree YAML, canon refs under content/; CDC + canon-index.",
        consumes=(),
        verify_steps=("cdc_manifest_has_drops", "canon_pass", "structure_pass"),
        default_review_passes=("structure_pass", "interpretation_pass", "canon_pass", "compliance_pass"),
    ),
    "presentation": LaneAgentSpec(
        lane_id="presentation",
        factory_name="Presentation",
        engine_adapter="godot_4_6_3_dotnet",
        mcp_adapter="godot :6505 UI scenes",
        drop_contract="pdc",
        produces="Control scenes, HUD wiring, LaunchShell/GameHud polish; PDC manifest; no sim logic in UI.",
        consumes=("cdc",),
        verify_steps=("pdc_manifest_has_drops", "depends_on_cdc", "usability_pass", "structure_pass"),
        default_review_passes=(
            "interpretation_pass",
            "structure_pass",
            "usability_pass",
            "integration_pass",
        ),
    ),
    "audio": LaneAgentSpec(
        lane_id="audio",
        factory_name="Audio",
        engine_adapter="vault_only",
        mcp_adapter="vault + optional TTS tooling",
        drop_contract="audc",
        produces="SFX/music stems, cue maps, TTS scripts under audio/; AuDC manifest (authored clips v1).",
        consumes=(),
        verify_steps=("audc_manifest_has_drops", "narrative_audio_pass", "compliance_pass"),
        default_review_passes=("structure_pass", "narrative_audio_pass", "compliance_pass"),
    ),
    "module": LaneAgentSpec(
        lane_id="module",
        factory_name="Module",
        engine_adapter="godot_4_6_3_dotnet",
        mcp_adapter="godot :6505",
        drop_contract="",
        produces="Systems/, Core/ integration glue, PlayRegion runtime; consumes ADC/TAC/CDC/PDC/AuDC drops only.",
        consumes=("adc", "tac", "cdc", "pdc"),
        verify_steps=(
            "depends_on_drops",
            "module_fit_pass",
            "integration_pass",
            "dotnet_build",
        ),
        default_review_passes=(
            "interpretation_pass",
            "structure_pass",
            "module_fit_pass",
            "integration_pass",
            "reliability_pass",
        ),
    ),
}


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
    lane_id = str(job.get("lane_id") or "")
    agent = get_lane_agent(lane_id)
    from_charter = job.get("review_passes") or []
    if from_charter:
        return [str(x) for x in from_charter]
    if agent:
        return list(agent.default_review_passes)
    return ["structure_pass", "interpretation_pass"]
