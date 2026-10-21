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

# Moment-only refuse (not appended on proof_shape: contract).
MOMENT_BASE_REFUSES: tuple[str, ...] = ("inspiration_shape_miss",)

# Place/craft + topology_law only — exact prefer_class, not substring.
CRAFT_CAM_REFUSES: tuple[str, ...] = (
    "craft_cam_recenter_on_place",
    "craft_terrain_blend",
)

# Product-named topology refuses live in legacy-refuse.yaml — not baked here.
TOPOLOGY_REFUSES: tuple[str, ...] = ()

# Back-compat alias — craft cams are no longer unconditional BASE.
BASE_REFUSES: tuple[str, ...] = MOMENT_BASE_REFUSES + CRAFT_CAM_REFUSES

_POINTS_GRID_RE = re.compile(
    r"\b(?:\d+\s*points?|point\s*cloud|hex[- ]?19|hexagonal\s+grid|"
    r"occupancy\s+(?:grid|lattice|markers?)|grid\s+of\s+points)\b",
    re.I,
)

# Deprecated empty: refuse codes no longer arm topology (kept for import stability).
ARMED_TOPOLOGY_REFUSES: tuple[str, ...] = ()

PLACE_OR_CRAFT_CLASSES: frozenset[str] = frozenset({"place", "craft"})


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
    """Legacy prose detector — does **not** arm topology_rewrite (informational only)."""
    return bool(_POINTS_GRID_RE.search(text or ""))


def _armed_step1_locks(armed: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    found: list[tuple[str, dict[str, Any]]] = []
    for key in ("step1_authorship", "step1_occupancy"):
        for holder in (locks.get(key), armed.get(key)):
            if isinstance(holder, dict) and holder:
                found.append((key, holder))
    return found


def _truthy_topology_law(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str) and value.strip().lower() in {"true", "1", "yes"}:
        return True
    return False


def topology_law_armed(armed: dict[str, Any] | None) -> bool:
    """True only when Prefer/locks set topology_law: true (exact field)."""
    armed = armed if isinstance(armed, dict) else {}
    if not armed:
        return False
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    if _truthy_topology_law(armed.get("topology_law")):
        return True
    if _truthy_topology_law(locks.get("topology_law")):
        return True
    for _key, holder in _armed_step1_locks(armed):
        if _truthy_topology_law(holder.get("topology_law")):
            return True
    return False


def prefer_class_exact(armed: dict[str, Any] | None) -> str:
    armed = armed if isinstance(armed, dict) else {}
    return str(armed.get("prefer_class") or "").strip().lower()


def armed_topology_signals(armed: dict[str, Any] | None) -> list[str]:
    """Topology-rewrite triggers — **only** explicit ``topology_law: true``.

    Refuse codes (incl. ``explicit_met_implicit_miss``), Success prose containing
    lattice words, and place/dual name substrings do **not** arm the axis.
    """
    if topology_law_armed(armed):
        return ["armed_topology_law:true"]
    return []


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
    armed = armed if isinstance(armed, dict) else {}
    sources = list(armed_topology_signals(armed))
    topology = bool(sources)
    proof_shape = str(armed.get("proof_shape") or "").strip().lower()
    # Moment (default when unset and not contract) may carry inspiration refuse.
    if proof_shape != "contract":
        for code in MOMENT_BASE_REFUSES:
            if code not in refuses:
                refuses.append(code)
    # craft_cam_* only when prefer_class is exactly place|craft AND topology_law.
    if prefer_class_exact(armed) in PLACE_OR_CRAFT_CLASSES and topology:
        for code in CRAFT_CAM_REFUSES:
            if code not in refuses:
                refuses.append(code)
    if topology:
        for code in TOPOLOGY_REFUSES:
            if code not in refuses:
                refuses.append(code)
    success = (structural_success or "").strip()
    if not success:
        # Prefer Success text, else the ask — never a silent hex-lattice default.
        success = str(armed.get("structural_success") or "").strip() or ask
    if inspiration_cites is not None:
        cites = list(inspiration_cites)
    elif proof_shape == "contract":
        cites = []
    else:
        raw = armed.get("inspiration_cites")
        cites = list(raw) if isinstance(raw, (list, tuple)) else []
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
    for key in ("explicit_ask", "structural_success"):
        if key not in data or data[key] in (None, ""):
            violations.append(f"implicit_bind_incomplete:{key}")
    if "refuse" not in data or not isinstance(data.get("refuse"), list):
        violations.append("implicit_bind_incomplete:refuse")
    if "inspiration_cites" not in data or not isinstance(
        data.get("inspiration_cites"), list
    ):
        # Empty list is valid (contract / no silent Townscaper cites).
        violations.append("implicit_bind_incomplete:inspiration_cites")
    refuse = data.get("refuse") if isinstance(data.get("refuse"), list) else []
    success = str(data.get("structural_success") or "")
    # Topology terms required only when topology_rewrite is actually armed.
    if bool(data.get("topology_rewrite")):
        # Prefer/job must name topology refuses; harness does not bake product codes.
        if not refuse:
            violations.append("implicit_bind_missing_refuse:topology")
        if re.search(r"^\s*\d+\s*points?\s*$", success, re.I):
            violations.append("implicit_bind_points_only_success")
        if not re.search(
            r"\b(edge|face|cell|lattice|graph|vertex|vertices)\b", success, re.I
        ):
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
        "`explicit_met_implicit_miss` / topology refuse.\n"
    )
