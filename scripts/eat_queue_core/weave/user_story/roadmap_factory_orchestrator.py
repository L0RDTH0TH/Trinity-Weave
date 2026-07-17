"""PMG factory bootstrap — reset cursor and run conductor tick."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .product_factory_pipeline import bootstrap as product_factory_bootstrap


def run_roadmap_factory_bootstrap(
    vault_root: Path,
    *,
    project_id: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """First factory boot — new run_id, empty completed_phases, then tick."""
    return product_factory_bootstrap(vault_root, project_id=project_id, params=params or {})


def run_roadmap_factory_relaunch(
    vault_root: Path,
    *,
    project_id: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Deprecated alias — use run_roadmap_factory_bootstrap."""
    return run_roadmap_factory_bootstrap(vault_root, project_id=project_id, params=params or {})
