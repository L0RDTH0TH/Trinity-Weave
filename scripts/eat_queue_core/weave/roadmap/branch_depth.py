"""Depth-first branch helpers — shared by roadmap deepen policy and conceptual gate anti-bloat."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ...merged_config import load_merged_yaml_blocks

DEFAULT_DEEPEN_TRAVERSAL: dict[str, Any] = {
    "deepen_traversal": "depth_first",
    "child_before_sibling_exit": True,
    "reject_oversized_without_children": True,
    "max_note_body_chars": {
        "primary": 2000,
        "secondary": 1400,
        "tertiary": 1200,
        "quaternary": 900,
        "task": 900,
        "default": 1200,
    },
    "split_warrant": {
        "min_edge_case_bullets": 3,
        "min_actor_flow_mentions": 2,
        "min_open_questions": 3,
    },
}

_EDGE_CASE_HEADING_RE = re.compile(r"(?im)^#{1,3}\s*edge\s*cases?\s*$")
_BEHAVIOR_HEADING_RE = re.compile(r"(?im)^#{1,3}\s*behavior\s*$")
_OPEN_QUESTIONS_HEADING_RE = re.compile(r"(?im)^#{1,3}\s*open\s*questions?\s*$")
_BULLET_RE = re.compile(r"(?m)^\s*[-*]\s+.+")
_ACTOR_FLOW_RE = re.compile(
    r"(?i)(player|dm|system|engine|observer|ui|server|client)\s*(→|->|:|,|\s+when|\s+if)"
)


def load_deepen_traversal_config(vault_root: Path) -> dict[str, Any]:
    cfg: dict[str, Any] = {}
    for key, val in DEFAULT_DEEPEN_TRAVERSAL.items():
        if isinstance(val, dict):
            cfg[key] = dict(val)
        else:
            cfg[key] = val
    try:
        blocks = load_merged_yaml_blocks(vault_root)
        roadmap = blocks.get("roadmap")
        if isinstance(roadmap, dict):
            for key, val in roadmap.items():
                if val is None:
                    continue
                if key in ("max_note_body_chars", "split_warrant") and isinstance(val, dict):
                    merged = dict(cfg.get(key) or {})
                    merged.update(val)
                    cfg[key] = merged
                elif key in DEFAULT_DEEPEN_TRAVERSAL:
                    cfg[key] = val
    except (ImportError, OSError, TypeError, ValueError):
        pass
    return cfg


def subphase_index_parts(idx: str) -> list[int] | None:
    raw = str(idx or "").strip().strip('"')
    if not raw or not re.fullmatch(r"[\d.]+", raw):
        return None
    parts: list[int] = []
    for piece in raw.split("."):
        if not piece.isdigit():
            return None
        parts.append(int(piece))
    return parts or None


def subphase_index_depth(idx: str) -> int:
    parts = subphase_index_parts(idx)
    return len(parts) if parts else 0


def _roadmap_level(fm: dict[str, Any], subphase_index: str) -> str:
    level = str(fm.get("roadmap-level") or "").lower().strip()
    if level:
        return level
    depth_map = {1: "primary", 2: "secondary", 3: "tertiary", 4: "quaternary"}
    depth = subphase_index_depth(subphase_index)
    return depth_map.get(depth, "deeper")


def _max_body_for_level(cfg: dict[str, Any], level: str) -> int:
    caps = cfg.get("max_note_body_chars") or {}
    if isinstance(caps, dict) and level in caps:
        return int(caps[level])
    if isinstance(caps, dict) and "default" in caps:
        return int(caps["default"])
    return 1200


def _section_body(body: str, heading_re: re.Pattern[str]) -> str:
    match = heading_re.search(body)
    if not match:
        return ""
    start = match.end()
    rest = body[start:]
    next_heading = re.search(r"(?m)^#{1,3}\s+\S", rest)
    chunk = rest[: next_heading.start()] if next_heading else rest
    return chunk.strip()


def _count_bullets(text: str) -> int:
    return len(_BULLET_RE.findall(text or ""))


def _count_actor_flows(behavior_text: str) -> int:
    return len(_ACTOR_FLOW_RE.findall(behavior_text or ""))


def has_child_notes(
    notes: list[tuple[str, dict[str, Any]]],
    parent_index: str,
) -> bool:
    """True when any note's subphase-index is a strict child of parent_index."""
    parent = str(parent_index or "").strip().strip('"')
    if not parent:
        return False
    prefix = f"{parent}."
    for idx, _fm in notes:
        child = str(idx or "").strip().strip('"')
        if child.startswith(prefix) and subphase_index_depth(child) > subphase_index_depth(parent):
            return True
    return False


