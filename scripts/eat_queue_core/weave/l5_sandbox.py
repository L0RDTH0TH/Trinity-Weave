"""Wave 5 H2 — L5 autonomous loop confined to the **sandbox** queue lane only.

Vocabulary: see 3-Resources/Second-Brain/Docs/Lane-Vocabulary.md
- **sandbox lane** = parallel track (bundle `.technical/parallel/sandbox/`).
- **sandbox-genesis-mythos-master** = PARA project (different thing).
- **NOT** Cursor/process \"sandboxed isolation\".
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

from .config import L5Config, load_l5_config
from .governance import append_metric_row, weave_dir
from .l3_self_heal import post_heal_verify
from .verifier import verify_operator_surface_integrity

# Locked: H2 primary experiments on sandbox parallel lane only.
SANDBOX_LANE = "sandbox"
GMM_MIRROR_LANE = SANDBOX_LANE  # deprecated alias (2026-05 rename reverted)
MAINTENANCE_LANE = "maintenance"
L5_SECONDARY_LANE_ALLOWLIST = frozenset({MAINTENANCE_LANE})

L5Status = Literal["idle", "armed", "running", "killed", "downgraded", "expired"]

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        raw = str(ts).strip()
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        return datetime.fromisoformat(raw)
    except (ValueError, TypeError):
        return None


def l5_state_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "l5_sandbox_state.json"


def l5_ledger_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "l5_sandbox_ledger.jsonl"


def _default_state() -> dict[str, Any]:
    return {
        "status": "idle",
        "kill_switch": False,
        "lane": SANDBOX_LANE,
        "timebox_start": None,
        "timebox_end": None,
        "consecutive_verifier_fails": 0,
        "loop_iterations_total": 0,
        "last_tick_at": None,
        "downgrade_reason": None,
        "note": "H2 sandbox — sandbox lane only; not Cursor isolation",
    }


def load_l5_state(vault_root: Path) -> dict[str, Any]:
    p = l5_state_path(vault_root)
    if not p.is_file():
        return _default_state()
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        raw = {}
    if not isinstance(raw, dict):
        raw = {}
    base = _default_state()
    base.update(raw)
    base["lane"] = SANDBOX_LANE
    return base


def save_l5_state(vault_root: Path, state: dict[str, Any]) -> Path:
    weave_dir(vault_root).mkdir(parents=True, exist_ok=True)
    state["lane"] = SANDBOX_LANE
    p = l5_state_path(vault_root)
    p.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return p


def append_l5_ledger(vault_root: Path, row: dict[str, Any]) -> None:
    weave_dir(vault_root).mkdir(parents=True, exist_ok=True)
    p = l5_ledger_path(vault_root)
    line = json.dumps({"timestamp": _now_iso(), **row}, ensure_ascii=False) + "\n"
    prev = p.read_text(encoding="utf-8") if p.is_file() else ""
    p.write_text((prev.rstrip("\n") + "\n" if prev.strip() else "") + line, encoding="utf-8")


def assert_sandbox_lane(lane: str) -> None:
    from ..lane_aliases import resolve_lane

    if resolve_lane(lane) != SANDBOX_LANE:
        raise ValueError(f"l5_sandbox_lane_only: got {lane!r}, required {SANDBOX_LANE!r}")


def assert_gmm_mirror_lane(lane: str) -> None:
    """Deprecated alias for assert_sandbox_lane."""
    assert_sandbox_lane(lane)


def assert_secondary_lane(lane: str) -> None:
    from ..lane_aliases import resolve_lane

    ln = resolve_lane(lane)
    if ln not in L5_SECONDARY_LANE_ALLOWLIST:
        raise ValueError(f"l5_secondary_lane_not_allowed: {lane!r}")


def l3_green_signal(vault_root: Path, *, min_pass_rate: float = 0.8, window: int = 10) -> tuple[bool, str]:
    """Soft readiness — recent board refresh integrity rate."""
    metrics = weave_dir(vault_root) / "metrics.jsonl"
    if not metrics.is_file():
        return False, "no_metrics"
    rows: list[dict[str, Any]] = []
    for line in metrics.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and row.get("metric_type") == "lane_board_refresh":
            rows.append(row)
    tail = rows[-window:]
    if len(tail) < 3:
        return False, f"insufficient_refresh_metrics={len(tail)}"
    ok = sum(1 for r in tail if r.get("integrity_ok") is True)
    rate = ok / len(tail)
    if rate >= min_pass_rate:
        return True, f"integrity_pass_rate={rate:.2f}"
    return False, f"integrity_pass_rate={rate:.2f}<{min_pass_rate}"


def _timebox_expired(state: dict[str, Any]) -> bool:
    end = _parse_iso(state.get("timebox_end"))
    if not end:
        return False
    return datetime.now(timezone.utc) >= end


def arm_l5_sandbox(
    vault_root: Path,
    *,
    days: int | None = None,
    cfg: L5Config | None = None,
    force: bool = False,
) -> dict[str, Any]:
    """AC2 — start sandbox-lane experiment window."""
    cfg = cfg or load_l5_config(vault_root)
    if not cfg.enabled:
        return {"ok": False, "error": "l5_disabled"}

    if cfg.require_l3_green and not force:
        green, reason = l3_green_signal(vault_root, min_pass_rate=cfg.l3_green_min_pass_rate)
        if not green:
            return {"ok": False, "error": "l3_not_green", "detail": reason}

    state = load_l5_state(vault_root)
    if state.get("kill_switch") and not force:
        return {"ok": False, "error": "kill_switch_active", "hint": "l5_release or counselor re-arm"}

    n_days = int(days if days is not None else cfg.ac2_timebox_days)
    start = datetime.now(timezone.utc)
    end = start + timedelta(days=n_days)
    state.update(
        {
            "status": "armed",
            "kill_switch": False,
            "timebox_start": start.isoformat().replace("+00:00", "Z"),
            "timebox_end": end.isoformat().replace("+00:00", "Z"),
            "consecutive_verifier_fails": 0,
            "downgrade_reason": None,
        }
    )
    save_l5_state(vault_root, state)
    append_l5_ledger(vault_root, {"event": "arm", "days": n_days, "timebox_end": state["timebox_end"]})
    append_metric_row(vault_root, {"metric_type": "l5_sandbox_arm", "days": n_days, "lane": SANDBOX_LANE})
    return {"ok": True, "state": state, "lane": SANDBOX_LANE}


def kill_l5_sandbox(vault_root: Path, *, reason: str = "operator_kill") -> dict[str, Any]:
    state = load_l5_state(vault_root)
    state["kill_switch"] = True
    state["status"] = "killed"
    state["downgrade_reason"] = reason
    save_l5_state(vault_root, state)
    append_l5_ledger(vault_root, {"event": "kill", "reason": reason})
    append_metric_row(vault_root, {"metric_type": "l5_sandbox_kill", "reason": reason})
    return {"ok": True, "state": state}


def release_l5_kill(vault_root: Path) -> dict[str, Any]:
    """Clear kill switch; status returns to idle (re-arm required)."""
    state = load_l5_state(vault_root)
    state["kill_switch"] = False
    state["status"] = "idle"
    state["downgrade_reason"] = None
    save_l5_state(vault_root, state)
    append_l5_ledger(vault_root, {"event": "release_kill"})
    return {"ok": True, "state": state}


def _downgrade_l5(vault_root: Path, state: dict[str, Any], reason: str) -> dict[str, Any]:
    state["status"] = "downgraded"
    state["kill_switch"] = True
    state["downgrade_reason"] = reason
    save_l5_state(vault_root, state)
    append_l5_ledger(vault_root, {"event": "downgrade", "reason": reason})
    append_metric_row(
        vault_root,
        {"metric_type": "l5_sandbox_downgrade", "reason": reason, "lane": SANDBOX_LANE},
    )
    return state


def _specialist_audit(vault_root: Path, *, dry_run: bool) -> dict[str, Any]:
    if dry_run:
        return {"ok": True, "specialist": "audit", "dry_run": True}
    from ..lane_status_board import write_lane_status_board

    out = write_lane_status_board(vault_root)
    return {"ok": bool(out.get("ok")), "specialist": "audit", "integrity_ok": out.get("integrity_ok")}


def _specialist_repair(vault_root: Path, lane: str, *, dry_run: bool) -> dict[str, Any]:
    from ..lane_recovery import load_lane_stall, run_recovery_cycle

    stall = load_lane_stall(vault_root, lane)
    if not stall:
        return {"ok": True, "specialist": "repair", "lane": lane, "skipped": True, "reason": "no_stall"}
    if dry_run:
        return {
            "ok": True,
            "specialist": "repair",
            "lane": lane,
            "dry_run": True,
            "handler": stall.get("handler"),
        }
    return {
        "ok": True,
        "specialist": "repair",
        "lane": lane,
        "recovery": run_recovery_cycle(vault_root, lane, architect_decision="proceed"),
    }


def _specialist_eat(vault_root: Path, lane: str, *, dry_run: bool, force: bool) -> dict[str, Any]:
    if dry_run:
        return {"ok": True, "specialist": "eat", "lane": lane, "dry_run": True}
    from ..headless_orchestrator import headless_eat

    try:
        eat = headless_eat(vault_root, lanes=[lane], force=force, dry_run=False)
    except (OSError, RuntimeError) as e:
        return {"ok": False, "specialist": "eat", "lane": lane, "error": str(e)}
    return {"ok": bool(eat.get("ok")), "specialist": "eat", "lane": lane, "headless_eat": eat}


def _run_lane_specialists(
    vault_root: Path,
    lane: str,
    *,
    dry_run: bool,
    force_eat: bool,
    include_eat: bool,
    phase: str,
) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    steps.append(_specialist_repair(vault_root, lane, dry_run=dry_run))
    if include_eat:
        steps.append(_specialist_eat(vault_root, lane, dry_run=dry_run, force=force_eat))
    for s in steps:
        s["phase"] = phase
    return steps


def run_sandbox_tick(
    vault_root: Path,
    *,
    dry_run: bool = False,
    force_eat: bool = False,
    cfg: L5Config | None = None,
) -> dict[str, Any]:
    """One H2 closed-loop iteration — **sandbox lane PQ only**."""
    cfg = cfg or load_l5_config(vault_root)
    state = load_l5_state(vault_root)

    if not cfg.enabled:
        return {"ok": False, "skipped": True, "reason": "l5_disabled"}
    if state.get("kill_switch"):
        return {"ok": False, "skipped": True, "reason": "kill_switch", "status": state.get("status")}
    if state.get("status") not in ("armed", "running"):
        return {"ok": False, "skipped": True, "reason": "not_armed", "status": state.get("status")}
    if _timebox_expired(state):
        state["status"] = "expired"
        state["kill_switch"] = True
        save_l5_state(vault_root, state)
        append_l5_ledger(vault_root, {"event": "timebox_expired"})
        return {"ok": False, "skipped": True, "reason": "timebox_expired"}

    if cfg.require_l3_green:
        green, detail = l3_green_signal(vault_root, min_pass_rate=cfg.l3_green_min_pass_rate)
        if not green:
            return {"ok": False, "skipped": True, "reason": "l3_not_green", "detail": detail}

    state["status"] = "running"
    save_l5_state(vault_root, state)

    from .l5_escalation_gate import user_escalation_pending

    escalation_blocked = False
    escalation_detail: dict[str, Any] = {}
    if cfg.block_on_user_escalation:
        escalation_blocked, escalation_detail = user_escalation_pending(vault_root)

    steps: list[dict[str, Any]] = []
    steps.append(_specialist_audit(vault_root, dry_run=dry_run))

    if escalation_blocked:
        steps.append(
            {
                "specialist": "gate",
                "ok": True,
                "skipped": True,
                "reason": "user_escalation_pending",
                "detail": escalation_detail,
            }
        )
    else:
        steps.extend(
            _run_lane_specialists(
                vault_root,
                SANDBOX_LANE,
                dry_run=dry_run,
                force_eat=force_eat,
                include_eat=True,
                phase="primary",
            )
        )
        if cfg.secondary_lanes_enabled:
            for sec_lane in cfg.secondary_lanes:
                try:
                    assert_secondary_lane(sec_lane)
                except ValueError as e:
                    steps.append(
                        {
                            "specialist": "secondary_skip",
                            "lane": sec_lane,
                            "ok": False,
                            "error": str(e),
                        }
                    )
                    continue
                steps.extend(
                    _run_lane_specialists(
                        vault_root,
                        sec_lane,
                        dry_run=dry_run,
                        force_eat=force_eat,
                        include_eat=cfg.secondary_eat_enabled,
                        phase="secondary",
                    )
                )

    verifier_ok = True
    if not dry_run and cfg.post_tick_verifier:
        v = post_heal_verify(vault_root)
        verifier_ok = v.ok
        steps.append({"specialist": "verify", "ok": v.ok, "code": v.code, "detail": v.detail})

    state = load_l5_state(vault_root)
    if verifier_ok:
        state["consecutive_verifier_fails"] = 0
    else:
        state["consecutive_verifier_fails"] = int(state.get("consecutive_verifier_fails") or 0) + 1
        if (
            cfg.auto_downgrade_on_instability
            and state["consecutive_verifier_fails"] >= cfg.max_consecutive_verifier_fails
        ):
            _downgrade_l5(vault_root, state, "verifier_fail_streak")
            return {
                "ok": False,
                "downgraded": True,
                "reason": "emergency_downgrade_l1_l2",
                "steps": steps,
                "lane": SANDBOX_LANE,
            }

    state["loop_iterations_total"] = int(state.get("loop_iterations_total") or 0) + 1
    state["last_tick_at"] = _now_iso()
    state["status"] = "armed"
    save_l5_state(vault_root, state)

    append_l5_ledger(
        vault_root,
        {"event": "tick", "dry_run": dry_run, "verifier_ok": verifier_ok, "steps": len(steps)},
    )
    append_metric_row(
        vault_root,
        {
            "metric_type": "l5_sandbox_tick",
            "lane": SANDBOX_LANE,
            "verifier_ok": verifier_ok,
            "iteration": state["loop_iterations_total"],
        },
    )
    return {
        "ok": True,
        "lane": SANDBOX_LANE,
        "secondary_lanes": list(cfg.secondary_lanes) if cfg.secondary_lanes_enabled else [],
        "user_escalation_blocked": escalation_blocked,
        "iteration": state["loop_iterations_total"],
        "verifier_ok": verifier_ok,
        "steps": steps,
        "dry_run": dry_run,
    }


def l5_status(vault_root: Path) -> dict[str, Any]:
    from .l5_escalation_gate import user_escalation_pending

    cfg = load_l5_config(vault_root)
    state = load_l5_state(vault_root)
    green, green_detail = l3_green_signal(vault_root, min_pass_rate=cfg.l3_green_min_pass_rate)
    esc_blocked, esc_detail = user_escalation_pending(vault_root)
    return {
        "ok": True,
        "lane": SANDBOX_LANE,
        "config": {
            "enabled": cfg.enabled,
            "ac2_timebox_days": cfg.ac2_timebox_days,
            "require_l3_green": cfg.require_l3_green,
            "secondary_lanes_enabled": cfg.secondary_lanes_enabled,
            "secondary_lanes": list(cfg.secondary_lanes),
            "secondary_eat_enabled": cfg.secondary_eat_enabled,
            "block_on_user_escalation": cfg.block_on_user_escalation,
        },
        "state": state,
        "l3_green": green,
        "l3_green_detail": green_detail,
        "user_escalation_blocked": esc_blocked,
        "user_escalation_detail": esc_detail,
        "timebox_expired": _timebox_expired(state),
    }


def render_l5_board_section(vault_root: Path, *, cfg: L5Config | None = None) -> str:
    cfg = cfg or load_l5_config(vault_root)
    st = load_l5_state(vault_root)
    status = st.get("status", "idle")
    kill = "ON" if st.get("kill_switch") else "off"
    end = st.get("timebox_end") or "—"
    iters = st.get("loop_iterations_total", 0)
    return (
        f"> [!warning] L5 autonomous lab (H2) — **primary:** `{SANDBOX_LANE}`\n"
        f"> **Secondary (opt-in):** `{', '.join(cfg.secondary_lanes) if cfg.secondary_lanes_enabled else 'off'}` "
        f"· repair{'' if cfg.secondary_eat_enabled else ' only (no eat)'}\n"
        f"> **User escalation gate:** {'on' if cfg.block_on_user_escalation else 'off'} — blocks repair/eat, not audit\n"
        f"> **Status:** `{status}` · **Kill:** {kill} · **AC2 ends:** `{end}` · **Ticks:** {iters}\n"
        f"> **godot / institute** never touched · Harness: `l5_arm` · `l5_sandbox_tick` · `l5_kill`"
    )
