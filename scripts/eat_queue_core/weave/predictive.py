"""Phase 3 predictive maintenance — E2 rule tiers, S2 calibration, T1/T3 enforcement."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .config import PredictiveConfig, load_predictive_config
from .governance import append_metric_row, metrics_path, weave_dir

RiskTier = Literal["low", "medium", "high", "critical"]

TIER_ORDER = ("low", "medium", "high", "critical")

# T1 / T3 patch caps (locked plan)
PATCH_LIMITS: dict[str, dict[str, int | bool]] = {
    "low": {"max_files": 10, "max_lines": 500, "block_autonomous": False},
    "medium": {"max_files": 5, "max_lines": 300, "block_autonomous": False},
    "high": {"max_files": 3, "max_lines": 200, "block_autonomous": False},
    "critical": {"max_files": 1, "max_lines": 80, "block_autonomous": True},
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_iso(ts: str) -> datetime | None:
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return None


@dataclass(frozen=True)
class CalibrationState:
    """S2 calibration snapshot persisted under .technical/weave/."""

    calibrated: bool
    valid_runs_in_window: int
    valid_runs_required: int
    integrity_pass_rate: float
    red_attention_rate: float
    enforcement_ready: bool
    tier_thresholds: dict[str, int]
    calibrated_at: str | None
    notes: str

    # blast-radius: low


@dataclass(frozen=True)
class RiskAssessment:
    """E2 assessment for a maintenance context."""

    maintenance_risk_score: int
    risk_tier: RiskTier
    signals: dict[str, Any]
    explanation: str
    calibration: CalibrationState
    enforcement_active: bool

    # blast-radius: medium


@dataclass(frozen=True)
class PatchScopeResult:
    ok: bool
    reason: str
    risk_tier: RiskTier
    limits: dict[str, int | bool]


def calibration_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "predictive_calibration.json"


def load_calibration(vault_root: Path) -> CalibrationState | None:
    p = calibration_path(vault_root)
    if not p.is_file():
        return None
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(raw, dict):
        return None
    th = raw.get("tier_thresholds") or {}
    return CalibrationState(
        calibrated=bool(raw.get("calibrated")),
        valid_runs_in_window=int(raw.get("valid_runs_in_window") or 0),
        valid_runs_required=int(raw.get("valid_runs_required") or 14),
        integrity_pass_rate=float(raw.get("integrity_pass_rate") or 0.0),
        red_attention_rate=float(raw.get("red_attention_rate") or 0.0),
        enforcement_ready=bool(raw.get("enforcement_ready")),
        tier_thresholds={
            "medium": int(th.get("medium", 40)),
            "high": int(th.get("high", 60)),
            "critical": int(th.get("critical", 80)),
        },
        calibrated_at=raw.get("calibrated_at"),
        notes=str(raw.get("notes") or ""),
    )


def save_calibration(vault_root: Path, state: CalibrationState) -> Path:
    weave_dir(vault_root).mkdir(parents=True, exist_ok=True)
    payload = {
        "calibrated": state.calibrated,
        "valid_runs_in_window": state.valid_runs_in_window,
        "valid_runs_required": state.valid_runs_required,
        "integrity_pass_rate": state.integrity_pass_rate,
        "red_attention_rate": state.red_attention_rate,
        "enforcement_ready": state.enforcement_ready,
        "tier_thresholds": state.tier_thresholds,
        "calibrated_at": state.calibrated_at,
        "notes": state.notes,
    }
    p = calibration_path(vault_root)
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return p


def _load_refresh_metrics(vault_root: Path, cfg: PredictiveConfig) -> list[dict[str, Any]]:
    p = metrics_path(vault_root)
    if not p.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        if row.get("metric_type") != "lane_board_refresh":
            continue
        rows.append(row)
    if cfg.calibration_max_age_days > 0:
        cutoff = datetime.now(timezone.utc).timestamp() - cfg.calibration_max_age_days * 86400
        filtered: list[dict[str, Any]] = []
        for row in rows:
            ts = _parse_iso(str(row.get("timestamp") or ""))
            if ts and ts.timestamp() >= cutoff:
                filtered.append(row)
        rows = filtered
    return rows


def calibrate_predictive_tiers(vault_root: Path) -> CalibrationState:
    """S2 — derive tier thresholds from telemetry (valid runs window)."""
    cfg = load_predictive_config(vault_root)
    rows = _load_refresh_metrics(vault_root, cfg)
    valid = [r for r in rows if r.get("integrity_ok") is True]
    n_valid = len(valid)
    required = max(1, cfg.calibration_valid_runs)

    if not valid:
        state = CalibrationState(
            calibrated=False,
            valid_runs_in_window=0,
            valid_runs_required=required,
            integrity_pass_rate=0.0,
            red_attention_rate=0.0,
            enforcement_ready=False,
            tier_thresholds={"medium": 40, "high": 60, "critical": 80},
            calibrated_at=None,
            notes="no valid refresh metrics yet",
        )
        save_calibration(vault_root, state)
        return state

    pass_rate = n_valid / max(1, len(rows))
    red_rate = sum(1 for r in valid if str(r.get("system_attention") or "") == "red") / max(1, n_valid)

    # Tighten thresholds when stability is poor (S2 intent)
    medium = 40
    high = 60
    critical = 80
    if pass_rate < 0.9:
        medium, high, critical = 35, 55, 75
    if red_rate > 0.5:
        medium, high, critical = 30, 50, 70

    calibrated = n_valid >= required
    enforcement_ready = calibrated and pass_rate >= cfg.min_integrity_pass_rate_for_enforcement

    state = CalibrationState(
        calibrated=calibrated,
        valid_runs_in_window=n_valid,
        valid_runs_required=required,
        integrity_pass_rate=round(pass_rate, 4),
        red_attention_rate=round(red_rate, 4),
        enforcement_ready=enforcement_ready,
        tier_thresholds={"medium": medium, "high": high, "critical": critical},
        calibrated_at=_now_iso() if calibrated else None,
        notes=f"valid_runs={n_valid}/{required} pass_rate={pass_rate:.2f} red_rate={red_rate:.2f}",
    )
    save_calibration(vault_root, state)
    append_metric_row(
        vault_root,
        {
            "metric_type": "predictive_calibration",
            "calibrated": calibrated,
            "valid_runs_in_window": n_valid,
            "integrity_pass_rate": state.integrity_pass_rate,
            "enforcement_ready": enforcement_ready,
            "tier_thresholds": state.tier_thresholds,
        },
    )
    return state


def _score_to_tier(score: int, thresholds: dict[str, int]) -> RiskTier:
    if score >= thresholds.get("critical", 80):
        return "critical"
    if score >= thresholds.get("high", 60):
        return "high"
    if score >= thresholds.get("medium", 40):
        return "medium"
    return "low"


def _build_explanation(score: int, tier: RiskTier, signals: dict[str, Any], cal: CalibrationState) -> str:
    """E2 — rule-based explanation text (LLM may extend in reports; this is deterministic baseline)."""
    parts = [
        f"Maintenance risk score {score}/100 → tier **{tier}**.",
        f"Calibration: {'ready' if cal.calibrated else 'collecting'} "
        f"({cal.valid_runs_in_window}/{cal.valid_runs_required} valid runs).",
    ]
    if signals.get("system_attention") == "red":
        parts.append("System attention is red across lanes.")
    if signals.get("integrity_failures_recent"):
        parts.append(f"Recent integrity failures: {signals['integrity_failures_recent']}.")
    if signals.get("low_health_lanes"):
        parts.append(f"Low health lanes: {', '.join(signals['low_health_lanes'])}.")
    if signals.get("governance_overdue"):
        parts.append("Governance cadence overdue.")
    if cal.enforcement_ready:
        parts.append("T1/T3 patch caps are **enforced**.")
    else:
        parts.append("T1/T3 enforcement **observe-only** until S2 calibration completes.")
    return " ".join(parts)


def assess_maintenance_risk(
    vault_root: Path,
    *,
    context: dict[str, Any] | None = None,
) -> RiskAssessment:
    """E2 rule-based risk assessment for maintenance actions."""
    vault_root = vault_root.resolve()
    cfg = load_predictive_config(vault_root)
    ctx = context or {}

    cal = load_calibration(vault_root)
    if cal is None or not cal.calibrated:
        cal = calibrate_predictive_tiers(vault_root)

    rows = _load_refresh_metrics(vault_root, cfg)
    recent = rows[-5:] if rows else []
    integrity_fails = sum(1 for r in recent if r.get("integrity_ok") is False)
    last = rows[-1] if rows else {}
    system_attention = str(ctx.get("system_attention") or last.get("system_attention") or "unknown")
    health_map = ctx.get("lane_health_score") or last.get("lane_health_score") or {}
    if not isinstance(health_map, dict):
        health_map = {}

    low_health = [str(ln) for ln, sc in health_map.items() if isinstance(sc, (int, float)) and sc < 40]
    governance_overdue = bool(ctx.get("governance_overdue", False))

    score = 0
    if system_attention == "red":
        score += 30
    elif system_attention == "yellow":
        score += 15
    if integrity_fails:
        score += min(25, integrity_fails * 8)
    if last.get("integrity_ok") is False:
        score += 20
    score += min(20, len(low_health) * 8)
    if governance_overdue:
        score += 10
    if cal.integrity_pass_rate and cal.integrity_pass_rate < 0.85:
        score += 10
    score = min(100, max(0, score))

    tier = _score_to_tier(score, cal.tier_thresholds)
    signals = {
        "system_attention": system_attention,
        "integrity_failures_recent": integrity_fails,
        "low_health_lanes": low_health,
        "governance_overdue": governance_overdue,
        "lane_health_score": health_map,
    }
    enforcement_active = cfg.enforcement_enabled and cal.enforcement_ready
    explanation = _build_explanation(score, tier, signals, cal)

    append_metric_row(
        vault_root,
        {
            "metric_type": "predictive_risk_assessment",
            "maintenance_risk_score": score,
            "risk_tier": tier,
            "enforcement_active": enforcement_active,
            "signals": {k: v for k, v in signals.items() if k != "lane_health_score"},
        },
    )
    return RiskAssessment(
        maintenance_risk_score=score,
        risk_tier=tier,
        signals=signals,
        explanation=explanation,
        calibration=cal,
        enforcement_active=enforcement_active,
    )


def check_patch_scope(
    tier: RiskTier,
    *,
    files_count: int,
    lines_count: int,
    enforcement_active: bool,
) -> PatchScopeResult:
    """T1/T3 — verify patch size against tier caps."""
    limits = dict(PATCH_LIMITS.get(tier, PATCH_LIMITS["low"]))
    if not enforcement_active:
        return PatchScopeResult(
            ok=True,
            reason="enforcement observe-only (S2 not ready or disabled)",
            risk_tier=tier,
            limits=limits,
        )
    if limits.get("block_autonomous"):
        return PatchScopeResult(
            ok=False,
            reason="critical tier blocks autonomous edit (T3)",
            risk_tier=tier,
            limits=limits,
        )
    max_f = int(limits.get("max_files") or 999)
    max_l = int(limits.get("max_lines") or 9999)
    if files_count > max_f or lines_count > max_l:
        return PatchScopeResult(
            ok=False,
            reason=f"patch exceeds tier caps ({files_count} files, {lines_count} lines)",
            risk_tier=tier,
            limits=limits,
        )
    return PatchScopeResult(ok=True, reason="within tier caps", risk_tier=tier, limits=limits)


def render_predictive_board_section(assessment: RiskAssessment) -> str:
    cal = assessment.calibration
    enforce = "active" if assessment.enforcement_active else "observe-only"
    return (
        f"> [!info] Predictive maintenance (E2 / S2)\n"
        f"> **Risk tier:** `{assessment.risk_tier}` · **Score:** {assessment.maintenance_risk_score}/100\n"
        f"> **Calibration:** {cal.valid_runs_in_window}/{cal.valid_runs_required} valid runs · "
        f"pass rate {cal.integrity_pass_rate:.0%} · enforcement **{enforce}**\n"
        f"> {assessment.explanation}"
    )


def gate_recoverable_handler(
    vault_root: Path,
    handler_name: str,
    *,
    context: dict[str, Any] | None = None,
) -> PatchScopeResult | None:
    """Optional gate before recoverable handlers when enforcement active."""
    low_risk_handlers = {
        "refresh_lane_board",
        "rebuild_board_snapshot",
        "operator_surface_repair",
        "ensure_lane_bundle",
        "reconcile_launch_registry",
        "noop_logged",
    }
    if handler_name in low_risk_handlers:
        return None
    assessment = assess_maintenance_risk(vault_root, context=context)
    if assessment.risk_tier == "critical" and assessment.enforcement_active:
        return PatchScopeResult(
            ok=False,
            reason=f"critical tier blocks handler {handler_name}",
            risk_tier="critical",
            limits=PATCH_LIMITS["critical"],
        )
    return None
