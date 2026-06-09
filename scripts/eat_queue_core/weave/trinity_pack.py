"""Build trinity_pack for Layer 0/1 context envelopes (Wave 2.5c)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from ..maintenance_io import MAINTENANCE_MODES
from .config import load_trinity_config, load_weave_config
from .trinity_touch_refresh import (
    build_closure_manifest,
    concept_map_path,
    load_trinity_card,
)

# All maintenance-lane PQ modes must carry trinity_pack (Phase 2 weave integration).
TRINITY_PACK_MAINTENANCE_MODES = frozenset(MAINTENANCE_MODES) | frozenset(
    {"STALE_LANE_BOARD", "TRINITY_SPINE_CATCHUP", "TRINITY_UPGRADE_INTEGRATE"}
)

DEFAULT_MAINTENANCE_TRINITY_ID = "lane_status_board"

# Explicit mode → component/bridge card (supplements concept-trinity-map maintainer_modes).
_MODE_TRINITY_OVERRIDES: dict[str, str] = {
    "MAINTENANCE_NOTE": "lane_status_board",
    "OPERATOR_ALERT": "lane_status_board",
    "MAINTENANCE_EVAL": "weave_governance",
    "MAINTENANCE_CHECKLIST": "lane_status_board",
    "GOVERNANCE_REVIEW": "invariant_registry",
    "OPERATOR_SURFACE_REPAIR": "recoverable_handlers",
    "REPAIR_PLAYBOOK": "recoverable_handlers",
    "REFRESH_LANE_BOARD": "lane_status_board",
    "GHOST_SKILL_AUDIT": "ghost_skill_audit",
    "REPAIR_ROUTING": "recoverable_handlers",
    "HEURISTIC_KNOB_PROPOSAL": "l4_adaptive_policy",
    "ADAPTIVE_POLICY_REVIEW": "l4_adaptive_policy",
    "SKILL_GAP_SCAN": "skill_gap",
    "SKILL_PROPOSAL_REVIEW": "skill_gap",
    "TRINITY_SPINE_CATCHUP": "trinity_spine_maintenance",
    "TRINITY_WEAVE_SELF_WRAP": "trinity_spine_maintenance",
    "TRINITY_CORPS_SWEEP": "trinity_spine_maintenance",
    "TRINITY_UPGRADE_INTEGRATE": "trinity_upgrade_integration",
}

_MAINTAINER_MODE_ALIASES = {
    "MAINTAIN_OPERATOR_SURFACE": "OPERATOR_SURFACE_REPAIR",
    "MAINTAIN OPERATOR SURFACE": "OPERATOR_SURFACE_REPAIR",
}


def _normalize_queue_mode(mode: str | None) -> str:
    mode_n = str(mode or "").strip().upper().replace(" ", "_")
    if mode_n == "STALE_LANE_BOARD":
        return "REFRESH_LANE_BOARD"
    return _MAINTAINER_MODE_ALIASES.get(mode_n, mode_n)


@lru_cache(maxsize=8)
def _maintenance_mode_trinity_map_key(vault_root_str: str) -> dict[str, str]:
    """Mode → trinity_id for maintenance PQ (concept map + overrides)."""
    vault_root = Path(vault_root_str)
    out = dict(_MODE_TRINITY_OVERRIDES)
    cmap_path = concept_map_path(vault_root)
    if not cmap_path.is_file():
        return out
    try:
        concepts = (_load_yaml(cmap_path).get("concepts") or {})
    except (OSError, ValueError, Exception):
        return out
    if not isinstance(concepts, dict):
        return out
    for _key, row in concepts.items():
        if not isinstance(row, dict):
            continue
        tid = str(row.get("trinity_id") or "").strip()
        if not tid and isinstance(row.get("trinity_ids"), list) and row["trinity_ids"]:
            tid = str(row["trinity_ids"][0]).strip()
        if not tid:
            continue
        for raw_mode in row.get("maintainer_modes") or []:
            mode_n = _normalize_queue_mode(str(raw_mode))
            if mode_n:
                out[mode_n] = tid
    return out


def maintenance_mode_trinity_map(vault_root: Path) -> dict[str, str]:
    return _maintenance_mode_trinity_map_key(str(vault_root.resolve()))


def resolve_trinity_id_for_mode(vault_root: Path, queue_mode: str | None) -> str | None:
    mode_n = _normalize_queue_mode(queue_mode)
    if not mode_n:
        return None
    return maintenance_mode_trinity_map(vault_root).get(mode_n)


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore[import-untyped]

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML object: {path}")
    return data


def resolve_trinity_id(
    vault_root: Path,
    *,
    trinity_id: str | None = None,
    concept: str | None = None,
    lane: str | None = None,
    queue_mode: str | None = None,
) -> str | None:
    """Resolve card id from explicit id, concept map, or maintenance defaults."""
    if trinity_id and str(trinity_id).strip():
        return str(trinity_id).strip()

    concept_key = str(concept or "").strip()
    if concept_key:
        cmap_path = concept_map_path(vault_root)
        if cmap_path.is_file():
            concepts = (_load_yaml(cmap_path).get("concepts") or {})
            row = concepts.get(concept_key) if isinstance(concepts, dict) else None
            if isinstance(row, dict) and row.get("trinity_id"):
                return str(row["trinity_id"]).strip()

    lane_n = str(lane or "").strip().lower()
    mode_n = _normalize_queue_mode(queue_mode)

    if mode_n:
        from_mode = resolve_trinity_id_for_mode(vault_root, mode_n)
        if from_mode:
            return from_mode

    if lane_n == "maintenance":
        return DEFAULT_MAINTENANCE_TRINITY_ID

    if mode_n in TRINITY_PACK_MAINTENANCE_MODES:
        return DEFAULT_MAINTENANCE_TRINITY_ID

    return None


def resolve_consumable_trinity_id(
    vault_root: Path,
    *,
    trinity_id: str | None = None,
    concept: str | None = None,
    lane: str | None = None,
    queue_mode: str | None = None,
) -> tuple[str | None, dict[str, Any]]:
    """Pack-safe id: locked core + conceptual_spine; provisionals → fallback + advisory."""
    from .trinity_dual_lock import is_consumable_for_pack

    vault_root = vault_root.resolve()
    extras: dict[str, Any] = {}
    explicit = str(trinity_id or "").strip() or None

    def _pick(raw: str | None) -> str | None:
        if not raw:
            return None
        if is_consumable_for_pack(vault_root, raw):
            return raw
        extras["trinity_id_advisory"] = raw
        extras["trinity_pack_omitted_reason"] = "not_consumable_for_pack"
        return None

    if explicit:
        consumable = _pick(explicit)
        if consumable:
            return consumable, extras
        fallback = resolve_trinity_id(
            vault_root,
            concept=concept,
            lane=lane,
            queue_mode=queue_mode,
        )
        fb = _pick(fallback)
        if fb:
            return fb, extras
        if lane and str(lane).strip().lower() == "maintenance":
            return DEFAULT_MAINTENANCE_TRINITY_ID, extras
        return None, extras

    raw = resolve_trinity_id(
        vault_root,
        concept=concept,
        lane=lane,
        queue_mode=queue_mode,
    )
    picked = _pick(raw)
    return picked, extras


def trinity_pack_required(
    vault_root: Path,
    *,
    lane: str | None = None,
    queue_mode: str | None = None,
    trinity_id: str | None = None,
    concept: str | None = None,
) -> bool:
    weave_cfg = load_weave_config(vault_root)
    cfg = load_trinity_config(vault_root)
    if not weave_cfg.enabled or not cfg.enabled:
        return False

    if trinity_id or concept:
        return True

    lane_n = str(lane or "").strip().lower()
    mode_n = _normalize_queue_mode(queue_mode)

    if lane_n == "maintenance" and cfg.pack_mandatory_on_maintenance_lane:
        return True

    if mode_n in TRINITY_PACK_MAINTENANCE_MODES:
        return True

    return False


def build_trinity_pack(
    vault_root: Path,
    trinity_id: str,
    *,
    concept: str | None = None,
) -> dict[str, Any]:
    """Communal hand-off: Conceptual + Rules + Touch (component-scoped; display only)."""
    from .trinity_card import get_conceptual, get_rules, get_touch, normalize_card

    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    card = normalize_card(load_trinity_card(vault_root, trinity_id))
    manifest = build_closure_manifest(
        vault_root,
        card,
        max_hops=cfg.max_closure_hops,
        max_paths=cfg.max_closure_paths,
    )

    conceptual = get_conceptual(card)
    rules = get_rules(card)
    touch = get_touch(card)
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}

    concept_out = concept or _concept_for_trinity_id(vault_root, trinity_id)

    anatomy = "component"
    bridge_endpoints: list[str] = []
    try:
        from .trinity_partition import load_partition_registry

        anatomy = load_partition_registry(vault_root).anatomy_for(trinity_id)
        if anatomy == "bridge":
            touch_raw = get_touch(card)
            raw_bridges = touch_raw.get("bridges") or []
            if isinstance(raw_bridges, list):
                bridge_endpoints = [str(x).strip() for x in raw_bridges if str(x).strip()]
    except (FileNotFoundError, OSError, ValueError):
        pass

    component_scope = anatomy == "component"

    pack: dict[str, Any] = {
        "trinity_id": trinity_id,
        "concept": concept_out,
        "anatomy": anatomy,
        "component_scope": component_scope,
        "conceptual": {
            "outcome": conceptual.get("outcome"),
            "summary": conceptual.get("summary"),
            "primary_case": conceptual.get("primary_case"),
            "edge_cases": _list_cap(conceptual.get("edge_cases"), 4),
            "misread_risks": _list_cap(conceptual.get("misread_risks"), 6),
        },
        "rules": {
            "forbidden": _list_cap(rules.get("forbidden"), 12),
            "fixtures": _list_cap(rules.get("fixtures"), 8),
            "precedence": _list_cap(rules.get("precedence"), 6),
            "acceptance": _list_cap(rules.get("acceptance"), 8),
        },
        "touch": {
            "blast_radius": touch.get("blast_radius"),
            "must_read": manifest.get("must_read") or [],
            "behavior_signals": _list_cap(touch.get("behavior_signals"), 16),
            "closure_hops": manifest.get("hop_limit"),
            "closure_path_cap": manifest.get("path_cap"),
        },
        "disconnect": _disconnect_list_for_pack(vault_root, trinity_id, meta, cfg),
        "meta": {
            "touch_content_hash": meta.get("touch_content_hash"),
            "touch_refreshed_at": meta.get("touch_refreshed_at"),
            "schema_version": meta.get("schema_version"),
        },
    }
    if anatomy == "bridge":
        pack["bridge_scope"] = True
        if bridge_endpoints:
            pack["bridge_endpoints"] = bridge_endpoints[:24]
    maint = rules.get("maintainer_invocation")
    if maint:
        pack["rules"]["maintainer_invocation"] = str(maint).strip()
    return pack


def _list_cap(raw: Any, n: int) -> list[str]:
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        s = str(item).strip()
        if s:
            out.append(s)
        if len(out) >= n:
            break
    return out


def _disconnect_list_for_pack(
    vault_root: Path,
    trinity_id: str,
    meta: dict[str, Any],
    cfg: Any,
) -> list[dict[str, Any]]:
    if getattr(cfg, "checks_enabled", False):
        from .trinity_align import check

        align = check(vault_root, trinity_id)
        return [d.to_dict() for d in align.disconnects]
    return _disconnect_block(meta)


def _disconnect_block(meta: dict[str, Any]) -> list[dict[str, Any]]:
    last = meta.get("last_disconnect")
    if not last:
        return []
    if isinstance(last, dict):
        return [last]
    if isinstance(last, list):
        return [x for x in last if isinstance(x, dict)]
    return []


def _concept_for_trinity_id(vault_root: Path, trinity_id: str) -> str | None:
    cmap_path = concept_map_path(vault_root)
    if not cmap_path.is_file():
        return None
    concepts = (_load_yaml(cmap_path).get("concepts") or {})
    if not isinstance(concepts, dict):
        return None
    for key, row in concepts.items():
        if isinstance(row, dict) and str(row.get("trinity_id")) == trinity_id:
            return str(key)
    return None


def format_trinity_pack_yaml(pack: dict[str, Any], indent: int = 0) -> list[str]:
    """Render trinity_pack as indented YAML lines (no PyYAML dump — stable order)."""
    prefix = " " * indent

    def emit(key: str, val: Any, ind: int) -> list[str]:
        p = " " * ind
        if isinstance(val, dict):
            lines = [f"{p}{key}:"]
            for k, v in val.items():
                lines.extend(emit(k, v, ind + 2))
            return lines
        if isinstance(val, list):
            if not val:
                return [f"{p}{key}: []"]
            lines = [f"{p}{key}:"]
            for item in val:
                if isinstance(item, dict):
                    lines.append(f"{p}  -")
                    for k, v in item.items():
                        lines.extend(emit(k, v, ind + 4))
                else:
                    lines.append(f'{p}  - "{_yaml_escape(str(item))}"')
            return lines
        if val is None:
            return [f"{p}{key}: null"]
        if isinstance(val, bool):
            return [f"{p}{key}: {'true' if val else 'false'}"]
        if isinstance(val, (int, float)):
            return [f"{p}{key}: {val}"]
        return [f'{p}{key}: "{_yaml_escape(str(val))}"']

    lines = [f"{prefix}trinity_pack:"]
    for k, v in pack.items():
        if k == "trinity_pack":
            continue
        lines.extend(emit(k, v, indent + 2))
    return lines


def _yaml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def build_trinity_pack_section(
    vault_root: Path,
    *,
    trinity_id: str | None = None,
    concept: str | None = None,
    lane: str | None = None,
    queue_mode: str | None = None,
) -> tuple[str, bool]:
    """Return YAML lines to append under context_envelope, and whether pack was mandatory."""
    resolved, _pack_extras = resolve_consumable_trinity_id(
        vault_root,
        trinity_id=trinity_id,
        concept=concept,
        lane=lane,
        queue_mode=queue_mode,
    )
    required = trinity_pack_required(
        vault_root,
        lane=lane,
        queue_mode=queue_mode,
        trinity_id=trinity_id,
        concept=concept,
    )
    if not resolved:
        if required:
            return (
                "trinity_pack_required: true\ntrinity_pack_missing: true\n"
                "trinity_pack_note: No trinity_id resolved; run trinity_touch_refresh and set params.trinity_id or concept.\n",
                True,
            )
        return "", False

    try:
        pack = build_trinity_pack(vault_root, resolved, concept=concept)
    except (OSError, ValueError, FileNotFoundError) as e:
        if required:
            return (
                f"trinity_pack_required: true\ntrinity_pack_error: \"{_yaml_escape(str(e))}\"\n",
                True,
            )
        return "", False

    lines = format_trinity_pack_yaml(pack, indent=0)
    return "\n".join(lines) + "\n", required


def trinity_pack_from_queue_entry(
    vault_root: Path,
    entry: dict[str, Any],
    *,
    lane: str | None = None,
) -> tuple[str, bool]:
    """Extract trinity hints from a PQ line for envelope assembly."""
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    mode = str(entry.get("mode") or "")
    lane_n = (
        str(lane or params.get("queue_lane") or entry.get("queue_lane") or "")
        .strip()
        .lower()
    )
    explicit_tid = str(params.get("trinity_id") or "").strip() or None
    return build_trinity_pack_section(
        vault_root,
        trinity_id=explicit_tid,
        concept=str(params.get("concept") or "") or None,
        lane=lane_n or None,
        queue_mode=mode,
    )


def enrich_maintenance_params(
    vault_root: Path,
    mode: str,
    params: dict[str, Any] | None,
) -> dict[str, Any]:
    """Default params.trinity_id from mode map; only consumable ids land in params (Phase 6)."""
    p = dict(params or {})
    mode_n = _normalize_queue_mode(mode)
    explicit = str(p.get("trinity_id") or "").strip()
    if explicit:
        tid, extras = resolve_consumable_trinity_id(
            vault_root,
            trinity_id=explicit,
            lane="maintenance",
            queue_mode=mode_n,
        )
        p.update(extras)
        if tid:
            p["trinity_id"] = tid
        else:
            p.pop("trinity_id", None)
        return p
    tid, extras = resolve_consumable_trinity_id(
        vault_root,
        lane="maintenance",
        queue_mode=mode_n,
    )
    p.update(extras)
    if tid:
        p["trinity_id"] = tid
    try:
        from .trinity_card_backlog import backlog_hint_for_params

        p.update(backlog_hint_for_params(vault_root, top_n=3))
    except (OSError, ValueError, FileNotFoundError):
        pass
    return p
