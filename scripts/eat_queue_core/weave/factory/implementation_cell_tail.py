"""Shared Implementation Cell tail — after final PM review pass."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...goal_authority_io import load_goal_authority
from ..user_story.depth_bump import try_weld_depth_bump_after_slice
from ..user_story.product_factory_state import (
    FACTORY_CELL_COMPLETE,
    load_product_factory,
    reopen_product_factory_loop_3,
    save_product_factory,
    update_implementation_cell,
)
from ..user_story.work_order_translate import FEED_VAULT_ROADMAP
from .factory_correlation import FactoryRunContext, append_gate_log
from .factory_honesty_gate import build_intent_receipt, enforce_factory_success
from .factory_orchestrator import run_factory_orchestrator
from .factory_pq_stage import append_factory_rework
from .factory_project import load_factory_project
from .playtest_brief import write_playtest_brief
from .review_pass_runner import run_slice_exit_gates

_VAULT_EXIT_GATES = (
    "surface_pass",
    "factory_output_conduct",
    "product_kinesthetic_honesty",
)


def build_depth_bump_params(vault_root: Path, project_id: str) -> dict[str, Any]:
    """Params for try_weld_depth_bump_after_slice from product-factory active_slice."""
    pf = load_product_factory(vault_root, project_id)
    active = pf.get("active_slice") if isinstance(pf.get("active_slice"), dict) else {}
    row_ids = active.get("row_ids") or []
    catalog_row_id = str(row_ids[0]) if row_ids else ""
    depth = active.get("dispatch_depth")
    return {
        "feed_authority": FEED_VAULT_ROADMAP,
        "catalog_row_id": catalog_row_id,
        "dispatch_depth": depth,
        "target_depth": depth,
    }


def _game_repo_rel(vault_root: Path, project_id: str) -> str:
    bootstrap = load_factory_project(vault_root, project_id)
    rel = str(bootstrap.get("game_repo_path") or "").strip().rstrip("/")
    return f"{rel}/" if rel else "game/"


def handle_pm_rework(
    vault_root: Path,
    *,
    project_id: str,
    slice_id: str,
    queue_lane: str,
    run_id: str,
    review: dict[str, Any],
) -> dict[str, Any]:
    """Enqueue rework lane after PM verdict rework (production review path)."""
    vault_root = vault_root.resolve()
    pf = load_product_factory(vault_root, project_id)
    cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
    rework_iters = dict(cell.get("rework_iterations") or {})
    rework_lane = ""
    for v in review.get("violations") or []:
        text = str(v)
        if text.startswith("lane_receipt_missing:"):
            rework_lane = text.split(":", 1)[1]
            break
    if not rework_lane:
        lanes = review.get("rework_lanes") or []
        if isinstance(lanes, list) and lanes:
            rework_lane = str(lanes[0])
    if not rework_lane:
        return {"ok": False, "detail": "no_rework_lane_identified"}

    next_iter = int(rework_iters.get(rework_lane) or 0) + 1
    rework_iters[rework_lane] = next_iter
    update_implementation_cell(
        vault_root,
        project_id,
        {"rework_iterations": rework_iters, "pm_review_status": "rework", "phase": "rework"},
    )

    packet = load_goal_authority(vault_root, queue_lane, require_confirmed=False) or {
        "project_id": project_id,
        "planner_hints": {"feed_authority": FEED_VAULT_ROADMAP},
    }
    orch = run_factory_orchestrator(
        vault_root,
        write_dispatch=False,
        run_gates=False,
        project_id=project_id,
    )
    rework = append_factory_rework(
        vault_root,
        queue_lane,
        packet,
        run_id=run_id or f"rework-{slice_id}",
        slice_id=slice_id,
        lane_id=rework_lane,
        jobs=list(orch.jobs),
        rework_iteration=next_iter,
    )
    return {"ok": True, "rework_lane": rework_lane, "rework_iteration": next_iter, **rework}


def run_implementation_cell_post_pm_tail(
    vault_root: Path,
    *,
    project_id: str,
    slice_id: str,
    queue_lane: str,
    product_factory_run_id: str = "",
    trigger_entry_id: str = "",
    skip_product_factory_continue: bool = False,
    ctx: FactoryRunContext | None = None,
) -> dict[str, Any]:
    """
    After final PM wave passes: slice exit gates → playtest brief → depth bump → cell complete.

    Invoked from SLICE_PRODUCER_REVIEW handler (production path) when no more waves remain.
    """
    vault_root = vault_root.resolve()
    params = build_depth_bump_params(vault_root, project_id)
    repo_rel = _game_repo_rel(vault_root, project_id)
    exit_gates = list(_VAULT_EXIT_GATES)

    slice_gates = run_slice_exit_gates(
        vault_root,
        exit_gates=exit_gates,
        game_repo_rel=repo_rel,
        lane_id="pm_review",
        job=None,
        changed_paths=None,
        run_probes=False,
        stack_integrate_dry_run=False,
    )
    if ctx is not None:
        for gname, gres in slice_gates.get("passes", {}).items():
            append_gate_log(
                vault_root,
                gname,
                ok=gres.ok,
                run_id=ctx.run_id,
                chain_id=ctx.chain_id,
                slice_id=slice_id,
                lane_id="pm_review",
                violations=list(gres.little_val.anti_pattern_violations),
            )

    slice_complete = bool(slice_gates.get("all_ok", True))
    gate_summary = {
        k: {"ok": v.ok, "detail": v.detail}
        for k, v in slice_gates.get("passes", {}).items()
    }

    playtest_brief: dict[str, Any] = {"skipped": True}
    if slice_complete:
        brief = write_playtest_brief(
            vault_root,
            slice_id=slice_id,
            queue_lane=queue_lane,
            slice_exit_gates_pass=slice_complete,
            slice_exit_gate_summary=gate_summary,
            receipt_id=trigger_entry_id or None,
        )
        playtest_brief = brief.to_dict()

    intent = build_intent_receipt(agent_ok=True, seat_results=slice_gates.get("passes", {}))
    may_success, _honesty_reason = enforce_factory_success(intent)

    depth_bump: dict[str, Any] = {"skipped": True}
    loop_reopen: dict[str, Any] | None = None
    if slice_complete and may_success:
        from ...goal_authority_io import load_goal_authority

        ga_packet = load_goal_authority(vault_root, queue_lane, require_confirmed=False)
        depth_bump = try_weld_depth_bump_after_slice(
            vault_root,
            project_id=project_id,
            params=params,
            slice_id=slice_id,
            all_lanes_done=True,
            honesty_ok=may_success,
            session_run_id=str(
                params.get("overnight_session_run_id")
                or params.get("architect_orchestration_run_id")
                or ""
            )
            or None,
            packet=ga_packet if isinstance(ga_packet, dict) else None,
        )
        if depth_bump.get("ok"):
            pf = load_product_factory(vault_root, project_id)
            completed = list(pf.get("completed_phases") or [])
            if FACTORY_CELL_COMPLETE not in completed:
                completed.append(FACTORY_CELL_COMPLETE)
                save_product_factory(vault_root, project_id, {**pf, "completed_phases": completed})
            if not skip_product_factory_continue:
                from ..user_story.product_factory_continue import append_product_factory_continue

                pf_run = product_factory_run_id or str(pf.get("run_id") or "")
                if pf_run:
                    append_product_factory_continue(
                        vault_root,
                        lane=queue_lane,
                        project_id=project_id,
                        run_id=pf_run,
                        trigger_entry_id=trigger_entry_id or f"pm-tail-{slice_id}",
                        source="depth_bump",
                    )
            loop_reopen = reopen_product_factory_loop_3(
                vault_root,
                project_id,
                reason="depth_bump_complete",
            )

    update_implementation_cell(
        vault_root,
        project_id,
        {
            "phase": "cell_complete" if slice_complete else "pm_review",
            "pm_review_status": "pass" if slice_complete else "rework",
            "pm_review_enqueued": False,
        },
    )

    return {
        "ok": slice_complete and may_success,
        "slice_exit_gates": slice_gates,
        "slice_complete": slice_complete,
        "playtest_brief": playtest_brief,
        "depth_bump": depth_bump,
        "loop_3_reopened": loop_reopen,
        "intent_actual_receipt": intent.to_dict(),
    }
