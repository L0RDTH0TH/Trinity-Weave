"""Vault-wide ticket-map schema — discover, parse, filter, sort.

Cite: 3-Resources/Second-Brain/Docs/Ticket-Map-Schema.md
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

# No product-map filename hardwire. Active map = factory-project.yaml
# ticket_map_runtime → :func:`resolve_active_ticket_map_rel` (fail-closed on None).

TICKET_STATUSES = frozenset({"open", "f5_good", "deferred", "superseded"})
MAP_STATUSES = frozenset({"active", "deferred", "complete"})
HIDDEN_TICKET_STATUSES = frozenset({"deferred", "superseded"})
SELECTABLE_TICKET_STATUS = "open"
GREYED_TICKET_STATUS = "f5_good"
OBSERVE_VALUES = frozenset({"person", "record"})
TOUCH_VALUES = frozenset({"f5", "none"})

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)

# Canonical: | `id` | status | job | notes | observe | touch |
# observe is person|record; touch is f5|none and must match observe.
# Ticketment / status stamp must not rewrite either cell.
# Back-compat: observe-only (no touch) still parses.
_ROW_STATUS_RE = re.compile(
    r"^\|\s*`(?P<id>[A-Za-z0-9][A-Za-z0-9_-]*)`(?:\s*\([^)]*\))?\s*\|"
    r"\s*`?(?P<status>open|f5_good|deferred|superseded)`?\s*\|"
    r"\s*(?P<job>[^|]*?)\s*\|"
    r"\s*(?P<notes>[^|]*?)\s*\|"
    r"(?:\s*`?(?P<observe>person|record)`?\s*\|"
    # Touch may be empty on a Touch table (Gate A missing_touch); do not invent f5|none.
    r"(?:\s*`?(?P<touch>f5|none)?`?\s*\|)?)?\s*$",
    re.M | re.I,
)

# Legacy 3-col: | `id` | job | notes |  (no status token in col2)
_ROW_LEGACY_RE = re.compile(
    r"^\|\s*`(?P<id>[A-Za-z0-9][A-Za-z0-9_-]*)`(?:\s*\([^)]*\))?\s*\|"
    r"\s*(?P<job>[^|]*?)\s*\|"
    r"\s*(?P<notes>[^|]*?)\s*\|\s*$",
    re.M,
)

# 4-col fidelity tables: | `id` | fidelity | job | proof |
_ROW_FIDELITY_RE = re.compile(
    r"^\|\s*`(?P<id>[A-Za-z0-9][A-Za-z0-9_-]*)`(?:\s*\([^)]*\))?\s*\|"
    r"\s*(?P<fidelity>[^|]*?)\s*\|"
    r"\s*(?P<job>[^|]*?)\s*\|"
    r"\s*(?P<notes>[^|]*?)\s*\|\s*$",
    re.M,
)

_HEADER_SKIP = frozenset(
    {
        "ticket",
        "product job",
        "notes",
        "status",
        "fidelity",
        "welds",
        "player-visible proof",
        "keep only if",
        "row",
        "was",
        "now",
        "observe",
        "touch",
    }
)


@dataclass
class MapTicketRow:
    ticket_map_id: str
    product_job: str
    welds: str
    status: str = "open"
    source_line: str = ""
    # Nearest ``##`` heading above the table row (empty if none).
    section_heading: str = ""
    # person | record — human-authored; generators must not edit.
    observe: str = ""
    # f5 | none — matches observe (person→f5, record→none); generators must not edit.
    touch: str = ""

    @property
    def proof_blob(self) -> str:
        return f"{self.product_job} {self.welds}".strip()

    @property
    def notes(self) -> str:
        return self.welds

    @property
    def section_key(self) -> str:
        """Section bucket for Ticketment neighbors; whole-map when unsectioned."""
        return (self.section_heading or "").strip() or "__map__"


@dataclass
class TicketMapDoc:
    path: Path
    rel_path: str
    map_id: str
    title: str
    project_id: str
    map_status: str
    created: str = ""
    updated: str = ""
    active_recovery: str = ""
    active_recovery_slice: str = ""
    tickets: dict[str, MapTicketRow] = field(default_factory=dict)
    ticket_order: list[str] = field(default_factory=list)
    frontmatter: dict[str, Any] = field(default_factory=dict)

    @property
    def sort_key(self) -> str:
        return self.updated or self.created or "1970-01-01"

    def map_rank(self, ticket_map_id: str) -> int:
        try:
            return self.ticket_order.index(ticket_map_id)
        except ValueError:
            return 10_000


@dataclass
class LivePickerRow:
    """One Prefer armed packet joined to a map ticket row.

    System still resolves by ticket_map_id; open drafts may list multiple
    slices (r1/r2/…). Trail (``f5_good``) collapses to one row per ticket —
    the Prefer with the latest F5/close timestamp — sorted newest-first.

    ``map_fidelity_hostile_ok`` is Gate B₁ from ``*.prefer-result.json``
    (cached at join time). Launchable requires map Status ``open`` **and**
    B₁ true — Prefer drafts are not factory tickets until B₁ passes.
    """

    ticket: MapTicketRow
    slice_id: str
    armed_path: str
    armed: dict[str, Any]
    mtime: float = 0.0
    map_fidelity_hostile_ok: bool = False
    # Unix epoch for trail sort (operator F5 / completed / closed); 0 if unknown
    trail_at: float = 0.0

    @property
    def ticket_map_id(self) -> str:
        return self.ticket.ticket_map_id

    @property
    def status(self) -> str:
        return self.ticket.status

    @property
    def launchable(self) -> bool:
        return (
            (self.ticket.status or "").lower() == SELECTABLE_TICKET_STATUS
            and self.map_fidelity_hostile_ok is True
        )

    @property
    def b1_pending(self) -> bool:
        """Open Prefer-linked row that has not passed Gate B₁ (draft)."""
        return (
            (self.ticket.status or "").lower() == SELECTABLE_TICKET_STATUS
            and self.map_fidelity_hostile_ok is not True
        )

    @property
    def trail(self) -> bool:
        return (self.ticket.status or "").lower() == GREYED_TICKET_STATUS


def _parse_iso_epoch(value: Any) -> float:
    """Best-effort ISO-8601 → UTC epoch seconds; 0 if unparseable."""
    if value is None:
        return 0.0
    s = str(value).strip()
    if not s:
        return 0.0
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return 0.0
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def prefer_trail_at(
    vault_root: Path,
    slice_id: str,
    armed_path: str | Path,
    armed: dict[str, Any] | None = None,
    *,
    fallback_mtime: float = 0.0,
) -> float:
    """When this Prefer step closed for trail ordering (newest first).

    Preference (prefer-result then armed): ``operator_f5_at`` → ``completed_at``
    → ``closed_at`` → ``greenlit_at`` → ``armed_at``, then file mtime.
    Do **not** prefer raw mtime over historical armed stamps — touching an
    armed file for ``ticket_map_id`` must not float a KEEP above a newer F5.
    """
    vault_root = vault_root.resolve()
    ap = Path(armed_path)
    if not ap.is_absolute():
        ap = vault_root / ap
    armed = armed if isinstance(armed, dict) else {}
    result: dict[str, Any] = {}
    sid = (slice_id or "").strip()
    if sid:
        pr = ap.parent / f"{sid}.prefer-result.json"
        if pr.is_file():
            try:
                data = json.loads(pr.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, ValueError):
                data = None
            if isinstance(data, dict):
                result = data
    receipt_fm: dict[str, str] = {}
    if sid:
        receipt = ap.parent / f"{sid}.receipt.md"
        if receipt.is_file():
            try:
                head = receipt.read_text(encoding="utf-8")[:4000]
            except OSError:
                head = ""
            for key in (
                "operator_f5_at",
                "completed_at",
                "closed_at",
                "greenlit_at",
                "armed_at",
            ):
                m = re.search(rf"(?m)^{key}:\s*['\"]?([^\n'\"]+)", head)
                if m:
                    receipt_fm[key] = m.group(1).strip()

    def _from_sources(key: str) -> float:
        for src in (result, armed, receipt_fm):
            epoch = _parse_iso_epoch(src.get(key) if isinstance(src, dict) else None)
            if epoch > 0:
                return epoch
        return 0.0

    # Close/F5 stamps beat greenlit/armed (receipt may hold F5 after weld greenlit)
    for key in ("operator_f5_at", "completed_at", "closed_at"):
        epoch = _from_sources(key)
        if epoch > 0:
            return epoch
    for key in ("greenlit_at", "armed_at"):
        epoch = _from_sources(key)
        if epoch > 0:
            return epoch
    if fallback_mtime > 0:
        return float(fallback_mtime)
    try:
        return float(ap.stat().st_mtime)
    except OSError:
        return 0.0


def prefer_b1_ok(
    vault_root: Path,
    slice_id: str,
    armed_path: str | Path,
) -> bool:
    """Gate B₁ fail-closed for factory launch.

    True only when prefer-result was stored by Trinity after a senior
    ``agent -p`` invoke (``source: cursor_senior_b1``, ``trinity_stamped: true``).
    Bare author ok, disk-shaped JSON without Trinity stamp, and ``harness_b1``
    are ignored.
    """
    from .prefer_map_fidelity import load_armed_yaml
    from .prefer_senior_gates import senior_pass_ok

    vault_root = vault_root.resolve()
    ap = Path(armed_path)
    if not ap.is_absolute():
        ap = vault_root / ap
    sid = (slice_id or "").strip()
    if not sid:
        return False
    armed: dict | None = None
    if ap.is_file():
        try:
            armed = load_armed_yaml(ap)
        except (OSError, ValueError):
            armed = None
    pr = ap.parent / f"{sid}.prefer-result.json"
    if not pr.is_file():
        return False
    try:
        data = json.loads(pr.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError):
        return False
    if not isinstance(data, dict):
        return False
    return senior_pass_ok(data, gate="b1", armed=armed if isinstance(armed, dict) else None)


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    m = _FRONTMATTER_RE.match(text or "")
    if not m:
        return {}, text or ""
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    body = text[m.end() :]
    return data, body


def infer_ticket_status(job: str, notes: str) -> str:
    blob = f"{job} {notes}".lower()
    # Active Prefer / staging work wins over incidental "superseded" mentions
    # (e.g. "piggyback SUPERSEDED" on an open recovery ticket).
    if any(
        x in blob
        for x in (
            "prefer draft",
            "awaiting gate",
            "gate a+b pending",
            "staging awaiting f5",
            "claim_class: staging",
            "claim_class staging",
        )
    ):
        return "open"
    if any(
        x in blob
        for x in (
            "*(superseded)*",
            "incomplete / superseded",
            "f5 fail superseded",
            "status: superseded",
            "**incomplete**",
        )
    ) or re.search(r"\bsuperseded by\b", blob):
        return "superseded"
    if notes.strip().lower().startswith("*(superseded)*") or job.strip().lower().startswith(
        "*(superseded)*"
    ):
        return "superseded"
    if any(
        x in blob
        for x in (
            "nursery parked",
            "keep-debt",
            "keep debt",
            "do not implement",
            "effect deferred",
            "parked until",
            "stay parked",
            "**parked**",
            "parked —",
        )
    ):
        return "deferred"
    if any(
        x in blob
        for x in (
            "keep-real",
            "operator f5 pass",
            "ask_success",
            "keep / ask_success",
        )
    ):
        return "f5_good"
    if "staging" in blob and "keep-real" not in blob:
        return "open"
    return "open"


def parse_ticket_map_rows(map_text: str) -> dict[str, MapTicketRow]:
    """Parse markdown tables into ticket_map_id → MapTicketRow (last wins)."""
    rows, _order = parse_ticket_map_rows_ordered(map_text)
    return rows


_SECTION_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)


def _section_heading_at(scan: str, pos: int) -> str:
    """Nearest ``##`` heading at or before ``pos`` (empty if none)."""
    heading = ""
    for m in _SECTION_HEADING_RE.finditer(scan):
        if m.start() <= pos:
            heading = m.group(1).strip()
        else:
            break
    return heading


