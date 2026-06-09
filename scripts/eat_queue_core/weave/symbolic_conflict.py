"""L2 symbolic conflict gate — K3 registry checks + tier-aware decisions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from .config import load_symbolic_config
from .governance import append_metric_row
from .invariant_registry import InvariantEntry, list_invariants

Decision = Literal["proceed", "block", "needs_human_resolution"]


@dataclass(frozen=True)
class ConflictDecision:
    decision: Decision
    violated_invariants: list[str]
    temporal_inconsistencies: list[str]
    ownership_clashes: list[str]
    cross_surface_drift_risks: list[str]
    stub_mode: bool = False
    enforcement_active: bool = False
    blocked: bool = False
    risk_tier: str = "low"

    # blast-radius: medium


def _check_invariant(entry: InvariantEntry, context: dict[str, Any]) -> str | None:
    """Return violation message or None."""
    check = entry.check
    flags = set(context.get("forbidden_flags") or [])
    if check == "forbidden_context_flag":
        flag = str(entry.meta.get("flag") or "")
        if flag and flag in flags:
            return entry.message or f"forbidden flag: {flag}"
    if check == "required_pre_read":
        step = str(entry.meta.get("step") or "")
        done = set(context.get("pre_read_steps") or [])
        if step and step not in done:
            return entry.message or f"missing pre_read: {step}"
    if check == "required_resolver":
        resolver = str(entry.meta.get("resolver") or "")
        used = str(context.get("resolver_used") or "")
        if resolver and used and used != resolver:
            return entry.message or f"wrong resolver: {used} != {resolver}"
    if check == "required_kernel":
        kernel = str(entry.meta.get("kernel") or "")
        used = str(context.get("kernel_used") or "")
        if kernel and used and used != kernel:
            return entry.message or f"wrong kernel: {used}"
    if check == "required_test_touch":
        if context.get("weave_code_change") and not context.get("tests_touched"):
            return entry.message or "tests not updated for weave change"
    if check == "integrity_required":
        if context.get("integrity_ok") is False:
            return entry.message or "operator surface integrity failed"
    return None


def evaluate_symbolic_conflict(
    vault_root: Path,
    *,
    context: dict[str, Any] | None = None,
    risk_tier: str = "low",
    invariant_ids: frozenset[str] | None = None,
) -> ConflictDecision:
    """L2 — evaluate active invariants and apply tier-aware gate policy.

    When ``invariant_ids`` is set, only those registry ids are checked (entry-point scoping).
    An empty frozenset() skips all invariant checks (proceed).
    """
    vault_root = vault_root.resolve()
    cfg = load_symbolic_config(vault_root)
    ctx = dict(context or {})

    if not cfg.enabled:
        return ConflictDecision(
            decision="proceed",
            violated_invariants=[],
            temporal_inconsistencies=[],
            ownership_clashes=[],
            cross_surface_drift_risks=[],
            stub_mode=True,
            enforcement_active=False,
        )

    violated: list[str] = []
    temporal: list[str] = []
    ownership: list[str] = []
    drift: list[str] = []

    for ent in list_invariants(vault_root, status="active"):
        if invariant_ids is not None and ent.id not in invariant_ids:
            continue
        msg = _check_invariant(ent, ctx)
        if not msg:
            continue
        line = f"{ent.id}: {msg}"
        if ent.check in ("required_pre_read", "integrity_required"):
            temporal.append(line)
        elif ent.check in ("required_resolver", "required_kernel"):
            drift.append(line)
        elif ent.risk in ("medium", "high"):
            ownership.append(line)
        else:
            violated.append(line)

    # Raw decision from invariant severity
    if temporal or (violated and risk_tier in ("high", "critical")):
        raw: Decision = "block"
    elif ownership or violated:
        raw = "needs_human_resolution"
    else:
        raw = "proceed"

    # L2 tier-aware policy (locked plan)
    final = raw
    tier = str(risk_tier or "low").lower()
    if tier in ("high", "critical") and raw != "proceed":
        final = "block"
    elif tier == "medium" and raw == "block":
        final = "needs_human_resolution"
    elif raw == "block" and tier == "low":
        final = "needs_human_resolution"

    enforcement_active = cfg.enforcement_enabled and not cfg.observe_only
    blocked = enforcement_active and final == "block"

    decision = ConflictDecision(
        decision=final,
        violated_invariants=violated,
        temporal_inconsistencies=temporal,
        ownership_clashes=ownership,
        cross_surface_drift_risks=drift,
        stub_mode=False,
        enforcement_active=enforcement_active,
        blocked=blocked,
        risk_tier=tier,
    )

    append_metric_row(
        vault_root,
        {
            "metric_type": "symbolic_conflict",
            "decision": decision.decision,
            "risk_tier": tier,
            "enforcement_active": enforcement_active,
            "blocked": blocked,
            "violation_count": len(violated) + len(temporal) + len(ownership) + len(drift),
        },
    )
    return decision


def evaluate_symbolic_conflict_stub(context: dict[str, Any] | None = None) -> ConflictDecision:
    """Backward-compatible stub when symbolic layer disabled."""
    return ConflictDecision(
        decision="proceed",
        violated_invariants=[],
        temporal_inconsistencies=[],
        ownership_clashes=[],
        cross_surface_drift_risks=[],
        stub_mode=True,
    )


def gate_symbolic_action(
    vault_root: Path,
    *,
    context: dict[str, Any] | None = None,
    risk_tier: str = "low",
) -> ConflictDecision:
    """Single entry for maintenance/recoverable paths."""
    return evaluate_symbolic_conflict(vault_root, context=context, risk_tier=risk_tier)


def render_symbolic_board_section(decision: ConflictDecision, *, active_count: int) -> str:
    mode = "active" if decision.enforcement_active else "observe-only"
    if decision.stub_mode:
        mode = "disabled"
    viol = (
        len(decision.violated_invariants)
        + len(decision.temporal_inconsistencies)
        + len(decision.ownership_clashes)
        + len(decision.cross_surface_drift_risks)
    )
    return (
        f"> [!info] Neuro-symbolic gate (K3 / L2 / N2)\n"
        f"> **Decision:** `{decision.decision}` · **Enforcement:** {mode} · "
        f"**Active invariants:** {active_count}\n"
        f"> **Violations:** {viol} (tier `{decision.risk_tier}`) · "
        f"**Blocked:** {'yes' if decision.blocked else 'no'}\n"
        f"> Low-risk invariants auto-active (M2); medium+ need counselor (Q3)."
    )
