"""Lane charters — ids come from bindings/lanes.yaml; missing file raises."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .bindings import BindingMissingError, load_family, require_project_id

DEFAULT_LANE_ROOT = ".technical/parallel"


@dataclass(frozen=True)
class LaneCharter:
    lane_id: str
    factory_name: str
    primary_artifact: str
    status: str
    path: Path

    @property
    def active(self) -> bool:
        return self.status in ("active", "trialing")


def lane_ids_for_project(vault_root: Path, project_id: str) -> tuple[str, ...]:
    pid = require_project_id(project_id)
    lanes = load_family(vault_root, pid, "lanes")
    raw = lanes.get("lane_ids")
    if not isinstance(raw, list) or not raw:
        raise BindingMissingError(
            "binding_missing",
            f"lanes:lane_ids_empty:{pid}",
        )
    return tuple(str(x).strip() for x in raw if str(x).strip())


def lane_charter_path(vault_root: Path, lane_id: str, root_rel: str = DEFAULT_LANE_ROOT) -> Path:
    return vault_root / root_rel / lane_id / "milestone-charter.yaml"


def load_lane_charter(vault_root: Path, lane_id: str) -> LaneCharter | None:
    path = lane_charter_path(vault_root, lane_id, DEFAULT_LANE_ROOT)
    if not path.is_file():
        return None
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        return None
    return LaneCharter(
        lane_id=lane_id,
        factory_name=str(raw.get("factory_name") or lane_id),
        primary_artifact=str(raw.get("primary_artifact") or ""),
        status=str(raw.get("status") or "draft"),
        path=path,
    )


def validate_lane_charters(vault_root: Path, project_id: str) -> list[str]:
    """Validate charters for lane_ids declared in bindings/lanes.yaml."""
    violations: list[str] = []
    try:
        ids = lane_ids_for_project(vault_root, project_id)
    except BindingMissingError as exc:
        return [str(exc.detail)]
    for lane_id in ids:
        ch = load_lane_charter(vault_root, lane_id)
        if ch is None:
            violations.append(f"lane_charter_missing:{lane_id}")
            continue
        if not ch.primary_artifact:
            violations.append(f"lane_charter_no_primary_artifact:{lane_id}")
        if ch.status == "draft":
            violations.append(f"lane_charter_not_active:{lane_id}")
    return violations


# Back-compat alias — callers must pass project_id via validate_lane_charters.
def validate_six_lane_charters(vault_root: Path, project_id: str | None = None) -> list[str]:
    if not str(project_id or "").strip():
        return ["lane_charters:project_id_missing"]
    return validate_lane_charters(vault_root, str(project_id))
