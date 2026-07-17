"""Factory honesty gate — block Success without little_val_ok + seat passes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .factory_little_val import FactoryLittleValResult, merge_results
from .proof_tiers import is_proxy_pass_as_kinesthetic
from .review_pass_runner import ReviewPassResult


@dataclass
class IntentActualReceipt:
    status_class: str
    divergence_codes: list[str] = field(default_factory=list)
    little_val_ok: bool = False
    anti_pattern_violations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status_class": self.status_class,
            "divergence_codes": list(self.divergence_codes),
            "little_val_ok": self.little_val_ok,
            "anti_pattern_violations": list(self.anti_pattern_violations),
        }


def build_intent_receipt(
    *,
    agent_ok: bool,
    seat_results: dict[str, ReviewPassResult],
    extra_violations: list[str] | None = None,
) -> IntentActualReceipt:
    violations: list[str] = list(extra_violations or [])
    for name, res in seat_results.items():
        if not res.ok:
            violations.append(f"seat_fail:{name}")
        violations.extend(res.little_val.anti_pattern_violations)
    little_val_ok = agent_ok and not violations
    if not agent_ok:
        status = "failure"
    elif violations:
        status = "provisional_success" if agent_ok else "failure"
    else:
        status = "success"
    return IntentActualReceipt(
        status_class=status,
        divergence_codes=violations,
        little_val_ok=little_val_ok,
        anti_pattern_violations=violations,
    )


def enforce_factory_success(
    receipt: IntentActualReceipt,
    *,
    allow_provisional: bool = False,
) -> tuple[bool, str]:
    """Return (may_claim_success, reason)."""
    if receipt.little_val_ok and receipt.status_class == "success":
        return True, "factory_honesty_ok"
    if allow_provisional and receipt.status_class == "provisional_success":
        return True, "provisional_success_allowed"
    if is_proxy_pass_as_kinesthetic(kinesthetic=True, pass_val=True, source="structural_lint"):
        return False, "proxy_pass_as_kinesthetic_forbidden"
    return False, receipt.status_class


def merge_seat_little_val(seat_results: dict[str, ReviewPassResult]) -> FactoryLittleValResult:
    parts = [r.little_val for r in seat_results.values()]
    return merge_results(*parts) if parts else FactoryLittleValResult(False, ["no_seat_results"], "merge")