def parse_ticket_map_rows_ordered(
    map_text: str,
) -> tuple[dict[str, MapTicketRow], list[str]]:
    """Parse tables; return rows + first-seen ticket order (map concordance)."""
    rows: dict[str, MapTicketRow] = {}
    order: list[str] = []
    body = map_text or ""
    _, body_only = _parse_frontmatter(body)
    scan = body_only if body_only != body or body.startswith("---") else body

    def _skip_job(job: str) -> bool:
        j = job.strip().lower()
        return j in _HEADER_SKIP or j in {"product job", "fidelity", "was", "now"}

    def _put(tid: str, row: MapTicketRow) -> None:
        if tid not in rows:
            order.append(tid)
        rows[tid] = row

    for m in _ROW_STATUS_RE.finditer(scan):
        tid = m.group("id").strip()
        status = m.group("status").strip().lower()
        job = " ".join(m.group("job").split())
        notes = " ".join(m.group("notes").split())
        obs_raw = m.groupdict().get("observe") or ""
        observe = str(obs_raw).strip().lower()
        if observe and observe not in OBSERVE_VALUES:
            observe = ""
        touch_raw = m.groupdict().get("touch") or ""
        touch = str(touch_raw).strip().lower()
        if touch and touch not in TOUCH_VALUES:
            touch = ""
        if _skip_job(job) or status not in TICKET_STATUSES:
            continue
        _put(
            tid,
            MapTicketRow(
                ticket_map_id=tid,
                product_job=job,
                welds=notes,
                status=status,
                source_line=m.group(0)[:200],
                section_heading=_section_heading_at(scan, m.start()),
                observe=observe,
                touch=touch,
            ),
        )

    for m in _ROW_FIDELITY_RE.finditer(scan):
        tid = m.group("id").strip()
        if tid in rows:
            continue
        fidelity = " ".join(m.group("fidelity").split())
        job = " ".join(m.group("job").split())
        notes = " ".join(m.group("notes").split())
        if fidelity.lower() in TICKET_STATUSES:
            continue
        if _skip_job(job) or fidelity.lower() in {"fidelity", "status", "was"}:
            continue
        if job.lower() in {"keep", "staging, generate = t"} and "keep-real" not in notes.lower():
            pass
        status = infer_ticket_status(fidelity + " " + job, notes)
        _put(
            tid,
            MapTicketRow(
                ticket_map_id=tid,
                product_job=job if len(job) > 12 else f"{fidelity} {job}".strip(),
                welds=notes,
                status=status,
                source_line=m.group(0)[:200],
                section_heading=_section_heading_at(scan, m.start()),
            ),
        )

    for m in _ROW_LEGACY_RE.finditer(scan):
        tid = m.group("id").strip()
        if tid in rows:
            continue
        job = " ".join(m.group("job").split())
        notes = " ".join(m.group("notes").split())
        if _skip_job(job):
            continue
        if job.lower() in TICKET_STATUSES:
            continue
        status = infer_ticket_status(job, notes)
        _put(
            tid,
            MapTicketRow(
                ticket_map_id=tid,
                product_job=job,
                welds=notes,
                status=status,
                source_line=m.group(0)[:200],
                section_heading=_section_heading_at(scan, m.start()),
            ),
        )

    return rows, order


