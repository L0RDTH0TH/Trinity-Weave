"""Deterministic catalog scaffold from PMG phase headings."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, save_yaml, user_story_paths


def _resolve_mint_batch(vault_root: Path, mint_batch: str | None) -> str:
    if mint_batch:
        return str(mint_batch).strip().lower()
    try:
        from ...merged_config import load_merged_yaml_blocks

        blocks = load_merged_yaml_blocks(vault_root)
        rf = blocks.get("roadmap_factory")
        if isinstance(rf, dict) and rf.get("default_mint_batch"):
            return str(rf["default_mint_batch"]).strip().lower()
    except (ImportError, OSError, TypeError, ValueError):
        pass
    return "pmg_phases"


def _filter_rows_for_mint_batch(
    headings: list[tuple[str, str]],
    smoke_rows: list[dict[str, Any]],
    mint_batch: str,
) -> tuple[list[tuple[str, str]], list[dict[str, Any]]]:
    """presentation_first = spine smoke only; pmg_phases = full harvest."""
    batch = mint_batch.lower()
    if batch == "presentation_first":
        filtered_smoke = [r for r in smoke_rows if str(r.get("id")) == "ui_presentation_shell"]
        filtered_headings = [
            (num, title)
            for num, title in headings
            if num.startswith("6.1") or num == "6"
        ]
        if not filtered_headings and headings:
            filtered_headings = headings[:1]
        return filtered_headings, filtered_smoke
    return headings, smoke_rows


@dataclass(frozen=True)
class CatalogMintProposeResult:
    ok: bool
    rows_added: int
    path: str
    proposed_ids: tuple[str, ...]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "rows_added": self.rows_added,
            "path": self.path,
            "proposed_ids": list(self.proposed_ids),
            "detail": self.detail,
        }


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return s[:48] or "row"


def _phase_headings(pmg_text: str) -> list[tuple[str, str]]:
    """Return (phase_num, title) from ## Phase N or ### Phase N.M headings."""
    out: list[tuple[str, str]] = []
    for m in re.finditer(r"^#{2,3}\s+Phase\s+([\d.]+)[:\s—-]*(.*)$", pmg_text, re.MULTILINE | re.IGNORECASE):
        num = m.group(1).strip()
        title = m.group(2).strip() or f"Phase {num}"
        out.append((num, title))
    return out


def _find_pmg_path(vault_root: Path, project_id: str) -> Path | None:
    base = vault_root / "1-Projects" / project_id
    for pat in ("*Master*Goal*", "*master*goal*", "*PMG*"):
        for p in base.rglob(pat):
            if p.is_file() and p.suffix == ".md":
                return p
    for p in base.glob("*.md"):
        if "master" in p.name.lower() and "goal" in p.name.lower():
            return p
    return None


def _factory_smoke_rows_from_pmg(pmg_text: str, pmg_rel: str) -> list[dict[str, Any]]:
    """PMG prose rows (e.g. ui_presentation_shell) not captured by ### Phase N headings."""
    rows: list[dict[str, Any]] = []
    if re.search(
        r"ui_presentation_shell|presentation\s+shell|Factory\s+Phase\s+0",
        pmg_text,
        re.IGNORECASE,
    ):
        rows.append(
            {
                "id": "ui_presentation_shell",
                "dimension": "ui_surface",
                "label": "Presentation shell (Factory Phase 0)",
                "planned": True,
                "conceptual_pin": f"[[{pmg_rel}]]",
                "execution_pins": [],
                "depends_on": [],
                "mint_status": "proposed",
                "touchstone_refs": [],
            }
        )
    return rows


def propose_catalog_from_pmg(
    vault_root: Path,
    *,
    project_id: str,
    pmg_path: Path | None = None,
    dimension: str = "system",
    merge: bool = True,
    mint_batch: str | None = None,
) -> CatalogMintProposeResult:
    """
    Scaffold slice-catalog rows from PMG phase headings.

    mint_batch: ``pmg_phases`` (default) harvests all phases + smokes;
    ``presentation_first`` is opt-in narrow mint (ui_presentation_shell + Phase 6.1).
    """
    vault_root = vault_root.resolve()
    batch = _resolve_mint_batch(vault_root, mint_batch)
    pmg = pmg_path or _find_pmg_path(vault_root, project_id)
    if pmg is None or not pmg.is_file():
        return CatalogMintProposeResult(False, 0, "", (), "pmg_not_found")

    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"]) if merge and paths["catalog"].is_file() else {"schema_version": 1, "rows": []}
    existing = catalog_rows_by_id(catalog)
    pmg_text = pmg.read_text(encoding="utf-8", errors="replace")
    headings = _phase_headings(pmg_text)
    if not headings:
        return CatalogMintProposeResult(False, 0, "", (), "no_phase_headings_in_pmg")

    pmg_rel = str(pmg.relative_to(vault_root))
    smoke_rows = _factory_smoke_rows_from_pmg(pmg_text, pmg_rel)
    headings, smoke_rows = _filter_rows_for_mint_batch(headings, smoke_rows, batch)

    added: list[str] = []
    rows = list(catalog.get("rows") or [])
    for smoke in smoke_rows:
        rid = str(smoke.get("id") or "")
        if rid and rid not in existing:
            rows.append(smoke)
            added.append(rid)
            existing[rid] = smoke
    for num, title in headings:
        row_id = f"phase_{_slug(num)}"
        if row_id in existing:
            continue
        rows.append(
            {
                "id": row_id,
                "dimension": dimension,
                "label": title,
                "planned": True,
                "conceptual_pin": f"[[{pmg.relative_to(vault_root)}]]",
                "execution_pins": [],
                "depends_on": [],
                "mint_status": "proposed",
                "touchstone_refs": [],
            }
        )
        added.append(row_id)

    catalog["rows"] = rows
    catalog["mint_source_pmg"] = str(pmg.relative_to(vault_root))
    catalog["mint_batch"] = batch
    save_yaml(paths["catalog"], catalog)

    return CatalogMintProposeResult(
        ok=True,
        rows_added=len(added),
        path=str(paths["catalog"].relative_to(vault_root)),
        proposed_ids=tuple(added),
        detail="catalog_mint_proposed" if added else "catalog_unchanged",
    )
