"""Advance alpha-factory-queue slice status after lane completion."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .factory_orchestrator import DEFAULT_QUEUE_REL, load_alpha_queue
from .merge_barrier import load_barrier_state, reset_slice_barrier

COMPLETION_TRACKER_REL = ".technical/factory/slice-lane-completion.json"


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _tracker_path(vault_root: Path) -> Path:
    return vault_root / COMPLETION_TRACKER_REL


def load_completion_tracker(vault_root: Path) -> dict[str, Any]:
    path = _tracker_path(vault_root)
    if not path.is_file():
        return {"slices": {}}
    import json

    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {"slices": {}}


def save_completion_tracker(vault_root: Path, data: dict[str, Any]) -> None:
    path = _tracker_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    import json

    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def mark_lane_complete(
    vault_root: Path,
    *,
    slice_id: str,
    lane_id: str,
    receipt_id: str,
) -> dict[str, Any]:
    tracker = load_completion_tracker(vault_root)
    slices = tracker.setdefault("slices", {})
    entry = slices.setdefault(slice_id, {"lanes_done": [], "receipts": {}})
    done = list(entry.get("lanes_done") or [])
    if lane_id not in done:
        done.append(lane_id)
    entry["lanes_done"] = done
    receipts = dict(entry.get("receipts") or {})
    receipts[lane_id] = receipt_id
    entry["receipts"] = receipts
    entry["updated_at"] = _utc_iso()
    save_completion_tracker(vault_root, tracker)
    return entry


def slice_lanes_complete(
    vault_root: Path,
    *,
    slice_id: str,
    required_lanes: list[str],
) -> bool:
    if not required_lanes:
        return False
    tracker = load_completion_tracker(vault_root)
    entry = (tracker.get("slices") or {}).get(slice_id) or {}
    done = set(str(x) for x in (entry.get("lanes_done") or []))
    return set(required_lanes).issubset(done)


def clear_lane_completion(
    vault_root: Path,
    *,
    slice_id: str,
    lane_id: str,
) -> dict[str, Any]:
    """Remove one lane from completion tracker (PM rework path)."""
    tracker = load_completion_tracker(vault_root)
    slices = tracker.setdefault("slices", {})
    entry = slices.setdefault(slice_id, {"lanes_done": [], "receipts": {}})
    done = [str(x) for x in (entry.get("lanes_done") or []) if str(x) != lane_id]
    entry["lanes_done"] = done
    receipts = dict(entry.get("receipts") or {})
    receipts.pop(lane_id, None)
    entry["receipts"] = receipts
    entry["updated_at"] = _utc_iso()
    save_completion_tracker(vault_root, tracker)
    return entry


def advance_alpha_queue_if_ready(
    vault_root: Path,
    *,
    queue_rel: str = DEFAULT_QUEUE_REL,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    queue_path = vault_root / queue_rel
    queue = load_alpha_queue(vault_root, queue_rel)
    slices = queue.get("slices") or []
    if not isinstance(slices, list):
        return {"ok": False, "error": "invalid_queue"}

    active_idx: int | None = None
    for i, sl in enumerate(slices):
        if isinstance(sl, dict) and str(sl.get("status")) == "active":
            active_idx = i
            break
    if active_idx is None:
        return {"ok": True, "advanced": False, "reason": "no_active_slice"}

    active = slices[active_idx]
    slice_id = str(active.get("id") or "")
    lanes = [str(x) for x in (active.get("lanes") or []) if x]
    if not slice_lanes_complete(vault_root, slice_id=slice_id, required_lanes=lanes):
        return {
            "ok": True,
            "advanced": False,
            "reason": "lanes_incomplete",
            "slice_id": slice_id,
            "required_lanes": lanes,
            "done": (load_completion_tracker(vault_root).get("slices") or {}).get(slice_id, {}),
        }

    pid = str(queue.get("project_id") or "")
    if not pid:
        try:
            from .project_identity import resolve_project_id

            pid = resolve_project_id(vault_root, None)
        except Exception:
            pid = ""
    from .weld_beat_ready import (
        PLAYTEST_PENDING_SIGN_OFF,
        playtest_exit_honestly_eligible,
        weld_beat_ready,
    )
    from ..user_story.product_factory_state import load_product_factory

    # Hard park: do not advance slices while awaiting operator playtest sign-off.
    if pid:
        pf = load_product_factory(vault_root, pid)
        if str(pf.get("blocked_at") or "") == PLAYTEST_PENDING_SIGN_OFF:
            return {
                "ok": True,
                "advanced": False,
                "reason": f"playtest_gate:{PLAYTEST_PENDING_SIGN_OFF}",
                "slice_id": slice_id,
            }

    if pid and playtest_exit_honestly_eligible(vault_root, pid):
        beat_ok, beat_reason = weld_beat_ready(vault_root, pid, slice_id=slice_id)
        if not beat_ok:
            return {
                "ok": True,
                "advanced": False,
                "reason": f"playtest_gate:{beat_reason}",
                "slice_id": slice_id,
            }

    slices[active_idx] = {**active, "status": "complete", "completed_at": _utc_iso()}
    next_idx = active_idx + 1
    next_id: str | None = None
    if next_idx < len(slices) and isinstance(slices[next_idx], dict):
        slices[next_idx] = {**slices[next_idx], "status": "active"}
        next_id = str(slices[next_idx].get("id") or "")

    queue["slices"] = slices
    queue["updated_at"] = _utc_iso()
    queue_path.write_text(yaml.safe_dump(queue, sort_keys=False), encoding="utf-8")
    reset_slice_barrier(vault_root, next_id or slice_id)

    return {
        "ok": True,
        "advanced": True,
        "completed_slice": slice_id,
        "next_slice": next_id,
    }


def run_post_slice_advance_hooks(
    vault_root: Path,
    queue_lane: str,
    packet: dict[str, Any],
    advance: dict[str, Any],
    *,
    run_id: str,
    queue_rel: str = DEFAULT_QUEUE_REL,
) -> dict[str, Any]:
    """After slice advance: sync goal-authority and re-stage PQ for the new active slice."""
    from .factory_authority_sync import sync_goal_authority_on_factory_advance
    from .factory_pq_stage import append_factory_wave

    out: dict[str, Any] = {"ok": True}
    if not advance.get("advanced"):
        out["skipped"] = True
        out["reason"] = advance.get("reason") or "no_advance"
        return out

    auth = sync_goal_authority_on_factory_advance(
        vault_root, queue_lane, advance, queue_rel=queue_rel
    )
    out["goal_authority_sync"] = auth

    restage_run_id = f"{run_id}-restage"
    restage = append_factory_wave(
        vault_root,
        queue_lane,
        packet,
        run_id=restage_run_id,
        wave=1,
        dry_run=False,
    )
    out["pq_restage"] = restage
    out["ok"] = bool(auth.get("ok")) and bool(restage.get("ok", restage.get("skipped")))
    return out