def section_open_neighbor_ids(
    rows: dict[str, MapTicketRow],
    ticket_map_id: str,
) -> list[str]:
    """Other ``open`` tickets in the same section (sorted). Map-wide if unsectioned."""
    tid = (ticket_map_id or "").strip()
    row = rows.get(tid) or rows.get(tid.replace("_", "-"))
    if row is None:
        return []
    key = row.section_key
    out = [
        r.ticket_map_id
        for r in rows.values()
        if r.section_key == key
        and (r.status or "").lower() == SELECTABLE_TICKET_STATUS
        and r.ticket_map_id != row.ticket_map_id
    ]
    return sorted(out)


def load_ticket_map_doc(
    path: Path,
    *,
    vault_root: Path | None = None,
    require_flag: bool = True,
) -> TicketMapDoc | None:
    path = path.resolve()
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, _ = _parse_frontmatter(text)
    ticket_map_flag = bool(fm.get("ticket_map"))
    name_hint = "Ticket-Map" in path.name or "ticket-map" in path.name.lower()
    if require_flag and not ticket_map_flag and not name_hint:
        return None

    rel = str(path)
    if vault_root is not None:
        try:
            rel = str(path.relative_to(vault_root.resolve()))
        except ValueError:
            rel = path.name

    title = str(fm.get("title") or path.stem)
    map_id = str(fm.get("map_id") or path.stem).strip()
    project_id = str(fm.get("project-id") or fm.get("project_id") or "").strip()
    map_status = str(fm.get("map_status") or fm.get("status") or "active").strip().lower()
    if map_status not in MAP_STATUSES:
        # legacy status: active on note
        map_status = "active" if map_status in {"active", "staging", ""} else (
            "deferred" if map_status == "deferred" else "active"
        )

    tickets, ticket_order = parse_ticket_map_rows_ordered(text)
    return TicketMapDoc(
        path=path,
        rel_path=rel.replace("\\", "/"),
        map_id=map_id,
        title=title,
        project_id=project_id,
        map_status=map_status,
        created=str(fm.get("created") or "")[:32],
        updated=str(fm.get("updated") or fm.get("created") or "")[:32],
        active_recovery=str(fm.get("active_recovery") or "").strip(),
        active_recovery_slice=str(fm.get("active_recovery_slice") or "").strip(),
        tickets=tickets,
        ticket_order=ticket_order,
        frontmatter=fm,
    )


