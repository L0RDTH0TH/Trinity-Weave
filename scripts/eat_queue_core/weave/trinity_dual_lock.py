"""Dual-lock constitution (Phase 5) — maintenance core vs conceptual spine."""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from .trinity_card_paths import is_locked_card, is_provisional_card, load_trinity_card

LockKind = Literal[
    "maintenance_core",
    "conceptual_spine",
    "full",
    "provisional",
    "usage_proven",
    "none",
]

DEFAULT_MAINTENANCE_META_CORE_IDS = frozenset(
    {"conceptual_style_guide", "trinity_card_authoring"}
)

operator_mutation_ctx: ContextVar[bool] = ContextVar("trinity_operator_mutation", default=False)

# Allowed on maintenance core without --operator-mutation (meta hash only, not leg edits).
CORE_HASH_RECONCILE_ACTIONS = frozenset(
    {
        "gate_hash_reconcile",
        "_sync_stored_touch_hash",
    }
)


class SystemMutationForbidden(Exception):
    """Automation attempted to mutate a maintenance-core card."""

    def __init__(self, trinity_id: str, action: str, detail: str = "") -> None:
        self.trinity_id = trinity_id
        self.action = action
        self.detail = detail or (
            f"maintenance core {trinity_id!r} is system_mutable=false; "
            "use harness --operator-mutation for operator edits"
        )
        super().__init__(self.detail)


@dataclass(frozen=True)
class MaintenanceCorePolicy:
    system_mutable: bool
    ids: frozenset[str]


def _card_meta(card: dict[str, Any]) -> dict[str, Any]:
    meta = card.get("meta")
    return meta if isinstance(meta, dict) else {}


def lock_kind_from_card(card: dict[str, Any]) -> LockKind:
    meta = _card_meta(card)
    raw = str(meta.get("lock_kind") or "").strip().lower()
    if raw == "maintenance_core":
        return "maintenance_core"
    if raw == "usage_proven":
        return "usage_proven"
    if raw == "conceptual_spine":
        return "conceptual_spine"
    if is_provisional_card(card):
        return "provisional"
    if is_locked_card(card):
        return "full"
    if meta.get("conceptual_confirmed_at") and not meta.get("rules_confirmed_at"):
        return "conceptual_spine"
    return "none"


def load_maintenance_core_policy(vault_root: Path) -> MaintenanceCorePolicy:
    """Registry-backed maintenance core ids (partition + optional meta)."""
    vault_root = vault_root.resolve()
    try:
        from .trinity_partition import load_partition_registry, registry_path

        reg = load_partition_registry(vault_root)
        raw = _load_registry_raw(registry_path(vault_root))
        core_block = raw.get("maintenance_core") or {}
        if not isinstance(core_block, dict):
            core_block = {}
        explicit = core_block.get("ids")
        ids: set[str] = set(reg.maintenance_trinity_ids())
        if bool(core_block.get("include_meta", True)):
            ids.update(DEFAULT_MAINTENANCE_META_CORE_IDS)
            for tid in reg.meta:
                if reg.meta[tid].partition == "maintenance":
                    ids.add(tid)
        if isinstance(explicit, list):
            ids = {str(x).strip() for x in explicit if str(x).strip()}
        system_mutable = bool(core_block.get("system_mutable", False))
        return MaintenanceCorePolicy(
            system_mutable=system_mutable,
            ids=frozenset(ids),
        )
    except (FileNotFoundError, OSError, ValueError):
        return MaintenanceCorePolicy(system_mutable=True, ids=frozenset())


