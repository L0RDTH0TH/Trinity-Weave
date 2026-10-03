"""Stage factory orchestrator dispatch jobs onto the lane PQ for headless eat."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from ...lane_bundle import bundle_dir_for_lane
from ...queue_bus import append_raw_queue_entries
from ..persona_handoff import merge_persona_into_params
from ..user_story.product_factory_state import (
    FACTORY_STAGED,
    load_product_factory,
    save_product_factory,
    update_implementation_cell,
)
from .factory_orchestrator import run_factory_orchestrator
from .factory_project import factory_project_rel, load_factory_project
from .prefer_authorship_contract import (
    PRODUCT_PREFER_DO_NOT_WAIVE,
    slice_requires_prefer_authorship,
)
from .slice_producer_harness import load_cell_dispatch_plan, load_producer_receipt, technical_slice_dir


def _pq_path(vault_root: Path, lane: str) -> Path:
    return bundle_dir_for_lane(vault_root, lane) / "prompt-queue.jsonl"


def _existing_factory_jobs(vault_root: Path, lane: str) -> set[tuple[str, str, int]]:
    pq = _pq_path(vault_root, lane)
    if not pq.is_file():
        return set()
    keys: set[tuple[str, str, int]] = set()
    for line in pq.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        params = row.get("params") if isinstance(row.get("params"), dict) else {}
        if str(params.get("action") or "").lower() != "factory_lane":
            continue
        sid = str(params.get("slice_id") or "")
        lid = str(params.get("lane_id") or "")
        rework = int(params.get("rework_iteration") or 0)
        if sid and lid:
            keys.add((sid, lid, rework))
    return keys


_VAULT_EXIT_GATES = (
    "surface_pass",
    "factory_output_conduct",
    "product_kinesthetic_honesty",
)


def armed_packet_rel_for_slice(project_id: str, slice_id: str) -> str:
    """Sibling armed packet of the slice brief: ``{slice_id}.armed.yaml``."""
    return f"1-Projects/{project_id}/Factory-DRB/slice-briefs/{slice_id}.armed.yaml"


def resolve_sibling_armed_packet(
    vault_root: Path, *, project_id: str, slice_id: str
) -> tuple[str, dict[str, Any]]:
    """Return (rel_path, armed_dict); ('', {}) when no sibling armed packet exists."""
    if not project_id or not slice_id:
        return "", {}
    rel = armed_packet_rel_for_slice(project_id, slice_id)
    path = vault_root / rel
    if not path.is_file():
        return "", {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return rel, {}
    return rel, data if isinstance(data, dict) else {}


def resolve_authority_armed_packet(
    vault_root: Path, *, project_id: str, slice_id: str
) -> tuple[str, dict[str, Any]]:
    """Armed packet with authority for a slice: sibling first, else project pointer.

    The project-level pointer matters because a stale implementation cell can tick
    under a different ``slice_id`` and still needs the armed law for context.
    """
    rel, armed = resolve_sibling_armed_packet(
        vault_root, project_id=project_id, slice_id=slice_id
    )
    if rel:
        return rel, armed
    # load_factory_project normalizes away armed_* keys — read the manifest directly.
    manifest_path = vault_root / factory_project_rel(project_id)
    if not manifest_path.is_file():
        return "", {}
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return "", {}
    if not isinstance(manifest, dict):
        return "", {}
    rel = str(manifest.get("armed_packet") or "").strip()
    path = vault_root / rel if rel else None
    if not rel or path is None or not path.is_file():
        return "", {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return rel, {}
    return rel, data if isinstance(data, dict) else {}


def armed_slice_authority_note(
    armed: dict[str, Any] | None, *, slice_id: str = ""
) -> str:
    """Advisory only — GO is an operator chat kickoff, never a YAML word-gate.

    Staging is never refused from armed-packet state. When the project's armed slice
    differs from the slice the orchestrator composed, return a note so the staged
    result carries the divergence for review; the armed slice stays the weld target.
    """
    armed = armed if isinstance(armed, dict) else {}
    armed_slice = str(armed.get("slice_id") or "")
    if slice_id and armed_slice and armed_slice != slice_id:
        return f"armed_slice_divergence:{armed_slice}!={slice_id}"
    return ""


def factory_lane_entries_from_dispatch(
    vault_root: Path,
    *,
    lane: str,
    packet: dict[str, Any],
    run_id: str,
    jobs: list[dict[str, Any]],
    slice_id: str,
    wave: int = 1,
    producer_receipt: dict[str, Any] | None = None,
    rework_iteration: int = 0,
) -> list[dict[str, Any]]:
    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    repo_rel = str(
        jobs[0].get("game_repo_rel") if jobs else hints.get("repo_path") or ""
    ).rstrip("/") + "/"
    project_id = str(packet.get("project_id") or "genesis-mythos-master")
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    existing = _existing_factory_jobs(vault_root, lane)
    vault_lanes = sorted({str(j.get("lane_id")) for j in jobs if j.get("lane_id")})
    vault_feed = any(str(j.get("feed_authority") or "") == "vault_roadmap" for j in jobs)

    cdp = None
    lane_missions: dict[str, Any] = {}
    sib_path = ""
    cdp_path = ""
    producer_run_id = ""
    if producer_receipt:
        sib_path = str(producer_receipt.get("sib_path") or "")
        cdp_path = str(producer_receipt.get("cdp_path") or "")
        producer_run_id = str(producer_receipt.get("producer_run_id") or "")
        cdp = load_cell_dispatch_plan(vault_root, cdp_path) if cdp_path else None
        if cdp:
            lane_missions = cdp.get("lane_missions") if isinstance(cdp.get("lane_missions"), dict) else {}

    wave_lanes: set[str] | None = None
    wave_lane_list: list[str] = []
    if cdp:
        for wdef in cdp.get("waves") or []:
            if isinstance(wdef, dict) and int(wdef.get("wave") or 0) == wave:
                wave_lane_list = [str(x) for x in (wdef.get("lanes") or []) if x]
                wave_lanes = set(wave_lane_list)
                break

    armed_rel, armed = resolve_sibling_armed_packet(
        vault_root, project_id=project_id, slice_id=slice_id
    )

    receipts_dir = technical_slice_dir(vault_root, slice_id) / "receipts" if slice_id else None

    def _sibling_status(for_lane: str) -> list[dict[str, Any]]:
        if not receipts_dir or not wave_lane_list:
            return []
        sibs: list[dict[str, Any]] = []
        for wl in wave_lane_list:
            if wl == for_lane:
                continue
            rp = receipts_dir / f"{wl}.json"
            sibs.append(
                {
                    "lane_id": wl,
                    "receipt_path": str(rp.relative_to(vault_root)) if rp.is_file() else "",
                    "ok": bool(rp.is_file()),
                }
            )
        return sibs

    out: list[dict[str, Any]] = []
    for job in jobs:
        lid = str(job.get("lane_id") or "")
        if not lid:
            continue
        if wave_lanes is not None and lid not in wave_lanes:
            continue
        key = (slice_id, lid, rework_iteration)
        if key in existing:
            continue
        mission_info = lane_missions.get(lid) if isinstance(lane_missions.get(lid), dict) else {}
        mission_path = str(mission_info.get("mission_path") or "")
        ux_bullet_ids = mission_info.get("ux_bullet_ids") or []
        eid = f"factory-{run_id[:8]}-{lid}-{uuid.uuid4().hex[:6]}"
        if rework_iteration:
            eid = f"{eid}-r{rework_iteration}"
        half_a_prov = job.get("half_a_provenance")
        if not isinstance(half_a_prov, dict):
            half_a_prov = producer_receipt.get("half_a_provenance") if producer_receipt else None
        lane_params: dict[str, Any] = {
            "action": "factory_lane",
            "effective_track": "implementation",
            "slice_id": slice_id,
            "lane_id": lid,
            "factory_name": job.get("factory_name"),
            "primary_artifact": job.get("primary_artifact"),
            "zone_write": job.get("zone_write") or [],
            "checklist_ids": job.get("checklist_ids") or [],
            "repo_path": repo_rel,
            "engine_adapter": hints.get("engine_adapter") or "godot_4_6_3_dotnet",
            "factory_dispatch_run_id": run_id,
            "catalog_row_id": job.get("catalog_row_id") or "",
            "target_depth": job.get("target_depth"),
            "dispatch_depth": job.get("dispatch_depth"),
            "current_depth": job.get("current_depth"),
            "rollout_version": job.get("rollout_version"),
            "execution_pin": job.get("execution_pin") or "",
            "beat_ref": job.get("beat_ref") or "",
            "feed_authority": job.get("feed_authority") or hints.get("feed_authority") or "",
            "vault_feed_objective": str(job.get("vault_feed_objective") or "")[:800],
            "vault_required_lanes": vault_lanes if vault_feed else [],
            "vault_exit_gates": list(_VAULT_EXIT_GATES) if vault_feed else [],
            "dependency_warnings": job.get("dependency_warnings") or [],
            "slice_brief_path": sib_path,
            "lane_mission_path": mission_path,
            "cell_dispatch_plan_path": cdp_path,
            "producer_run_id": producer_run_id,
            "wave": wave,
            "rework_iteration": rework_iteration,
            "ux_bullet_ids": ux_bullet_ids,
        }
        if isinstance(half_a_prov, dict):
            lane_params["half_a_provenance"] = half_a_prov
        if armed_rel:
            lane_params["armed_packet_path"] = armed_rel
            lane_params["half_b_brief_path"] = str(armed.get("brief_path") or sib_path or "")
            lane_params["half_b_overlay_slice_id"] = str(armed.get("slice_id") or slice_id)
            ask_id = str(armed.get("ask_id") or "")
            if ask_id:
                lane_params["ask_id"] = ask_id
            umbrella = str(armed.get("umbrella_ask_id") or "")
            if umbrella:
                lane_params["umbrella_ask_id"] = umbrella
            if armed.get("step1_authorship") or (
                isinstance(armed.get("locks"), dict)
                and (
                    armed["locks"].get("step1_authorship")
                    or armed["locks"].get("step1_occupancy")
                )
            ):
                lane_params["step1_authorship"] = True
        if slice_requires_prefer_authorship(slice_id, lane_params):
            lane_params["do_not_waive"] = list(PRODUCT_PREFER_DO_NOT_WAIVE)
        lane_params["sibling_lane_status"] = _sibling_status(lid)
        lane_params = merge_persona_into_params(lane_params)
        out.append(
            {
                "id": eid,
                "mode": "IMPLEMENT_SLICE",
                "timestamp": now,
                "project_id": project_id,
                "queue_lane": lane,
                "params": lane_params,
                "architect_orchestration_run_id": run_id,
            }
        )
    return out


def _prepare_factory_dispatch(
    vault_root: Path,
    lane: str,
    packet: dict[str, Any],
    *,
    run_id: str,
    wave: int = 1,
) -> dict[str, Any]:
    """Run orchestrator and build IMPLEMENT_SLICE entries for one CDP wave."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    project_id = str(packet.get("project_id") or hints.get("project_id") or "genesis-mythos-master")

    from .implementation_handoff_ready import implementation_handoff_ready

    handoff_ok, handoff_reason = implementation_handoff_ready(vault_root, project_id)
    if not handoff_ok:
        return {
            "ok": False,
            "orchestrator": None,
            "entries": [],
            "detail": f"implementation_handoff_blocked:{handoff_reason}",
            "project_id": project_id,
            "wave": wave,
        }

    bootstrap = load_factory_project(vault_root, project_id)
    pf = load_product_factory(vault_root, project_id)
    active_slice = None
    if pf.get("slice_selection_confirmed_at"):
        raw = pf.get("active_slice")
        active_slice = raw if isinstance(raw, dict) else None

    orch = run_factory_orchestrator(
        vault_root,
        write_dispatch=True,
        run_gates=True,
        feed_authority=str(hints.get("feed_authority") or bootstrap.get("feed_authority") or "") or None,
        project_id=project_id,
        active_slice=active_slice,
    )
    result = orch.to_dict()
    if not orch.ok and not orch.jobs:
        return {
            "ok": False,
            "orchestrator": result,
            "entries": [],
            "detail": orch.detail,
            "project_id": project_id,
            "wave": wave,
        }

    slice_id = str(orch.active_slice_id or "")

    armed_rel, armed = resolve_authority_armed_packet(
        vault_root, project_id=project_id, slice_id=slice_id
    )
    armed_note = armed_slice_authority_note(armed, slice_id=slice_id)

    vault_feed = any(str(j.get("feed_authority") or "") == "vault_roadmap" for j in orch.jobs)
    producer_receipt = load_producer_receipt(vault_root, slice_id) if vault_feed else {"ok": True}
    if vault_feed and (not producer_receipt or not producer_receipt.get("ok")):
        return {
            "ok": False,
            "orchestrator": result,
            "entries": [],
            "detail": "producer_receipt_missing",
            "project_id": project_id,
            "slice_id": slice_id,
            "wave": wave,
        }

    entries = factory_lane_entries_from_dispatch(
        vault_root,
        lane=lane,
        packet=packet,
        run_id=run_id,
        jobs=list(orch.jobs),
        slice_id=slice_id,
        wave=int(wave),
        producer_receipt=producer_receipt if vault_feed else None,
    )

    # Fail-closed dispatch preflight — armed paths / identity / shell-era checklist.
    from .factory_dispatch_preflight import run_factory_dispatch_preflight

    for entry in entries:
        params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
        pf_job = {
            **params,
            "project_id": project_id,
            "slice_id": params.get("slice_id") or slice_id,
        }
        pre = run_factory_dispatch_preflight(
            vault_root,
            job=pf_job,
            project_id=project_id,
            game_repo_rel=str(params.get("repo_path") or params.get("game_repo_rel") or ""),
            zone_write=[str(z) for z in (params.get("zone_write") or []) if z],
            checklist_ids=[str(x) for x in (params.get("checklist_ids") or []) if x],
        )
        if not pre.ok:
            return {
                "ok": False,
                "orchestrator": result,
                "entries": [],
                "detail": "dispatch_preflight_failed",
                "dispatch_preflight": pre.to_dict(),
                "project_id": project_id,
                "slice_id": slice_id,
                "wave": int(wave),
                "fail_closed": True,
            }

    return {
        "ok": True,
        "orchestrator": result,
        "entries": entries,
        "project_id": project_id,
        "slice_id": slice_id,
        "wave": int(wave),
        "vault_feed": vault_feed,
        "armed_packet_path": armed_rel,
        "armed_slice_note": armed_note,
    }


