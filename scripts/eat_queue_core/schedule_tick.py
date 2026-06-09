"""Schedule tick orchestrator — four planes (Phase 17); replaces monolithic pseudo_clock logic."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .pseudo_clock import DEFAULT_KNOBS, parse_curator_pseudo_clock_enabled, load_knobs
from .schedule_config import SchedulePlanesConfig, load_schedule_planes_config
from .schedule_planes import (
    run_graduation_plane,
    run_listener_plane,
    run_reactive_plane,
    run_scheduled_plane,
)
from .schedule_state import load_schedule_state, save_schedule_state


def run_schedule_tick(
    vault_root: Path,
    *,
    config_path: Path | None = None,
    increment_eat: bool = False,
    pq_consumed: int = 0,
    planes_cfg: SchedulePlanesConfig | None = None,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    if not parse_curator_pseudo_clock_enabled(vault_root, config_path):
        return {"ok": True, "skipped": True, "reason": "curator_pseudo_clock disabled in config"}

    cfg = planes_cfg or load_schedule_planes_config(vault_root)
    knobs = load_knobs(vault_root)
    state = load_schedule_state(vault_root)

    state["tick_count"] = int(state.get("tick_count") or 0) + 1
    counters = state.setdefault("counters", {})
    if increment_eat:
        counters["eat_queue_completions"] = int(counters.get("eat_queue_completions", 0)) + 1
    if pq_consumed:
        counters["pq_lines_consumed"] = int(counters.get("pq_lines_consumed", 0)) + pq_consumed

    by_plane: dict[str, list[dict[str, Any]]] = {
        "listener": [],
        "scheduled": [],
        "reactive": [],
        "graduation": [],
    }

    if cfg.listener_enabled:
        by_plane["listener"] = run_listener_plane(
            vault_root, config_path=config_path, state=state
        )

    if cfg.scheduled_enabled:
        by_plane["scheduled"] = run_scheduled_plane(
            vault_root,
            config_path=config_path,
            cfg=cfg,
            state=state,
            knobs=knobs,
        )

    if cfg.reactive_enabled:
        by_plane["reactive"] = run_reactive_plane(
            vault_root,
            config_path=config_path,
            cfg=cfg,
            state=state,
            knobs=knobs,
            increment_eat=increment_eat,
            pq_consumed=pq_consumed,
        )

    last_mw = next(
        (a for a in by_plane["scheduled"] if a.get("action") == "maintain_wrap"),
        None,
    )
    by_plane["graduation"] = run_graduation_plane(
        vault_root, cfg=cfg, state=state, last_maintain_wrap=last_mw
    )

    for plane, actions in by_plane.items():
        prior = (state.get("last_actions_by_plane") or {}).get(plane) or []
        if not isinstance(prior, list):
            prior = []
        state.setdefault("last_actions_by_plane", {})[plane] = (prior + actions)[-25:]

    save_schedule_state(vault_root, state)

    flat_actions: list[dict[str, Any]] = []
    for plane in ("listener", "scheduled", "reactive", "graduation"):
        flat_actions.extend(by_plane.get(plane) or [])

    return {
        "ok": True,
        "surface": "schedule_tick",
        "tick_count": state.get("tick_count"),
        "maintain_wrap_streak": state.get("maintain_wrap_streak"),
        "knobs": {k: knobs[k] for k in DEFAULT_KNOBS if k in knobs},
        "schedule_planes": {
            "listener_enabled": cfg.listener_enabled,
            "scheduled_enabled": cfg.scheduled_enabled,
            "reactive_enabled": cfg.reactive_enabled,
            "graduation_enabled": cfg.graduation_enabled,
            "maintain_wrap_every_n_ticks": cfg.maintain_wrap_every_n_ticks,
        },
        "counters": counters,
        "actions_by_plane": by_plane,
        "actions": flat_actions,
    }
