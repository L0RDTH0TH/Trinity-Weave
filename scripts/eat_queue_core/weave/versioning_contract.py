"""Cross-layer versioning contract — system, weave, product, artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..weave_observability import WEAVE_CORE_VERSION

# Bump when BOM step schema or evaluator semantics change (breaking).
BOM_SCHEMA_VERSION = 2

# Bump when version document fields change (breaking).
VERSION_CONTRACT_SCHEMA = 1

SUPPORTED_BOM_SCHEMA_VERSIONS = frozenset({1, 2})


@dataclass(frozen=True)
class VersionLayers:
    """Resolved version pins for a product BOM evaluation."""

    bom_schema_version: int
    bom_revision: int
    product_version: str
    release_definition_ref: str
    weave_core_version: str = WEAVE_CORE_VERSION
    rollout_version: int | None = None
    depth_charter_version: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "bom_schema_version": self.bom_schema_version,
            "bom_revision": self.bom_revision,
            "product_version": self.product_version,
            "release_definition_ref": self.release_definition_ref,
            "weave_core_version": self.weave_core_version,
            "rollout_version": self.rollout_version,
            "depth_charter_version": self.depth_charter_version,
            **self.extra,
        }


def parse_version_block(doc: dict[str, Any]) -> VersionLayers:
    """Read versioning block from product-bom.yaml (or legacy top-level fields)."""
    ver = doc.get("versioning") if isinstance(doc.get("versioning"), dict) else {}
    merged = {**doc, **ver}
    bom_schema = int(merged.get("bom_schema_version") or BOM_SCHEMA_VERSION)
    bom_revision = int(merged.get("bom_revision") or 1)
    product_version = str(merged.get("product_version") or merged.get("product_id") or "")
    release_ref = str(
        merged.get("release_definition_ref")
        or merged.get("release_definition_rel")
        or ""
    )
    rollout = merged.get("rollout_version")
    rollout_int = int(rollout) if rollout is not None else None
    depth_cv = merged.get("depth_charter_version")
    return VersionLayers(
        bom_schema_version=bom_schema,
        bom_revision=bom_revision,
        product_version=product_version,
        release_definition_ref=release_ref,
        rollout_version=rollout_int,
        depth_charter_version=str(depth_cv) if depth_cv else None,
        extra={
            "version_contract_schema": VERSION_CONTRACT_SCHEMA,
            "target_milestone": str(merged.get("target_milestone") or ""),
        },
    )


def check_bom_schema_compat(bom_schema_version: int) -> tuple[bool, str]:
    if bom_schema_version in SUPPORTED_BOM_SCHEMA_VERSIONS:
        return True, "bom_schema_ok"
    return (
        False,
        f"bom_schema_unsupported:{bom_schema_version}:supported={sorted(SUPPORTED_BOM_SCHEMA_VERSIONS)}",
    )


def check_weave_core_compat(
    doc: dict[str, Any],
    *,
    current: str = WEAVE_CORE_VERSION,
) -> tuple[bool, str]:
    """Optional warn-only compat list on BOM (compatible_weave_core)."""
    ver = doc.get("versioning") if isinstance(doc.get("versioning"), dict) else {}
    allowed = ver.get("compatible_weave_core") or doc.get("compatible_weave_core")
    if not allowed:
        return True, "weave_core_compat_unpinned"
    if isinstance(allowed, str):
        allowed = [allowed]
    if not isinstance(allowed, list):
        return True, "weave_core_compat_unpinned"
    if current in [str(x) for x in allowed]:
        return True, "weave_core_compat_ok"
    return False, f"weave_core_compat_mismatch:current={current}:allowed={allowed}"
