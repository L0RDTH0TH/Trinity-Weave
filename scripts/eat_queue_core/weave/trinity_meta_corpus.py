"""Phase 11 — meta corpus charter workflow (config-gated; default off)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import load_trinity_config

# Phase 11 meta ids merged into generator/audit when charter master switch is on.
DEFAULT_META_GENERATION_LOAD_IDS: tuple[str, ...] = (
    "agent_implementation_style",
    "harness_runtime_contract",
    "schedule_event_planes",
    "cursor_host_adapter",
    "persona_atlas",
    "vault_layout_naming_doctrine",
    "maintenance_honesty_anchor",
    "config_knob_parity",
    "factory_lifecycle_doctrine",
    "trinity_prompt_context",
)


def meta_corpus_charter_status(vault_root: Path) -> dict[str, Any]:
    """Report charter workflow state — bulk promote deferred unless explicitly enabled."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    enabled = bool(getattr(cfg, "meta_corpus_enabled", False))
    charter = bool(getattr(cfg, "meta_corpus_charter_enabled", False))
    deferred = bool(getattr(cfg, "queue_payload_meta_deferred", True))
    load_ids = resolve_meta_generation_load_ids(vault_root)

    return {
        "ok": True,
        "trinity_meta_corpus_enabled": enabled,
        "trinity_meta_corpus_charter_enabled": charter,
        "trinity_queue_payload_meta_deferred": deferred,
        "bulk_promote_active": enabled and charter,
        "bulk_promote_deferred": not (enabled and charter),
        "meta_generation_load_ids": load_ids,
        "default_off": not enabled,
        "reason": (
            "charter_bulk_promote_off"
            if not charter
            else ("master_switch_off" if not enabled else "charter_active")
        ),
    }


def resolve_meta_generation_load_ids(vault_root: Path) -> list[str]:
    """Ids for generator/audit context — empty when master switch off."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not getattr(cfg, "meta_corpus_enabled", False):
        return []

    explicit = getattr(cfg, "meta_generation_load_ids", ()) or ()
    if explicit:
        return list(explicit)
    return list(DEFAULT_META_GENERATION_LOAD_IDS)


def merge_meta_generation_context(
    vault_root: Path,
    base_ids: list[str] | tuple[str, ...],
) -> list[str]:
    """Merge charter load ids into a base list when enabled; no-op when off."""
    extra = resolve_meta_generation_load_ids(vault_root)
    if not extra:
        return list(base_ids)
    seen: set[str] = set()
    out: list[str] = []
    for mid in [*base_ids, *extra]:
        if mid and mid not in seen:
            seen.add(mid)
            out.append(mid)
    return out
