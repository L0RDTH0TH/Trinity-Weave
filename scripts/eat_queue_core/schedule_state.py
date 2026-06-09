"""Schedule tick state — canonical schedule.json with pseudo-clock.json legacy mirror."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_LEGACY_COUNTERS: dict[str, Any] = {
    "eat_queue_completions": 0,
    "pq_lines_consumed": 0,
    "code_exhibit_notes_created": 0,
    "vault_md_writes": 0,
}


def institute_bundle_dir(vault_root: Path) -> Path:
    return vault_root / ".technical" / "parallel" / "institute"


DEFAULT_SCHEDULE: dict[str, Any] = {
    "version": 2,
    "updated_at": None,
    "tick_count": 0,
    "maintain_wrap_streak": 0,
    "last_skill_gap_scan_date": None,
    "last_maintain_wrap_at": None,
    "counters": dict(_LEGACY_COUNTERS),
    "last_actions": [],
    "headless_eat_today": {"date": None, "count": 0},
    "recipe_stagnant_passes": 0,
    "last_actions_by_plane": {
        "listener": [],
        "scheduled": [],
        "reactive": [],
        "graduation": [],
    },
}


def schedule_path(vault_root: Path) -> Path:
    return institute_bundle_dir(vault_root) / "schedule.json"


def legacy_clock_path(vault_root: Path) -> Path:
    return institute_bundle_dir(vault_root) / "pseudo-clock.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _merge_defaults(data: dict[str, Any]) -> dict[str, Any]:
    out = json.loads(json.dumps(DEFAULT_SCHEDULE))
    for key, val in data.items():
        if key == "last_actions_by_plane" and isinstance(val, dict):
            lap = out.setdefault("last_actions_by_plane", {})
            for plane, actions in val.items():
                if isinstance(actions, list):
                    lap[plane] = actions
            continue
        out[key] = val
    if "counters" not in out or not isinstance(out["counters"], dict):
        out["counters"] = dict(DEFAULT_CLOCK["counters"])
    else:
        for k, v in _LEGACY_COUNTERS.items():
            out["counters"].setdefault(k, v)
    return out


def _migrate_legacy_clock(data: dict[str, Any]) -> dict[str, Any]:
    """Upgrade pseudo-clock.json v1 → schedule v2 shape."""
    merged = _merge_defaults(data)
    if merged.get("version", 1) < 2:
        merged["version"] = 2
        merged.setdefault("tick_count", 0)
        merged.setdefault("maintain_wrap_streak", 0)
        legacy_actions = merged.pop("last_actions", None)
        lap = merged.setdefault("last_actions_by_plane", {})
        if isinstance(legacy_actions, list) and legacy_actions and not any(lap.values()):
            lap["listener"] = legacy_actions[-20:]
    return merged


def load_schedule_state(vault_root: Path) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    sp = schedule_path(vault_root)
    lp = legacy_clock_path(vault_root)
    if sp.is_file():
        try:
            data = json.loads(sp.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return _migrate_legacy_clock(data)
        except (OSError, json.JSONDecodeError):
            pass
    if lp.is_file():
        try:
            data = json.loads(lp.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return _migrate_legacy_clock(data)
        except (OSError, json.JSONDecodeError):
            pass
    return json.loads(json.dumps(DEFAULT_SCHEDULE))


def save_schedule_state(vault_root: Path, state: dict[str, Any]) -> None:
    vault_root = vault_root.resolve()
    bundle = institute_bundle_dir(vault_root)
    bundle.mkdir(parents=True, exist_ok=True)
    state = _merge_defaults(state)
    state["updated_at"] = _now_iso()
    sp = schedule_path(vault_root)
    sp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    legacy = {
        k: state[k]
        for k in (
            "version",
            "updated_at",
            "counters",
            "headless_eat_today",
            "recipe_stagnant_passes",
        )
        if k in state
    }
    legacy["version"] = 1
    planes = state.get("last_actions_by_plane") or {}
    flat: list[dict[str, Any]] = []
    for plane in ("listener", "scheduled", "reactive", "graduation"):
        for act in planes.get(plane) or []:
            if isinstance(act, dict):
                row = dict(act)
                row.setdefault("plane", plane)
                flat.append(row)
    legacy["last_actions"] = flat[-40:]
    legacy_clock_path(vault_root).write_text(json.dumps(legacy, indent=2) + "\n", encoding="utf-8")