def discover_ticket_maps(
    vault_root: Path,
    *,
    include_deferred_maps: bool = False,
) -> list[TicketMapDoc]:
    """Find conforming ticket maps under 1-Projects and 3-Resources.

    Requires frontmatter ``ticket_map: true`` (schema Docs alone do not qualify).
    """
    vault_root = vault_root.resolve()
    found: dict[str, TicketMapDoc] = {}
    roots = [
        vault_root / "1-Projects",
        vault_root / "3-Resources",
    ]
    skip_name_bits = (
        ".receipt",
        "sync-conflict",
        "Ticket-Map-Schema",
    )
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            if any(p.startswith(".") for p in path.parts):
                continue
            name = path.name
            if any(b in name for b in skip_name_bits):
                continue
            try:
                text_head = path.read_text(encoding="utf-8", errors="replace")[:6000]
            except OSError:
                continue
            # Frontmatter flag only — avoid filename false positives
            if "ticket_map:" not in text_head[:800]:
                continue
            fm, _ = _parse_frontmatter(text_head)
            if not fm.get("ticket_map"):
                continue
            doc = load_ticket_map_doc(path, vault_root=vault_root, require_flag=True)
            if doc is None:
                continue
            if not doc.frontmatter.get("ticket_map"):
                continue
            if doc.map_status == "deferred" and not include_deferred_maps:
                continue
            found[doc.rel_path] = doc

    docs = list(found.values())
    docs.sort(key=lambda d: d.sort_key, reverse=True)
    return docs


def filter_tickets_for_picker(
    tickets: Iterable[MapTicketRow],
    *,
    show_hidden: bool = False,
) -> list[MapTicketRow]:
    """Legacy map-row filter (open + f5_good). Prefer build_live_picker_rows."""
    out: list[MapTicketRow] = []
    for t in tickets:
        st = (t.status or "open").lower()
        if st in HIDDEN_TICKET_STATUSES and not show_hidden:
            continue
        out.append(t)
    out.sort(
        key=lambda t: (
            0 if t.status == SELECTABLE_TICKET_STATUS else 1,
            t.ticket_map_id,
        )
    )
    return out


_MD_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_MD_CODE_RE = re.compile(r"`([^`]+)`")


def strip_job_markup(job: str) -> str:
    """Remove light markdown so picker lines stay scannable."""
    text = _MD_BOLD_RE.sub(r"\1", job or "")
    text = _MD_CODE_RE.sub(r"\1", text)
    return " ".join(text.split())


def format_picker_ticket_label(
    ticket: MapTicketRow,
    *,
    recovery_id: str = "",
    id_width: int = 22,
    job_max: int = 56,
    slice_id: str = "",
    slice_width: int = 0,
) -> str:
    """Id-first picker line: ★, ticket id, optional slice, short prose.

    Example: ``★ PLACE-product  ·  alpha0_…_r1  ·  Grey ghost → LMB…``
    ``f5_good`` trail rows prefix ``[f5_good]`` (primary visual trail).
    """
    job = strip_job_markup(ticket.product_job)
    if len(job) > job_max:
        job = job[: max(1, job_max - 1)] + "…"
    star = "★ " if recovery_id and ticket.ticket_map_id == recovery_id else "  "
    tid = ticket.ticket_map_id.ljust(id_width)
    st = (ticket.status or SELECTABLE_TICKET_STATUS).lower()
    slice_bit = ""
    if slice_id:
        sw = slice_width or len(slice_id)
        slice_bit = f"  ·  {slice_id.ljust(sw)}"
    mid = f"{tid}{slice_bit}  ·  {job}"
    if st == GREYED_TICKET_STATUS:
        return f"{star}[f5_good] {mid}"
    if st in HIDDEN_TICKET_STATUSES:
        return f"{star}[{st}] {mid}"
    return f"{star}{mid}"


