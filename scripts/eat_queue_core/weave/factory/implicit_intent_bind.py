"""Implicit-intent bind — entry seat maps colloquial asks to structural Success.

Fail-closed for Prefer / townscaper / tutorial worldgen slices: before IMPLEMENT_SLICE,
slice-producer (or factory entry) must emit an artifact that rewrites countable proxies
(e.g. "19 points") into lattice-graph Success and lists refuse codes.

Law: Factory-DRB/Prefer-Authorship-Host-Law.md § D · Grid-Topology-Host-Law.md
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .prefer_authorship_contract import (
    load_armed_packet,
    slice_requires_prefer_authorship,
)

BIND_SCHEMA_VERSION = 1
BIND_FILENAME = "implicit-intent-bind.json"

BASE_REFUSES: tuple[str, ...] = (
    "inspiration_shape_miss",
    "craft_cam_recenter_on_place",
    "craft_terrain_blend",
)

TOPOLOGY_REFUSES: tuple[str, ...] = (
    "points_as_grid",
    "count_equals_topology",
    "infinite_rect_as_hex19",
    "prop_scatter_as_composition",
)

_POINTS_GRID_RE = re.compile(
    r"\b(?:\d+\s*points?|point\s*cloud|hex[- ]?19|hexagonal\s+grid|"
    r"occupancy\s+(?:grid|lattice|markers?)|grid\s+of\s+points)\b",
    re.I,
)

# Refuse codes that arm the topology axis by law when locked in an armed packet.
ARMED_TOPOLOGY_REFUSES: tuple[str, ...] = (
    "points_as_grid",
    "count_equals_topology",
    "explicit_met_implicit_miss",
    "infinite_rect_as_hex19",
)

# Law text that names the lattice axis outright …
_LATTICE_WORD_RE = re.compile(r"\blattice\b|\btopolog\w*\b|hex[-_ ]?19", re.I)
# … or spells it out as vertices + edges + faces/cells.
_VERTEX_WORD_RE = re.compile(r"\bvert(?:ex|ices)\b|\bcorners?\b|\bscaffold\b", re.I)
_EDGE_WORD_RE = re.compile(r"\bedges?\b|\bneighbou?r\w*\b|\badjacen\w*\b", re.I)
_FACE_WORD_RE = re.compile(r"\bfaces?\b|\bcells?\b", re.I)

DEFAULT_STRUCTURAL_SUCCESS = (
    "Hex lattice graph: vertices (scaffold count) + neighbor edges + faces/cells; "
    "ghost snaps to a cell (or the vertex set that defines it); F5 shows a readable "
    "hex lattice of cells — not floating disks. Dual MeshLibrary / connectors / art "
    "out of scope until their ladder steps."
)

DEFAULT_INSPIRATION_CITES: tuple[str, ...] = (
    "https://www.youtube.com/watch?v=Y19Mw5YsgjI",
    "1-Projects/genesis-mythos-master/Factory-DRB/Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI.md",
    "1-Projects/genesis-mythos-master/Factory-DRB/Grid-Topology-Host-Law.md",
    "1-Projects/genesis-mythos-master/Factory-DRB/Prefer-Authorship-Host-Law.md",
    "1-Projects/genesis-mythos-master/Roadmap/User-Story/Inspiration-UX-Feedstock/cards/dual-grid-nested-placetile-world-authorship.md",
)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(value: Any) -> datetime | None:
    s = str(value or "").strip().strip("'\"")
    if not s:
        return None
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def slice_requires_implicit_bind(slice_id: str, job: dict[str, Any] | None = None) -> bool:
    """True when Prefer authorship applies or slice is townscaper / tutorial ladder."""
    if slice_requires_prefer_authorship(slice_id, job):
        return True
    blob = " ".join(
        [
            str(slice_id or ""),
            str((job or {}).get("ask_id") or ""),
            str((job or {}).get("series_id") or ""),
            str((job or {}).get("armed_packet_path") or ""),
        ]
    ).lower()
    return any(
        m in blob
        for m in (
            "townscaper",
            "tutorial_s",
            "dualgrid",
            "dual_grid",
            "occupancy",
            "worldgen",
        )
    )


def ask_triggers_topology_rewrite(text: str) -> bool:
    return bool(_POINTS_GRID_RE.search(text or ""))


def _law_text(value: Any) -> str:
    """Flatten a law fragment (str / list / dict) into searchable text."""
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, default=str)
    except (TypeError, ValueError):
        return str(value)


def _names_lattice_topology(text: str) -> bool:
    if not text:
        return False
    if _LATTICE_WORD_RE.search(text):
        return True
    return bool(
        _VERTEX_WORD_RE.search(text)
        and _EDGE_WORD_RE.search(text)
        and _FACE_WORD_RE.search(text)
    )


def _armed_step1_locks(armed: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    found: list[tuple[str, dict[str, Any]]] = []
    for key in ("step1_authorship", "step1_occupancy"):
        for holder in (locks.get(key), armed.get(key)):
            if isinstance(holder, dict) and holder:
                found.append((key, holder))
    return found


def armed_topology_signals(armed: dict[str, Any] | None) -> list[str]:
    """Topology-rewrite triggers derived from the resolved armed packet.

    Law, not prose: a reworded ask cannot disarm the axis, because the triggers
    are the locked refuse codes, the structural Success / done_when text, and the
    topology-law lock the operator armed.
    """
    armed = armed if isinstance(armed, dict) else {}
    if not armed:
        return []
    signals: list[str] = []
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    step1_locks = _armed_step1_locks(armed)

    for key, holder in step1_locks:
        refuses = holder.get("refuse")
        if isinstance(refuses, str):
            refuses = [refuses]
        for code in refuses or []:
            code_s = str(code).strip()
            if code_s in ARMED_TOPOLOGY_REFUSES:
                signals.append(f"armed_lock_refuse:{key}:{code_s}")

    law_fields: list[tuple[str, Any]] = [
        ("structural_success", armed.get("structural_success")),
        ("done_when", armed.get("done_when")),
        ("hard_prefer_gaps", armed.get("hard_prefer_gaps")),
    ]
    for key, holder in step1_locks:
        for field in ("structural_success", "law", "replace_live_assumption"):
            law_fields.append((f"{key}.{field}", holder.get(field)))
    for label, value in law_fields:
        if _names_lattice_topology(_law_text(value)):
            signals.append(f"armed_structural_topology:{label}")

    prefer = bool(
        armed.get("prefer_authorship")
        or armed.get("step1_authorship")
        or locks.get("step1_authorship")
        or locks.get("step1_occupancy")
    )
    topology_law = (
        armed.get("topology_law")
        or locks.get("topology_law")
        or any(h.get("topology_law") or h.get("topology_cite") for _k, h in step1_locks)
    )
    if prefer and topology_law:
        signals.append("armed_prefer_authorship_with_topology_law")
    return sorted(set(signals))


def armed_triggers_topology_rewrite(armed: dict[str, Any] | None) -> bool:
    return bool(armed_topology_signals(armed))


def resolve_armed_for_bind(
    vault_root: Path,
    *,
    project_id: str,
    slice_id: str,
    job: dict[str, Any] | None = None,
    armed: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve armed law for a slice: caller-supplied → job pointer → project authority."""
    if isinstance(armed, dict) and armed:
        return armed
    loaded = load_armed_packet(vault_root, job)
    if loaded:
        return loaded
    if not project_id or not slice_id:
        return {}
    from .factory_pq_stage import resolve_authority_armed_packet

    try:
        _rel, data = resolve_authority_armed_packet(
            vault_root, project_id=project_id, slice_id=slice_id
        )
    except Exception:  # authority lookup is best-effort context, never a hard stop
        return {}
    return data if isinstance(data, dict) else {}


