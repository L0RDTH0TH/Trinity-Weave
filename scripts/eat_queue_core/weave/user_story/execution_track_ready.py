"""Execution map completeness — content gate before factory_staged / Half B handoff."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ...merged_config import load_merged_yaml_blocks
from .conceptual_track_ready import (
    _group_notes_by_phase_and_level,
    _is_scaffold_only,
    _note_phase_number,
    _note_qualifies,
    _normalize_completed_phases,
    _read_note,
    _roadmap_level,
    load_conceptual_gate_config,
    phase_dirs_for_project,
)
from .execution_pseudo_code_audit import run_execution_pseudo_code_audit
from .product_factory_state import execution_track_exists

_PSEUDO_FENCE = re.compile(r"```(?:pseudo|pseudocode)?", re.I)
_PSEUDO_HEADING = re.compile(r"^#+\s*(pseudo[- ]?code|implementation sketch)", re.I | re.M)

DEFAULT_EXECUTION_GATE: dict[str, Any] = {
    "require_execution_state_complete": True,
    "require_pin_audit": True,
    "require_pseudo_code_primary": True,
    "min_handoff_readiness_primary": 75,
}

_SKIP_EXEC_NAMES = frozenset(
    {
        "roadmap-state-execution.md",
        "workflow_state.md",
        "distilled-core.md",
    }
)


def load_execution_gate_config(vault_root: Path) -> dict[str, Any]:
    cfg: dict[str, Any] = {}
    gate = load_conceptual_gate_config(vault_root)
    for k, v in gate.items():
        if isinstance(v, dict):
            cfg[k] = dict(v)
        else:
            cfg[k] = v
    for k, v in DEFAULT_EXECUTION_GATE.items():
        cfg[k] = v
    try:
        blocks = load_merged_yaml_blocks(vault_root)
        rf = blocks.get("roadmap_factory")
        if isinstance(rf, dict):
            eg = rf.get("execution_gate")
            if isinstance(eg, dict):
                for key, val in eg.items():
                    if val is not None:
                        cfg[key] = val
    except (ImportError, OSError, TypeError, ValueError):
        pass
    return cfg


def _execution_root(vault_root: Path, project_id: str) -> Path:
    return vault_root / "1-Projects" / project_id / "Roadmap" / "Execution"


def _read_execution_state_frontmatter(vault_root: Path, project_id: str) -> dict[str, Any]:
    path = _execution_root(vault_root, project_id) / "roadmap-state-execution.md"
    if not path.is_file():
        return {}
    fm, _ = _read_note(path)
    return fm


def _execution_state_terminal(fm: dict[str, Any], gate: dict[str, Any]) -> tuple[bool, str]:
    if not gate.get("require_execution_state_complete"):
        return True, "execution_state_check_skipped"

    status = str(fm.get("status") or "").lower().strip()
    if status not in ("complete", "completed", "ready-for-implementation", "implementation-ready"):
        return False, f"execution_state_not_complete:{status or 'missing'}"

    min_phases = int(gate.get("min_phases") or 6)
    try:
        current_phase = int(fm.get("current_phase") or 0)
    except (TypeError, ValueError):
        current_phase = 0
    if current_phase < min_phases:
        return False, f"execution_current_phase_below_{min_phases}:{current_phase}"

    if gate.get("require_completed_phases_1_through_n"):
        done = _normalize_completed_phases(fm.get("completed_phases"))
        missing = [n for n in range(1, min_phases + 1) if n not in done]
        if missing:
            return False, f"execution_completed_phases_missing:{missing[0]}"

    return True, "execution_state_terminal"


def _note_has_pseudo_code(body: str) -> bool:
    if _PSEUDO_FENCE.search(body) or _PSEUDO_HEADING.search(body):
        return True
    lowered = body.lower()
    return "pseudo-code" in lowered and len(body.strip()) > 400


def _passes_execution_nl(body: str, level: str, *, gate: dict[str, Any]) -> bool:
    if level == "primary" and gate.get("require_pseudo_code_primary"):
        return _note_has_pseudo_code(body)
    if level in ("secondary", "tertiary", "quaternary", "deeper"):
        return len(body.strip()) >= 120
    return True


def _execution_note_qualifies(
    fm: dict[str, Any],
    body: str,
    *,
    gate: dict[str, Any],
    level: str | None = None,
    min_readiness: int | None = None,
) -> bool:
    lvl = level or _roadmap_level(fm, Path("."))
    if not _note_qualifies(fm, body, gate=gate, level=lvl, min_readiness=min_readiness):
        return False
    return _passes_execution_nl(body, lvl, gate=gate)


def iter_execution_roadmap_notes(
    vault_root: Path, project_id: str
) -> list[tuple[Path, dict[str, Any], str]]:
    exec_root = _execution_root(vault_root, project_id)
    if not exec_root.is_dir():
        return []
    out: list[tuple[Path, dict[str, Any], str]] = []
    for path in exec_root.rglob("*.md"):
        if path.name in _SKIP_EXEC_NAMES:
            continue
        fm, body = _read_note(path)
        out.append((path, fm, body))
    return out


def execution_phase_dirs(vault_root: Path, project_id: str) -> dict[int, Path]:
    exec_root = _execution_root(vault_root, project_id)
    by_num: dict[int, Path] = {}
    if not exec_root.is_dir():
        return by_num
    for child in exec_root.iterdir():
        if not child.is_dir() or not child.name.startswith("Phase-"):
            continue
        m = re.match(r"Phase-(\d+)-", child.name)
        if m:
            by_num[int(m.group(1))] = child
    return by_num


def execution_map_complete(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """
    True when Execution/ tree passes content bar + optional pin audit.

    State file alone is insufficient — note bodies must qualify.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return False, "no_project_id"

    if not execution_track_exists(vault_root, pid):
        return False, "execution_track_missing"

    gate = load_execution_gate_config(vault_root)
    min_phases = int(gate.get("min_phases") or 6)
    min_primary_readiness = int(gate.get("min_handoff_readiness_primary") or 75)

    state_fm = _read_execution_state_frontmatter(vault_root, pid)
    ok, reason = _execution_state_terminal(state_fm, gate)
    if not ok:
        return False, reason

    phase_dirs = execution_phase_dirs(vault_root, pid)
    for n in range(1, min_phases + 1):
        if n not in phase_dirs:
            return False, f"execution_phases_missing:{n}"

    all_notes = iter_execution_roadmap_notes(vault_root, pid)
    grouped = _group_notes_by_phase_and_level(all_notes)

    for phase_num in range(1, min_phases + 1):
        levels = grouped.get(phase_num) or {}
        primaries = levels.get("primary") or []
        if not primaries:
            return False, f"execution_primary_missing:phase_{phase_num}"

        qualified = [
            (p, fm, b)
            for p, fm, b in primaries
            if _execution_note_qualifies(
                fm, b, gate=gate, level="primary", min_readiness=min_primary_readiness
            )
        ]
        if not qualified:
            return False, f"execution_primary_incomplete:phase_{phase_num}"

        for level_name in ("secondary", "tertiary", "quaternary", "deeper"):
            for path, fm, body in levels.get(level_name) or []:
                if not _execution_note_qualifies(fm, body, gate=gate, level=level_name):
                    rel = path.relative_to(vault_root)
                    return False, f"execution_note_incomplete:{rel}"

    if gate.get("require_pin_audit"):
        audit = run_execution_pseudo_code_audit(vault_root, project_id=pid)
        if not audit.ok:
            detail = audit.violations[0] if audit.violations else "pin_audit_failed"
            return False, f"execution_pin_audit:{detail}"

    return True, "execution_map_complete"


def execution_factory_handoff_ready(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """Hard gate before factory_staged / IMPLEMENT_SLICE staging."""
    return execution_map_complete(vault_root, project_id)


def execution_track_ready(vault_root: Path, project_id: str) -> tuple[bool, str]:
    return execution_map_complete(vault_root, project_id)