def format_live_picker_label(
    row: LivePickerRow,
    *,
    recovery_id: str = "",
    id_width: int = 22,
    slice_width: int = 0,
    job_max: int = 48,
) -> str:
    return format_picker_ticket_label(
        row.ticket,
        recovery_id=recovery_id,
        id_width=id_width,
        job_max=job_max,
        slice_id=row.slice_id,
        slice_width=slice_width,
    )


def tickets_newest_first(
    tickets: list[MapTicketRow],
    *,
    recovery_id: str = "",
) -> list[MapTicketRow]:
    """Prefer recovery first among open; then open before f5_good; stable id reverse as proxy for recent."""
    def key(t: MapTicketRow) -> tuple:
        is_recovery = 1 if recovery_id and t.ticket_map_id == recovery_id else 0
        open_rank = 1 if t.status == SELECTABLE_TICKET_STATUS else 0
        return (is_recovery, open_rank, t.ticket_map_id)

    return sorted(tickets, key=key, reverse=True)


def _slice_briefs_dirs(vault_root: Path, project_id: str) -> list[Path]:
    candidates: list[Path] = []
    if not project_id:
        return candidates
    primary = vault_root / "1-Projects" / project_id / "Factory-DRB" / "slice-briefs"
    if primary.is_dir():
        candidates.append(primary)
    proj = vault_root / "1-Projects" / project_id
    if proj.is_dir():
        for p in proj.rglob("slice-briefs"):
            if p.is_dir() and p not in candidates:
                candidates.append(p)
    return candidates


_WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]+)?\]\]")


def iter_armed_prefers(
    vault_root: Path,
    *,
    project_id: str,
) -> list[tuple[str, str, Path, dict[str, Any], float]]:
    """Scan project slice-briefs for *.armed.yaml that declare ticket_map_id.

    Returns list of (ticket_map_id, slice_id, armed_path, armed_dict, mtime).
    """
    vault_root = vault_root.resolve()
    out: list[tuple[str, str, Path, dict[str, Any], float]] = []
    for briefs in _slice_briefs_dirs(vault_root, project_id):
        for armed_path in briefs.glob("*.armed.yaml"):
            try:
                raw = yaml.safe_load(armed_path.read_text(encoding="utf-8")) or {}
            except (OSError, yaml.YAMLError):
                continue
            if not isinstance(raw, dict):
                continue
            tid = str(raw.get("ticket_map_id") or "").strip()
            if not tid:
                continue
            sid = str(raw.get("slice_id") or armed_path.name.replace(".armed.yaml", "")).strip()
            try:
                mtime = armed_path.stat().st_mtime
            except OSError:
                mtime = 0.0
            out.append((tid, sid, armed_path, raw, mtime))
    return out


def _armed_index_by_slice(
    vault_root: Path, project_id: str
) -> dict[str, tuple[Path, dict[str, Any], float]]:
    """slice_id → (armed_path, armed_dict, mtime) for all armed packets."""
    vault_root = vault_root.resolve()
    idx: dict[str, tuple[Path, dict[str, Any], float]] = {}
    for briefs in _slice_briefs_dirs(vault_root, project_id):
        for armed_path in briefs.glob("*.armed.yaml"):
            try:
                raw = yaml.safe_load(armed_path.read_text(encoding="utf-8")) or {}
            except (OSError, yaml.YAMLError):
                continue
            if not isinstance(raw, dict):
                continue
            sid = str(raw.get("slice_id") or armed_path.name.replace(".armed.yaml", "")).strip()
            if not sid:
                continue
            try:
                mtime = armed_path.stat().st_mtime
            except OSError:
                mtime = 0.0
            idx[sid] = (armed_path, raw, mtime)
    return idx


def _wiki_slice_ids(blob: str) -> list[str]:
    out: list[str] = []
    for m in _WIKI_LINK_RE.finditer(blob or ""):
        name = m.group(1).strip()
        if name.endswith(".receipt"):
            continue
        # Prefer slice notes are usually the bare slice_id
        if name and name not in out:
            out.append(name)
    return out


