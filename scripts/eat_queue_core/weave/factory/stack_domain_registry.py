"""Load Stack-Domain-Registry-v1.yaml."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .factory_drb_paths import drb_artifact_path, resolve_project_id

DEFAULT_REGISTRY_REL = (
    "1-Projects/genesis-mythos-master/Factory-DRB/Stack-Domain-Registry-v1.yaml"
)


@dataclass(frozen=True)
class StackDomain:
    id: str
    title: str
    research_domain_id: str
    baseline_required: bool
    interop_pairs: tuple[str, ...]
    spine_interface: str | None
    raw: dict[str, Any]


@dataclass(frozen=True)
class StackDomainRegistry:
    path: Path
    poc_canonical: bool
    interop_gate_required: bool
    domains: tuple[StackDomain, ...]

    def domain_ids(self) -> set[str]:
        return {d.id for d in self.domains}


def _load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    import yaml  # type: ignore[import-untyped]

    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"registry root must be mapping: {path}")
    return data


def load_stack_domain_registry(
    vault_root: Path,
    project_id: str | None = None,
    registry_rel: str | None = None,
) -> StackDomainRegistry:
    if registry_rel:
        path = vault_root / registry_rel
    else:
        path = drb_artifact_path(vault_root, "stack_domain_registry", project_id=project_id)
    if not path.is_file():
        raise FileNotFoundError(f"stack domain registry missing: {path}")
    data = _load_yaml(path)
    domains_raw = data.get("domains") or []
    domains: list[StackDomain] = []
    for item in domains_raw:
        if not isinstance(item, dict) or "id" not in item:
            continue
        pairs = item.get("interop_pairs") or []
        domains.append(
            StackDomain(
                id=str(item["id"]),
                title=str(item.get("title", item["id"])),
                research_domain_id=str(item.get("research_domain_id", "")),
                baseline_required=bool(item.get("baseline_required", True)),
                interop_pairs=tuple(str(p) for p in pairs),
                spine_interface=item.get("spine_interface"),
                raw=item,
            )
        )
    return StackDomainRegistry(
        path=path,
        poc_canonical=bool(data.get("poc_canonical", False)),
        interop_gate_required=bool(data.get("interop_gate_required", True)),
        domains=tuple(domains),
    )
