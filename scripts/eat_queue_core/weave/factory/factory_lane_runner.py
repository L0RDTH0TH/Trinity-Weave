"""End-to-end factory lane execution — six agents, seats, honesty gate."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ...goal_authority_io import load_goal_authority
from ..engine_preflight import run_engine_preflight
from .agent_changed_paths import extract_changed_paths_from_agent
from .drop_contract_base import LANE_DROP_TYPE, register_lane_drop
from .factory_correlation import FactoryRunContext, append_factory_event, append_gate_log
from .factory_honesty_gate import build_intent_receipt, enforce_factory_success
from .factory_orchestrator import DEFAULT_QUEUE_REL, load_alpha_queue
from .factory_self_heal import attempt_self_heal_chain, handle_seat_failure_escalation
from .interpretation_pass import run_interpretation_pass
from .lane_agent_registry import build_lane_agent_handoff, enrich_job_from_charter, lane_review_passes
from .merge_barrier import acquire_lane_job, check_job_allowed, release_lane_job
from .factory_output_gate import apply_factory_output_gate_to_trace
from .factory_run_summary import write_lane_run_summary, write_slice_run_summary
from .playtest_brief import write_playtest_brief
from .review_pass_runner import run_slice_exit_gates
from .slice_advance import (
    advance_alpha_queue_if_ready,
    mark_lane_complete,
    run_post_slice_advance_hooks,
    slice_lanes_complete,
)
from ..user_story.depth_bump import try_weld_depth_bump_after_slice
from ..user_story.product_factory_state import (
    FACTORY_CELL_COMPLETE,
    load_product_factory,
    reopen_product_factory_loop_3,
    release_pm_review_lock,
    save_product_factory,
    try_acquire_pm_review_lock,
    update_implementation_cell,
)
from ..persona_handoff import synthetic_persona_attestation, merge_lane_persona_attestation
from ..user_story.work_order_translate import FEED_VAULT_ROADMAP
from .factory_pq_stage import append_factory_rework
from .slice_producer_harness import (
    load_cell_dispatch_plan,
    run_slice_producer_review,
    technical_slice_dir,
)

from ..mcp_postedit_validate import run_mcp_postedit_validate
from .factory_machine_state import (
    init_machine_state,
    mark_complete_state,
    mark_jam,
    save_machine_state,
    set_machine,
)


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _persist_state(vault_root: Path, state: dict[str, Any]) -> None:
    try:
        save_machine_state(vault_root, state)
    except (OSError, ValueError):
        pass


def _run_lane_seats(
    vault_root: Path,
    *,
    ctx: FactoryRunContext,
    job: dict[str, Any],
    repo_rel: str,
    lane_id: str,
    changed_paths: tuple[str, ...],
) -> dict[str, Any]:
    lane_gates = lane_review_passes(job)
    lane_seats = run_slice_exit_gates(
        vault_root,
        exit_gates=lane_gates,
        game_repo_rel=repo_rel,
        lane_id=lane_id,
        job=job,
        changed_paths=changed_paths,
        run_probes=True,
        stack_integrate_dry_run=False,
        lane_seat=True,
    )
    for gname, gres in lane_seats.get("passes", {}).items():
        append_gate_log(
            vault_root,
            gname,
            ok=gres.ok,
            run_id=ctx.run_id,
            chain_id=ctx.chain_id,
            slice_id=ctx.slice_id,
            lane_id=lane_id,
            violations=list(gres.little_val.anti_pattern_violations),
        )
    return lane_seats


def _seat_violations(lane_seats: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for gname, gres in lane_seats.get("passes", {}).items():
        if not gres.ok:
            out.extend([f"seat_fail:{gname}:{v}" for v in gres.little_val.anti_pattern_violations])
    return out or ["seat_fail:lane_seats"]


def _all_violations_healed(heal: list[Any]) -> bool:
    return bool(heal) and all(getattr(h, "healed", False) for h in heal)


def _build_replay_agent_out(vault_root: Path, agent_log_path: str) -> dict[str, Any]:
    rel = agent_log_path
    p = vault_root / rel
    if not p.is_file() and Path(agent_log_path).is_file():
        rel = str(Path(agent_log_path).resolve().relative_to(vault_root.resolve()))
    return {"ok": True, "skipped": True, "replay": True, "log_path": rel}


def _write_lane_receipt(
    vault_root: Path,
    *,
    slice_id: str,
    lane_id: str,
    receipt_id: str,
    ux_bullet_ids: list[Any],
    ok: bool = True,
    wrote_paths: list[str] | None = None,
    agent_out: dict[str, Any] | None = None,
    repo_rel: str = "",
    zone_write: list[str] | None = None,
    project_id: str = "",
) -> Path:
    import json

    receipts_dir = technical_slice_dir(vault_root, slice_id) / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)
    path = receipts_dir / f"{lane_id}.json"
    rel_receipt = str(path.relative_to(vault_root.resolve()))
    att, att_source = merge_lane_persona_attestation(
        lane_id=lane_id,
        agent_out=agent_out or {},
        changed_paths=list(wrote_paths or []),
        receipt_rel_path=rel_receipt,
    )
    if wrote_paths and repo_rel:
        from ..persona_handoff import validate_attestation_wrote_paths_in_repo

        zone_v = validate_attestation_wrote_paths_in_repo(
            att,
            repo_prefix=repo_rel,
            zone_write=zone_write,
        )
        if zone_v and att_source == "harness":
            paths = [p for p in (wrote_paths or []) if p] or [rel_receipt]
            att = synthetic_persona_attestation(f"half_b.lane.{lane_id}", paths)
    doc = {
        "ok": ok,
        "lane_id": lane_id,
        "slice_id": slice_id,
        "receipt_id": receipt_id,
        "ux_bullet_ids": ux_bullet_ids,
        "lane_persona_attestation": att,
        "attestation_source": att_source,
    }
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    if ok and project_id:
        try:
            from ..user_story.implementation_artifact_ledger import record_implementation_artifact

            record_implementation_artifact(
                vault_root,
                project_id,
                artifact_path=str(path.relative_to(vault_root.resolve())),
                event_type="lane_receipt",
                slice_id=slice_id,
            )
        except (OSError, ValueError):
            pass
    return path


def _wave_required_lanes(
    vault_root: Path,
    *,
    slice_id: str,
    params: dict[str, Any],
    vault_lanes: list[str],
) -> list[str]:
    cdp_rel = str(params.get("cell_dispatch_plan_path") or "")
    wave = int(params.get("wave") or 1)
    if cdp_rel:
        cdp = load_cell_dispatch_plan(vault_root, cdp_rel)
        if cdp:
            for wdef in cdp.get("waves") or []:
                if isinstance(wdef, dict) and int(wdef.get("wave") or 0) == wave:
                    lanes = [str(x) for x in (wdef.get("lanes") or []) if x]
                    if lanes:
                        return lanes
    if vault_lanes:
        return vault_lanes
    return []


def run_factory_lane_job(
    vault_root: Path,
    queue_lane: str,
    entry: dict[str, Any],
    *,
    params: dict[str, Any],
    dry_run: bool = False,
    parent_run_id: str | None = None,
    skip_agent: bool = False,
    skip_preflight: bool = False,
    run_agent_fn: Any = None,
    agent_log_path: str | None = None,
    resume_from: str | None = None,
    complete_pipeline: bool = True,
    auto_retry_seats: bool = True,
) -> dict[str, Any]:
    """Execute one factory_lane IMPLEMENT_SLICE with per-lane agent + review seats."""
    vault_root = vault_root.resolve()
    eid = str(entry.get("id") or "")
    slice_id = str(params.get("slice_id") or "")
    lane_id = str(params.get("lane_id") or "")
    project_id = str(entry.get("project_id") or params.get("project_id") or "godot-genesis-mythos-master")
    engine_adapter = str(params.get("engine_adapter") or "godot_4_6_3_dotnet")
    repo_rel = str(
        params.get("repo_path") or "5-Attachments/Code-Repos/genesis-mythos-alpha/"
    ).rstrip("/") + "/"
    packet = load_goal_authority(vault_root, queue_lane, require_confirmed=False)

    from .implementation_cursor import reconcile_implementation_cursor
    from ..user_story.product_factory_state import load_product_factory

    reconcile = reconcile_implementation_cursor(
        vault_root, project_id, packet or {}, lane=queue_lane
    )
    pf_pre = load_product_factory(vault_root, project_id)
    cell_pre = pf_pre.get("implementation_cell") if isinstance(pf_pre.get("implementation_cell"), dict) else {}
    cell_phase_pre = str(cell_pre.get("phase") or "")
    if cell_phase_pre in ("", "idle") and not reconcile.handoff_ready:
        return {
            "ok": False,
            "id": eid,
            "error": "implementation_handoff_blocked",
            "detail": reconcile.handoff_reason,
            "reconcile": reconcile.to_dict(),
            "segment": "IMPLEMENT_SLICE",
        }

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "id": eid,
            "slice_id": slice_id,
            "lane_id": lane_id,
            "segment": "IMPLEMENT_SLICE",
            "would_run_agent": True,
        }

    job: dict[str, Any] = {
        "lane_id": lane_id,
        "slice_id": slice_id,
        "repo_path": repo_rel,
        "zone_write": params.get("zone_write") or [],
        "factory_name": params.get("factory_name"),
        "primary_artifact": params.get("primary_artifact"),
        "checklist_ids": params.get("checklist_ids") or [],
        **{
            k: params[k]
            for k in params
            if k.startswith("depends_on")
            or k
            in (
                "blocks_parallel_lanes",
                "target_files",
                "drb_ref",
                "slice_brief_path",
                "lane_mission_path",
                "cell_dispatch_plan_path",
                "producer_run_id",
                "ux_bullet_ids",
                "wave",
                "rework_iteration",
                "catalog_row_id",
                "dispatch_depth",
                "target_depth",
            )
        },
    }
    enrich_job_from_charter(vault_root, job)

    ctx = FactoryRunContext.from_entry(
        entry, params, queue_lane=queue_lane, parent_run_id=parent_run_id
    )
    mstate = init_machine_state(
        entry_id=eid,
        slice_id=slice_id,
        lane_id=lane_id,
        queue_lane=queue_lane,
        run_id=ctx.run_id,
        chain_id=ctx.chain_id,
    )

    seats_only = resume_from == "seats" or (skip_agent and bool(agent_log_path))

    merge_check = check_job_allowed(vault_root, job, game_repo_rel=repo_rel)
    if not merge_check.allowed:
        mstate = mark_jam(mstate, machine="preflight", error="merge_barrier_blocked")
        _persist_state(vault_root, mstate)
        return {
            "ok": False,
            "id": eid,
            "slice_id": slice_id,
            "lane_id": lane_id,
            "error": "merge_barrier_blocked",
            "merge_barrier": merge_check.to_dict(),
            "segment": "IMPLEMENT_SLICE",
            "resume_from": "seats" if seats_only else "agent",
        }

    if not seats_only:
        interp = run_interpretation_pass(vault_root, lane_id=lane_id, job=job)
        mstate = set_machine(
            mstate,
            "interpretation",
            status="ok" if interp.ok else "fail",
            detail=interp.detail if hasattr(interp, "detail") else "",
        )
        append_gate_log(
            vault_root,
            "interpretation_pass",
            ok=interp.ok,
            run_id=ctx.run_id,
            chain_id=ctx.chain_id,
            slice_id=slice_id,
            lane_id=lane_id,
        )
        if not interp.ok:
            heal = attempt_self_heal_chain(vault_root, interp.little_val.anti_pattern_violations)
            esc = handle_seat_failure_escalation(
                vault_root,
                slice_id=slice_id,
                lane_id=lane_id,
                violations=list(interp.little_val.anti_pattern_violations),
                game_repo_rel=repo_rel,
                job=job,
                run_id=ctx.run_id,
                queue_lane=queue_lane,
            )
            mstate = mark_jam(mstate, machine="interpretation", error="interpretation_pass_failed")
            _persist_state(vault_root, mstate)
            return {
                "ok": False,
                "id": eid,
                "run_id": ctx.run_id,
                "chain_id": ctx.chain_id,
                "slice_id": slice_id,
                "lane_id": lane_id,
                "error": "interpretation_pass_failed",
                "interpretation": interp.to_dict(),
                "self_heal": [h.__dict__ for h in heal],
                "escalation": esc,
                "segment": "IMPLEMENT_SLICE",
                "resume_from": "interpretation",
            }

    acquire_lane_job(vault_root, job)
    append_factory_event(
        vault_root,
        queue_lane,
        "lane_job_start" if not seats_only else "lane_replay_seats",
        run_id=ctx.run_id,
        chain_id=ctx.chain_id,
        factory_lane=lane_id,
        slice_id=slice_id,
        parent_run_id=parent_run_id,
        message=f"factory_lane {lane_id}" + (" replay_seats" if seats_only else ""),
    )

    agent_out: dict[str, Any] = {"ok": True, "skipped": True}
    receipt_id = str(eid)
    receipt: dict[str, Any] = {"receipt_id": receipt_id}
    verify_preflight: dict[str, Any] = {"ok": True, "skipped": seats_only}

    if seats_only:
        if not agent_log_path:
            release_lane_job(vault_root, job, ok=False)
            mstate = mark_jam(mstate, machine="agent", error="no_agent_log_for_replay")
            _persist_state(vault_root, mstate)
            return {
                "ok": False,
                "id": eid,
                "slice_id": slice_id,
                "lane_id": lane_id,
                "error": "no_agent_log_for_replay",
                "segment": "IMPLEMENT_SLICE",
                "resume_from": "seats",
            }
        agent_out = _build_replay_agent_out(vault_root, agent_log_path)
        mstate = set_machine(mstate, "agent", status="ok", detail="replay_from_log")
        mstate = set_machine(mstate, "preflight", status="ok", detail="skipped_replay")
        mstate = set_machine(mstate, "post_preflight", status="ok", detail="skipped_replay")
        mstate["agent_log_path"] = agent_out.get("log_path")
    else:
        if not skip_preflight:
            preflight = run_engine_preflight(
                vault_root, repo_rel, requires_mcp=False, run_dotnet_build=True
            )
            mstate = set_machine(
                mstate,
                "preflight",
                status="ok" if preflight.get("ok") else "fail",
                detail=str(preflight.get("error") or ""),
            )
            if not preflight.get("ok"):
                release_lane_job(vault_root, job, ok=False)
                mstate = mark_jam(mstate, machine="preflight", error="engine_preflight_failed")
                _persist_state(vault_root, mstate)
                return {
                    "ok": False,
                    "id": eid,
                    "slice_id": slice_id,
                    "lane_id": lane_id,
                    "error": "engine_preflight_failed",
                    "preflight": preflight,
                    "segment": "IMPLEMENT_SLICE",
                    "resume_from": "preflight",
                }
        else:
            mstate = set_machine(mstate, "preflight", status="ok", detail="skipped")

        handoff = build_lane_agent_handoff(
            vault_root, queue_lane=queue_lane, job=job, goal_packet=packet
        )
        if not skip_agent:
            if run_agent_fn is None:
                from ..implement_slice import run_implementation_agent

                run_agent_fn = run_implementation_agent
            log_path = (
                vault_root
                / ".technical"
                / "Run-Telemetry"
                / queue_lane
                / f"factory-lane-{lane_id}-{slice_id}-{_utc_stamp()}.log"
            )
            agent_out = run_agent_fn(vault_root, handoff, dry_run=False, log_path=log_path)
        mstate = set_machine(
            mstate,
            "agent",
            status="ok" if agent_out.get("ok") else "fail",
            detail=str(agent_out.get("error") or ""),
        )
        if agent_out.get("log_path"):
            mstate["agent_log_path"] = agent_out["log_path"]

        if not agent_out.get("ok"):
            release_lane_job(vault_root, job, ok=False)
            mstate = mark_jam(
                mstate,
                machine="agent",
                error="agent_run_failed",
                agent_log_path=agent_out.get("log_path"),
            )
            _persist_state(vault_root, mstate)
            append_factory_event(
                vault_root,
                queue_lane,
                "lane_job_fail",
                run_id=ctx.run_id,
                chain_id=ctx.chain_id,
                factory_lane=lane_id,
                slice_id=slice_id,
                status="failure",
            )
            return {
                "ok": False,
                "id": eid,
                "slice_id": slice_id,
                "lane_id": lane_id,
                "error": "agent_run_failed",
                "agent": agent_out,
                "segment": "IMPLEMENT_SLICE",
                "resume_from": "agent",
            }

        verify_preflight = run_engine_preflight(
            vault_root, repo_rel, requires_mcp=False, run_dotnet_build=True
        )
        mstate = set_machine(
            mstate,
            "post_preflight",
            status="ok" if verify_preflight.get("ok") else "fail",
            detail=str(verify_preflight.get("error") or ""),
        )
        if not verify_preflight.get("ok"):
            release_lane_job(vault_root, job, ok=False)
            mstate = mark_jam(
                mstate,
                machine="post_preflight",
                error="post_agent_build_failed",
                agent_log_path=agent_out.get("log_path"),
            )
            _persist_state(vault_root, mstate)
            return {
                "ok": False,
                "id": eid,
                "slice_id": slice_id,
                "lane_id": lane_id,
                "error": "post_agent_build_failed",
                "verify": verify_preflight,
                "agent": agent_out,
                "segment": "IMPLEMENT_SLICE",
                "resume_from": "agent",
            }

        receipt = run_mcp_postedit_validate(
            vault_root,
            lane=queue_lane,
            project_id=project_id,
            engine_adapter=engine_adapter,
            milestone_id=slice_id,
            repo_root=repo_rel.rstrip("/"),
            status="pass",
            message=f"{lane_id} factory_lane {slice_id} agent complete",
            smoke=False,
            extra={
                "dispatch": "factory_lane",
                "parent_run_id": parent_run_id,
                "entry_id": eid,
                "lane_id": lane_id,
                "slice_id": slice_id,
            },
        )
        receipt_id = str(receipt.get("receipt_id") or eid)
        mstate = set_machine(mstate, "receipt", status="ok", detail=receipt_id)
        mstate["receipt_id"] = receipt_id

        zone_paths = [
            str(z).rstrip("/")
            for z in (job.get("zone_write") or params.get("zone_write") or [])
            if z
        ]
        if zone_paths and lane_id in LANE_DROP_TYPE:
            game_repo = vault_root / repo_rel.strip("/")
            register_lane_drop(
                game_repo,
                lane_id=lane_id,
                slice_id=slice_id,
                receipt_id=receipt_id,
                paths=zone_paths[:5],
            )

    zone_write = [str(z) for z in (job.get("zone_write") or params.get("zone_write") or []) if z]
    changed_paths = extract_changed_paths_from_agent(
        vault_root,
        agent_out,
        repo_rel,
        zone_write=zone_write or None,
    )
    mstate["changed_paths"] = list(changed_paths)

    lane_seats = _run_lane_seats(
        vault_root,
        ctx=ctx,
        job=job,
        repo_rel=repo_rel,
        lane_id=lane_id,
        changed_paths=changed_paths,
    )
    seat_self_heal: list[Any] = []
    seat_retried = False
    if not lane_seats.get("all_ok", True) and auto_retry_seats:
        raw_violations: list[str] = []
        for gname, gres in lane_seats.get("passes", {}).items():
            if not gres.ok:
                raw_violations.extend(list(gres.little_val.anti_pattern_violations))
        seat_self_heal = attempt_self_heal_chain(
            vault_root, raw_violations, game_repo_rel=repo_rel, job=job
        )
        if _all_violations_healed(seat_self_heal):
            changed_paths = extract_changed_paths_from_agent(
                vault_root,
                agent_out,
                repo_rel,
                zone_write=zone_write or None,
            )
            mstate["changed_paths"] = list(changed_paths)
            lane_seats = _run_lane_seats(
                vault_root,
                ctx=ctx,
                job=job,
                repo_rel=repo_rel,
                lane_id=lane_id,
                changed_paths=changed_paths,
            )
            seat_retried = True

    seats_ok = bool(lane_seats.get("all_ok", True))
    mstate = set_machine(
        mstate,
        "seats",
        status="ok" if seats_ok else "fail",
        detail="retried" if seat_retried and seats_ok else "",
    )

    if not seats_ok:
        release_lane_job(vault_root, job, ok=False)
        seat_violations = _seat_violations(lane_seats)
        esc = handle_seat_failure_escalation(
            vault_root,
            slice_id=slice_id,
            lane_id=lane_id,
            violations=seat_violations,
            game_repo_rel=repo_rel,
            job=job,
            run_id=ctx.run_id,
            queue_lane=queue_lane,
        )
        lane_seats_summary = {
            k: {"ok": v.ok, "detail": v.detail}
            for k, v in lane_seats.get("passes", {}).items()
        }
        mstate = mark_jam(
            mstate,
            machine="seats",
            error="lane_seats_failed",
            agent_log_path=agent_out.get("log_path"),
            changed_paths=list(changed_paths),
            lane_seats=lane_seats_summary,
        )
        _persist_state(vault_root, mstate)
        append_factory_event(
            vault_root,
            queue_lane,
            "lane_job_fail",
            run_id=ctx.run_id,
            chain_id=ctx.chain_id,
            factory_lane=lane_id,
            slice_id=slice_id,
            status="failure",
            extra={"phase": "lane_seats", "seat_retried": seat_retried},
        )
        return {
            "ok": False,
            "id": eid,
            "run_id": ctx.run_id,
            "chain_id": ctx.chain_id,
            "slice_id": slice_id,
            "lane_id": lane_id,
            "error": "lane_seats_failed",
            "lane_seats": lane_seats_summary,
            "self_heal": [h.__dict__ for h in seat_self_heal],
            "seat_retried": seat_retried,
            "escalation": esc,
            "agent": agent_out,
            "changed_paths": list(changed_paths),
            "segment": "IMPLEMENT_SLICE",
            "resume_from": "seats",
        }

    release_lane_job(vault_root, job, ok=True)

    if not complete_pipeline:
        mstate = mark_complete_state(mstate)
        _persist_state(vault_root, mstate)
        return {
            "ok": True,
            "id": eid,
            "run_id": ctx.run_id,
            "chain_id": ctx.chain_id,
            "slice_id": slice_id,
            "lane_id": lane_id,
            "segment": "REPLAY_SEATS" if seats_only else "IMPLEMENT_SLICE",
            "agent": agent_out,
            "changed_paths": list(changed_paths),
            "lane_seats": {
                k: {"ok": v.ok, "detail": v.detail}
                for k, v in lane_seats.get("passes", {}).items()
            },
            "seat_retried": seat_retried,
            "message": f"factory_lane {lane_id} seats ok (pipeline not completed)",
        }

    mark_lane_complete(vault_root, slice_id=slice_id, lane_id=lane_id, receipt_id=receipt_id)
    ux_bullet_ids = params.get("ux_bullet_ids") or []
    if not isinstance(ux_bullet_ids, list):
        ux_bullet_ids = []
    _write_lane_receipt(
        vault_root,
        slice_id=slice_id,
        lane_id=lane_id,
        receipt_id=receipt_id,
        ux_bullet_ids=ux_bullet_ids,
        ok=True,
        wrote_paths=list(changed_paths),
        agent_out=agent_out if isinstance(agent_out, dict) else None,
        repo_rel=repo_rel,
        zone_write=zone_write,
        project_id=project_id,
    )

    feed_authority = str(params.get("feed_authority") or "")
    is_vault_feed = feed_authority == FEED_VAULT_ROADMAP or slice_id.startswith("row_")
    vault_lanes = params.get("vault_required_lanes") or []
    if isinstance(vault_lanes, list) and vault_lanes:
        vault_lane_list = [str(x) for x in vault_lanes if x]
    elif is_vault_feed:
        vault_lane_list = []
    else:
        vault_lane_list = []
    required_lanes = _wave_required_lanes(
        vault_root,
        slice_id=slice_id,
        params=params,
        vault_lanes=vault_lane_list,
    )
    if is_vault_feed and not required_lanes:
        required_lanes = vault_lane_list
    if not is_vault_feed:
        queue = load_alpha_queue(vault_root, DEFAULT_QUEUE_REL)
        active = next(
            (s for s in (queue.get("slices") or []) if isinstance(s, dict) and s.get("status") == "active"),
            {},
        )
        required_lanes = [str(x) for x in (active.get("lanes") or []) if x]
    vault_gates = params.get("vault_exit_gates") or []
    if isinstance(vault_gates, list) and vault_gates:
        exit_gates = [str(g) for g in vault_gates if g]
    elif is_vault_feed:
        exit_gates = [
            "surface_pass",
            "factory_output_conduct",
            "product_kinesthetic_honesty",
        ]
    else:
        queue = load_alpha_queue(vault_root, DEFAULT_QUEUE_REL)
        active = next(
            (s for s in (queue.get("slices") or []) if isinstance(s, dict) and s.get("status") == "active"),
            {},
        )
        exit_gates = [str(g) for g in (active.get("exit_gates") or []) if g]
    all_lanes_done = slice_lanes_complete(
        vault_root, slice_id=slice_id, required_lanes=required_lanes
    )

    pm_review: dict[str, Any] = {"skipped": True}
    pm_pass = False
    current_wave = int(params.get("wave") or 1)
    skip_pm_agent = bool(params.get("skip_pm_agent"))
    if all_lanes_done and is_vault_feed:
        if try_acquire_pm_review_lock(vault_root, project_id):
            if skip_pm_agent:
                pm_review = run_slice_producer_review(
                    vault_root,
                    project_id=project_id,
                    slice_id=slice_id,
                    queue_lane=queue_lane,
                    current_wave=current_wave,
                )
                pm_pass = bool(pm_review.get("ok"))
            else:
                from ..user_story.slice_producer_enqueue import enqueue_slice_producer_review

                pf_run = str(params.get("product_factory_run_id") or "")
                if not pf_run:
                    pf_loaded = load_product_factory(vault_root, project_id)
                    pf_run = str(pf_loaded.get("run_id") or "")
                pm_review = enqueue_slice_producer_review(
                    vault_root,
                    lane=queue_lane,
                    project_id=project_id,
                    run_id=pf_run,
                    slice_id=slice_id,
                    wave=current_wave,
                )
                if not pm_review.get("ok"):
                    release_pm_review_lock(vault_root, project_id, status="idle")
                else:
                    update_implementation_cell(
                        vault_root,
                        project_id,
                        {"phase": "pm_review", "pm_review_enqueued": True},
                    )
                pm_pass = False
            if skip_pm_agent and pm_review.get("verdict") == "rework" and packet:
                pf = load_product_factory(vault_root, project_id)
                cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
                rework_iters = dict(cell.get("rework_iterations") or {})
                rework_lane = lane_id
                for v in pm_review.get("violations") or []:
                    if str(v).startswith("lane_receipt_missing:"):
                        rework_lane = str(v).split(":", 1)[1]
                        break
                next_iter = int(rework_iters.get(rework_lane) or 0) + 1
                rework_iters[rework_lane] = next_iter
                update_implementation_cell(
                    vault_root,
                    project_id,
                    {"rework_iterations": rework_iters, "pm_review_status": "rework"},
                )
                from .factory_orchestrator import run_factory_orchestrator

                orch = run_factory_orchestrator(
                    vault_root,
                    write_dispatch=False,
                    run_gates=False,
                    project_id=project_id,
                )
                append_factory_rework(
                    vault_root,
                    queue_lane,
                    packet,
                    run_id=ctx.chain_id,
                    slice_id=slice_id,
                    lane_id=rework_lane,
                    jobs=list(orch.jobs),
                    rework_iteration=next_iter,
                )
        else:
            pf = load_product_factory(vault_root, project_id)
            cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
            pm_pass = str(cell.get("pm_review_status") or "") == "pass"

    slice_gates: dict[str, Any] = {"all_ok": True, "passes": {}}
    slice_complete = False
    run_slice_gates = all_lanes_done and (pm_pass or not is_vault_feed)
    if run_slice_gates and exit_gates:
        slice_gates = run_slice_exit_gates(
            vault_root,
            exit_gates=exit_gates,
            game_repo_rel=repo_rel,
            lane_id=lane_id,
            job=job,
            changed_paths=changed_paths,
            run_probes=False,
            stack_integrate_dry_run=False,
        )
        slice_complete = bool(slice_gates.get("all_ok"))
        for gname, gres in slice_gates.get("passes", {}).items():
            append_gate_log(
                vault_root,
                gname,
                ok=gres.ok,
                run_id=ctx.run_id,
                chain_id=ctx.chain_id,
                slice_id=slice_id,
                lane_id=lane_id,
                violations=list(gres.little_val.anti_pattern_violations),
            )
    elif run_slice_gates and not exit_gates:
        slice_complete = True

    all_seats = {**lane_seats.get("passes", {}), **slice_gates.get("passes", {})}
    intent = build_intent_receipt(agent_ok=True, seat_results=all_seats)
    may_success, honesty_reason = enforce_factory_success(intent)
    gate_result, gate_trace = apply_factory_output_gate_to_trace(vault_root, {})

    advance: dict[str, Any] = {"ok": True, "advanced": False, "reason": "lanes_incomplete_or_gates_pending"}
    post_hooks: dict[str, Any] = {"skipped": True}
    playtest_brief: dict[str, Any] = {"skipped": True}
    slice_exit_blocked = run_slice_gates and exit_gates and not slice_gates.get("all_ok", True)

    lane_summary_path = write_lane_run_summary(
        vault_root,
        ctx=ctx,
        receipt_id=receipt_id,
        lane_seats=lane_seats,
        changed_paths=changed_paths,
        agent_ok=bool(agent_out.get("ok")),
    )
    slice_summary_path: Path | None = None

    if all_lanes_done and slice_complete:
        gate_summary = {
            k: {"ok": v.ok, "detail": v.detail}
            for k, v in slice_gates.get("passes", {}).items()
        }
        brief = write_playtest_brief(
            vault_root,
            slice_id=slice_id,
            queue_lane=queue_lane,
            slice_exit_gates_pass=slice_complete,
            slice_exit_gate_summary=gate_summary,
            receipt_id=receipt_id,
        )
        playtest_brief = brief.to_dict()

        from .playtest_gate_policy import resolve_playtest_gate_policy, should_exit_playtest_after_beat
        from .weld_beat_ready import park_playtest_machine_ready, weld_beat_machine_ready

        machine_ok, machine_reason = weld_beat_machine_ready(
            vault_root,
            project_id,
            slice_id=slice_id,
            required_lanes=required_lanes,
            gate_summary=gate_summary,
            honesty_ok=may_success,
        )
        if machine_ok:
            policy = resolve_playtest_gate_policy(vault_root, packet, project_id=project_id)
            session_id = str(
                params.get("overnight_session_run_id")
                or params.get("architect_orchestration_run_id")
                or ctx.chain_id
                or ""
            )
            pf_sess = load_product_factory(vault_root, project_id)
            beats = int(pf_sess.get("playtest_beats_this_session") or 0)
            should_exit, exit_reason = should_exit_playtest_after_beat(
                vault_root,
                project_id,
                packet=packet,
                session_run_id=session_id,
                row_id=str(params.get("catalog_row_id") or ""),
                dispatch_depth=params.get("dispatch_depth"),
                target_depth=params.get("target_depth"),
                beats_this_session=beats,
            )
            playtest_brief["playtest_policy"] = policy
            playtest_brief["playtest_should_exit"] = should_exit
            playtest_brief["playtest_exit_reason"] = exit_reason
            if should_exit:
                park = park_playtest_machine_ready(
                    vault_root,
                    project_id,
                    slice_id=slice_id,
                    session_run_id=session_id,
                    gate_summary=gate_summary,
                )
                playtest_brief["playtest_park"] = park
                save_product_factory(
                    vault_root,
                    project_id,
                    {
                        **load_product_factory(vault_root, project_id),
                        "playtest_beats_this_session": beats + 1,
                    },
                )
            else:
                playtest_brief["playtest_park"] = {
                    "skipped": True,
                    "reason": exit_reason or "policy_continue_weld",
                }

    depth_bump: dict[str, Any] = {"skipped": True}
    block_depth_for_playtest = bool(
        playtest_brief.get("playtest_should_exit") and playtest_brief.get("playtest_park", {}).get("ok")
    )
    if all_lanes_done and slice_complete and may_success and (pm_pass or not is_vault_feed):
        if block_depth_for_playtest:
            depth_bump = {"skipped": True, "reason": "playtest_exit_same_run"}
        else:
            session_id = str(
                params.get("overnight_session_run_id")
                or params.get("architect_orchestration_run_id")
                or ctx.chain_id
                or ""
            )
            depth_bump = try_weld_depth_bump_after_slice(
                vault_root,
                project_id=project_id,
                params=params,
                slice_id=slice_id,
                all_lanes_done=all_lanes_done,
                honesty_ok=may_success,
                session_run_id=session_id or None,
                packet=packet,
            )
            if depth_bump.get("ok") and is_vault_feed:
                from ..user_story.implementation_artifact_ledger import record_implementation_artifact

                budget_rel = ""
                try:
                    from ..user_story.catalog_io import user_story_paths

                    budget_rel = str(
                        user_story_paths(vault_root, project_id)["budget"].relative_to(vault_root)
                    )
                except (OSError, ValueError, KeyError):
                    pass
                if budget_rel:
                    record_implementation_artifact(
                        vault_root,
                        project_id,
                        artifact_path=budget_rel,
                        event_type="depth_bump",
                        slice_id=slice_id,
                        product_factory_run_id=str(params.get("product_factory_run_id") or ""),
                    )
        if depth_bump.get("ok") and is_vault_feed:
            pf = load_product_factory(vault_root, project_id)
            completed = list(pf.get("completed_phases") or [])
            if FACTORY_CELL_COMPLETE not in completed:
                completed.append(FACTORY_CELL_COMPLETE)
                save_product_factory(vault_root, project_id, {**pf, "completed_phases": completed})
            if not params.get("skip_product_factory_continue"):
                from ..user_story.product_factory_continue import append_product_factory_continue

                pf_run = str(params.get("product_factory_run_id") or pf.get("run_id") or "")
                if pf_run:
                    append_product_factory_continue(
                        vault_root,
                        lane=queue_lane,
                        project_id=project_id,
                        run_id=pf_run,
                        trigger_entry_id=str(params.get("request_id") or receipt_id),
                        source="depth_bump",
                    )

    if all_lanes_done and slice_complete:
        if is_vault_feed:
            if depth_bump.get("ok"):
                loop_reopen = reopen_product_factory_loop_3(
                    vault_root,
                    project_id,
                    reason="depth_bump_complete",
                )
                advance = {
                    "ok": True,
                    "advanced": False,
                    "vault_feed": True,
                    "loop_3_reopened": loop_reopen,
                }
            else:
                advance = {
                    "ok": True,
                    "advanced": False,
                    "vault_feed": True,
                    "reason": "depth_bump_skipped_or_incomplete",
                }
        else:
            advance = advance_alpha_queue_if_ready(vault_root)
            if advance.get("advanced") and packet:
                post_hooks = run_post_slice_advance_hooks(
                    vault_root,
                    queue_lane,
                    packet,
                    advance,
                    run_id=ctx.chain_id,
                )

    if advance.get("vault_feed") and packet:
        from .factory_authority_sync import sync_goal_authority_from_vault_feed

        pid = str(entry.get("project_id") or params.get("project_id") or "godot-genesis-mythos-master")
        auth = sync_goal_authority_from_vault_feed(
            vault_root, queue_lane, advance, project_id=pid
        )
        advance["goal_authority_sync"] = auth

    if all_lanes_done:
        slice_summary_path = write_slice_run_summary(
            vault_root,
            ctx=ctx,
            receipt_id=receipt_id,
            slice_exit_gates=slice_gates,
            all_lanes_done=all_lanes_done,
            slice_complete=slice_complete,
            advance=advance,
            playtest_brief=playtest_brief,
        )

    append_factory_event(
        vault_root,
        queue_lane,
        "lane_job_complete",
        run_id=ctx.run_id,
        chain_id=ctx.chain_id,
        factory_lane=lane_id,
        slice_id=slice_id,
        receipt_id=receipt_id,
        status="success",
        extra={
            "slice_advance": advance,
            "slice_all_lanes_done": all_lanes_done,
            "slice_exit_gates_pass": slice_complete,
            "post_slice_hooks": post_hooks,
            "vault_depth_bump": depth_bump,
            "playtest_brief": playtest_brief,
            "intent_actual_receipt": intent.to_dict(),
            "lane_summary": str(lane_summary_path.relative_to(vault_root)),
            "slice_summary": str(slice_summary_path.relative_to(vault_root)) if slice_summary_path else None,
            "changed_paths": list(changed_paths),
            "seat_retried": seat_retried,
            "replay": seats_only,
        },
    )

    mstate = mark_complete_state(mstate)
    mstate["agent_log_path"] = agent_out.get("log_path") or mstate.get("agent_log_path")
    mstate["changed_paths"] = list(changed_paths)
    mstate["receipt_id"] = receipt_id
    _persist_state(vault_root, mstate)

    message = f"factory_lane {lane_id} @ {slice_id} complete (honesty ok)"
    if slice_exit_blocked:
        message = f"factory_lane {lane_id} @ {slice_id} lane ok; slice exit gates blocked"
    elif not all_lanes_done:
        message = f"factory_lane {lane_id} @ {slice_id} lane ok; awaiting sibling lanes"

    return {
        "ok": True,
        "id": eid,
        "run_id": ctx.run_id,
        "chain_id": ctx.chain_id,
        "slice_id": slice_id,
        "lane_id": lane_id,
        "segment": "IMPLEMENT_SLICE",
        "agent": agent_out,
        "verify": verify_preflight,
        "receipt": receipt,
        "changed_paths": list(changed_paths),
        "lane_summary_path": str(lane_summary_path.relative_to(vault_root)),
        "slice_summary_path": str(slice_summary_path.relative_to(vault_root)) if slice_summary_path else None,
        "intent_actual_receipt": intent.to_dict(),
        "lane_seats": {k: {"ok": v.ok, "detail": v.detail} for k, v in lane_seats.get("passes", {}).items()},
        "slice_exit_gates": {k: {"ok": v.ok, "detail": v.detail} for k, v in slice_gates.get("passes", {}).items()},
        "slice_all_lanes_done": all_lanes_done,
        "slice_exit_gates_pass": slice_complete,
        "slice_exit_gates_blocked": slice_exit_blocked,
        "slice_advance": advance,
        "post_slice_advance": post_hooks,
        "playtest_brief": playtest_brief,
        "factory_output_gate": gate_result.to_dict(),
        "factory_output_trace": gate_trace,
        "honesty_reason": honesty_reason if not may_success else "",
        "seat_retried": seat_retried,
        "replay": seats_only,
        "message": message,
    }
