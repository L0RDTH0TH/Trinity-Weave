"""Vault resume pointer reconcile — Half A roadmap factory ledger vs goal packet."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .catalog_io import user_story_paths
from .conceptual_track_ready import conceptual_factory_handoff_ready, roadmap_tree_complete
from .done_when_eval import (
    done_when_requests_operator_loop_2,
    loop2_exit_eligible_for_project,
    loop2_exit_honestly_eligible,
    loop2_machine_artifacts_ready,
    loop2_machine_ready,
    operator_loop_2_pending,
)
from .execution_track_ready import execution_map_complete
from .goal_packet_profile import ProfileValidation, validate_goal_packet_profile
from .product_factory_state import load_product_factory, normalize_completed_phases


@dataclass
class ReconcileResult:
    ok: bool
    project_id: str
    drift_codes: list[str] = field(default_factory=list)
    inferred_phases: dict[str, bool] = field(default_factory=dict)
    conceptual_map_complete: bool = False
    conceptual_reason: str = ""
    pipeline_phase: str = ""
    blocker: str = ""
    gate_evidence: dict[str, Any] = field(default_factory=dict)
    execution_ready: bool = False
    execution_reason: str = ""
    loop2_exit_eligible: bool = False
    goal_packet_run_id: str = ""
    profile: ProfileValidation | None = None
    recommended_action: str = ""

    # Back-compat alias — same bar as conceptual_map_complete
    @property
    def conceptual_ready(self) -> bool:
        return self.conceptual_map_complete

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "project_id": self.project_id,
            "drift_codes": list(self.drift_codes),
            "inferred_phases": dict(self.inferred_phases),
            "conceptual_map_complete": self.conceptual_map_complete,
            "conceptual_ready": self.conceptual_map_complete,
            "conceptual_reason": self.conceptual_reason,
            "pipeline_phase": self.pipeline_phase,
            "blocker": self.blocker,
            "gate_evidence": dict(self.gate_evidence),
            "execution_ready": self.execution_ready,
            "execution_reason": self.execution_reason,
            "loop2_exit_eligible": self.loop2_exit_eligible,
            "goal_packet_run_id": self.goal_packet_run_id,
            "profile": self.profile.to_dict() if self.profile else None,
            "recommended_action": self.recommended_action,
        }


def should_factory_bootstrap(
    vault_root: Path,
    project_id: str,
    goal_packet: dict[str, Any] | None,
    params: dict[str, Any] | None = None,
) -> bool:
    """
    True only when factory spine should be wiped and re-seeded (BOOTSTRAP).

    Resume / remint with existing tree must not reset the ledger.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return True
    hints: dict[str, Any] = {}
    if isinstance(goal_packet, dict):
        hints = (
            goal_packet.get("planner_hints")
            if isinstance(goal_packet.get("planner_hints"), dict)
            else {}
        )
    if isinstance(params, dict):
        if params.get("force_factory_bootstrap") is True:
            return True
        if params.get("session_mode"):
            hints = {**hints, "session_mode": params["session_mode"]}

    if hints.get("force_factory_bootstrap") is True:
        return True

    session = str(hints.get("session_mode") or "").lower().strip()
    if session in ("resume", "remint", "deepen_only"):
        return False

    if hints.get("resume_factory") is True and roadmap_tree_complete(vault_root, pid):
        return False

    if roadmap_tree_complete(vault_root, pid):
        return False

    return True


def _resolve_recommended_action(
    *,
    strict_ok: bool,
    strict_reason: str,
    execution_ok: bool,
    arts_ok: bool,
    loop2_ready: bool,
    loop2_pending: bool,
    goal_packet: dict[str, Any],
    catalog_on_disk: bool,
    profile: ProfileValidation | None,
) -> tuple[str, str, str]:
    """Return recommended_action, pipeline_phase, blocker — single unified conceptual bar."""
    if profile and not profile.ok:
        return "fix_goal_packet", "goal_packet", "profile_invalid"

    if not strict_ok:
        return "conceptual_deepen", "conceptual_deepen", strict_reason

    if loop2_ready or loop2_pending:
        return "operator_loop_2_gate", "operator_loop_2", "pending_human_sign_off"

    if not catalog_on_disk:
        return "harness_catalog_mint", "catalog_mint", "catalog_missing"

    if arts_ok and done_when_requests_operator_loop_2(goal_packet):
        return "harness_loop2_prep", "loop2_prep", "machine_artifacts_ready"

    if arts_ok and not loop2_ready:
        return "harness_loop2_prep", "loop2_prep", "conductor_not_parked"

    if loop2_ready and not execution_ok:
        return "execution_deepen", "execution_deepen", "execution_track_incomplete"

    return "continue", "continue", ""


