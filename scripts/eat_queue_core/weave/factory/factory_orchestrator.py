"""Factory orchestrator — vault_roadmap feed (product factory loop 3) or legacy alpha queue."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .drop_contract_base import bootstrap_all_drop_manifests
from .tech_stack_manifest import load_manifest
from .factory_correlation import append_factory_event, append_gate_log
from .factory_output_gate import parse_factory_orchestrator_yaml
from .factory_run_summary import write_factory_run_summary
from .factory_bootstrap import evaluate_bootstrap_gates, load_bootstrap_policy
from .factory_dispatch_policy import allow_dispatch_with_red_gates, dispatch_policy_payload
from .factory_honesty_rollup import honesty_rollup_summary, run_factory_honesty_rollup
from .factory_project import load_factory_project
from .interpretation_pass import run_interpretation_pass
from .lane_charters import validate_six_lane_charters
from .lane_factories import dispatch_slice_lanes, enrich_job_from_charter
from .merge_barrier import filter_dispatch_jobs, reset_slice_barrier
from .surface_pass import run_surface_pass
from ..user_story.work_order_translate import (
    FEED_ALPHA_QUEUE,
    FEED_VAULT_ROADMAP,
    resolve_feed_authority,
    translate_failure_reason,
    translate_vault_work_orders,
)

DEFAULT_QUEUE_REL = "1-Projects/godot-genesis-mythos-master/Factory-DRB/alpha-factory-queue.yaml"
DISPATCH_DIR_REL = ".technical/factory/dispatch"


@dataclass(frozen=True)
class OrchestratorResult:
    ok: bool
    active_slice_id: str | None
    dispatch_path: str | None
    jobs: tuple[dict[str, Any], ...]
    blocked_jobs: tuple[dict[str, Any], ...]
    gate_violations: tuple[str, ...]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "active_slice_id": self.active_slice_id,
            "dispatch_path": self.dispatch_path,
            "jobs": list(self.jobs),
            "blocked_jobs": list(self.blocked_jobs),
            "gate_violations": list(self.gate_violations),
            "detail": self.detail,
        }


def load_alpha_queue(vault_root: Path, rel: str = DEFAULT_QUEUE_REL) -> dict[str, Any]:
    path = vault_root / rel
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _active_slice(queue: dict[str, Any]) -> dict[str, Any] | None:
    slices = queue.get("slices") or []
    if not isinstance(slices, list):
        return None
    for item in slices:
        if isinstance(item, dict) and str(item.get("status")) == "active":
            return item
    for item in slices:
        if isinstance(item, dict) and str(item.get("status")) == "pending":
            return item
    return None


def _parallel_enabled(vault_root: Path) -> bool:
    cfg_path = vault_root / "3-Resources/Second-Brain-Config.md"
    raw = parse_factory_orchestrator_yaml(cfg_path)
    return bool(raw.get("parallel_factory_lanes_enabled"))


def _manifest_stack_baseline_vetted(vault_root: Path) -> bool:
    try:
        return bool(load_manifest(vault_root).operator_stack_baseline_vetted)
    except (FileNotFoundError, OSError, ValueError):
        return False


def run_factory_orchestrator(
    vault_root: Path,
    *,
    queue_rel: str = DEFAULT_QUEUE_REL,
    write_dispatch: bool = True,
    run_gates: bool = True,
    run_id: str | None = None,
    feed_authority: str | None = None,
    project_id: str | None = None,
    active_slice: dict[str, Any] | None = None,
) -> OrchestratorResult:
    vault_root = vault_root.resolve()
    run_id = run_id or f"factory-orch-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    authority = resolve_feed_authority(vault_root, feed_authority)

    pid = str(project_id or "").strip()
    if pid and authority == FEED_VAULT_ROADMAP:
        from .implementation_handoff_ready import implementation_handoff_ready

        handoff_ok, handoff_reason = implementation_handoff_ready(vault_root, pid)
        if not handoff_ok:
            return OrchestratorResult(
                ok=False,
                active_slice_id=None,
                dispatch_path=None,
                jobs=(),
                blocked_jobs=(),
                gate_violations=(f"implementation_handoff_blocked:{handoff_reason}",),
                detail=f"implementation_handoff_blocked:{handoff_reason}",
            )

    if authority == FEED_VAULT_ROADMAP:
        bootstrap = load_factory_project(vault_root, project_id)
        return _run_vault_roadmap_orchestrator(
            vault_root,
            queue=bootstrap,
            write_dispatch=write_dispatch,
            run_gates=run_gates,
            run_id=run_id,
            active_slice=active_slice,
        )

    queue = load_alpha_queue(vault_root, queue_rel)
    if not queue:
        return OrchestratorResult(
            ok=False,
            active_slice_id=None,
            dispatch_path=None,
            jobs=(),
            blocked_jobs=(),
            gate_violations=("alpha_factory_queue_missing",),
            detail="queue_missing",
        )

    return _run_alpha_queue_orchestrator(
        vault_root,
        queue=queue,
        write_dispatch=write_dispatch,
        run_gates=run_gates,
        run_id=run_id,
    )


def _run_vault_roadmap_orchestrator(
    vault_root: Path,
    *,
    queue: dict[str, Any],
    write_dispatch: bool,
    run_gates: bool,
    run_id: str,
    active_slice: dict[str, Any] | None = None,
) -> OrchestratorResult:
    game_repo_rel = str(queue.get("game_repo_path") or "")
    game_repo = vault_root / game_repo_rel.strip("/")
    if not game_repo_rel or not game_repo.is_dir():
        return OrchestratorResult(
            ok=False,
            active_slice_id=None,
            dispatch_path=None,
            jobs=(),
            blocked_jobs=(),
            gate_violations=("game_repo_missing",),
            detail="game_repo_missing",
        )

    project_id = str(queue.get("project_id") or "")
    bundle = translate_vault_work_orders(
        vault_root,
        project_id=project_id,
        queue_bootstrap=queue,
        active_slice=active_slice,
    )
    if bundle is None:
        reason = translate_failure_reason(
            vault_root, project_id=project_id, active_slice=active_slice
        )
        return OrchestratorResult(
            ok=False,
            active_slice_id=None,
            dispatch_path=None,
            jobs=(),
            blocked_jobs=(),
            gate_violations=(reason,),
            detail=reason,
        )

    bootstrap_all_drop_manifests(game_repo)

    charter_v = validate_six_lane_charters(vault_root)
    if charter_v:
        return OrchestratorResult(
            ok=False,
            active_slice_id=None,
            dispatch_path=None,
            jobs=(),
            blocked_jobs=(),
            gate_violations=tuple(charter_v),
            detail="lane_charters_invalid",
        )

    bootstrap_ok, bootstrap_violations = evaluate_bootstrap_gates(
        vault_root, queue, run_honesty_checks=run_gates
    )
    if not bootstrap_ok:
        return OrchestratorResult(
            ok=False,
            active_slice_id=None,
            dispatch_path=None,
            jobs=(),
            blocked_jobs=(),
            gate_violations=tuple(bootstrap_violations),
            detail="bootstrap_gates_blocked",
        )

    active = bundle.active_slice()
    slice_id = bundle.slice_id
    reset_slice_barrier(vault_root, slice_id)
    job_dicts = list(bundle.jobs)

    return _finalize_orchestrator_dispatch(
        vault_root,
        queue=queue,
        active=active,
        slice_id=slice_id,
        game_repo_rel=game_repo_rel,
        job_dicts=job_dicts,
        write_dispatch=write_dispatch,
        run_gates=run_gates,
        run_id=run_id,
        feed_metadata=bundle.feed_metadata(),
    )


def _run_alpha_queue_orchestrator(
    vault_root: Path,
    *,
    queue: dict[str, Any],
    write_dispatch: bool,
    run_gates: bool,
    run_id: str,
) -> OrchestratorResult:
    game_repo_rel = str(queue.get("game_repo_path") or "")
    game_repo = vault_root / game_repo_rel.strip("/")
    if not game_repo_rel or not game_repo.is_dir():
        return OrchestratorResult(
            ok=False,
            active_slice_id=None,
            dispatch_path=None,
            jobs=(),
            blocked_jobs=(),
            gate_violations=("game_repo_missing",),
            detail="game_repo_missing",
        )

    bootstrap_all_drop_manifests(game_repo)

    charter_v = validate_six_lane_charters(vault_root)
    if charter_v:
        return OrchestratorResult(
            ok=False,
            active_slice_id=None,
            dispatch_path=None,
            jobs=(),
            blocked_jobs=(),
            gate_violations=tuple(charter_v),
            detail="lane_charters_invalid",
        )

    bootstrap_ok, bootstrap_violations = evaluate_bootstrap_gates(
        vault_root, queue, run_honesty_checks=run_gates
    )
    if not bootstrap_ok:
        return OrchestratorResult(
            ok=False,
            active_slice_id=None,
            dispatch_path=None,
            jobs=(),
            blocked_jobs=(),
            gate_violations=tuple(bootstrap_violations),
            detail="bootstrap_gates_blocked",
        )

    active = _active_slice(queue)
    if active is None:
        return OrchestratorResult(
            ok=False,
            active_slice_id=None,
            dispatch_path=None,
            jobs=(),
            blocked_jobs=(),
            gate_violations=("no_active_slice",),
            detail="no_active_slice",
        )

    slice_id = str(active.get("id") or "")
    reset_slice_barrier(vault_root, slice_id)
    lane_ids = tuple(str(x) for x in (active.get("lanes") or []) if x)
    raw_jobs = dispatch_slice_lanes(
        vault_root,
        slice_id=slice_id,
        lane_ids=lane_ids,
        game_repo_rel=game_repo_rel,
    )
    job_dicts = [enrich_job_from_charter(vault_root, j.to_dict()) for j in raw_jobs]

    return _finalize_orchestrator_dispatch(
        vault_root,
        queue=queue,
        active=active,
        slice_id=slice_id,
        game_repo_rel=game_repo_rel,
        job_dicts=job_dicts,
        write_dispatch=write_dispatch,
        run_gates=run_gates,
        run_id=run_id,
        feed_metadata={"feed_authority": "alpha_queue"},
    )


def _finalize_orchestrator_dispatch(
    vault_root: Path,
    *,
    queue: dict[str, Any],
    active: dict[str, Any],
    slice_id: str,
    game_repo_rel: str,
    job_dicts: list[dict[str, Any]],
    write_dispatch: bool,
    run_gates: bool,
    run_id: str,
    feed_metadata: dict[str, Any] | None = None,
) -> OrchestratorResult:
    lane_ids = tuple(str(x) for x in (active.get("lanes") or []) if x)

    gate_violations: list[str] = []
    if run_gates:
        interp = run_interpretation_pass(vault_root, lane_id=lane_ids[0] if lane_ids else None)
        append_gate_log(
            vault_root, "interpretation_pass", ok=interp.ok, run_id=run_id, slice_id=slice_id
        )
        if not interp.ok:
            gate_violations.extend(interp.little_val.anti_pattern_violations)

        surface = run_surface_pass(vault_root, run_probes=False)
        append_gate_log(vault_root, "surface_pass", ok=surface.ok, run_id=run_id, slice_id=slice_id)
        if not surface.ok:
            gate_violations.extend(surface.little_val.anti_pattern_violations)

        honesty = run_factory_honesty_rollup(vault_root)
        for name, hres in honesty.get("passes", {}).items():
            append_gate_log(
                vault_root,
                name,
                ok=hres.ok,
                run_id=run_id,
                slice_id=slice_id,
            )
            if not hres.ok:
                gate_violations.extend(hres.little_val.anti_pattern_violations)

    parallel = _parallel_enabled(vault_root)
    allowed_jobs, blocked_jobs = filter_dispatch_jobs(
        vault_root, job_dicts, game_repo_rel=game_repo_rel, parallel_enabled=parallel
    )

    for job in allowed_jobs:
        append_factory_event(
            vault_root,
            "godot",
            "dispatch_job",
            run_id=run_id,
            factory_lane=str(job.get("lane_id")),
            slice_id=slice_id,
            message="orchestrator_dispatch",
        )

    dispatch_path: str | None = None
    if write_dispatch:
        out_dir = vault_root / DISPATCH_DIR_REL
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_file = out_dir / f"dispatch-{stamp}.json"
        payload = {
            "schema_version": 2,
            "run_id": run_id,
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
            "project_id": queue.get("project_id"),
            "game_repo_path": game_repo_rel,
            "archive_repo_path": queue.get("archive_repo_path"),
            "execution_roadmap_ref": queue.get("execution_roadmap_ref"),
            "feed_authority": (feed_metadata or {}).get("feed_authority", "alpha_queue"),
            "vault_feed": feed_metadata or {},
            "active_slice": active,
            "forbidden_shortcuts": queue.get("forbidden_shortcuts") or [],
            "jobs": allowed_jobs,
            "blocked_jobs": blocked_jobs,
            "parallel_factory_lanes_enabled": parallel,
            "gate_violations": gate_violations,
            "dispatch_policy": dispatch_policy_payload(active),
            "factory_bootstrap": load_bootstrap_policy(queue),
            "stack_baseline_vetted": _manifest_stack_baseline_vetted(vault_root),
            "honesty_rollup": honesty_rollup_summary(
                run_factory_honesty_rollup(vault_root)
            ),
            "ok_to_implement": len(gate_violations) == 0 or allow_dispatch_with_red_gates(active),
        }
        out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        latest = out_dir / "latest.json"
        latest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        dispatch_path = str(out_file.relative_to(vault_root))
        write_factory_run_summary(vault_root, run_id=run_id)

    ok = bool(allowed_jobs) and (
        not run_gates or len(gate_violations) == 0 or allow_dispatch_with_red_gates(active)
    )
    detail = "dispatch_ok" if ok else "; ".join(gate_violations) or "dispatch_blocked"
    return OrchestratorResult(
        ok=bool(ok),
        active_slice_id=slice_id,
        dispatch_path=dispatch_path,
        jobs=tuple(allowed_jobs),
        blocked_jobs=tuple(blocked_jobs),
        gate_violations=tuple(gate_violations),
        detail=detail,
    )
