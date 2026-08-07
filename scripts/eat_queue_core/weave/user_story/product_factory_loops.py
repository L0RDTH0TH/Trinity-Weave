"""Operator loop aggregates for product factory (BOM v2 + conductor)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog_coverage import run_catalog_coverage_structure, run_catalog_coverage_strict
from .catalog_io import catalog_rows_by_id, load_json, load_yaml, parse_state_frontmatter, user_story_paths
from .catalog_mint_propose import _find_pmg_path
from .depth_scope import resolve_dispatch_depth, scope_path
from .product_factory_state import execution_track_exists, load_product_factory
from .product_factory_ux_context import validate_ux_context
from .user_story_feedback import (
    all_rows_operator_confirmed,
    all_rows_scopes_validated,
    load_user_story_feedback,
)
from .wire_execution_pins import wire_execution_pins


@dataclass(frozen=True)
class LoopCheck:
    loop_id: str
    ok: bool
    sub_checks: tuple[tuple[str, bool, str], ...]  # id, pass, detail

    @property
    def blocked_at(self) -> str | None:
        return None if self.ok else self.loop_id


from .product_factory_budget import budget_row_ids as _budget_row_ids


def _pmg_normalized(pmg_path: Path | None) -> bool:
    if not pmg_path or not pmg_path.is_file():
        return False
    text = pmg_path.read_text(encoding="utf-8", errors="replace")
    return "is_master_goal" in text or "Master Goal" in text or "One-line" in text


def check_operator_loop_1(vault_root: Path, project_id: str) -> LoopCheck:
    pmg = _find_pmg_path(vault_root, project_id)
    checks: list[tuple[str, bool, str]] = [
        ("pmg_exists", pmg is not None, "pmg_found" if pmg else "pmg_missing"),
        ("pmg_normalized", _pmg_normalized(pmg), "pmg_normalized" if _pmg_normalized(pmg) else "pmg_not_normalized"),
    ]
    ok = all(c[1] for c in checks)
    return LoopCheck("operator_loop_1_pmg", ok, tuple(checks))


def check_operator_loop_2(vault_root: Path, project_id: str) -> LoopCheck:
    """Exit criteria for Operator Loop 2 (depth slice + level validate + sign).

    ``depth_sliced`` (L1 present) is an *exit* check. The pipeline must run
    ``run_depth_slicer`` before requiring this check to pass — do not treat
    missing L1 as a reason to refuse starting the slicer.
    """
    paths = user_story_paths(vault_root, project_id)
    state = parse_state_frontmatter(paths["state"])
    row_ids = _budget_row_ids(vault_root, project_id)

    struct = run_catalog_coverage_structure(vault_root, project_id=project_id)
    l5_missing: list[str] = []
    for rid in row_ids:
        l5 = scope_path(vault_root, project_id, rid, 5)
        if not l5.is_file() or len(l5.read_text(encoding="utf-8", errors="replace").strip()) < 80:
            l5_missing.append(rid)

    l1_missing: list[str] = []
    for rid in row_ids:
        if not scope_path(vault_root, project_id, rid, 1).is_file():
            l1_missing.append(rid)

    budget = load_json(paths["budget"])
    has_budget = bool(budget.get("rows"))
    signed = bool(state.get("catalog_signed_at"))
    feedback = load_user_story_feedback(vault_root, project_id)
    if signed and not feedback:
        levels_confirmed = True
    else:
        levels_confirmed = all_rows_operator_confirmed(vault_root, project_id, row_ids) if row_ids else signed
    scopes_validated = all_rows_scopes_validated(vault_root, project_id, row_ids) if row_ids else False

    checks: list[tuple[str, bool, str]] = [
        ("catalog_exists", paths["catalog"].is_file(), "catalog_ok" if paths["catalog"].is_file() else "catalog_missing"),
        (
            "catalog_coverage_structure",
            struct.ok,
            "structure_ok" if struct.ok else ";".join(struct.violations),
        ),
        ("l5_complete_per_row", not l5_missing, f"missing:{l5_missing}" if l5_missing else "l5_ok"),
        ("depth_sliced", not l1_missing, f"missing_l1:{l1_missing}" if l1_missing else "sliced_ok"),
        (
            "scopes_operator_validated",
            scopes_validated,
            "scopes_validated" if scopes_validated else "awaiting_scope_read",
        ),
        ("rollout_budget_set", has_budget, "budget_ok" if has_budget else "budget_missing"),
        (
            "catalog_levels_signed",
            signed and levels_confirmed,
            f"signed={signed}:levels_confirmed={levels_confirmed}",
        ),
    ]
    ok = all(c[1] for c in checks)
    return LoopCheck("operator_loop_2_catalog_levels", ok, tuple(checks))


def check_execution_engineering(vault_root: Path, project_id: str) -> LoopCheck:
    pf = load_product_factory(vault_root, project_id)
    exec_exists = execution_track_exists(vault_root, project_id)
    pins = wire_execution_pins(vault_root, project_id=project_id)
    strict = run_catalog_coverage_strict(vault_root, project_id=project_id)
    ux = pf.get("ux_context")
    ux_val = (
        validate_ux_context({"ux_context": ux, "product_factory_run_id": pf.get("run_id")})
        if isinstance(ux, dict)
        else validate_ux_context({})
    )
    ux_ready = ux_val.ok

    checks: list[tuple[str, bool, str]] = [
        ("execution_track_scaffolded", exec_exists, "execution_ok" if exec_exists else "execution_missing"),
        ("execution_pins_wired", pins.ok, ";".join(pins.violations) if pins.violations else "pins_ok"),
        ("catalog_coverage_strict", strict.ok, ";".join(strict.violations) if strict.violations else "strict_ok"),
        ("ux_context_envelope_ready", ux_ready, "ux_context_ok" if ux_ready else ";".join(ux_val.violations)),
    ]
    ok = all(c[1] for c in checks)
    loop_id = "machine:execution_engineering"
    return LoopCheck(loop_id, ok, tuple(checks))


def check_operator_loop_3(vault_root: Path, project_id: str) -> LoopCheck:
    pf = load_product_factory(vault_root, project_id)
    active = pf.get("active_slice") if isinstance(pf.get("active_slice"), dict) else {}
    row_ids = active.get("row_ids") if isinstance(active.get("row_ids"), list) else []
    row_ids = [str(x) for x in row_ids if x]
    dispatch_depth = active.get("dispatch_depth")
    confirmed = bool(pf.get("slice_selection_confirmed_at"))

    depth_ok = True
    detail = "dispatch_ok"
    if row_ids and dispatch_depth is not None:
        budget = load_json(user_story_paths(vault_root, project_id)["budget"])
        by_id = {str(r.get("row_id")): r for r in budget.get("rows") or [] if isinstance(r, dict)}
        for rid in row_ids:
            br = by_id.get(rid) or {}
            cur = int(br.get("current_depth") or 0)
            tgt = int(br.get("target_depth") or 0)
            expected = resolve_dispatch_depth(cur, tgt)
            if expected != int(dispatch_depth):
                depth_ok = False
                detail = f"{rid}:expected={expected}:got={dispatch_depth}"
                break

    checks: list[tuple[str, bool, str]] = [
        ("active_slice_declared", bool(row_ids), f"rows={row_ids}" if row_ids else "no_active_rows"),
        (
            "dispatch_depth_set",
            dispatch_depth is not None and depth_ok,
            detail if dispatch_depth is not None else "dispatch_depth_missing",
        ),
        ("slice_confirmed", confirmed, "confirmed" if confirmed else "awaiting_confirm"),
    ]
    ok = all(c[1] for c in checks)
    return LoopCheck("operator_loop_3_slice_selection", ok, tuple(checks))


def resolve_blocking_operator_loop(vault_root: Path, project_id: str) -> str | None:
    """First operator loop that is not green (1 → 2 → 3). Machine phases not included."""
    for fn in (check_operator_loop_1, check_operator_loop_2, check_operator_loop_3):
        chk = fn(vault_root, project_id)
        if not chk.ok and chk.loop_id.startswith("operator_loop_"):
            return chk.loop_id
    return None


def loop_status_dict(vault_root: Path, project_id: str) -> dict[str, Any]:
    l1 = check_operator_loop_1(vault_root, project_id)
    l2 = check_operator_loop_2(vault_root, project_id)
    l3 = check_operator_loop_3(vault_root, project_id)
    eng = check_execution_engineering(vault_root, project_id)
    blocked = resolve_blocking_operator_loop(vault_root, project_id)
    if not blocked and not eng.ok:
        blocked = eng.loop_id
    return {
        "operator_loop_1_pmg": {"ok": l1.ok, "sub_checks": l1.sub_checks},
        "operator_loop_2_catalog_levels": {"ok": l2.ok, "sub_checks": l2.sub_checks},
        "execution_engineering": {"ok": eng.ok, "sub_checks": eng.sub_checks},
        "operator_loop_3_slice_selection": {"ok": l3.ok, "sub_checks": l3.sub_checks},
        "blocked_at": blocked,
    }
