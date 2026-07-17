"""Vault resume pointer reconcile — Half B implementation factory vs goal packet."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .factory_levels import factory_levels_satisfied
from .factory_orchestrator import DEFAULT_QUEUE_REL, load_alpha_queue
from .implementation_handoff_ready import implementation_handoff_ready
from .playtest_gate_policy import DEFAULT_POLICY, resolve_playtest_gate_policy
from .slice_advance import load_completion_tracker
from ..user_story.goal_packet_profile import ProfileValidation, validate_goal_packet_profile
from ..user_story.implementation_artifact_ledger import reconcile_implementation_ledger_drift
from ..user_story.playtest_manual_gate import playtest_gate_surface_ready
from ..user_story.product_factory_state import (
    FACTORY_STAGED,
    load_product_factory,
    normalize_completed_phases,
)
from .weld_beat_ready import (
    playtest_attestation_complete,
    playtest_exit_eligible_for_project,
    playtest_exit_honestly_eligible,
)


@dataclass
class ImplementationReconcileResult:
    ok: bool
    project_id: str
    drift_codes: list[str] = field(default_factory=list)
    levels_satisfied: bool = False
    levels_reason: str = ""
    handoff_ready: bool = False
    handoff_reason: str = ""
    playtest_gate_ready: bool = False
    playtest_reason: str = ""
    playtest_exit_eligible: bool = False
    playtest_attested: bool = False
    implementation_cell_phase: str = ""
    active_slice_id: str = ""
    cdp_present: bool = False
    alpha_queue_active: str = ""
    goal_packet_run_id: str = ""
    playtest_gate_policy: str = ""
    profile: ProfileValidation | None = None
    recommended_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "project_id": self.project_id,
            "drift_codes": list(self.drift_codes),
            "levels_satisfied": self.levels_satisfied,
            "levels_reason": self.levels_reason,
            "handoff_ready": self.handoff_ready,
            "handoff_reason": self.handoff_reason,
            "playtest_gate_ready": self.playtest_gate_ready,
            "playtest_reason": self.playtest_reason,
            "playtest_exit_eligible": self.playtest_exit_eligible,
            "playtest_attested": self.playtest_attested,
            "implementation_cell_phase": self.implementation_cell_phase,
            "active_slice_id": self.active_slice_id,
            "cdp_present": self.cdp_present,
            "alpha_queue_active": self.alpha_queue_active,
            "goal_packet_run_id": self.goal_packet_run_id,
            "playtest_gate_policy": self.playtest_gate_policy,
            "profile": self.profile.to_dict() if self.profile else None,
            "recommended_action": self.recommended_action,
        }


def _active_alpha_slice(vault_root: Path, queue_rel: str = DEFAULT_QUEUE_REL) -> str:
    queue = load_alpha_queue(vault_root, queue_rel)
    for sl in queue.get("slices") or []:
        if isinstance(sl, dict) and str(sl.get("status")) == "active":
            return str(sl.get("id") or "")
    return ""


def _resolve_active_slice_id(vault_root: Path, project_id: str, pf: dict[str, Any]) -> str:
    active = pf.get("active_slice") if isinstance(pf.get("active_slice"), dict) else {}
    row_ids = active.get("row_ids") if isinstance(active.get("row_ids"), list) else []
    if row_ids:
        return str(row_ids[0])
    cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
    sid = str(cell.get("slice_id") or "")
    if sid:
        return sid
    tracker = load_completion_tracker(vault_root)
    slices = tracker.get("slices") or {}
    if isinstance(slices, dict) and slices:
        return next(iter(slices.keys()), "")
    return _active_alpha_slice(vault_root)


def reconcile_implementation_cursor(
    vault_root: Path,
    project_id: str,
    goal_packet: dict[str, Any] | None = None,
    *,
    lane: str = "",
) -> ImplementationReconcileResult:
    """
    Merge Half B resume pointer with goal packet intent.

    Authority: operator playtest attestations > weld_beat_ready > handoff content >
    implementation_cell + budget + CDP + completion tracker > goal packet intent.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    drift: list[str] = []

    from .half_b_ledger_sync import honest_half_b_ledger_sync

    sync = honest_half_b_ledger_sync(vault_root, pid) if pid else {"steps": []}

    packet = goal_packet if isinstance(goal_packet, dict) else {}
    run_id = str(packet.get("run_id") or "")

    profile = validate_goal_packet_profile(packet, vault_root) if packet else None
    if profile and not profile.ok:
        drift.extend([f"profile:{v}" for v in profile.violations[:8]])

    policy = resolve_playtest_gate_policy(vault_root, packet, project_id=pid) if pid else DEFAULT_POLICY

    pf = load_product_factory(vault_root, pid) if pid else {}
    completed = normalize_completed_phases(list(pf.get("completed_phases") or []))
    if FACTORY_STAGED not in completed:
        drift.append("factory_staged_missing")

    cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
    cell_phase = str(cell.get("phase") or "")
    slice_id = _resolve_active_slice_id(vault_root, pid, pf)

    handoff_ok, handoff_reason = implementation_handoff_ready(vault_root, pid) if pid else (False, "")
    if not handoff_ok and FACTORY_STAGED in completed:
        drift.append(f"handoff_regress:{handoff_reason}")

    cdp_present = False
    if slice_id:
        cdp = load_cell_dispatch_plan(vault_root, slice_id)
        cdp_present = bool(cdp and cdp.get("lanes"))

    alpha_active = _active_alpha_slice(vault_root)

    levels_ok, levels_reason = factory_levels_satisfied(vault_root, pid) if pid else (False, "no_project_id")
    playtest_ok, playtest_reason = playtest_gate_surface_ready(vault_root, pid) if pid else (False, "")
    playtest_eligible = playtest_exit_honestly_eligible(vault_root, pid) if pid else False
    raw_playtest_eligible = playtest_exit_eligible_for_project(vault_root, pid) if pid else False
    att_ok, att_reason = playtest_attestation_complete(vault_root, pid) if pid else (False, "")

    ledger = reconcile_implementation_ledger_drift(vault_root, pid) if pid else None
    if ledger and not ledger.ok:
        drift.extend([f"ledger:{c}" for c in ledger.drift_codes[:6]])

    if raw_playtest_eligible and not playtest_ok and not att_ok:
        drift.append("playtest_exit_eligible_without_surface")
    if raw_playtest_eligible and not playtest_eligible:
        drift.append("playtest_exit_eligible_without_handoff")

    recommended = "continue_weld"
    if levels_ok:
        recommended = "levels_complete"
    elif playtest_eligible and not att_ok:
        recommended = "playtest_manual_gate"
    elif playtest_ok and not playtest_eligible:
        recommended = "playtest_manual_gate"
    elif FACTORY_STAGED not in completed:
        recommended = "await_factory_staged"
    elif not handoff_ok:
        recommended = "await_implementation_handoff"
    elif cell_phase in ("awaiting_compose", "composed", "wave_dispatched", "lanes_running", "pm_review", "rework"):
        recommended = "continue_weld"
    elif profile and not profile.ok:
        recommended = "fix_goal_packet"
    elif playtest_eligible and att_ok:
        recommended = "depth_bump_continue"

    ok = len(drift) == 0 and (profile is None or profile.ok)

    return ImplementationReconcileResult(
        ok=ok,
        project_id=pid,
        drift_codes=drift,
        levels_satisfied=levels_ok,
        levels_reason=levels_reason,
        handoff_ready=handoff_ok,
        handoff_reason=handoff_reason,
        playtest_gate_ready=playtest_ok,
        playtest_reason=playtest_reason,
        playtest_exit_eligible=playtest_eligible,
        playtest_attested=att_ok,
        implementation_cell_phase=cell_phase,
        active_slice_id=slice_id,
        cdp_present=cdp_present,
        alpha_queue_active=alpha_active,
        goal_packet_run_id=run_id,
        playtest_gate_policy=policy,
        profile=profile,
        recommended_action=recommended,
    )
