"""Trinity card storage tiers — locked production vs provisional (ghost-pattern)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from .trinity_card import normalize_card

TrinityTier = Literal["locked", "provisional"]

SCHEMA_CARD = "_schema"
META_CARD_ID = "trinity_card_authoring"


def is_locked_card(card: dict[str, Any]) -> bool:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    return bool(meta.get("conceptual_confirmed_at") and meta.get("rules_confirmed_at"))


def components_dir(vault_root: Path) -> Path:
    """Operator-locked cards only (`conceptual_confirmed_at` + `rules_confirmed_at`)."""
    return vault_root / ".technical" / "weave" / "components"


def component_proposals_dir(vault_root: Path) -> Path:
    """Promoted auto-gen cards — production-usable, not locked until operator gate."""
    return vault_root / ".technical" / "weave" / "component-proposals"


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore[import-untyped]

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML object: {path}")
    return data


def _dump_yaml(data: dict[str, Any]) -> str:
    import yaml  # type: ignore[import-untyped]

    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def is_provisional_card(card: dict[str, Any]) -> bool:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    if meta.get("promotion_tier") == "provisional":
        return True
    return bool(meta.get("provisional"))


def resolve_trinity_card_path(
    vault_root: Path,
    trinity_id: str,
    *,
    prefer: TrinityTier | None = None,
) -> tuple[Path, TrinityTier]:
    """Resolve card path. Default: locked first, then provisional."""
    locked = components_dir(vault_root) / f"{trinity_id}.yaml"
    prov = component_proposals_dir(vault_root) / f"{trinity_id}.yaml"
    if prefer == "provisional":
        if prov.is_file():
            return prov, "provisional"
        if locked.is_file():
            return locked, "locked"
    elif prefer == "locked":
        if locked.is_file():
            return locked, "locked"
        if prov.is_file():
            return prov, "provisional"
    else:
        if locked.is_file():
            return locked, "locked"
        if prov.is_file():
            return prov, "provisional"
    raise FileNotFoundError(
        f"trinity card not found (locked or provisional): {trinity_id}"
    )


def load_trinity_card(
    vault_root: Path,
    trinity_id: str,
    *,
    prefer: TrinityTier | None = None,
) -> dict[str, Any]:
    path, _tier = resolve_trinity_card_path(vault_root, trinity_id, prefer=prefer)
    card = _load_yaml(path)
    if str(card.get("id") or "") != trinity_id:
        card["id"] = trinity_id
    return normalize_card(card)


def write_trinity_card(
    vault_root: Path,
    trinity_id: str,
    card: dict[str, Any],
    *,
    tier: TrinityTier | None = None,
    mutation_action: str = "write_trinity_card",
    operator_override: bool | None = None,
) -> Path:
    """Write card to the tier it already lives in, or explicit tier."""
    from .trinity_dual_lock import assert_system_may_mutate

    assert_system_may_mutate(
        vault_root,
        trinity_id,
        mutation_action,
        operator_override=operator_override,
    )
    from .trinity_dual_lock import (
        CORE_HASH_RECONCILE_ACTIONS,
        is_maintenance_core_id,
        operator_mutation_ctx,
    )

    op_ov = (
        operator_override
        if operator_override is not None
        else operator_mutation_ctx.get()
    )
    if (
        mutation_action not in CORE_HASH_RECONCILE_ACTIONS
        and not is_maintenance_core_id(vault_root, trinity_id)
        and not op_ov
    ):
        from .trinity_spine_guard import assert_respects_locked_spine

        assert_respects_locked_spine(
            vault_root, trinity_id, card=normalize_card(card)
        )
    if tier is None:
        try:
            path, tier = resolve_trinity_card_path(vault_root, trinity_id)
        except FileNotFoundError:
            tier = "provisional"
    if tier == "locked":
        path = components_dir(vault_root) / f"{trinity_id}.yaml"
    else:
        path = component_proposals_dir(vault_root) / f"{trinity_id}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_dump_yaml(normalize_card(card)), encoding="utf-8")
    return path


def list_locked_trinity_card_ids(vault_root: Path) -> list[str]:
    base = components_dir(vault_root)
    if not base.is_dir():
        return []
    out: list[str] = []
    for p in sorted(base.glob("*.yaml")):
        if p.stem in (SCHEMA_CARD, META_CARD_ID) or p.name.startswith("_"):
            continue
        try:
            card = _load_yaml(p)
        except (OSError, ValueError):
            continue
        if is_locked_card(card):
            out.append(p.stem)
    return out


def list_provisional_trinity_card_ids(vault_root: Path) -> list[str]:
    base = component_proposals_dir(vault_root)
    if not base.is_dir():
        return []
    locked = set(list_locked_trinity_card_ids(vault_root))
    out: list[str] = []
    for p in sorted(base.glob("*.yaml")):
        if p.name.startswith("_"):
            continue
        if p.stem in locked:
            continue
        out.append(p.stem)
    return out


def list_trinity_card_ids(
    vault_root: Path,
    *,
    pilot_only: bool = False,
    include_provisional: bool = True,
) -> list[str]:
    ids = list_locked_trinity_card_ids(vault_root)
    if include_provisional:
        for tid in list_provisional_trinity_card_ids(vault_root):
            if tid not in ids:
                ids.append(tid)
    if pilot_only:
        pilot = {
            "lane_status_board",
            "lane_activity",
            "launch_registry_reconcile",
        }
        ids = [i for i in ids if i in pilot]
    return ids


def ensure_trinity_storage_dirs(vault_root: Path) -> None:
    components_dir(vault_root).mkdir(parents=True, exist_ok=True)
    component_proposals_dir(vault_root).mkdir(parents=True, exist_ok=True)
