"""Milestone charter for Track C implementation slices."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ..goal_authority_io import goal_authority_path_for_lane

MILESTONE_ORDER = ("M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8")

_DEFAULT_CHARTER: dict[str, dict[str, Any]] = {
    "M1": {
        "kind": "vault_doc",
        "requires_mcp": False,
        "requires_agent": False,
        "done_when": "Repo link documented in demo spec + prototype history",
        "target_files": [],
        "verify": [],
    },
    "M2": {
        "kind": "repo_build",
        "requires_mcp": True,
        "requires_agent": True,
        "done_when": "WorldBlockout.tscn — floor, walls, spawn, lighting",
        "target_files": ["WorldBlockout.tscn"],
        "verify": ["dotnet_build", "file_exists:WorldBlockout.tscn"],
    },
    "M3": {
        "kind": "repo_build",
        "requires_mcp": True,
        "requires_agent": True,
        "done_when": "PlayerFP.tscn — WASD + mouse look",
        "target_files": ["PlayerFP.tscn"],
        "verify": ["dotnet_build", "file_exists:PlayerFP.tscn"],
    },
    "M4": {
        "kind": "repo_build",
        "requires_mcp": True,
        "requires_agent": True,
        "done_when": "DMCameraRig.tscn — toggle FP ↔ DM cam",
        "target_files": ["DMCameraRig.tscn"],
        "verify": ["dotnet_build", "file_exists:DMCameraRig.tscn"],
    },
    "M5": {
        "kind": "repo_build",
        "requires_mcp": True,
        "requires_agent": True,
        "done_when": "IntentEnvelope → visible feedback",
        "target_files": [],
        "verify": ["dotnet_build"],
    },
    "M6": {
        "kind": "repo_build",
        "requires_mcp": True,
        "requires_agent": True,
        "done_when": "One tick-driven sim change",
        "target_files": [],
        "verify": ["dotnet_build"],
    },
    "M7": {
        "kind": "repo_build",
        "requires_mcp": True,
        "requires_agent": True,
        "done_when": "One rule primitive → HUD/debug",
        "target_files": [],
        "verify": ["dotnet_build"],
    },
    "M8": {
        "kind": "playtest_gate",
        "requires_mcp": True,
        "requires_agent": True,
        "done_when": "30-min playtest script passable",
        "target_files": [],
        "verify": ["dotnet_build", "godot_headless_smoke"],
    },
}


def charter_path(vault_root: Path, lane: str) -> Path:
    return goal_authority_path_for_lane(vault_root, lane).parent / "milestone-charter.yaml"


def load_milestone_charter(vault_root: Path, lane: str) -> dict[str, dict[str, Any]]:
    """Load per-lane charter YAML; fall back to embedded defaults."""
    p = charter_path(vault_root, lane)
    if not p.is_file():
        return dict(_DEFAULT_CHARTER)
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    out = dict(_DEFAULT_CHARTER)
    for mid in MILESTONE_ORDER[1:]:
        block = raw.get(mid)
        if isinstance(block, dict):
            out[mid] = {**out.get(mid, {}), **block}
    return out


def get_milestone_spec(
    vault_root: Path, lane: str, milestone_id: str
) -> dict[str, Any] | None:
    mid = str(milestone_id or "").strip().upper()
    if mid not in MILESTONE_ORDER:
        return None
    charter = load_milestone_charter(vault_root, lane)
    return charter.get(mid)


def next_milestone_id(current: str) -> str | None:
    cur = str(current or "").strip().upper()
    try:
        idx = MILESTONE_ORDER.index(cur)
    except ValueError:
        return None
    if idx + 1 >= len(MILESTONE_ORDER):
        return None
    return MILESTONE_ORDER[idx + 1]
