"""Half A → Half B boundary — content gate before IMPLEMENT_SLICE staging."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..user_story.execution_pseudo_code_audit import run_execution_pseudo_code_audit
from ..user_story.execution_track_ready import execution_factory_handoff_ready
from ..user_story.product_factory_loops import check_operator_loop_2, check_operator_loop_3


def implementation_handoff_ready(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """
    Hard gate before factory_staged / first IMPLEMENT_SLICE dispatch.

    Requires execution map content, operator loops 2+3 machine checks, and pseudo-code audit.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return False, "no_project_id"

    exec_ok, exec_reason = execution_factory_handoff_ready(vault_root, pid)
    if not exec_ok:
        return False, f"execution_handoff:{exec_reason}"

    l2 = check_operator_loop_2(vault_root, pid)
    if not l2.ok:
        fail = next((c[0] for c in l2.sub_checks if not c[1]), l2.loop_id)
        return False, f"operator_loop_2:{fail}"

    l3 = check_operator_loop_3(vault_root, pid)
    if not l3.ok:
        fail = next((c[0] for c in l3.sub_checks if not c[1]), l3.loop_id)
        return False, f"operator_loop_3:{fail}"

    audit = run_execution_pseudo_code_audit(vault_root, project_id=pid)
    if not audit.ok:
        detail = audit.violations[0] if audit.violations else "pseudo_code_audit_failed"
        return False, f"pseudo_code_audit:{detail}"

    return True, "implementation_handoff_ready"


def implementation_handoff_detail(vault_root: Path, project_id: str) -> dict[str, Any]:
    """Structured sub-checks for reconcile / wind-down reports."""
    pid = str(project_id or "").strip()
    exec_ok, exec_reason = execution_factory_handoff_ready(vault_root, pid)
    l2 = check_operator_loop_2(vault_root, pid)
    l3 = check_operator_loop_3(vault_root, pid)
    audit = run_execution_pseudo_code_audit(vault_root, project_id=pid)
    ok = exec_ok and l2.ok and l3.ok and audit.ok
    return {
        "ok": ok,
        "execution_handoff": {"ok": exec_ok, "reason": exec_reason},
        "operator_loop_2": {"ok": l2.ok, "loop_id": l2.loop_id},
        "operator_loop_3": {"ok": l3.ok, "loop_id": l3.loop_id},
        "pseudo_code_audit": {
            "ok": audit.ok,
            "violations": list(audit.violations),
        },
    }
