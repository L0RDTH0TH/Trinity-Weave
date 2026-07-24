"""Feed envelope helpers — core vs thickeners; completeness flags; capped neighbors.

Does not reopen frozen conceptual. Neighbors are opt-in / bounded (no auto-flood).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, user_story_paths
from .depth_scope import scope_path
from .ux_mint_backlog import load_mint_backlog, next_pending_item

DEFAULT_NEIGHBOR_CAP = 3
THIN_EXCERPT_CHARS = 400


def resolve_neighbor_refs(
    vault_root: Path,
    *,
    project_id: str,
    focal_ids: list[str] | None = None,
    include_neighbors: bool = False,
    cap: int = DEFAULT_NEIGHBOR_CAP,
) -> list[dict[str, Any]]:
    """
    Optional thickeners: same ux_axis backlog siblings, then sequential backlog neighbors.

    Empty unless include_neighbors is True. Cap defaults to 3.
    """
    if not include_neighbors:
        return []
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    items = [i for i in (bl.get("items") or []) if isinstance(i, dict) and i.get("id")]
    if not items:
        return []

    focals = [str(x) for x in (focal_ids or []) if x]
    if not focals:
        nxt = next_pending_item(bl)
        if nxt and nxt.get("id"):
            focals = [str(nxt["id"])]
    if not focals:
        return []

    by_id = {str(i["id"]): i for i in items}
    ordered_ids = [str(i["id"]) for i in items]
    out: list[dict[str, Any]] = []
    seen: set[str] = set(focals)

    for fid in focals:
        focal = by_id.get(fid)
        if not focal:
            continue
        axis = str(focal.get("ux_axis") or "").strip()
        if axis:
            for it in items:
                iid = str(it["id"])
                if iid in seen:
                    continue
                if str(it.get("ux_axis") or "") == axis:
                    out.append(
                        {
                            "id": iid,
                            "reason": "same_ux_axis",
                            "ux_axis": axis,
                            "label": str(it.get("label") or ""),
                        }
                    )
                    seen.add(iid)
                    if len(out) >= cap:
                        return out[:cap]

        if fid in ordered_ids:
            idx = ordered_ids.index(fid)
            for j in (idx - 1, idx + 1):
                if 0 <= j < len(ordered_ids):
                    iid = ordered_ids[j]
                    if iid in seen:
                        continue
                    nbr = by_id[iid]
                    out.append(
                        {
                            "id": iid,
                            "reason": "backlog_adjacent",
                            "ux_axis": str(nbr.get("ux_axis") or ""),
                            "label": str(nbr.get("label") or ""),
                        }
                    )
                    seen.add(iid)
                    if len(out) >= cap:
                        return out[:cap]
    return out[:cap]


def assess_feed_completeness(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str | None = None,
) -> dict[str, Any]:
    """
    Lightweight flags — surfaces thin feed; does not mandate research.

    Flags: backlog_not_frozen, pin_excerpt_thin, conceptual_excerpt_thin,
    l5_missing, catalog_row_missing.
    """
    vault_root = vault_root.resolve()
    flags: list[str] = []
    detail: dict[str, Any] = {}

    bl = load_mint_backlog(vault_root, project_id)
    status = str(bl.get("backlog_status") or "proposed")
    if status != "frozen_for_mint":
        flags.append("backlog_not_frozen")
    detail["backlog_status"] = status

    from .catalog_mint_pack import PACK_DOCS_REL

    pack = vault_root / PACK_DOCS_REL / project_id
    conceptual = pack / "CONCEPTUAL-EXCERPT.md"
    if conceptual.is_file():
        body = conceptual.read_text(encoding="utf-8", errors="replace")
        # strip header lines roughly
        if len(body.strip()) < THIN_EXCERPT_CHARS or "Missing PMG" in body:
            flags.append("conceptual_excerpt_thin")
    else:
        flags.append("conceptual_excerpt_thin")

    rid = row_id
    if not rid:
        nxt = next_pending_item(bl)
        rid = str(nxt["id"]) if nxt else None
    detail["focal_id"] = rid

    if rid:
        paths = user_story_paths(vault_root, project_id)
        cat = load_yaml(paths["catalog"]) if paths["catalog"].is_file() else {"rows": []}
        by_id = catalog_rows_by_id(cat)
        if rid not in by_id and not any(
            str(i.get("id")) == rid for i in (bl.get("items") or []) if isinstance(i, dict)
        ):
            flags.append("catalog_row_missing")
        # pin excerpt thin: check PIN-EXCERPTS for conceptual_pin stem or empty dir
        excerpts = pack / "PIN-EXCERPTS"
        if excerpts.is_dir():
            files = list(excerpts.glob("*.md"))
            if not files:
                flags.append("pin_excerpt_thin")
            else:
                # any very short excerpt counts as thin pressure
                short = [p for p in files if p.stat().st_size < THIN_EXCERPT_CHARS]
                if len(short) == len(files):
                    flags.append("pin_excerpt_thin")
        else:
            flags.append("pin_excerpt_thin")

        l5 = scope_path(vault_root, project_id, rid, 5)
        if not l5.is_file():
            # Only flag l5_missing when row is already in catalog (Loop 2+)
            if rid in by_id:
                flags.append("l5_missing")
    else:
        flags.append("no_focal_item")

    thin = len(flags) > 0
    return {
        "ok": not thin or flags == ["backlog_not_frozen"],  # proposed alone is expected pre-prune
        "thin": thin,
        "flags": flags,
        "detail": detail,
        "research_hint": (
            "Consider influence or gap research enqueue if pin/UX feel thin "
            "(set enqueue_thin_feed_research=true to auto-hint)."
            if thin
            else ""
        ),
    }


def build_feed_envelope_doc(
    vault_root: Path,
    *,
    project_id: str,
    include_neighbors: bool = False,
    neighbor_cap: int = DEFAULT_NEIGHBOR_CAP,
    enqueue_thin_feed_research: bool = False,
) -> dict[str, Any]:
    """Pack-facing FEED-ENVELOPE.yaml payload."""
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    nxt = next_pending_item(bl)
    focal = str(nxt["id"]) if nxt else None
    neighbors = resolve_neighbor_refs(
        vault_root,
        project_id=project_id,
        focal_ids=[focal] if focal else None,
        include_neighbors=include_neighbors,
        cap=neighbor_cap,
    )
    completeness = assess_feed_completeness(vault_root, project_id=project_id, row_id=focal)
    research_enqueue_suggested = bool(
        enqueue_thin_feed_research
        and completeness.get("thin")
        and any(
            f in (completeness.get("flags") or [])
            for f in ("pin_excerpt_thin", "conceptual_excerpt_thin", "l5_missing")
        )
    )
    return {
        "schema_version": 1,
        "project_id": project_id,
        "core": [
            "CONCEPTUAL-EXCERPT.md",
            "MINT-BACKLOG.yaml",
            "PIN-INDEX.md",
            "Tech-Stack-Excerpt.yaml",
            "Stack-Domain-Registry-Excerpt.yaml",
            "slice-catalog.yaml",
        ],
        "thickeners": {
            "neighbor_refs": neighbors,
            "poll_index": "ROADMAP-RESOURCE-INDEX.yaml",
            "friction_check": "Docs/catalog-mint/_shared/FRICTION-CHECK.md",
            "rubric": "Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md",
        },
        "focal_pending_id": focal,
        "completeness": completeness,
        "research_enqueue_suggested": research_enqueue_suggested,
        "note": (
            "Core is always present. neighbor_refs stay empty unless include_neighbors "
            "was requested at pack emit — no auto-flood."
        ),
    }