def build_live_picker_rows(
    vault_root: Path,
    map_doc: TicketMapDoc,
    *,
    show_hidden: bool = False,
) -> list[LivePickerRow]:
    """Map ∩ Prefer: armed packets linked to this map.

    Link paths:
    1) ``ticket_map_id`` on armed.yaml matches a map row
    2) Map Notes/job wiki-link to a slice whose ``*.armed.yaml`` exists
       (covers older Prefer that omit ticket_map_id)

    - Launchable: map Status ``open`` **and** Gate B₁
      (``map_fidelity_hostile_ok: true`` in prefer-result.json).
    - Default list: omit open Prefer drafts that fail B₁ (not yet tickets).
    - With ``show_hidden`` / ``--all-tickets``: may include B₁-pending opens
      (caller disables them); ``f5_good`` trail unchanged.
    - Primary trail: map Status ``f5_good`` Prefer-linked rows (greyed).
    - Trail collapses to **one Prefer per ticket_map_id** (latest F5/close).
    - Trail order = steps taken: **newest F5 first** (not map tip→tail grouping).
    - Open seats may still list multiple armed slices (draft revisions).
    - Naked map rows without Prefer do not appear.
    """
    vault_root = vault_root.resolve()
    by_slice = _armed_index_by_slice(vault_root, map_doc.project_id)
    # (ticket_map_id, slice_id) → LivePickerRow
    joined: dict[tuple[str, str], LivePickerRow] = {}

    def _add(map_row: MapTicketRow, sid: str, armed_path: Path, armed: dict, mtime: float) -> None:
        st = (map_row.status or "open").lower()
        if st in HIDDEN_TICKET_STATUSES and not show_hidden:
            return
        if st not in {SELECTABLE_TICKET_STATUS, GREYED_TICKET_STATUS} and not show_hidden:
            return
        b1 = prefer_b1_ok(vault_root, sid, armed_path)
        # Prefer + Gate A + B₁ = ticket. Open without B₁ is draft — omit by default.
        if st == SELECTABLE_TICKET_STATUS and not b1 and not show_hidden:
            return
        key = (map_row.ticket_map_id, sid)
        if key in joined:
            return
        rel = str(armed_path.relative_to(vault_root)).replace("\\", "/")
        # Ensure launch resolve sees ticket_map_id even on legacy armed
        armed_view = dict(armed)
        if not str(armed_view.get("ticket_map_id") or "").strip():
            armed_view["ticket_map_id"] = map_row.ticket_map_id
        trail_at = prefer_trail_at(
            vault_root, sid, armed_path, armed_view, fallback_mtime=mtime
        )
        joined[key] = LivePickerRow(
            ticket=map_row,
            slice_id=sid,
            armed_path=rel,
            armed=armed_view,
            mtime=mtime,
            map_fidelity_hostile_ok=b1,
            trail_at=trail_at,
        )

    for tid, sid, armed_path, armed, mtime in iter_armed_prefers(
        vault_root, project_id=map_doc.project_id
    ):
        map_row = map_doc.tickets.get(tid)
        if map_row is None:
            continue
        _add(map_row, sid, armed_path, armed, mtime)

    # Wiki-link join from map Notes (legacy Prefer without ticket_map_id field)
    for map_row in map_doc.tickets.values():
        blob = f"{map_row.product_job} {map_row.welds}"
        for link in _wiki_slice_ids(blob):
            hit = by_slice.get(link)
            if hit is None:
                continue
            armed_path, armed, mtime = hit
            sid = str(armed.get("slice_id") or link).strip()
            # If armed declares a different ticket_map_id, trust armed (already joined)
            declared = str(armed.get("ticket_map_id") or "").strip()
            if declared and declared != map_row.ticket_map_id:
                continue
            _add(map_row, sid, armed_path, armed, mtime)

    # Trail = one Prefer per ticket (latest close); open keeps multi-slice drafts.
    by_ticket_trail: dict[str, LivePickerRow] = {}
    open_rows: list[LivePickerRow] = []
    other_rows: list[LivePickerRow] = []
    for row in joined.values():
        st = (row.status or "").lower()
        if st == GREYED_TICKET_STATUS:
            prev = by_ticket_trail.get(row.ticket_map_id)
            if prev is None or row.trail_at >= prev.trail_at:
                by_ticket_trail[row.ticket_map_id] = row
        elif st == SELECTABLE_TICKET_STATUS:
            open_rows.append(row)
        else:
            other_rows.append(row)

    live = open_rows + list(by_ticket_trail.values()) + other_rows
    recovery = map_doc.active_recovery or ""

    def sort_key(row: LivePickerRow) -> tuple:
        st = (row.status or "").lower()
        is_recovery = 1 if recovery and row.ticket_map_id == recovery else 0
        if st == SELECTABLE_TICKET_STATUS:
            # Open / recovery first; tip→tail among opens
            return (2, is_recovery, -map_doc.map_rank(row.ticket_map_id), row.mtime, 0.0)
        if st == GREYED_TICKET_STATUS:
            # History: newest F5/close first (steps taken, reverse chrono)
            return (1, 0, row.trail_at, -map_doc.map_rank(row.ticket_map_id), row.mtime)
        return (0, 0, 0.0, -map_doc.map_rank(row.ticket_map_id), row.mtime)

    live.sort(key=sort_key, reverse=True)
    return live


def prefer_dict_from_live_row(
    vault_root: Path,
    row: LivePickerRow,
) -> dict[str, Any]:
    """Build resolve_prefer-shaped dict from an already-joined live row."""
    vault_root = vault_root.resolve()
    out: dict[str, Any] = {
        "slice_id": row.slice_id,
        "armed_path": row.armed_path,
        "prefer_result_path": "",
        "brief_path": "",
        "armed": row.armed,
        "prefer_result": None,
        "warnings": [],
    }
    armed_path = vault_root / row.armed_path
    brief = armed_path.parent / f"{row.slice_id}.md"
    if brief.is_file():
        out["brief_path"] = str(brief.relative_to(vault_root)).replace("\\", "/")
    pr = armed_path.parent / f"{row.slice_id}.prefer-result.json"
    if pr.is_file():
        out["prefer_result_path"] = str(pr.relative_to(vault_root)).replace("\\", "/")
        try:
            out["prefer_result"] = json.loads(pr.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, ValueError):
            out["prefer_result"] = None
    return out


