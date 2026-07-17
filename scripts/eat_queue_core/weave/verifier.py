"""Phase 1 strict integrity verifier for operator surface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..lane_board_integrity import is_v2_board, is_v3_weave_board

REQUIRED_SECTIONS_V1 = (
    "## At a glance",
    "## Lanes",
    "## Health history",
    "## Recent runs",
    "## Governance cadence",
    "## Predictive maintenance",
    "## Neuro-symbolic gate",
    "## L3 self-healing",
    "## L4 adaptive pilot",
    "## L5 autonomous lab (H2)",
    "## Audit trail",
)

REQUIRED_SECTIONS_V2 = (
    "## At a glance",
    "## Factory floor",
    "## Lanes by project",
    "## Health history",
    "## Recent runs",
    "## Audit trail",
)

REQUIRED_SECTIONS_V3 = (
    "## At a glance",
    "## Warehouses",
    "## Overnight",
    "## Health history",
    "## Audit",
)

REQUIRED_TOKENS_V1 = (
    "operator_surface: lane_board",
    "system_attention:",
    "| Tier | Lane | Health | Run | Summary | Depth | Norm | Est. drain | Last success |",
)

REQUIRED_TOKENS_V2 = (
    "operator_surface: lane_board",
    "system_attention:",
    "schema_version: 2",
)

REQUIRED_TOKENS_V3 = (
    "operator_surface: weave_status",
    "system_attention:",
    "weave_status:",
    "schema_version: 3",
)


@dataclass(frozen=True)
class VerifierResult:
    ok: bool
    code: str
    detail: str


REQUIRED_SECTIONS = REQUIRED_SECTIONS_V1
REQUIRED_TOKENS = REQUIRED_TOKENS_V1


def verify_operator_surface_integrity(board_path: Path) -> VerifierResult:
    if not board_path.is_file():
        return VerifierResult(False, "board_missing", f"missing file: {board_path}")

    text = board_path.read_text(encoding="utf-8", errors="replace")
    if is_v3_weave_board(text):
        tokens = REQUIRED_TOKENS_V3
        sections = REQUIRED_SECTIONS_V3
    elif is_v2_board(text):
        tokens = REQUIRED_TOKENS_V2
        sections = REQUIRED_SECTIONS_V2
    else:
        tokens = REQUIRED_TOKENS_V1
        sections = REQUIRED_SECTIONS_V1

    for token in tokens:
        if token not in text:
            return VerifierResult(False, "token_missing", f"missing token: {token}")

    for section in sections:
        if section not in text:
            return VerifierResult(False, "section_missing", f"missing section: {section}")

    return VerifierResult(True, "ok", "strict verifier passed")
