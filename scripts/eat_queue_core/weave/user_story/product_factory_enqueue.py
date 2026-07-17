"""Enqueue product factory agent steps (RESUME_ROADMAP) with ux_context + tech_level."""

from __future__ import annotations

from typing import Any

from pathlib import Path

from ...lane_queue_io import append_lane_queue_entry
from ...models import QueueEntry
from .product_factory_ux_context import (
    is_product_factory_execution_resume,
    is_product_factory_roadmap_resume,
    merge_ux_context_into_params,
    validate_ux_context,
)
from .product_factory_state import load_product_factory, save_product_factory
from .research_context import build_research_context, format_research_context_block
from .tech_level_resolver import resolve_tech_level_params
from ..persona_handoff import build_validator_persona_supplement, merge_persona_into_params
from .done_when_eval import loop2_exit_honestly_eligible
from .factory_harness_rails import (
    implement_slice_handoff_blocked,
    resume_roadmap_conceptual_factory_blocked,
    resume_roadmap_execution_implementation_blocked,
)
from .l5_scope_guard import resume_roadmap_l5_blocked, resume_roadmap_loop2_blocked


def enrich_queue_entry(entry: QueueEntry, vault_root: Path) -> QueueEntry:
    """Layer 1 pre-dispatch: merge ux_context, research_context, tech_level."""
    vault_root = vault_root.resolve()
    params = dict(entry.params) if isinstance(entry.params, dict) else {}
    mode = (entry.mode or "").upper().replace("-", "_")
    if mode != "RESUME_ROADMAP":
        return entry
    if not is_product_factory_roadmap_resume(params):
        return entry

    project_id = str(
        entry.project_id or params.get("project_id") or "godot-genesis-mythos-master"
    )
    track = str(params.get("roadmap_track") or "execution").lower()
    merged = dict(params)

    if is_product_factory_execution_resume(merged):
        merged = merge_ux_context_into_params(vault_root, project_id=project_id, params=merged)
        val = validate_ux_context(merged)
        if not val.ok:
            merged["product_factory_ux_context_error"] = list(val.violations)

    ctx = build_research_context(vault_root, project_id=project_id)
    merged["research_context"] = ctx
    block = format_research_context_block(ctx)
    if block:
        guidance = str(merged.get("user_guidance") or "")
        if block not in guidance:
            merged["user_guidance"] = (guidance.rstrip() + "\n\n" + block).strip()

    merged = resolve_tech_level_params(merged, vault_root=vault_root, track=track)
    if track == "conceptual" and str(merged.get("action") or "deepen").lower() == "deepen":
        from .conceptual_dispatch_authority import (
            build_conceptual_dispatch_verdict,
            stamp_harness_gate_params,
        )

        verdict = build_conceptual_dispatch_verdict(vault_root, project_id)
        if verdict.deepen_required or not merged.get("harness_gate_authority"):
            merged = stamp_harness_gate_params(merged, verdict)
    merged = merge_persona_into_params(merged)

    l5_blocked, l5_reason = resume_roadmap_l5_blocked(mode, merged)
    if l5_blocked:
        merged["l5_scope_route_blocked"] = True
        merged["l5_scope_block_reason"] = l5_reason
        merged["layer1_task_dispatch_capability"] = False
    else:
        conceptual_blocked, conceptual_reason = resume_roadmap_conceptual_factory_blocked(
            vault_root, project_id, mode, merged
        )
        if conceptual_blocked:
            merged["conceptual_harness_rail_blocked"] = True
            merged["l5_scope_block_reason"] = conceptual_reason
            merged["layer1_task_dispatch_capability"] = False
        elif loop2_exit_honestly_eligible(vault_root, project_id):
            loop2_blocked, loop2_reason = resume_roadmap_loop2_blocked(
                mode, merged, loop2_exit_eligible=True
            )
            if loop2_blocked:
                merged["loop2_exit_route_blocked"] = True
                merged["l5_scope_block_reason"] = loop2_reason
                merged["layer1_task_dispatch_capability"] = False
        else:
            impl_blocked, impl_reason = resume_roadmap_execution_implementation_blocked(
                vault_root, project_id, mode, merged
            )
            if impl_blocked:
                merged["implementation_harness_rail_blocked"] = True
                merged["l5_scope_block_reason"] = impl_reason
                merged["layer1_task_dispatch_capability"] = False

    norm_mode = mode.upper().replace("-", "_")
    if norm_mode == "IMPLEMENT_SLICE" or str(merged.get("action") or "").lower() == "factory_lane":
        handoff_blocked, handoff_reason = implement_slice_handoff_blocked(
            vault_root, project_id, norm_mode, merged
        )
        if handoff_blocked:
            merged["implementation_handoff_blocked"] = True
            merged["l5_scope_block_reason"] = handoff_reason
            merged["layer1_task_dispatch_capability"] = False

    validator_sup = build_validator_persona_supplement(merged)
    if validator_sup:
        merged["validator_persona_supplement"] = validator_sup
    return entry.model_copy(update={"params": merged, "project_id": project_id})