def _load_registry_raw(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore[import-untyped]

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def is_maintenance_core_id(vault_root: Path, trinity_id: str) -> bool:
    tid = str(trinity_id or "").strip()
    if not tid:
        return False
    return tid in load_maintenance_core_policy(vault_root).ids


def is_usage_proven_id(vault_root: Path, trinity_id: str) -> bool:
    """True when card carries usage_proven lock_kind (Phase 15 earned freeze)."""
    tid = str(trinity_id or "").strip()
    if not tid:
        return False
    try:
        card = load_trinity_card(vault_root, tid, prefer="locked")
    except (OSError, ValueError, FileNotFoundError):
        try:
            card = load_trinity_card(vault_root, tid, prefer="provisional")
        except (OSError, ValueError, FileNotFoundError):
            return False
    return lock_kind_from_card(card) == "usage_proven"


def corps_repair_skip_reason(vault_root: Path, trinity_id: str) -> str | None:
    """Return skip token for corps repair paths (10d/10f/10g), or None if mutable."""
    if is_maintenance_core_id(vault_root, trinity_id):
        return "maintenance_core"
    if is_usage_proven_id(vault_root, trinity_id):
        return "usage_proven"
    return None


def is_maintenance_core_card(card: dict[str, Any], *, vault_root: Path | None = None) -> bool:
    tid = str(card.get("id") or "").strip()
    if lock_kind_from_card(card) == "maintenance_core":
        return True
    if vault_root is not None and tid:
        return is_maintenance_core_id(vault_root, tid)
    return False


def is_conceptual_spine_locked(card: dict[str, Any]) -> bool:
    return lock_kind_from_card(card) == "conceptual_spine"


def is_full_operator_lock(card: dict[str, Any]) -> bool:
    kind = lock_kind_from_card(card)
    return kind == "full" or (is_locked_card(card) and kind != "maintenance_core")


def is_consumable_for_pack(vault_root: Path, trinity_id: str) -> bool:
    """Production trinity_pack may reference locked, core, conceptual-spine, or usage_proven ids."""
    tid = str(trinity_id or "").strip()
    if not tid:
        return False
    if is_usage_proven_id(vault_root, tid):
        try:
            load_trinity_card(vault_root, tid, prefer="locked")
            return True
        except (OSError, ValueError, FileNotFoundError):
            return False
    if is_maintenance_core_id(vault_root, tid):
        try:
            load_trinity_card(vault_root, tid, prefer="locked")
            return True
        except (OSError, ValueError, FileNotFoundError):
            return False
    try:
        card = load_trinity_card(vault_root, tid)
    except (OSError, ValueError, FileNotFoundError):
        return False
    if is_conceptual_spine_locked(card):
        return True
    return is_full_operator_lock(card)


def system_may_mutate(
    vault_root: Path,
    trinity_id: str,
    action: str = "write_trinity_card",
    *,
    operator_override: bool | None = None,
) -> bool:
    if operator_override is None:
        operator_override = operator_mutation_ctx.get()
    if operator_override:
        return True
    if is_maintenance_core_id(vault_root, trinity_id):
        if action in CORE_HASH_RECONCILE_ACTIONS:
            return True
        policy = load_maintenance_core_policy(vault_root)
        return policy.system_mutable
    if is_usage_proven_id(vault_root, trinity_id):
        if action in CORE_HASH_RECONCILE_ACTIONS:
            return True
        return False
    return True


def assert_system_may_mutate(
    vault_root: Path,
    trinity_id: str,
    action: str,
    *,
    operator_override: bool | None = None,
) -> None:
    if not system_may_mutate(
        vault_root,
        trinity_id,
        action,
        operator_override=operator_override,
    ):
        raise SystemMutationForbidden(trinity_id, action)


def filter_mutable_trinity_ids(
    vault_root: Path,
    trinity_ids: list[str],
    *,
    operator_override: bool | None = None,
) -> tuple[list[str], list[str]]:
    """Return (mutable, skipped_core) for batch harness paths."""
    mutable: list[str] = []
    skipped: list[str] = []
    for tid in trinity_ids:
        if system_may_mutate(vault_root, tid, operator_override=operator_override):
            mutable.append(tid)
        elif is_maintenance_core_id(vault_root, tid) or is_usage_proven_id(vault_root, tid):
            skipped.append(tid)
        else:
            mutable.append(tid)
    return mutable, skipped


def apply_lock_kind_to_card(
    card: dict[str, Any],
    lock_kind: LockKind,
    *,
    now_iso: str,
) -> dict[str, Any]:
    """Operator lock_card — stamp meta for full, conceptual_spine, or core re-lock."""
    meta = dict(_card_meta(card))
    src = dict(meta.get("source") or {}) if isinstance(meta.get("source"), dict) else {}

    if lock_kind == "conceptual_spine":
        meta["provisional"] = False
        meta["promotion_tier"] = "locked"
        meta["card_class"] = "complete_draft"
        meta["lock_kind"] = "conceptual_spine"
        meta["system_mutable"] = True
        meta["conceptual_confirmed_at"] = now_iso
        meta.pop("rules_confirmed_at", None)
        src["locked_at"] = now_iso
        src["locked_from"] = "component-proposals"
        src["lock_kind"] = "conceptual_spine"
    elif lock_kind == "maintenance_core":
        meta["provisional"] = False
        meta["promotion_tier"] = "locked"
        meta["card_class"] = "complete_draft"
        meta["lock_kind"] = "maintenance_core"
        meta["system_mutable"] = False
        meta["conceptual_confirmed_at"] = now_iso
        meta["rules_confirmed_at"] = now_iso
        src["locked_at"] = now_iso
        src["locked_from"] = "component-proposals"
        src["lock_kind"] = "maintenance_core"
    else:
        meta["provisional"] = False
        meta["promotion_tier"] = "locked"
        meta["card_class"] = "complete_draft"
        meta.pop("lock_kind", None)
        meta.pop("system_mutable", None)
        meta["conceptual_confirmed_at"] = now_iso
        meta["rules_confirmed_at"] = now_iso
        src["locked_at"] = now_iso
        src["locked_from"] = "component-proposals"

    meta["source"] = src
    card["meta"] = meta
    return card


def apply_usage_proven_to_card(
    card: dict[str, Any],
    *,
    evidence: dict[str, Any] | None = None,
    now_iso: str,
) -> dict[str, Any]:
    """Stamp usage_proven earned freeze — system_mutable=false; operator unfreeze only."""
    meta = dict(_card_meta(card))
    src = dict(meta.get("source") or {}) if isinstance(meta.get("source"), dict) else {}
    meta["provisional"] = False
    meta["promotion_tier"] = "locked"
    meta["card_class"] = "complete_draft"
    meta["lock_kind"] = "usage_proven"
    meta["system_mutable"] = False
    meta["usage_proven_at"] = now_iso
    if evidence:
        meta["usage_proven_evidence"] = evidence
    src["locked_at"] = now_iso
    src["locked_from"] = "component-proposals"
    src["lock_kind"] = "usage_proven"
    meta["source"] = src
    card["meta"] = meta
    return card
