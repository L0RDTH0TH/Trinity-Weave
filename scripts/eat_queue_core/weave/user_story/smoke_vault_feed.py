#!/usr/bin/env python3
"""Smoke test vault_roadmap factory feed — factory-project manifest + loop 3 active_slice."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eat_queue_core.weave.factory.factory_bootstrap import evaluate_bootstrap_gates
from eat_queue_core.weave.factory.factory_orchestrator import run_factory_orchestrator
from eat_queue_core.weave.factory.factory_pq_stage import stage_factory_dispatch_to_pq
from eat_queue_core.weave.factory.factory_project import load_factory_project
from eat_queue_core.weave.factory.surface_pass import run_surface_pass
from eat_queue_core.weave.user_story.product_factory_state import load_product_factory
from eat_queue_core.weave.user_story.work_order_translate import (
    FEED_VAULT_ROADMAP,
    translate_vault_work_orders,
)

# Operator playtest rows — honest fail until product work ships (not pipe blockers).
_KINESTHETIC_DEBT_PREFIXES = (
    "kinesthetic_feedback_fail:",
    "kinesthetic_feedback_undecided:",
    "kinesthetic_feedback_missing:",
    "proxy_pass_as_kinesthetic:",
    "invalid_proof_tier_for_pass:",
    "premature_alpha_sign_without_surface_pass",
    "factory_ship_valid_true_while_surface_fail",
)


def _partition_violations(violations: tuple[str, ...] | list[str]) -> tuple[list[str], list[str]]:
    hard: list[str] = []
    debt: list[str] = []
    for v in violations:
        if any(v.startswith(p) for p in _KINESTHETIC_DEBT_PREFIXES):
            debt.append(v)
        else:
            hard.append(v)
    return hard, debt


def _resolve_active_slice(
    vault_root: Path,
    project_id: str,
    *,
    row_id: str | None,
    dispatch_depth: int | None,
) -> dict[str, object] | None:
    if row_id and dispatch_depth is not None:
        return {"row_ids": [row_id], "dispatch_depth": dispatch_depth}
    pf = load_product_factory(vault_root, project_id)
    if pf.get("slice_selection_confirmed_at"):
        raw = pf.get("active_slice")
        return raw if isinstance(raw, dict) else None
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smoke test vault_roadmap factory feed")
    parser.add_argument("--vault-root", type=Path, default=Path.cwd())
    parser.add_argument("--project-id", default="godot-genesis-mythos-master")
    parser.add_argument("--lane", default="godot")
    parser.add_argument("--row-id", default="", help="Loop 3 catalog row (smoke override)")
    parser.add_argument("--dispatch-depth", type=int, default=None, help="Loop 3 dispatch depth")
    parser.add_argument("--dry-run", action="store_true", help="Orchestrator + PQ preview only; no PQ append")
    parser.add_argument("--skip-gates", action="store_true", help="Skip honesty gates in orchestrator")
    parser.add_argument("--translate-only", action="store_true", help="Only run translator; no orchestrator")
    parser.add_argument(
        "--require-trinity-green",
        action="store_true",
        help="Fail if surface_pass is red (operator kinesthetic debt must be cleared)",
    )
    args = parser.parse_args(argv)

    vault_root = args.vault_root.resolve()
    print(f"vault_root={vault_root}")
    print(f"feed_authority={FEED_VAULT_ROADMAP}")

    bootstrap = load_factory_project(vault_root, args.project_id)
    active_slice = _resolve_active_slice(
        vault_root,
        args.project_id,
        row_id=args.row_id or None,
        dispatch_depth=args.dispatch_depth,
    )
    if active_slice is None:
        print(
            "FAIL: loop 3 not confirmed — run product-factory-confirm-slice "
            "or pass --row-id and --dispatch-depth"
        )
        return 1

    bundle = translate_vault_work_orders(
        vault_root,
        project_id=args.project_id,
        queue_bootstrap=bootstrap,
        active_slice=active_slice,
    )
    if bundle is None:
        print("FAIL: translate_vault_work_orders returned None")
        return 1

    print("OK: translate")
    print(json.dumps(bundle.feed_metadata(), indent=2))
    print(f"slice_id={bundle.slice_id} lanes={bundle.lane_ids} jobs={len(bundle.jobs)}")

    if args.translate_only:
        return 0

    bootstrap_ok, bootstrap_v = evaluate_bootstrap_gates(
        vault_root, bootstrap, run_honesty_checks=not args.skip_gates
    )
    print(f"bootstrap_ok={bootstrap_ok}")
    if bootstrap_v:
        print("bootstrap_violations:", bootstrap_v)
    if not bootstrap_ok:
        print("FAIL: Trinity bootstrap gates blocked")
        return 1

    surface = run_surface_pass(vault_root, run_probes=False)
    print(f"trinity_surface_pass={surface.ok}")
    if not surface.ok:
        print("surface_violations:", surface.little_val.anti_pattern_violations)

    orch = run_factory_orchestrator(
        vault_root,
        write_dispatch=not args.dry_run,
        run_gates=not args.skip_gates,
        feed_authority=FEED_VAULT_ROADMAP,
        project_id=args.project_id,
        active_slice=active_slice,
    )
    print(f"orchestrator ok={orch.ok} detail={orch.detail} slice={orch.active_slice_id} jobs={len(orch.jobs)}")
    hard_v, debt_v = _partition_violations(orch.gate_violations)
    if hard_v:
        print("gate_violations_hard:", hard_v)
    if debt_v:
        print("gate_violations_kinesthetic_debt:", debt_v)

    if not orch.jobs:
        print("FAIL: orchestrator produced no jobs")
        return 1

    if hard_v and not args.skip_gates:
        print("FAIL: Trinity hard gate violations (not operator kinesthetic debt)")
        return 1

    if not orch.ok and not args.skip_gates and hard_v:
        print("FAIL: orchestrator blocked on hard gates")
        return 1

    packet = {
        "project_id": args.project_id,
        "planner_hints": {
            "feed_authority": FEED_VAULT_ROADMAP,
            "repo_path": bundle.game_repo_rel,
        },
    }
    staged = stage_factory_dispatch_to_pq(
        vault_root,
        args.lane,
        packet,
        run_id="smoke-vault-feed",
        dry_run=True,
    )
    preview = staged.get("entries_preview") or []
    print(f"PQ dry-run would_append={staged.get('would_append', 0)}")
    if preview:
        sample = preview[0]
        params = sample.get("params") or {}
        print("PQ sample params keys:", sorted(params.keys()))
        print("catalog_row_id:", params.get("catalog_row_id"))
        print("ux_feed:", params.get("ux_feed"))
        print("slice_id:", params.get("slice_id"))

    if orch.active_slice_id and not orch.active_slice_id.startswith("row_"):
        print("FAIL: expected vault slice_id prefix row_")
        return 1

    if not any(j.get("catalog_row_id") for j in orch.jobs):
        print("FAIL: jobs missing catalog_row_id")
        return 1

    if args.require_trinity_green and not surface.ok:
        print("FAIL: --require-trinity-green but surface_pass is red (operator kinesthetic debt)")
        return 1

    if debt_v and not args.require_trinity_green:
        print(
            "NOTE: Trinity surface_pass red — honest operator kinesthetic debt; "
            "pipe OK; dispatch allowed via allow_implement_with_gates_red"
        )

    print("SMOKE PASS: vault roadmap → dispatch → PQ preview (Trinity bootstrap green)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
