"""Rollback helper (Grok A) — restore cards from Trinity-Corpus archive bundle."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .trinity_card_paths import component_proposals_dir, components_dir

ARCHIVE_ROOT_REL = Path("4-Archives/Weave/Trinity-Corpus")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def list_archive_bundles(vault_root: Path) -> list[str]:
    root = vault_root.resolve() / ARCHIVE_ROOT_REL
    if not root.is_dir():
        return []
    return sorted(
        [p.name for p in root.iterdir() if p.is_dir()],
        reverse=True,
    )


def resolve_archive_bundle(vault_root: Path, stamp: str | None) -> Path | None:
    vault_root = vault_root.resolve()
    base = vault_root / ARCHIVE_ROOT_REL
    if stamp:
        path = base / stamp
        return path if path.is_dir() else None
    bundles = list_archive_bundles(vault_root)
    if not bundles:
        return None
    return base / bundles[0]


def restore_cards_from_archive(
    vault_root: Path,
    *,
    stamp: str | None = None,
    dry_run: bool = False,
    target: str = "proposals",
) -> dict[str, Any]:
    """
    Restore YAML from archive ``cards/`` into component-proposals/ (default) or components/.

    Does not restore trashed tests — operator copies from archive ``tests/`` manually if needed.
    """
    vault_root = vault_root.resolve()
    bundle = resolve_archive_bundle(vault_root, stamp)
    if bundle is None:
        return {"ok": False, "error": "archive_bundle_not_found", "stamp": stamp}

    cards_src = bundle / "cards"
    if not cards_src.is_dir():
        return {"ok": False, "error": "archive_missing_cards_dir", "bundle": str(bundle)}

    manifest_path = bundle / "manifest.json"
    manifest: dict[str, Any] = {}
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = {}

    dest = (
        components_dir(vault_root)
        if target == "components"
        else component_proposals_dir(vault_root)
    )
    restored: list[str] = []
    skipped: list[str] = []
    for src in sorted(cards_src.glob("*.yaml")):
        tid = src.stem
        dest_path = dest / src.name
        if dest_path.is_file() and not dry_run:
            skipped.append(tid)
            continue
        if dry_run:
            restored.append(tid)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_path)
        restored.append(tid)

    return {
        "ok": True,
        "dry_run": dry_run,
        "archive_path": str(bundle.relative_to(vault_root)),
        "stamp": bundle.name,
        "target_dir": str(dest.relative_to(vault_root)),
        "restored_count": len(restored),
        "restored_ids": restored[:50],
        "skipped_existing": skipped[:20],
        "manifest_archived_count": manifest.get("archived_card_count"),
        "completed_at": _now_iso(),
    }
