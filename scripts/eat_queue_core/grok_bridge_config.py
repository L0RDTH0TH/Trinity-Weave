"""Grok bridge config from live Second-Brain-Config."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .live_config import load_live_config
from .weave_public_publish import get_weave_publish_config

DEFAULT_PILOT_PROJECT_ID = "godot-genesis-mythos-master"
DEFAULT_EXPORT_ROOT = "/home/darth/Documents/trinity-weave-export"
DEFAULT_REMOTE_URL = "https://github.com/L0RDTH0TH/Trinity-Weave.git"
DEFAULT_MAIN_BRANCH = "main"
DEFAULT_PROJECT_BRANCH_PREFIX = "project/"
GMMR_EXPORT_ROOT = "/home/darth/Documents/gmm-roadmap-export"


def get_grok_bridge_config(merged: dict[str, Any] | None = None) -> dict[str, Any]:
    raw = merged.get("grok_bridge") if isinstance(merged, dict) else None
    return raw if isinstance(raw, dict) else {}


def resolve_grok_bridge(merged: dict[str, Any]) -> dict[str, Any]:
    gb = get_grok_bridge_config(merged)
    wp = get_weave_publish_config(merged)
    github = gb.get("github") if isinstance(gb.get("github"), dict) else {}
    push_economy = gb.get("push_economy") if isinstance(gb.get("push_economy"), dict) else {}

    export_root_s = github.get("export_repo_root") or wp.get("export_repo_root") or DEFAULT_EXPORT_ROOT
    remote_url = str(github.get("remote_url") or wp.get("remote_url") or DEFAULT_REMOTE_URL)
    pilot = str(gb.get("pilot_project_id") or DEFAULT_PILOT_PROJECT_ID)

    return {
        "enabled": bool(gb.get("enabled", True)),
        "pilot_project_id": pilot,
        "export_repo_root": str(Path(str(export_root_s)).expanduser().resolve()),
        "remote_url": remote_url,
        "main_branch": str(github.get("main_branch") or wp.get("branch") or DEFAULT_MAIN_BRANCH),
        "project_branch_prefix": str(github.get("project_branch_prefix") or DEFAULT_PROJECT_BRANCH_PREFIX),
        "project_branch": f"{github.get('project_branch_prefix') or DEFAULT_PROJECT_BRANCH_PREFIX}{pilot}".rstrip("/"),
        "ignore_gmmr_for_bridge": bool(gb.get("ignore_gmmr_for_bridge", True)),
        "gmmr_zero_bridge_budget": bool(gb.get("gmmr_zero_bridge_budget", True)),
        "gmmr_export_root": GMMR_EXPORT_ROOT,
        "max_nodes_per_fulfill": int(gb.get("max_nodes_per_fulfill") or 5),
        "max_chars_per_node": int(gb.get("max_chars_per_node") or 2000),
        "deny_globs": list(gb.get("deny_globs") or []),
        "push_economy": {
            "respect_git_push_enabled": bool(push_economy.get("respect_git_push_enabled", True)),
            "push_cooldown_hours": float(push_economy.get("push_cooldown_hours") or 24),
            "max_pushes_per_day": int(push_economy.get("max_pushes_per_day") or 1),
            "max_pushes_per_week": int(push_economy.get("max_pushes_per_week") or 5),
            "trinity_share_of_daily_pushes": int(push_economy.get("trinity_share_of_daily_pushes") or 1),
            "priority_order": list(push_economy.get("priority_order") or ["trinity_main", "project_pilot"]),
            "allow_force_push_override": bool(push_economy.get("allow_force_push_override", True)),
        },
    }


def load_grok_bridge(vault_root: Path, config_path: Path) -> dict[str, Any]:
    merged = load_live_config(vault_root, config_path=config_path)
    return resolve_grok_bridge(merged)


def project_dir(vault_root: Path, project_id: str) -> Path:
    return vault_root / "1-Projects" / project_id


def project_branch_name(cfg: dict[str, Any], project_id: str | None = None) -> str:
    pid = project_id or cfg["pilot_project_id"]
    prefix = cfg.get("project_branch_prefix") or DEFAULT_PROJECT_BRANCH_PREFIX
    if not prefix.endswith("/"):
        prefix = prefix + "/"
    return f"{prefix}{pid}"