def resolve_prefer_for_ticket(
    vault_root: Path,
    *,
    project_id: str,
    ticket_map_id: str,
    slice_hint: str = "",
) -> dict[str, Any]:
    """Join Prefer under project slice-briefs. Returns paths + loaded dicts."""
    vault_root = vault_root.resolve()
    out: dict[str, Any] = {
        "slice_id": "",
        "armed_path": "",
        "prefer_result_path": "",
        "brief_path": "",
        "armed": None,
        "prefer_result": None,
        "warnings": [],
    }
    if not project_id:
        out["warnings"].append("missing_project_id")
        return out

    matches: list[tuple[str, Path, dict[str, Any], float]] = []
    for tid, sid, armed_path, raw, mtime in iter_armed_prefers(
        vault_root, project_id=project_id
    ):
        if tid == ticket_map_id or (slice_hint and sid == slice_hint):
            matches.append((sid, armed_path, raw, mtime))

    if not matches and slice_hint:
        for briefs in _slice_briefs_dirs(vault_root, project_id):
            ap = briefs / f"{slice_hint}.armed.yaml"
            if ap.is_file():
                try:
                    raw = yaml.safe_load(ap.read_text(encoding="utf-8")) or {}
                except (OSError, yaml.YAMLError):
                    raw = {}
                if isinstance(raw, dict):
                    try:
                        mtime = ap.stat().st_mtime
                    except OSError:
                        mtime = 0.0
                    matches.append((slice_hint, ap, raw, mtime))

    if not matches:
        out["warnings"].append("prefer_missing")
        return out

    exact_tid = [
        m for m in matches if str(m[2].get("ticket_map_id") or "") == ticket_map_id
    ]
    pool = exact_tid or matches
    if slice_hint:
        by_slice = [m for m in pool if m[0] == slice_hint]
        if by_slice:
            pool = by_slice
    if len(pool) > 1 and not slice_hint:
        out["warnings"].append(f"ambiguous_prefer_matches:{len(pool)}")
    # Newest armed wins when ambiguous
    pool.sort(key=lambda m: m[3], reverse=True)
    sid, armed_path, armed, _mtime = pool[0]
    live = LivePickerRow(
        ticket=MapTicketRow(ticket_map_id, "", "", "open"),
        slice_id=sid,
        armed_path=str(armed_path.relative_to(vault_root)).replace("\\", "/"),
        armed=armed,
        mtime=_mtime,
    )
    return prefer_dict_from_live_row(vault_root, live)


def build_factory_weld_prompt(
    *,
    map_doc: TicketMapDoc,
    ticket: MapTicketRow,
    prefer: dict[str, Any],
) -> str:
    """Emit FACTORY GREENLIGHT WELD launch text for clipboard."""
    armed = prefer.get("armed") if isinstance(prefer.get("armed"), dict) else {}
    pr = prefer.get("prefer_result") if isinstance(prefer.get("prefer_result"), dict) else {}
    slice_id = prefer.get("slice_id") or map_doc.active_recovery_slice or ""
    live = str(armed.get("live_write_target") or "")
    do_not_arm = armed.get("do_not_arm_next") or armed.get("do_not_arm") or pr.get("do_not_arm") or []
    if isinstance(do_not_arm, str):
        do_not_arm = [do_not_arm]
    b1 = pr.get("map_fidelity_hostile_ok")
    b2 = pr.get("weld_intent_hostile_ok")
    greenlit = armed.get("factory_greenlit") or pr.get("factory_greenlit")
    welded = armed.get("live_weld_landed") or pr.get("live_weld_landed")

    warnings = list(prefer.get("warnings") or [])
    prefer_note = ""
    if "prefer_missing" in warnings:
        prefer_note = "Prefer missing — compose Prefer first (Gate A/B₁ before GREENLIGHT)."
    elif warnings:
        prefer_note = "Warnings: " + ", ".join(warnings)

    status_lines = [
        f"- map: {map_doc.title} (`{map_doc.map_id}`) project-id={map_doc.project_id} map_status={map_doc.map_status}",
        f"- ticket_map_id: `{ticket.ticket_map_id}` status={ticket.status}",
        f"- slice_id: `{slice_id or '(none)'}`",
        f"- Prefer armed: {prefer.get('armed_path') or '(none)'}",
        f"- B₁ map_fidelity_hostile_ok: {b1!r}",
        f"- B₂ weld_intent_hostile_ok: {b2!r}",
        f"- factory_greenlit: {greenlit!r} live_weld_landed: {welded!r}",
        f"- live_write_target: {live or '(from Prefer / factory-project)'}",
        f"- do_not_arm: {do_not_arm or '(none)'}",
    ]
    if prefer_note:
        status_lines.append(f"- NOTE: {prefer_note}")

    job = ticket.product_job
    return f"""FACTORY GREENLIGHT WELD — {ticket.ticket_map_id}

Path (binding, in order — do not skip):
1) Prefer authorship / Gate A (mechanical packet; map optional unless ticket_map_id set)
2) Gate B₁ Prefer hostile → map_fidelity_hostile_ok: true
   STOP if B₁ fails. Do not greenlight. Do not weld.
3) STOP for operator GREENLIGHT WELD (explicit). No weld without it.
4) Prefer-align (factory eat preflight before the implementation seat)
   Prefer ↔ identity / factory-project. Writes nothing. Does not rewrite Prefer or point configs.
   Empty behavior_keys, unnamed entries, host-law cite with empty host_law_ids,
   factory-project game_repo_path disagreeing with identity/Prefer, or umbrella pointing
   elsewhere → block. STOP if Prefer-align fails. Do not run the seat.
5) Weld LIVE (factory path only — named live_write_target; after Prefer-align ok)
6) Gate B₂ weld intent hostile → weld_intent_hostile_ok: true
   Evidence = behavior (required keys for ticket class). Tags/logs may indict, never acquit.
   Bare weld_intent_hostile_ok stamp = fail. Implementer {{key: true}} / agent evidence_pack = fail.
   Eat Success uses evaluate_behavior_evidence only (pass_basis: behavior). B₂ must not rewrite Prefer Success.
   STOP if B₂ fails → rework weld, re-run B₂. Do not ask for F5.
7) STOP for operator F5 (feel). No KEEP / ask_success / next_world_armed without F5.
8) After F5 pass: stamp map ticket Status → f5_good; bump map updated.
   KEEP / pointer only if A + B₁ + Prefer-align + B₂ + F5 (and map law).

Defaults:
- Default factory. Chat LIVE hotfix = STOP and ASK \"Skip factory Prefer+hostile and weld in chat?\"
  Bypass only on explicit yes + factory_bypass: true + factory_bypass_ack quote.
  Never factory_greenlit on bypass.
- Ticket map optional unless ticket_map_id is set (this launch has ticket_map_id).
- Do not arm: {", ".join(str(x) for x in do_not_arm) if do_not_arm else "(see Prefer)"}.

This run:
- map_id: {map_doc.map_id}
- map path: {map_doc.rel_path}
- ticket_map_id: {ticket.ticket_map_id}
- product job: {job}
- slice / Prefer: {prefer.get("brief_path") or prefer.get("armed_path") or "(compose Prefer)"}
- live target: {live or "(resolve from Prefer)"}
- out of scope: do not advance unrelated map pointers; do not arm listed do_not_arm

Status snapshot:
{chr(10).join(status_lines)}
"""


