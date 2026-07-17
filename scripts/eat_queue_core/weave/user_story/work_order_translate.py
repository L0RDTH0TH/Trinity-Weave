"""Vault roadmap → factory dispatch jobs (Phase 0 pipe)."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ..factory.factory_output_gate import parse_factory_orchestrator_yaml
from ..factory.lane_factories import build_lane_job, enrich_job_from_charter
from .catalog_io import (
    catalog_rows_by_id,
    load_json,
    load_yaml,
    normalize_pin,
    user_story_paths,
)
from .depth_scope import factory_feed_objective, load_scope_body, resolve_dispatch_depth, scope_path
from .product_factory_state import load_product_factory

FEED_ALPHA_QUEUE = "alpha_queue"
FEED_VAULT_ROADMAP = "vault_roadmap"
VALID_FEED_AUTHORITIES = frozenset({FEED_ALPHA_QUEUE, FEED_VAULT_ROADMAP})

DEFAULT_PROJECT_ID = "godot-genesis-mythos-master"
DEFAULT_BUDGET_REL = "Roadmap/User-Story/slice-depth-budget.json"
DEFAULT_CATALOG_REL = "Roadmap/User-Story/slice-catalog.yaml"
DEFAULT_LANE_MAP_REL = "Factory-DRB/lane-map.yaml"


@dataclass(frozen=True)
class VaultWorkOrderBundle:
    """One catalog row dispatch unit — Option A (one row per orchestrator pass)."""

    project_id: str
    game_repo_rel: str
    slice_id: str
    row_id: str
    target_depth: int
    current_depth: int
    rollout_version: int
    dimension: str
    lane_ids: tuple[str, ...]
    execution_pins: tuple[str, ...]
    beat_ref: str | None
    jobs: tuple[dict[str, Any], ...]
    queue_bootstrap: dict[str, Any]

    def active_slice(self) -> dict[str, Any]:
        """Synthetic alpha-slice-shaped dict for dispatch policy + dispatch JSON."""
        return {
            "id": self.slice_id,
            "status": "active",
            "source": "vault_roadmap",
            "catalog_row_id": self.row_id,
            "target_depth": self.target_depth,
            "rollout_version": self.rollout_version,
            "lanes": list(self.lane_ids),
            "allow_implement_with_gates_red": True,
            "exit_gates": ["surface_pass", "factory_output_conduct", "product_kinesthetic_honesty"],
        }

    def feed_metadata(self) -> dict[str, Any]:
        meta: dict[str, Any] = {
            "feed_authority": FEED_VAULT_ROADMAP,
            "catalog_row_id": self.row_id,
            "target_depth": self.target_depth,
            "current_depth": self.current_depth,
            "dispatch_depth": (
                int(self.jobs[0].get("dispatch_depth") or 0) if self.jobs else None
            ),
            "ux_feed": self.jobs[0].get("ux_feed") if self.jobs else {},
            "rollout_version": self.rollout_version,
            "dimension": self.dimension,
            "execution_pins": list(self.execution_pins),
            "beat_ref": self.beat_ref,
            "required_lanes": list(self.lane_ids),
        }
        if self.jobs:
            dw = self.jobs[0].get("dependency_warnings") or []
            if dw:
                meta["dependency_warnings"] = dw
        return meta


def build_ux_feed_for_dispatch(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    dispatch_depth: int,
    target_depth: int,
    execution_pins: tuple[str, ...],
) -> dict[str, Any]:
    """Structured UX pillar envelope for factory handoff."""
    vault_root = vault_root.resolve()
    l5 = scope_path(vault_root, project_id, row_id, 5)
    dispatch_scope = scope_path(vault_root, project_id, row_id, dispatch_depth)
    return {
        "catalog_row_id": row_id,
        "dispatch_depth": dispatch_depth,
        "target_depth": target_depth,
        "l5_scope_path": str(l5.relative_to(vault_root)) if l5.is_file() else "",
        "dispatch_scope_path": str(dispatch_scope.relative_to(vault_root)) if dispatch_scope.is_file() else "",
        "execution_pin_path": execution_pins[0] if execution_pins else "",
    }


def _resolve_active_slice(
    vault_root: Path,
    project_id: str,
    explicit: dict[str, Any] | None,
) -> tuple[list[str], int | None, bool]:
    """Return (row_ids, dispatch_depth, confirmed)."""
    if explicit is not None and isinstance(explicit, dict):
        row_ids = explicit.get("row_ids") if isinstance(explicit.get("row_ids"), list) else []
        row_ids = [str(x) for x in row_ids if x]
        depth = explicit.get("dispatch_depth")
        dispatch_depth = int(depth) if depth is not None else None
        return row_ids, dispatch_depth, True

    pf = load_product_factory(vault_root, project_id)
    confirmed = bool(pf.get("slice_selection_confirmed_at"))
    active = pf.get("active_slice") if isinstance(pf.get("active_slice"), dict) else {}
    row_ids = active.get("row_ids") if isinstance(active.get("row_ids"), list) else []
    row_ids = [str(x) for x in row_ids if x]
    depth = active.get("dispatch_depth")
    dispatch_depth = int(depth) if depth is not None else None
    return row_ids, dispatch_depth, confirmed


def _budget_row(budget: dict[str, Any], row_id: str) -> dict[str, Any] | None:
    for row in budget.get("rows") or []:
        if isinstance(row, dict) and str(row.get("row_id")) == row_id:
            return row
    return None


def resolve_feed_authority(vault_root: Path, override: str | None = None) -> str:
    if override and override in VALID_FEED_AUTHORITIES:
        return override
    cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
    raw = str(cfg.get("feed_authority") or FEED_ALPHA_QUEUE).strip().lower()
    return raw if raw in VALID_FEED_AUTHORITIES else FEED_ALPHA_QUEUE


def _project_root(vault_root: Path, project_id: str) -> Path:
    return vault_root / "1-Projects" / project_id


def _vault_feed_paths(vault_root: Path, project_id: str) -> dict[str, Path]:
    paths = user_story_paths(vault_root, project_id)
    return {
        "budget": paths["budget"],
        "catalog": paths["catalog"],
        "lane_map": paths["lane_map"],
        "beats_dir": paths["beats_dir"],
    }


def _resolve_beat_ref(
    vault_root: Path,
    *,
    beats_dir: Path,
    row_id: str,
    rollout_version: int,
    explicit: str | None,
) -> str | None:
    if explicit:
        return explicit
    if not beats_dir.is_dir():
        return None
    safe = re.sub(r"[^a-zA-Z0-9_]+", "-", row_id).strip("-")
    candidates = [
        beats_dir / f"beat-r{rollout_version}-{safe}.md",
        beats_dir / f"beat-r{rollout_version}-{row_id}.md",
    ]
    for p in beats_dir.glob(f"beat-r{rollout_version}-*.md"):
        if row_id in p.read_text(encoding="utf-8", errors="replace"):
            return str(p.relative_to(vault_root))
    for c in candidates:
        if c.is_file():
            return str(c.relative_to(vault_root))
    return None


def _beat_excerpt(vault_root: Path, beat_ref: str | None, max_chars: int = 800) -> str:
    if not beat_ref:
        return ""
    path = vault_root / beat_ref
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    for heading in ("## Experiential narrative", "## Rows", "## Depth context"):
        idx = text.find(heading)
        if idx >= 0:
            return text[idx : idx + max_chars].strip()
    return text[:max_chars].strip()


def _dependency_warnings_for_row(
    catalog_by_id: dict[str, dict[str, Any]],
    budget_rows: list[dict[str, Any]],
    row_id: str,
) -> tuple[str, ...]:
    warnings: list[str] = []
    depth_by_row: dict[str, int] = {}
    for r in budget_rows:
        if isinstance(r, dict) and r.get("row_id"):
            depth_by_row[str(r["row_id"])] = int(r.get("current_depth") or 0)
    row = catalog_by_id.get(row_id) or {}
    deps = row.get("depends_on") or []
    if not isinstance(deps, list):
        return ()
    for dep in deps:
        dep_id = str(dep.get("row_id") if isinstance(dep, dict) else dep)
        min_depth = int(dep.get("min_depth", 1) if isinstance(dep, dict) else 1)
        dep_depth = depth_by_row.get(dep_id, 0)
        if dep_depth < min_depth:
            warnings.append(f"depends_on_unmet:{row_id}:{dep_id}>={min_depth}")
        if dep_id not in catalog_by_id:
            warnings.append(f"depends_on_unknown:{row_id}:{dep_id}")
    return tuple(warnings)


def _pending_budget_rows(budget: dict[str, Any]) -> list[dict[str, Any]]:
    pending: list[dict[str, Any]] = []
    rows = budget.get("rows") or []
    if not isinstance(rows, list):
        return pending
    for row in rows:
        if not isinstance(row, dict):
            continue
        row_id = str(row.get("row_id") or "")
        if not row_id:
            continue
        target = int(row.get("target_depth") or 0)
        current = int(row.get("current_depth") or 0)
        if target > 0 and current < target:
            pending.append(row)
    return pending


def _lanes_for_dimension(lane_map: dict[str, Any], dimension: str) -> tuple[str, ...]:
    dims = lane_map.get("dimensions") or {}
    if isinstance(dims, dict) and dimension in dims:
        block = dims[dimension]
        if isinstance(block, dict):
            lanes = block.get("lanes") or []
            if isinstance(lanes, list):
                return tuple(str(x) for x in lanes if x)
    default = lane_map.get("default_lanes") or ["module"]
    if isinstance(default, list):
        return tuple(str(x) for x in default if x)
    return ("module",)


def _lane_checklists(lane_map: dict[str, Any], dimension: str, lane_id: str) -> tuple[str, ...]:
    dims = lane_map.get("dimensions") or {}
    if not isinstance(dims, dict):
        return ()
    block = dims.get(dimension)
    if not isinstance(block, dict):
        return ()
    lc = block.get("lane_checklists") or {}
    if not isinstance(lc, dict):
        return ()
    ids = lc.get(lane_id) or []
    if isinstance(ids, list):
        return tuple(str(x) for x in ids if x)
    return ()


def _execution_excerpt(vault_root: Path, pins: tuple[str, ...], max_chars: int = 1200) -> str:
    for pin in pins:
        rel = normalize_pin(pin)
        path = vault_root / rel
        if not path.is_file() and not rel.endswith(".md"):
            path = vault_root / f"{rel}.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for heading in ("## Acceptance", "## Done when", "## Objective", "## Scope"):
            idx = text.find(heading)
            if idx >= 0:
                chunk = text[idx : idx + max_chars]
                return chunk.strip()
        return text[:max_chars].strip()
    return ""


def _make_slice_id(row_id: str, rollout: int, target_depth: int) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_]+", "_", row_id).strip("_")
    return f"row_{safe}_r{rollout}_d{target_depth}"


def translate_failure_reason(
    vault_root: Path,
    *,
    project_id: str,
    active_slice: dict[str, Any] | None = None,
) -> str:
    """Machine-readable reason when translate_vault_work_orders returns None."""
    row_ids, operator_depth, confirmed = _resolve_active_slice(
        vault_root, project_id, active_slice
    )
    if not confirmed or not row_ids:
        return "operator_loop_3_not_confirmed"
    paths = _vault_feed_paths(vault_root, project_id)
    if not paths["budget"].is_file():
        return "budget_missing"
    budget = load_json(paths["budget"])
    row_id = row_ids[0]
    row_entry = _budget_row(budget, row_id)
    if row_entry is None:
        return f"budget_row_missing:{row_id}"
    target_depth = int(row_entry.get("target_depth") or 0)
    current_depth = int(row_entry.get("current_depth") or 0)
    computed_depth = resolve_dispatch_depth(current_depth, target_depth)
    if computed_depth is None:
        return f"row_depth_complete:{row_id}"
    if operator_depth is not None and operator_depth != computed_depth:
        return f"dispatch_depth_mismatch:expected={computed_depth}:got={operator_depth}"
    return "vault_work_order_invalid"


def translate_vault_work_orders(
    vault_root: Path,
    *,
    project_id: str | None = None,
    queue_bootstrap: dict[str, Any] | None = None,
    active_slice: dict[str, Any] | None = None,
) -> VaultWorkOrderBundle | None:
    """Return operator-confirmed catalog row as a factory dispatch bundle, or None."""
    vault_root = vault_root.resolve()
    bootstrap = queue_bootstrap or {}
    project_id = str(
        project_id or bootstrap.get("project_id") or DEFAULT_PROJECT_ID
    )
    game_repo_rel = str(bootstrap.get("game_repo_path") or "").strip("/")
    if not game_repo_rel:
        cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
        game_repo_rel = str(cfg.get("game_repo_path") or "").strip("/")
    if not game_repo_rel:
        return None

    paths = _vault_feed_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    catalog = load_yaml(paths["catalog"])
    lane_map = load_yaml(paths["lane_map"])
    catalog_by_id = catalog_rows_by_id(catalog)

    row_ids, operator_depth, confirmed = _resolve_active_slice(
        vault_root, project_id, active_slice
    )
    if not confirmed or not row_ids:
        return None

    row_id = row_ids[0]
    row_entry = _budget_row(budget, row_id)
    if row_entry is None:
        return None

    target_depth = int(row_entry["target_depth"])
    current_depth = int(row_entry.get("current_depth") or 0)
    computed_depth = resolve_dispatch_depth(current_depth, target_depth)
    if computed_depth is None:
        return None

    dispatch_depth = operator_depth if operator_depth is not None else computed_depth
    if dispatch_depth != computed_depth:
        return None
    rollout_version = int(budget.get("rollout_version") or 1)

    cat_row = catalog_by_id.get(row_id, {})
    dimension = str(cat_row.get("dimension") or row_entry.get("dimension") or "system")
    pins_raw = cat_row.get("execution_pins") or row_entry.get("execution_pins") or []
    pins: tuple[str, ...] = ()
    if isinstance(pins_raw, list):
        pins = tuple(str(normalize_pin(p)) for p in pins_raw if p)

    dep_warnings = _dependency_warnings_for_row(
        catalog_by_id, budget.get("rows") or [], row_id
    )

    lane_ids = _lanes_for_dimension(lane_map, dimension)
    if not lane_ids:
        return None

    slice_id = _make_slice_id(row_id, rollout_version, dispatch_depth)
    pin_excerpt = _execution_excerpt(vault_root, pins)
    beat_ref = _resolve_beat_ref(
        vault_root,
        beats_dir=paths["beats_dir"],
        row_id=row_id,
        rollout_version=rollout_version,
        explicit=str(cat_row.get("beat_ref") or "") or None,
    )
    excerpt = factory_feed_objective(
        vault_root,
        project_id=project_id,
        row_id=row_id,
        dispatch_depth=dispatch_depth,
        pin_excerpt=pin_excerpt,
    )
    ux_feed = build_ux_feed_for_dispatch(
        vault_root,
        project_id=project_id,
        row_id=row_id,
        dispatch_depth=dispatch_depth,
        target_depth=target_depth,
        execution_pins=pins,
    )

    jobs: list[dict[str, Any]] = []
    for lane_id in lane_ids:
        built = build_lane_job(
            vault_root,
            lane_id=lane_id,
            slice_id=slice_id,
            game_repo_rel=game_repo_rel,
        )
        if built is None:
            continue
        job = enrich_job_from_charter(vault_root, built.to_dict())
        checklists = _lane_checklists(lane_map, dimension, lane_id)
        if checklists:
            job["checklist_ids"] = list(checklists)
        job["catalog_row_id"] = row_id
        job["target_depth"] = target_depth
        job["dispatch_depth"] = dispatch_depth
        job["current_depth"] = current_depth
        job["rollout_version"] = rollout_version
        job["execution_pin"] = pins[0] if pins else ""
        job["beat_ref"] = beat_ref or ""
        job["vault_feed_objective"] = excerpt
        job["ux_feed"] = ux_feed
        job["feed_authority"] = FEED_VAULT_ROADMAP
        job["dependency_warnings"] = list(dep_warnings)
        jobs.append(job)

    if not jobs:
        return None

    return VaultWorkOrderBundle(
        project_id=project_id,
        game_repo_rel=game_repo_rel,
        slice_id=slice_id,
        row_id=row_id,
        target_depth=target_depth,
        current_depth=current_depth,
        rollout_version=rollout_version,
        dimension=dimension,
        lane_ids=lane_ids,
        execution_pins=pins,
        beat_ref=beat_ref,
        jobs=tuple(jobs),
        queue_bootstrap=bootstrap,
    )


def resolve_vault_note(
    vault_root: Path,
    ref: str,
    *,
    project_id: str,
    max_chars: int = 4000,
) -> tuple[str, str]:
    """Resolve wiki-link or vault-relative path to (rel_path, body excerpt)."""
    vault_root = vault_root.resolve()
    raw = normalize_pin(str(ref))
    candidates: list[Path] = []
    if raw:
        candidates.append(vault_root / raw)
        if not raw.endswith((".md", ".yaml", ".yml")):
            candidates.append(vault_root / f"{raw}.md")
        proj_prefix = f"1-Projects/{project_id}/"
        if not raw.startswith("1-Projects/"):
            candidates.append(vault_root / proj_prefix / raw)
            if not raw.endswith(".md"):
                candidates.append(vault_root / f"{proj_prefix}{raw}.md")
    for path in candidates:
        if path.is_file():
            rel = str(path.relative_to(vault_root))
            body = path.read_text(encoding="utf-8", errors="replace")[:max_chars].strip()
            return rel, body
    return "", ""


def assemble_pillar_packet(
    vault_root: Path,
    *,
    project_id: str,
    producer_run_id: str | None = None,
    active_slice: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Harness assembly of UX/conceptual/execution pillar inputs for Slice Producer."""
    vault_root = vault_root.resolve()
    bundle = translate_vault_work_orders(
        vault_root,
        project_id=project_id,
        active_slice=active_slice,
    )
    if bundle is None:
        return None

    paths = _vault_feed_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    catalog_by_id = catalog_rows_by_id(catalog)
    cat_row = catalog_by_id.get(bundle.row_id) or {}
    budget = load_json(paths["budget"])
    budget_row = _budget_row(budget, bundle.row_id) or {}

    dispatch_depth = int(bundle.jobs[0].get("dispatch_depth") or 0) if bundle.jobs else 0
    l5_body = load_scope_body(vault_root, project_id, bundle.row_id, 5)
    dispatch_body = load_scope_body(vault_root, project_id, bundle.row_id, dispatch_depth)

    conceptual_ref = str(cat_row.get("conceptual_pin") or "")
    conceptual_path, conceptual_body = resolve_vault_note(
        vault_root, conceptual_ref, project_id=project_id
    )
    exec_excerpt = _execution_excerpt(vault_root, bundle.execution_pins)
    exec_pins_resolved = [
        resolve_vault_note(vault_root, p, project_id=project_id)[0] or normalize_pin(str(p))
        for p in bundle.execution_pins
    ]

    dep_warnings = list(
        _dependency_warnings_for_row(
            catalog_by_id,
            list(budget.get("rows") or []),
            bundle.row_id,
        )
    )

    packet: dict[str, Any] = {
        "schema_version": 1,
        "project_id": project_id,
        "slice_id": bundle.slice_id,
        "row_ids": [bundle.row_id],
        "catalog_row_id": bundle.row_id,
        "row_label": str(cat_row.get("label") or bundle.row_id),
        "dimension": bundle.dimension,
        "dispatch_depth": dispatch_depth,
        "target_depth": bundle.target_depth,
        "current_depth": bundle.current_depth,
        "rollout_version": bundle.rollout_version,
        "producer_run_id": producer_run_id or "",
        "game_repo_rel": bundle.game_repo_rel,
        "lane_roster": list(bundle.lane_ids),
        "ux": {
            "l5_scope_path": str(scope_path(vault_root, project_id, bundle.row_id, 5).relative_to(vault_root))
            if scope_path(vault_root, project_id, bundle.row_id, 5).is_file()
            else "",
            "dispatch_scope_path": str(
                scope_path(vault_root, project_id, bundle.row_id, dispatch_depth).relative_to(vault_root)
            )
            if scope_path(vault_root, project_id, bundle.row_id, dispatch_depth).is_file()
            else "",
            "l5_body": l5_body,
            "dispatch_body": dispatch_body,
        },
        "conceptual": {
            "pin_ref": conceptual_ref,
            "pin_path": conceptual_path,
            "body": conceptual_body,
        },
        "execution": {
            "pins": list(bundle.execution_pins),
            "pin_paths": exec_pins_resolved,
            "acceptance_excerpt": exec_excerpt,
        },
        "beat_ref": bundle.beat_ref,
        "beat_excerpt": _beat_excerpt(vault_root, bundle.beat_ref),
        "dependency_warnings": dep_warnings,
        "budget_receipt": {
            "row_id": bundle.row_id,
            "current_depth": bundle.current_depth,
            "target_depth": bundle.target_depth,
            "status": budget_row.get("status"),
        },
    }
    from ..persona_handoff import build_half_a_provenance_from_packet

    packet["half_a_provenance"] = build_half_a_provenance_from_packet(
        packet,
        vault_root=vault_root,
        project_id=project_id,
    )
    canonical = json.dumps(packet, sort_keys=True, ensure_ascii=False)
    packet["pillar_packet_hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    return packet