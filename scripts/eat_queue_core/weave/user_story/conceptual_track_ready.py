"""Conceptual map completeness and factory feed gate before catalog mint / L5."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from ...merged_config import load_merged_yaml_blocks
from ..roadmap.branch_depth import (
    collect_subphase_indexes,
    load_deepen_traversal_config,
    oversized_note_without_children,
)

_SKIP_REL_PARTS = (
    "/User-Story/",
    "/Execution/",
    "/Conceptual-Amendments/",
    "/Conceptual-Decision-Records/",
    "/Versions/",
    "/.snapshots/",
)

_SKIP_NAMES = frozenset(
    {
        "workflow_state.md",
        "roadmap-state.md",
        "distilled-core.md",
        "decisions-log.md",
    }
)

# Factory default: mint-batch feed gate (pmg_phases stress test). Legacy full_tree via mode override.
DEFAULT_CONCEPTUAL_GATE: dict[str, Any] = {
    "mode": "factory_feed_ready",
    "default_mint_batch": "pmg_phases",
    "min_phases": 6,
    "require_roadmap_state_complete": True,
    "require_completed_phases_1_through_n": True,
    "require_secondary_per_primary": True,
    "require_tertiary_per_secondary": True,
    "apply_oversize_branch_gate_at_freeze": True,
    "min_handoff_readiness_primary": 75,
    "min_handoff_readiness_feedstock": 75,
    "min_body_chars": {
        "primary": 500,
        "secondary": 450,
        "tertiary": 400,
        "quaternary": 350,
        "default": 300,
    },
    "require_nl_checklist": True,
}

_HARD_CONCEPTUAL_BLOCKERS = frozenset(
    {
        "contradictions_detected",
        "incoherence",
        "state_hygiene_failure",
        "safety_critical_ambiguity",
    }
)

_NL_BEHAVIOR_RE = re.compile(
    r"(?i)(##\s*behavior|actors[,:\s]|inputs[,:\s].*outputs|core loop|player-visible)"
)
_NL_SCOPE_RE = re.compile(
    r"(?i)(##\s*scope|does not cover|explicitly out of scope|in scope)"
)
_SCAFFOLD_MARKERS = (
    "Seed tasks",
    "aligned with PMG Phase",
    "Half A factory loop 1",
    "no catalog mint",
    "vision only",
)


def load_conceptual_gate_config(vault_root: Path) -> dict[str, Any]:
    cfg: dict[str, Any] = {}
    for k, v in DEFAULT_CONCEPTUAL_GATE.items():
        if isinstance(v, dict):
            cfg[k] = dict(v)
        else:
            cfg[k] = v
    try:
        blocks = load_merged_yaml_blocks(vault_root)
        rf = blocks.get("roadmap_factory")
        if isinstance(rf, dict):
            gate = rf.get("conceptual_gate")
            if isinstance(gate, dict):
                for key, val in gate.items():
                    if val is None:
                        continue
                    if key == "min_body_chars" and isinstance(val, dict):
                        merged = dict(cfg.get("min_body_chars") or {})
                        merged.update(val)
                        cfg["min_body_chars"] = merged
                    else:
                        cfg[key] = val
        roadmap = blocks.get("roadmap")
        if isinstance(roadmap, dict) and roadmap.get("conceptual_design_handoff_min_readiness") is not None:
            cfg["min_handoff_readiness_primary"] = int(
                roadmap["conceptual_design_handoff_min_readiness"]
            )
    except (ImportError, OSError, TypeError, ValueError):
        pass
    return cfg


def _read_note(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}, text.strip()
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text.strip()
    fm = yaml.safe_load(text[4:end]) or {}
    body = text[end + 4 :].lstrip("\n").strip()
    return (fm if isinstance(fm, dict) else {}), body


def _read_state_frontmatter(vault_root: Path, project_id: str) -> dict[str, Any]:
    path = vault_root / "1-Projects" / project_id / "Roadmap" / "roadmap-state.md"
    if not path.is_file():
        return {}
    fm, _ = _read_note(path)
    return fm


def _is_conceptual_roadmap_path(rel: str) -> bool:
    if any(part in rel for part in _SKIP_REL_PARTS):
        return False
    name = Path(rel).name
    if name in _SKIP_NAMES or "MOC" in name or "Roadmap-MOC" in name:
        return False
    if name.startswith("Source-"):
        return False
    if "/Phase-" not in rel:
        return False
    return rel.endswith(".md")


def iter_conceptual_roadmap_notes(vault_root: Path, project_id: str) -> list[tuple[Path, dict[str, Any], str]]:
    road = vault_root / "1-Projects" / project_id / "Roadmap"
    if not road.is_dir():
        return []
    out: list[tuple[Path, dict[str, Any], str]] = []
    for path in road.rglob("*.md"):
        rel = str(path.relative_to(vault_root))
        if not _is_conceptual_roadmap_path(rel):
            continue
        fm, body = _read_note(path)
        if str(fm.get("roadmap_track") or "").lower() == "execution":
            continue
        out.append((path, fm, body))
    return out


def phase_dirs_for_project(vault_root: Path, project_id: str) -> dict[int, Path]:
    road = vault_root / "1-Projects" / project_id / "Roadmap"
    by_num: dict[int, Path] = {}
    if not road.is_dir():
        return by_num
    for child in road.iterdir():
        if not child.is_dir() or not child.name.startswith("Phase-"):
            continue
        m = re.match(r"Phase-(\d+)-", child.name)
        if m:
            by_num[int(m.group(1))] = child
    return by_num


def _subphase_index_parts(idx: str) -> list[int] | None:
    raw = str(idx or "").strip().strip('"')
    if not raw or not re.fullmatch(r"[\d.]+", raw):
        return None
    parts: list[int] = []
    for piece in raw.split("."):
        if not piece.isdigit():
            return None
        parts.append(int(piece))
    return parts or None


def _note_phase_number(fm: dict[str, Any], path: Path) -> int | None:
    parts = _subphase_index_parts(str(fm.get("subphase-index") or ""))
    if parts:
        return parts[0]
    phase_num = fm.get("phase-number")
    if phase_num is not None:
        try:
            return int(phase_num)
        except (TypeError, ValueError):
            pass
    m = re.search(r"Phase-(\d+)-", str(path))
    return int(m.group(1)) if m else None


def _roadmap_level(fm: dict[str, Any], path: Path) -> str:
    level = str(fm.get("roadmap-level") or "").lower().strip()
    if level:
        return level
    parts = _subphase_index_parts(str(fm.get("subphase-index") or ""))
    if not parts:
        return "unknown"
    depth_map = {1: "primary", 2: "secondary", 3: "tertiary", 4: "quaternary"}
    return depth_map.get(len(parts), "deeper")


def _handoff_readiness(fm: dict[str, Any]) -> int | None:
    raw = fm.get("handoff_readiness")
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def _min_body_for_level(gate: dict[str, Any], level: str) -> int:
    chars = gate.get("min_body_chars") or {}
    if isinstance(chars, dict) and level in chars:
        return int(chars[level])
    if isinstance(chars, dict) and "default" in chars:
        return int(chars["default"])
    return 300


def _is_scaffold_only(body: str, fm: dict[str, Any]) -> bool:
    if "#review-needed" in body:
        return True
    if str(fm.get("status") or "").lower() in ("draft", "stub", "scaffold"):
        return True
    if str(fm.get("handoff_readiness") or "").lower() == "partial":
        return True
    unchecked = body.count("- [ ]")
    checked = body.count("- [x]") + body.count("- [X]")
    if unchecked >= 3 and checked == 0:
        return True
    if any(marker in body for marker in _SCAFFOLD_MARKERS) and len(body) < 700:
        return True
    return False


def _passes_nl_checklist(body: str, level: str) -> bool:
    if level == "primary":
        return bool(_NL_SCOPE_RE.search(body) or _NL_BEHAVIOR_RE.search(body))
    return bool(_NL_BEHAVIOR_RE.search(body))


def _note_qualifies(
    fm: dict[str, Any],
    body: str,
    *,
    gate: dict[str, Any],
    level: str | None = None,
    min_readiness: int | None = None,
) -> bool:
    lvl = level or _roadmap_level(fm, Path("."))
    if _is_scaffold_only(body, fm):
        return False
    if len(body) < _min_body_for_level(gate, lvl):
        return False
    if gate.get("require_nl_checklist") and not _passes_nl_checklist(body, lvl):
        return False
    if min_readiness is not None:
        readiness = _handoff_readiness(fm)
        if readiness is None or readiness < min_readiness:
            return False
    return True


def _normalize_completed_phases(raw: Any) -> set[int]:
    out: set[int] = set()
    if not isinstance(raw, list):
        return out
    for item in raw:
        try:
            out.add(int(item))
        except (TypeError, ValueError):
            continue
    return out


def _roadmap_state_terminal(fm: dict[str, Any], gate: dict[str, Any]) -> tuple[bool, str]:
    track = str(fm.get("roadmap_track") or "conceptual").lower()
    if track == "execution":
        return False, "roadmap_track_execution"

    if gate.get("require_roadmap_state_complete"):
        status = str(fm.get("status") or "").lower().strip()
        if status != "complete":
            return False, f"roadmap_state_not_complete:{status or 'missing'}"

    min_phases = int(gate.get("min_phases") or 6)
    try:
        current_phase = int(fm.get("current_phase") or 0)
    except (TypeError, ValueError):
        current_phase = 0
    if current_phase < min_phases:
        return False, f"current_phase_below_{min_phases}:{current_phase}"

    if gate.get("require_completed_phases_1_through_n"):
        done = _normalize_completed_phases(fm.get("completed_phases"))
        missing = [n for n in range(1, min_phases + 1) if n not in done]
        if missing:
            return False, f"completed_phases_missing:{missing[0]}"

    return True, "roadmap_state_terminal"


def _group_notes_by_phase_and_level(
    notes: list[tuple[Path, dict[str, Any], str]],
) -> dict[int, dict[str, list[tuple[Path, dict[str, Any], str]]]]:
    grouped: dict[int, dict[str, list[tuple[Path, dict[str, Any], str]]]] = {}
    for path, fm, body in notes:
        phase = _note_phase_number(fm, path)
        if phase is None:
            continue
        level = _roadmap_level(fm, path)
        grouped.setdefault(phase, {}).setdefault(level, []).append((path, fm, body))
    return grouped


def conceptual_map_complete(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """
    True when the PMG conceptual map is **complete** per factory law — not a deepen floor.

    Matches roadmap.md conceptual ``conceptual_target_reached`` criteria (deterministic subset):
    - ``roadmap-state``: status complete, phases 1..N done, conceptual track
    - Every phase note in tree passes NL + body bar (no ROADMAP_MODE scaffolds)
    - Primary per phase: handoff_readiness floor
    - Structural: secondary under each primary, tertiary under each secondary
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return False, "no_project_id"

    if not roadmap_tree_complete(vault_root, pid):
        return False, "roadmap_tree_incomplete"

    gate = load_conceptual_gate_config(vault_root)
    min_phases = int(gate.get("min_phases") or 6)
    min_primary_readiness = int(gate.get("min_handoff_readiness_primary") or 75)

    state_fm = _read_state_frontmatter(vault_root, pid)
    ok, reason = _roadmap_state_terminal(state_fm, gate)
    if not ok:
        return False, reason

    phase_dirs = phase_dirs_for_project(vault_root, pid)
    for n in range(1, min_phases + 1):
        if n not in phase_dirs:
            return False, f"conceptual_phases_missing:{n}"

    all_notes = iter_conceptual_roadmap_notes(vault_root, pid)
    grouped = _group_notes_by_phase_and_level(all_notes)
    traversal_cfg = load_deepen_traversal_config(vault_root)
    subphase_indexes = (
        collect_subphase_indexes(vault_root, pid)
        if traversal_cfg.get("reject_oversized_without_children")
        else []
    )

    for phase_num in range(1, min_phases + 1):
        levels = grouped.get(phase_num) or {}
        primaries = levels.get("primary") or []
        if not primaries:
            return False, f"conceptual_primary_missing:phase_{phase_num}"

        qualified_primaries = [
            (p, fm, b)
            for p, fm, b in primaries
            if _note_qualifies(fm, b, gate=gate, level="primary", min_readiness=min_primary_readiness)
        ]
        if not qualified_primaries:
            return False, f"conceptual_primary_incomplete:phase_{phase_num}"

        if gate.get("require_secondary_per_primary"):
            secondaries = levels.get("secondary") or []
            qual_sec = [
                (p, fm, b)
                for p, fm, b in secondaries
                if _note_qualifies(fm, b, gate=gate, level="secondary")
            ]
            if len(qual_sec) < len(primaries):
                return False, f"conceptual_secondary_tree_incomplete:phase_{phase_num}"

            if gate.get("require_tertiary_per_secondary"):
                tertiaries = levels.get("tertiary") or []
                qual_ter = [
                    (p, fm, b)
                    for p, fm, b in tertiaries
                    if _note_qualifies(fm, b, gate=gate, level="tertiary")
                ]
                if len(qual_ter) < len(qual_sec):
                    return False, f"conceptual_tertiary_tree_incomplete:phase_{phase_num}"

        for level_name in ("secondary", "tertiary", "quaternary", "deeper"):
            for path, fm, body in levels.get(level_name) or []:
                if not _note_qualifies(fm, body, gate=gate, level=level_name):
                    rel = path.relative_to(vault_root)
                    return False, f"conceptual_note_incomplete:{rel}"
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
                        return False, oreason

    return True, "conceptual_map_complete"


