"""Phase 13 — lens-informed align: load MVL bundle before align_spine (read-only steering)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .trinity_meta_corpus import meta_corpus_charter_status, resolve_meta_generation_load_ids
from .trinity_mvl_lens import (
    get_lens_contract,
    load_meta_lens_legs,
    probe_mvl_lens,
    resolve_config_slice,
)

# Meta ids that must appear in prepend + resolve for harness wiring (Phase 11 corpus).
_META_WIRING_REQUIRED: tuple[str, ...] = (
    "maintenance_honesty_anchor",
    "config_knob_parity",
    "factory_lifecycle_doctrine",
)

_META_WIRING_CORE: tuple[str, ...] = (
    "conceptual_style_guide",
    "trinity_card_authoring",
    "trinity_prompt_context",
    "host_execution_safety_contract",
    "agent_implementation_style",
    "harness_runtime_contract",
)


def verify_meta_corpus_harness_wiring(
    vault_root: Path,
    *,
    lens: Any | None = None,
    meta_legs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Confirm locked meta corpus ids are in prepend order and loadable."""
    vault_root = vault_root.resolve()
    lens = lens or get_lens_contract(vault_root)
    prepend = set(lens.meta_prepend_order)
    missing_prepend = [mid for mid in _META_WIRING_REQUIRED if mid not in prepend]

    if meta_legs is None:
        check_ids = list(dict.fromkeys([*lens.meta_prepend_order, *_META_WIRING_CORE]))
        meta_legs = load_meta_lens_legs(vault_root, check_ids)

    missing_locked: list[str] = []
    for mid in (*_META_WIRING_REQUIRED, *_META_WIRING_CORE):
        leg = meta_legs.get(mid) or {}
        if leg.get("error"):
            missing_locked.append(mid)

    wired = [
        mid
        for mid in (*_META_WIRING_REQUIRED, *_META_WIRING_CORE)
        if mid not in missing_prepend and mid not in missing_locked
    ]
    return {
        "ok": len(missing_prepend) == 0 and len(missing_locked) == 0,
        "missing_prepend": missing_prepend,
        "missing_locked_meta": missing_locked,
        "wired_ids": wired,
        "required_prepend": list(_META_WIRING_REQUIRED),
    }


def _build_steering_tags(
    lens: Any,
    meta_legs: dict[str, Any],
) -> list[dict[str, str]]:
    """Read-only disconnect tags for align / corps priority (no vault writes)."""
    tags: list[dict[str, str]] = []
    prepend = set(lens.meta_prepend_order)

    for mid in _META_WIRING_REQUIRED:
        if mid not in prepend:
            tags.append(
                {
                    "lens_disconnect_kind": "meta_prepend_gap",
                    "meta_id": mid,
                    "repair_class": "surgical",
                }
            )
        elif (meta_legs.get(mid) or {}).get("error"):
            tags.append(
                {
                    "lens_disconnect_kind": "meta_card_missing",
                    "meta_id": mid,
                    "repair_class": "surgical",
                }
            )

    if lens.source != "locked":
        tags.append(
            {
                "lens_disconnect_kind": "lens_fallback",
                "meta_id": "trinity_prompt_context",
                "repair_class": "surgical",
            }
        )

    return tags


def load_mvl_bundle(vault_root: Path) -> dict[str, Any]:
    """Load locked meta + config slice before align_spine (MVL conductor bundle)."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not getattr(cfg, "mvl_conductor_enabled", True):
        return {"ok": True, "skipped": True, "reason": "mvl_conductor_disabled"}
    if not getattr(cfg, "lens_informed_align_enabled", True):
        return {"ok": True, "skipped": True, "reason": "lens_informed_align_disabled"}

    lens = get_lens_contract(vault_root)
    meta_prepend = list(lens.meta_prepend_order)
    check_ids = list(dict.fromkeys([*meta_prepend, *_META_WIRING_CORE]))
    meta_legs = load_meta_lens_legs(vault_root, check_ids)
    config_slice = resolve_config_slice(vault_root)
    config_slice["meta_generation_load_ids"] = list(
        resolve_meta_generation_load_ids(vault_root)
    )
    steering_tags = _build_steering_tags(lens, meta_legs)
    wiring = verify_meta_corpus_harness_wiring(
        vault_root, lens=lens, meta_legs=meta_legs
    )
    charter = meta_corpus_charter_status(vault_root)

    return {
        "ok": True,
        "wiring_ok": wiring.get("ok", False),
        "lens_source": lens.source,
        "meta_prepend_order": meta_prepend,
        "meta_legs": meta_legs,
        "config_slice": config_slice,
        "steering_tags": steering_tags,
        "meta_corpus_wiring": wiring,
        "meta_corpus_charter": charter,
    }


def run_lens_informed_align_gate(vault_root: Path) -> dict[str, Any]:
    """Post-align validation: MVL probe + wiring (replaces probe-only placement)."""
    vault_root = vault_root.resolve()
    bundle = load_mvl_bundle(vault_root)
    if bundle.get("skipped"):
        return probe_mvl_lens(vault_root)
    probe = probe_mvl_lens(vault_root)
    return {
        **probe,
        "steering_tags": bundle.get("steering_tags") or [],
        "meta_corpus_wiring": bundle.get("meta_corpus_wiring"),
        "meta_corpus_charter": bundle.get("meta_corpus_charter"),
        "lens_informed_align": True,
    }
