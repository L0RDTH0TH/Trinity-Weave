"""Pass/fail playtest lifecycle — feedback on live goal packet + rework signal."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ...goal_authority_io import goal_authority_path_for_lane
from ..user_story.playtest_manual_gate import playtest_feedback_pending
from .factory_pq_stage import append_factory_rework
from .factory_orchestrator import run_factory_orchestrator
from .weld_beat_ready import clear_playtest_exit_after_attestation


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_operator_playtest_feedback(
    vault_root: Path,
    queue_lane: str,
    *,
    passed: bool | None,
    notes: str = "",
    slice_id: str = "",
    run_id: str = "",
) -> dict[str, Any]:
    """Append operator_playtest_feedback row to goal-authority.json (packet stays live)."""
    vault_root = vault_root.resolve()
    lane = queue_lane.strip().lower()
    path = goal_authority_path_for_lane(vault_root, lane)
    if not path.is_file():
        return {"ok": False, "error": "goal_authority_missing"}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return {"ok": False, "error": f"read_failed:{e}"}

    if not isinstance(data, dict):
        return {"ok": False, "error": "invalid_packet"}

    rows = data.get("operator_playtest_feedback")
    if not isinstance(rows, list):
        rows = []
    rows.append(
        {
            "recorded_at": _utc_iso(),
            "pass": passed,
            "notes": notes.strip(),
            "slice_id": slice_id,
            "run_id": run_id or str(data.get("run_id") or ""),
        }
    )
    data["operator_playtest_feedback"] = rows[-20:]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "path": str(path), "feedback_count": len(data["operator_playtest_feedback"])}


def record_playtest_pass(
    vault_root: Path,
    project_id: str,
    queue_lane: str,
    *,
    notes: str = "",
    slice_id: str = "",
) -> dict[str, Any]:
    """Operator pass between sessions — clear park, allow depth bump next overnight."""
    out = append_operator_playtest_feedback(
        vault_root,
        queue_lane,
        passed=True,
        notes=notes,
        slice_id=slice_id,
    )
    cleared = clear_playtest_exit_after_attestation(vault_root, project_id)
    return {"ok": out.get("ok") and cleared.get("ok", False), "feedback": out, "cleared": cleared}


def record_playtest_fail_and_enqueue_rework(
    vault_root: Path,
    project_id: str,
    queue_lane: str,
    packet: dict[str, Any],
    *,
    notes: str = "",
    slice_id: str = "",
    run_id: str = "",
    lane_id: str = "",
) -> dict[str, Any]:
    """
    Operator fail — packet stays live; append feedback; optional rework PQ lines.
    """
    feedback = append_operator_playtest_feedback(
        vault_root,
        queue_lane,
        passed=False,
        notes=notes,
        slice_id=slice_id,
        run_id=run_id,
    )
    rework: dict[str, Any] = {"skipped": True}
    if slice_id and lane_id:
        orch = run_factory_orchestrator(
            vault_root,
            write_dispatch=False,
            run_gates=False,
            project_id=project_id,
        )
        if orch.jobs:
            target_lane = lane_id
            matching = [j for j in orch.jobs if str(j.get("lane_id")) == target_lane]
            jobs = matching or list(orch.jobs[:1])
            rework = append_factory_rework(
                vault_root,
                queue_lane,
                packet,
                run_id=run_id or f"playtest-fail-{slice_id}",
                slice_id=slice_id,
                lane_id=str(jobs[0].get("lane_id") or lane_id),
                jobs=jobs,
                rework_iteration=1,
            )

    pending, pending_ids = playtest_feedback_pending(vault_root, project_id)
    return {
        "ok": bool(feedback.get("ok")),
        "feedback": feedback,
        "rework": rework,
        "feedback_still_pending": pending,
        "pending_ids": pending_ids,
    }