def conceptual_factory_handoff_ready(
    vault_root: Path,
    project_id: str,
    *,
    mint_batch: str | None = None,
    goal_packet: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    """Hard gate before catalog mint / L5 — feed gate or legacy full-tree per config mode."""
    gate = load_conceptual_gate_config(vault_root)
    mode = str(gate.get("mode") or "factory_feed_ready").lower().strip()
    if mode == "factory_feed_ready":
        from .conceptual_factory_feed import conceptual_factory_feed_ready

        return conceptual_factory_feed_ready(
            vault_root,
            project_id,
            mint_batch=mint_batch,
            goal_packet=goal_packet,
        )
    return conceptual_map_complete(vault_root, project_id)


def conceptual_track_ready(
    vault_root: Path,
    project_id: str,
    *,
    mint_batch: str | None = None,
    goal_packet: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    """Factory gate alias — feed-ready or legacy complete map; not execution, not L5."""
    return conceptual_factory_handoff_ready(
        vault_root,
        project_id,
        mint_batch=mint_batch,
        goal_packet=goal_packet,
    )


def conceptual_notes_for_phase(
    vault_root: Path,
    project_id: str,
    phase_num: int,
) -> list[tuple[Path, dict[str, Any], str]]:
    phase_dir = phase_dirs_for_project(vault_root, project_id).get(phase_num)
    if phase_dir is None:
        return []
    notes: list[tuple[Path, dict[str, Any], str]] = []
    for path in phase_dir.rglob("*.md"):
        rel = str(path.relative_to(vault_root)).replace("\\", "/")
        if not _is_conceptual_roadmap_path(rel):
            continue
        fm, body = _read_note(path)
        if str(fm.get("roadmap_track") or "").lower() == "execution":
            continue
        if _note_phase_number(fm, path) == phase_num:
            notes.append((path, fm, body))
    return notes


def roadmap_tree_complete(vault_root: Path, project_id: str) -> bool:
    """True when ROADMAP MODE setup artifacts exist (master + phase folders + MOC)."""
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return False
    project_root = vault_root / "1-Projects" / pid
    road = project_root / "Roadmap"
    if not road.is_dir():
        return False
    phase_dirs = [p for p in road.iterdir() if p.is_dir() and p.name.startswith("Phase-")]
    moc = list(project_root.glob("*Roadmap-MOC*")) + list(road.glob("*Roadmap-MOC*"))
    masters = [p for p in road.glob("*.md") if "Roadmap" in p.name and "MOC" not in p.name]
    return len(phase_dirs) >= 6 and bool(moc) and bool(masters)


def conceptual_track_substantive(vault_root: Path, project_id: str) -> bool:
    ok, _ = conceptual_map_complete(vault_root, project_id)
    return ok
