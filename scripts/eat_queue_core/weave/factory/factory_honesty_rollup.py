"""Factory honesty rollup — stack_baseline_honesty + product_kinesthetic_honesty mirrors."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .factory_little_val import FactoryLittleValResult
from .product_kinesthetic_honesty import run_product_kinesthetic_honesty
from .review_pass_runner import ReviewPassResult, run_pipeline_proof_pass, run_release_readiness_pass


def run_stack_baseline_honesty_rollup(vault_root: Path) -> dict[str, Any]:
    """Mirror Trinity stack_baseline_honesty factory passes."""
    pipeline = run_pipeline_proof_pass(vault_root)
    release = run_release_readiness_pass(vault_root)
    passes = {
        "pipeline_proof_pass": pipeline,
        "release_readiness_pass": release,
    }
    all_ok = all(r.ok for r in passes.values())
    return {"all_ok": all_ok, "passes": passes}


def run_product_kinesthetic_honesty_rollup(vault_root: Path) -> dict[str, Any]:
    pk = run_product_kinesthetic_honesty(vault_root)
    result = ReviewPassResult(
        "product_kinesthetic_honesty",
        pk.ok,
        FactoryLittleValResult(pk.ok, list(pk.violations), pk.detail),
        pk.detail,
    )
    return {"all_ok": pk.ok, "passes": {"product_kinesthetic_honesty": result}}


def run_factory_honesty_rollup(vault_root: Path) -> dict[str, Any]:
    """Combined honesty rollup for overnight wind-down and dispatch snapshots."""
    stack = run_stack_baseline_honesty_rollup(vault_root)
    product = run_product_kinesthetic_honesty_rollup(vault_root)
    passes = {**stack["passes"], **product["passes"]}
    all_ok = bool(stack["all_ok"] and product["all_ok"])
    return {
        "all_ok": all_ok,
        "stack_baseline_honesty": stack,
        "product_kinesthetic_honesty": product,
        "passes": passes,
    }


def honesty_rollup_summary(rollup: dict[str, Any]) -> dict[str, Any]:
    """JSON-serializable summary for dispatch / overnight receipts."""
    out: dict[str, Any] = {"all_ok": rollup.get("all_ok")}
    for name, result in (rollup.get("passes") or {}).items():
        if isinstance(result, ReviewPassResult):
            out[name] = {
                "ok": result.ok,
                "detail": result.detail,
                "violations": list(result.little_val.anti_pattern_violations),
            }
    return out
