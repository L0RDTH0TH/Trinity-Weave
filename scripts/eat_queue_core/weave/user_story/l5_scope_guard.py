"""Block RESUME_ROADMAP deepen from mutating L5 scope files — route to L5_SCOPE_AUTHOR."""

from __future__ import annotations

import re
from typing import Any

_L5_PATH_RE = re.compile(r"/User-Story/scopes/[^/]+/L5\.md", re.IGNORECASE)
_FACTORY_L5_LINKED = re.compile(r"factory[/\\]l5", re.IGNORECASE)
_L5_SCOPE_NAME = re.compile(r"l5[-_]?scope", re.IGNORECASE)

_L5_LINKED_PHASES = frozenset(
    {
        "l5",
        "factory_l5",
        "l5_scope",
        "loop2_l5",
        "l5_manual_gate",
    }
)

_BLOCK_REASON = "l5_scope_author_required"
_LOOP2_BLOCK_REASON = "loop2_exit_eligible"


def _normalize_mode(mode: str) -> str:
    return str(mode or "").strip().upper().replace(" ", "_").replace("-", "_")


def is_l5_scope_target(params: dict[str, Any]) -> bool:
    """True when queue params target User-Story L5 scope authoring."""
    linked = str(params.get("linked_phase") or "").lower().replace("-", "_").replace("/", "_")
    if linked in _L5_LINKED_PHASES or linked.endswith("_l5") or linked.startswith("l5_"):
        return True
    if _FACTORY_L5_LINKED.search(str(params.get("linked_phase") or "")):
        return True

    subphase = str(params.get("current_subphase_index") or params.get("subphase_index") or "")
    if _FACTORY_L5_LINKED.search(subphase):
        return True

    for key in (
        "source_file",
        "target_file",
        "deepen_target",
        "file_path",
        "source_path",
        "note_path",
    ):
        val = str(params.get(key) or "")
        if _L5_PATH_RE.search(val) or _FACTORY_L5_LINKED.search(val):
            return True
        if _L5_SCOPE_NAME.search(val) and "scope" in val.lower():
            return True

    deepen_name = str(params.get("deepen_note_name") or params.get("note_name") or "")
    if _L5_SCOPE_NAME.search(deepen_name):
        return True

    if params.get("author_l5") or params.get("l5_author"):
        return True

    action = str(params.get("action") or "").lower()
    if action in ("l5_scope", "l5_author", "author_l5"):
        return True

    return False


def resume_roadmap_l5_blocked(mode: str, params: dict[str, Any]) -> tuple[bool, str]:
    """RESUME_ROADMAP must not deepen L5 — use L5_SCOPE_AUTHOR or machine draft_l5."""
    if _normalize_mode(mode) != "RESUME_ROADMAP":
        return False, ""
    if is_l5_scope_target(params):
        return True, _BLOCK_REASON
    return False, ""


def resume_roadmap_loop2_blocked(
    mode: str,
    params: dict[str, Any],
    *,
    loop2_exit_eligible: bool,
) -> tuple[bool, str]:
    """When Loop 2 machine exit is eligible, block new RESUME_ROADMAP deepen (not eat_factory_lanes)."""
    if not loop2_exit_eligible:
        return False, ""
    if _normalize_mode(mode) != "RESUME_ROADMAP":
        return False, ""
    action = str(params.get("action") or "").lower()
    if action in ("bootstrap-execution-track", "pass3_repair_drain"):
        return False, ""
    return True, _LOOP2_BLOCK_REASON


def build_l5_scope_author_params(
    *,
    project_id: str,
    row_id: str,
    product_factory_run_id: str | None = None,
    overwrite_placeholder: bool = True,
) -> dict[str, Any]:
    """Params for deterministic L5_SCOPE_AUTHOR queue line."""
    out: dict[str, Any] = {
        "project_id": project_id,
        "row_id": row_id,
        "action": "author_l5",
        "overwrite_placeholder": overwrite_placeholder,
    }
    if product_factory_run_id:
        out["product_factory_run_id"] = product_factory_run_id
    return out