def reconcile_factory_cursor(
    vault_root: Path,
    project_id: str,
    goal_packet: dict[str, Any] | None = None,
) -> ReconcileResult:
    """
    Merge vault resume pointer with goal packet intent.

    Authority: operator attestations > live content gates > product_factory ledger > packet.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    drift: list[str] = []
    inferred: dict[str, bool] = {}

    packet = goal_packet if isinstance(goal_packet, dict) else {}
    run_id = str(packet.get("run_id") or "")

    profile = validate_goal_packet_profile(packet, vault_root) if packet else None
    if profile and not profile.ok:
        drift.extend([f"profile:{v}" for v in profile.violations[:8]])

    strict_ok, strict_reason = conceptual_factory_handoff_ready(
        vault_root, pid, goal_packet=packet if packet else None
    )
    execution_ok, execution_reason = execution_map_complete(vault_root, pid)

    pf = load_product_factory(vault_root, pid) if pid else {}
    completed = normalize_completed_phases(list(pf.get("completed_phases") or []))

    paths = user_story_paths(vault_root, pid) if pid else {}
    catalog_on_disk = bool(paths.get("catalog") and paths["catalog"].is_file())

    inferred["conceptual_deepen"] = strict_ok
    inferred["catalog_mint"] = strict_ok and ("catalog_mint" in completed or catalog_on_disk)
    inferred["execution_deepen"] = execution_ok or "execution_deepen" in completed
    inferred["factory_staged"] = "factory_staged" in completed

    if catalog_on_disk and not strict_ok:
        drift.append("catalog_ahead_of_conceptual_freeze")

    if "conceptual_deepen" in completed and not strict_ok:
        drift.append("ledger_conceptual_complete_but_content_gate_failed")
        inferred["conceptual_deepen"] = False

    if "catalog_mint" in completed and not strict_ok:
        drift.append("ledger_catalog_mint_ahead_of_conceptual_freeze")
        inferred["catalog_mint"] = False

    if pf.get("loop2_exit_eligible") is True and not strict_ok:
        drift.append("loop2_exit_eligible_without_conceptual_freeze")

    if pid and not strict_ok:
        from .conceptual_dispatch_authority import workflow_state_contradicts_feed_gate

        if workflow_state_contradicts_feed_gate(vault_root, pid):
            drift.append("legacy_rollup_closed_contradicts_feed_gate")

    if "execution_deepen" in completed and not execution_ok:
        drift.append("ledger_execution_complete_but_content_gate_failed")
        inferred["execution_deepen"] = False

    if "factory_staged" in completed and not execution_ok:
        drift.append("factory_staged_without_execution_handoff")

    loop2_eligible = loop2_exit_honestly_eligible(vault_root, pid) if pid else False
    loop2_ready, _loop2_reason = loop2_machine_ready(vault_root, pid) if pid else (False, "")
    raw_loop2_flag = loop2_exit_eligible_for_project(vault_root, pid) if pid else False
    arts_ok, art_reason, art_evidence = (
        loop2_machine_artifacts_ready(vault_root, pid) if pid else (False, "", {})
    )

    if raw_loop2_flag and not loop2_ready:
        drift.append("loop2_exit_eligible_without_artifacts")

    loop2_pending = operator_loop_2_pending(vault_root, pid) if pid else False

    recommended, pipeline_phase, blocker = _resolve_recommended_action(
        strict_ok=strict_ok,
        strict_reason=strict_reason,
        execution_ok=execution_ok,
        arts_ok=arts_ok,
        loop2_ready=loop2_ready,
        loop2_pending=loop2_pending,
        goal_packet=packet,
        catalog_on_disk=catalog_on_disk,
        profile=profile,
    )

    ok = len(drift) == 0 and (profile is None or profile.ok)

    return ReconcileResult(
        ok=ok,
        project_id=pid,
        drift_codes=drift,
        inferred_phases=inferred,
        conceptual_map_complete=strict_ok,
        conceptual_reason=strict_reason,
        pipeline_phase=pipeline_phase,
        blocker=blocker,
        gate_evidence={"loop2_artifacts": art_evidence, "loop2_artifact_reason": art_reason},
        execution_ready=execution_ok,
        execution_reason=execution_reason,
        loop2_exit_eligible=loop2_eligible,
        goal_packet_run_id=run_id,
        profile=profile,
        recommended_action=recommended,
    )
