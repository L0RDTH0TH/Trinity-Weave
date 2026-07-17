"""Weld beat content gates — machine prep vs operator-attested depth bump."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .gate_precedence import PASS_TIERS, GateTier, evaluate_precedence
from .implementation_handoff_ready import implementation_handoff_ready
from .slice_advance import load_completion_tracker, slice_lanes_complete
from ..user_story.implementation_artifact_ledger import record_implementation_artifact
from ..user_story.playtest_manual_gate import (
    latest_playtest_brief,
    playtest_feedback_pending,
    playtest_gate_surface_ready,
)
from ..user_story.product_factory_state import load_product_factory, save_product_factory

PLAYTEST_PENDING_SIGN_OFF = "operator_playtest_pending_sign_off"
PLAYTEST_BLOCKED_DISPATCH = "blocked_pending_playtest"


def playtest_exit_eligible_for_project(vault_root: Path, project_id: str) -> bool:
    """Raw disk flag — use playtest_exit_honestly_eligible for routing/overnight exit."""
    pf = load_product_factory(vault_root, str(project_id or "").strip())
    return pf.get("playtest_exit_eligible") is True


def playtest_attestation_complete(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """Operator confirmed feedback rows — pass or fail recorded between sessions."""
    pending, pending_ids = playtest_feedback_pending(vault_root, project_id)
    if pending:
        detail = pending_ids[0] if pending_ids else "pending"
        return False, f"playtest_pending:{detail}"
    brief = latest_playtest_brief(vault_root, project_id)
    if brief is None:
        return False, "no_playtest_brief"
    return True, "playtest_attested"


def _tier_a_green(gate_summary: dict[str, Any]) -> tuple[bool, str]:
    if not gate_summary:
        return False, "no_gate_summary"
    pass_map: dict[str, bool] = {}
    for name, res in gate_summary.items():
        if isinstance(res, dict):
            pass_map[name] = bool(res.get("ok"))
        else:
            pass_map[name] = bool(getattr(res, "ok", res))
    verdict = evaluate_precedence(pass_map)
    tier_a_fail = [
        name
        for name, ok in pass_map.items()
        if not ok and PASS_TIERS.get(name) == GateTier.A
    ]
    if tier_a_fail:
        return False, f"tier_a_fail:{tier_a_fail[0]}"
    if not verdict.ok:
        return False, f"precedence:{verdict.detail}"
    return True, "tier_a_green"


def weld_beat_machine_ready(
    vault_root: Path,
    project_id: str,
    *,
    slice_id: str,
    required_lanes: list[str],
    gate_summary: dict[str, Any] | None = None,
    honesty_ok: bool = True,
) -> tuple[bool, str]:
    """
    Machine playtest surface ready — lanes + Tier A exit gates + brief path.

    Does not require operator attestation (that is weld_beat_ready for depth bump).
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    sid = str(slice_id or "").strip()
    if not pid or not sid:
        return False, "missing_project_or_slice"
    if not honesty_ok:
        return False, "honesty_gate_failed"
    if required_lanes and not slice_lanes_complete(
        vault_root, slice_id=sid, required_lanes=required_lanes
    ):
        return False, "lanes_incomplete"

    if gate_summary is not None:
        tier_ok, tier_reason = _tier_a_green(gate_summary)
        if not tier_ok:
            return False, tier_reason

    brief = latest_playtest_brief(vault_root, pid)
    if brief is None:
        return False, "no_playtest_brief"

    return True, "weld_beat_machine_ready"


