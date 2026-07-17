"""Gates-before-slices bootstrap protocol for factory orchestrator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .factory_honesty_rollup import run_stack_baseline_honesty_rollup
from .tech_stack_manifest import load_manifest
from .weave_track import factory_dispatch_allowed


def load_bootstrap_policy(queue: dict[str, Any]) -> dict[str, Any]:
    raw = queue.get("factory_bootstrap")
    if not isinstance(raw, dict):
        return {
            "gates_before_slices": True,
            "bootstrap_waiver": False,
            "require_weave_track_coupled": True,
        }
    return {
        "gates_before_slices": raw.get("gates_before_slices", True) is not False,
        "bootstrap_waiver": raw.get("bootstrap_waiver") is True,
        "require_weave_track_coupled": raw.get("require_weave_track_coupled", True) is not False,
    }


def evaluate_bootstrap_gates(
    vault_root: Path,
    queue: dict[str, Any],
    *,
    run_honesty_checks: bool = True,
) -> tuple[bool, list[str]]:
    """
    Return (allowed, violations).

    When gates_before_slices is true, stack baseline must be vetted unless bootstrap_waiver.
    """
    policy = load_bootstrap_policy(queue)
    violations: list[str] = []

    if policy["require_weave_track_coupled"]:
        allowed, reason = factory_dispatch_allowed(vault_root)
        if not allowed:
            violations.append(f"weave_track:{reason}")

    try:
        manifest = load_manifest(vault_root)
        vetted = bool(manifest.operator_stack_baseline_vetted)
    except (FileNotFoundError, OSError, ValueError):
        vetted = False

    if policy["gates_before_slices"] and not vetted and not policy["bootstrap_waiver"]:
        violations.append("gates_before_slices:stack_baseline_not_vetted")

    if run_honesty_checks and policy["gates_before_slices"] and not policy["bootstrap_waiver"]:
        rollup = run_stack_baseline_honesty_rollup(vault_root)
        if not rollup.get("all_ok"):
            for name, result in rollup.get("passes", {}).items():
                if hasattr(result, "ok") and not result.ok:
                    violations.append(f"stack_honesty_fail:{name}")

    return len(violations) == 0, violations
