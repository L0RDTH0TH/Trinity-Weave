"""Wire gap_autonomy_router into detect + research enqueue."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .factory_research_enqueue import ResearchEnqueueResult, build_research_queue_entries
from .gap_autonomy_router import GapAction, route_gap
from .research_gap_detect import detect_gaps, findings_to_gap_notes
from .tech_stack_manifest import load_manifest


def enrich_gap_note(note: dict[str, Any], vault_root: Path) -> dict[str, Any]:
    manifest = load_manifest(vault_root)
    row = manifest.row_by_id(str(note.get("manifest_row_id") or ""))
    raw = row.raw if row else {}
    route = route_gap(
        gap_id=str(note.get("gap_id") or "unknown"),
        manifest_row_status=str(raw.get("status") or raw.get("row_kind") or ""),
        manifest_category=str(raw.get("category") or raw.get("stack_domain_id") or ""),
        has_official_docs=bool(note.get("has_official_docs")),
        has_institute_receipt=bool(note.get("has_institute_receipt")),
        prior_green_integrate=bool(row.operational_confirmed if row else False),
        credible_source_count=int(note.get("credible_source_count", 0)),
        license_clear=bool(note.get("license_clear")),
        conflicting_sources=bool(note.get("conflicting_sources")),
    )
    out = dict(note)
    out["gap_route"] = {
        "confidence": route.confidence.value,
        "action": route.action.value,
        "reason": route.reason,
    }
    return out


def detect_and_route_gaps(vault_root: Path) -> list[dict[str, Any]]:
    findings = detect_gaps(vault_root)
    notes = findings_to_gap_notes(findings)
    return [enrich_gap_note(n, vault_root) for n in notes]


def build_routed_research_entries(vault_root: Path) -> list[dict[str, Any]]:
    """Research queue entries with gap_route metadata; skip BLOCK_AUTO rows."""
    base = build_research_queue_entries(vault_root)
    manifest = load_manifest(vault_root)
    routed: list[dict[str, Any]] = []

    for entry in base:
        params = dict(entry.get("params") or {})
        row_id = str(params.get("manifest_row_id") or "")
        row = manifest.row_by_id(row_id)
        raw = row.raw if row else {}
        route = route_gap(
            gap_id=str(params.get("gap_id") or f"gap-{row_id}"),
            manifest_row_status=str(raw.get("status") or raw.get("row_kind") or ""),
            manifest_category=str(params.get("stack_domain_id") or ""),
            prior_green_integrate=bool(row.operational_confirmed if row else False),
        )
        if route.action == GapAction.BLOCK_AUTO:
            continue
        params["gap_route"] = {
            "confidence": route.confidence.value,
            "action": route.action.value,
            "reason": route.reason,
        }
        entry = {**entry, "params": params}
        routed.append(entry)
    return routed


def enqueue_routed_stack_research(
    vault_root: Path,
    *,
    dry_run: bool = True,
    lane: str | None = None,
    output_rel: str | None = None,
    overwrite: bool = True,
) -> ResearchEnqueueResult:
    """Delegate to queue_bus batch enqueue (R-phase). output_rel deprecated."""
    from .factory_research_enqueue import enqueue_stack_research

    _ = output_rel
    _ = overwrite
    return enqueue_stack_research(vault_root, dry_run=dry_run, lane=lane)
