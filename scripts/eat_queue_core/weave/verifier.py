"""Phase 1 strict integrity verifier for operator surface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = (
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

REQUIRED_TOKENS = (
    "operator_surface: lane_board",
    "system_attention:",
    "| Tier | Lane | Health | Run | Summary | Depth | Norm | Est. drain | Last success |",
)


@dataclass(frozen=True)
class VerifierResult:
    ok: bool
    code: str
    detail: str


def verify_operator_surface_integrity(board_path: Path) -> VerifierResult:
    if not board_path.is_file():
        return VerifierResult(False, "board_missing", f"missing file: {board_path}")

    text = board_path.read_text(encoding="utf-8", errors="replace")
    for token in REQUIRED_TOKENS:
        if token not in text:
            return VerifierResult(False, "token_missing", f"missing token: {token}")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            return VerifierResult(False, "section_missing", f"missing section: {section}")

    return VerifierResult(True, "ok", "strict verifier passed")
