"""Populate catalog execution_pins from Execution tree when deepen left them empty."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .catalog_io import catalog_rows_by_id, load_yaml, user_story_paths

_WIKI = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


@dataclass(frozen=True)
class PinSyncResult:
    ok: bool
    linked: int
    skipped: int
    details: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "linked": self.linked,
            "skipped": self.skipped,
            "details": list(self.details),
        }


def _wiki_stem(ref: str) -> str:
    ref = ref.strip().strip("/")
    return Path(ref).stem.lower()


def _find_execution_match(exec_root: Path, stem: str) -> Path | None:
    if not exec_root.is_dir():
        return None
    candidates = list(exec_root.rglob("*.md"))
    for c in candidates:
        if c.stem.lower() == stem:
            return c
    for c in candidates:
        if stem in c.stem.lower() or stem in str(c).lower():
            return c
    return None


def sync_catalog_execution_pins(vault_root: Path, *, project_id: str) -> PinSyncResult:
    """Write execution_pins for planned rows that are still empty (post-deepen)."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog_path = paths["catalog"]
    catalog = load_yaml(catalog_path)
    rows = catalog_rows_by_id(catalog)
    exec_root = vault_root / f"1-Projects/{project_id}/Roadmap/Execution"

    linked = 0
    skipped = 0
    details: list[str] = []

    for row_id, row in rows.items():
        if not row.get("planned"):
            skipped += 1
            continue
        pins = row.get("execution_pins") or []
        if isinstance(pins, list) and pins:
            skipped += 1
            continue

        stem = ""
        cp = str(row.get("conceptual_pin") or "")
        m = _WIKI.search(cp)
        if m:
            stem = _wiki_stem(m.group(1))
        if not stem:
            stem = str(row_id).replace("_", "-").lower()

        match = _find_execution_match(exec_root, stem)
        if match is None:
            details.append(f"no_match:{row_id}")
            continue

        rel = str(match.relative_to(vault_root))
        row["execution_pins"] = [rel]
        linked += 1
        details.append(f"linked:{row_id}:{rel}")

    if linked:
        catalog_path.write_text(yaml.dump(catalog, sort_keys=False, allow_unicode=True), encoding="utf-8")

    return PinSyncResult(ok=linked > 0 or skipped > 0, linked=linked, skipped=skipped, details=tuple(details))
