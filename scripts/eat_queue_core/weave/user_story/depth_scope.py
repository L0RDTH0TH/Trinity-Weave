"""Per-row depth scopes (L5 complete → L4..L1) and dispatch depth resolution."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, normalize_pin, user_story_paths

LEVELS = (5, 4, 3, 2, 1)


def scope_dir(vault_root: Path, project_id: str, row_id: str) -> Path:
    paths = user_story_paths(vault_root, project_id)
    scopes_rel = paths.get("scopes_dir")
    if scopes_rel:
        return scopes_rel / row_id
    return paths["budget"].parent / "scopes" / row_id


def scope_path(vault_root: Path, project_id: str, row_id: str, level: int) -> Path:
    return scope_dir(vault_root, project_id, row_id) / f"L{level}.md"


def resolve_dispatch_depth(current_depth: int, target_depth: int) -> int | None:
    """Next factory pass depth: one rung at a time until target."""
    if target_depth <= 0 or current_depth >= target_depth:
        return None
    return min(current_depth + 1, target_depth)


def load_scope_body(vault_root: Path, project_id: str, row_id: str, level: int) -> str:
    path = scope_path(vault_root, project_id, row_id, level)
    if path.is_file():
        return path.read_text(encoding="utf-8", errors="replace").strip()
    return ""


def load_charter_level_lines(vault_root: Path, project_id: str) -> dict[int, str]:
    paths = user_story_paths(vault_root, project_id)
    charter = ""
    if paths["depth_charter"].is_file():
        charter = paths["depth_charter"].read_text(encoding="utf-8", errors="replace")
    out: dict[int, str] = {}
    for level in LEVELS:
        m = re.search(rf"^\|\s*{level}\s*\|\s*(.+?)\s*\|", charter, re.MULTILINE)
        if m:
            out[level] = m.group(1).strip()
    return out


def _pin_excerpt(vault_root: Path, pins: list[Any], max_chars: int = 2000) -> str:
    for pin in pins:
        rel = normalize_pin(str(pin))
        path = vault_root / rel
        if not path.is_file() and not rel.endswith(".md"):
            path = vault_root / f"{rel}.md"
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            return text[:max_chars].strip()
    return ""


def bootstrap_l5_scope(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
) -> Path | None:
    """Create substantive L5 factory draft when operator has not authored L5 yet."""
    from .loop2_prep import draft_l5_user_story

    out = draft_l5_user_story(vault_root, project_id=project_id, row_id=row_id)
    if not out.get("ok"):
        return None
    rel = out.get("path")
    if not rel:
        return None
    path = vault_root.resolve() / rel
    return path if path.is_file() else None


def _section_chunks(l5_text: str) -> dict[str, str]:
    chunks: dict[str, str] = {"_preamble": ""}
    current = "_preamble"
    buf: list[str] = []
    for line in l5_text.splitlines():
        if line.startswith("## "):
            if buf:
                chunks[current] = "\n".join(buf).strip()
            current = line[3:].strip().lower()
            buf = [line]
        else:
            buf.append(line)
    if buf:
        chunks[current] = "\n".join(buf).strip()
    return chunks


def _level_body(
    *,
    level: int,
    row_id: str,
    label: str,
    l5_text: str,
    charter_line: str,
) -> str:
    chunks = _section_chunks(l5_text)
    complete = chunks.get("complete vision", "") or chunks.get("_preamble", "")
    core = chunks.get("core loop", "")
    polish = chunks.get("integration & polish", "") or chunks.get("polish & integration", "")
    scaffold = chunks.get("scaffold minimum", "")

    if level == 5:
        vision_block = l5_text.strip()
    elif level == 4:
        vision_block = "\n\n".join(x for x in [complete, core, polish] if x)
    elif level == 3:
        vision_block = "\n\n".join(x for x in [complete, core] if x)
    elif level == 2:
        vision_block = "\n\n".join(x for x in [core or complete, scaffold] if x)
    else:
        vision_block = scaffold or (core.split("\n")[0:8] if core else complete[:600])

    above = ""
    if level < 5:
        above = (
            f"## Out of scope above L{level}\n"
            f"Do **not** implement L{level + 1}…L5 behaviors in this factory pass.\n"
        )

    return (
        f"---\nlevel: {level}\nrow_id: {row_id}\nlabel: {label}\n"
        f"derived_from: L5\nscope_kind: depth_slice\n---\n\n"
        f"# {label} — depth {level} scope\n\n"
        f"## Level contract\n{charter_line or f'Global depth level {level}'}\n\n"
        f"## Vision at this depth\n{vision_block.strip()}\n\n"
        f"{above}"
    ).strip() + "\n"


def slice_l5_to_levels(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    bootstrap: bool = True,
) -> dict[str, Any]:
    """
    Top-down depth slicer: L5 complete vision → L4..L1 manageable scope files.

    Operator/agent authors L5 first; harness writes derived level scopes.
    """
    vault_root = vault_root.resolve()
    if bootstrap:
        bootstrap_l5_scope(vault_root, project_id=project_id, row_id=row_id)

    l5_path = scope_path(vault_root, project_id, row_id, 5)
    if not l5_path.is_file():
        return {"ok": False, "detail": "l5_missing", "row_id": row_id}

    catalog = load_yaml(user_story_paths(vault_root, project_id)["catalog"])
    row = catalog_rows_by_id(catalog).get(row_id) or {}
    label = str(row.get("label") or row_id)
    l5_text = l5_path.read_text(encoding="utf-8", errors="replace")
    charter = load_charter_level_lines(vault_root, project_id)

    written: list[str] = []
    out_dir = scope_dir(vault_root, project_id, row_id)
    out_dir.mkdir(parents=True, exist_ok=True)

    for level in LEVELS:
        if level == 5:
            # L5 is the operator/factory source document — never derive-overwrite it.
            written.append(str(l5_path.relative_to(vault_root)))
            continue
        body = _level_body(
            level=level,
            row_id=row_id,
            label=label,
            l5_text=l5_text,
            charter_line=charter.get(level, ""),
        )
        rel = scope_path(vault_root, project_id, row_id, level)
        if level < 5 and rel.is_file():
            old = rel.read_text(encoding="utf-8")
            if "<!-- operator-edited: true -->" in old:
                continue
        rel.write_text(body, encoding="utf-8")
        written.append(str(rel.relative_to(vault_root)))

    return {
        "ok": True,
        "row_id": row_id,
        "l5_path": str(l5_path.relative_to(vault_root)),
        "written": written,
        "detail": "depth_sliced",
    }


def slice_all_catalog_rows(
    vault_root: Path,
    *,
    project_id: str,
    row_ids: list[str] | None = None,
    bootstrap: bool = True,
) -> dict[str, Any]:
    catalog = load_yaml(user_story_paths(vault_root, project_id)["catalog"])
    by_id = catalog_rows_by_id(catalog)
    ids = row_ids or list(by_id.keys())
    results: list[dict[str, Any]] = []
    for rid in ids:
        results.append(
            slice_l5_to_levels(vault_root, project_id=project_id, row_id=rid, bootstrap=bootstrap)
        )
    ok = all(r.get("ok") for r in results) if results else False
    return {"ok": ok, "results": results, "row_count": len(results)}


def factory_feed_objective(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    dispatch_depth: int,
    pin_excerpt: str = "",
) -> str:
    """Level-scoped factory food; pin excerpt only as fallback."""
    scope = load_scope_body(vault_root, project_id, row_id, dispatch_depth)
    if scope:
        return scope[:2400]
    if pin_excerpt:
        return (
            f"## Depth {dispatch_depth} (scope file missing — pin fallback)\n\n"
            f"{pin_excerpt[:1600]}"
        )
    return f"Implement catalog row `{row_id}` at depth {dispatch_depth}. Author L5 + run depth slicer."
