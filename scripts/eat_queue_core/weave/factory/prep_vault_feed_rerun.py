"""Prep vault-feed product factory re-run — goal packet + PQ hygiene (not closed-alpha queue)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ...goal_authority_io import goal_authority_path_for_lane
from ...lane_bundle import bundle_dir_for_lane
from ..user_story.product_factory_budget import budget_row_ids
from ..user_story.catalog_io import load_json, user_story_paths


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def refresh_goal_packet_vault_feed(
    vault_root: Path,
    *,
    lane: str,
    project_id: str = "genesis-mythos-master",
) -> dict[str, Any]:
    """Rewrite goal-authority for levels+waves (vault_roadmap). closed_alpha = user label only."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    path = goal_authority_path_for_lane(vault_root, lane)

    row_ids = budget_row_ids(vault_root, project_id)
    budget = load_json(user_story_paths(vault_root, project_id)["budget"])
    rows = budget.get("rows") or []
    primary_row = row_ids[0] if row_ids else "ui_presentation_shell"
    row_state = next(
        (r for r in rows if isinstance(r, dict) and str(r.get("row_id")) == primary_row),
        {},
    )
    target_depth = int(row_state.get("target_depth") or 2)
    current_depth = int(row_state.get("current_depth") or 0)

    now = _utc_iso()
    run_id = f"gmm-vault-feed-{now.replace(':', '').replace('-', '')[:15]}Z"
    prior_run = None
    if path.is_file():
        try:
            prior = json.loads(path.read_text(encoding="utf-8"))
            prior_run = prior.get("run_id")
        except (json.JSONDecodeError, OSError):
            pass

    packet: dict[str, Any] = {
        "run_id": run_id,
        "confirmed_at": now,
        "confirmed_by": "operator",
        "confirmed_by_operator": True,
        "subject_lane": lane,
        "project_id": project_id,
        "master_goal_ref": f"1-Projects/{project_id}/{project_id}-goal.md",
        "also_run_lanes": [],
        "intent_summary": (
            f"Product factory — {primary_row} at dispatch_depth 1 (levels + waves, vault_roadmap feed). "
            "Stage 2: factory lanes + PM waves. Stage 3: operator playtest + kinesthetic confirm. "
            "'closed_alpha' is an optional user release label only — not the scheduling rail."
        ),
        "done_when": [
            f"budget row {primary_row}: current_depth >= target_depth ({target_depth})",
            "factory_staged IMPLEMENT_SLICE jobs consumed on godot PQ",
            "PM review pass + depth bump per beat",
            "operator kinesthetic rows confirmed before slice exit surface_pass",
        ],
        "not_done_signals": [
            "factory_ship_valid: false",
            "slice exit gates red (surface_pass, factory_output_conduct, product_kinesthetic_honesty)",
            "operator kinesthetic rows not confirmed (source: operator)",
            "legacy alpha-factory-queue slice ids on PQ",
        ],
        "allow_layer1_empty_queue_bootstrap": True,
        "overnight_launch_authorized": True,
        "overnight_authorized_at": now,
        "allow_dynamic_lanes": False,
        "packet_ttl_hours": 168,
        "early_stop_policy": {
            "implementation_gate": False,
            "on_implementation_necessary": "prefer_factory_lane_work_over_roadmap_deepen",
            "forbidden_without_packet": [
                "sandbox_lane_resumes",
                "resume_roadmap_deepen_on_godot_pq",
            ],
        },
        "planner_hints": {
            "queue_lane": lane,
            "roadmap_track": "execution",
            "effective_track": "implementation",
            "feed_authority": "vault_roadmap",
            "factory_project_ref": f"1-Projects/{project_id}/Factory-DRB/factory-project.yaml",
            "budget_ref": f"1-Projects/{project_id}/Roadmap/User-Story/slice-depth-budget.json",
            "catalog_ref": f"1-Projects/{project_id}/Roadmap/User-Story/slice-catalog.yaml",
            "active_row_id": primary_row,
            "target_depth": target_depth,
            "current_depth": current_depth,
            "dispatch_depth": 1,
            "user_release_label": "closed_alpha",
            "repo_path": "5-Attachments/Code-Repos/genesis-mythos-alpha/",
            "engine_adapter": "godot_4_6_3_dotnet",
            "launch_scene": "5-Attachments/Code-Repos/genesis-mythos-alpha/LaunchShell.tscn",
            "play_region_scene": "5-Attachments/Code-Repos/genesis-mythos-alpha/PlayRegion.tscn",
            "operator_feedback_ref": (
                f"1-Projects/{project_id}/Factory-DRB/operator-feedback/"
                "godot-closed-alpha-kinesthetic.yaml"
            ),
            "factory_ship_valid": False,
            "legacy_alpha_queue_ref": (
                f"1-Projects/{project_id}/Factory-DRB/alpha-factory-queue.yaml"
            ),
            "legacy_alpha_queue_note": "DEPRECATED — scheduling uses product_factory + slice-depth-budget only",
        },
    }
    if prior_run:
        packet["supersedes"] = prior_run

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "path": str(path), "run_id": run_id, "active_row_id": primary_row}


def clear_legacy_alpha_pq(vault_root: Path, *, lane: str) -> dict[str, Any]:
    """Remove legacy closed-alpha IMPLEMENT_SLICE / decoy lines from lane PQ."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    bundle = bundle_dir_for_lane(vault_root, lane)
    pq = bundle / "prompt-queue.jsonl"
    archive = bundle / "prompt-queue-archive-legacy-alpha.jsonl"

    if not pq.is_file():
        return {"ok": True, "removed": 0, "reason": "no_pq"}

    kept: list[str] = []
    removed: list[str] = []
    for line in pq.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            kept.append(line)
            continue
        mode = str(entry.get("mode") or "")
        params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
        slice_id = str(params.get("slice_id") or "")
        legacy = (
            slice_id.startswith("alpha_")
            or mode == "RESUME_ROADMAP"
            or str(entry.get("id") or "").startswith("decoy-")
        )
        if legacy:
            removed.append(line)
        else:
            kept.append(line)

    if removed:
        archive.parent.mkdir(parents=True, exist_ok=True)
        with archive.open("a", encoding="utf-8") as af:
            for ln in removed:
                af.write(ln + "\n")

    pq.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    return {"ok": True, "removed": len(removed), "kept": len(kept), "archive": str(archive)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Prep vault-feed factory re-run")
    p.add_argument("--vault-root", type=Path, default=Path("."))
    p.add_argument("--lane", default="godot")
    p.add_argument("--project-id", default="genesis-mythos-master")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("goal-packet", help="Refresh goal-authority.json for vault_roadmap")
    sub.add_parser("clear-pq", help="Archive legacy alpha-queue PQ lines")
    args = p.parse_args(argv)
    vault = args.vault_root.resolve()

    if args.cmd == "goal-packet":
        out = refresh_goal_packet_vault_feed(vault, lane=args.lane, project_id=args.project_id)
    elif args.cmd == "clear-pq":
        out = clear_legacy_alpha_pq(vault, lane=args.lane)
    else:
        print(json.dumps({"ok": False, "error": "unknown_cmd"}))
        return 1

    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
