"""Post-agent handlers for SLICE_PRODUCER_COMPOSE / REVIEW queue modes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..factory.factory_pq_stage import append_factory_wave
from ..factory.implementation_cell_tail import (
    handle_pm_rework,
    run_implementation_cell_post_pm_tail,
)
from ..factory.slice_producer_harness import (
    load_producer_receipt,
    run_slice_producer_compose,
    run_slice_producer_review,
    validate_producer_receipt,
    validate_producer_review,
    technical_slice_dir,
)
from ...goal_authority_io import load_goal_authority
from ..persona_handoff import build_pm_persona_envelope, load_pillar_packet_half_a_provenance
from .product_factory_state import load_product_factory, update_implementation_cell

SLICE_PRODUCER_MODES = frozenset({"SLICE_PRODUCER_COMPOSE", "SLICE_PRODUCER_REVIEW"})


def _normalize_mode(mode: str) -> str:
    return str(mode or "").strip().upper().replace(" ", "_").replace("-", "_")


def _project_id(entry: dict[str, Any]) -> str:
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    return str(entry.get("project_id") or params.get("project_id") or "godot-genesis-mythos-master")


def _queue_lane(entry: dict[str, Any]) -> str:
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    return str(entry.get("queue_lane") or params.get("queue_lane") or "godot").strip().lower()


def _load_review_doc(vault_root: Path, slice_id: str) -> dict[str, Any] | None:
    path = technical_slice_dir(vault_root, slice_id) / "producer-review.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def _handle_compose(
    vault_root: Path,
    entry: dict[str, Any],
    *,
    harness_fallback: bool,
) -> dict[str, Any]:
    eid = str(entry.get("id") or "")
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    project_id = _project_id(entry)
    run_id = str(params.get("product_factory_run_id") or "")
    slice_id = str(params.get("slice_id") or "")
    pf = load_product_factory(vault_root, project_id)
    active_slice = pf.get("active_slice") if isinstance(pf.get("active_slice"), dict) else None

    receipt = load_producer_receipt(vault_root, slice_id) if slice_id else None
    if receipt:
        ok, violations = validate_producer_receipt(vault_root, receipt)
        if ok:
            update_implementation_cell(
                vault_root,
                project_id,
                {
                    "phase": "composed",
                    "pm_compose_enqueued": False,
                    "factory_beat_id": slice_id,
                },
            )
            return {
                "ok": True,
                "id": eid,
                "mode": "SLICE_PRODUCER_COMPOSE",
                "detail": "producer_receipt_valid",
                "slice_id": slice_id,
            }
        return {
            "ok": False,
            "id": eid,
            "mode": "SLICE_PRODUCER_COMPOSE",
            "detail": "producer_receipt_invalid",
            "violations": violations,
        }

    if not harness_fallback:
        return {
            "ok": False,
            "id": eid,
            "mode": "SLICE_PRODUCER_COMPOSE",
            "detail": "awaiting_pm_agent_compose",
            "hint": "Dispatch Task(slice-producer) mode compose or set params.harness_fallback",
        }

    compose = run_slice_producer_compose(
        vault_root,
        project_id=project_id,
        run_id=run_id or str(pf.get("run_id") or "harness"),
        active_slice=active_slice,
    )
    if not compose.get("ok"):
        return {
            "ok": False,
            "id": eid,
            "mode": "SLICE_PRODUCER_COMPOSE",
            **compose,
        }
    update_implementation_cell(
        vault_root,
        project_id,
        {
            "phase": "composed",
            "pm_compose_enqueued": False,
            "factory_beat_id": str(compose.get("slice_id") or slice_id),
        },
    )
    return {
        "ok": True,
        "id": eid,
        "mode": "SLICE_PRODUCER_COMPOSE",
        "path": "harness_fallback",
        **compose,
    }


def _handle_review(
    vault_root: Path,
    entry: dict[str, Any],
    *,
    harness_fallback: bool,
    auto_stage_next_wave: bool = False,
) -> dict[str, Any]:
    eid = str(entry.get("id") or "")
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    project_id = _project_id(entry)
    lane = _queue_lane(entry)
    slice_id = str(params.get("slice_id") or "")
    wave = int(params.get("wave") or 1)
    run_id = str(params.get("product_factory_run_id") or "")

    review = _load_review_doc(vault_root, slice_id)
    if review is None and harness_fallback:
        review = run_slice_producer_review(
            vault_root,
            project_id=project_id,
            slice_id=slice_id,
            queue_lane=lane,
            current_wave=wave,
        )
    if review is None:
        return {
            "ok": False,
            "id": eid,
            "mode": "SLICE_PRODUCER_REVIEW",
            "detail": "awaiting_pm_agent_review",
        }

    struct_ok, struct_violations = validate_producer_review(vault_root, review)
    if not struct_ok:
        return {
            "ok": False,
            "id": eid,
            "mode": "SLICE_PRODUCER_REVIEW",
            "detail": "pm_review_persona_invalid",
            "violations": struct_violations,
        }

    if not review.get("ok"):
        verdict = str(review.get("verdict") or "rework")
        rework: dict[str, Any] | None = None
        if verdict == "rework":
            rework = handle_pm_rework(
                vault_root,
                project_id=project_id,
                slice_id=slice_id,
                queue_lane=lane,
                run_id=run_id,
                review=review,
            )
        else:
            update_implementation_cell(
                vault_root,
                project_id,
                {"phase": "rework", "pm_review_status": verdict},
            )
        return {
            "ok": False,
            "id": eid,
            "mode": "SLICE_PRODUCER_REVIEW",
            "rework": rework,
            **review,
        }

    if review.get("more_waves"):
        if auto_stage_next_wave:
            next_wave = wave + 1
            packet = load_goal_authority(vault_root, lane, require_confirmed=False) or {
                "project_id": project_id,
                "planner_hints": {"feed_authority": "vault_roadmap"},
            }
            staged = append_factory_wave(
                vault_root,
                lane,
                packet,
                run_id=run_id or f"wave-{next_wave}",
                wave=next_wave,
                dry_run=False,
            )
            update_implementation_cell(
                vault_root,
                project_id,
                {
                    "phase": "lanes_running",
                    "current_wave": next_wave,
                    "pm_review_enqueued": False,
                    "pm_review_status": "idle",
                },
            )
            return {
                "ok": True,
                "id": eid,
                "mode": "SLICE_PRODUCER_REVIEW",
                "detail": "pm_review_pass_more_waves",
                "wave_staged": staged,
                **review,
            }
        update_implementation_cell(
            vault_root,
            project_id,
            {
                "pm_review_enqueued": False,
                "pm_review_status": "idle",
                "phase": "lanes_running",
            },
        )
        return {
            "ok": True,
            "id": eid,
            "mode": "SLICE_PRODUCER_REVIEW",
            "detail": "pm_review_pass_await_next_wave",
            **review,
        }

    tail = run_implementation_cell_post_pm_tail(
        vault_root,
        project_id=project_id,
        slice_id=slice_id,
        queue_lane=lane,
        product_factory_run_id=run_id,
        trigger_entry_id=eid,
    )

    return {
        "ok": True,
        "id": eid,
        "mode": "SLICE_PRODUCER_REVIEW",
        "detail": "pm_review_pass",
        "post_pm_tail": tail,
        **review,
    }


def handle_slice_producer_entry(
    vault_root: Path,
    entry: dict[str, Any],
    *,
    harness_fallback: bool = False,
    auto_stage_next_wave: bool = False,
) -> dict[str, Any]:
    """Validate PM agent artifacts after compose/review (harness layer1 path)."""
    vault_root = vault_root.resolve()
    mode = _normalize_mode(str(entry.get("mode") or ""))
    if mode not in SLICE_PRODUCER_MODES:
        return {"ok": False, "error": "unknown_slice_producer_mode", "mode": mode}

    if mode == "SLICE_PRODUCER_COMPOSE":
        return _handle_compose(vault_root, entry, harness_fallback=harness_fallback)
    return _handle_review(
        vault_root,
        entry,
        harness_fallback=harness_fallback,
        auto_stage_next_wave=auto_stage_next_wave,
    )


def build_slice_producer_handoff(
    entry: dict[str, Any], vault_root: Path | None = None
) -> dict[str, Any]:
    """Structured hand-off for Task(slice-producer) from a queue line."""
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    mode = _normalize_mode(str(entry.get("mode") or ""))
    agent_mode = str(params.get("agent_mode") or ("compose" if "COMPOSE" in mode else "review"))
    project_id = _project_id(entry)
    half_a_prov = params.get("half_a_provenance")
    if not isinstance(half_a_prov, dict):
        packet_path = str(params.get("pillar_packet_path") or "")
        if packet_path and vault_root is not None:
            half_a_prov = load_pillar_packet_half_a_provenance(vault_root, packet_path)
    persona_handoff = params.get("persona_handoff")
    if not isinstance(persona_handoff, dict):
        persona_handoff = build_pm_persona_envelope(
            agent_mode=agent_mode,
            half_a_provenance=half_a_prov if isinstance(half_a_prov, dict) else None,
        )
    return {
        "subagent_type": "slice-producer",
        "agent_mode": agent_mode,
        "project_id": project_id,
        "queue_lane": _queue_lane(entry),
        "slice_id": params.get("slice_id"),
        "producer_run_id": params.get("producer_run_id"),
        "pillar_packet_path": params.get("pillar_packet_path"),
        "product_factory_run_id": params.get("product_factory_run_id"),
        "wave": params.get("wave", 1),
        "persona_handoff": persona_handoff,
        "half_a_provenance": half_a_prov,
        "return_contract": {
            "compose": ["ok", "sib_path", "cdp_path", "mission_paths", "violations", "persona_attestation"],
            "review": ["ok", "verdict", "current_wave", "more_waves", "violations", "persona_drift_findings"],
        },
    }
