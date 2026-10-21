"""Deterministic stall compensation for roadmap lanes (no LLM)."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .handoff_build import bundle_dir_for_lane
from .headless_orchestrator import lane_is_paused, load_orchestrator_policy
from .health_controls import load_health_control_config
from .plan import load_queue_file
from .harness_drain_state import _load_state, drain_state_path


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _pq_depth(bundle: Path) -> int:
    pq = bundle / "prompt-queue.jsonl"
    if not pq.is_file():
        return 0
    return len(load_queue_file(pq))


def _append_hygiene_line(bundle: Path, lane: str, mode: str, params: dict[str, Any]) -> str | None:
    pq = bundle / "prompt-queue.jsonl"
    eid = f"stall-{uuid.uuid4().hex[:12]}"
    entry = {
        "id": eid,
        "timestamp": _now_iso(),
        "mode": mode,
        "queue_lane": lane,
        "params": params,
    }
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    existing = pq.read_text(encoding="utf-8", errors="replace") if pq.is_file() else ""
    pq.parent.mkdir(parents=True, exist_ok=True)
    pq.write_text((existing.rstrip("\n") + "\n" if existing.strip() else "") + line, encoding="utf-8")
    return eid


def stall_compensate(
    vault_root: Path,
    *,
    lanes: list[str] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    policy = load_orchestrator_policy(vault_root)
    watch = [str(x).strip().lower() for x in (lanes or policy.get("stall_watch_lanes") or ["godot", "sandbox"])]
    paused = {str(x).strip().lower() for x in (policy.get("paused_lanes") or [])}
    actions: list[dict[str, Any]] = []

    for lane in watch:
        if lane in paused or lane_is_paused(vault_root, lane):
            actions.append({"lane": lane, "action": "paused_skip", "reason": "paused_lanes"})
            continue
        bundle = bundle_dir_for_lane(vault_root, lane)
        depth = _pq_depth(bundle)
        hc = load_health_control_config(vault_root, lane)
        drain = _load_state(drain_state_path(bundle))
        lane_state = (drain.get("lanes") or {}).get(lane) or {}
        depth_max = getattr(hc, "lane_pq_depth_max", 45) or 45

        if depth >= int(depth_max):
            act = {
                "lane": lane,
                "action": "depth_high",
                "pq_depth": depth,
                "would_append": "RESUME_ROADMAP handoff-audit or hygiene",
            }
            if not dry_run and not lane_is_paused(vault_root, lane):
                # Fail-closed: never invent a product slug from lane name.
                project_id = str(lane_state.get("project_id") or "").strip()
                if not project_id:
                    act["skipped"] = "project_id_missing"
                    actions.append(act)
                    continue
                _append_hygiene_line(
                    bundle,
                    lane,
                    "RESUME_ROADMAP",
                    {"action": "handoff-audit", "project_id": project_id},
                )
                act["appended"] = True
            actions.append(act)

        if depth > 0 and not lane_state.get("last_activated"):
            actions.append({"lane": lane, "action": "stall_watch", "pq_depth": depth})

    return {"ok": True, "dry_run": dry_run, "actions": actions}
