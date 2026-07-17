"""Alpha-queue exit gates not covered by standard review seats."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .factory_little_val import FactoryLittleValResult
from .operator_feedback import DEFAULT_FEEDBACK_REL, KINESTHETIC_CHECKLIST_IDS, load_operator_feedback, validate_kinesthetic_feedback
from .playtest_session_ingest import ingest_playtest_session
from .review_pass_runner import ReviewPassResult


def run_playtest_trace_ingest_gate(vault_root: Path, **_: Any) -> ReviewPassResult:
    """
    Operator-session gate — ingest F6 capture when present; never block overnight on missing session.
    """
    result = ingest_playtest_session(vault_root, write_feedback=True)
    if result.detail in ("no_playtest_session",):
        lv = FactoryLittleValResult(True, [], "playtest_trace_ingest_pending_operator")
        return ReviewPassResult(
            "playtest_trace_ingest",
            True,
            lv,
            "no_playtest_session_operator_pending",
        )
    if not result.ok:
        lv = FactoryLittleValResult(False, [result.detail], "playtest_trace_ingest")
        return ReviewPassResult("playtest_trace_ingest", False, lv, result.detail)

    lv = FactoryLittleValResult(True, [], "playtest_trace_ingest")
    return ReviewPassResult(
        "playtest_trace_ingest",
        True,
        lv,
        f"ingested:{result.rows_updated}_rows",
    )


def run_operator_confirm_all_kinesthetic_gate(
    vault_root: Path,
    *,
    feedback_rel: str = DEFAULT_FEEDBACK_REL,
    **_: Any,
) -> ReviewPassResult:
    """Ship rollup gate — all kinesthetic checklist rows decided and shippable."""
    rows = load_operator_feedback(vault_root, feedback_rel)
    required = tuple(
        r.checklist_id for r in rows if r.kinesthetic and r.checklist_id in KINESTHETIC_CHECKLIST_IDS
    )
    if not required:
        required = tuple(cid for cid in KINESTHETIC_CHECKLIST_IDS)

    violations = validate_kinesthetic_feedback(vault_root, required_ids=required, feedback_rel=feedback_rel)
    ok = len(violations) == 0
    lv = FactoryLittleValResult(ok, violations, "operator_confirm_all_kinesthetic")
    detail = "; ".join(violations) if violations else "operator_confirm_all_kinesthetic_ok"
    return ReviewPassResult("operator_confirm_all_kinesthetic", ok, lv, detail)
