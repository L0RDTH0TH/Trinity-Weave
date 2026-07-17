"""Catalog completeness + pre-freeze gate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, parse_state_frontmatter, user_story_paths


@dataclass(frozen=True)
class CatalogCoverageResult:
    ok: bool
    violations: tuple[str, ...]
    orphan_pins: tuple[str, ...]
    missing_rows: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "violations": list(self.violations),
            "orphan_pins": list(self.orphan_pins),
            "missing_rows": list(self.missing_rows),
        }


def run_catalog_coverage(
    vault_root: Path,
    *,
    project_id: str,
    planned_row_ids: tuple[str, ...] | None = None,
    require_pins: bool = True,
) -> CatalogCoverageResult:
    """Full coverage check. When require_pins=False, structure-only (pre-execution)."""
    if not require_pins:
        return run_catalog_coverage_structure(vault_root, project_id=project_id, planned_row_ids=planned_row_ids)
    return run_catalog_coverage_strict(vault_root, project_id=project_id, planned_row_ids=planned_row_ids)


def run_catalog_coverage_structure(
    vault_root: Path,
    *,
    project_id: str,
    planned_row_ids: tuple[str, ...] | None = None,
) -> CatalogCoverageResult:
    """Rows, dimensions, planned flags — no execution_pins required."""
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    rows = catalog_rows_by_id(catalog)
    violations: list[str] = []

    if not rows:
        violations.append("catalog_empty")

    for row_id, row in rows.items():
        if row.get("planned") and not row.get("dimension"):
            violations.append(f"row_missing_dimension:{row_id}")

    if planned_row_ids:
        for pid in planned_row_ids:
            if pid not in rows:
                violations.append(f"planned_row_missing:{pid}")

    ok = len(violations) == 0
    return CatalogCoverageResult(
        ok=ok,
        violations=tuple(violations),
        orphan_pins=tuple(),
        missing_rows=tuple(violations),
    )


def run_catalog_coverage_strict(
    vault_root: Path,
    *,
    project_id: str,
    planned_row_ids: tuple[str, ...] | None = None,
) -> CatalogCoverageResult:
    """Pins exist and resolve on disk — pre-factory."""
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    rows = catalog_rows_by_id(catalog)
    violations: list[str] = []

    if not rows:
        violations.append("catalog_empty")

    check_ids = [str(x) for x in planned_row_ids] if planned_row_ids else list(rows.keys())
    for row_id in check_ids:
        row = rows.get(row_id) or {}
        if not row:
            violations.append(f"planned_row_missing:{row_id}")
            continue
        if row.get("planned") and not row.get("dimension"):
            violations.append(f"row_missing_dimension:{row_id}")
        pins = row.get("execution_pins") or []
        if row.get("planned") and not pins:
            violations.append(f"row_missing_execution_pin:{row_id}")
        for pin in pins if isinstance(pins, list) else []:
            rel = str(pin).strip()
            if rel and not (vault_root / rel).is_file() and not (vault_root / f"{rel}.md").is_file():
                pin_path = rel if rel.endswith(".md") else f"{rel}.md"
                if not (vault_root / pin_path).is_file():
                    violations.append(f"execution_pin_missing:{row_id}:{rel}")

    ok = len(violations) == 0
    return CatalogCoverageResult(
        ok=ok,
        violations=tuple(violations),
        orphan_pins=tuple(),
        missing_rows=tuple(violations),
    )


def run_catalog_freeze_gate(
    vault_root: Path,
    *,
    project_id: str,
) -> dict[str, Any]:
    """Block conceptual freeze until catalog + depth charter signed."""
    paths = user_story_paths(vault_root, project_id)
    violations: list[str] = []

    if not paths["catalog"].is_file():
        violations.append("catalog_missing")
    if not paths["depth_charter"].is_file():
        violations.append("depth_charter_missing")
    if not paths["influence"].is_file():
        violations.append("influence_deck_missing")

    state = parse_state_frontmatter(paths["state"])
    if not state.get("catalog_signed_at"):
        violations.append("catalog_not_signed")
    if not state.get("depth_charter_version"):
        violations.append("depth_charter_not_versioned")

    coverage = run_catalog_coverage(vault_root, project_id=project_id)
    violations.extend(list(coverage.violations))

    return {
        "ok": len(violations) == 0,
        "violations": violations,
        "coverage": coverage.to_dict(),
    }
