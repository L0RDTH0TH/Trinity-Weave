"""Harness rail guards — block agent RESUME_ROADMAP when factory harness owns the phase."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .conceptual_track_ready import conceptual_factory_handoff_ready
from .done_when_eval import operator_loop_2_pending
from .product_factory_state import load_product_factory, normalize_completed_phases


def _normalize_mode(mode: str) -> str:
    return str(mode or "").strip().upper().replace(" ", "_").replace("-", "_")


def resume_roadmap_conceptual_factory_blocked(
    vault_root: Path,
    project_id: str,
    mode: str,
    params: dict[str, Any],
) -> tuple[bool, str]:
    """
    After conceptual factory handoff, RESUME_ROADMAP conceptual deepen is not the harness rail.

    Catalog mint / L5 use CATALOG_MINT_PROPOSE / L5_SCOPE_AUTHOR instead.
    """
    if _normalize_mode(mode) != "RESUME_ROADMAP":
        return False, ""
    track = str(params.get("roadmap_track") or "execution").lower()
    if track != "conceptual":
        return False, ""
    action = str(params.get("action") or "deepen").lower()
    if action in ("bootstrap-execution-track", "pass3_repair_drain", "handoff-audit"):
        return False, ""

    pid = str(project_id or params.get("project_id") or "").strip()
    if not pid:
        return False, ""

    if operator_loop_2_pending(vault_root, pid):
        return True, "operator_loop_2_pending_use_harness_rail"

    ready, _ = conceptual_factory_handoff_ready(vault_root, pid)
    if not ready:
        return False, ""

    pf = load_product_factory(vault_root, pid)
    completed = normalize_completed_phases(list(pf.get("completed_phases") or []))
    if "conceptual_deepen" not in completed:
        return False, ""

    return True, "conceptual_handoff_use_harness_rail"


def resume_roadmap_execution_implementation_blocked(
    vault_root: Path,
    project_id: str,
    mode: str,
    params: dict[str, Any],
) -> tuple[bool, str]:
    """
    When implementation_cell owns an active weld beat, RESUME_ROADMAP execution deepen is blocked.

    Half B factory dispatch / IMPLEMENT_SLICE owns the queue — not roadmap deepen.
    """
    if _normalize_mode(mode) != "RESUME_ROADMAP":
        return False, ""
    track = str(params.get("roadmap_track") or "execution").lower()
    if track != "execution":
        return False, ""
    action = str(params.get("action") or "deepen").lower()
    if action in ("bootstrap-execution-track", "pass3_repair_drain", "handoff-audit"):
        return False, ""

    pid = str(project_id or params.get("project_id") or "").strip()
    if not pid:
        return False, ""

    pf = load_product_factory(vault_root, pid)
    cell = pf.get("implementation_cell")
    if not isinstance(cell, dict):
        return False, ""
    phase = str(cell.get("phase") or "")
    if phase in ("", "idle", "cell_complete"):
        return False, ""

    return True, "implementation_cell_owns_beat"


def implement_slice_handoff_blocked(
    vault_root: Path,
    project_id: str,
    mode: str,
    params: dict[str, Any],
) -> tuple[bool, str]:
    """Block IMPLEMENT_SLICE / factory_lane when Half A→B handoff content gate fails."""
    action = str(params.get("action") or "").lower()
    norm_mode = _normalize_mode(mode)
    if norm_mode != "IMPLEMENT_SLICE" and action != "factory_lane":
        return False, ""

    pid = str(project_id or params.get("project_id") or "").strip()
    if not pid:
        return False, ""

    from ..factory.implementation_handoff_ready import implementation_handoff_ready

    pf = load_product_factory(vault_root, pid)
    cell = pf.get("implementation_cell")
    if isinstance(cell, dict):
        phase = str(cell.get("phase") or "")
        if phase not in ("", "idle", "cell_complete"):
            return False, ""

    ready, reason = implementation_handoff_ready(vault_root, pid)
    if not ready:
        return True, f"implementation_handoff_blocked:{reason}"
    return False, ""
