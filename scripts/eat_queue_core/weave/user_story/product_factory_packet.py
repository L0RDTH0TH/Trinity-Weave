"""Goal-packet helpers — Architect roadmap factory (Half A) profile."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .done_when_eval import (
    LOOP_2_BLOCKED_AT,
    OPERATOR_LOOP_2_DONE_WHEN_TOKENS,
    _normalize_done_when_token,
    done_when_requests_operator_loop_2,
    evaluate_done_when,
    loop2_machine_ready,
    roadmap_tree_complete,
)
from .product_factory_state import load_product_factory


def greenfield_roadmap_launch_needed(vault_root: Path, packet: dict[str, Any]) -> bool:
    """
    Greenfield Half A — ROADMAP_MODE (full tree) before product factory conductor.

    Packet hints: fresh_greenfield, greenfield_launch, require_roadmap_mode_setup,
    or primary_mode ROADMAP_MODE when roadmap tree is incomplete.
    """
    if not product_factory_roadmap_packet(packet):
        return False
    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    pid = str(packet.get("project_id") or "").strip()
    if hints.get("fresh_greenfield") is True or hints.get("greenfield_launch") is True:
        if pid and roadmap_tree_complete(vault_root, pid):
            return False
        return True
    if hints.get("require_roadmap_mode_setup") is True:
        return True
    primary = str(hints.get("primary_mode") or "").upper().replace("-", "_")
    if primary == "ROADMAP_MODE":
        pid = str(packet.get("project_id") or "").strip()
        return bool(pid) and not roadmap_tree_complete(vault_root, pid)
    return False


def product_factory_roadmap_packet(packet: dict[str, Any]) -> bool:
    """
    Half A product factory packet — project_id + PMG + explicit factory intent.

    Not active when implementation-track overnight (unless implementation_gate blocks deepen).
    """
    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    if str(hints.get("effective_track") or "").lower() == "implementation":
        policy = packet.get("early_stop_policy") if isinstance(packet.get("early_stop_policy"), dict) else {}
        if policy.get("implementation_gate") is not True:
            return False
    if not str(packet.get("project_id") or "").strip():
        return False
    if not str(packet.get("master_goal_ref") or "").strip():
        return False

    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    if hints.get("product_factory") is True:
        return True
    primary = str(hints.get("primary_mode") or "").upper().replace("-", "_")
    if primary in (
        "ROADMAP_FACTORY_BOOTSTRAP",
        "ROADMAP_FACTORY_RELAUNCH",
        "PRODUCT_FACTORY_CONTINUE",
    ):
        return True
    if str(hints.get("factory_profile") or "").lower() in ("roadmap", "product_factory", "half_a"):
        return True
    if done_when_requests_operator_loop_2(packet):
        return True

    policy = packet.get("early_stop_policy") if isinstance(packet.get("early_stop_policy"), dict) else {}
    if policy.get("implementation_gate") is True and hints.get("feed_authority") == "vault_roadmap":
        return True
    return False


def factory_bootstrap_needed(vault_root: Path, packet: dict[str, Any]) -> bool:
    """
    True only for first factory boot — no roadmap tree yet, or operator forced reset.

    When the tree exists, overnight/planner must seed PRODUCT_FACTORY_CONTINUE instead.
    """
    if not product_factory_roadmap_packet(packet):
        return False
    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    if hints.get("force_factory_bootstrap") is True:
        return True
    pid = str(packet.get("project_id") or "").strip()
    if not pid:
        return True
    return not roadmap_tree_complete(vault_root, pid)


def loop2_surface_ready(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """Backward-compatible alias — delegates to loop2_machine_ready."""
    ok, reason = loop2_machine_ready(vault_root, project_id)
    if ok:
        return True, "loop2_surface_ready"
    return False, reason


def roadmap_factory_mission_incomplete(
    vault_root: Path,
    packet: dict[str, Any],
) -> tuple[bool, str]:
    """
    True while a Half A roadmap-factory goal packet still owes deliverables on disk.

    Project-agnostic — driven by ``packet.project_id`` and vault gates, not greenfield hints.
    """
    if not product_factory_roadmap_packet(packet):
        return False, ""
    pid = str(packet.get("project_id") or "").strip()
    if not pid:
        return False, "no_project_id"

    from .done_when_eval import loop2_exit_honestly_eligible

    if loop2_exit_honestly_eligible(vault_root, pid):
        return False, "loop2_exit_eligible"

    result = evaluate_done_when(vault_root, packet, project_id=pid)
    if result.matched:
        return False, ""

    if not roadmap_tree_complete(vault_root, pid):
        return True, "roadmap_tree_incomplete"

    pf = load_product_factory(vault_root, pid)
    completed = pf.get("completed_phases") or []
    if "conceptual_deepen" not in completed:
        from .conceptual_track_ready import conceptual_track_ready

        ready, reason = conceptual_track_ready(vault_root, pid)
        if not ready:
            return True, reason or "conceptual_deepen_pending"

    ready, reason = loop2_machine_ready(vault_root, pid)
    if not ready:
        return True, reason
    return False, ""


def defer_hollow_eat_for_roadmap_factory_mission(
    vault_root: Path,
    packet: dict[str, Any],
) -> tuple[bool, str]:
    """
    Pass-level hollow must not end overnight while Half A mission is active.

    Mission authority (goal packet + vault gates) outranks ``hollow_eat_success``.
    """
    if not product_factory_roadmap_packet(packet):
        return False, ""
    policy = packet.get("early_stop_policy") if isinstance(packet.get("early_stop_policy"), dict) else {}
    if policy.get("hollow_fatal") is True:
        return False, "hollow_fatal_policy"
    result = evaluate_done_when(vault_root, packet)
    if result.matched:
        return False, ""
    inc, reason = roadmap_factory_mission_incomplete(vault_root, packet)
    if inc:
        return True, reason
    if done_when_requests_operator_loop_2(packet):
        return True, "done_when_not_met"
    return True, "roadmap_factory_active"


def greenfield_factory_overnight_incomplete(
    vault_root: Path,
    packet: dict[str, Any],
) -> tuple[bool, str]:
    """
    True while a greenfield Half A packet still needs factory passes after PQ drain.

    Prevents premature ``pq_drained`` exit between ROADMAP_MODE and factory conductor.
    """
    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    if not (hints.get("greenfield_launch") or hints.get("fresh_greenfield")):
        return False, ""
    return roadmap_factory_mission_incomplete(vault_root, packet)


def operator_loop_2_gate_reached(
    vault_root: Path,
    project_id: str,
) -> tuple[bool, str]:
    """True when loop-2 deliverable surface exists and conductor awaits operator mutate/attest."""
    return loop2_machine_ready(vault_root, project_id)


def roadmap_factory_done_when_matched(
    vault_root: Path,
    packet: dict[str, Any],
    *,
    project_id: str | None = None,
) -> tuple[bool, str]:
    """Match goal packet done_when for operator loop 2 / L5 manual gate."""
    result = evaluate_done_when(vault_root, packet, project_id=project_id)
    if not result.matched:
        return False, result.reason
    reason = result.reason
    if reason in ("loop2_machine_ready", "loop2_exit_eligible"):
        reason = "loop2_surface_ready"
    return True, reason
