"""Emit RESEARCH-AGENT queue lines for baseline stack domains (external-primary)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ...research_enqueue import (
    DEPRECATED_SIDE_QUEUE,
    default_research_lane,
    enqueue_research_batch,
)
from .stack_domain_registry import load_stack_domain_registry
from .tech_stack_manifest import load_manifest

# Deprecated R-phase: do not write this path; use lane PQ via enqueue_research_batch.
DEFAULT_QUEUE_OUT = DEPRECATED_SIDE_QUEUE

_EXTERNAL_QUERY_TEMPLATES: dict[str, list[str]] = {
    "world_gen_pipeline": [
        "Godot 4.6 C# procedural world generation pipeline stages open source 2025 2026",
        "modular world gen DAG game engine plugin alternatives",
    ],
    "procedural_maps": [
        "Godot 4 procedural 2D map generation C# library addon",
        "fantasy map generator open source API export heightmap JSON Godot",
    ],
    "procedural_terrain": [
        "Godot 4.6 Terrain3D alternatives C# procedural terrain streaming",
        "heightmap to 3D terrain Godot 4 open source MIT",
    ],
    "character_creation": [
        "Godot 4 character creation system RPG C# open source",
        "VTT character builder Godot addon data model",
    ],
    "rules_engine": [
        "Godot D&D rules engine plugin open source C#",
        "tabletop RPG rules as data plugin Godot 4 dice resolution",
    ],
    "simulation_tick": [
        "game simulation tick event bus C# Godot 4 decoupled from rendering",
        "ECS vs event bus Godot 4.6 C# living world simulation",
    ],
    "intent_lore_loop": [
        "procedural narrative intent system game lore to mechanics hooks",
        "player intent parser RPG world state Godot",
    ],
    "perspective_camera": [
        "Godot 4.6 C# camera rig Cinemachine alternative Phantom Camera comparison",
        "free look orthographic camera Godot 4 addon MIT",
    ],
    "regional_modules": [
        "modular regional world chunks game engine plugin open world",
        "Godot 4 streaming regions module pattern C#",
    ],
    "ci_tooling": [
        "GdUnit4Net Godot 4.6 headless CI ubuntu C# 2025",
        "Godot 4 mono CI github actions integration test",
    ],
}


@dataclass(frozen=True)
class ResearchEnqueueResult:
    entries: tuple[dict[str, Any], ...]
    output_path: Path | None
    lane: str | None = None


def _external_queries(domain_id: str, title: str) -> list[str]:
    base = _EXTERNAL_QUERY_TEMPLATES.get(domain_id, [])
    if base:
        return base[:3]
    return [
        f"Godot 4.6.3 C# {title} open source library addon 2025 2026",
        f"{title} game development alternatives MIT license",
    ]


def build_research_queue_entries(vault_root: Path) -> list[dict[str, Any]]:
    manifest = load_manifest(vault_root)
    registry = load_stack_domain_registry(vault_root)
    entries: list[dict[str, Any]] = []
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for domain in registry.domains:
        if not domain.baseline_required:
            continue
        row = manifest.row_by_stack_domain(domain.id)
        if row is None:
            continue
        if row.operational_confirmed:
            continue
        row_id = row.id
        gap_id = row.raw.get("gap_id") or f"gap-{row_id}"
        interop = list(domain.interop_pairs)
        queries = _external_queries(domain.id, domain.title)

        entries.append(
            {
                "id": f"stack-research-{domain.id}-{ts}-{uuid.uuid4().hex[:6]}",
                "mode": "RESEARCH_AGENT",
                "project_id": manifest.project_id,
                "params": {
                    "research_profile": "stack_vetting",
                    "stack_vetting": True,
                    "research_primary": "external",
                    "vault_context_mode": "museum_anti_patterns_only",
                    "research_domain_id": domain.research_domain_id,
                    "manifest_row_id": row_id,
                    "stack_domain_id": domain.id,
                    "gap_id": gap_id,
                    "vetting_policy": "fresh_candidate_search",
                    "poc_canonical": False,
                    "interop_pairs": interop,
                    "operator_question": domain.raw.get("operator_question", ""),
                    "research_queries": queries,
                    "research_tools": ["web", "firecrawl"],
                    "research_focus": "spike_proposal",
                    "research_strategy": "deep",
                    "store_raw": True,
                    "output_path": f"Ingest/Agent-Research/Stack-Gaps/{gap_id}.md",
                    "raw_output_dir": "Ingest/Agent-Research/Raw/Stack-Vetting",
                    "require_alternatives": True,
                    "require_interop_analysis": True,
                    "linked_phase": f"Factory-DRB/Stack-Domain-Registry-v1#{domain.id}",
                },
                "prompt": (
                    f"STACK VETTING — external-primary research for: {domain.title}. "
                    f"Do NOT vault-first inventory or default to POC museum choices. "
                    f"Search externally for Godot 4.6.3 .NET candidates; produce ≥2 alternatives, "
                    f"interop analysis for [{', '.join(interop) or 'n/a'}], write synthesis to "
                    f"Ingest/Agent-Research/Stack-Gaps/{gap_id}.md with external Sources."
                ),
            }
        )
    return entries


def enqueue_stack_research(
    vault_root: Path,
    *,
    dry_run: bool = True,
    lane: str | None = None,
    output_rel: str | None = None,
    overwrite: bool = True,
) -> ResearchEnqueueResult:
    """Enqueue stack vetting research via queue_bus (R-phase). output_rel ignored (deprecated)."""
    _ = output_rel
    _ = overwrite
    from .gap_research_router import build_routed_research_entries

    entries = build_routed_research_entries(vault_root)
    if dry_run or not entries:
        return ResearchEnqueueResult(tuple(entries), None, None)

    manifest = load_manifest(vault_root)
    use_lane = lane or default_research_lane(vault_root, manifest.project_id)
    out = enqueue_research_batch(
        vault_root,
        use_lane,
        list(entries),
        source="stack_vetting",
    )
    pq_rel = out.get("path")
    out_path = (vault_root / pq_rel) if pq_rel else None
    return ResearchEnqueueResult(tuple(entries), out_path, use_lane)
