"""Project-scoped Factory-DRB path resolver (general-purpose factory)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .project_identity import (
    ProjectIdMissingError,
    resolve_project_id,
)

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

__all__ = [
    "DRB_ARTIFACTS",
    "ProjectIdMissingError",
    "drb_artifact_path",
    "factory_drb_dir",
    "resolve_game_repo_path",
    "resolve_project_id",
    "scaffold_factory_project",
    "stack_domain_registry_path",
    "tech_stack_manifest_path",
]


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
    """Game repo relative path — sole source identity.yaml via bindings (no silent default)."""
    from .bindings import game_repo_path as bind_game_repo

    pid = resolve_project_id(vault_root, project_id)
    return bind_game_repo(vault_root, pid)


def scaffold_factory_project(
    vault_root: Path,
    *,
    project_id: str,
    game_repo_path: str,
    release_tier: str = "",
) -> dict[str, Any]:
    """Create minimal Factory-DRB + bindings identity + eat-latch factory-project.yaml.

    Does **not** write weave_track.yaml or default require_weave_track_coupled true.
    game_repo_path lives in bindings/identity.yaml only.
    """
    import yaml

    from .bindings import bindings_family_path

    vault_root = vault_root.resolve()
    drb = factory_drb_dir(vault_root, project_id)
    drb.mkdir(parents=True, exist_ok=True)
    (drb / "Release-Definitions").mkdir(parents=True, exist_ok=True)
    (drb / "bindings").mkdir(parents=True, exist_ok=True)

    identity_path = bindings_family_path(vault_root, project_id, "identity")
    identity_path.write_text(
        yaml.dump(
            {
                "project_id": project_id,
                "game_repo_path": game_repo_path.strip("/"),
                "archive_path": "",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    for fam, body in (
        ("engine", {"adapter_id": "", "build_command": "", "ports": {}}),
        ("proof-catalog", {"probes": {}}),
        ("lanes", {"lane_ids": [], "order": []}),
        ("host-law", {"entries": []}),
        ("legacy-refuse", {"refuse_strings": []}),
    ):
        bindings_family_path(vault_root, project_id, fam).write_text(
            yaml.dump(body, sort_keys=False), encoding="utf-8"
        )

    manifest_body = {
        "schema_version": 1,
        "project_id": project_id,
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
        yaml.dump({"default_lanes": []}),
        encoding="utf-8",
    )
    (drb / "factory-project.yaml").write_text(
        yaml.dump(
            {
                "schema_version": 1,
                "project_id": project_id,
                "factory_greenlit": False,
                "slice_factory_greenlit": False,
                "factory_bootstrap": {
                    "gates_before_slices": False,
                    "bootstrap_waiver": False,
                    "require_weave_track_coupled": False,
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
                    "product_version": release_tier or "",
                },
                "product_id": project_id,
            }
        ),
        encoding="utf-8",
    )
    if release_tier.strip():
        (drb / "Release-Definitions" / f"{release_tier.strip()}.md").write_text(
            f"---\ntitle: {release_tier.strip()}\ngame_repo: {game_repo_path.strip('/')}\n---\n",
            encoding="utf-8",
        )
    repo = vault_root / game_repo_path.strip("/")
    repo.mkdir(parents=True, exist_ok=True)
    # Do not write weave_track.yaml — coupling is operator/project data, not scaffold default.
    return {
        "ok": True,
        "project_id": project_id,
        "drb_dir": str(drb.relative_to(vault_root)),
        "game_repo_path": game_repo_path.strip("/"),
    }
