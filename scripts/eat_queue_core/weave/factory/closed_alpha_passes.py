"""Release-tier passes — only ids listed in identity.release_checks.

Closed-alpha release readiness alias is deleted. No alias. No auto-green.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .bindings import BindingMissingError, require_project_id, resolve
from .factory_little_val import FactoryLittleValResult
from .review_pass_runner import ReviewPassResult


def _release_checks(vault_root: Path, project_id: str) -> list[str]:
    """Raise on missing identity; return list (may be empty)."""
    pid = require_project_id(project_id)
    raw = resolve(vault_root, pid, "identity", "release_checks")
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise BindingMissingError(
            "binding_missing", "identity:release_checks_not_list"
        )
    return [str(x).strip() for x in raw if str(x).strip()]


def run_release_readiness_pass(
    vault_root: Path,
    *,
    project_id: str,
) -> ReviewPassResult:
    """Run only when caller supplies project_id. Empty checks → not applicable (ok skip)."""
    checks = _release_checks(vault_root, project_id)
    if not checks:
        lv = FactoryLittleValResult(
            little_val_ok=True,
            anti_pattern_violations=[],
            detail="release_checks_empty_not_applicable",
        )
        return ReviewPassResult(
            "release_readiness_pass",
            True,
            lv,
            "release_checks_empty_not_applicable",
        )
    # Declared ids must be implemented elsewhere — unimplemented → fail closed.
    violations = [f"release_check_unimplemented:{c}" for c in checks]
    lv = FactoryLittleValResult(
        little_val_ok=False,
        anti_pattern_violations=violations,
        detail="release_readiness_pass",
    )
    return ReviewPassResult(
        "release_readiness_pass",
        False,
        lv,
        "; ".join(violations),
    )


def run_configured_release_passes(
    vault_root: Path,
    *,
    project_id: str,
    pass_runners: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Rollup only identity.release_checks ids. Missing identity raises."""
    checks = _release_checks(vault_root, project_id)
    results: dict[str, Any] = {}
    runners = pass_runners or {}
    for cid in checks:
        runner = runners.get(cid)
        if runner is None:
            lv = FactoryLittleValResult(
                little_val_ok=False,
                anti_pattern_violations=[f"release_check_unimplemented:{cid}"],
                detail=cid,
            )
            results[cid] = ReviewPassResult(cid, False, lv, f"unimplemented:{cid}")
            continue
        results[cid] = runner(vault_root, project_id=project_id)
    all_ok = all(getattr(r, "ok", False) for r in results.values()) if results else True
    return {"all_ok": all_ok, "passes": results, "check_ids": checks}
