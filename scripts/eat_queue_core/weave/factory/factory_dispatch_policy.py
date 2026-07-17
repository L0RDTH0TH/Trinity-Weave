"""Factory dispatch policy — separate overnight dispatch from slice advance / ship gates."""

from __future__ import annotations

from typing import Any


def allow_dispatch_with_red_gates(active_slice: dict[str, Any] | None) -> bool:
    """Orchestrator may stage PQ while Tier B/C gates are red when slice opts in."""
    if not active_slice:
        return False
    return active_slice.get("allow_implement_with_gates_red") is True


def slice_advance_requires_exit_gates() -> bool:
    """Slice yaml may only advance when exit_gates pass (factory_lane_runner enforces)."""
    return True


def overnight_blocks_on_playtest_ingest() -> bool:
    """F6 playtest ingest is operator-session only — never blocks headless eat."""
    return False


def dispatch_policy_payload(active_slice: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "allow_implement_with_gates_red": allow_dispatch_with_red_gates(active_slice),
        "slice_advance_requires_exit_gates": slice_advance_requires_exit_gates(),
        "overnight_blocks_on_playtest_ingest": overnight_blocks_on_playtest_ingest(),
        "playtest_ingest_gate_mode": "operator_session_non_blocking",
    }
