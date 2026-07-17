"""CLI entry for Implementation Factory harness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .factory_research_enqueue import DEPRECATED_SIDE_QUEUE, enqueue_stack_research
from .gap_research_router import detect_and_route_gaps
from .interop_pass import run_interop_pass
from .review_pass_runner import (
    run_all_baseline_passes,
    run_pipeline_proof_pass,
    run_stack_operational_pass,
)
from .closed_alpha_passes import run_all_closed_alpha_passes
from .factory_output_gate import run_factory_output_gate
from .kinesthetic_probes import run_and_sync_probes
from .gate_precedence import evaluate_precedence
from .lane_charters import validate_six_lane_charters
from .factory_orchestrator import run_factory_orchestrator
from .playtest_session_ingest import ingest_playtest_session
from .playtest_brief import write_playtest_brief
from .operator_confirm import (
    confirm_all_kinesthetic_operator,
    confirm_from_playtest_ingest,
    confirm_operator_feedback_row,
    list_pending_confirmations,
)
from .operator_playtest_session import run_operator_playtest_session
from .weave_track import disconnect_track, reconnect_track, track_status
from .surface_pass import run_surface_pass
from .structure_lint import run_structure_pass
from .tech_stack_manifest import load_manifest, validate_manifest_schema


def _serialize_passes(out: dict) -> dict:
    return {
        "all_ok": out["all_ok"],
        "passes": {
            k: {
                "ok": v.ok,
                "detail": getattr(v, "detail", ""),
                "violations": list(getattr(v, "little_val", None).anti_pattern_violations)
                if getattr(v, "little_val", None)
                else list(getattr(v, "violations", ())),
            }
            for k, v in out["passes"].items()
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Implementation Factory harness")
    parser.add_argument("--vault-root", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("manifest-validate", help="Validate Tech-Stack-Manifest + domain registry")
    sub.add_parser("integrate", help="Run stack_integrate_pass")
    sub.add_parser("gaps", help="Detect stack gaps from manifest")
    sub.add_parser("operational", help="Run stack_operational_pass")
    sub.add_parser("pipeline-proof", help="Run pipeline_proof_pass")
    sub.add_parser("interop", help="Run interop_pass")
    sub.add_parser("all-passes", help="Run all baseline passes")
    sub.add_parser("lane-charters-validate", help="Validate six factory lane milestone charters")
    kp = sub.add_parser("kinesthetic-probe", help="Run automated kinesthetic probes and sync operator_feedback")
    kp.add_argument("--smokes", action="store_true", help="Also run headless Godot smokes (slow)")
    kp.add_argument("--dry-run", action="store_true", help="Do not write operator_feedback YAML")

    sp = sub.add_parser("surface-pass", help="Surface seat / usability_pass (Tier B human gate)")
    sp.add_argument("--no-probe", action="store_true", help="Skip kinesthetic probe sync before gate")
    sp.add_argument("--smokes", action="store_true", help="Run Godot smokes during probe sync")

    pi = sub.add_parser("playtest-ingest", help="Ingest latest F6 playtest session JSONL into operator_feedback")
    pi.add_argument("--session", type=Path, default=None, help="Session JSONL path (default: latest on product track)")
    pi.add_argument("--dry-run", action="store_true", help="Do not write operator_feedback YAML")

    ops = sub.add_parser(
        "operator-playtest-session",
        help="Post-F6 operator session: ingest capture + list pending confirms (not overnight)",
    )
    ops.add_argument("--session", type=Path, default=None)
    ops.add_argument("--surface", action="store_true", help="Also run surface-pass after ingest")
    ops.add_argument("--no-write", action="store_true", help="Dry-run ingest (no feedback write)")

    pb = sub.add_parser("playtest-brief", help="Write Playtest-Brief for a factory slice (operator handoff)")
    pb.add_argument("--slice-id", type=str, required=True)
    pb.add_argument("--queue-lane", type=str, default="godot")

    oc = sub.add_parser("operator-confirm", help="Set operator_confirmed + pass on kinesthetic feedback rows")
    oc.add_argument("--list", action="store_true", help="List rows pending operator confirm")
    oc.add_argument("--checklist-id", type=str, default=None)
    oc.add_argument("--pass", dest="pass_val", type=str, default=None, help="true|false")
    oc.add_argument("--notes", type=str, default="")
    oc.add_argument("--confirm", action="store_true", help="Set operator_confirmed true")
    oc.add_argument("--from-ingest", action="store_true", help="Confirm playtest_trace rows with window_pass=true")
    oc.add_argument("--all", action="store_true", help="Bulk confirm all kinesthetic IDs (operator source)")
    oc.add_argument("--dry-run", action="store_true")

    sub.add_parser("closed-alpha-passes", help="Closed Alpha passes incl. Surface + rollup + precedence")
    sub.add_parser("factory-orchestrator", help="Dispatch active alpha slice to six lane factories")
    sub.add_parser("bootstrap-drops", help="Create ADC/TAC/CDC/PDC/AuDC manifest skeletons in game repo")
    sub.add_parser("factory-run-summary", help="Write Factory-Run-Summary rollup from correlation logs")
    mb = sub.add_parser("merge-barrier-check", help="Check merge_barrier for a dispatch job JSON on stdin")
    sub.add_parser("structure-pass", help="Oak topology lint vs FACTORY_ZONES.yaml")

    gp = sub.add_parser("gate-precedence-check", help="Evaluate gate precedence from pass map JSON on stdin")
    gp.add_argument("--pass-json", type=str, default=None, help='JSON object pass_name -> bool, e.g. {"surface_pass":false}')

    fog = sub.add_parser(
        "factory-output-gate",
        help="Closed Alpha factory output conduct (off|warn|block from Config)",
    )
    fog.add_argument(
        "--mode",
        choices=("off", "warn", "block"),
        default=None,
        help="Override factory_output_trinity_gate from Config",
    )
    fog.add_argument("--no-align", action="store_true", help="Skip trinity_align on factory_output_conduct")
    fog.add_argument("--no-narrative-scan", action="store_true", help="Skip Core/ narrative drift scan")

    rq = sub.add_parser("research-enqueue", help="Build RESEARCH-AGENT entries for baseline domains")
    rq.add_argument("--dry-run", action="store_true", default=False)
    rq.add_argument("--write-queue", action="store_true", default=False)

    wt = sub.add_parser("weave-track", help="Product weave_track coupled/disconnected status")
    wt.add_argument("--disconnect", action="store_true", help="Set track_status disconnected")
    wt.add_argument("--reconnect", action="store_true", help="Reconnect when product welds exist")
    wt.add_argument("--reason", default="", help="Reason for status change")

    hr = sub.add_parser("honesty-rollup", help="Stack + product kinesthetic honesty rollup")

    rs = sub.add_parser(
        "replay-seats",
        help="Replay lane seats for a jammed factory job without re-running the agent",
    )
    rs.add_argument("--queue-lane", type=str, default="godot")
    rs.add_argument("--job-id", type=str, required=True)
    rs.add_argument("--agent-log", type=str, default=None, help="Vault-relative agent telemetry log")
    rs.add_argument(
        "--seats-only",
        action="store_true",
        help="Run seats only; do not mark lane complete or slice rollup",
    )

    ms = sub.add_parser("machine-status", help="List per-job factory machine state (jam checkpoints)")
    ms.add_argument("--jammed-only", action="store_true", help="Only show jammed jobs")
    ms.add_argument("--job-id", type=str, default=None, help="Show one job state JSON")

    fb = sub.add_parser("factory-bom", help="Evaluate Product Factory BOM (setup checklist)")
    fb.add_argument("--project-id", type=str, default="godot-genesis-mythos-master")
    fb.add_argument(
        "--sections",
        type=str,
        default=None,
        help="Comma-separated sections (default: all)",
    )

    fbb = sub.add_parser("factory-bom-brief", help="Write operator Factory BOM brief markdown")
    fbb.add_argument("--project-id", type=str, default="godot-genesis-mythos-master")

    sc = sub.add_parser("scaffold-project", help="Bootstrap Factory-DRB for a new project_id")
    sc.add_argument("--project-id", type=str, required=True)
    sc.add_argument("--game-repo-path", type=str, required=True)
    sc.add_argument("--release-tier", type=str, default="closed_alpha")

    args = parser.parse_args(argv)
    vault = args.vault_root.resolve()

    if args.cmd == "manifest-validate":
        m = load_manifest(vault)
        v = validate_manifest_schema(m, vault)
        print(json.dumps({"ok": not v, "violations": v, "pipeline_certified": m.pipeline_certified}, indent=2))
        return 0 if not v else 1

    if args.cmd == "integrate":
        r = run_stack_integrate_pass(vault)
        print(json.dumps({"ok": r.ok, "run_id": r.run_id, "violations": list(r.violations)}, indent=2))
        return 0 if r.ok else 1

    if args.cmd == "gaps":
        notes = detect_and_route_gaps(vault)
        print(json.dumps(notes, indent=2))
        return 0

    if args.cmd == "operational":
        r = run_stack_operational_pass(vault)
        print(json.dumps({"ok": r.ok, "detail": r.detail}, indent=2))
        return 0 if r.ok else 1

    if args.cmd == "pipeline-proof":
        r = run_pipeline_proof_pass(vault)
        print(json.dumps({"ok": r.ok, "detail": r.detail, "violations": r.little_val.anti_pattern_violations}, indent=2))
        return 0 if r.ok else 1

    if args.cmd == "interop":
        r = run_interop_pass(vault)
        print(json.dumps({"ok": r.ok, "detail": r.detail, "pending_domains": list(r.pending_domains), "violations": r.little_val.anti_pattern_violations}, indent=2))
        return 0 if r.ok else 1

    if args.cmd == "all-passes":
        out = run_all_baseline_passes(vault)
        print(json.dumps(_serialize_passes(out), indent=2))
        return 0 if out["all_ok"] else 1

    if args.cmd == "lane-charters-validate":
        v = validate_six_lane_charters(vault)
        print(json.dumps({"ok": not v, "violations": v}, indent=2))
        return 0 if not v else 1

    if args.cmd == "kinesthetic-probe":
        out = run_and_sync_probes(
            vault,
            run_smokes=bool(getattr(args, "smokes", False)),
            write_feedback=not bool(getattr(args, "dry_run", False)),
        )
        print(json.dumps(out, indent=2))
        return 0 if out["all_ok"] else 1

    if args.cmd == "surface-pass":
        r = run_surface_pass(
            vault,
            run_probes=not bool(getattr(args, "no_probe", False)),
            run_smokes=bool(getattr(args, "smokes", False)),
        )
        print(json.dumps(r.to_dict(), indent=2))
        return 0 if r.ok else 1

    if args.cmd == "playtest-ingest":
        session = getattr(args, "session", None)
        r = ingest_playtest_session(
            vault,
            session_path=session,
            write_feedback=not bool(getattr(args, "dry_run", False)),
        )
        print(json.dumps(r.to_dict(), indent=2))
        return 0 if r.ok else 1

    if args.cmd == "operator-playtest-session":
        r = run_operator_playtest_session(
            vault,
            session_path=getattr(args, "session", None),
            run_surface_pass=bool(getattr(args, "surface", False)),
            write_feedback=not bool(getattr(args, "no_write", False)),
        )
        print(json.dumps(r.to_dict(), indent=2))
        return 0 if r.ok else 1

    if args.cmd == "playtest-brief":
        r = write_playtest_brief(
            vault,
            slice_id=str(args.slice_id),
            queue_lane=str(args.queue_lane),
        )
        print(json.dumps(r.to_dict(), indent=2))
        return 0 if r.ok else 1

    if args.cmd == "operator-confirm":
        if getattr(args, "list", False):
            pending = list_pending_confirmations(vault)
            print(json.dumps({"pending": pending}, indent=2))
            return 0
        if getattr(args, "from_ingest", False):
            r = confirm_from_playtest_ingest(vault, dry_run=bool(getattr(args, "dry_run", False)))
            print(json.dumps(r.to_dict(), indent=2))
            return 0 if r.ok else 1
        if getattr(args, "all", False):
            pv = getattr(args, "pass_val", None)
            if pv is None:
                print(json.dumps({"ok": False, "error": "--pass required with --all"}, indent=2))
                return 1
            r = confirm_all_kinesthetic_operator(
                vault, pass_=str(pv).lower() in ("true", "1", "yes"), notes=str(args.notes or "")
            )
            print(json.dumps(r.to_dict(), indent=2))
            return 0 if r.ok else 1
        cid = getattr(args, "checklist_id", None)
        pv = getattr(args, "pass_val", None)
        if not cid or pv is None:
            print(json.dumps({"ok": False, "error": "use --list, --from-ingest, --all, or --checklist-id + --pass"}, indent=2))
            return 1
        r = confirm_operator_feedback_row(
            vault,
            checklist_id=str(cid),
            pass_=str(pv).lower() in ("true", "1", "yes"),
            notes=str(args.notes or ""),
            source="operator",
            operator_confirmed=bool(getattr(args, "confirm", False) or True),
        )
        print(json.dumps(r.to_dict(), indent=2))
        return 0 if r.ok else 1

    if args.cmd == "factory-orchestrator":
        r = run_factory_orchestrator(vault)
        print(json.dumps(r.to_dict(), indent=2))
        return 0 if r.ok else 1

    if args.cmd == "bootstrap-drops":
        from .drop_contract_base import bootstrap_all_drop_manifests
        from .tech_stack_manifest import load_manifest

        m = load_manifest(vault)
        repo = vault / m.game_repo_path
        created = bootstrap_all_drop_manifests(repo)
        print(json.dumps({"ok": True, "created": created}, indent=2))
        return 0

    if args.cmd == "factory-run-summary":
        from .factory_run_summary import write_factory_run_summary

        p = write_factory_run_summary(vault)
        print(json.dumps({"ok": True, "path": str(p.relative_to(vault))}, indent=2))
        return 0

    if args.cmd == "merge-barrier-check":
        from .merge_barrier import check_job_allowed
        from .tech_stack_manifest import load_manifest

        job = json.load(sys.stdin)
        m = load_manifest(vault)
        r = check_job_allowed(vault, job, game_repo_rel=m.game_repo_path)
        print(json.dumps(r.to_dict(), indent=2))
        return 0 if r.allowed else 1

    if args.cmd == "closed-alpha-passes":
        out = run_all_closed_alpha_passes(vault)
        payload = {
            "all_ok": out["all_ok"],
            "precedence": out["precedence"],
            "passes": {
                k: {
                    "ok": v.ok,
                    "detail": v.detail,
                    "violations": list(v.little_val.anti_pattern_violations),
                }
                for k, v in out["passes"].items()
            },
        }
        print(json.dumps(payload, indent=2))
        return 0 if out["all_ok"] else 1

    if args.cmd == "gate-precedence-check":
        raw = getattr(args, "pass_json", None)
        if raw:
            pass_map = json.loads(raw)
        else:
            pass_map = json.load(sys.stdin)
        if not isinstance(pass_map, dict):
            print(json.dumps({"ok": False, "error": "pass map must be object"}, indent=2))
            return 1
        verdict = evaluate_precedence({k: bool(v) for k, v in pass_map.items()})
        print(json.dumps(verdict.to_dict(), indent=2))
        return 0 if verdict.ok else 1

    if args.cmd == "structure-pass":
        r = run_structure_pass(vault)
        print(json.dumps(r.to_dict(), indent=2))
        return 0 if r.ok else 1

    if args.cmd == "factory-output-gate":
        mode = getattr(args, "mode", None)
        result = run_factory_output_gate(
            vault,
            mode=mode,
            run_align=not bool(getattr(args, "no_align", False)),
            scan_narrative=not bool(getattr(args, "no_narrative_scan", False)),
        )
        print(json.dumps(result.to_dict(), indent=2))
        return 0 if result.ok else 1

    if args.cmd == "research-enqueue":
        dry = not args.write_queue
        result = enqueue_stack_research(vault, dry_run=dry)
        payload = {
            "count": len(result.entries),
            "dry_run": dry,
            "lane": result.lane,
            "output_path": str(result.output_path) if result.output_path else None,
            "deprecated_side_queue": DEPRECATED_SIDE_QUEUE,
            "entries": list(result.entries),
        }
        print(json.dumps(payload, indent=2))
        return 0

    if args.cmd == "weave-track":
        if args.disconnect:
            path = disconnect_track(vault, reason=args.reason or "operator_disconnect")
            print(json.dumps({"ok": True, "track_status": "disconnected", "path": str(path)}, indent=2))
            return 0
        if args.reconnect:
            ok, detail = reconnect_track(vault, reason=args.reason or "operator_reconnect")
            print(json.dumps({"ok": ok, "detail": detail, "track_status": track_status(vault)}, indent=2))
            return 0 if ok else 1
        print(json.dumps({"track_status": track_status(vault)}, indent=2))
        return 0

    if args.cmd == "honesty-rollup":
        from .factory_honesty_rollup import honesty_rollup_summary, run_factory_honesty_rollup

        rollup = honesty_rollup_summary(run_factory_honesty_rollup(vault))
        print(json.dumps(rollup, indent=2))
        return 0 if rollup.get("all_ok") else 1

    if args.cmd == "replay-seats":
        from .factory_lane_recovery import replay_factory_lane_by_job_id

        out = replay_factory_lane_by_job_id(
            vault,
            str(args.queue_lane),
            str(args.job_id),
            agent_log_path=getattr(args, "agent_log", None),
            complete_if_ok=not bool(getattr(args, "seats_only", False)),
        )
        print(json.dumps(out, indent=2, default=str))
        return 0 if out.get("ok") else 1

    if args.cmd == "machine-status":
        from .factory_machine_state import list_machine_states, load_machine_state

        job_id = getattr(args, "job_id", None)
        if job_id:
            state = load_machine_state(vault, str(job_id))
            if state is None:
                print(json.dumps({"ok": False, "error": "machine_state_not_found", "job_id": job_id}, indent=2))
                return 1
            print(json.dumps({"ok": True, "state": state}, indent=2))
            return 0
        rows = list_machine_states(vault, jammed_only=bool(getattr(args, "jammed_only", False)))
        print(json.dumps({"ok": True, "count": len(rows), "states": rows}, indent=2))
        return 0

    if args.cmd == "factory-bom":
        from .factory_bom import evaluate_factory_bom

        sections = None
        if args.sections:
            sections = tuple(x.strip() for x in args.sections.split(",") if x.strip())
        out = evaluate_factory_bom(vault, project_id=args.project_id, sections=sections)
        print(json.dumps(out.to_dict(), indent=2))
        return 0 if out.ok else 1

    if args.cmd == "factory-bom-brief":
        from .factory_bom_brief import write_factory_bom_brief

        out = write_factory_bom_brief(vault, project_id=args.project_id)
        print(json.dumps(out.to_dict(), indent=2))
        return 0 if out.ok else 1

    if args.cmd == "scaffold-project":
        from .factory_drb_paths import scaffold_factory_project

        out = scaffold_factory_project(
            vault,
            project_id=args.project_id,
            game_repo_path=args.game_repo_path,
            release_tier=args.release_tier,
        )
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
