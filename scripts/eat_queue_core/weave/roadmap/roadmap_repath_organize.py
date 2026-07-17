"""Repath flat roadmap notes to canonical nested layout (content-preserving moves)."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import yaml

from .roadmap_path_resolver import (
    canonical_repath_target,
    scan_structural_path_violations,
)


def _read_note(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    fm = yaml.safe_load(text[4:end]) or {}
    return fm if isinstance(fm, dict) else {}


def _plan_moves(vault_root: Path, project_id: str) -> list[dict[str, Any]]:
    violations = scan_structural_path_violations(vault_root, project_id)
    plans: list[dict[str, Any]] = []
    for row in violations:
        src = vault_root / row["rel_path"]
        if not src.is_file():
            continue
        fm = _read_note(src)
        target = canonical_repath_target(vault_root, src, fm)
        if not target:
            continue
        _rel_dir, rel_path = target
        dst = vault_root / rel_path
        if src.resolve() == dst.resolve():
            continue
        plans.append(
            {
                "from": str(src.relative_to(vault_root)),
                "to": rel_path,
                "violations": row["violations"],
                "subphase_index": fm.get("subphase-index"),
            }
        )

    def sort_key(p: dict[str, Any]) -> tuple[int, str]:
        idx = str(p.get("subphase_index") or "")
        depth = len(idx.split(".")) if idx else 0
        return (-depth, str(p.get("from") or ""))

    plans.sort(key=sort_key)
    return plans


def organize_roadmap_paths(
    vault_root: Path,
    project_id: str,
    *,
    dry_run: bool = True,
) -> dict[str, Any]:
    """
    Move misplaced roadmap notes into canonical folders.

    Content is unchanged; only path moves. Wikilink repair is best-effort in-roadmap.
    """
    vault_root = vault_root.resolve()
    plans = _plan_moves(vault_root, project_id)
    moved: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []

    for plan in plans:
        src = vault_root / plan["from"]
        dst = vault_root / plan["to"]
        if dry_run:
            moved.append({"from": plan["from"], "to": plan["to"], "dry_run": "true"})
            continue
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists() and src.resolve() != dst.resolve():
                errors.append({"from": plan["from"], "error": "destination_exists", "to": plan["to"]})
                continue
            shutil.move(str(src), str(dst))
            _repair_wikilinks_in_tree(
                vault_root,
                project_id,
                old_rel=plan["from"],
                new_rel=plan["to"],
            )
            moved.append({"from": plan["from"], "to": plan["to"]})
        except OSError as exc:
            errors.append({"from": plan["from"], "error": str(exc), "to": plan["to"]})

    remaining = scan_structural_path_violations(vault_root, project_id)
    return {
        "ok": not errors,
        "project_id": project_id,
        "dry_run": dry_run,
        "planned": len(plans),
        "moved": moved,
        "errors": errors,
        "remaining_violations": len(remaining),
    }


def _repair_wikilinks_in_tree(
    vault_root: Path,
    project_id: str,
    *,
    old_rel: str,
    new_rel: str,
) -> int:
    """Replace wiki path strings under project Roadmap/ after a move."""
    road = vault_root / "1-Projects" / project_id / "Roadmap"
    if not road.is_dir():
        return 0
    old_stem = Path(old_rel).stem
    new_stem = Path(new_rel).stem
    old_name = Path(old_rel).name
    new_name = Path(new_rel).name
    count = 0
    for path in road.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        updated = text
        updated = updated.replace(f"[[{old_rel}]]", f"[[{new_rel}]]")
        updated = updated.replace(f"[[{old_name}]]", f"[[{new_name}]]")
        updated = updated.replace(f"[[{old_stem}]]", f"[[{new_stem}]]")
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            count += 1
    return count
