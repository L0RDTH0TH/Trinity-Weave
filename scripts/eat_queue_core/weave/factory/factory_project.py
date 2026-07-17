"""Factory project manifest — bootstrap for vault_roadmap feed (replaces alpha-queue spine)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .factory_output_gate import parse_factory_orchestrator_yaml

DEFAULT_PROJECT_ID = "godot-genesis-mythos-master"
LEGACY_ALPHA_QUEUE_REL = f"1-Projects/{DEFAULT_PROJECT_ID}/Factory-DRB/alpha-factory-queue.yaml"


def factory_project_rel(project_id: str) -> str:
    return f"1-Projects/{project_id}/Factory-DRB/factory-project.yaml"


def load_factory_project(
    vault_root: Path,
    project_id: str | None = None,
    *,
    legacy_alpha_rel: str | None = None,
) -> dict[str, Any]:
    """
    Merge factory-project.yaml with Second-Brain-Config factory_orchestrator block.

    Legacy alpha-factory-queue.yaml is used only to fill missing fields when manifest
    is absent (migration shim).
    """
    vault_root = vault_root.resolve()
    cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
    pid = str(project_id or cfg.get("project_id") or DEFAULT_PROJECT_ID)

    manifest: dict[str, Any] = {}
    manifest_path = vault_root / factory_project_rel(pid)
    if manifest_path.is_file():
        raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        if isinstance(raw, dict):
            manifest = raw

    legacy_rel = legacy_alpha_rel or str(
        manifest.get("legacy_alpha_queue_ref") or LEGACY_ALPHA_QUEUE_REL
    )
    legacy: dict[str, Any] = {}
    if legacy_rel:
        from .factory_orchestrator import load_alpha_queue

        legacy = load_alpha_queue(vault_root, legacy_rel)

    def _pick(*keys: str, default: Any = "") -> Any:
        for source in (manifest, cfg, legacy):
            if not isinstance(source, dict):
                continue
            for key in keys:
                val = source.get(key)
                if val is not None and val != "":
                    return val
        return default

    bootstrap_raw = manifest.get("factory_bootstrap")
    if not isinstance(bootstrap_raw, dict) and isinstance(legacy.get("factory_bootstrap"), dict):
        bootstrap_raw = legacy["factory_bootstrap"]

    bootstrap = {
        "gates_before_slices": True,
        "bootstrap_waiver": False,
        "require_weave_track_coupled": True,
    }
    if isinstance(bootstrap_raw, dict):
        bootstrap.update(bootstrap_raw)

    shortcuts = manifest.get("forbidden_shortcuts")
    if not isinstance(shortcuts, list):
        shortcuts = legacy.get("forbidden_shortcuts") or []

    return {
        "schema_version": manifest.get("schema_version") or 1,
        "project_id": pid,
        "game_repo_path": str(_pick("game_repo_path")).strip("/"),
        "archive_repo_path": str(_pick("archive_repo_path")).strip("/"),
        "execution_roadmap_ref": str(_pick("execution_roadmap_ref")),
        "release_tier": str(_pick("release_tier", default="closed_alpha")),
        "feed_authority": str(
            manifest.get("feed_authority") or cfg.get("feed_authority") or "vault_roadmap"
        ),
        "factory_bootstrap": bootstrap,
        "forbidden_shortcuts": list(shortcuts),
        "legacy_alpha_queue_ref": legacy_rel,
        "manifest_path": str(manifest_path.relative_to(vault_root)) if manifest_path.is_file() else "",
    }
