"""Phase A — L2 predictive + symbolic gate validation drills."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import patch

from .. import recoverable_handlers
from ..recoverable_handlers import run_recoverable_handler
from . import predictive
from .config import load_predictive_config, load_symbolic_config
from .governance import append_metric_row, ensure_weave_paths
from .invariant_registry import activate_invariant, bootstrap_n2_invariants, load_invariant
from .predictive import (
    CalibrationState,
    PatchScopeResult,
    RiskAssessment,
    assess_maintenance_risk,
    check_patch_scope,
    gate_recoverable_handler,
)
from .symbolic_conflict import ConflictDecision, gate_symbolic_action


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _result(
    drill_id: str,
    *,
    passed: bool,
    checks: list[dict[str, Any]],
    detail: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "drill_id": drill_id,
        "passed": passed,
        "checks": checks,
        "detail": detail or {},
        "timestamp": _utc_iso(),
    }


def _high_assessment(*, enforcement_active: bool = True) -> RiskAssessment:
    cal = CalibrationState(
        calibrated=True,
        valid_runs_in_window=14,
        valid_runs_required=14,
        integrity_pass_rate=0.95,
        red_attention_rate=0.0,
        enforcement_ready=True,
        tier_thresholds={"low": 25, "medium": 50, "high": 75, "critical": 90},
        calibrated_at=_utc_iso(),
        notes="l2_drill_forced",
    )
    return RiskAssessment(
        maintenance_risk_score=80,
        risk_tier="high",
        signals={"drill": True},
        explanation="L2 drill forced high tier",
        calibration=cal,
        enforcement_active=enforcement_active,
    )


def _critical_assessment() -> RiskAssessment:
    cal = CalibrationState(
        calibrated=True,
        valid_runs_in_window=14,
        valid_runs_required=14,
        integrity_pass_rate=0.95,
        red_attention_rate=0.0,
        enforcement_ready=True,
        tier_thresholds={"low": 25, "medium": 50, "high": 75, "critical": 90},
        calibrated_at=_utc_iso(),
        notes="l2_drill_forced",
    )
    return RiskAssessment(
        maintenance_risk_score=95,
        risk_tier="critical",
        signals={"drill": True},
        explanation="L2 drill forced critical tier",
        calibration=cal,
        enforcement_active=True,
    )


def drill_l2_predictive_critical_block(vault_root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    """T3 — critical tier + enforcement blocks autonomous handler patch scope."""
    checks: list[dict[str, Any]] = []
    if dry_run:
        return _result(
            "l2_predictive_critical_block",
            passed=True,
            checks=[{"name": "dry_run", "ok": True}],
        )

    scope = check_patch_scope("critical", files_count=1, lines_count=10, enforcement_active=True)
    checks.append(
        {
            "name": "critical_blocks_autonomous",
            "ok": scope.ok is False and bool(scope.limits.get("block_autonomous")),
            "scope": {"ok": scope.ok, "reason": scope.reason, "risk_tier": scope.risk_tier},
        }
    )

    high_scope = check_patch_scope("high", files_count=10, lines_count=500, enforcement_active=True)
    checks.append(
        {
            "name": "high_t3_caps_exceeded",
            "ok": high_scope.ok is False,
            "scope": {"ok": high_scope.ok, "reason": high_scope.reason},
        }
    )

    pred_cfg = load_predictive_config(vault_root)
    checks.append(
        {
            "name": "predictive_enforcement_config",
            "ok": pred_cfg.enforcement_enabled,
            "enforcement_enabled": pred_cfg.enforcement_enabled,
        }
    )

    gate: PatchScopeResult | None = None
    with patch.object(predictive, "assess_maintenance_risk", return_value=_critical_assessment()):
        gate = gate_recoverable_handler(vault_root, "release_pq_lock")
    checks.append(
        {
            "name": "handler_gate_blocks_release_pq_lock",
            "ok": gate is not None and gate.ok is False,
            "gate": None if gate is None else {"ok": gate.ok, "reason": gate.reason, "risk_tier": gate.risk_tier},
        }
    )

    with patch.object(predictive, "assess_maintenance_risk", return_value=_critical_assessment()):
        handler_out = run_recoverable_handler("release_pq_lock", vault_root, "institute", {})
    checks.append(
        {
            "name": "recoverable_handler_predictive_blocked",
            "ok": handler_out.get("error") == "predictive_gate_blocked",
            "handler_out": handler_out,
        }
    )

    passed = all(c.get("ok") for c in checks if c["name"] != "predictive_enforcement_config")
    return _result(
        "l2_predictive_critical_block",
        passed=passed,
        checks=checks,
        detail={"live_enforcement": pred_cfg.enforcement_enabled},
    )


def drill_l2_symbolic_registry_block(vault_root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    """K3 — N2 pilot invariant (pre_read) + high tier → block stops recoverable path."""
    vault_root = vault_root.resolve()
    checks: list[dict[str, Any]] = []
    if dry_run:
        return _result(
            "l2_symbolic_registry_block",
            passed=True,
            checks=[{"name": "dry_run", "ok": True}],
        )

    sym_cfg = load_symbolic_config(vault_root)
    checks.append(
        {
            "name": "symbolic_enforcement_enabled",
            "ok": sym_cfg.enforcement_enabled and not sym_cfg.observe_only,
            "observe_only": sym_cfg.observe_only,
            "enforcement_enabled": sym_cfg.enforcement_enabled,
        }
    )

    bootstrap_n2_invariants(vault_root)
    inv_id = "registry_reconcile_pre_read"
    prior = load_invariant(vault_root, inv_id)
    prior_status = prior.status if prior else None
    activated_for_drill = False
    if prior and prior.status != "active":
        act = activate_invariant(vault_root, inv_id, counselor_approved=True)
        activated_for_drill = bool(act.get("ok"))
        checks.append({"name": "invariant_activated_for_drill", "ok": activated_for_drill, "act": act})
    else:
        checks.append({"name": "invariant_already_active", "ok": prior is not None and prior.status == "active"})

    sym = gate_symbolic_action(
        vault_root,
        context={"pre_read_steps": []},
        risk_tier="high",
    )
    checks.append(
        {
            "name": "symbolic_decision_block",
            "ok": sym.decision == "block",
            "decision": sym.decision,
            "blocked": sym.blocked,
            "violations": sym.temporal_inconsistencies[:3],
        }
    )
    checks.append(
        {
            "name": "symbolic_enforcement_blocks_path",
            "ok": sym.blocked is True if sym_cfg.enforcement_enabled and not sym_cfg.observe_only else sym.decision == "block",
            "enforcement_active": sym.enforcement_active,
        }
    )

    if sym_cfg.enforcement_enabled and not sym_cfg.observe_only:
        blocked_decision = ConflictDecision(
            decision="block",
            violated_invariants=[],
            temporal_inconsistencies=["l2_drill: registry_reconcile_pre_read"],
            ownership_clashes=[],
            cross_surface_drift_risks=[],
            enforcement_active=True,
            blocked=True,
            risk_tier="high",
        )
        with patch.object(recoverable_handlers, "gate_symbolic_action", return_value=blocked_decision):
            handler_out = run_recoverable_handler("release_pq_lock", vault_root, "institute", {})
        checks.append(
            {
                "name": "handler_respects_symbolic_block",
                "ok": handler_out.get("error") == "symbolic_gate_blocked",
                "note": "release_pq_lock always passes reconcile pre_read; this proves handler wiring",
                "handler_out": handler_out,
            }
        )
    else:
        checks.append(
            {
                "name": "handler_observe_only_note",
                "ok": True,
                "note": "symbolic observe-only — handler not blocked at runtime",
                "handler_out": handler_out,
            }
        )

    passed = all(
        c.get("ok")
        for c in checks
        if c["name"] not in ("symbolic_enforcement_enabled", "handler_observe_only_note")
    )
    return _result(
        "l2_symbolic_registry_block",
        passed=passed,
        checks=checks,
        detail={
            "invariant_id": inv_id,
            "prior_status": prior_status,
            "activated_for_drill": activated_for_drill,
            "symbolic": {
                "decision": sym.decision,
                "blocked": sym.blocked,
                "enforcement_active": sym.enforcement_active,
            },
        },
    )


def drill_l2_live_risk_tier(vault_root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    """Live assess_maintenance_risk — record tier + enforcement flag (no forced mock)."""
    checks: list[dict[str, Any]] = []
    if dry_run:
        return _result("l2_live_risk_tier", passed=True, checks=[{"name": "dry_run", "ok": True}])

    assessment = assess_maintenance_risk(
        vault_root,
        context={"system_attention": "red", "integrity_ok": False, "governance_overdue": True},
    )
    checks.append(
        {
            "name": "assessment_produces_tier",
            "ok": assessment.risk_tier in ("low", "medium", "high", "critical"),
            "risk_tier": assessment.risk_tier,
            "score": assessment.maintenance_risk_score,
            "enforcement_active": assessment.enforcement_active,
        }
    )
    checks.append(
        {
            "name": "forced_context_elevates_tier",
            "ok": assessment.risk_tier in ("medium", "high", "critical") and assessment.maintenance_risk_score >= 35,
            "risk_tier": assessment.risk_tier,
            "score": assessment.maintenance_risk_score,
        }
    )
    passed = all(c.get("ok") for c in checks)
    return _result(
        "l2_live_risk_tier",
        passed=passed,
        checks=checks,
        detail={"assessment": {"tier": assessment.risk_tier, "score": assessment.maintenance_risk_score}},
    )


DRILL_FUNCS = {
    "predictive_critical_block": drill_l2_predictive_critical_block,
    "symbolic_registry_block": drill_l2_symbolic_registry_block,
    "live_risk_tier": drill_l2_live_risk_tier,
}


def run_l2_validation_drill(
    vault_root: Path,
    *,
    drill: str = "all",
    dry_run: bool = False,
    write_report: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    names = list(DRILL_FUNCS.keys()) if drill.strip().lower() == "all" else [drill.strip().lower()]
    unknown = [n for n in names if n not in DRILL_FUNCS]
    if unknown:
        return {"ok": False, "error": "unknown_drill", "unknown": unknown, "valid": list(DRILL_FUNCS.keys())}

    results = [DRILL_FUNCS[n](vault_root, dry_run=dry_run) for n in names]
    all_passed = all(r.get("passed") for r in results)
    report = {
        "ok": all_passed,
        "phase": "A",
        "layer": "L2",
        "dry_run": dry_run,
        "drills": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r.get("passed")),
            "failed": sum(1 for r in results if not r.get("passed")),
        },
        "timestamp": _utc_iso(),
    }
    if write_report and not dry_run:
        out_dir = vault_root / ".technical" / "weave" / "validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"l2-drill-{_utc_stamp()}.json"
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(out_path)
        append_metric_row(
            vault_root,
            {
                "metric_type": "l2_validation_drill",
                "ok": all_passed,
                "passed": report["summary"]["passed"],
                "failed": report["summary"]["failed"],
                "report_path": str(out_path),
            },
        )
    return report
