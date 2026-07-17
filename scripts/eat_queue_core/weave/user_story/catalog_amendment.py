"""Catalog row amendments and execution_gap queue helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, save_yaml, user_story_paths


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def apply_catalog_amendment(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    patch: dict[str, Any],
) -> dict[str, Any]:
    """Merge patch into one catalog row; stamp amendment metadata."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    rows = catalog.get("rows") or []
    if not isinstance(rows, list):
        return {"ok": False, "detail": "catalog_rows_invalid"}

    found = False
    for row in rows:
        if isinstance(row, dict) and str(row.get("id")) == row_id:
            amendments = list(row.get("amendments") or [])
            amendments.append({"at": _utc_iso(), "patch_keys": sorted(patch.keys())})
            row.update(patch)
            row["amendments"] = amendments
            row["mint_status"] = row.get("mint_status") or "amended"
            found = True
            break

    if not found:
        return {"ok": False, "detail": f"row_not_found:{row_id}"}

    catalog["rows"] = rows
    catalog["last_amended_at"] = _utc_iso()
    save_yaml(paths["catalog"], catalog)
    return {
        "ok": True,
        "path": str(paths["catalog"].relative_to(vault_root)),
        "row_id": row_id,
        "patch_keys": sorted(patch.keys()),
    }


def build_execution_gap_queue_line(
    *,
    request_id: str,
    project_id: str,
    row_id: str,
    gap_code: str,
    detail: str = "",
) -> dict[str, Any]:
    """RETIRED — do not enqueue EXECUTION_GAP. Use execution_pseudo_code_audit + roadmap_gap research."""
    raise RuntimeError(
        "EXECUTION_GAP queue lines are retired; use execution_pseudo_code_audit + enqueue_research(roadmap_gap)"
    )
