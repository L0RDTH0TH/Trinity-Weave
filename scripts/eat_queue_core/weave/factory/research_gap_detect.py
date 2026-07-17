"""Scan manifest for TBD rows and missing research receipts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .stack_domain_registry import load_stack_domain_registry
from .tech_stack_manifest import ROW_KINDS_SKELETON, load_manifest


@dataclass(frozen=True)
class GapFinding:
    gap_id: str
    manifest_row_id: str
    stack_domain_id: str | None
    operator_summary: str
    confidence: str
    research_domain_id: str | None


def detect_gaps(vault_root: Path) -> list[GapFinding]:
    manifest = load_manifest(vault_root)
    registry = load_stack_domain_registry(vault_root)
    findings: list[GapFinding] = []

    for row in manifest.baseline_required_rows():
        if row.id == "engine-godot-463-dotnet":
            continue
        gap_id = str(row.raw.get("gap_id") or f"gap-{row.id}")
        domain_id = row.stack_domain_id
        research_domain = row.raw.get("research_domain_id")

        if row.row_kind in ROW_KINDS_SKELETON or not row.operational_confirmed:
            domain = next((d for d in registry.domains if d.id == domain_id), None)
            question = domain.raw.get("operator_question", "") if domain else ""
            findings.append(
                GapFinding(
                    gap_id=gap_id,
                    manifest_row_id=row.id,
                    stack_domain_id=domain_id,
                    operator_summary=(
                        f"Fresh search required for '{row.id}' ({domain_id}). "
                        f"POC museum is not canonical. {question}"
                    ).strip(),
                    confidence="low",
                    research_domain_id=str(research_domain) if research_domain else None,
                )
            )
            continue

        if row.interop_required and not row.raw.get("interop_receipt_id"):
            findings.append(
                GapFinding(
                    gap_id=f"{gap_id}-interop",
                    manifest_row_id=row.id,
                    stack_domain_id=domain_id,
                    operator_summary=f"Row '{row.id}' is operational but missing interop_receipt_id.",
                    confidence="medium",
                    research_domain_id=str(research_domain) if research_domain else None,
                )
            )

    return findings


def findings_to_gap_notes(findings: list[GapFinding]) -> list[dict[str, Any]]:
    return [
        {
            "gap_id": f.gap_id,
            "manifest_row_id": f.manifest_row_id,
            "stack_domain_id": f.stack_domain_id,
            "operator_summary": f.operator_summary,
            "confidence": f.confidence,
            "research_domain_id": f.research_domain_id,
            "vetting_policy": "fresh_candidate_search",
            "poc_canonical": False,
        }
        for f in findings
    ]