def append_factory_wave(
    vault_root: Path,
    lane: str,
    packet: dict[str, Any],
    *,
    run_id: str,
    wave: int,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Append IMPLEMENT_SLICE lines for CDP lane batch N.

    Legacy name: CDP used ``waves[]``. Prefer ``append_factory_lane_batch``.
    Release **wave** means alpha/beta/rc/ga — not this function.
    """
    prepared = _prepare_factory_dispatch(
        vault_root, lane, packet, run_id=run_id, wave=int(wave)
    )
    if not prepared.get("ok"):
        return {**prepared, "appended": 0}

    entries = prepared.get("entries") or []
    project_id = str(prepared.get("project_id") or "")
    slice_id = str(prepared.get("slice_id") or "")

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "would_append": len(entries),
            "wave": int(wave),
            "slice_id": slice_id,
            "entries_preview": entries,
            "orchestrator": prepared.get("orchestrator"),
        }

    if not entries:
        return {
            "ok": True,
            "appended": 0,
            "skipped": True,
            "reason": "no_new_factory_jobs_for_wave",
            "wave": int(wave),
            "slice_id": slice_id,
            "orchestrator": prepared.get("orchestrator"),
        }

    append_raw_queue_entries(
        vault_root,
        lane,
        entries,
        source=f"factory_pq_wave_{int(wave)}",
    )
    update_implementation_cell(
        vault_root,
        project_id,
        {"phase": "lanes_running", "current_wave": int(wave), "pm_review_enqueued": False},
    )
    return {
        "ok": True,
        "appended": len(entries),
        "wave": int(wave),
        "lane_batch": int(wave),
        "slice_id": slice_id,
        "orchestrator": prepared.get("orchestrator"),
    }


def append_factory_lane_batch(
    vault_root: Path,
    lane: str,
    packet: dict[str, Any],
    *,
    run_id: str,
    batch: int,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Append IMPLEMENT_SLICE lines for CDP lane_batch N (preferred name).

    CDP schema still accepts ``waves[]`` during transition; prefer ``lane_batches[]``.
    """
    out = append_factory_wave(
        vault_root,
        lane,
        packet,
        run_id=run_id,
        wave=int(batch),
        dry_run=dry_run,
    )
    if isinstance(out, dict):
        out = {**out, "lane_batch": int(batch), "wave": int(batch)}
    return out


def stage_factory_dispatch_to_pq(
    vault_root: Path,
    lane: str,
    packet: dict[str, Any],
    *,
    run_id: str,
    dry_run: bool = False,
    wave: int = 1,
) -> dict[str, Any]:
    """Run factory orchestrator and append lane jobs to PQ when implementation track is active."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    wave = int(wave)

    prepared = _prepare_factory_dispatch(
        vault_root, lane, packet, run_id=run_id, wave=wave
    )
    if not prepared.get("ok"):
        return {**prepared, "appended": 0}

    entries = prepared.get("entries") or []
    project_id = str(prepared.get("project_id") or "")
    slice_id = str(prepared.get("slice_id") or "")
    vault_feed = bool(prepared.get("vault_feed"))

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "orchestrator": prepared.get("orchestrator"),
            "would_append": len(entries),
            "wave": wave,
            "entries_preview": entries,
        }

    if not entries:
        return {
            "ok": True,
            "orchestrator": prepared.get("orchestrator"),
            "appended": 0,
            "skipped": True,
            "reason": "no_new_factory_jobs",
            "wave": wave,
        }

    append_raw_queue_entries(
        vault_root,
        lane,
        entries,
        source="factory_pq_stage",
    )

    from ..user_story.implementation_artifact_ledger import record_implementation_artifact

    cdp_path = str(prepared.get("slice_id") or "")
    if cdp_path:
        try:
            from .slice_producer_harness import technical_slice_dir

            rel = str(technical_slice_dir(vault_root, cdp_path) / "cell-dispatch-plan.yaml")
            if (vault_root / rel).is_file():
                record_implementation_artifact(
                    vault_root,
                    project_id,
                    artifact_path=rel,
                    event_type="cdp_wave_dispatch",
                    slice_id=slice_id,
                    wave=wave,
                )
        except (OSError, ValueError, TypeError):
            pass

    update_implementation_cell(
        vault_root,
        project_id,
        {"phase": "lanes_running", "current_wave": wave},
    )
    if vault_feed:
        pf = load_product_factory(vault_root, project_id)
        completed = list(pf.get("completed_phases") or [])
        if FACTORY_STAGED not in completed:
            completed.append(FACTORY_STAGED)
            save_product_factory(vault_root, project_id, {**pf, "completed_phases": completed})

    return {
        "ok": True,
        "orchestrator": prepared.get("orchestrator"),
        "appended": len(entries),
        "slice_id": slice_id,
        "wave": wave,
        "dispatch_path": (prepared.get("orchestrator") or {}).get("dispatch_path"),
    }


def append_factory_rework(
    vault_root: Path,
    lane: str,
    packet: dict[str, Any],
    *,
    run_id: str,
    slice_id: str,
    lane_id: str,
    jobs: list[dict[str, Any]],
    rework_iteration: int,
) -> dict[str, Any]:
    """Re-queue one lane after PM rework verdict."""
    from .slice_advance import clear_lane_completion

    vault_root = vault_root.resolve()
    producer_receipt = load_producer_receipt(vault_root, slice_id)
    if not producer_receipt:
        return {"ok": False, "error": "producer_receipt_missing"}
    clear_lane_completion(vault_root, slice_id=slice_id, lane_id=lane_id)
    filtered = [j for j in jobs if str(j.get("lane_id") or "") == lane_id]
    entries = factory_lane_entries_from_dispatch(
        vault_root,
        lane=lane,
        packet=packet,
        run_id=run_id,
        jobs=filtered or jobs,
        slice_id=slice_id,
        wave=int((load_product_factory(vault_root, str(packet.get("project_id") or "")).get("implementation_cell") or {}).get("current_wave") or 1),
        producer_receipt=producer_receipt,
        rework_iteration=rework_iteration,
    )
    if not entries:
        return {"ok": True, "appended": 0, "skipped": True}
    append_raw_queue_entries(
        vault_root,
        lane,
        entries,
        source="factory_pq_stage_rework",
    )
    project_id = str(packet.get("project_id") or "genesis-mythos-master")
    update_implementation_cell(vault_root, project_id, {"phase": "lanes_running"})
    return {"ok": True, "appended": len(entries), "lane_id": lane_id, "rework_iteration": rework_iteration}
