"""Product factory conductor — PMG → product via three operator loops."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ...research_enqueue import enqueue_research
from ..roadmap.deepen_enqueue import merge_deepen_params
from .ux_mint_backlog import generate_ux_mint_backlog, load_mint_backlog
from .catalog_io import user_story_paths
from .depth_slicer import run_depth_slicer
from .execution_pin_sync import sync_catalog_execution_pins
from .execution_pseudo_code_audit import run_execution_pseudo_code_audit
from .product_factory_enqueue import flush_pending_enqueues
from .product_factory_loops import (
    check_execution_engineering,
    check_operator_loop_1,
    check_operator_loop_2,
    check_operator_loop_3,
    loop_status_dict,
    resolve_blocking_operator_loop,
)
from .product_factory_state import (
    FACTORY_CELL_COMPLETE,
    FACTORY_STAGED,
    LEGACY_FACTORY_STAGE,
    clear_factory_beat_phases,
    default_implementation_cell,
    detect_project_profile,
    execution_track_exists,
    load_product_factory,
    normalize_completed_phases,
    save_product_factory,
)
from .research_context import influence_deck_needs_research
from .wire_execution_pins import wire_execution_pins

MAX_EXECUTION_DEEPEN_PASSES = 5


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _honest_ledger_sync(
    vault_root: Path,
    project_id: str,
    pf: dict[str, Any],
    completed: list[str],
    *,
    goal_packet: dict[str, Any] | None = None,
    mint_batch: str | None = None,
) -> tuple[list[str], dict[str, Any], list[dict[str, Any]]]:
    """
    Derive completed_phases and conductor flags from live gates — no optimistic ledger.

    When strict conceptual is red, reopen machine phases and clear premature Loop 2 park.
    """
    vault_root = vault_root.resolve()
    steps: list[dict[str, Any]] = []
    ready, gate_reason = conceptual_track_ready(
        vault_root,
        project_id,
        mint_batch=mint_batch,
        goal_packet=goal_packet,
    )
    updates: dict[str, Any] = {}
    paths = user_story_paths(vault_root, project_id)
    catalog_on_disk = paths["catalog"].is_file()

    if not ready:
        stripped = [p for p in completed if p in ("conceptual_deepen", "catalog_mint", "loop2_prep")]
        if stripped:
            completed = [p for p in completed if p not in stripped]
            steps.append({"step": "honest_ledger_reopen", "stripped": stripped, "reason": gate_reason})
        if pf.get("loop2_exit_eligible") is True:
            updates["loop2_exit_eligible"] = False
            updates["blocked_at"] = "machine:conceptual_deepen"
            updates["phase"] = "conceptual_deepen"
            updates["operator_loop"] = 1
            steps.append({"step": "honest_ledger_clear_loop2_park", "reason": gate_reason})
        elif catalog_on_disk:
            steps.append({"step": "catalog_ahead_of_conceptual_freeze", "reason": gate_reason})

    return completed, updates, steps


from .conceptual_track_ready import conceptual_track_ready
from .factory_conceptual_freeze import stamp_factory_conceptual_freeze
from .factory_cursor import reconcile_factory_cursor, should_factory_bootstrap


def _gate_kwargs(
    params: dict[str, Any],
    goal_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    mb = params.get("mint_batch")
    return {"mint_batch": str(mb) if mb else None, "goal_packet": goal_packet}


@dataclass
class TickResult:
    ok: bool
    blocked_at: str | None
    phase: str
    operator_loop: int | None
    steps: list[dict[str, Any]] = field(default_factory=list)
    detail: str = ""
    pending_enqueues: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "blocked_at": self.blocked_at,
            "phase": self.phase,
            "operator_loop": self.operator_loop,
            "steps": self.steps,
            "detail": self.detail,
            "pending_enqueues": self.pending_enqueues,
        }


def _loop_num(loop_id: str | None) -> int | None:
    if loop_id == "operator_loop_1_pmg":
        return 1
    if loop_id == "operator_loop_2_catalog_levels":
        return 2
    if loop_id == "operator_loop_3_slice_selection":
        return 3
    return None


def _agent_enqueue(
    vault_root: Path,
    *,
    project_id: str,
    run_id: str,
    pending: list[dict[str, Any]],
    params: dict[str, Any],
    steps: list[dict[str, Any]],
    phase: str,
    completed: list[str],
    persist_fn,
) -> TickResult:
    """Flush pending RESUME / RESEARCH lines to lane PQ."""
    lane = str(params.get("queue_lane") or "godot")
    written = flush_pending_enqueues(
        vault_root,
        project_id=project_id,
        pending=pending,
        lane=lane,
        run_id=run_id,
    )
    steps.append({"step": f"{phase}_enqueue", "written": written})
    failures = [w for w in written if not w.get("ok", True)]
    if failures:
        persist_fn(phase, blocked_at=f"machine:{phase}")
        return TickResult(
            False,
            f"machine:{phase}",
            phase,
            None,
            steps,
            "enqueue_failed",
            written,
        )
    meta_key = phase.replace("-", "_")
    pf = load_product_factory(vault_root, project_id)
    deepen_meta = dict(pf.get(meta_key) or {}) if isinstance(pf.get(meta_key), dict) else {}
    deepen_meta["waiting_agent"] = True
    deepen_meta["last_enqueued_at"] = _utc_iso()
    save_product_factory(vault_root, project_id, {**pf, meta_key: deepen_meta})
    persist_fn(phase, blocked_at=f"machine:{phase}")
    return TickResult(
        True,
        f"machine:{phase}",
        phase,
        None,
        steps,
        "needs_agent_enqueue",
        written,
    )


def _enqueue_research_gaps(
    vault_root: Path,
    *,
    project_id: str,
    lane: str,
    gaps: tuple[str, ...],
    linked_phase: str,
) -> dict[str, Any]:
    return enqueue_research(
        vault_root,
        lane=lane,
        project_id=project_id,
        linked_phase=linked_phase,
        profile="roadmap_gap",
        params={
            "gaps": list(gaps),
            "research_focus": "junior_handoff",
            "origin": "roadmap-deepen",
            "product_factory_run_id": linked_phase,
        },
        source="product_factory_conductor",
    )


def _machine_blocked(step_id: str, sub_reason: str | None = None) -> str:
    if sub_reason:
        return f"machine:{step_id}"
    return f"machine:{step_id}"


def _run_factory_compose_tail(
    vault_root: Path,
    *,
    project_id: str,
    run_id: str,
    lane: str,
    pf: dict[str, Any],
    params: dict[str, Any],
    steps: list[dict[str, Any]],
    completed: list[str],
    _persist,
) -> TickResult | None:
    from ..factory.factory_bom import bom_blocks_factory_stage_v2
    from ..factory.factory_pq_stage import stage_factory_dispatch_to_pq
    from ..factory.slice_producer_harness import (
        load_producer_receipt,
        run_slice_producer_compose,
        validate_producer_receipt,
    )
    from ...goal_authority_io import load_goal_authority
    from .slice_producer_enqueue import enqueue_slice_producer_compose
    from .product_factory_state import update_implementation_cell

    skip_pm = bool(params.get("skip_pm_agent", params.get("dry_run")))

    bom_ok, bom_blocked, bom_result = bom_blocks_factory_stage_v2(vault_root, project_id=project_id)
    steps.append(
        {
            "step": "factory_bom",
            "ok": bom_ok,
            "blocked_at": bom_blocked,
            "summary": bom_result.summary,
        }
    )
    if not bom_ok:
        _persist("factory_compose", blocked_at=_machine_blocked("factory_compose", bom_blocked))
        return TickResult(
            True,
            _machine_blocked("factory_compose"),
            "factory_compose",
            3,
            steps,
            f"bom_gate:{bom_blocked}",
        )

    active_slice = pf.get("active_slice") if isinstance(pf.get("active_slice"), dict) else None
    cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
    slice_id = str(cell.get("factory_beat_id") or "")
    receipt = load_producer_receipt(vault_root, slice_id) if slice_id else None
    receipt_ok = False
    if receipt:
        receipt_ok, violations = validate_producer_receipt(vault_root, receipt)
        if not receipt_ok:
            steps.append({"step": "producer_receipt_validate", "ok": False, "violations": violations})

    if not receipt_ok:
        if skip_pm:
            compose = run_slice_producer_compose(
                vault_root,
                project_id=project_id,
                run_id=run_id,
                active_slice=active_slice,
            )
            steps.append({"step": "slice_producer_compose", **compose, "path": "harness_fallback"})
            if not compose.get("ok"):
                _persist("factory_compose", blocked_at=_machine_blocked("factory_compose"))
                return TickResult(
                    True,
                    _machine_blocked("factory_compose"),
                    "factory_compose",
                    3,
                    steps,
                    "producer_compose",
                )
            slice_id = str(compose.get("slice_id") or slice_id)
        else:
            if not cell.get("pm_compose_enqueued"):
                enq = enqueue_slice_producer_compose(
                    vault_root,
                    lane=lane,
                    project_id=project_id,
                    run_id=run_id,
                    active_slice=active_slice,
                )
                steps.append({"step": "slice_producer_compose_enqueue", **enq})
                if not enq.get("ok"):
                    _persist("pm_compose", blocked_at=_machine_blocked("pm_compose"))
                    return TickResult(
                        False,
                        _machine_blocked("pm_compose"),
                        "pm_compose",
                        3,
                        steps,
                        "pm_compose_enqueue_failed",
                    )
                update_implementation_cell(
                    vault_root,
                    project_id,
                    {"phase": "awaiting_compose", "pm_compose_enqueued": True},
                )
            _persist("pm_compose", blocked_at=_machine_blocked("pm_compose"))
            return TickResult(
                True,
                _machine_blocked("pm_compose"),
                "pm_compose",
                3,
                steps,
                "awaiting_pm_compose",
            )

    packet = load_goal_authority(vault_root, lane, require_confirmed=False) or {
        "project_id": project_id,
        "planner_hints": {"feed_authority": "vault_roadmap", "effective_track": "implementation"},
    }
    hints = packet.setdefault("planner_hints", {})
    if isinstance(hints, dict):
        hints["feed_authority"] = "vault_roadmap"
    stage = stage_factory_dispatch_to_pq(
        vault_root, lane, packet, run_id=run_id, dry_run=bool(params.get("dry_run"))
    )
    steps.append({"step": "factory_pq_stage", **stage})
    if not stage.get("ok"):
        _persist("factory_compose", blocked_at=_machine_blocked("factory_compose"))
        return TickResult(
            True,
            _machine_blocked("factory_compose"),
            "factory_compose",
            3,
            steps,
            str(stage.get("detail") or "factory_pq_stage"),
        )
    if FACTORY_STAGED not in completed:
        completed.append(FACTORY_STAGED)
    update_implementation_cell(
        vault_root,
        project_id,
        {"phase": "lanes_running", "pm_compose_enqueued": False},
    )
    _persist("factory_staged", operator_loop=None, blocked_at=None)

    appended = int(stage.get("appended") or 0)
    if appended > 0 and not params.get("dry_run"):
        from .factory_eat_handoff import append_factory_eat_handoff

        handoff = append_factory_eat_handoff(
            vault_root,
            lane=lane,
            project_id=project_id,
            run_id=run_id,
            slice_id=str(stage.get("slice_id") or slice_id),
            wave=int(stage.get("wave") or 1),
            lane_job_count=appended,
        )
        steps.append({"step": "factory_eat_handoff", **handoff})

    return TickResult(
        bool(stage.get("ok")),
        None,
        "factory_staged",
        None,
        steps,
        "factory_staged_awaiting_lanes",
    )


def product_factory_status(vault_root: Path, *, project_id: str) -> dict[str, Any]:
    pf = load_product_factory(vault_root, project_id)
    loops = loop_status_dict(vault_root, project_id)
    profile = pf.get("project_profile") or detect_project_profile(vault_root, project_id)
    return {
        "project_id": project_id,
        "project_profile": profile,
        "phase": pf.get("phase") or "unknown",
        "operator_loop": pf.get("operator_loop") or _loop_num(loops.get("blocked_at")),
        "loops": loops,
        "product_factory": pf,
    }


def tick(
    vault_root: Path,
    *,
    project_id: str,
    params: dict[str, Any] | None = None,
) -> TickResult:
    """
    Advance product factory until an operator loop, machine gate, or completion.

    Agent steps enqueue to lane PQ via flush_pending_enqueues unless skip_agent_enqueue.
  """
    vault_root = vault_root.resolve()
    params = dict(params or {})
    skip_agent = bool(params.get("skip_agent_enqueue", params.get("dry_run")))
    steps: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    lane = str(params.get("queue_lane") or "godot")

    goal_packet = params.get("goal_packet") if isinstance(params.get("goal_packet"), dict) else None
    gate_kw = _gate_kwargs(params, goal_packet)
    reconcile = reconcile_factory_cursor(vault_root, project_id, goal_packet)
    steps.append({"step": "factory_cursor_reconcile", **reconcile.to_dict()})

    rec_action = str(reconcile.recommended_action or "continue")
    strict_ok = reconcile.conceptual_map_complete
    strict_reason = reconcile.conceptual_reason

    if rec_action == "fix_goal_packet":
        violations = (
            list(reconcile.profile.violations[:6])
            if reconcile.profile and reconcile.profile.violations
            else ["profile_invalid"]
        )
        _persist_early = lambda: save_product_factory(
            vault_root,
            project_id,
            {
                **load_product_factory(vault_root, project_id),
                "blocked_at": "machine:fix_goal_packet",
                "updated_at": _utc_iso(),
            },
        )
        _persist_early()
        return TickResult(
            True,
            "machine:fix_goal_packet",
            "goal_packet",
            None,
            steps,
            ";".join(violations),
            pending,
        )

    from .done_when_eval import LOOP_2_PENDING_SIGN_OFF, loop2_exit_honestly_eligible

    pf_early = load_product_factory(vault_root, project_id)
    completed_early = normalize_completed_phases(list(pf_early.get("completed_phases") or []))
    completed_early, ledger_updates, ledger_steps = _honest_ledger_sync(
        vault_root, project_id, pf_early, completed_early, **gate_kw
    )
    steps.extend(ledger_steps)
    if ledger_updates:
        save_product_factory(
            vault_root,
            project_id,
            {**pf_early, **ledger_updates, "completed_phases": completed_early, "updated_at": _utc_iso()},
        )

    if (
        strict_ok
        and loop2_exit_honestly_eligible(vault_root, project_id)
        and rec_action == "operator_loop_2_gate"
    ):
        pf_gate = load_product_factory(vault_root, project_id)
        save_product_factory(
            vault_root,
            project_id,
            {
                **pf_gate,
                "phase": "catalog_and_levels",
                "operator_loop": 2,
                "blocked_at": LOOP_2_PENDING_SIGN_OFF,
                "updated_at": _utc_iso(),
            },
        )
        steps.append(
            {
                "step": "tick_deferred_loop2_operator_gate",
                "recommended_action": rec_action,
            }
        )
        return TickResult(
            True,
            LOOP_2_PENDING_SIGN_OFF,
            "loop2_operator_gate",
            2,
            steps,
            "loop2_exit_eligible",
            pending,
        )

    pf = load_product_factory(vault_root, project_id)
    profile = str(pf.get("project_profile") or detect_project_profile(vault_root, project_id))
    run_id = str(pf.get("run_id") or uuid.uuid4().hex[:12])
    completed = normalize_completed_phases(list(pf.get("completed_phases") or []))

    agent_phase = str(params.get("agent_phase_complete") or "").strip()
    if agent_phase == "conceptual_deepen":
        ready, gate_reason = conceptual_track_ready(vault_root, project_id, **gate_kw)
        if not ready:
            agent_phase = ""
            steps.append({"step": "conceptual_deepen_continue_deferred", "reason": gate_reason})
    if agent_phase and agent_phase not in completed:
        completed.append(agent_phase)
        meta = dict(pf.get(agent_phase) or {}) if isinstance(pf.get(agent_phase), dict) else {}
        meta["waiting_agent"] = False
        meta["agent_completed_at"] = _utc_iso()
        pf = {**pf, agent_phase: meta}
        steps.append({"step": f"{agent_phase}_continue", "ok": True})
        save_product_factory(vault_root, project_id, {**pf, "completed_phases": completed})

    def _persist(phase: str, *, operator_loop: int | None = None, blocked_at: str | None = None) -> None:
        nonlocal pf
        pf = load_product_factory(vault_root, project_id)
        save_product_factory(
            vault_root,
            project_id,
            {
                **pf,
                "project_id": project_id,
                "project_profile": profile,
                "run_id": run_id,
                "phase": phase,
                "operator_loop": operator_loop,
                "completed_phases": completed,
                "ux_first": True,
                "blocked_at": blocked_at,
                "updated_at": _utc_iso(),
            },
        )

    # Loop 1
    l1 = check_operator_loop_1(vault_root, project_id)
    if not l1.ok:
        _persist("pmg_normalize", operator_loop=1, blocked_at=l1.loop_id)
        return TickResult(True, l1.loop_id, "pmg_normalize", 1, steps, "operator_loop_1_pmg")

    # Conceptual deepen (before catalog mint)
    if "conceptual_deepen" in completed:
        ready, gate_reason = conceptual_track_ready(vault_root, project_id, **gate_kw)
        if not ready:
            completed = [p for p in completed if p != "conceptual_deepen"]
            steps.append({"step": "conceptual_deepen_reopened", "reason": gate_reason})
            save_product_factory(vault_root, project_id, {**pf, "completed_phases": completed})

    if "conceptual_deepen" not in completed:
        ready, gate_reason = conceptual_track_ready(vault_root, project_id, **gate_kw)
        if ready:
            steps.append({"step": "conceptual_deepen", "skipped": False, "reason": gate_reason})
            completed.append("conceptual_deepen")
            save_product_factory(vault_root, project_id, {**pf, "completed_phases": completed})
        else:
            if influence_deck_needs_research(vault_root, project_id=project_id) and not skip_agent:
                research_out = enqueue_research(
                    vault_root,
                    lane=lane,
                    project_id=project_id,
                    linked_phase="conceptual_deepen",
                    profile="influence",
                    params={
                        "research_focus": "cto_brief",
                        "prefer": "diverse",
                        "product_factory_run_id": run_id,
                    },
                    source="product_factory_conductor",
                )
                steps.append({"step": "conceptual_influence_research", **research_out})
            pending.append(
                {
                    "mode": "RESUME_ROADMAP",
                    "params": merge_deepen_params(
                        vault_root,
                        {
                            "action": "deepen",
                            "roadmap_track": "conceptual",
                            "project_id": project_id,
                            "product_factory_run_id": run_id,
                            "queue_next": True,
                            "linked_phase": "conceptual",
                        },
                        track="conceptual",
                    ),
                }
            )
            if skip_agent:
                _persist("conceptual_deepen", blocked_at="machine:conceptual_deepen")
                return TickResult(
                    True,
                    "machine:conceptual_deepen",
                    "conceptual_deepen",
                    None,
                    steps,
                    "needs_agent_enqueue",
                    pending,
                )
            return _agent_enqueue(
                vault_root,
                project_id=project_id,
                run_id=run_id,
                pending=pending,
                params=params,
                steps=steps,
                phase="conceptual_deepen",
                completed=completed,
                persist_fn=_persist,
            )

    if "catalog_mint" not in completed:
        if rec_action == "conceptual_deepen":
            pending.append(
                {
                    "mode": "RESUME_ROADMAP",
                    "params": merge_deepen_params(
                        vault_root,
                        {
                            "action": "deepen",
                            "roadmap_track": "conceptual",
                            "project_id": project_id,
                            "product_factory_run_id": run_id,
                            "queue_next": True,
                            "linked_phase": "conceptual",
                        },
                        track="conceptual",
                    ),
                }
            )
            _persist("conceptual_deepen", blocked_at="machine:conceptual_deepen")
            if skip_agent:
                return TickResult(
                    True,
                    "machine:conceptual_deepen",
                    "conceptual_deepen",
                    None,
                    steps,
                    "reconcile_conceptual_deepen",
                    pending,
                )
            return _agent_enqueue(
                vault_root,
                project_id=project_id,
                run_id=run_id,
                pending=pending,
                params=params,
                steps=steps,
                phase="conceptual_deepen",
                completed=completed,
                persist_fn=_persist,
            )
        ready, gate_reason = conceptual_track_ready(vault_root, project_id, **gate_kw)
        if not ready:
            _persist("catalog_mint", operator_loop=1, blocked_at=f"machine:conceptual_pre_freeze:{gate_reason}")
            return TickResult(
                True,
                f"machine:conceptual_pre_freeze",
                "catalog_mint",
                1,
                steps + [{"step": "conceptual_pre_freeze", "ok": False, "reason": gate_reason}],
                gate_reason,
            )
        freeze_stamp = stamp_factory_conceptual_freeze(
            vault_root, project_id, gate_signature=gate_reason
        )
        steps.append({"step": "conceptual_freeze_stamp", **freeze_stamp})
        # UX backlog replaces automatic PMG phase→slice-catalog flood.
        backlog = generate_ux_mint_backlog(
            vault_root,
            project_id=project_id,
            pmg_path=Path(vault_root / params["pmg_path"]) if params.get("pmg_path") else None,
        )
        steps.append({"step": "ux_mint_backlog", **backlog.to_dict()})
        bl_doc = load_mint_backlog(vault_root, project_id)
        bl_status = str(bl_doc.get("backlog_status") or "proposed")
        if not backlog.coverage_ok:
            _persist(
                "catalog_mint",
                operator_loop=1,
                blocked_at="ux_axis_coverage_gap",
            )
            return TickResult(
                True,
                "ux_axis_coverage_gap",
                "catalog_mint",
                1,
                steps,
                "ux_axis_coverage_gap",
            )
        if bl_status != "frozen_for_mint":
            _persist(
                "catalog_mint",
                operator_loop=1,
                blocked_at="ux_mint_backlog_prune",
            )
            return TickResult(
                True,
                "ux_mint_backlog_prune",
                "catalog_mint",
                1,
                steps,
                "ux_mint_backlog_prune",
            )
        from .catalog_mint_pack import emit_catalog_mint_pack
        from .roadmap_artifact_ledger import record_artifact

        pack = emit_catalog_mint_pack(
            vault_root,
            project_id=project_id,
            include_neighbors=bool(params.get("include_neighbors")),
            neighbor_cap=int(params.get("neighbor_cap") or 3),
            enqueue_thin_feed_research=bool(params.get("enqueue_thin_feed_research")),
        )
        steps.append({"step": "catalog_mint_pack", **pack.to_dict()})
        from .feed_envelope import assess_feed_completeness

        steps.append(
            {
                "step": "feed_completeness",
                **assess_feed_completeness(vault_root, project_id=project_id),
            }
        )
        paths = user_story_paths(vault_root, project_id)
        record_artifact(
            vault_root,
            project_id,
            artifact_path=str(paths["catalog"].parent.joinpath("MINT-BACKLOG.yaml").relative_to(vault_root)),
            event_type="ux_mint_backlog_written",
            product_factory_run_id=run_id,
            goal_authority_run_id=str((goal_packet or {}).get("run_id") or ""),
        )
        steps.append(
            {
                "step": "catalog_mint",
                "ok": True,
                "detail": "backlog_frozen_pack_emitted",
                "rows_added": 0,
                "note": "catalog rows enter only via operator/Grok receipt apply",
            }
        )
        completed.append("catalog_mint")

    if "loop2_prep" not in completed:
        from .loop2_prep import prepare_loop2_operator_surface
        from .done_when_eval import park_loop2_machine_ready
        from .ux_mint_backlog import backlog_summary

        bl_surf = backlog_summary(vault_root, project_id)
        paths = user_story_paths(vault_root, project_id)
        from .catalog_io import load_yaml, catalog_rows_by_id

        cat = load_yaml(paths["catalog"]) if paths["catalog"].is_file() else {"rows": []}
        planned = [
            rid
            for rid, r in catalog_rows_by_id(cat).items()
            if r.get("planned") is not False
        ]
        if not planned:
            steps.append(
                {
                    "step": "loop2_prep",
                    "ok": False,
                    "detail": "ux_mint_walk_pending",
                    "mint_backlog": bl_surf,
                }
            )
            _persist(
                "catalog_mint",
                operator_loop=1,
                blocked_at="ux_mint_walk_pending",
            )
            return TickResult(
                True,
                "ux_mint_walk_pending",
                "catalog_mint",
                1,
                steps,
                "ux_mint_walk_pending",
            )

        prep = prepare_loop2_operator_surface(vault_root, project_id=project_id)
        prep["mint_backlog"] = bl_surf
        steps.append({"step": "loop2_prep", **prep})
        if prep.get("ok"):
            completed.append("loop2_prep")
            park = park_loop2_machine_ready(vault_root, project_id)
            steps.append({"step": "loop2_machine_park", **park})

    # Loop 2
    l2 = check_operator_loop_2(vault_root, project_id)
    if not l2.ok:
        from .done_when_eval import LOOP_2_PENDING_SIGN_OFF, park_loop2_machine_ready

        park = park_loop2_machine_ready(vault_root, project_id)
        blocked = LOOP_2_PENDING_SIGN_OFF if park.get("ok") else l2.loop_id
        _persist("catalog_and_levels", operator_loop=2, blocked_at=blocked)
        return TickResult(True, blocked, "catalog_and_levels", 2, steps, blocked)

    if "depth_slice" not in completed:
        ds = run_depth_slicer(vault_root, project_id=project_id)
        steps.append({"step": "depth_slice", **ds})
        completed.append("depth_slice")

    # Execution engineering (machine)
    if profile == "greenfield" and not execution_track_exists(vault_root, project_id):
        if "execution_bootstrap" not in completed:
            pending.append(
                {
                    "mode": "RESUME_ROADMAP",
                    "params": {
                        "action": "bootstrap-execution-track",
                        "project_id": project_id,
                        "product_factory_run_id": run_id,
                    },
                }
            )
            if skip_agent:
                _persist("execution_bootstrap", blocked_at="machine:execution_bootstrap")
                return TickResult(
                    True,
                    "machine:execution_bootstrap",
                    "execution_bootstrap",
                    None,
                    steps,
                    "needs_agent_enqueue",
                    pending,
                )
            return _agent_enqueue(
                vault_root,
                project_id=project_id,
                run_id=run_id,
                pending=pending,
                params=params,
                steps=steps,
                phase="execution_bootstrap",
                completed=completed,
                persist_fn=_persist,
            )

    if profile == "gmm_resume" and execution_track_exists(vault_root, project_id):
        if "execution_bootstrap" not in completed:
            from .execution_track_ready import execution_track_ready

            exec_ready, _exec_reason = execution_track_ready(vault_root, project_id)
            if exec_ready:
                completed.append("execution_bootstrap")

    if "execution_deepen" not in completed:
        audit = run_execution_pseudo_code_audit(vault_root, project_id=project_id)
        steps.append({"step": "execution_pseudo_code_audit", **audit.to_dict()})
        if audit.ok:
            pin_sync = sync_catalog_execution_pins(vault_root, project_id=project_id)
            steps.append({"step": "execution_pin_sync", **pin_sync.to_dict()})
            completed.append("execution_deepen")
            from .product_factory_ux_context import build_ux_context

            ux = build_ux_context(vault_root, project_id=project_id)
            pf = load_product_factory(vault_root, project_id)
            ed = dict(pf.get("execution_deepen") or {}) if isinstance(pf.get("execution_deepen"), dict) else {}
            ed["audit_passed_at"] = _utc_iso()
            ed["waiting_agent"] = False
            save_product_factory(
                vault_root,
                project_id,
                {**pf, "execution_deepen": ed, "ux_context": ux},
            )
        else:
            pf = load_product_factory(vault_root, project_id)
            ed = dict(pf.get("execution_deepen") or {}) if isinstance(pf.get("execution_deepen"), dict) else {}
            passes = int(ed.get("passes") or 0)
            if passes >= MAX_EXECUTION_DEEPEN_PASSES:
                stall = {
                    "phase": "execution_deepen",
                    "stall_reason": "max_deepen_passes",
                    "passes": passes,
                    "violations": list(audit.violations),
                }
                save_product_factory(
                    vault_root,
                    project_id,
                    {**pf, "product_factory_stall": stall, "execution_deepen": ed},
                )
                _persist("execution_deepen", blocked_at="machine:execution_deepen")
                return TickResult(
                    False,
                    "machine:execution_deepen",
                    "execution_deepen",
                    None,
                    steps,
                    "product_factory_stall",
                    pending,
                )

            deepen_pending: list[dict[str, Any]] = []
            if audit.gaps and passes > 0:
                research_out = _enqueue_research_gaps(
                    vault_root,
                    project_id=project_id,
                    lane=lane,
                    gaps=audit.gaps,
                    linked_phase="execution_deepen",
                )
                steps.append({"step": "execution_gap_research", **research_out})

            deepen_pending.append(
                {
                    "mode": "RESUME_ROADMAP",
                    "params": merge_deepen_params(
                        vault_root,
                        {
                            "action": "deepen",
                            "roadmap_track": "execution",
                            "project_id": project_id,
                            "product_factory_run_id": run_id,
                            "queue_next": True,
                            "linked_phase": "execution",
                        },
                        track="execution",
                    ),
                }
            )
            ed["passes"] = passes + 1
            ed["waiting_agent"] = True
            save_product_factory(vault_root, project_id, {**pf, "execution_deepen": ed})

            if skip_agent:
                _persist("execution_deepen", blocked_at="machine:execution_deepen")
                return TickResult(
                    True,
                    "machine:execution_deepen",
                    "execution_deepen",
                    None,
                    steps,
                    "needs_agent_enqueue",
                    deepen_pending,
                )
            return _agent_enqueue(
                vault_root,
                project_id=project_id,
                run_id=run_id,
                pending=deepen_pending,
                params=params,
                steps=steps,
                phase="execution_deepen",
                completed=completed,
                persist_fn=_persist,
            )

    if "wire_execution_pins" not in completed:
        wp = wire_execution_pins(vault_root, project_id=project_id)
        steps.append({"step": "wire_execution_pins", **wp.to_dict()})
        if wp.ok:
            completed.append("wire_execution_pins")
        else:
            _persist("wire_execution_pins", blocked_at="machine:execution_pins_wired")
            return TickResult(
                False,
                "machine:execution_pins_wired",
                "wire_execution_pins",
                None,
                steps,
                ";".join(wp.violations),
            )

    eng = check_execution_engineering(vault_root, project_id)
    if not eng.ok:
        fail_id = next((c[0] for c in eng.sub_checks if not c[1]), "execution_engineering")
        _persist("execution_engineering", blocked_at=f"machine:{fail_id}")
        return TickResult(
            True,
            f"machine:{fail_id}",
            "execution_engineering",
            None,
            steps,
            "execution_engineering_incomplete",
            pending,
        )
    completed.append("execution_engineering")

    # Loop 3
    l3 = check_operator_loop_3(vault_root, project_id)
    if not l3.ok:
        _persist("slice_selection", operator_loop=3, blocked_at=l3.loop_id)
        return TickResult(True, l3.loop_id, "slice_selection", 3, steps, "operator_loop_3_slice_selection")

    if FACTORY_STAGED not in completed and LEGACY_FACTORY_STAGE not in (pf.get("completed_phases") or []) and not params.get("dry_run"):
        if rec_action == "execution_deepen" and not reconcile.execution_ready:
            pending.append(
                {
                    "mode": "RESUME_ROADMAP",
                    "params": merge_deepen_params(
                        vault_root,
                        {
                            "action": "deepen",
                            "roadmap_track": "execution",
                            "project_id": project_id,
                            "product_factory_run_id": run_id,
                            "queue_next": True,
                            "linked_phase": "execution",
                        },
                        track="execution",
                    ),
                }
            )
            _persist("execution_deepen", blocked_at="machine:execution_deepen")
            if skip_agent:
                return TickResult(
                    True,
                    "machine:execution_deepen",
                    "execution_deepen",
                    None,
                    steps,
                    "reconcile_execution_deepen",
                    pending,
                )
            return _agent_enqueue(
                vault_root,
                project_id=project_id,
                run_id=run_id,
                pending=pending,
                params=params,
                steps=steps,
                phase="execution_deepen",
                completed=completed,
                persist_fn=_persist,
            )
        from .execution_track_ready import execution_factory_handoff_ready

        exec_ready, exec_reason = execution_factory_handoff_ready(vault_root, project_id)
        if not exec_ready:
            steps.append({"step": "execution_handoff_gate", "ok": False, "reason": exec_reason})
            _persist("execution_handoff", blocked_at=f"machine:execution_handoff:{exec_reason}")
            return TickResult(
                True,
                f"machine:execution_handoff",
                "execution_handoff",
                None,
                steps,
                exec_reason,
                pending,
            )
        tail = _run_factory_compose_tail(
            vault_root,
            project_id=project_id,
            run_id=run_id,
            lane=lane,
            pf=pf,
            params=params,
            steps=steps,
            completed=completed,
            _persist=_persist,
        )
        if tail is not None:
            return tail

    if FACTORY_CELL_COMPLETE in completed:
        _persist("ready", operator_loop=_loop_num(resolve_blocking_operator_loop(vault_root, project_id)))
        return TickResult(True, None, pf.get("phase") or "ready", None, steps, "tick_complete", pending)

    if FACTORY_STAGED in completed:
        cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
        cell_phase = str(cell.get("phase") or "lanes_running")
        _persist(cell_phase, operator_loop=None, blocked_at=None)
        return TickResult(
            True,
            None,
            cell_phase,
            None,
            steps,
            "factory_cell_in_progress",
        )

    _persist("ready", operator_loop=_loop_num(resolve_blocking_operator_loop(vault_root, project_id)))
    return TickResult(True, None, pf.get("phase") or "ready", None, steps, "tick_complete", pending)


def launch(
    vault_root: Path,
    *,
    project_id: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Entry: initialize run_id and tick until block, or resume without ledger wipe."""
    params = dict(params or {})
    goal_packet = params.get("goal_packet") if isinstance(params.get("goal_packet"), dict) else None

    if not should_factory_bootstrap(vault_root, project_id, goal_packet, params):
        pf = load_product_factory(vault_root, project_id)
        run_id = str(pf.get("run_id") or uuid.uuid4().hex[:12])
        if not pf.get("run_id"):
            save_product_factory(vault_root, project_id, {**pf, "run_id": run_id})
        out = tick(vault_root, project_id=project_id, params=params)
        return {**out.to_dict(), "bootstrap": False, "resumed": True}

    profile = detect_project_profile(vault_root, project_id)
    run_id = uuid.uuid4().hex[:12]
    save_product_factory(
        vault_root,
        project_id,
        {
            "project_id": project_id,
            "project_profile": profile,
            "run_id": run_id,
            "ux_first": True,
            "completed_phases": [],
            "active_slice": {"row_ids": [], "dispatch_depth": None},
            "started_at": _utc_iso(),
        },
    )
    out = tick(vault_root, project_id=project_id, params=params)
    return {**out.to_dict(), "bootstrap": True}


