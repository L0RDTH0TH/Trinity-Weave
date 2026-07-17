"""Six factory lane charters — org ownership, not game build order."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

LANE_IDS: tuple[str, ...] = ("asset", "techart", "content", "presentation", "audio", "module")

DEFAULT_LANE_ROOT = ".technical/parallel"
FALLBACK_LANE_ROOT = "1-Projects/godot-genesis-mythos-master/Factory-DRB/lanes"


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


def lane_charter_path(vault_root: Path, lane_id: str, root_rel: str = DEFAULT_LANE_ROOT) -> Path:
    return vault_root / root_rel / lane_id / "milestone-charter.yaml"


def load_lane_charter(vault_root: Path, lane_id: str) -> LaneCharter | None:
    for root_rel in (DEFAULT_LANE_ROOT, FALLBACK_LANE_ROOT):
        path = lane_charter_path(vault_root, lane_id, root_rel)
        if not path.is_file():
            continue
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
    return None


def validate_six_lane_charters(vault_root: Path) -> list[str]:
    violations: list[str] = []
    for lane_id in LANE_IDS:
        ch = load_lane_charter(vault_root, lane_id)
        if ch is None:
            violations.append(f"lane_charter_missing:{lane_id}")
            continue
        if not ch.primary_artifact:
            violations.append(f"lane_charter_no_primary_artifact:{lane_id}")
        if ch.status == "draft":
            violations.append(f"lane_charter_not_active:{lane_id}")
    return violations
