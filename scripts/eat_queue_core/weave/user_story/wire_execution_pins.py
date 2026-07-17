"""Link catalog rows to Roadmap/Execution paths — verify pins resolve."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog_coverage import run_catalog_coverage_strict
from .catalog_io import catalog_rows_by_id, load_yaml, user_story_paths
from .product_factory_budget import budget_row_ids


@dataclass(frozen=True)
class WirePinsResult:
    ok: bool
    wired_count: int
    violations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "wired_count": self.wired_count,
            "violations": list(self.violations),
        }


def wire_execution_pins(vault_root: Path, *, project_id: str) -> WirePinsResult:
    """
    Verify catalog execution_pins resolve on disk.
    Does not mutate catalog — pins are authored during execution deepen / operator loop 2.
    """
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    rows = catalog_rows_by_id(catalog)
    wired = 0
    for row_id, row in rows.items():
        if not row.get("planned"):
            continue
        pins = row.get("execution_pins") or []
        if isinstance(pins, list) and pins:
            wired += 1

    cov = run_catalog_coverage_strict(
        vault_root,
        project_id=project_id,
        planned_row_ids=tuple(budget_row_ids(vault_root, project_id)),
    )
    return WirePinsResult(
        ok=cov.ok,
        wired_count=wired,
        violations=cov.violations,
    )