def branch_split_warrant(
    fm: dict[str, Any],
    body: str,
    *,
    cfg: dict[str, Any] | None = None,
    track: str = "conceptual",
) -> tuple[bool, str]:
    """
    True when this note should split into child files before sibling exit.

    track is reserved for future execution-specific thresholds; both tracks share
    the same heuristics today.
    """
    _ = track
    cfg = cfg or DEFAULT_DEEPEN_TRAVERSAL
    sub_idx = str(fm.get("subphase-index") or "")
    level = _roadmap_level(fm, sub_idx)
    body_stripped = (body or "").strip()
    body_len = len(body_stripped)

    max_chars = _max_body_for_level(cfg, level)
    if body_len > max_chars:
        return True, f"body_over_cap:{body_len}>{max_chars}"

    split = cfg.get("split_warrant") or {}
    min_edges = int(split.get("min_edge_case_bullets") or 3)
    min_flows = int(split.get("min_actor_flow_mentions") or 2)
    min_open = int(split.get("min_open_questions") or 3)

    edge_section = _section_body(body_stripped, _EDGE_CASE_HEADING_RE)
    if _count_bullets(edge_section) >= min_edges:
        return True, "edge_case_bullets"

    behavior_section = _section_body(body_stripped, _BEHAVIOR_HEADING_RE)
    if _count_actor_flows(behavior_section) >= min_flows:
        return True, "actor_flows"

    open_section = _section_body(body_stripped, _OPEN_QUESTIONS_HEADING_RE)
    open_bullets = _count_bullets(open_section)
    if open_bullets >= min_open:
        return True, "open_questions"

    return False, ""


def oversized_note_without_children(
    vault_root: Path,
    project_id: str,
    path: Path,
    fm: dict[str, Any],
    body: str,
    *,
    sibling_indexes: list[tuple[str, dict[str, Any]]] | None = None,
    cfg: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    """Gate helper: note exceeds size cap and split warrant fired but no child notes exist."""
    cfg = cfg or load_deepen_traversal_config(vault_root)
    if not cfg.get("reject_oversized_without_children"):
        return False, ""

    sub_idx = str(fm.get("subphase-index") or "")
    level = _roadmap_level(fm, sub_idx)
    body_len = len((body or "").strip())
    max_chars = _max_body_for_level(cfg, level)
    if body_len <= max_chars:
        return False, ""

    warrant, reason = branch_split_warrant(fm, body, cfg=cfg)
    if not warrant:
        return False, ""

    if sibling_indexes is None:
        sibling_indexes = _collect_subphase_indexes(vault_root, project_id)

    if has_child_notes(sibling_indexes, sub_idx):
        return False, ""

    rel = path.name
    try:
        rel = str(path.relative_to(vault_root))
    except ValueError:
        pass
    return True, f"conceptual_note_oversized:{rel}:{reason}"


def collect_subphase_indexes(
    vault_root: Path,
    project_id: str,
) -> list[tuple[str, dict[str, Any]]]:
    """Subphase-index list under Roadmap/ for child detection."""
    return _collect_subphase_indexes(vault_root, project_id)


def _collect_subphase_indexes(
    vault_root: Path,
    project_id: str,
) -> list[tuple[str, dict[str, Any]]]:
    """Lightweight index list for child detection under Roadmap/."""
    import yaml

    road = vault_root / "1-Projects" / project_id / "Roadmap"
    if not road.is_dir():
        return []
    out: list[tuple[str, dict[str, Any]]] = []
    for path in road.rglob("*.md"):
        rel = str(path).replace("\\", "/")
        if any(
            part in rel
            for part in (
                "/Execution/",
                "/Versions/",
                "/.snapshots/",
                "/User-Story/",
                "/Conceptual-Decision-Records/",
                "/Conceptual-Amendments/",
            )
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 4)
        if end < 0:
            continue
        fm = yaml.safe_load(text[4:end]) or {}
        if not isinstance(fm, dict):
            continue
        idx = str(fm.get("subphase-index") or "").strip()
        if idx:
            out.append((idx, fm))
    return out


def branch_closed_for_exit(
    fm: dict[str, Any],
    body: str,
    *,
    sibling_indexes: list[tuple[str, dict[str, Any]]],
    cfg: dict[str, Any] | None = None,
    track: str = "conceptual",
) -> tuple[bool, str]:
    """
    Slice-exit helper: branch may advance to sibling only when closed.

    Closed = no split warrant, or warrant satisfied by existing children.
    """
    cfg = cfg or DEFAULT_DEEPEN_TRAVERSAL
    if cfg.get("deepen_traversal") != "depth_first":
        return True, "breadth_mode"

    sub_idx = str(fm.get("subphase-index") or "")
    warrant, reason = branch_split_warrant(fm, body, cfg=cfg, track=track)
    if not warrant:
        return True, "no_split_warrant"

    if has_child_notes(sibling_indexes, sub_idx):
        return True, "children_present"

    if cfg.get("child_before_sibling_exit"):
        return False, f"branch_open:{reason}"
    return True, "child_exit_disabled"
