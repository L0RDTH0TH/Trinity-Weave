"""Option B playtest gate policy — when overnight exits vs keeps welding."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...merged_config import load_merged_yaml_blocks
from ..user_story.catalog_io import load_json, user_story_paths

POLICY_TOKENS: frozenset[str] = frozenset(
    {
        "every_beat",
        "target_depth_milestone",
        "first_rung_per_row",
        "once_per_overnight",
        "off",
    }
)

DEFAULT_POLICY = "once_per_overnight"


def resolve_playtest_gate_policy(
    vault_root: Path,
    packet: dict[str, Any] | None = None,
    *,
    project_id: str | None = None,
) -> str:
    hints = (packet or {}).get("planner_hints") if isinstance((packet or {}).get("planner_hints"), dict) else {}
    raw = str(hints.get("playtest_gate_policy") or "").strip().lower()
    if raw in POLICY_TOKENS:
        return raw

    try:
        blocks = load_merged_yaml_blocks(vault_root)
        pf_cfg = blocks.get("product_factory")
        if isinstance(pf_cfg, dict):
            cfg = str(pf_cfg.get("playtest_gate_policy") or "").strip().lower()
            if cfg in POLICY_TOKENS:
                return cfg
    except (ImportError, OSError, TypeError, ValueError):
        pass

    pid = str(project_id or (packet or {}).get("project_id") or "").strip()
    if pid:
        try:
            paths = user_story_paths(vault_root, pid)
            state = load_json(paths["state"])
            pf = state.get("product_factory") if isinstance(state.get("product_factory"), dict) else {}
            cfg = str(pf.get("playtest_gate_policy") or "").strip().lower()
            if cfg in POLICY_TOKENS:
                return cfg
        except (OSError, TypeError, ValueError, KeyError):
            pass

    return DEFAULT_POLICY


def should_block_depth_bump_same_run(
    vault_root: Path,
    project_id: str,
    *,
    session_run_id: str | None = None,
    policy: str | None = None,
    packet: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    """
    Block depth bump in the same overnight run when policy triggers playtest exit.

    Uses product_factory.playtest_exit_session_id to detect same-session park.
    """
    from ..user_story.product_factory_state import load_product_factory

    pid = str(project_id or "").strip()
    if not pid:
        return False, ""

    pol = policy or resolve_playtest_gate_policy(vault_root, packet, project_id=pid)
    if pol == "off":
        return False, "policy_off"

    pf = load_product_factory(vault_root, pid)
    if not pf.get("playtest_exit_eligible"):
        return False, "not_playtest_exit_eligible"

    parked_session = str(pf.get("playtest_exit_session_id") or "")
    if not parked_session:
        return False, "no_park_session"

    if session_run_id and parked_session == session_run_id:
        return True, f"playtest_exit_same_session:{pol}"

    if pol in ("every_beat", "once_per_overnight", "first_rung_per_row", "target_depth_milestone"):
        if parked_session and not session_run_id:
            return True, f"playtest_exit_pending_attestation:{pol}"

    return False, ""


def should_exit_playtest_after_beat(
    vault_root: Path,
    project_id: str,
    *,
    packet: dict[str, Any] | None = None,
    session_run_id: str | None = None,
    row_id: str = "",
    dispatch_depth: int | None = None,
    target_depth: int | None = None,
    beats_this_session: int = 0,
) -> tuple[bool, str]:
    """Return True when machine-ready beat should trigger overnight playtest exit."""
    pol = resolve_playtest_gate_policy(vault_root, packet, project_id=project_id)

    if pol == "off":
        return False, "policy_off"

    if pol == "every_beat":
        return True, "every_beat"

    if pol == "once_per_overnight":
        if beats_this_session >= 1:
            return False, "once_per_overnight_already_used"
        return True, "once_per_overnight"

    if pol == "first_rung_per_row":
        if dispatch_depth is not None and int(dispatch_depth) <= 1:
            return True, "first_rung_per_row"
        return False, "not_first_rung"

    if pol == "target_depth_milestone":
        if dispatch_depth is not None and target_depth is not None:
            if int(dispatch_depth) >= int(target_depth):
                return True, "target_depth_milestone"
        return False, "below_target_depth"

    if beats_this_session >= 1:
        return False, f"{pol}_session_cap"
    return True, pol
