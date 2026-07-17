"""Product weave_track.yaml — coupled / disconnected harness behavior."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

MANIFEST_REL = "1-Projects/godot-genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml"
DEFAULT_GAME_REPO_REL = "5-Attachments/Code-Repos/genesis-mythos-demo"

TRACK_COUPLED = "coupled"
TRACK_DISCONNECTED = "disconnected"
WEAVE_TRACK_REL = ".technical/weave/weave_track.yaml"


def _game_repo(vault_root: Path, project_id: str | None = None) -> Path:
    from .factory_drb_paths import resolve_game_repo_path

    rel = resolve_game_repo_path(vault_root, project_id)
    return vault_root / rel


def weave_track_path(vault_root: Path) -> Path:
    return _game_repo(vault_root) / WEAVE_TRACK_REL


def load_weave_track(vault_root: Path) -> dict[str, Any]:
    path = weave_track_path(vault_root)
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def track_status(vault_root: Path) -> str:
    return str(load_weave_track(vault_root).get("track_status") or TRACK_DISCONNECTED)


def is_track_coupled(vault_root: Path) -> bool:
    return track_status(vault_root) == TRACK_COUPLED


def set_track_status(vault_root: Path, status: str, *, reason: str = "") -> Path:
    """Update track_status on product repo weave_track.yaml."""
    if status not in (TRACK_COUPLED, TRACK_DISCONNECTED):
        raise ValueError(f"invalid_track_status:{status}")
    path = weave_track_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = load_weave_track(vault_root) if path.is_file() else {}
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data["track_status"] = status
    data["track_status_updated_at"] = stamp
    if reason:
        data["track_status_reason"] = reason
    if "schema_version" not in data:
        data.setdefault("schema_version", 1)
    path.write_text(yaml.dump(data, sort_keys=False), encoding="utf-8")
    return path


def disconnect_track(vault_root: Path, *, reason: str) -> Path:
    return set_track_status(vault_root, TRACK_DISCONNECTED, reason=reason)


def reconnect_track(vault_root: Path, *, reason: str = "operator_reconnect") -> tuple[bool, str]:
    """Reconnect only when product welds listed in weave_track exist."""
    data = load_weave_track(vault_root)
    repo = _game_repo(vault_root)
    missing: list[str] = []
    for rel in data.get("product_welds") or []:
        if not (repo / str(rel)).exists():
            missing.append(str(rel))
    if missing:
        return False, f"missing_product_welds:{missing[:5]}"
    set_track_status(vault_root, TRACK_COUPLED, reason=reason)
    return True, "reconnected"


def factory_dispatch_allowed(vault_root: Path) -> tuple[bool, str]:
    """Factory belt requires coupled product track unless explicitly disconnected with policy."""
    data = load_weave_track(vault_root)
    if not data:
        return False, "weave_track_missing"
    status = str(data.get("track_status") or TRACK_DISCONNECTED)
    if status == TRACK_COUPLED:
        return True, "track_coupled"
    policy = str(data.get("disconnect_policy") or "")
    if status == TRACK_DISCONNECTED and policy == "welds_travel_with_product_track":
        return False, "track_disconnected_factory_blocked"
    return False, f"track_status:{status}"
