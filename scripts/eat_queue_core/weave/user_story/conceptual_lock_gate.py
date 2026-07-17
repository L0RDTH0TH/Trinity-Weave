"""Loop 2 levels freeze gate (rung 2) — operator catalog + depth charter sign-off."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog_coverage import run_catalog_freeze_gate


def loop2_levels_freeze_allowed(
    vault_root: Path,
    *,
    project_id: str,
) -> dict[str, Any]:
    """Return {ok, violations} before treating Loop 2 levels as signed/frozen."""
    return run_catalog_freeze_gate(vault_root, project_id=project_id)


def conceptual_lock_allowed(
    vault_root: Path,
    *,
    project_id: str,
    require_user_story: bool = True,
) -> dict[str, Any]:
    """
    Back-compat alias — **Loop 2 levels gate only** (rung 2).

    Rung 1 conceptual immutability is ``stamp_factory_conceptual_freeze`` on feed pass,
    not catalog_signed_at.
    """
    if not require_user_story:
        return {"ok": True, "skipped": True, "reason": "user_story_not_required"}
    return loop2_levels_freeze_allowed(vault_root, project_id=project_id)
