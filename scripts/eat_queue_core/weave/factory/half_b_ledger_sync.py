"""Half B honest ledger sync — derive playtest park flags from live gates."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .implementation_handoff_ready import implementation_handoff_ready
from ..user_story.playtest_manual_gate import playtest_gate_surface_ready
from ..user_story.product_factory_state import (
    load_product_factory,
    normalize_completed_phases,
    save_product_factory,
)

_HALF_B_BEATS = frozenset({"weld_beat_prep", "playtest_brief"})


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def honest_half_b_ledger_sync(vault_root: Path, project_id: str) -> dict[str, Any]:
    """
    Derive Half B completed_phases and playtest park flags from live gates.

    When implementation handoff regresses, reopen weld beats and clear premature park.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return {"ok": False, "reason": "no_project_id", "steps": []}

    pf = load_product_factory(vault_root, pid)
    completed = normalize_completed_phases(list(pf.get("completed_phases") or []))
    steps: list[dict[str, Any]] = []
    updates: dict[str, Any] = {}

    handoff_ok, handoff_reason = implementation_handoff_ready(vault_root, pid)

    if not handoff_ok:
        stripped = [p for p in completed if p in _HALF_B_BEATS]
        if stripped:
            completed = [p for p in completed if p not in _HALF_B_BEATS]
            steps.append(
                {"step": "honest_half_b_reopen", "stripped": stripped, "reason": handoff_reason}
            )
        if pf.get("playtest_exit_eligible") is True:
            updates["playtest_exit_eligible"] = False
            updates["playtest_exit_session_id"] = ""
            updates["blocked_at"] = "machine:implementation_handoff"
            steps.append(
                {"step": "honest_half_b_clear_playtest_park", "reason": handoff_reason}
            )
    elif pf.get("playtest_exit_eligible") is True:
        from .weld_beat_ready import playtest_attestation_complete

        surface_ok, surface_reason = playtest_gate_surface_ready(vault_root, pid)
        att_ok, _ = playtest_attestation_complete(vault_root, pid)
        if not surface_ok and not att_ok:
            stripped = [p for p in completed if p in _HALF_B_BEATS]
            if stripped:
                completed = [p for p in completed if p not in _HALF_B_BEATS]
                steps.append(
                    {
                        "step": "honest_half_b_reopen",
                        "stripped": stripped,
                        "reason": surface_reason,
                    }
                )
            updates["playtest_exit_eligible"] = False
            updates["playtest_exit_session_id"] = ""
            updates["blocked_at"] = "machine:weld_beat_prep"
            steps.append(
                {
                    "step": "honest_half_b_clear_playtest_without_surface",
                    "reason": surface_reason,
                }
            )

    if updates or any(s.get("step") == "honest_half_b_reopen" for s in steps):
        save_product_factory(
            vault_root,
            pid,
            {**pf, **updates, "completed_phases": completed, "updated_at": _utc_iso()},
        )

    return {"ok": True, "steps": steps, "updates": updates}
