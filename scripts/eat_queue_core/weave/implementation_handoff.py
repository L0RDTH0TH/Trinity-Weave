"""Scoped Cursor agent handoff for one implementation milestone / factory lane."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .persona_handoff import format_persona_block, merge_persona_into_params


def _proof_shape(params: dict[str, Any], armed: dict[str, Any] | None) -> str:
    for blob in (params, armed or {}):
        ps = str((blob or {}).get("proof_shape") or "").strip().lower()
        if ps:
            return ps
    return ""


def _catalog_row_named_on_map(
    vault_root: Path,
    *,
    catalog_row_id: str,
    ticket_map_id: str,
    project_id: str,
) -> bool:
    """True only when the map row text names this catalog_row_id."""
    if not catalog_row_id or not ticket_map_id:
        return False
    try:
        from .factory.prefer_map_fidelity import row_names_field_value
        from .factory.ticket_map_schema import load_ticket_map_rows
    except ImportError:
        from eat_queue_core.weave.factory.prefer_map_fidelity import (  # type: ignore
            row_names_field_value,
        )
        from eat_queue_core.weave.factory.ticket_map_schema import (  # type: ignore
            load_ticket_map_rows,
        )
    rows = load_ticket_map_rows(
        vault_root, ticket_map_id=ticket_map_id, project_id=project_id or None
    )
    row = rows.get(ticket_map_id)
    if row is None:
        return False
    return row_names_field_value(row, "catalog_row_id", catalog_row_id)


def _load_armed_from_params(
    vault_root: Path, params: dict[str, Any]
) -> dict[str, Any]:
    rel = str(params.get("armed_packet_path") or "").strip()
    if not rel:
        return {}
    path = vault_root / rel
    if not path.is_file():
        return {}
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _mission_first_block(
    vault_root: Path,
    params: dict[str, Any],
    *,
    proof_shape: str,
) -> str:
    """SIB/LMB-first cognitive block — no UX sermon on contract eats."""
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
    )
    if proof_shape != "contract":
        block += "**Restate the UX goal in one sentence before coding.**\n\n"
    else:
        block += (
            "**Contract seat:** implement the Prefer invariant / behavior keys only. "
            "Do not expand into a demo moment.\n\n"
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
    armed = _load_armed_from_params(vault_root, params)
    proof_shape = _proof_shape(params, armed)
    milestone_id = str(params.get("milestone_id") or charter.get("milestone_id") or "").upper()
    hints = (goal_packet or {}).get("planner_hints") or {}
    repo_rel = str(
        params.get("repo_path")
        or hints.get("repo_path")
        or armed.get("live_write_target")
        or ""
    ).rstrip("/")
    if not repo_rel:
        repo_rel = "(missing — set factory-project.yaml game_repo_path / params.repo_path)"
    spec_ref = str(
        params.get("demo_spec_ref")
        or hints.get("demo_spec_ref")
        or ""
    ).strip()
    guidance = str(params.get("user_guidance") or charter.get("done_when") or "")
    targets = charter.get("target_files") or []
    target_block = (
        "\n".join(f"- `{repo_rel}/{t}`" for t in targets)
        if targets
        else "- (see Prefer / charter targets)"
    )
    persona_params = merge_persona_into_params(dict(params))
    persona_block = format_persona_block(
        persona_params.get("persona_handoff")
        if isinstance(persona_params.get("persona_handoff"), dict)
        else {}
    )
    spec_line = f"Spec ref: `{spec_ref}`\n" if spec_ref else ""

    return (
        f"{persona_block}"
        f"You are the **Implementation Factory** agent.\n\n"
        f"Vault root: `{vault_root}`\n"
        f"Lane: `{lane}`\n"
        f"Milestone: **{milestone_id}** (`IMPLEMENT_SLICE`)\n"
        f"Repo (edit in-vault): `{repo_rel}/`\n"
        f"{spec_line}\n"
        f"## Objective\n{guidance}\n\n"
        f"## Acceptance ({milestone_id})\n{charter.get('done_when', '')}\n\n"
        f"## Target artifacts\n{target_block}\n\n"
        f"## Constraints\n"
        f"- Edit files under `{repo_rel}/` only for engine work\n"
        f"- Do **not** run RESUME_ROADMAP, roadmap deepen, or sandbox lane work\n"
        f"- Do **not** edit `.cursor/rules/**`\n"
        f"- Build only if `engine.yaml` `build_command` is non-empty (no invented build)\n\n"
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
    armed = _load_armed_from_params(vault_root, params)
    proof_shape = _proof_shape(params, armed)
    hints = (goal_packet or {}).get("planner_hints") or {}
    slice_id = str(params.get("slice_id") or armed.get("slice_id") or "")
    # lane_id / launch_scene from Prefer **fields** only (never body scan).
    from .factory.prefer_map_fidelity import (
        lane_id_from_armed_fields,
        launch_scene_from_armed_fields,
    )

    lane_id = (
        lane_id_from_armed_fields(armed)
        or str(params.get("lane_id") or "").strip()
    )
    factory_name = str(params.get("factory_name") or lane_id or "factory_lane")
    repo_rel = str(
        params.get("repo_path")
        or hints.get("repo_path")
        or armed.get("live_write_target")
        or ""
    ).rstrip("/")
    zone_write = params.get("zone_write") or []
    checklists = params.get("checklist_ids")
    if checklists is None:
        checklists = armed.get("checklist_ids") or []
    zone_block = (
        "\n".join(f"- `{repo_rel}/{z}`" for z in zone_write)
        if zone_write
        else "- (lane charter zone_write)"
    )
    checklist_block = (
        "\n".join(f"- `{c}`" for c in checklists)
        if checklists
        else "- (none — contract/Prefer declared empty)"
    )

    mission_block = _mission_first_block(
        vault_root, params, proof_shape=proof_shape
    )

    catalog_row_id = str(
        params.get("catalog_row_id") or armed.get("catalog_row_id") or ""
    ).strip()
    ux_feed = params.get("ux_feed") if isinstance(params.get("ux_feed"), dict) else {}
    ticket_map_id = str(
        params.get("ticket_map_id") or armed.get("ticket_map_id") or ""
    ).strip()
    project_id = str(
        params.get("project_id") or armed.get("project_id")
    )
    vault_feed_block = ""
    allow_ux = False
    if catalog_row_id or ux_feed:
        if ticket_map_id and catalog_row_id:
            allow_ux = _catalog_row_named_on_map(
                vault_root,
                catalog_row_id=catalog_row_id,
                ticket_map_id=ticket_map_id,
                project_id=project_id,
            )
        if allow_ux and proof_shape != "contract":
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
                f"- **dispatch_depth:** `{dispatch_depth}` (target `{target_depth}`) | "
                f"**rollout:** `{rollout}`\n"
                f"- **L5 north star:** `{l5_path}`\n"
                f"- **dispatch scope:** `{scope_path_rel}`\n"
                f"- **execution_pin (context only):** `{exec_pin}`\n"
                f"- Implement **only** the scope for depth `{dispatch_depth}`; "
                f"do not exceed this level.\n"
            )
            objective = str(params.get("vault_feed_objective") or "")
            if scope_path_rel:
                scope_file = vault_root / scope_path_rel
                if scope_file.is_file():
                    objective = scope_file.read_text(
                        encoding="utf-8", errors="replace"
                    )[:3200]
            if objective:
                vault_feed_block += f"\n### Depth scope (factory food)\n{objective}\n"

    persona_params = merge_persona_into_params(dict(params))
    ph = persona_params.get("persona_handoff")
    persona_block = format_persona_block(ph if isinstance(ph, dict) else {})

    launch = launch_scene_from_armed_fields(armed) or str(
        hints.get("launch_scene") or ""
    ).strip()
    launch_line = (
        f"- Launch scene (Prefer field): `{launch}`\n" if launch else ""
    )
    lane_label = f"`{lane_id}`" if lane_id else "(Prefer field lane_id unset)"

    return (
        f"{persona_block}"
        f"You are the **{factory_name}** factory lane agent.\n\n"
        f"Vault root: `{vault_root}`\n"
        f"Queue lane: `{lane}`\n"
        f"Factory lane: **{lane_label}**\n"
        f"Active slice: **{slice_id}** (`IMPLEMENT_SLICE` / `factory_lane`)\n"
        f"Game repo (edit in-vault): `{repo_rel or '(missing)'}/`\n"
        f"Factory manifest: `1-Projects/{project_id}/Factory-DRB/factory-project.yaml`\n"
        f"{mission_block}"
        f"{vault_feed_block}\n"
        f"## Objective\n"
        f"Implement your lane's work for slice `{slice_id}` per the Prefer packet. "
        f"Primary artifact: `{params.get('primary_artifact') or 'see Prefer / lane charter'}`.\n\n"
        f"## Zone write (edit ONLY these paths under the game repo)\n{zone_block}\n\n"
        f"## Kinesthetic checklist IDs\n{checklist_block}\n\n"
        f"## Constraints\n"
        f"- **No** RESUME_ROADMAP, roadmap deepen, or sandbox lane work\n"
        f"- Do **not** edit `.cursor/rules/**`\n"
        f"- Build only if `engine.yaml` `build_command` is non-empty (no invented build)\n"
        f"{launch_line}\n"
        f"## Finish\n"
        f"Complete only this lane job for `{slice_id}`. Report files changed and build result.\n"
    )
