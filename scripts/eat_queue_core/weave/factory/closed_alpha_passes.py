"""Release-tier passes — run only when project config names them.

No baked closed_alpha stage in the harness. Absent release_checks → nothing runs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from .factory_little_val import FactoryLittleValResult
from .review_pass_runner import ReviewPassResult


def _named_checks(vault_root: Path, project_id: str | None) -> list[str]:
    if not str(project_id or "").strip():
        return []
    try:
        from .bindings import resolve_optional

        raw = resolve_optional(
            vault_root, str(project_id), "identity", "release_checks", default=[]
        )
    except Exception:
        return []
    if not isinstance(raw, list):
        return []
    return [str(x).strip() for x in raw if str(x).strip()]


def run_release_readiness_pass(
    vault_root: Path,
    *,
    project_id: str | None = None,
) -> ReviewPassResult:
    """Generic release readiness — no-op success when project lists no checks."""
    checks = _named_checks(vault_root, project_id)
    if not checks:
        lv = FactoryLittleValResult(
            little_val_ok=True,
            anti_pattern_violations=[],
            detail="release_checks_empty",
        )
        return ReviewPassResult("release_readiness_pass", True, lv, "release_checks_empty")

    # Named checks are opaque ids for now — project must supply runners via review registry.
    # Fail closed: declared but unimplemented → violation.
    violations = [f"release_check_unimplemented:{c}" for c in checks]
    ok = False
    lv = FactoryLittleValResult(
        little_val_ok=ok,
        anti_pattern_violations=violations,
        detail="release_readiness_pass",
    )
    return ReviewPassResult(
        "release_readiness_pass",
        ok,
        lv,
        "; ".join(violations),
    )


# Legacy name kept as thin alias so call sites compile until they migrate.
def run_closed_alpha_release_readiness_pass(vault_root: Path) -> ReviewPassResult:
    return run_release_readiness_pass(vault_root, project_id=None)


def run_all_closed_alpha_passes(vault_root: Path) -> dict[str, Any]:
    rollup = run_release_readiness_pass(vault_root, project_id=None)
    results = {"release_readiness_pass": rollup}
    return {"all_ok": rollup.ok, "passes": results, "precedence": {"ok": rollup.ok}}