def resolve_active_ticket_map_rel(
    vault_root: Path,
    *,
    project_id: str | None = None,
    ticket_map_id: str | None = None,
) -> str | None:
    """Resolve vault-relative path of the active ticket map (no product hardwire).

    Order:
    1. ``factory-project.yaml`` → ``ticket_map_runtime.map_note`` (or ``map_path``)
    2. ``ticket_map_runtime.map_id`` matched via :func:`discover_ticket_maps`
    3. Sole active map under the project (or vault-wide if one)
    4. If ``ticket_map_id`` is set, the active map that contains that row
    5. ``None`` — caller fail-closes (never invent a mini-game path)
    """
    vault_root = vault_root.resolve()
    tid = (ticket_map_id or "").strip()

    # 1–2: project manifest socket
    try:
        from .factory_project import load_factory_project

        boot = load_factory_project(vault_root, project_id)
    except Exception:
        boot = {}
    runtime = boot.get("ticket_map_runtime") if isinstance(boot, dict) else None
    if isinstance(runtime, dict):
        note = str(
            runtime.get("map_note") or runtime.get("map_path") or ""
        ).strip().lstrip("/")
        if note and (vault_root / note).is_file():
            return note
        want_id = str(runtime.get("map_id") or "").strip()
        if want_id:
            for doc in discover_ticket_maps(vault_root):
                if doc.map_id == want_id:
                    return doc.rel_path

    # 3: sole active map (project-scoped when possible)
    docs = discover_ticket_maps(vault_root)
    pid = str(
        (boot.get("project_id") if isinstance(boot, dict) else None)
        or project_id
        or ""
    ).strip()
    if pid:
        scoped = [
            d
            for d in docs
            if d.rel_path.startswith(f"1-Projects/{pid}/")
            or str(d.frontmatter.get("project-id") or "") == pid
        ]
        if len(scoped) == 1:
            return scoped[0].rel_path
        docs = scoped or docs
    if len(docs) == 1:
        return docs[0].rel_path

    # 4: ticket id → owning active map
    if tid:
        for doc in docs:
            if tid in doc.tickets or tid.replace("_", "-") in doc.tickets:
                return doc.rel_path
    return None


def load_ticket_map_rows(
    vault_root: Path,
    *,
    map_rel: str | None = None,
    project_id: str | None = None,
    ticket_map_id: str | None = None,
) -> dict[str, MapTicketRow]:
    """Load ticket rows from an explicit map path or the active project map."""
    vault_root = vault_root.resolve()
    rel = (map_rel or "").strip().lstrip("/")
    if not rel:
        rel = resolve_active_ticket_map_rel(
            vault_root,
            project_id=project_id,
            ticket_map_id=ticket_map_id,
        ) or ""
    if not rel:
        return {}
    path = vault_root / rel
    if not path.is_file():
        return {}
    doc = load_ticket_map_doc(path, vault_root=vault_root, require_flag=False)
    if doc is not None:
        return doc.tickets
    return parse_ticket_map_rows(path.read_text(encoding="utf-8", errors="replace"))