# Deprecated alias — use bootstrap (= reset factory cursor + tick).
relaunch = launch
bootstrap = launch


def confirm_slice_selection(
    vault_root: Path,
    *,
    project_id: str,
    row_ids: list[str],
    dispatch_depth: int,
) -> dict[str, Any]:
    pf = load_product_factory(vault_root, project_id)
    completed = clear_factory_beat_phases(
        normalize_completed_phases(list(pf.get("completed_phases") or []))
    )
    from .work_order_translate import assemble_pillar_packet

    from .product_factory_ux_context import build_ux_context

    run_id = str(pf.get("run_id") or uuid.uuid4().hex[:12])
    active_slice = {"row_ids": row_ids, "dispatch_depth": dispatch_depth}
    ux_context = build_ux_context(
        vault_root, project_id=project_id, active_slice=active_slice
    )
    packet = assemble_pillar_packet(
        vault_root,
        project_id=project_id,
        producer_run_id=f"sp-pending-{run_id[:8]}",
        active_slice=active_slice,
    )
    slice_id = str(packet.get("slice_id") or "") if packet else ""
    cell = (
        default_implementation_cell(slice_id=slice_id, producer_run_id=f"sp-pending-{run_id[:8]}")
        if slice_id
        else {"phase": "awaiting_compose", "pm_review_status": "idle"}
    )
    save_product_factory(
        vault_root,
        project_id,
        {
            **pf,
            "active_slice": active_slice,
            "slice_selection_confirmed_at": _utc_iso(),
            "ux_context": ux_context,
            "operator_loop": 3,
            "phase": "slice_selection",
            "completed_phases": completed,
            "implementation_cell": cell,
        },
    )
    return {"ok": True, "row_ids": row_ids, "dispatch_depth": dispatch_depth, "slice_id": slice_id}