def playtest_machine_ready(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """Machine playtest park honestly eligible — handoff + surface or attestation."""
    pid = str(project_id or "").strip()
    if not pid:
        return False, "no_project_id"

    handoff_ok, handoff_reason = implementation_handoff_ready(vault_root, pid)
    if not handoff_ok:
        return False, f"implementation_handoff:{handoff_reason}"

    pf = load_product_factory(vault_root, pid)
    if pf.get("playtest_exit_eligible") is not True:
        return False, "not_playtest_exit_eligible"

    blocked = str(pf.get("blocked_at") or "")
    if blocked != PLAYTEST_PENDING_SIGN_OFF:
        return False, "not_parked_at_playtest_gate"

    att_ok, att_reason = playtest_attestation_complete(vault_root, pid)
    if att_ok:
        return True, "playtest_attested"

    surface_ok, surface_reason = playtest_gate_surface_ready(vault_root, pid)
    if surface_ok:
        return True, "playtest_exit_eligible"

    return False, surface_reason or att_reason


def playtest_exit_honestly_eligible(vault_root: Path, project_id: str) -> bool:
    """Disk flag + live gate chain — safe for overnight exit and queue routing."""
    ok, _ = playtest_machine_ready(vault_root, project_id)
    return ok


def park_playtest_machine_ready(
    vault_root: Path,
    project_id: str,
    *,
    slice_id: str = "",
    session_run_id: str = "",
    gate_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Park Half B at playtest manual gate when handoff + machine surface are ready."""
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return {"ok": False, "reason": "no_project_id"}

    handoff_ok, handoff_reason = implementation_handoff_ready(vault_root, pid)
    if not handoff_ok:
        return {"ok": False, "reason": f"implementation_handoff:{handoff_reason}"}

    sid = str(slice_id or "").strip()
    if sid:
        machine_ok, machine_reason = weld_beat_machine_ready(
            vault_root,
            pid,
            slice_id=sid,
            required_lanes=[],
            gate_summary=gate_summary,
            honesty_ok=True,
        )
        if not machine_ok:
            return {"ok": False, "reason": machine_reason}
    else:
        surface_ok, surface_reason = playtest_gate_surface_ready(vault_root, pid)
        if not surface_ok:
            return {"ok": False, "reason": surface_reason}

    pf = load_product_factory(vault_root, pid)
    if pf.get("playtest_exit_eligible") is True and str(pf.get("blocked_at") or "") == PLAYTEST_PENDING_SIGN_OFF:
        return {"ok": True, "reason": "already_parked"}

    completed = list(pf.get("completed_phases") or [])
    for beat in ("weld_beat_prep", "playtest_brief"):
        if beat not in completed:
            completed.append(beat)

    updates: dict[str, Any] = {
        **pf,
        "playtest_exit_eligible": True,
        "blocked_at": PLAYTEST_PENDING_SIGN_OFF,
        "playtest_exit_session_id": session_run_id or pf.get("playtest_exit_session_id") or "",
        "playtest_exit_slice_id": slice_id or pf.get("playtest_exit_slice_id") or "",
        "completed_phases": completed,
        "factory_staged_dispatch": PLAYTEST_BLOCKED_DISPATCH,
    }
    if gate_summary:
        updates["playtest_exit_gate_summary"] = {
            k: (v if isinstance(v, dict) else {"ok": bool(getattr(v, "ok", v))})
            for k, v in gate_summary.items()
        }

    save_product_factory(vault_root, pid, updates)

    brief = latest_playtest_brief(vault_root, pid)
    if brief is not None:
        try:
            rel = str(brief.relative_to(vault_root))
            record_implementation_artifact(
                vault_root,
                pid,
                artifact_path=rel,
                event_type="playtest_exit_park",
                slice_id=slice_id,
            )
        except ValueError:
            pass

    return {"ok": True, "reason": "parked_playtest_machine_ready", "slice_id": slice_id}


def weld_beat_ready(
    vault_root: Path,
    project_id: str,
    *,
    slice_id: str = "",
    required_lanes: list[str] | None = None,
    gate_summary: dict[str, Any] | None = None,
    honesty_ok: bool = True,
) -> tuple[bool, str]:
    """
    Operator-attested weld beat — required before depth bump on next session.

    When playtest_exit_eligible is set, attestation must be complete.
    """
    pid = str(project_id or "").strip()
    lanes = list(required_lanes or [])

    if playtest_exit_eligible_for_project(vault_root, pid):
        att_ok, att_reason = playtest_attestation_complete(vault_root, pid)
        if not att_ok:
            return False, att_reason
        return True, "playtest_attested"

    handoff_ok, handoff_reason = implementation_handoff_ready(vault_root, pid)
    if not handoff_ok:
        return False, f"implementation_handoff:{handoff_reason}"

    machine_ok, machine_reason = weld_beat_machine_ready(
        vault_root,
        pid,
        slice_id=slice_id,
        required_lanes=lanes,
        gate_summary=gate_summary,
        honesty_ok=honesty_ok,
    )
    return machine_ok, machine_reason


def clear_playtest_exit_after_attestation(vault_root: Path, project_id: str) -> dict[str, Any]:
    """Clear park flags after operator pass — allows depth bump on next overnight."""
    pid = str(project_id or "").strip()
    pf = load_product_factory(vault_root, pid)
    if not pf.get("playtest_exit_eligible"):
        return {"ok": True, "skipped": True, "reason": "not_parked"}

    att_ok, att_reason = playtest_attestation_complete(vault_root, pid)
    if not att_ok:
        return {"ok": False, "reason": att_reason}

    updates = {
        **pf,
        "playtest_exit_eligible": False,
        "playtest_exit_session_id": "",
        "blocked_at": None,
        "playtest_last_attestation_at": _utc_iso(),
    }
    save_product_factory(vault_root, pid, updates)
    return {"ok": True, "reason": "playtest_attestation_cleared"}


def _utc_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
