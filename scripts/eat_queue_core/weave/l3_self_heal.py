"""Level 3 scoped self-healing — F2 pilot → F3 maintenance → F4 all lanes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import L3Config, load_l3_config
from .governance import append_metric_row
from .verifier import VerifierResult, verify_operator_surface_integrity

# F2 locked pilot set (plan: lock, board regen, registry reconcile, PQ bundle)
F2_HANDLER_ALLOWLIST = frozenset(
    {
        "release_pq_lock",
        "ensure_lane_bundle",
        "refresh_lane_board",
        "rebuild_board_snapshot",
        "operator_surface_repair",
        "reconcile_launch_registry",
    }
)

FULL_HANDLER_ALLOWLIST = frozenset(
    F2_HANDLER_ALLOWLIST
    | {
        "ghost_skill_audit",
        "noop_logged",
    }
)

BOARD_PATH_HANDLERS = frozenset(
    {
        "refresh_lane_board",
        "rebuild_board_snapshot",
        "operator_surface_repair",
        "reconcile_launch_registry",
    }
)

VALID_ROLLOUT = frozenset({"f2", "f3", "f4"})


def normalize_rollout(phase: str) -> str:
    p = str(phase or "f4").strip().lower()
    return p if p in VALID_ROLLOUT else "f4"


def handlers_for_rollout(phase: str) -> frozenset[str]:
    p = normalize_rollout(phase)
    if p == "f2":
        return F2_HANDLER_ALLOWLIST
    return FULL_HANDLER_ALLOWLIST


def lane_auto_heal_permitted(lane: str, cfg: L3Config) -> bool:
    if not cfg.enabled:
        return False
    ln = str(lane or "").strip().lower()
    phase = normalize_rollout(cfg.rollout_phase)
    if phase == "f4":
        return True
    if phase == "f3":
        return ln == "maintenance"
    # f2: maintenance lane only (handlers are maintenance/board scoped)
    return ln == "maintenance"


def handler_permitted(handler_name: str, lane: str, cfg: L3Config) -> bool:
    if not cfg.enabled:
        return False
    name = str(handler_name or "").strip()
    allowed = handlers_for_rollout(cfg.rollout_phase)
    if name not in allowed:
        return False
    phase = normalize_rollout(cfg.rollout_phase)
    if phase == "f2" and name not in BOARD_PATH_HANDLERS and lane.strip().lower() != "maintenance":
        return False
    return True


def new_evidence_for_retry(stall: dict[str, Any], cfg: L3Config) -> bool:
    if not cfg.require_new_evidence:
        return True
    attempt = int(stall.get("l3_heal_attempts") or 0)
    if attempt <= 0:
        return True
    prev_fp = str(stall.get("last_heal_fingerprint") or "")
    cur_fp = _stall_fingerprint(stall)
    return cur_fp != prev_fp


def _stall_fingerprint(stall: dict[str, Any]) -> str:
    receipt = stall.get("receipt") if isinstance(stall.get("receipt"), dict) else {}
    return "|".join(
        [
            str(stall.get("primary_code") or ""),
            str(receipt.get("error") or "")[:200],
            str(stall.get("handler") or ""),
        ]
    )


def post_heal_verify(vault_root: Path) -> VerifierResult:
    board_path = vault_root.resolve() / "Ingest" / "Lane-Status-Board.md"
    result = verify_operator_surface_integrity(board_path)
    try:
        from .trinity_align import check_spine_bridge_status

        check_spine_bridge_status(vault_root)
    except Exception:
        pass
    return result


def record_l3_heal_metric(vault_root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    row = {"metric_type": "l3_self_heal", **payload}
    return append_metric_row(vault_root, row)


def apply_l3_heal_attempt(
    stall: dict[str, Any],
    *,
    handler: str,
    patch: dict[str, Any],
    verifier: VerifierResult | None,
) -> dict[str, Any]:
    attempt = int(stall.get("l3_heal_attempts") or 0) + 1
    stall["l3_heal_attempts"] = attempt
    stall["last_heal_fingerprint"] = _stall_fingerprint(stall)
    stall["last_l3_handler"] = handler
    stall["last_l3_patch"] = patch
    if verifier is not None:
        stall["last_post_heal_verify"] = {"ok": verifier.ok, "code": verifier.code, "detail": verifier.detail}
    return stall


def render_l3_board_section(cfg: L3Config, *, last_metric: dict[str, Any] | None = None) -> str:
    phase = normalize_rollout(cfg.rollout_phase)
    handlers_n = len(handlers_for_rollout(phase))
    enforce = "active" if cfg.enabled else "off"
    verify = "required" if cfg.post_heal_verifier_required else "optional"
    tail = ""
    if last_metric:
        h = last_metric.get("handler") or "—"
        ok = last_metric.get("patch_ok")
        tail = f"\n> Last heal: `{h}` ok={ok} · attempts={last_metric.get('l3_heal_attempts', '—')}"
    return (
        f"> [!info] L3 self-healing (F2→F3→F4)\n"
        f"> **Rollout:** `{phase}` · **Auto-heal:** {enforce} · **Handlers:** {handlers_n} allowlisted\n"
        f"> **Post-heal verifier:** {verify} · **Max L3 attempts/stall:** {cfg.max_heal_attempts_per_stall}"
        f"{tail}"
    )


def latest_l3_metric(vault_root: Path) -> dict[str, Any] | None:
    path = vault_root / ".technical" / "weave" / "metrics.jsonl"
    if not path.is_file():
        return None
    last: dict[str, Any] | None = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and row.get("metric_type") == "l3_self_heal":
            last = row
    return last
