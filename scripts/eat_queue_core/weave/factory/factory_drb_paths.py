"""Project-scoped Factory-DRB path resolver (general-purpose factory)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .factory_project import DEFAULT_PROJECT_ID, load_factory_project

DRB_ARTIFACTS: dict[str, str] = {
    "tech_stack_manifest": "Tech-Stack-Manifest-v1.yaml",
    "stack_domain_registry": "Stack-Domain-Registry-v1.yaml",
    "factory_project": "factory-project.yaml",
    "lane_map": "lane-map.yaml",
    "product_bom": "product-bom.yaml",
    "factory_zones": "FACTORY_ZONES.yaml",
    "stack_charter": "Stack-Charter-v0.md",
    "spine_host": "Spine-Host-Contract-v0.md",
    "constitution": "Implementation-Factory-Constitution.md",
    "usability_nav": "usability-navigation-v1.md",
    "usability_launch": "usability-launch-v1.md",
    "gate_precedence": "Gate-Precedence-Conflict-Doctrine-v1.md",
    "visual_style": "Visual-Style-Charter-v1.md",
    "closed_alpha_release": "Release-Definitions/closed-alpha-v1.md",
}


def resolve_project_id(vault_root: Path, project_id: str | None = None) -> str:
    if project_id:
        return project_id.strip()
    boot = load_factory_project(vault_root, None)
    return str(boot.get("project_id") or DEFAULT_PROJECT_ID)


def factory_drb_dir(vault_root: Path, project_id: str | None = None) -> Path:
    pid = resolve_project_id(vault_root, project_id)
    return vault_root / "1-Projects" / pid / "Factory-DRB"


def drb_artifact_path(
    vault_root: Path,
    artifact_key: str,
    *,
    project_id: str | None = None,
) -> Path:
    name = DRB_ARTIFACTS.get(artifact_key)
    if not name:
        raise KeyError(f"unknown_drb_artifact:{artifact_key}")
    return factory_drb_dir(vault_root, project_id) / name


def tech_stack_manifest_path(vault_root: Path, project_id: str | None = None) -> Path:
    return drb_artifact_path(vault_root, "tech_stack_manifest", project_id=project_id)


def stack_domain_registry_path(vault_root: Path, project_id: str | None = None) -> Path:
    return drb_artifact_path(vault_root, "stack_domain_registry", project_id=project_id)


def resolve_game_repo_path(vault_root: Path, project_id: str | None = None) -> str:
    """Game repo relative path from factory-project.yaml or tech stack manifest."""
    import yaml

    boot = load_factory_project(vault_root, project_id)
    rel = str(boot.get("game_repo_path") or "").strip("/")
    if rel:
        return rel
    manifest_path = tech_stack_manifest_path(vault_root, project_id)
    if manifest_path.is_file():
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict) and data.get("game_repo_path"):
            return str(data["game_repo_path"]).strip("/")
    return "game"


def scaffold_factory_project(
    vault_root: Path,
    *,
    project_id: str,
    game_repo_path: str,
    release_tier: str = "closed_alpha",
) -> dict[str, Any]:
    """Create minimal Factory-DRB + factory-project.yaml for a new project_id."""
    import yaml

    vault_root = vault_root.resolve()
    drb = factory_drb_dir(vault_root, project_id)
    drb.mkdir(parents=True, exist_ok=True)
    (drb / "Release-Definitions").mkdir(parents=True, exist_ok=True)

    manifest_body = {
        "schema_version": 1,
        "project_id": project_id,
        "game_repo_path": game_repo_path.strip("/"),
        "operator_stack_baseline_vetted": False,
        "pipeline_certified": False,
        "rows": [],
    }
    (drb / "Tech-Stack-Manifest-v1.yaml").write_text(
        yaml.dump(manifest_body, sort_keys=False),
        encoding="utf-8",
    )
    (drb / "Stack-Domain-Registry-v1.yaml").write_text(
        yaml.dump({"domains": [], "interop_gate_required": False}),
        encoding="utf-8",
    )
    (drb / "lane-map.yaml").write_text(
        yaml.dump({"default_lanes": ["module", "presentation"]}),
        encoding="utf-8",
    )
    (drb / "factory-project.yaml").write_text(
        yaml.dump(
            {
                "schema_version": 1,
                "project_id": project_id,
                "game_repo_path": game_repo_path.strip("/"),
                "feed_authority": "vault_roadmap",
                "release_tier": release_tier,
                "factory_bootstrap": {
                    "gates_before_slices": True,
                    "bootstrap_waiver": False,
                    "require_weave_track_coupled": True,
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (drb / "product-bom.yaml").write_text(
        yaml.dump(
            {
                "versioning": {
                    "bom_schema_version": 2,
                    "bom_revision": 1,
                    "product_version": release_tier,
                },
                "product_id": project_id,
            }
        ),
        encoding="utf-8",
    )
    (drb / "Release-Definitions" / f"{release_tier}.md").write_text(
        f"---\ntitle: {release_tier}\ngame_repo: {game_repo_path.strip('/')}\n---\n",
        encoding="utf-8",
    )
    repo = vault_root / game_repo_path.strip("/")
    repo.mkdir(parents=True, exist_ok=True)
    weave = repo / ".technical" / "weave"
    weave.mkdir(parents=True, exist_ok=True)
    (weave / "weave_track.yaml").write_text(
        yaml.dump({"track_status": "coupled", "schema_version": 1}),
        encoding="utf-8",
    )
    return {
        "ok": True,
        "project_id": project_id,
        "drb_dir": str(drb.relative_to(vault_root)),
        "game_repo_path": game_repo_path.strip("/"),
    }
