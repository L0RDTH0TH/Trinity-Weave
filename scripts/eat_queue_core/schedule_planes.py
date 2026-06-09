"""Schedule planes — listener, scheduled, reactive (Phase 17)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .plan import load_queue_file
from .pq_lock import merge_pending_into_pq
from .pseudo_clock import (
    _append_hygiene_line,
    _now_iso,
    _today_utc,
    load_knobs,
    pq_path,
)
from .schedule_config import SchedulePlanesConfig


def _run_harness(
    vault_root: Path,
    command: str,
    *,
    config_path: Path | None = None,
    extra_args: list[str] | None = None,
    timeout: int = 7200,
) -> dict[str, Any]:
    script = [
        sys.executable,
        "-m",
        "scripts.eat_queue_core.harness",
        command,
        "--vault-root",
        str(vault_root),
    ]
    if config_path:
        script.extend(["--config", str(config_path)])
    if extra_args:
        script.extend(extra_args)
    env = {**dict(os.environ), "PYTHONPATH": str(vault_root / "scripts")}
    r = subprocess.run(
        script,
        cwd=vault_root,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    parsed: dict[str, Any] | None = None
    if r.stdout and r.stdout.strip():
        try:
            parsed = json.loads(r.stdout)
        except json.JSONDecodeError:
            parsed = None
    return {
        "command": command,
        "exit_code": r.returncode,
        "parsed": parsed,
        "stdout_tail": (r.stdout or "")[-800:],
        "stderr_tail": (r.stderr or "")[-400:],
    }


def run_maintain_wrap(
    vault_root: Path,
    *,
    config_path: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    if dry_run:
        return {
            "action": "maintain_wrap",
            "dry_run": True,
            "would_run": ["trinity_type2_verify", "trinity_core_charter_audit"],
        }
    type2 = _run_harness(vault_root, "trinity_type2_verify", config_path=config_path)
    charter = _run_harness(
        vault_root, "trinity_core_charter_audit", config_path=config_path
    )
    t2 = type2.get("parsed") if isinstance(type2.get("parsed"), dict) else {}
    ch = charter.get("parsed") if isinstance(charter.get("parsed"), dict) else {}
    type2_ok = bool(t2.get("pass_gate_ok")) and type2.get("exit_code", 1) == 0
    charter_ok = bool(ch.get("charter_aligned")) and charter.get("exit_code", 1) == 0
    return {
        "action": "maintain_wrap",
        "ok": type2_ok and charter_ok,
        "type2_ok": type2_ok,
        "charter_ok": charter_ok,
        "type2": type2,
        "charter": charter,
    }


def run_listener_plane(
    vault_root: Path,
    *,
    config_path: Path | None = None,
    state: dict[str, Any],
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    bundle = vault_root / ".technical" / "parallel" / "institute"

    merged = merge_pending_into_pq(bundle, pq_path(vault_root))
    if merged:
        actions.append({"action": "merge_pending_pq", "lines": merged, "plane": "listener"})

    try:
        from .queue_neighbor_prep import write_queue_neighbor_prep

        qnp = write_queue_neighbor_prep(vault_root, dry_run=False)
        actions.append(
            {
                "action": "queue_neighbor_prep",
                "entries": qnp.get("entries_prepared"),
                "plane": "listener",
            }
        )
    except Exception as exc:
        actions.append(
            {"action": "queue_neighbor_prep", "error": str(exc)[:200], "plane": "listener"}
        )

    try:
        from .nav_color_refresh import write_nav_color_index

        ncr = write_nav_color_index(vault_root, dry_run=False, use_pq_defaults=True)
        actions.append(
            {"action": "nav_color_refresh", "rows": ncr.get("rows_written"), "plane": "listener"}
        )
    except OSError:
        pass

    try:
        from .operator_inbox import sweep_reviewed_operator_inbox

        sweep_reviewed_operator_inbox(vault_root)
        actions.append({"action": "inbox_sweep", "plane": "listener"})
    except OSError:
        pass

    try:
        from .continuity_bridge import append_timing_log, seed_memory_from_clock, write_continuity_tail

        write_continuity_tail(
            vault_root,
            last_run_id=f"schedule_tick_{state.get('updated_at', '')}",
            next_action="monitor_receipts",
        )
        seed_memory_from_clock(vault_root)
        append_timing_log(
            vault_root,
            f"- **{_now_iso()}** — schedule_tick listener plane actions={len(actions)}",
        )
        actions.append({"action": "continuity_rollup", "plane": "listener"})
    except OSError:
        pass

    try:
        from .warning_ledger import rollup_warnings_to_maintenance

        rollup = rollup_warnings_to_maintenance(vault_root)
        if rollup.get("appended"):
            actions.append(
                {
                    "action": "warning_ledger_rollup",
                    "appended": len(rollup.get("appended") or []),
                    "plane": "listener",
                }
            )
    except Exception:
        pass

    try:
        from .lane_status_board import write_lane_status_board

        lb = write_lane_status_board(vault_root)
        actions.append(
            {
                "action": "lane_status_board",
                "system_attention": lb.get("system_attention"),
                "plane": "listener",
            }
        )
    except OSError:
        pass

    return actions


def run_scheduled_plane(
    vault_root: Path,
    *,
    config_path: Path | None = None,
    cfg: SchedulePlanesConfig,
    state: dict[str, Any],
    knobs: dict[str, Any],
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    counters = state.setdefault("counters", {})
    eat_n = int(counters.get("eat_queue_completions", 0))
    tick_n = int(state.get("tick_count") or 0)

    compact_thresh = cfg.memory_compact_every_n_eats
    if compact_thresh > 0 and eat_n >= compact_thresh and eat_n % compact_thresh == 0:
        r = _run_harness(
            vault_root,
            "memory_compact",
            config_path=config_path,
            extra_args=["--lane", "institute"],
            timeout=120,
        )
        actions.append(
            {
                "action": "memory_compact",
                "exit_code": r.get("exit_code"),
                "plane": "scheduled",
            }
        )

    wrap_n = cfg.maintain_wrap_every_n_ticks
    if wrap_n > 0 and tick_n > 0 and tick_n % wrap_n == 0:
        mw = run_maintain_wrap(vault_root, config_path=config_path)
        mw["plane"] = "scheduled"
        actions.append(mw)
        state["last_maintain_wrap_at"] = _now_iso()
        if mw.get("ok"):
            state["maintain_wrap_streak"] = int(state.get("maintain_wrap_streak") or 0) + 1
        else:
            state["maintain_wrap_streak"] = 0

    try:
        from .weave.config import load_trinity_config
        from .weave.trinity_catchup_sweep import maybe_catchup_on_pseudo_clock

        tcfg = load_trinity_config(vault_root)
        if tcfg.enabled and tcfg.catchup_on_pseudo_clock:
            cu = maybe_catchup_on_pseudo_clock(vault_root)
            if cu is not None:
                actions.append(
                    {
                        "action": "trinity_catchup_sweep",
                        "ok": cu.get("ok"),
                        "plane": "scheduled",
                    }
                )
    except Exception:
        pass

    try:
        from .weave.config import load_trinity_config
        from .weave.trinity_card_backlog import maybe_backlog_on_pseudo_clock

        tcfg = load_trinity_config(vault_root)
        if tcfg.enabled and tcfg.backlog_on_pseudo_clock:
            bl = maybe_backlog_on_pseudo_clock(vault_root)
            if bl is not None:
                actions.append(
                    {
                        "action": "assess_trinity_card_backlog",
                        "ok": bl.get("ok"),
                        "plane": "scheduled",
                    }
                )
    except Exception:
        pass

    try:
        from .weave.config import load_trinity_config
        from .weave.trinity_touch_refresh import maybe_refresh_on_pseudo_clock

        tcfg = load_trinity_config(vault_root)
        if tcfg.enabled and tcfg.touch_refresh_on_pseudo_clock:
            tr = maybe_refresh_on_pseudo_clock(vault_root)
            if tr is not None:
                actions.append(
                    {
                        "action": "trinity_touch_refresh",
                        "ok": tr.get("ok"),
                        "plane": "scheduled",
                    }
                )
    except Exception:
        pass

    return actions


def run_reactive_plane(
    vault_root: Path,
    *,
    config_path: Path | None = None,
    cfg: SchedulePlanesConfig,
    state: dict[str, Any],
    knobs: dict[str, Any],
    increment_eat: bool = False,
    pq_consumed: int = 0,
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    repeat_thresh = int(knobs.get("skill_gap_after_repeat_recipe", 3))
    stagnant = int(state.get("recipe_stagnant_passes") or 0)
    if increment_eat and pq_consumed == 0:
        stagnant += 1
    elif pq_consumed > 0:
        stagnant = 0
    state["recipe_stagnant_passes"] = stagnant
    if stagnant >= repeat_thresh:
        try:
            from .continuity_bridge import append_memory_gap

            if append_memory_gap(
                vault_root,
                "institute",
                "repeat_recipe",
                f"stagnant_passes={stagnant} pq_consumed=0",
            ):
                actions.append({"action": "memory_gap", "key": "repeat_recipe", "plane": "reactive"})
            state["recipe_stagnant_passes"] = 0
        except OSError:
            pass

    pq_entries = load_queue_file(pq_path(vault_root)) if pq_path(vault_root).is_file() else []
    depth_thresh = int(knobs.get("pq_depth_map_refresh_threshold", 8))
    if len(pq_entries) >= depth_thresh:
        has_map = any((e.mode or "").upper() == "MAP_REFRESH" for e in pq_entries)
        if not has_map:
            eid = _append_hygiene_line(
                vault_root,
                "MAP_REFRESH",
                {"queue_lane": "institute", "reason": "schedule_pq_depth"},
            )
            actions.append({"action": "append_map_refresh", "id": eid, "plane": "reactive"})

    try:
        from .headless_orchestrator import load_orchestrator_policy

        policy = load_orchestrator_policy(vault_root)
        if policy.get("orchestrator_enabled") and policy.get("stall_compensate_on_tick") is True:
            from .stall_compensator import stall_compensate

            sc = stall_compensate(vault_root, dry_run=False)
            actions.append({"action": "stall_compensate", "result": sc, "plane": "reactive"})
    except Exception:
        pass

    today = _today_utc()
    last_sg = state.get("last_skill_gap_scan_date")
    allow_sg = last_sg != today or cfg.skill_gap_scan_max_per_day > 1
    try:
        from .weave.config import skill_proposals_enabled

        if allow_sg and skill_proposals_enabled(vault_root) and knobs.get("auto_pilot_skills", True):
            from .skill_gap import scan_and_stub

            sg = scan_and_stub(vault_root)
            state["last_skill_gap_scan_date"] = today
            if sg.get("proposals_created"):
                actions.append(
                    {
                        "action": "skill_gap_scan",
                        "created": sg["proposals_created"],
                        "plane": "reactive",
                    }
                )
    except ImportError:
        pass

    try:
        from .weave.config import load_trinity_config
        from .weave.trinity_weave_self_wrap import maybe_weave_self_wrap_on_pseudo_clock

        tcfg = load_trinity_config(vault_root)
        if tcfg.enabled and tcfg.weave_self_wrap_on_pseudo_clock:
            ws = maybe_weave_self_wrap_on_pseudo_clock(vault_root)
            if ws is not None:
                actions.append(
                    {
                        "action": "trinity_weave_self_wrap",
                        "ok": ws.get("ok"),
                        "skipped": ws.get("skipped"),
                        "plane": "reactive",
                    }
                )
    except Exception:
        pass

    try:
        from .weave.config import load_trinity_config
        from .weave.trinity_usage_proven import maybe_usage_proven_on_pseudo_clock

        tcfg = load_trinity_config(vault_root)
        if tcfg.enabled and tcfg.usage_proven_on_pseudo_clock:
            up = maybe_usage_proven_on_pseudo_clock(vault_root)
            if up is not None:
                actions.append(
                    {
                        "action": "trinity_usage_proven",
                        "ok": up.get("ok"),
                        "stamped": up.get("stamped"),
                        "plane": "reactive",
                    }
                )
    except Exception:
        pass

    return actions


def run_graduation_plane(
    vault_root: Path,
    *,
    cfg: SchedulePlanesConfig,
    state: dict[str, Any],
    last_maintain_wrap: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if not cfg.graduation_enabled:
        return [
            {
                "action": "graduation_evaluator",
                "skipped": True,
                "reason": "graduation_enabled false",
                "plane": "graduation",
            }
        ]
    from .weave.trinity_graduation_evaluator import run_graduation_evaluator

    out = run_graduation_evaluator(
        vault_root,
        cfg,
        maintain_wrap_streak=int(state.get("maintain_wrap_streak") or 0),
        maintain_wrap_result=last_maintain_wrap,
    )
    out["plane"] = "graduation"
    return [out]
