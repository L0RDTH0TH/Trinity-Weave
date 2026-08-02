"""Per-noun mint walk files under scopes/<parent>/children-of-<parent>/<child>/WALK.md."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from .catalog_io import user_story_paths

_WALK_FIELD_RE = re.compile(r"^- ([a-z0-9_]+):\s*(.*)$", re.MULTILINE)
_ITEM_KEYS = (
    "status",
    "walk_tier",
    "mint_lane",
    "parent_id",
    "depth_band",
    "fanout",
    "depends_on",
    "historical_id",
    "series_id",
    "series_order",
    "series_walk_rank",
    "altitude",
    "seat",
    "time_scale",
    "does_not_mandate",
    "alternatives_not_banned",
    "catalog_face",
    "experience_mode",
    "mode_tier",
    "dnd_pillar",
    "ux_axis",
    "dimension",
    "summary",
    "pillar_notes",
    "conceptual_pin",
    "derived_from",
    "ux_family",
    "supplement",
    "coverage_slot",
    "maps_to",
    "notes",
    "label",
)


def children_of_dirname(parent_id: str) -> str:
    pid = str(parent_id or "").strip() or "_unparented"
    return f"children-of-{pid}"


def series_walk_path(scopes_dir: Path, series_id: str) -> Path:
    return scopes_dir / str(series_id).strip() / "SERIES.md"


def child_walk_path(scopes_dir: Path, parent_id: str, child_id: str) -> Path:
    parent = str(parent_id or "").strip() or "_unparented"
    return scopes_dir / parent / children_of_dirname(parent) / str(child_id).strip() / "WALK.md"


def walk_tree_present(scopes_dir: Path) -> bool:
    if not scopes_dir.is_dir():
        return False
    if any(scopes_dir.glob("*/SERIES.md")):
        return True
    if any(scopes_dir.glob("*/children-of-*/**/WALK.md")):
        return True
    return False


def render_walk_card(item: dict[str, Any]) -> str:
    iid = str(item.get("id") or "").strip()
    label = str(item.get("label") or iid).strip()
    walk = str(item.get("walk_tier") or "coverage")
    parent = str(item.get("parent_id") or "").strip()
    fm = {
        "title": f"{'Series' if walk == 'series' else 'Walk'} — {iid}",
        "row_id": iid,
        "parent_id": parent or None,
        "walk_tier": walk,
        "label": label,
        "status": str(item.get("status") or "pending"),
    }
    # drop None
    fm = {k: v for k, v in fm.items() if v is not None}
    body_lines = [f"# `{iid}` — {label}", ""]
    for key in _ITEM_KEYS:
        if key == "label":
            continue
        val = item.get(key)
        if val is None:
            continue
        if isinstance(val, (list, dict)):
            text = json.dumps(val, ensure_ascii=False)
        else:
            text = str(val).replace("\n", " ").strip()
        if text == "" and not isinstance(val, (list, dict)):
            continue
        if isinstance(val, bool):
            text = "true" if val else "false"
        body_lines.append(f"- {key}: {text}")
    body_lines.append("")
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n\n" + "\n".join(body_lines)


def parse_walk_card(text: str, *, fallback_id: str = "") -> dict[str, Any]:
    fm: dict[str, Any] = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            try:
                parsed = yaml.safe_load(text[3:end].strip()) or {}
                if isinstance(parsed, dict):
                    fm = parsed
            except Exception:
                fm = {}
            body = text[end + 4 :].lstrip("\n")

    fields: dict[str, str] = {}
    for m in _WALK_FIELD_RE.finditer(body):
        fields[m.group(1)] = m.group(2).strip()

    iid = str(fm.get("row_id") or fields.get("id") or fallback_id).strip()
    label = str(fm.get("label") or fields.get("label") or iid).strip()
    item: dict[str, Any] = {
        "id": iid,
        "label": label,
        "status": str(fm.get("status") or fields.get("status") or "pending"),
        "walk_tier": str(fm.get("walk_tier") or fields.get("walk_tier") or "coverage"),
        "dimension": fields.get("dimension") or "",
        "ux_axis": fields.get("ux_axis") or "",
        "summary": fields.get("summary") or "",
        "conceptual_pin": fields.get("conceptual_pin") or "",
        "derived_from": fields.get("derived_from") or "",
        "ux_family": fields.get("ux_family") or "",
    }
    parent = fm.get("parent_id") or fields.get("parent_id")
    if parent:
        item["parent_id"] = str(parent).strip()

    for extra in _ITEM_KEYS:
        if extra in item and extra not in ("status", "walk_tier", "label"):
            continue
        raw = fields.get(extra)
        if raw is None or raw == "":
            continue
        if extra in ("seat", "does_not_mandate", "alternatives_not_banned", "depends_on") and raw.strip().startswith("["):
            try:
                parsed = json.loads(raw)
                item[extra] = parsed if isinstance(parsed, list) else raw
                continue
            except Exception:
                try:
                    parsed = yaml.safe_load(raw)
                    item[extra] = parsed if isinstance(parsed, list) else raw
                    continue
                except Exception:
                    pass
        if extra in ("series_order", "depth_band", "series_walk_rank"):
            try:
                item[extra] = int(raw)
                continue
            except (TypeError, ValueError):
                pass
        if extra in ("supplement", "coverage_slot", "feedstock_hit"):
            item[extra] = str(raw).strip().lower() in {"true", "1", "yes"}
            continue
        item[extra] = raw
    return item


def write_item_walk_file(scopes_dir: Path, item: dict[str, Any]) -> Path:
    iid = str(item.get("id") or "").strip()
    if not iid:
        raise ValueError("item missing id")
    walk = str(item.get("walk_tier") or "")
    if walk == "series":
        path = series_walk_path(scopes_dir, iid)
    else:
        parent = str(item.get("parent_id") or "").strip() or "_unparented"
        path = child_walk_path(scopes_dir, parent, iid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_walk_card(item), encoding="utf-8")
    return path


def sync_all_walk_files(vault_root: Path, project_id: str, doc: dict[str, Any]) -> list[Path]:
    scopes = user_story_paths(vault_root, project_id)["scopes_dir"]
    written: list[Path] = []
    for it in doc.get("items") or []:
        if not isinstance(it, dict) or not str(it.get("id") or "").strip():
            continue
        written.append(write_item_walk_file(scopes, it))
    written.extend(sync_batch_digests(vault_root, project_id, doc))
    return written


def load_items_from_walk_files(scopes_dir: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if not scopes_dir.is_dir():
        return items
    for series_md in sorted(scopes_dir.glob("*/SERIES.md")):
        items.append(parse_walk_card(series_md.read_text(encoding="utf-8"), fallback_id=series_md.parent.name))
    for walk_md in sorted(scopes_dir.glob("*/children-of-*/**/WALK.md")):
        child_id = walk_md.parent.name
        items.append(parse_walk_card(walk_md.read_text(encoding="utf-8"), fallback_id=child_id))
    # de-dupe by id (SERIES wins if collision)
    by_id: dict[str, dict[str, Any]] = {}
    for it in items:
        iid = str(it.get("id") or "").strip()
        if not iid:
            continue
        if iid in by_id and str(by_id[iid].get("walk_tier")) == "series":
            continue
        by_id[iid] = it
    return list(by_id.values())


def split_backlog_doc_to_walk_dirs(vault_root: Path, project_id: str, doc: dict[str, Any]) -> dict[str, Any]:
    """Write walk tree from doc; mark doc as split; return updated doc."""
    sync_all_walk_files(vault_root, project_id, doc)
    out = dict(doc)
    out["walk_defs_split"] = True
    out["walk_defs_layout"] = "scopes/<parent>/children-of-<parent>/<child>/WALK.md"
    return out


_RESIDUE_MARKERS = (
    "Feedstock:",
    "Nearest context:",
    "Pillars:",
    "roleplay: (infer",
    "combat: (infer",
    "exploration: (infer",
)


def summary_has_residue(text: str) -> bool:
    s = str(text or "")
    if any(m in s for m in _RESIDUE_MARKERS):
        return True
    if "- label:" in s and "summary:" in s.lower():
        return True
    return False


def _anti_mandate_list(item: dict[str, Any]) -> list[str]:
    raw = item.get("does_not_mandate")
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
        except Exception:
            pass
        return [raw.strip()]
    return []


def batch_digest_path(scopes_dir: Path, parent_id: str) -> Path:
    return scopes_dir / str(parent_id).strip() / "BATCH-DIGEST.md"


def render_batch_digest(
    parent: dict[str, Any] | None,
    children: list[dict[str, Any]],
    *,
    parent_id: str,
) -> str:
    """Receipt-first digest for one-turn Pass B validation."""
    parent = parent or {}
    pid = str(parent_id or parent.get("id") or "").strip() or "_unparented"
    plabel = str(parent.get("label") or pid).strip()
    psum = str(parent.get("summary") or "").replace("\n", " ").strip()
    p_anti = _anti_mandate_list(parent)
    lines = [
        "---",
        f"title: Batch digest — {pid}",
        f"parent_id: {pid}",
        "walk_surface: batch_digest",
        "---",
        "",
        f"# Batch digest — `{pid}`",
        "",
        f"**Parent:** {plabel}",
        f"**Contract:** {psum or '(missing series summary)'}",
        "",
        "**Parent does_not_mandate (inherit — do not re-litigate):**",
    ]
    if p_anti:
        for a in p_anti:
            lines.append(f"- {a}")
    else:
        lines.append("- _(none listed)_")
    lines.extend(
        [
            "",
            "Open full `children-of-*/<child>/WALK.md` **only** for yellow / red / thin ids.",
            "Primary fields below: `summary` + `does_not_mandate`.",
            "",
            "| id | status | summary_residue | anti_mandate_n | summary | does_not_mandate |",
            "|----|--------|-----------------|----------------|---------|------------------|",
        ]
    )
    for ch in sorted(children, key=lambda i: str(i.get("id") or "")):
        if not isinstance(ch, dict):
            continue
        cid = str(ch.get("id") or "").strip()
        if not cid:
            continue
        status = str(ch.get("status") or "pending")
        summary = str(ch.get("summary") or "").replace("\n", " ").replace("|", "\\|").strip()
        anti = _anti_mandate_list(ch)
        residue = "yes" if summary_has_residue(summary) else "no"
        anti_s = "; ".join(anti).replace("|", "\\|") if anti else ""
        lines.append(
            f"| `{cid}` | {status} | {residue} | {len(anti)} | {summary} | {anti_s} |"
        )
    lines.append("")
    return "\n".join(lines)


def sync_batch_digests(vault_root: Path, project_id: str, doc: dict[str, Any]) -> list[Path]:
    """Write BATCH-DIGEST.md under each parent that has coverage children."""
    scopes = user_story_paths(vault_root, project_id)["scopes_dir"]
    items = [i for i in (doc.get("items") or []) if isinstance(i, dict)]
    by_id = {str(i.get("id") or "").strip(): i for i in items if str(i.get("id") or "").strip()}
    children_by_parent: dict[str, list[dict[str, Any]]] = {}
    for it in items:
        walk = str(it.get("walk_tier") or "")
        if walk == "series":
            continue
        parent = str(it.get("parent_id") or "").strip() or "_unparented"
        children_by_parent.setdefault(parent, []).append(it)
    written: list[Path] = []
    for parent_id, kids in sorted(children_by_parent.items()):
        parent = by_id.get(parent_id)
        path = batch_digest_path(scopes, parent_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            render_batch_digest(parent, kids, parent_id=parent_id),
            encoding="utf-8",
        )
        written.append(path)
    return written
