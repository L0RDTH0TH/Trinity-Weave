"""Trinity partition registry — component / bridge / meta anatomy (Phase 0)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

Anatomy = Literal["component", "bridge", "meta", "deferred", "unknown"]

REGISTRY_REL = Path(".technical/weave/trinity-partition-registry.yaml")


def registry_path(vault_root: Path) -> Path:
    return vault_root / REGISTRY_REL


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore[import-untyped]

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML object: {path}")
    return data


@dataclass(frozen=True)
class ComponentEntry:
    trinity_id: str
    partition: str
    anatomy: Anatomy
    primary_anchor: str = ""
    role: str = ""
    overlap_watch: tuple[str, ...] = ()
    status: str = "locked"


@dataclass
class PartitionRegistry:
    schema_version: int
    components: dict[str, ComponentEntry] = field(default_factory=dict)
    bridges: dict[str, ComponentEntry] = field(default_factory=dict)
    meta: dict[str, ComponentEntry] = field(default_factory=dict)
    deferred: dict[str, ComponentEntry] = field(default_factory=dict)
    known_overlap_risks: list[dict[str, Any]] = field(default_factory=list)
    provisionals_default_anatomy: str = "component"

    def anatomy_for(self, trinity_id: str) -> Anatomy:
        if trinity_id in self.components:
            return "component"
        if trinity_id in self.bridges:
            return "bridge"
        if trinity_id in self.meta:
            return "meta"
        if trinity_id in self.deferred:
            return "deferred"
        return "unknown"

    def entry_for(self, trinity_id: str) -> ComponentEntry | None:
        for bucket in (self.components, self.bridges, self.meta, self.deferred):
            if trinity_id in bucket:
                return bucket[trinity_id]
        return None

    def maintenance_component_ids(self) -> list[str]:
        return sorted(
            tid for tid, e in self.components.items() if e.partition == "maintenance"
        )

    def maintenance_bridge_ids(self) -> list[str]:
        return sorted(
            tid for tid, e in self.bridges.items() if e.partition == "maintenance"
        )

    def maintenance_trinity_ids(self) -> list[str]:
        """All maintenance partition component + bridge trinity_ids (registry order)."""
        return self.maintenance_component_ids() + self.maintenance_bridge_ids()


@dataclass(frozen=True)
class MaintenanceTrinityIds:
    """Canonical maintenance partition id bundles (from trinity-partition-registry.yaml)."""

    components: tuple[str, ...]
    bridges: tuple[str, ...]

    @property
    def all(self) -> tuple[str, ...]:
        return self.components + self.bridges


def load_maintenance_trinity_ids(vault_root: Path) -> MaintenanceTrinityIds:
    """Single source of truth for plan MAINTENANCE_*_IDS (registry-backed).

    - MAINTENANCE_COMPONENT_IDS → .components
    - MAINTENANCE_BRIDGE_IDS → .bridges
    - MAINTENANCE_TRINITY_IDS → .all
    """
    reg = load_partition_registry(vault_root)
    return MaintenanceTrinityIds(
        components=tuple(reg.maintenance_component_ids()),
        bridges=tuple(reg.maintenance_bridge_ids()),
    )


def load_partition_registry(vault_root: Path) -> PartitionRegistry:
    path = registry_path(vault_root.resolve())
    if not path.is_file():
        raise FileNotFoundError(f"partition registry missing: {path}")
    raw = _load_yaml(path)
    reg = PartitionRegistry(
        schema_version=int(raw.get("schema_version") or 1),
        known_overlap_risks=list(raw.get("known_overlap_risks") or []),
        provisionals_default_anatomy=str(
            (raw.get("provisionals") or {}).get("default_anatomy") or "component"
        ),
    )
    partitions = raw.get("partitions") or {}
    if not isinstance(partitions, dict):
        raise ValueError("partitions must be a mapping")

    for partition_name, part in partitions.items():
        if not isinstance(part, dict):
            continue
        for row in part.get("components") or []:
            if not isinstance(row, dict):
                continue
            tid = str(row.get("id") or "").strip()
            if not tid:
                continue
            reg.components[tid] = ComponentEntry(
                trinity_id=tid,
                partition=str(partition_name),
                anatomy="component",
                primary_anchor=str(row.get("primary_anchor") or "").strip(),
                role=str(row.get("role") or row.get("mandate") or "").strip(),
                overlap_watch=tuple(str(x) for x in (row.get("overlap_watch") or [])),
                status="locked",
            )
        for row in part.get("bridges") or []:
            if not isinstance(row, dict):
                continue
            tid = str(row.get("id") or "").strip()
            if not tid:
                continue
            reg.bridges[tid] = ComponentEntry(
                trinity_id=tid,
                partition=str(partition_name),
                anatomy="bridge",
                role=str(row.get("role") or row.get("mandate") or "").strip(),
                status=str(row.get("status") or "planned"),
            )
        for row in part.get("meta") or []:
            if not isinstance(row, dict):
                continue
            tid = str(row.get("id") or "").strip()
            if not tid:
                continue
            reg.meta[tid] = ComponentEntry(
                trinity_id=tid,
                partition=str(partition_name),
                anatomy="meta",
                status=str(row.get("status") or "stub"),
            )
        for row in part.get("deferred") or []:
            if isinstance(row, dict):
                tid = str(row.get("id") or "").strip()
                reason = str(row.get("reason") or "")
            else:
                tid = str(row).strip()
                reason = ""
            if not tid:
                continue
            reg.deferred[tid] = ComponentEntry(
                trinity_id=tid,
                partition=str(partition_name),
                anatomy="deferred",
                status=reason or "deferred",
            )
    return reg


def upsert_registry_bridge(
    vault_root: Path,
    *,
    trinity_id: str,
    partition: str = "maintenance",
    role: str = "vehicle",
    status: str = "locked",
    dry_run: bool = False,
) -> dict[str, Any]:
    """Add or update a bridge row in trinity-partition-registry.yaml."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id or "").strip()
    if not tid:
        return {"ok": False, "error": "trinity_id required"}

    path = registry_path(vault_root)
    if not path.is_file():
        return {"ok": False, "error": "registry_missing", "path": str(path)}

    raw = _load_yaml(path)
    partitions = raw.setdefault("partitions", {})
    part = partitions.setdefault(partition, {})
    bridges = part.setdefault("bridges", [])
    if not isinstance(bridges, list):
        bridges = []
        part["bridges"] = bridges

    entry = {"id": tid, "status": status, "role": role}
    updated = False
    for i, row in enumerate(bridges):
        if isinstance(row, dict) and str(row.get("id") or "").strip() == tid:
            bridges[i] = {**row, **entry}
            updated = True
            break
    if not updated:
        bridges.append(entry)

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "trinity_id": tid,
            "would_update_registry": True,
            "entry": entry,
        }

    import yaml  # type: ignore[import-untyped]

    path.write_text(
        yaml.dump(raw, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )
    return {
        "ok": True,
        "trinity_id": tid,
        "registry_path": str(REGISTRY_REL),
        "updated": updated,
        "entry": entry,
    }
