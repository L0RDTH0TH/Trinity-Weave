"""Gate Precedence — Tier A–D; Tier D cannot waive human Surface (Tier B) failures."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class GateTier(str, Enum):
    A = "A"  # hard veto — module_fit, structure, integration, interop
    B = "B"  # human-facing — usability_pass (Surface), art_direction, narrative_audio
    C = "C"  # polish — balance, juice, extensibility
    D = "D"  # rollup only — release_readiness_pass


# Normative mapping from implementation factory plan § Gate Precedence
PASS_TIERS: dict[str, GateTier] = {
    "module_fit_pass": GateTier.A,
    "structure_pass": GateTier.A,
    "integration_pass": GateTier.A,
    "interop_pass": GateTier.A,
    "compliance_pass": GateTier.A,
    "reliability_pass": GateTier.A,
    "interpretation_pass": GateTier.A,
    "stack_integrate_pass": GateTier.A,
    "stack_operational_pass": GateTier.A,
    "pipeline_proof_pass": GateTier.A,
    "usability_pass": GateTier.B,
    "surface_pass": GateTier.B,
    "art_direction_pass": GateTier.B,
    "narrative_audio_pass": GateTier.B,
    "perf_pass": GateTier.B,
    "balance_pass": GateTier.C,
    "juice_pass": GateTier.C,
    "extensibility_pass": GateTier.C,
    "release_readiness_pass": GateTier.D,
    "closed_alpha_release_readiness_pass": GateTier.D,
    "playtest_gate": GateTier.B,
}

ANTI_PATTERNS: tuple[tuple[str, str], ...] = (
    ("release_readiness_pass", "tier_d_waives_tier_b"),
    ("interpretation_pass", "conflated_with_usability_pass"),
    ("operator_closed_alpha_vetted", "without_surface_pass"),
    ("harness_green", "substituted_for_playtest_gate"),
    ("slice_complete", "without_human_facing_bundle"),
)


@dataclass(frozen=True)
class PrecedenceVerdict:
    ok: bool
    violations: tuple[str, ...]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "violations": list(self.violations), "detail": self.detail}


def evaluate_precedence(pass_results: dict[str, bool]) -> PrecedenceVerdict:
    """
    pass_results: pass_name -> ok (True = green).

    Rules:
    - Any Tier A FAIL => rollup cannot be ok
    - Any Tier B FAIL on human_facing bundle => rollup cannot be ok
    - Tier D True while Tier B usability/surface False => tier_d_waives_tier_b
    """
    violations: list[str] = []

    tier_a_fail = [n for n, ok in pass_results.items() if not ok and PASS_TIERS.get(n) == GateTier.A]
    tier_b_fail = [n for n, ok in pass_results.items() if not ok and PASS_TIERS.get(n) == GateTier.B]

    if tier_a_fail:
        violations.append(f"tier_a_fail:{tier_a_fail}")

    rollup_names = ("release_readiness_pass", "closed_alpha_release_readiness_pass")
    rollup_ok = any(pass_results.get(n) for n in rollup_names if n in pass_results)
    surface_ok = pass_results.get("surface_pass", pass_results.get("usability_pass", False))

    if rollup_ok and tier_b_fail:
        violations.append(f"tier_d_waives_tier_b:{tier_b_fail}")

    if rollup_ok and not surface_ok and ("surface_pass" in pass_results or "usability_pass" in pass_results):
        violations.append("tier_d_waives_surface_seat")

    # interpretation green but surface red is explicit anti-pattern
    if pass_results.get("interpretation_pass") and not surface_ok:
        violations.append("interpretation_pass_conflated_with_usability_pass")

    ok = len(violations) == 0
    detail = "; ".join(violations) if violations else "gate_precedence_ok"
    return PrecedenceVerdict(ok=ok, violations=tuple(violations), detail=detail)
