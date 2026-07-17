"""Shared I/O for User-Story track artifacts."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from ..factory.factory_output_gate import parse_factory_orchestrator_yaml

DEFAULT_PROJECT_ID = "godot-genesis-mythos-master"
DEFAULT_BUDGET_REL = "Roadmap/User-Story/slice-depth-budget.json"
DEFAULT_CATALOG_REL = "Roadmap/User-Story/slice-catalog.yaml"
DEFAULT_LANE_MAP_REL = "Factory-DRB/lane-map.yaml"
DEFAULT_STATE_REL = "Roadmap/User-Story/user-story-state.md"
DEFAULT_BEATS_DIR = "Roadmap/User-Story/beats"
DEFAULT_INFLUENCE_REL = "Roadmap/User-Story/influence-deck.md"
DEFAULT_DEPTH_CHARTER_REL = "Roadmap/User-Story/depth-semantics.md"
DEFAULT_SCOPES_DIR = "Roadmap/User-Story/scopes"


def project_root(vault_root: Path, project_id: str) -> Path:
    return vault_root / "1-Projects" / project_id


def ensure_user_story_state(vault_root: Path, project_id: str) -> Path:
    """Create Roadmap/User-Story/user-story-state.md for greenfield factory runs."""
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        raise ValueError("project_id required")
    state_path = user_story_paths(vault_root, pid)["state"]
    if state_path.is_file():
        return state_path
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        f"---\n"
        f"roadmap_track: user_story\n"
        f"rollout_version: 1\n"
        f"depth_charter_version: 1\n"
        f"---\n\n"
        f"# User story — {pid}\n\n"
        f"Greenfield factory state (auto-bootstrap).\n",
        encoding="utf-8",
    )
    return state_path


def user_story_paths(vault_root: Path, project_id: str) -> dict[str, Path]:
    cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
    us = cfg.get("user_story") if isinstance(cfg.get("user_story"), dict) else {}
    vr = cfg.get("vault_roadmap") if isinstance(cfg.get("vault_roadmap"), dict) else {}
    merged = {**vr, **us}
    base = project_root(vault_root, project_id)
    return {
        "budget": base / str(merged.get("budget_rel") or DEFAULT_BUDGET_REL),
        "catalog": base / str(merged.get("catalog_rel") or DEFAULT_CATALOG_REL),
        "lane_map": base / str(merged.get("lane_map_rel") or DEFAULT_LANE_MAP_REL),
        "state": base / str(merged.get("state_rel") or DEFAULT_STATE_REL),
        "beats_dir": base / str(merged.get("beats_dir") or DEFAULT_BEATS_DIR),
        "influence": base / str(merged.get("influence_rel") or DEFAULT_INFLUENCE_REL),
        "depth_charter": base / str(merged.get("depth_charter_rel") or DEFAULT_DEPTH_CHARTER_REL),
        "scopes_dir": base / str(merged.get("scopes_dir") or DEFAULT_SCOPES_DIR),
    }


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def save_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def parse_state_frontmatter(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    block = yaml.safe_load(m.group(1)) or {}
    return block if isinstance(block, dict) else {}


def catalog_rows_by_id(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = catalog.get("rows") or []
    out: dict[str, dict[str, Any]] = {}
    if not isinstance(rows, list):
        return out
    for row in rows:
        if isinstance(row, dict) and row.get("id"):
            out[str(row["id"])] = row
    return out


def normalize_pin(pin: str) -> str:
    s = pin.strip()
    s = re.sub(r"^\[\[|\]\]$", "", s)
    return s.strip()
