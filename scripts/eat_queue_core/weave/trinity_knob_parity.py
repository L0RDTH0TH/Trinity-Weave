"""Phase 16 — knob parity matrix proofs (factory × knob-option cells)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from ..config_resolve_profile import (
    CANONICAL_KNOB_FAMILIES,
    DEFAULT_FAMILIAL_BUNDLE,
    ResolveResult,
    all_single_knob_sweeps,
    resolve_profile,
)
from .config import load_trinity_config
from .trinity_card_paths import load_trinity_card

MATRIX_ARTIFACT = Path(".technical/weave/validation/knob-parity-matrix.json")

FactoryCheck = Callable[[ResolveResult, dict[str, str]], tuple[bool, list[str]]]


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _nested_get(d: dict[str, Any], *keys: str, default: Any = None) -> Any:
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
    return cur if cur is not None else default


def _check_queue_dispatch(res: ResolveResult, familial: dict[str, str]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    flat = res.expanded_flat
    pm = flat.get("pipeline_mode")
    if not pm:
        errors.append("missing pipeline_mode")
    rpo = _nested_get(flat, "queue", "roadmap_pass_order")
    expected_rpo = familial.get("repair_strategy", "repair_first")
    if rpo != expected_rpo:
        errors.append(f"roadmap_pass_order={rpo!r} expected {expected_rpo!r}")
    tiered = _nested_get(flat, "validator", "tiered_blocks_enabled")
    if familial.get("validator_tier") == "forgiving" and tiered is not True:
        errors.append(f"tiered_blocks_enabled={tiered!r} expected True for forgiving")
    if familial.get("validator_tier") == "aggressive" and tiered is not False:
        errors.append(f"tiered_blocks_enabled={tiered!r} expected False for aggressive")
    return len(errors) == 0, errors


def _check_gitforge_tail(res: ResolveResult, familial: dict[str, str]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    mode = res.expanded_flat.get("gitforge_effective_mode")
    sm = familial.get("speed_mode", "balance")
    if sm == "fast" and mode != "speed":
        errors.append(f"fast speed_mode must map gitforge to speed, got {mode!r}")
    if sm in ("balance", "extreme") and mode != "balance":
        errors.append(f"{sm} speed_mode must map gitforge to balance, got {mode!r}")
    return len(errors) == 0, errors


def _check_corps_sweep(res: ResolveResult, _familial: dict[str, str]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if res.unknown_tokens:
        errors.append(f"unknown_tokens={res.unknown_tokens}")
    if not res.expanded_flat.get("pipeline_mode"):
        errors.append("missing pipeline_mode after expansion")
    return len(errors) == 0, errors


def _check_weave_self_wrap(res: ResolveResult, familial: dict[str, str]) -> tuple[bool, list[str]]:
    ok, errs = _check_corps_sweep(res, familial)
    if familial.get("speed_mode") == "extreme":
        if res.expanded_flat.get("target_nested_validator_passes") != 4:
            errs.append("extreme speed_mode must set target_nested_validator_passes=4")
            ok = False
    return ok, errs


def _check_roadmap_resume(res: ResolveResult, familial: dict[str, str]) -> tuple[bool, list[str]]:
    return _check_queue_dispatch(res, familial)


FACTORY_REGISTRY: dict[str, dict[str, Any]] = {
    "queue_dispatch": {
        "description": "Layer 1 EAT-QUEUE / multi-dispatch graph",
        "required_families": tuple(CANONICAL_KNOB_FAMILIES.keys()),
        "check": _check_queue_dispatch,
    },
    "roadmap_resume": {
        "description": "RESUME_ROADMAP deepen/recal dispatch",
        "required_families": tuple(CANONICAL_KNOB_FAMILIES.keys()),
        "check": _check_roadmap_resume,
    },
    "corps_sweep": {
        "description": "Phase 10 corps full-corpus nerve",
        "required_families": ("speed_mode", "validator_tier"),
        "check": _check_corps_sweep,
    },
    "weave_self_wrap": {
        "description": "trinity_weave_self_wrap combined cycle",
        "required_families": tuple(CANONICAL_KNOB_FAMILIES.keys()),
        "check": _check_weave_self_wrap,
    },
    "gitforge_tail": {
        "description": "Post-A.7a GitForge harness skip policy",
        "required_families": ("speed_mode",),
        "check": _check_gitforge_tail,
    },
}


def load_meta_knob_families(vault_root: Path) -> dict[str, list[str]] | None:
    try:
        card = load_trinity_card(vault_root, "config_knob_parity", prefer="locked")
    except (OSError, ValueError):
        return None
    touch = card.get("touch") or {}
    raw = touch.get("knob_families")
    if not isinstance(raw, dict):
        return None
    return {str(k): [str(x) for x in v] for k, v in raw.items()}


def meta_knob_drift(vault_root: Path) -> list[dict[str, Any]]:
    """Report when locked meta touch.knob_families diverges from Config-Profiles canonical."""
    meta = load_meta_knob_families(vault_root)
    if not meta:
        return [{"issue": "meta_unreadable"}]
    drift: list[dict[str, Any]] = []
    for family, canonical in CANONICAL_KNOB_FAMILIES.items():
        meta_opts = tuple(meta.get(family) or [])
        if meta_opts != canonical:
            drift.append(
                {
                    "family": family,
                    "canonical": list(canonical),
                    "meta_touch": list(meta_opts),
                }
            )
    return drift


def build_matrix_cells(
    *,
    config_flat: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Factory × single-knob sweep cells."""
    cells: list[dict[str, Any]] = []
    sweeps = all_single_knob_sweeps()

    for factory_id, spec in FACTORY_REGISTRY.items():
        check: FactoryCheck = spec["check"]
        required: tuple[str, ...] = spec["required_families"]
        for sweep in sweeps:
            varied = [f for f in required if sweep.get(f) != DEFAULT_FAMILIAL_BUNDLE.get(f)]
            if not varied:
                continue
            if varied[0] not in required:
                continue
            familial = {k: sweep[k] for k in CANONICAL_KNOB_FAMILIES if k in sweep}
            params = dict(familial)
            res = resolve_profile(params, config_flat=config_flat)
            ok, errors = check(res, familial)
            cells.append(
                {
                    "factory": factory_id,
                    "familial": familial,
                    "varied_family": varied[0],
                    "varied_option": sweep.get(varied[0]),
                    "ok": ok,
                    "errors": errors,
                    "pipeline_mode": res.expanded_flat.get("pipeline_mode"),
                }
            )
    return cells


