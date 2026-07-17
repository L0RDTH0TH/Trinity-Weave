"""Scoped Cursor agent handoff for one implementation milestone."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .persona_handoff import format_persona_block, merge_persona_into_params


def _mission_first_block(
    vault_root: Path,
    params: dict[str, Any],
) -> str:
    """SIB/LMB-first cognitive block for Implementation Cell seats."""
    sib_path = str(params.get("slice_brief_path") or "")
    mission_path = str(params.get("lane_mission_path") or "")
    ux_ids = params.get("ux_bullet_ids") or []
    if not sib_path and not mission_path:
        return ""

    mission_body = ""
    if mission_path:
        mp = vault_root / mission_path
        if mp.is_file():
            mission_body = mp.read_text(encoding="utf-8", errors="replace")[:3500]

    sib_excerpt = ""
    if sib_path:
        sp = vault_root / sib_path
        if sp.is_file():
            sib_excerpt = sp.read_text(encoding="utf-8", errors="replace")[:2000]

    ux_line = ", ".join(str(x) for x in ux_ids) if ux_ids else "(see mission)"
    block = (
        f"\n## Implementation Cell — mission-first\n\n"
        f"- **Slice brief (SIB):** `{sib_path or '(missing)'}`\n"
        f"- **Your lane mission (LMB):** `{mission_path or '(missing)'}`\n"
        f"- **UX bullets you own:** {ux_line}\n\n"
        f"**Restate the UX goal in one sentence before coding.**\n\n"
    )
    if mission_body:
        block += f"### Lane mission\n{mission_body}\n\n"
    if sib_excerpt:
        block += f"### Slice brief excerpt\n{sib_excerpt}\n\n"
    return block


def build_implementation_handoff(
    vault_root: Path,
    *,
    lane: str,
    entry: dict[str, Any],
    charter: dict[str, Any],
    goal_packet: dict[str, Any] | None,
) -> str:
    vault_root = vault_root.resolve()
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    milestone_id = str(params.get("milestone_id") or charter.get("milestone_id") or "").upper()
    repo_rel = str(
        params.get("repo_path")
        or (goal_packet or {}).get("planner_hints", {}).get("repo_path")
        or "5-Attachments/Code-Repos/genesis-mythos-demo/"
    ).rstrip("/")
    repo_abs = vault_root / repo_rel
    spec_ref = str(
        params.get("demo_spec_ref")
        or (goal_packet or {}).get("planner_hints", {}).get("demo_spec_ref")
        or "1-Projects/godot-genesis-mythos-master/Horizon-Q3-Demo-Spec.md"
    )
    guidance = str(params.get("user_guidance") or charter.get("done_when") or "")
    targets = charter.get("target_files") or []
    target_block = "\n".join(f"- `{repo_rel}/{t}`" for t in targets) if targets else "- (see demo spec scenes)"
    persona_params = merge_persona_into_params(dict(params))
    persona_block = format_persona_block(
        persona_params.get("persona_handoff")
        if isinstance(persona_params.get("persona_handoff"), dict)
        else {}
    )

    return (
        f"{persona_block}"
        f"You are the **Implementation Factory** agent for Track C (Horizon-Q3 Demo v1).\n\n"
        f"Vault root: `{vault_root}`\n"
        f"Lane: `{lane}`\n"
        f"Milestone: **{milestone_id}** (`IMPLEMENT_SLICE`)\n"
        f"Repo (edit in-vault): `{repo_rel}/`\n"
        f"Demo spec: `{spec_ref}`\n\n"
        f"## Objective\n{guidance}\n\n"
        f"## Acceptance ({milestone_id})\n{charter.get('done_when', '')}\n\n"
        f"## Target artifacts\n{target_block}\n\n"
        f"## Constraints\n"
        f"- Godot **4.6.3 .NET**, C# primary, Linux\n"
        f"- Edit files under `{repo_rel}/` only for engine work\n"
        f"- Do **not** run RESUME_ROADMAP, roadmap deepen, or sandbox lane work\n"
        f"- Do **not** edit `.cursor/rules/**`\n"
        f"- When done: ensure `dotnet build` passes in `{repo_rel}/`\n"
        f"- Append a one-line receipt stub to "
        f"`1-Projects/godot-genesis-mythos-master/GMM-Godot-Prototype-History.md` "
        f"under a `## {milestone_id} harness receipt` heading\n\n"
        f"## Finish\n"
        f"Implement **only** {milestone_id}. Do not start later milestones. "
        f"Report files created/changed and build result."
    )


def build_factory_lane_handoff(
    vault_root: Path,
    *,
    lane: str,
    entry: dict[str, Any],
    goal_packet: dict[str, Any] | None,
) -> str:
    vault_root = vault_root.resolve()
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    hints = (goal_packet or {}).get("planner_hints") or {}
    slice_id = str(params.get("slice_id") or "")
    lane_id = str(params.get("lane_id") or "")
    factory_name = str(params.get("factory_name") or lane_id)
    repo_rel = str(params.get("repo_path") or hints.get("repo_path") or "").rstrip("/")
    zone_write = params.get("zone_write") or []
    checklists = params.get("checklist_ids") or []
    zone_block = "\n".join(f"- `{repo_rel}/{z}`" for z in zone_write) if zone_write else "- (lane charter zone_write)"
    checklist_block = "\n".join(f"- `{c}`" for c in checklists) if checklists else "- (slice lane checklist)"

    mission_block = _mission_first_block(vault_root, params)

    catalog_row_id = str(params.get("catalog_row_id") or "")
    ux_feed = params.get("ux_feed") if isinstance(params.get("ux_feed"), dict) else {}
    vault_feed_block = ""
    if catalog_row_id or ux_feed:
        exec_pin = str(
            ux_feed.get("execution_pin_path") or params.get("execution_pin") or ""
        )
        target_depth = ux_feed.get("target_depth", params.get("target_depth"))
        dispatch_depth = ux_feed.get("dispatch_depth", params.get("dispatch_depth"))
        rollout = params.get("rollout_version")
        l5_path = str(ux_feed.get("l5_scope_path") or "")
        scope_path_rel = str(ux_feed.get("dispatch_scope_path") or "")
        vault_feed_block = (
            f"\n## UX pillar feed (authoritative)\n"
            f"- **catalog_row_id:** `{catalog_row_id or ux_feed.get('catalog_row_id')}`\n"
            f"- **dispatch_depth:** `{dispatch_depth}` (target `{target_depth}`) | **rollout:** `{rollout}`\n"
            f"- **L5 north star:** `{l5_path}`\n"
            f"- **dispatch scope:** `{scope_path_rel}`\n"
            f"- **execution_pin (context only):** `{exec_pin}`\n"
            f"- Implement **only** the scope for depth `{dispatch_depth}`; do not exceed this level.\n"
        )
        objective = str(params.get("vault_feed_objective") or "")
        if scope_path_rel:
            scope_file = vault_root / scope_path_rel
            if scope_file.is_file():
                objective = scope_file.read_text(encoding="utf-8", errors="replace")[:3200]
        if objective:
            vault_feed_block += f"\n### Depth scope (factory food)\n{objective}\n"

    persona_params = merge_persona_into_params(dict(params))
    ph = persona_params.get("persona_handoff")
    persona_block = format_persona_block(ph if isinstance(ph, dict) else {})
    lane_id = str(params.get("lane_id") or lane_id)

    return (
        f"{persona_block}"
        f"You are the **{factory_name}** factory lane agent (`half_b.lane.{lane_id}`).\n\n"
        f"Vault root: `{vault_root}`\n"
        f"Queue lane: `{lane}`\n"
        f"Factory lane: **{lane_id}**\n"
        f"Active slice: **{slice_id}** (`IMPLEMENT_SLICE` / `factory_lane`)\n"
        f"Game repo (edit in-vault): `{repo_rel}/`\n"
        f"Factory manifest: `1-Projects/{params.get('project_id') or 'godot-genesis-mythos-master'}/Factory-DRB/factory-project.yaml`\n"
        f"{mission_block}"
        f"{vault_feed_block}\n"
        f"## Objective\n"
        f"Implement your lane's work for slice `{slice_id}` on genesis-mythos-alpha. "
        f"Primary artifact: `{params.get('primary_artifact') or 'see lane charter'}`.\n\n"
        f"## Zone write (edit ONLY these paths under the game repo)\n{zone_block}\n\n"
        f"## Kinesthetic checklist IDs (design for these; operator confirms later)\n{checklist_block}\n\n"
        f"## Constraints\n"
        f"- Godot **4.6.3 .NET**, C# primary, Linux\n"
        f"- **No** Q3 graybox / demo acceptance remnants on play path\n"
        f"- **No** RESUME_ROADMAP, roadmap deepen, or sandbox lane work\n"
        f"- Do **not** edit `.cursor/rules/**`\n"
        f"- `dotnet build` must pass in `{repo_rel}/`\n"
        f"- Launch path: `{hints.get('launch_scene') or 'LaunchShell.tscn'}` → PlayRegion\n\n"
        f"## Finish\n"
        f"Complete only this lane job for `{slice_id}`. Report files changed and build result.\n"
        f"Include `lane_persona_attestation` in your lane receipt JSON "
        f"(persona_id: half_b.lane.{lane_id}, wrote_paths, persona_violations)."
    )
