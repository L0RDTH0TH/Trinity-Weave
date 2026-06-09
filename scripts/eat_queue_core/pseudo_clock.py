"""Harness pseudo-clock / schedule tick — weave background heartbeat (Phase 17 planes)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schedule_state import (
    institute_bundle_dir,
    legacy_clock_path,
    load_schedule_state,
    save_schedule_state,
)

DEFAULT_KNOBS: dict[str, Any] = {
    "headless_eat": False,
    "headless_lanes": ["institute"],
    "auto_after_sync": False,
    "max_headless_eat_per_day": 3,
    "memory_compact_after_eat_completions": 10,
    "skill_gap_after_repeat_recipe": 3,
    "pq_depth_map_refresh_threshold": 8,
    "auto_pilot_skills": True,
    "watcher_auto_append_hygiene": True,
}

DEFAULT_CLOCK: dict[str, Any] = {
    "version": 1,
    "updated_at": None,
    "counters": {
        "eat_queue_completions": 0,
        "pq_lines_consumed": 0,
        "code_exhibit_notes_created": 0,
        "vault_md_writes": 0,
    },
    "last_actions": [],
    "headless_eat_today": {"date": None, "count": 0},
}


def curator_bundle_dir(vault_root: Path) -> Path:
    """Deprecated — use institute_bundle_dir."""
    return institute_bundle_dir(vault_root)


def knobs_path(vault_root: Path) -> Path:
    return institute_bundle_dir(vault_root) / "curator-knobs.yaml"


def clock_path(vault_root: Path) -> Path:
    return legacy_clock_path(vault_root)


def schedule_state_path(vault_root: Path) -> Path:
    from .schedule_state import schedule_path

    return schedule_path(vault_root)


def pq_path(vault_root: Path) -> Path:
    return institute_bundle_dir(vault_root) / "prompt-queue.jsonl"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    """Minimal YAML for curator-knobs (scalars + inline/list dash lines)."""
    out: dict[str, Any] = {}
    current_list: str | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- ") and current_list:
            out.setdefault(current_list, [])
            if isinstance(out[current_list], list):
                out[current_list].append(line[2:].strip().strip('"').strip("'"))
            continue
        current_list = None
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if not val:
            current_list = key
            out[key] = []
            continue
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            out[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
        elif val.lower() in ("true", "false"):
            out[key] = val.lower() == "true"
        else:
            try:
                out[key] = int(val)
            except ValueError:
                out[key] = val.strip('"').strip("'")
    return out


def load_knobs(vault_root: Path) -> dict[str, Any]:
    knobs = dict(DEFAULT_KNOBS)
    p = knobs_path(vault_root)
    if p.is_file():
        knobs.update(_parse_simple_yaml(p.read_text(encoding="utf-8", errors="replace")))
    return knobs


def load_clock(vault_root: Path) -> dict[str, Any]:
    return load_schedule_state(vault_root)


def save_clock(vault_root: Path, clock: dict[str, Any]) -> None:
    save_schedule_state(vault_root, clock)


def parse_curator_pseudo_clock_enabled(
    vault_root: Path | None = None, config_path: Path | None = None
) -> bool:
    if vault_root is not None:
        try:
            from .merged_config import curator_pseudo_clock_enabled_merged

            return curator_pseudo_clock_enabled_merged(vault_root.resolve())
        except Exception:
            pass
    if not config_path or not config_path.is_file():
        return True
    text = config_path.read_text(encoding="utf-8", errors="replace")
    m = re.search(
        r"curator_pseudo_clock:\s*\n(?:\s+[^\n]+\n)*\s+enabled:\s*(true|false)",
        text,
        re.IGNORECASE,
    )
    if m:
        return m.group(1).lower() == "true"
    return True


def _append_hygiene_line(vault_root: Path, mode: str, params: dict[str, Any]) -> str | None:
    import uuid

    eid = f"harness-hygiene-{uuid.uuid4().hex[:12]}"
    entry = {
        "id": eid,
        "timestamp": _now_iso(),
        "mode": mode,
        "queue_lane": "curator",
        "params": params,
    }
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    pq = pq_path(vault_root)
    existing = pq.read_text(encoding="utf-8", errors="replace") if pq.is_file() else ""
    pq.parent.mkdir(parents=True, exist_ok=True)
    pq.write_text((existing.rstrip("\n") + "\n" if existing.strip() else "") + line, encoding="utf-8")
    return eid


def tick(
    vault_root: Path,
    *,
    config_path: Path | None = None,
    increment_eat: bool = False,
    pq_consumed: int = 0,
) -> dict[str, Any]:
    """Evaluate schedule planes; return action log (alias: schedule_tick)."""
    from .schedule_tick import run_schedule_tick

    return run_schedule_tick(
        vault_root,
        config_path=config_path,
        increment_eat=increment_eat,
        pq_consumed=pq_consumed,
    )


def record_headless_eat(vault_root: Path) -> tuple[bool, str]:
    """Increment daily headless cap counter. Returns (allowed, reason)."""
    knobs = load_knobs(vault_root)
    try:
        from .headless_orchestrator import load_orchestrator_policy

        policy = load_orchestrator_policy(vault_root)
        cap_enabled = policy.get("headless_daily_cap_enabled", knobs.get("headless_daily_cap_enabled", True))
    except Exception:
        cap_enabled = knobs.get("headless_daily_cap_enabled", True)
    if cap_enabled is False:
        clock = load_clock(vault_root)
        today = _today_utc()
        slot = clock.setdefault("headless_eat_today", {"date": None, "count": 0})
        if slot.get("date") != today:
            slot["date"] = today
            slot["count"] = 0
        slot["count"] = int(slot.get("count", 0)) + 1
        save_clock(vault_root, clock)
        return True, "ok_cap_disabled"
    cap = int(knobs.get("max_headless_eat_per_day", 3))
    clock = load_clock(vault_root)
    today = _today_utc()
    slot = clock.setdefault("headless_eat_today", {"date": None, "count": 0})
    if slot.get("date") != today:
        slot["date"] = today
        slot["count"] = 0
    count = int(slot.get("count", 0))
    if count >= cap:
        return False, f"daily_cap:{cap}"
    slot["count"] = count + 1
    save_clock(vault_root, clock)
    return True, "ok"
