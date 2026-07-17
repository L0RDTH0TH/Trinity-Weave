"""Read/write product_factory block in user-story-state.md frontmatter."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .catalog_io import ensure_user_story_state, parse_state_frontmatter, user_story_paths

FACTORY_STAGED = "factory_staged"
FACTORY_CELL_COMPLETE = "factory_cell_complete"
LEGACY_FACTORY_STAGE = "factory_stage"

IMPLEMENTATION_CELL_PHASES = frozenset(
    {
        "idle",
        "awaiting_compose",
        "composed",
        "wave_dispatched",
        "lanes_running",
        "pm_review",
        "rework",
        "wave_complete",
        "cell_complete",
        "escalated",
    }
)

OPERATOR_LOOP_IDS = frozenset(
    {
        "operator_loop_1_pmg",
        "operator_loop_2_catalog_levels",
        "operator_loop_3_slice_selection",
    }
)


def load_product_factory(vault_root: Path, project_id: str) -> dict[str, Any]:
    state = parse_state_frontmatter(user_story_paths(vault_root, project_id)["state"])
    pf = state.get("product_factory")
    return dict(pf) if isinstance(pf, dict) else {}


def merge_state_frontmatter(vault_root: Path, project_id: str, updates: dict[str, Any]) -> bool:
    """Merge top-level frontmatter keys (supports nested product_factory merge)."""
    vault_root = vault_root.resolve()
    state_path = ensure_user_story_state(vault_root, project_id)
    text = state_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 4)
    if end < 0:
        return False
    fm = yaml.safe_load(text[4:end]) or {}
    if not isinstance(fm, dict):
        fm = {}
    for key, val in updates.items():
        if key == "product_factory" and isinstance(val, dict):
            existing = fm.get("product_factory")
            if isinstance(existing, dict):
                merged = {**existing, **val}
            else:
                merged = dict(val)
            fm["product_factory"] = merged
        else:
            fm[key] = val
    body = text[end + 4 :].lstrip("\n")
    new_fm = yaml.dump(fm, sort_keys=False, allow_unicode=True).strip()
    state_path.write_text(f"---\n{new_fm}\n---\n\n{body}", encoding="utf-8")
    return True


def save_product_factory(vault_root: Path, project_id: str, pf: dict[str, Any]) -> bool:
    return merge_state_frontmatter(vault_root, project_id, {"product_factory": pf})


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_completed_phases(phases: list[Any] | None) -> list[str]:
    """Migrate legacy factory_stage token; dedupe factory beat markers."""
    out: list[str] = []
    seen: set[str] = set()
    for raw in phases or []:
        token = str(raw)
        if token == LEGACY_FACTORY_STAGE:
            token = FACTORY_STAGED
        if token in seen:
            continue
        seen.add(token)
        out.append(token)
    return out


def clear_factory_beat_phases(phases: list[str]) -> list[str]:
    drop = {FACTORY_STAGED, FACTORY_CELL_COMPLETE, LEGACY_FACTORY_STAGE}
    return [p for p in phases if p not in drop]


def default_implementation_cell(*, slice_id: str, producer_run_id: str) -> dict[str, Any]:
    return {
        "factory_beat_id": slice_id,
        "phase": "awaiting_compose",
        "producer_run_id": producer_run_id,
        "current_wave": 1,
        "rework_iterations": {},
        "pm_review_status": "idle",
        "sib_path": "",
        "cdp_path": "",
        "last_event_at": _utc_iso(),
    }


def update_implementation_cell(
    vault_root: Path,
    project_id: str,
    updates: dict[str, Any],
) -> dict[str, Any]:
    pf = load_product_factory(vault_root, project_id)
    cell = pf.get("implementation_cell")
    base = dict(cell) if isinstance(cell, dict) else {}
    merged = {**base, **updates, "last_event_at": _utc_iso()}
    save_product_factory(vault_root, project_id, {**pf, "implementation_cell": merged})
    return merged


def try_acquire_pm_review_lock(vault_root: Path, project_id: str) -> bool:
    """Idempotent PM review entry — only one lane runner proceeds."""
    pf = load_product_factory(vault_root, project_id)
    cell = pf.get("implementation_cell")
    if not isinstance(cell, dict):
        return False
    status = str(cell.get("pm_review_status") or "idle")
    if status == "in_progress":
        return False
    if status in ("pass", "escalated"):
        return False
    update_implementation_cell(
        vault_root,
        project_id,
        {"phase": "pm_review", "pm_review_status": "in_progress"},
    )
    return True


def release_pm_review_lock(
    vault_root: Path,
    project_id: str,
    *,
    status: str = "idle",
) -> None:
    """Clear in_progress after failed PM enqueue or cancelled review."""
    update_implementation_cell(
        vault_root,
        project_id,
        {"pm_review_status": status, "pm_review_enqueued": False},
    )


def reopen_product_factory_loop_3(
    vault_root: Path,
    project_id: str,
    *,
    reason: str = "depth_bump_complete",
) -> dict[str, Any]:
    """After vault-feed weld + depth bump — operator must re-confirm loop 3."""
    pf = load_product_factory(vault_root, project_id)
    completed = clear_factory_beat_phases(
        normalize_completed_phases(list(pf.get("completed_phases") or []))
    )
    cell = pf.get("implementation_cell")
    cell_idle = (
        {**cell, "phase": "idle", "pm_review_status": "idle"}
        if isinstance(cell, dict)
        else {"phase": "idle", "pm_review_status": "idle"}
    )
    updated = {
        **pf,
        "active_slice": {"row_ids": [], "dispatch_depth": None},
        "slice_selection_confirmed_at": None,
        "operator_loop": 3,
        "phase": "slice_selection",
        "blocked_at": "operator_loop_3_slice_selection",
        "completed_phases": completed,
        "implementation_cell": cell_idle,
        "last_factory_weld_at": _utc_iso(),
        "last_loop_3_reopen_reason": reason,
    }
    save_product_factory(vault_root, project_id, updated)
    return {"ok": True, "reason": reason, "blocked_at": "operator_loop_3_slice_selection"}


def detect_project_profile(vault_root: Path, project_id: str) -> str:
    """greenfield vs gmm_resume — Execution tree presence selects resume."""
    exec_root = vault_root / f"1-Projects/{project_id}/Roadmap/Execution"
    if exec_root.is_dir() and any(exec_root.rglob("*.md")):
        return "gmm_resume"
    return "greenfield"


def execution_track_exists(vault_root: Path, project_id: str) -> bool:
    exec_root = vault_root / f"1-Projects/{project_id}/Roadmap/Execution"
    return exec_root.is_dir() and any(exec_root.rglob("*.md"))
