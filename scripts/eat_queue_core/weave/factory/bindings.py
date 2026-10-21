"""Project bindings — fail-closed resolve from Factory-DRB/bindings/*.yaml.

Families live in project data. The harness does not silently default to a product.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

BINDING_MISSING = "binding_missing"
UNKNOWN_PROBE = "unknown_probe"

_FAMILIES: frozenset[str] = frozenset(
    {
        "identity",
        "engine",
        "proof-catalog",
        "lanes",
        "host-law",
        "legacy-refuse",
    }
)


class BindingMissingError(KeyError):
    """Raised when a bindings family file or key is absent."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def bindings_family_rel(project_id: str, family: str) -> str:
    """Sole vault-layout helper for bindings paths — do not paste this elsewhere."""
    pid = str(project_id or "").strip()
    fam = str(family or "").strip()
    if not pid:
        raise BindingMissingError(BINDING_MISSING, "bindings:project_id_empty")
    if fam not in _FAMILIES:
        raise BindingMissingError(BINDING_MISSING, f"bindings:unknown_family:{fam}")
    return f"1-Projects/{pid}/Factory-DRB/bindings/{fam}.yaml"


def bindings_family_path(vault_root: Path, project_id: str, family: str) -> Path:
    return vault_root.resolve() / bindings_family_rel(project_id, family)


def load_family(
    vault_root: Path, project_id: str, family: str
) -> dict[str, Any]:
    path = bindings_family_path(vault_root, project_id, family)
    if not path.is_file():
        raise BindingMissingError(
            BINDING_MISSING,
            f"bindings:missing_file:{bindings_family_rel(project_id, family)}",
        )
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise BindingMissingError(
            BINDING_MISSING,
            f"bindings:unreadable:{bindings_family_rel(project_id, family)}:{exc}",
        ) from exc
    if not isinstance(data, dict):
        raise BindingMissingError(
            BINDING_MISSING,
            f"bindings:not_mapping:{bindings_family_rel(project_id, family)}",
        )
    return data


def resolve(
    vault_root: Path,
    project_id: str,
    family: str,
    key: str,
) -> Any:
    """Return bindings[family][key]. Missing file or key raises BindingMissingError."""
    data = load_family(vault_root, project_id, family)
    if key not in data:
        raise BindingMissingError(
            BINDING_MISSING,
            f"bindings:missing_key:{family}:{key}",
        )
    return data[key]


def resolve_optional(
    vault_root: Path,
    project_id: str,
    family: str,
    key: str,
    *,
    default: Any = None,
) -> Any:
    """Optional key inside an existing family file. Missing file still raises."""
    data = load_family(vault_root, project_id, family)
    if key not in data:
        return default
    return data[key]


def require_project_id(project_id: str | None) -> str:
    pid = str(project_id or "").strip()
    if not pid:
        from .project_identity import ProjectIdMissingError

        raise ProjectIdMissingError()
    return pid


def add_project_id_argument(parser: Any, *, required: bool = True) -> None:
    """Single CLI socket — never add a default project id at call sites."""
    parser.add_argument(
        "--project-id",
        type=str,
        required=required,
        default=None,
        help="Factory project id (required; no silent default)",
    )


def game_repo_path(vault_root: Path, project_id: str) -> str:
    """Sole source: identity.yaml game_repo_path. No factory-project merge fallback."""
    raw = resolve(vault_root, project_id, "identity", "game_repo_path")
    rel = str(raw or "").strip().strip("/")
    if not rel:
        raise BindingMissingError(
            BINDING_MISSING, "bindings:identity:game_repo_path_empty"
        )
    return rel


def factory_drb_rel(project_id: str, *parts: str) -> str:
    """Sole layout helper for Factory-DRB paths under a project id."""
    pid = require_project_id(project_id)
    base = f"1-Projects/{pid}/Factory-DRB"
    cleaned = [str(p).strip("/") for p in parts if str(p).strip("/")]
    return base if not cleaned else base + "/" + "/".join(cleaned)


def queue_lane(vault_root: Path, project_id: str) -> str:
    """Sole queue/lane id from identity.yaml — no harness lane literals."""
    raw = resolve(vault_root, project_id, "identity", "queue_lane")
    lane = str(raw or "").strip()
    if not lane:
        raise BindingMissingError(BINDING_MISSING, "bindings:identity:queue_lane_empty")
    return lane
