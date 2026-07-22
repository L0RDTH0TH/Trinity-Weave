"""Closed Alpha tier passes — separate from stack_baseline release_readiness_pass."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .factory_honesty_rollup import run_product_kinesthetic_honesty_rollup
from .factory_little_val import FactoryLittleValResult, merge_results
from .factory_output_gate import run_factory_output_gate
from .gate_precedence import evaluate_precedence
from .review_pass_runner import ReviewPassResult
from .surface_pass import run_surface_pass
from .tech_stack_manifest import load_manifest


def run_closed_alpha_release_readiness_pass(vault_root: Path) -> ReviewPassResult:
    """
    Tier D rollup for Product 2 — requires stack baseline + Surface (Tier B) + conduct gate.

    Does NOT substitute harness smokes for Surface seat.
    """
    violations: list[str] = []

    try:
        manifest = load_manifest(vault_root)
    except FileNotFoundError:
        lv = FactoryLittleValResult(
            little_val_ok=False,
            anti_pattern_violations=["manifest_missing"],
            detail="closed_alpha_release_readiness_pass",
        )
        return ReviewPassResult("closed_alpha_release_readiness_pass", False, lv, "manifest_missing")

    if not manifest.operator_stack_baseline_vetted:
        violations.append("stack_baseline_not_vetted")

    surface = run_surface_pass(vault_root)
    if not surface.ok:
        violations.extend(surface.little_val.anti_pattern_violations)

    conduct = run_factory_output_gate(vault_root, mode="block")
    if not conduct.ok:
        violations.append("factory_output_conduct_fail")

    closed_alpha_doc = vault_root / (
        "1-Projects/genesis-mythos-master/Factory-DRB/Release-Definitions/closed-alpha-v1.md"
    )
    if closed_alpha_doc.is_file():
        text = closed_alpha_doc.read_text(encoding="utf-8")
        if "operator_closed_alpha_vetted: true" in text and not surface.ok:
            violations.append("release_def_claims_vetted_while_surface_fail")

    precedence = evaluate_precedence(
        {
            "surface_pass": surface.ok,
            "usability_pass": surface.ok,
            "factory_output_conduct": conduct.ok,
            "closed_alpha_release_readiness_pass": False,
        }
    )
    violations.extend(precedence.violations)

    ok = len(violations) == 0
    lv = merge_results(surface.little_val)
    lv.anti_pattern_violations = list(dict.fromkeys([*lv.anti_pattern_violations, *violations]))
    lv.little_val_ok = ok
    lv.detail = "closed_alpha_release_readiness_pass"

    return ReviewPassResult(
        "closed_alpha_release_readiness_pass",
        ok,
        lv,
        "; ".join(violations) if violations else "closed_alpha_release_readiness_ok",
    )


def run_all_closed_alpha_passes(vault_root: Path) -> dict[str, Any]:
    surface = run_surface_pass(vault_root)
    rollup = run_closed_alpha_release_readiness_pass(vault_root)
    conduct = run_factory_output_gate(vault_root, mode="block")
    pk_rollup = run_product_kinesthetic_honesty_rollup(vault_root)
    pk_result = pk_rollup["passes"]["product_kinesthetic_honesty"]

    pass_map = {
        "surface_pass": surface.ok,
        "usability_pass": surface.ok,
        "factory_output_conduct": conduct.ok,
        "product_kinesthetic_honesty": pk_result.ok,
        "closed_alpha_release_readiness_pass": rollup.ok,
    }
    precedence = evaluate_precedence(pass_map)

    results = {
        "surface_pass": ReviewPassResult("surface_pass", surface.ok, surface.little_val, surface.detail),
        "product_kinesthetic_honesty": pk_result,
        "closed_alpha_release_readiness_pass": rollup,
        "factory_output_conduct": ReviewPassResult(
            "factory_output_conduct",
            conduct.ok,
            FactoryLittleValResult(
                little_val_ok=conduct.ok,
                anti_pattern_violations=list(conduct.failures),
                detail="factory_output_conduct",
            ),
            "; ".join(conduct.failures) or "ok",
        ),
        "gate_precedence": ReviewPassResult(
            "gate_precedence",
            precedence.ok,
            FactoryLittleValResult(
                little_val_ok=precedence.ok,
                anti_pattern_violations=list(precedence.violations),
                detail=precedence.detail,
            ),
            precedence.detail,
        ),
    }

    all_ok = all(r.ok for r in results.values())
    return {"all_ok": all_ok, "passes": results, "precedence": precedence.to_dict()}
