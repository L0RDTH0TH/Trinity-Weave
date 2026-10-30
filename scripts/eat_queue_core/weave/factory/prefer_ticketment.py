"""Ticketment draft bundle — load map context before Prefer / Gate A / B₁.

Does not weld. Builds the fixed read set for ``prefer-ticketment-draft``:

1. Active map from ``factory-project.yaml`` ``ticket_map_runtime`` only
2. Done-sentence + Order (short)
3. Section heading + charter above this table
4. This row verbatim
5. Other open rows in the same section as ``out_of_scope``
6. Nothing else (no mini-game archive, no dual-grid law unless place seat)

Cite: Prefer-Authorship-Host-Law · Ticket-Map-Schema.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .factory_project import load_factory_project
from .observe_class import person_observer_ready
from .ticket_map_schema import (
    load_ticket_map_doc,
    resolve_active_ticket_map_rel,
    section_open_neighbor_ids,
)


def _person_observer_ready(vault_root: Path) -> bool:
    return bool(person_observer_ready(vault_root))

_DONE_HEADING_RE = re.compile(
    r"^##\s+What done means\s*$", re.M | re.I
)
_ORDER_HEADING_RE = re.compile(r"^##\s+Order\b.*$", re.M | re.I)
_HIERARCHY_HEADING_RE = re.compile(r"^##\s+Hierarchy\b.*$", re.M | re.I)
_NEXT_H2_RE = re.compile(r"^##\s+", re.M)


def _section_body(text: str, heading_re: re.Pattern[str], *, max_chars: int = 1200) -> str:
    m = heading_re.search(text or "")
    if not m:
        return ""
    start = m.end()
    nxt = _NEXT_H2_RE.search(text, start)
    end = nxt.start() if nxt else len(text)
    body = text[start:end].strip()
    if len(body) > max_chars:
        body = body[: max_chars - 1].rstrip() + "…"
    return body


def _charter_above_section(text: str, section_heading: str) -> str:
    """Paragraph(s) between the ``##`` section heading and the first table."""
    if not section_heading:
        return ""
    pat = re.compile(
        rf"^##\s+{re.escape(section_heading)}\s*$", re.M
    )
    m = pat.search(text or "")
    if not m:
        return ""
    start = m.end()
    table = re.search(r"^\|", text[start:], re.M)
    end = start + table.start() if table else start
    body = text[start:end].strip()
    if len(body) > 800:
        body = body[:799].rstrip() + "…"
    return body


def build_ticketment_bundle(
    vault_root: Path,
    ticket_map_id: str,
    *,
    project_id: str | None = None,
) -> dict[str, Any]:
    """Return the Ticketment draft bundle for one ticket id (fail-closed)."""
    vault_root = vault_root.resolve()
    tid = (ticket_map_id or "").strip()
    boot = load_factory_project(vault_root, project_id)
    pid = str(boot.get("project_id") or project_id or "").strip()
    runtime = boot.get("ticket_map_runtime") if isinstance(boot.get("ticket_map_runtime"), dict) else {}
    map_rel = resolve_active_ticket_map_rel(
        vault_root, project_id=pid or None, ticket_map_id=tid or None
    )
    if not map_rel:
        return {
            "ok": False,
            "error": "active_ticket_map_unresolved",
            "ticket_map_id": tid,
            "project_id": pid,
        }
    path = vault_root / map_rel
    doc = load_ticket_map_doc(path, vault_root=vault_root)
    if doc is None:
        return {
            "ok": False,
            "error": "ticket_map_unreadable",
            "map_note": map_rel,
            "ticket_map_id": tid,
        }
    row = doc.tickets.get(tid) or doc.tickets.get(tid.replace("_", "-"))
    if row is None:
        return {
            "ok": False,
            "error": "ticket_not_on_map",
            "map_note": map_rel,
            "map_id": doc.map_id,
            "ticket_map_id": tid,
        }
    tid = row.ticket_map_id
    text = path.read_text(encoding="utf-8", errors="replace")
    oos = section_open_neighbor_ids(doc.tickets, tid)
    neighbors = [
        {
            "ticket_map_id": sid,
            "product_job": doc.tickets[sid].product_job,
            "out_of_scope": True,
        }
        for sid in oos
    ]
    place_markers = ("place", "dual", "stalberg", "coast", "lattice")
    is_place_seat = any(m in tid.lower() for m in place_markers)

    return {
        "ok": True,
        "project_id": pid,
        "map_id": str(runtime.get("map_id") or doc.map_id),
        "map_note": map_rel,
        "ignore_release_tier": True,
        "done_sentence": _section_body(text, _DONE_HEADING_RE, max_chars=900),
        "order": (
            _section_body(text, _ORDER_HEADING_RE, max_chars=700)
            or _section_body(text, _HIERARCHY_HEADING_RE, max_chars=700)
        ),
        "section_heading": row.section_heading,
        "section_charter": _charter_above_section(text, row.section_heading),
        "row": {
            "ticket_map_id": tid,
            "status": row.status,
            "product_job": row.product_job,
            "notes": row.welds,
            "observe": getattr(row, "observe", "") or "",
            "touch": getattr(row, "touch", "") or "",
        },
        "observe": getattr(row, "observe", "") or "",
        "touch": getattr(row, "touch", "") or "",
        "out_of_scope_ticket_ids": oos,
        "section_open_neighbors": neighbors,
        "load_dual_grid_host_law": is_place_seat,
        "required_prefer_fields": [
            "ticket_map_id",
            "structural_success",
            "out_of_scope_ticket_ids",
            "proof_shape",
            "claim_class",
            "behavior_keys",
            "do_not_waive",
        ],
        "person_observer_ready": _person_observer_ready(vault_root),
        "notes": (
            "Copy the row. structural_success = product_job verbatim only — "
            "never System or Walk. proof_shape/claim_class from observe. "
            "Touch is map-authored (f5|none); do not write Touch. "
            "f5 + person_observer_ready false → incomplete_missing_observer "
            "(empty checks + person missing_observer); do not arm; do not B1. "
            "none → harness record probe or stop; never person_window_pointer. "
            "Do not shop catalog stubs for Gate A. Do not set hostile ok bits. "
            "Do not FactoryEat; do not set factory_greenlit. "
            "B1 terminal → archive. B2 may cite Walk as gap question only."
        ),
    }
