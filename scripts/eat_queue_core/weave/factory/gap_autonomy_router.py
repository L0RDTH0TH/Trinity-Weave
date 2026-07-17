"""Rules-based gap confidence routing (Gap-Autonomy-Policy-v1)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class GapAction(str, Enum):
    INTEGRATE_AND_INFORM = "integrate_and_inform"
    PROPOSE_INTEGRATE = "propose_integrate"
    OPERATOR_SELECT = "operator_select"
    BLOCK_AUTO = "block_auto"


@dataclass(frozen=True)
class GapRoute:
    gap_id: str
    confidence: Confidence
    action: GapAction
    reason: str


def route_gap(
    *,
    gap_id: str,
    manifest_row_status: str | None = None,
    manifest_category: str | None = None,
    has_official_docs: bool = False,
    has_institute_receipt: bool = False,
    prior_green_integrate: bool = False,
    credible_source_count: int = 0,
    license_clear: bool = False,
    conflicting_sources: bool = False,
) -> GapRoute:
    """Classify a gap note into confidence + next action."""

    locked = manifest_row_status == "locked"
    engine = manifest_category == "engine_runtime"

    if locked or engine:
        return GapRoute(
            gap_id=gap_id,
            confidence=Confidence.LOW if conflicting_sources else Confidence.MEDIUM,
            action=GapAction.BLOCK_AUTO,
            reason="locked row or engine_runtime — operator sign required",
        )

    if has_official_docs and has_institute_receipt and prior_green_integrate:
        return GapRoute(
            gap_id=gap_id,
            confidence=Confidence.HIGH,
            action=GapAction.INTEGRATE_AND_INFORM,
            reason="official docs + institute receipt + prior green integrate",
        )

    if credible_source_count >= 2 and license_clear and not conflicting_sources:
        return GapRoute(
            gap_id=gap_id,
            confidence=Confidence.MEDIUM,
            action=GapAction.PROPOSE_INTEGRATE,
            reason="two+ credible sources; license clear",
        )

    return GapRoute(
        gap_id=gap_id,
        confidence=Confidence.LOW,
        action=GapAction.OPERATOR_SELECT,
        reason="vendor unclear, license ambiguous, or conflicting sources",
    )


def route_from_gap_note(note: dict[str, Any]) -> GapRoute:
    return route_gap(
        gap_id=str(note.get("gap_id", "unknown")),
        manifest_row_status=note.get("manifest_row_status"),
        manifest_category=note.get("manifest_category"),
        has_official_docs=bool(note.get("has_official_docs")),
        has_institute_receipt=bool(note.get("has_institute_receipt")),
        prior_green_integrate=bool(note.get("prior_green_integrate")),
        credible_source_count=int(note.get("credible_source_count", 0)),
        license_clear=bool(note.get("license_clear")),
        conflicting_sources=bool(note.get("conflicting_sources")),
    )
