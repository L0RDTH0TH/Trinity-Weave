"""Factory feed readiness — mint-batch-scoped gate before catalog mint (rung 1)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog_mint_propose import _find_pmg_path, _resolve_mint_batch
from .conceptual_track_ready import (
    _group_notes_by_phase_and_level,
    _note_qualifies,
    _roadmap_state_terminal,
    _read_state_frontmatter,
    iter_conceptual_roadmap_notes,
    load_conceptual_gate_config,
    phase_dirs_for_project,
    roadmap_tree_complete,
)
from ..roadmap.branch_depth import (
    collect_subphase_indexes,
    load_deepen_traversal_config,
    oversized_note_without_children,
)


def resolve_feed_mint_batch(
    vault_root: Path,
    *,
    mint_batch: str | None = None,
    goal_packet: dict[str, Any] | None = None,
) -> str:
    if mint_batch:
        return str(mint_batch).strip().lower()
    packet = goal_packet if isinstance(goal_packet, dict) else {}
    for key in ("mint_batch",):
        if packet.get(key):
            return str(packet[key]).strip().lower()
    hints = packet.get("planner_hints")
    if isinstance(hints, dict) and hints.get("mint_batch"):
        return str(hints["mint_batch"]).strip().lower()
    return _resolve_mint_batch(vault_root, None)


def _feed_handoff_floor(gate: dict[str, Any]) -> int:
    raw = gate.get("min_handoff_readiness_feedstock")
    if raw is None:
        raw = gate.get("min_handoff_readiness_primary", 75)
    return int(raw or 75)


def _validate_phases(
    vault_root: Path,
    project_id: str,
    *,
    phase_nums: range,
    gate: dict[str, Any],
) -> tuple[bool, str, dict[str, Any]]:
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    min_readiness = _feed_handoff_floor(gate)
    phase_dirs = phase_dirs_for_project(vault_root, pid)
    all_notes = iter_conceptual_roadmap_notes(vault_root, pid)
    grouped = _group_notes_by_phase_and_level(all_notes)
    traversal_cfg = load_deepen_traversal_config(vault_root)
    subphase_indexes = (
        collect_subphase_indexes(vault_root, pid)
        if traversal_cfg.get("reject_oversized_without_children")
        else []
    )

    evidence: dict[str, Any] = {
        "phases_checked": list(phase_nums),
        "feedstock_paths": [],
    }

    for phase_num in phase_nums:
        if phase_num not in phase_dirs:
            return False, f"conceptual_phases_missing:{phase_num}", evidence

        levels = grouped.get(phase_num) or {}
        primaries = levels.get("primary") or []
        if not primaries:
            return False, f"conceptual_primary_missing:phase_{phase_num}", evidence

        qual_primaries = [
            (p, fm, b)
            for p, fm, b in primaries
            if _note_qualifies(
                fm, b, gate=gate, level="primary", min_readiness=min_readiness
            )
        ]
        if not qual_primaries:
            return False, f"conceptual_primary_incomplete:phase_{phase_num}", evidence

        if gate.get("require_secondary_per_primary"):
            secondaries = levels.get("secondary") or []
            qual_sec = [
                (p, fm, b)
                for p, fm, b in secondaries
                if _note_qualifies(
                    fm, b, gate=gate, level="secondary", min_readiness=min_readiness
                )
            ]
            if len(qual_sec) < len(primaries):
                return False, f"conceptual_secondary_tree_incomplete:phase_{phase_num}", evidence

            if gate.get("require_tertiary_per_secondary"):
                tertiaries = levels.get("tertiary") or []
                qual_ter = [
                    (p, fm, b)
                    for p, fm, b in tertiaries
                    if _note_qualifies(
                        fm, b, gate=gate, level="tertiary", min_readiness=min_readiness
                    )
                ]
                if len(qual_ter) < len(qual_sec):
                    return False, f"conceptual_tertiary_tree_incomplete:phase_{phase_num}", evidence

        for level_name in ("primary", "secondary", "tertiary", "quaternary", "deeper"):
            for path, fm, body in levels.get(level_name) or []:
                if not _note_qualifies(
                    fm,
                    body,
                    gate=gate,
                    level=level_name,
                    min_readiness=min_readiness,
                ):
                    rel = str(path.relative_to(vault_root))
                    return False, f"feedstock_incomplete:{rel}", evidence
                evidence["feedstock_paths"].append(str(path.relative_to(vault_root)))
                if gate.get("apply_oversize_branch_gate_at_freeze", True):
                    oversize, oreason = oversized_note_without_children(
                        vault_root,
                        pid,
                        path,
                        fm,
                        body,
                        sibling_indexes=subphase_indexes,
                        cfg=traversal_cfg,
                    )
                    if oversize:
                        return False, oreason, evidence

    return True, "conceptual_factory_feed_ready", evidence


def conceptual_factory_feed_ready(
    vault_root: Path,
    project_id: str,
    *,
    mint_batch: str | None = None,
    goal_packet: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    """
    True when conceptual feedstock is sufficient for the declared mint batch.

    pmg_phases: phases 1..min_phases full structural + NL + handoff bar.
    presentation_first: Phase 6 feedstock only (6.1.x spine).
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return False, "no_project_id"

    if not roadmap_tree_complete(vault_root, pid):
        return False, "roadmap_tree_incomplete"

    if _find_pmg_path(vault_root, pid) is None:
        return False, "pmg_not_found"

    gate = load_conceptual_gate_config(vault_root)
    batch = resolve_feed_mint_batch(vault_root, mint_batch=mint_batch, goal_packet=goal_packet)
    min_phases = int(gate.get("min_phases") or 6)

    state_fm = _read_state_frontmatter(vault_root, pid)
    ok, reason = _roadmap_state_terminal(state_fm, gate)
    if not ok:
        return False, reason

    if batch == "presentation_first":
        phase_nums = range(6, 7)
    else:
        phase_nums = range(1, min_phases + 1)

    ready, reason, _evidence = _validate_phases(
        vault_root, pid, phase_nums=phase_nums, gate=gate
    )
    if not ready:
        return False, reason
    return True, f"conceptual_factory_feed_ready:{batch}"


def conceptual_factory_feed_report(
    vault_root: Path,
    project_id: str,
    *,
    mint_batch: str | None = None,
    goal_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Harness report with evidence."""
    batch = resolve_feed_mint_batch(vault_root, mint_batch=mint_batch, goal_packet=goal_packet)
    gate = load_conceptual_gate_config(vault_root)
    min_phases = int(gate.get("min_phases") or 6)
    phase_nums = range(6, 7) if batch == "presentation_first" else range(1, min_phases + 1)

    state_fm = _read_state_frontmatter(vault_root, project_id)
    state_ok, state_reason = _roadmap_state_terminal(state_fm, gate)
    if not state_ok:
        return {
            "ok": False,
            "mint_batch": batch,
            "reason": state_reason,
            "violations": [state_reason],
            "evidence": {},
        }

    ready, reason, evidence = _validate_phases(
        vault_root, project_id, phase_nums=phase_nums, gate=gate
    )
    return {
        "ok": ready,
        "mint_batch": batch,
        "reason": reason,
        "violations": [] if ready else [reason],
        "evidence": evidence,
    }