def technical_bind_path(vault_root: Path, project_id: str, slice_id: str) -> Path:
    return (
        vault_root
        / ".technical"
        / "weave"
        / "factory"
        / project_id
        / slice_id
        / BIND_FILENAME
    )


def compose_implicit_intent_bind(
    *,
    slice_id: str,
    project_id: str,
    explicit_ask: str,
    structural_success: str | None = None,
    refuse: list[str] | None = None,
    inspiration_cites: list[str] | None = None,
    producer_run_id: str | None = None,
    armed: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build bind artifact dict (does not write)."""
    ask = (explicit_ask or "").strip() or f"slice:{slice_id}"
    refuses = list(refuse or [])
    # Armed law is primary: locked topology refuses / structural Success / topology law.
    sources = list(armed_topology_signals(armed))
    sources.extend(
        f"composed_refuse:{code}"
        for code in refuses
        if str(code) in TOPOLOGY_REFUSES
    )
    # Prose wording is the weakest signal — a reworded ask must not disarm the axis.
    if ask_triggers_topology_rewrite(ask):
        sources.append("ask_prose")
    if ask_triggers_topology_rewrite(slice_id):
        sources.append("slice_id_prose")
    topology = bool(sources)
    for code in BASE_REFUSES:
        if code not in refuses:
            refuses.append(code)
    if topology:
        for code in TOPOLOGY_REFUSES:
            if code not in refuses:
                refuses.append(code)
    success = (structural_success or "").strip()
    if not success:
        success = DEFAULT_STRUCTURAL_SUCCESS if topology else ask
    cites = list(inspiration_cites or DEFAULT_INSPIRATION_CITES)
    return {
        "schema_version": BIND_SCHEMA_VERSION,
        "slice_id": slice_id,
        "project_id": project_id,
        "composed_at": _utc_iso(),
        "producer_run_id": producer_run_id or "",
        "explicit_ask": ask,
        "structural_success": success,
        "refuse": refuses,
        "inspiration_cites": cites,
        "topology_rewrite": topology,
        "topology_rewrite_sources": sorted(set(sources)),
    }


def write_implicit_intent_bind(
    vault_root: Path,
    *,
    slice_id: str,
    project_id: str,
    explicit_ask: str,
    structural_success: str | None = None,
    refuse: list[str] | None = None,
    inspiration_cites: list[str] | None = None,
    producer_run_id: str | None = None,
    armed: dict[str, Any] | None = None,
    job: dict[str, Any] | None = None,
) -> Path:
    """Write bind artifact under .technical/weave/factory/<project>/<slice>/."""
    vault_root = vault_root.resolve()
    payload = compose_implicit_intent_bind(
        slice_id=slice_id,
        project_id=project_id,
        explicit_ask=explicit_ask,
        structural_success=structural_success,
        refuse=refuse,
        inspiration_cites=inspiration_cites,
        producer_run_id=producer_run_id,
        armed=resolve_armed_for_bind(
            vault_root,
            project_id=project_id,
            slice_id=slice_id,
            job=job,
            armed=armed,
        ),
    )
    path = technical_bind_path(vault_root, project_id, slice_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def bind_is_stale(
    bind: dict[str, Any] | None, armed: dict[str, Any] | None
) -> bool:
    """True when armed law was amended after the bind was composed."""
    if not bind:
        return True
    amended = _parse_iso((armed or {}).get("law_amended_at"))
    if amended is None:
        return False
    composed = _parse_iso(bind.get("composed_at"))
    if composed is None:
        return True
    return amended > composed


def bind_needs_rewrite(
    vault_root: Path,
    *,
    project_id: str,
    slice_id: str,
    armed: dict[str, Any] | None = None,
    force: bool = False,
) -> tuple[bool, str]:
    """Decide whether the bind artifact must be re-composed. Returns (needs, reason)."""
    if force:
        return True, "force_reweld_compose"
    existing = load_implicit_intent_bind(
        vault_root, project_id=project_id, slice_id=slice_id
    )
    if not existing:
        return True, "bind_absent"
    if validate_bind_artifact(existing):
        return True, "bind_invalid"
    if bind_is_stale(existing, armed):
        return True, "armed_law_amended_after_compose"
    return False, "bind_fresh"


def ensure_implicit_intent_bind(
    vault_root: Path,
    *,
    slice_id: str,
    project_id: str,
    explicit_ask: str,
    armed: dict[str, Any] | None = None,
    force: bool = False,
    structural_success: str | None = None,
    refuse: list[str] | None = None,
    inspiration_cites: list[str] | None = None,
    producer_run_id: str | None = None,
    job: dict[str, Any] | None = None,
) -> tuple[Path, str]:
    """Write the bind only when absent / invalid / stale vs armed law. Returns (path, reason)."""
    vault_root = vault_root.resolve()
    armed = resolve_armed_for_bind(
        vault_root,
        project_id=project_id,
        slice_id=slice_id,
        job=job,
        armed=armed,
    )
    needs, reason = bind_needs_rewrite(
        vault_root,
        project_id=project_id,
        slice_id=slice_id,
        armed=armed,
        force=force,
    )
    path = technical_bind_path(vault_root, project_id, slice_id)
    if not needs:
        return path, reason
    return (
        write_implicit_intent_bind(
            vault_root,
            slice_id=slice_id,
            project_id=project_id,
            explicit_ask=explicit_ask,
            structural_success=structural_success,
            refuse=refuse,
            inspiration_cites=inspiration_cites,
            producer_run_id=producer_run_id,
            armed=armed,
        ),
        reason,
    )


def load_implicit_intent_bind(
    vault_root: Path, *, project_id: str, slice_id: str
) -> dict[str, Any] | None:
    path = technical_bind_path(vault_root.resolve(), project_id, slice_id)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def validate_bind_artifact(data: dict[str, Any] | None) -> list[str]:
    """Return violation codes; empty = ok."""
    if not data:
        return ["implicit_bind_missing"]
    violations: list[str] = []
    for key in ("explicit_ask", "structural_success", "refuse", "inspiration_cites"):
        if key not in data or data[key] in (None, "", []):
            violations.append(f"implicit_bind_incomplete:{key}")
    refuse = data.get("refuse") or []
    if not isinstance(refuse, list) or len(refuse) < 1:
        violations.append("implicit_bind_incomplete:refuse")
    ask = str(data.get("explicit_ask") or "")
    success = str(data.get("structural_success") or "")
    if (
        ask_triggers_topology_rewrite(ask)
        or ask_triggers_topology_rewrite(str(data.get("slice_id") or ""))
        or bool(data.get("topology_rewrite"))
        or any(str(code) in TOPOLOGY_REFUSES for code in refuse if isinstance(refuse, list))
    ):
        for code in ("points_as_grid", "count_equals_topology"):
            if code not in refuse:
                violations.append(f"implicit_bind_missing_refuse:{code}")
        # Structural success must not merely restate a bare point count.
        if re.search(r"^\s*\d+\s*points?\s*$", success, re.I):
            violations.append("implicit_bind_points_only_success")
        if not re.search(r"\b(edge|face|cell|lattice|graph|vertex|vertices)\b", success, re.I):
            violations.append("implicit_bind_success_missing_topology_terms")
    return violations


@dataclass(frozen=True)
class ImplicitBindCheckResult:
    ok: bool
    violations: tuple[str, ...]
    detail: str
    applicable: bool = True
    bind_path: str | None = None
    bind: dict[str, Any] | None = None
    armed_topology_signals: tuple[str, ...] = ()

    @property
    def topology_rewrite(self) -> bool:
        return bool((self.bind or {}).get("topology_rewrite"))

    @property
    def armed_topology_rewrite(self) -> bool:
        return bool(self.armed_topology_signals)

    @property
    def topology_axis_armed(self) -> bool:
        """Law-derived OR bind-declared — the axis a reworded ask cannot disarm."""
        return self.topology_rewrite or self.armed_topology_rewrite

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "violations": list(self.violations),
            "detail": self.detail,
            "applicable": self.applicable,
            "bind_path": self.bind_path,
            "topology_rewrite": self.topology_rewrite,
            "armed_topology_signals": list(self.armed_topology_signals),
            "topology_axis_armed": self.topology_axis_armed,
        }


def check_implicit_intent_bind(
    vault_root: Path,
    *,
    slice_id: str,
    job: dict[str, Any] | None = None,
    project_id: str | None = None,
) -> ImplicitBindCheckResult:
    """Fail-closed preflight seat when bind is required."""
    job = dict(job or {})
    if not slice_requires_implicit_bind(slice_id, job):
        return ImplicitBindCheckResult(
            True, (), "implicit_bind_not_applicable", applicable=False
        )
    pid = str(project_id or job.get("project_id") or "").strip()
    if not pid:
        return ImplicitBindCheckResult(
            False, ("implicit_bind_missing:project_id",), "implicit_bind_missing"
        )
    path = technical_bind_path(vault_root.resolve(), pid, slice_id)
    data = load_implicit_intent_bind(vault_root, project_id=pid, slice_id=slice_id)
    violations = validate_bind_artifact(data)
    armed = resolve_armed_for_bind(
        vault_root, project_id=pid, slice_id=slice_id, job=job
    )
    law_signals = armed_topology_signals(armed)
    if data and armed and bind_is_stale(data, armed):
        violations.append("implicit_bind_stale_vs_armed_law")
    # A bind may not under-claim the axis the armed packet already locked.
    if data and law_signals and not data.get("topology_rewrite"):
        violations.append(
            "implicit_bind_topology_rewrite_disarmed_vs_armed_law:"
            + ",".join(law_signals[:4])
        )
    ok = len(violations) == 0
    detail = "; ".join(violations) if violations else "implicit_bind_ok"
    return ImplicitBindCheckResult(
        ok,
        tuple(violations),
        detail,
        applicable=True,
        bind_path=str(path.relative_to(vault_root.resolve())) if path else None,
        bind=data,
        armed_topology_signals=tuple(law_signals),
    )


def bind_markdown_overlay(data: dict[str, Any]) -> str:
    """Inject into lane missions / producer SIB."""
    refuses = ", ".join(f"`{c}`" for c in (data.get("refuse") or []))
    cites = "\n".join(f"- {c}" for c in (data.get("inspiration_cites") or []))
    return (
        "## Implicit-intent bind (entry seat — fail-closed)\n\n"
        f"**Explicit ask:** {data.get('explicit_ask')}\n\n"
        f"**Structural Success (binding):** {data.get('structural_success')}\n\n"
        f"**Refuse:** {refuses}\n\n"
        f"**Inspiration cites:**\n{cites}\n\n"
        "Meeting the countable proxy without this structural Success → "
        "`explicit_met_implicit_miss` / `points_as_grid`.\n"
    )