def run_knob_parity_proofs(
    vault_root: Path,
    *,
    dry_run: bool = False,
    write_artifact: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)

    if not getattr(cfg, "knob_parity_enabled", True):
        return {"ok": True, "skipped": True, "reason": "knob_parity_disabled"}

    drift = meta_knob_drift(vault_root)
    cells = build_matrix_cells()
    green = sum(1 for c in cells if c.get("ok"))
    red = len(cells) - green
    meta_card = load_meta_knob_families(vault_root) is not None

    report: dict[str, Any] = {
        "ok": red == 0,
        "dry_run": dry_run,
        "generated_at": _now_iso(),
        "canonical_families": {k: list(v) for k, v in CANONICAL_KNOB_FAMILIES.items()},
        "default_bundle": dict(DEFAULT_FAMILIAL_BUNDLE),
        "factories": list(FACTORY_REGISTRY.keys()),
        "meta_card_readable": meta_card,
        "meta_knob_drift": drift,
        "cells": cells,
        "summary": {
            "total": len(cells),
            "green": green,
            "red": red,
        },
        "artifact_path": str(MATRIX_ARTIFACT),
    }

    if drift and meta_card:
        report["meta_drift_advisory"] = True

    if not dry_run and write_artifact:
        out_path = vault_root / MATRIX_ARTIFACT
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["written"] = True

    if red > 0:
        report["ok"] = False
        report["red_cells"] = [c for c in cells if not c.get("ok")]

    return report
