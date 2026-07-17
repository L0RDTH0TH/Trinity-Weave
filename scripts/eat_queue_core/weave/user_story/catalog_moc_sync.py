"""Sync slice-catalog.yaml → operator-facing slice-catalog.md MOC."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, user_story_paths


def sync_catalog_moc(vault_root: Path, *, project_id: str) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    if not paths["catalog"].is_file():
        return {"ok": False, "detail": "catalog_missing"}

    catalog = load_yaml(paths["catalog"])
    by_id = catalog_rows_by_id(catalog)
    moc_path = paths["catalog"].with_suffix(".md")

    lines = [
        "---",
        "title: Slice catalog MOC",
        f"project-id: {project_id}",
        "roadmap_track: user_story",
        "status: active",
        "---",
        "",
        f"# Slice catalog — {project_id}",
        "",
        "> Auto-synced from `slice-catalog.yaml`. Edit rows via catalog mint / operator attestation.",
        "",
        "| row_id | label | dimension | mint_status | L5 |",
        "|--------|-------|-----------|-------------|-----|",
    ]
    for rid, row in sorted(by_id.items()):
        label = str(row.get("label") or rid)
        dim = str(row.get("dimension") or "")
        mint = str(row.get("mint_status") or "")
        l5 = paths["scopes_dir"] / rid / "L5.md"
        l5_link = f"[[{l5.relative_to(vault_root)}|L5]]" if l5.is_file() else "—"
        lines.append(f"| `{rid}` | {label} | {dim} | {mint} | {l5_link} |")

    lines.extend(
        [
            "",
            "## Attestation order (OQ-factory-001)",
            "",
            "Sign off **factory-spine** rows at Loop 2 before minting later content batches.",
            "Multiple rows and later mint batches are allowed — ordering only, not a one-row cap.",
            "",
        ]
    )

    moc_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "path": str(moc_path.relative_to(vault_root)),
        "row_count": len(by_id),
        "detail": "catalog_moc_synced",
    }
