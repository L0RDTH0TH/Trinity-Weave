"""Recover from illegal conceptual deepen_noop consumes while feed gate is red."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from ...goal_authority_io import load_goal_authority
from ...lane_bundle import bundle_dir_for_lane
from .conceptual_dispatch_authority import (
    build_conceptual_dispatch_verdict,
    reconcile_workflow_state_telemetry,
)


def _recent_watcher_lines(vault_root: Path, *, tail: int = 40) -> list[str]:
    path = vault_root / "3-Resources" / "Watcher-Result.md"
    if not path.is_file():
        mirror = vault_root / "3-Resources" / "Watcher-Result-godot.md"
        path = mirror if mirror.is_file() else path
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return [ln for ln in lines if ln.strip().startswith("requestId:")][-tail:]


def _parse_request_id(line: str) -> str:
    m = re.search(r"requestId:\s*([^\s|]+)", line)
    return m.group(1).strip() if m else ""


def _line_is_deepen_noop(line: str) -> bool:
    low = line.lower()
    return "deepen_noop" in low or "reason_code: deepen_noop" in low


def audit_recent_conceptual_noop_consume(
    vault_root: Path,
    lane: str,
    *,
    goal_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    If the latest RESUME_ROADMAP consume was deepen_noop while feed gate is red,
    re-seed conceptual deepen on the lane PQ.
    """
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    packet = goal_packet if isinstance(goal_packet, dict) else load_goal_authority(vault_root, lane)
    if not isinstance(packet, dict) or not packet.get("project_id"):
        return {"ok": True, "action": "skip", "reason": "no_goal_packet"}

    project_id = str(packet.get("project_id") or "").strip()
    verdict = build_conceptual_dispatch_verdict(vault_root, project_id, packet)
    if verdict.ready:
        return {"ok": True, "action": "skip", "reason": "feed_gate_ready"}

    lines = _recent_watcher_lines(vault_root)
    noop_ids: list[str] = []
    for ln in reversed(lines):
        if "resume_roadmap" in ln.lower() or "deepen" in ln.lower():
            if _line_is_deepen_noop(ln):
                rid = _parse_request_id(ln)
                if rid:
                    noop_ids.append(rid)
                break

    if not noop_ids:
        return {"ok": True, "action": "skip", "reason": "no_recent_deepen_noop"}

    telemetry = reconcile_workflow_state_telemetry(vault_root, project_id, packet)

    from ...architect_pq_planner import _reconcile_driven_entries, append_entries

    run_id = str(packet.get("run_id") or "spin-recovery")
    entries = _reconcile_driven_entries(
        vault_root,
        packet,
        run_id=run_id,
        subject_lane=lane,
        skip_dedupe=True,
    )
    appended = append_entries(vault_root, lane, entries) if entries else 0

    guard_path = bundle_dir_for_lane(vault_root, lane) / "conceptual-feed-spin-guard.json"
    guard: dict[str, Any] = {}
    if guard_path.is_file():
        try:
            guard = json.loads(guard_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            guard = {}
    guard.update(
        {
            "last_noop_request_id": noop_ids[0],
            "noop_recovery_count": int(guard.get("noop_recovery_count") or 0) + 1,
            "feed_gate_reason": verdict.reason,
            "reappended": appended,
        }
    )
    try:
        guard_path.write_text(json.dumps(guard, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass

    return {
        "ok": True,
        "action": "reseed" if appended else "reseed_skipped",
        "noop_request_id": noop_ids[0],
        "appended": appended,
        "telemetry": telemetry,
        "feed_gate_reason": verdict.reason,
    }


def factory_telemetry_preflight(
    vault_root: Path,
    lane: str,
    *,
    goal_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Demote legacy workflow_state rollup stamps before Layer 1 reads them."""
    packet = goal_packet if isinstance(goal_packet, dict) else load_goal_authority(vault_root, lane)
    if not isinstance(packet, dict):
        return {"ok": True, "skipped": True, "reason": "no_goal_packet"}
    pid = str(packet.get("project_id") or "").strip()
    if not pid:
        return {"ok": True, "skipped": True, "reason": "no_project_id"}
    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    if not hints.get("product_factory") and hints.get("factory_profile") != "half_a":
        return {"ok": True, "skipped": True, "reason": "not_factory_packet"}
    out = reconcile_workflow_state_telemetry(vault_root, pid, packet)
    return {"ok": True, "lane": lane, "project_id": pid, **out}
