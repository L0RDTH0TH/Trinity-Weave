"""Lightweight weave Phase 0 scaffold.

Phase 0 intentionally keeps this package small and deterministic:
- plain dataclasses + stdlib/json
- no heavy schema/rule engine
- explicit file contracts under .technical/weave/
"""

from .config import WeaveConfig, load_weave_config
from .governance import (
    ensure_weave_paths,
    governance_record_path,
    lane_board_snapshot_path,
    metrics_path,
    write_governance_review_record,
)
from .invariant_registry import (
    activate_invariant,
    bootstrap_n2_invariants,
    list_invariants,
    load_invariant,
)
from .predictive import (
    assess_maintenance_risk,
    calibrate_predictive_tiers,
    check_patch_scope,
    render_predictive_board_section,
)
from .symbolic_conflict import (
    ConflictDecision,
    evaluate_symbolic_conflict,
    evaluate_symbolic_conflict_stub,
    gate_symbolic_action,
    render_symbolic_board_section,
)
from .verifier import VerifierResult, verify_operator_surface_integrity

__all__ = [
    "activate_invariant",
    "assess_maintenance_risk",
    "bootstrap_n2_invariants",
    "calibrate_predictive_tiers",
    "check_patch_scope",
    "ConflictDecision",
    "WeaveConfig",
    "ensure_weave_paths",
    "evaluate_symbolic_conflict",
    "evaluate_symbolic_conflict_stub",
    "gate_symbolic_action",
    "governance_record_path",
    "lane_board_snapshot_path",
    "list_invariants",
    "load_invariant",
    "load_weave_config",
    "metrics_path",
    "write_governance_review_record",
    "render_predictive_board_section",
    "render_symbolic_board_section",
    "VerifierResult",
    "verify_operator_surface_integrity",
]