def enrich_loaded_entries(vault_root: Path, entries: list[QueueEntry]) -> list[QueueEntry]:
    return [enrich_queue_entry(e, vault_root) for e in entries]


def flush_pending_enqueues(
    vault_root: Path,
    *,
    project_id: str,
    pending: list[dict[str, Any]],
    lane: str = "godot",
    run_id: str,
) -> list[dict[str, Any]]:
    """Write pending_enqueues from conductor tick to lane PQ."""
    vault_root = vault_root.resolve()
    written: list[dict[str, Any]] = []
    ux = merge_ux_context_into_params(
        vault_root,
        project_id=project_id,
        params={"product_factory_run_id": run_id, "roadmap_track": "execution"},
    ).get("ux_context")
    pf = load_product_factory(vault_root, project_id)
    save_product_factory(
        vault_root,
        project_id,
        {**pf, "ux_context": ux, "run_id": run_id},
    )

    for item in pending:
        mode = str(item.get("mode") or "RESUME_ROADMAP")
        params = dict(item.get("params") or {})
        params.setdefault("project_id", project_id)
        params.setdefault("product_factory_run_id", run_id)
        track = str(params.get("roadmap_track") or "execution").lower()
        norm_mode = mode.upper().replace("-", "_")
        if norm_mode == "RESUME_ROADMAP":
            l5_blocked, l5_reason = resume_roadmap_l5_blocked(norm_mode, params)
            if l5_blocked:
                written.append({"ok": False, "mode": mode, "skipped": True, "reason": l5_reason})
                continue
            conceptual_blocked, conceptual_reason = resume_roadmap_conceptual_factory_blocked(
                vault_root, project_id, norm_mode, params
            )
            if conceptual_blocked:
                written.append(
                    {"ok": False, "mode": mode, "skipped": True, "reason": conceptual_reason}
                )
                continue
            if loop2_exit_honestly_eligible(vault_root, project_id):
                loop2_blocked, loop2_reason = resume_roadmap_loop2_blocked(
                    norm_mode, params, loop2_exit_eligible=True
                )
                if loop2_blocked:
                    written.append({"ok": False, "mode": mode, "skipped": True, "reason": loop2_reason})
                    continue
        if norm_mode == "RESUME_ROADMAP":
            if is_product_factory_execution_resume(params):
                params = merge_ux_context_into_params(vault_root, project_id=project_id, params=params)
            ctx = build_research_context(vault_root, project_id=project_id)
            params["research_context"] = ctx
            block = format_research_context_block(ctx)
            if block:
                guidance = str(params.get("user_guidance") or "")
                if block not in guidance:
                    params["user_guidance"] = (guidance.rstrip() + "\n\n" + block).strip()
            params = resolve_tech_level_params(params, vault_root=vault_root, track=track)
            params = merge_persona_into_params(params)
            val = validate_ux_context(params) if is_product_factory_execution_resume(params) else None
            if val and not val.ok:
                written.append({"ok": False, "mode": mode, "violations": list(val.violations)})
                continue
        fp = f"product-factory:{run_id}:{mode}:{params.get('action', '')}:{track}"
        out = append_lane_queue_entry(
            vault_root,
            lane=lane,
            mode=mode,
            params=params,
            source="product_factory_conductor",
            fingerprint=fp,
        )
        written.append(out)
    return written
