"""
Unified EAT-QUEUE harness CLI (single writer for PQ bytes).

Run from vault root::

    PYTHONPATH=scripts python3 -m eat_queue_core.harness snapshot --vault-root .
    PYTHONPATH=. python3 -m scripts.eat_queue_core.harness snapshot --vault-root .

See 3-Resources/Second-Brain/Docs/Queue-Harness-Architecture.md

Telemetry field reference: ``scripts/eat_queue_core/docs/TELEMETRY_CONTRACT.md``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .a5b_dedupe import (
    decide_append,
    estimate_context_tokens,
    intra_batch_strict_merge,
    _guidance_from_entry,
)
from ._lock import acquire_gitforge_lock, release_gitforge_lock
from .config_loader import (
    default_mutation_recovery_mode,
    max_midrun_appends,
    origin_dedupe_window_hours,
    parallel_execution_tracks_enabled,
    parse_queue_config,
)
from .full_cycle import (
    append_task_handoff_jsonl,
    apply_queue_cleanup,
    apply_queue_cleanup_dual_track,
    build_a5b_append_intent_receipt_row,
    effective_queue_lane,
    parallel_track_for_lane,
    run_full_eat_queue_cycle,
)
from .harness_queue_settings import effective_harness_settings, resolve_harness_config_path
from .lane_queue_config import effective_max_inline_a5b
from .watcher_append import append_watcher_telemetry_line
from .models import QueueEntry
from .lanes import FALLBACK_ALLOWED_LANES, validate_lane_filter_token
from .plan import append_decisions, build_plan, emit_plan_json, load_queue_file, print_plan_success_summary
from .pool_sync import hydrate_track_pq_from_pool
from .post_queue_gitforge import load_handoff_json, run_post_queue_gitforge
from .post_queue_weave_publish import run_post_queue_weave_publish
from .weave_public_publish import run_weave_public_sync
from .project_bridge_sync import run_project_bridge_sync
from .project_bridge_push import run_project_bridge_push
from .grok_bridge_status import write_grok_bridge_status
from .grok_fulfill_broker import run_grok_fulfill_broker
from .continuity_handoff import load_handoff_json as load_memory_handoff_json
from .continuity_handoff import run_post_queue_memory_pass
from .lane_status_board import write_lane_status_board
from .syncthing_sync_policy import run_syncthing_sync_policy
from .nav_color_refresh import write_nav_color_index
from .queue_neighbor_prep import write_queue_neighbor_prep
from .pseudo_clock import tick as pseudo_clock_tick
from .schedule_tick import run_schedule_tick
from .vault_scan import vault_scan
from .cli_eat import cli_eat
from .skill_gap import scan_and_stub
from .skill_trial import activate_trial, record_pilot_run


def _read_json_or_yaml_file(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    text = text.strip()
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore[import-untyped]

            data = yaml.safe_load(text)
        except ImportError:
            raise SystemExit(
                "harness: PyYAML required for .yaml parallel-context files "
                "(pip install pyyaml) or use .json"
            ) from None
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("parallel context must be a JSON/YAML object")
    return data


from .parallel_context_util import (
    infer_lane_from_context_path,
    parallel_context_from_config_track,
    synthetic_parallel_context_for_lane,
)


def _infer_lane_from_context_path(path: Path) -> str | None:
    cand = infer_lane_from_context_path(path)
    return cand if cand and validate_lane_filter_token(cand, FALLBACK_ALLOWED_LANES) else None


def _parse_parallel_inline(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    try:
        out = json.loads(raw)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore[import-untyped]

            out = yaml.safe_load(raw)
        except ImportError as e:
            raise SystemExit(
                "harness: parallel-context-yaml must be JSON unless PyYAML is installed"
            ) from e
    if not isinstance(out, dict):
        raise SystemExit("harness: parallel-context-yaml must be a JSON/YAML object")
    return out


def resolve_parallel_context(
    vault_root: Path,
    parallel_file: Path | None,
    parallel_yaml: str | None,
    *,
    lane: str | None = None,
) -> dict[str, Any]:
    """
    Resolve parallel hand-off dict. If ``--parallel-context-file`` is missing on disk,
    use ``--lane`` or infer lane from ``.../parallel/<lane>/...`` and apply
    :func:`synthetic_parallel_context_for_lane` (stderr notice).

    When a context file exists and loads successfully, ``--parallel-context-yaml`` is ignored
    (legacy behavior). Inline YAML merges when no file was loaded from disk.
    """
    root = vault_root.resolve()
    out: dict[str, Any] = {}
    loaded_from_file = False

    if parallel_file is not None:
        p = parallel_file.expanduser()
        p = p if p.is_absolute() else (root / p)
        p = p.resolve()
        if p.is_file():
            out = dict(_read_json_or_yaml_file(p))
            loaded_from_file = True
        else:
            chosen: str | None = None
            if lane and str(lane).strip():
                t = lane.strip().lower()
                if validate_lane_filter_token(t, FALLBACK_ALLOWED_LANES):
                    chosen = t
                else:
                    raise SystemExit(
                        f"harness: invalid --lane {t!r}; expected one of {sorted(FALLBACK_ALLOWED_LANES)}"
                    )
            if chosen is None:
                chosen = _infer_lane_from_context_path(p)
            if chosen:
                print(
                    f"harness: parallel context file missing; using synthetic defaults for lane {chosen!r} ({p})",
                    file=sys.stderr,
                )
                out = synthetic_parallel_context_for_lane(chosen)
            else:
                raise SystemExit(
                    f"harness: parallel context file not found: {p}\n"
                    "Fix: create the file, pass --lane <godot|sandbox|...>, "
                    "or use --queue / --parallel-context-yaml with a JSON object."
                )
    elif lane and str(lane).strip():
        t = lane.strip().lower()
        if not validate_lane_filter_token(t, FALLBACK_ALLOWED_LANES):
            raise SystemExit(
                f"harness: invalid --lane {t!r}; expected one of {sorted(FALLBACK_ALLOWED_LANES)}"
            )
        out = synthetic_parallel_context_for_lane(t)

    if parallel_yaml and not loaded_from_file:
        extra = _parse_parallel_inline(parallel_yaml)
        out = {**out, **extra}
    return out


def _rel_vault(vault_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(vault_root.resolve()))
    except ValueError:
        return str(path)


def resolve_queue_and_plan_paths(
    vault_root: Path,
    *,
    queue: Path | None,
    parallel: dict[str, Any],
) -> tuple[Path, Path]:
    """Return (prompt_queue_path, eat_queue_run_plan_path)."""
    root = vault_root.resolve()
    if queue is not None:
        q = queue if queue.is_absolute() else (root / queue)
        q = q.resolve()
    else:
        rp = parallel.get("resolved_prompt_queue_path")
        if isinstance(rp, str) and rp.strip():
            q = (root / rp.strip()).resolve()
        else:
            q = (root / ".technical" / "prompt-queue.jsonl").resolve()
    plan = q.parent / "eat_queue_run_plan.json"
    return q, plan.resolve()


def cmd_snapshot(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    cfg = parse_queue_config(args.resolved_config)
    pool_default = (vault_root / ".technical" / "prompt-queue.jsonl").resolve()
    out: dict[str, Any] = {"vault_root": str(vault_root.resolve())}
    targets: list[tuple[str, Path]] = [("prompt_queue", qpath)]
    if cfg.get("central_pool_fanout_enabled") is True and qpath.resolve() != pool_default.resolve():
        targets.append(("central_pool", pool_default))
    for label, path in targets:
        if path.is_file():
            data = path.read_bytes()
            lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
            out[label] = {
                "path": _rel_vault(vault_root, path),
                "sha256": hashlib.sha256(data).hexdigest(),
                "line_count": len(lines),
            }
        else:
            out[label] = {
                "path": _rel_vault(vault_root, path),
                "sha256": None,
                "line_count": 0,
                "missing": True,
            }
    print(json.dumps(out, indent=2))
    return 0


def cmd_verify(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    cfg = parse_queue_config(args.resolved_config)
    expected_path = Path(args.expected_snapshot)
    if not expected_path.is_file():
        print(json.dumps({"ok": False, "error": "expected_snapshot file missing"}), file=sys.stderr)
        return 1
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    pool_default = (vault_root / ".technical" / "prompt-queue.jsonl").resolve()

    def snap_one(label: str, path: Path) -> dict[str, Any]:
        if not path.is_file():
            return {"path": str(path), "sha256": None, "line_count": 0, "missing": True}
        data = path.read_bytes()
        lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        return {
            "path": str(path),
            "sha256": hashlib.sha256(data).hexdigest(),
            "line_count": len(lines),
        }

    current_prompt = snap_one("prompt_queue", qpath)
    checks = [("prompt_queue", qpath, expected.get("prompt_queue"))]
    if cfg.get("central_pool_fanout_enabled") is True and qpath.resolve() != pool_default.resolve():
        checks.append(("central_pool", pool_default, expected.get("central_pool")))

    mismatches: list[str] = []
    for label, path, exp in checks:
        if exp is None and label != "prompt_queue":
            continue
        cur = snap_one(label, path)
        if exp and exp.get("sha256") and cur.get("sha256") != exp.get("sha256"):
            mismatches.append(label)

    recovery = default_mutation_recovery_mode(cfg)
    ok = len(mismatches) == 0
    result = {
        "ok": ok,
        "mismatches": mismatches,
        "mutation_recovery_mode": recovery,
        "recovery_hint": (
            "no_action"
            if ok
            else (
                "refuse_rewrite_log_errors"
                if recovery == "hard_stop"
                else (
                    "rerun_full_cycle_from_disk"
                    if recovery == "restart_plan"
                    else "rewrite_using_latest_snapshot_and_plan_ids"
                )
            )
        ),
    }
    print(json.dumps(result, indent=2))
    return 0 if ok else 2


def cmd_rewrite_consumed(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, plan_path = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    ids: set[str] = set()
    if args.ids:
        ids = {x.strip() for x in args.ids.split(",") if x.strip()}
    if args.plan:
        raw = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        rw = raw.get("queue_rewrite_ids")
        if isinstance(rw, list):
            ids |= {str(x) for x in rw}
        cons = raw.get("consumed_ids")
        if isinstance(cons, list):
            ids |= {str(x) for x in cons}
        # EatQueueRunPlan model uses consumed_ids on plan object
        if not ids and "consumed_ids" in raw:
            c2 = raw.get("consumed_ids")
            if isinstance(c2, list):
                ids = {str(x) for x in c2}
    if not ids:
        print(json.dumps({"ok": False, "error": "no ids to remove; pass --ids or --plan"}))
        return 1
    cfg = parse_queue_config(args.resolved_config)
    pool_default = (vault_root / ".technical" / "prompt-queue.jsonl").resolve()
    dual = (
        cfg.get("central_pool_fanout_enabled") is True
        and qpath.resolve() != pool_default.resolve()
        and not args.single_pool
    )
    if dual:
        tc, pc = apply_queue_cleanup_dual_track(qpath, pool_default, ids)
        out = {"ok": True, "track_pq_changed": tc, "central_pool_changed": pc, "removed_ids": sorted(ids)}
    else:
        ch = apply_queue_cleanup(qpath, ids)
        out = {"ok": True, "queue_changed": ch, "removed_ids": sorted(ids)}
    print(json.dumps(out, indent=2))
    return 0


def _resolve_parallel_track(parallel: dict[str, Any]) -> str:
    pt = parallel.get("parallel_track")
    if isinstance(pt, str) and pt.strip():
        return parallel_track_for_lane(pt.strip().lower())
    return parallel_track_for_lane(None)


def _append_prompt_queue_audit(audit_path: Path, record: dict[str, Any]) -> None:
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False) + "\n"
    prev = audit_path.read_text(encoding="utf-8") if audit_path.is_file() else ""
    audit_path.write_text(prev + line, encoding="utf-8")


def _snap_one_queue(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"sha256": None, "line_count": 0, "missing": True}
    data = path.read_bytes()
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "line_count": len(lines),
    }


def _verify_snapshot_for_append(
    vault_root: Path,
    qpath: Path,
    expected_path: Path,
    cfg: dict[str, Any],
) -> tuple[bool, list[str]]:
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    pool_default = (vault_root / ".technical" / "prompt-queue.jsonl").resolve()
    mismatches: list[str] = []
    cur_p = _snap_one_queue(qpath)
    exp_p = expected.get("prompt_queue") or {}
    if exp_p.get("sha256") and cur_p.get("sha256") != exp_p.get("sha256"):
        mismatches.append("prompt_queue")
    if cfg.get("central_pool_fanout_enabled") is True and qpath.resolve() != pool_default.resolve():
        cur_c = _snap_one_queue(pool_default)
        exp_c = expected.get("central_pool") or {}
        if exp_c.get("sha256") and cur_c.get("sha256") != exp_c.get("sha256"):
            mismatches.append("central_pool")
    return len(mismatches) == 0, mismatches


def _pass3_repair_count_from_plan(plan_path: Path) -> int:
    if not plan_path.is_file():
        return 0
    try:
        data = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0
    intents = data.get("intents")
    if not isinstance(intents, list):
        return 0
    n = 0
    for it in intents:
        if not isinstance(it, dict):
            continue
        if it.get("pass_id") == "pass3" and it.get("queue_pass_phase") == "repair":
            n += 1
    return n


def _lane_token_for_config(parallel: dict[str, Any], first_entry: QueueEntry | None) -> str | None:
    pt = parallel.get("parallel_track")
    if isinstance(pt, str) and pt.strip():
        return pt.strip().lower()
    if first_entry is not None:
        return effective_queue_lane(first_entry) or None
    return None


def cmd_append_entries(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    cfg = parse_queue_config(args.resolved_config)
    max_a = max_midrun_appends(cfg)
    current = int(args.current_midrun_count)
    oh = origin_dedupe_window_hours(cfg)
    if getattr(args, "origin_dedupe_window_hours", None) is not None:
        try:
            oh = float(args.origin_dedupe_window_hours)
        except (TypeError, ValueError):
            pass

    req_snap = getattr(args, "require_snapshot_json", None)
    if req_snap:
        ok_snap, miss = _verify_snapshot_for_append(
            vault_root.resolve(), qpath, Path(req_snap), cfg
        )
        if not ok_snap:
            print(
                json.dumps({"ok": False, "error": "snapshot_mismatch", "mismatches": miss}),
                file=sys.stderr,
            )
            return 2

    if args.lines_file:
        raw = Path(args.lines_file).read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "append_entries_stdin_required",
                        "hint": "Provide JSONL via stdin (pipe or heredoc) or use --lines-file PATH. "
                        "Refusing to read from an interactive empty terminal (would block).",
                    }
                ),
                file=sys.stderr,
            )
            return 1
        raw = sys.stdin.read()
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    nlines = len(lines)
    candidates: list[tuple[QueueEntry, str]] = []
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "error": f"line {i+1} invalid json: {e}"}), file=sys.stderr)
            return 1
        if not isinstance(obj, dict) or "id" not in obj or "mode" not in obj:
            print(
                json.dumps({"ok": False, "error": f"line {i+1} missing id/mode"}),
                file=sys.stderr,
            )
            return 1
        try:
            candidates.append((QueueEntry.model_validate(obj), line))
        except ValidationError as e:
            print(
                json.dumps({"ok": False, "error": f"line {i+1} invalid queue entry: {e}"}),
                file=sys.stderr,
            )
            return 1

    root = vault_root.resolve()
    first_entry = candidates[0][0] if candidates else None
    lane_tok = _lane_token_for_config(parallel, first_entry)
    hs = effective_harness_settings(root, lane_tok)

    entries_only = [c[0] for c in candidates]
    merged_entries, merge_telemetry = intra_batch_strict_merge(
        entries_only,
        enabled=hs.strict_merge_enabled,
        jaccard_threshold=hs.strict_merge_jaccard_threshold,
    )
    candidates_merged: list[tuple[QueueEntry, str]] = []
    for e in merged_entries:
        if hs.context_cost_enabled:
            g = _guidance_from_entry(e)
            tok = estimate_context_tokens(g)
            p = dict(e.params) if isinstance(e.params, dict) else {}
            p["estimated_context_tokens"] = tok
            e = e.model_copy(update={"params": p})
        raw = json.dumps(e.model_dump(mode="json"), ensure_ascii=False)
        candidates_merged.append((e, raw))
    candidates = candidates_merged
    pass3_manual = int(getattr(args, "inline_pass3_repair_count", 0) or 0)
    plan_path_arg = getattr(args, "eat_queue_run_plan", None)
    plan_path = (
        Path(plan_path_arg).resolve()
        if plan_path_arg
        else (qpath.parent / "eat_queue_run_plan.json").resolve()
    )
    pass3_from_plan = _pass3_repair_count_from_plan(plan_path)
    pass3_used = pass3_manual if pass3_manual > 0 else pass3_from_plan
    max_inline = effective_max_inline_a5b(root, lane_tok)
    inline_budget_rem = max(0, max_inline - pass3_used)

    existing = load_queue_file(qpath) if qpath.is_file() else []
    pending: list[QueueEntry] = []
    to_write: list[str] = []
    dedupe_events: list[dict[str, Any]] = []
    audit_path = qpath.parent / "prompt-queue-audit.jsonl"
    comms_path = qpath.parent / "task-handoff-comms.jsonl"
    parallel_track = _resolve_parallel_track(parallel)
    parent_run_id = str(getattr(args, "parent_run_id", "eatq-append"))
    emit_audit = getattr(args, "emit_audit", True)
    emit_intent_receipt = getattr(args, "emit_intent_receipt", True)
    emit_watcher = getattr(args, "emit_watcher_result", True)
    dry_run = getattr(args, "dry_run", False)
    use_lock = getattr(args, "use_gitforge_lock", False)
    lock_track = parallel_track if parallel_track != "-" else "default"

    if use_lock and not dry_run:
        if not acquire_gitforge_lock(root, lock_track, 30.0):
            print(json.dumps({"ok": False, "error": "gitforge_lock_not_acquired"}), file=sys.stderr)
            return 1
    try:
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        if emit_audit and not dry_run and merge_telemetry:
            for mt in merge_telemetry:
                rec_m = {
                    **mt,
                    "iso_timestamp": now_iso,
                    "parent_run_id": parent_run_id,
                }
                _append_prompt_queue_audit(audit_path, rec_m)

        for cand, raw_line in candidates:
            decision = decide_append(
                cand,
                existing,
                pending,
                origin_window_hours=oh,
            )
            oid = (cand.params or {}).get("origin_request_id") if isinstance(cand.params, dict) else None
            oid_s = oid.strip() if isinstance(oid, str) else None
            ev: dict[str, Any] = {
                "queue_entry_id": cand.id,
                "dedupe_attempted": decision.dedupe_attempted,
                "dedupe_suppressed": decision.dedupe_suppressed,
                "suppressed_by": decision.suppressed_by,
                "inline_drain_budget_remaining": inline_budget_rem,
            }
            if decision.audit_suppressed_by:
                ev["audit_suppressed_by"] = decision.audit_suppressed_by
            if decision.suppressing_entry_id:
                ev["suppressing_queue_entry_id"] = decision.suppressing_entry_id
            dedupe_events.append(ev)

            if emit_audit and not dry_run:
                rec_a: dict[str, Any] = {
                    "record_type": "a5b_enqueue_dedupe",
                    "iso_timestamp": now_iso,
                    "queue_entry_id": cand.id,
                    "dedupe_attempted": decision.dedupe_attempted,
                    "dedupe_suppressed": decision.dedupe_suppressed,
                    "suppressed_by": decision.suppressed_by,
                    "parent_run_id": parent_run_id,
                    "inline_drain_budget_remaining": inline_budget_rem,
                    "max_inline_a5b_effective": max_inline,
                    "pass3_repair_count_used": pass3_used,
                }
                if decision.audit_suppressed_by:
                    rec_a["audit_suppressed_by"] = decision.audit_suppressed_by
                if oid_s:
                    rec_a["origin_request_id"] = oid_s
                if decision.dedupe_suppressed:
                    rec_a["dedupe_suppressed_handoff_repair"] = True
                _append_prompt_queue_audit(audit_path, rec_a)

            if emit_intent_receipt and not dry_run:
                receipt = build_a5b_append_intent_receipt_row(
                    vault_root=root,
                    parent_run_id=parent_run_id,
                    entry=cand,
                    decision=decision,
                    parallel_track=parallel_track,
                    inline_drain_budget_remaining=inline_budget_rem,
                )
                append_task_handoff_jsonl(comms_path, receipt)

            if emit_watcher and not dry_run:
                trace_payload: dict[str, Any] = {
                    "source": "eat_queue_core_append_entries",
                    "record_type": "harness_append_telemetry",
                    "queue_entry_id": cand.id,
                    "parent_run_id": parent_run_id,
                    "parallel_track": parallel_track,
                    "queue_lane": effective_queue_lane(cand),
                    "dedupe_attempted": decision.dedupe_attempted,
                    "dedupe_suppressed": decision.dedupe_suppressed,
                    "suppressed_by": decision.suppressed_by,
                    "inline_drain_budget_remaining": inline_budget_rem,
                    "max_inline_a5b_effective": max_inline,
                    "pass3_repair_count_used": pass3_used,
                }
                if decision.audit_suppressed_by:
                    trace_payload["audit_suppressed_by"] = decision.audit_suppressed_by
                if hs.context_cost_enabled:
                    g = _guidance_from_entry(cand)
                    trace_payload["estimated_context_tokens"] = estimate_context_tokens(g)
                append_watcher_telemetry_line(
                    root,
                    request_id=f"harness-append-{cand.id}",
                    message="harness append_entries telemetry",
                    trace_payload=trace_payload,
                )

            if not decision.dedupe_suppressed:
                to_write.append(raw_line)
                pending.append(cand)

        n_append = len(to_write)
        if current + n_append > max_a:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "queue_midrun_append_cap",
                        "max_midrun_jsonl_appends_per_eat_queue_run": max_a,
                        "current_midrun_count": current,
                        "requested_lines": nlines,
                        "would_append_after_dedupe": n_append,
                    }
                ),
                file=sys.stderr,
            )
            return 1

        if not dry_run:
            qpath.parent.mkdir(parents=True, exist_ok=True)
            with open(qpath, "a", encoding="utf-8") as f:
                for raw_line in to_write:
                    f.write(raw_line + "\n")
            if n_append > 0:
                try:
                    write_lane_status_board(root)
                except OSError:
                    pass

        out: dict[str, Any] = {
            "ok": True,
            "dry_run": dry_run,
            "appended": n_append,
            "requested_lines": nlines,
            "suppressed_count": nlines - n_append,
            "path": str(qpath),
            "midrun_count_after": current + (0 if dry_run else n_append),
            "dedupe_events": dedupe_events,
            "strict_merge_events": merge_telemetry,
            "inline_drain_budget_remaining": inline_budget_rem,
            "max_inline_a5b_effective": max_inline,
            "pass3_repair_count_used": pass3_used,
        }
        print(json.dumps(out, indent=2))
        return 0
    finally:
        if use_lock and not dry_run:
            release_gitforge_lock(root)


def cmd_pool_sync(vault_root: Path, args: argparse.Namespace) -> int:
    from .pool_sync import read_central_pool_fanout_enabled

    if not read_central_pool_fanout_enabled(vault_root):
        print(
            json.dumps(
                {
                    "ok": True,
                    "skipped": True,
                    "reason": "central_pool_fanout_disabled",
                    "message": "Per-lane PQs only; central pool retired.",
                },
                indent=2,
            )
        )
        return 0
    lane = args.lane.strip().lower()
    target = args.target_pq
    if not target.is_absolute():
        target = (vault_root / target).resolve()
    res = hydrate_track_pq_from_pool(
        vault_root=vault_root.resolve(),
        lane_filter=lane,
        target_pq=target,
        pool_path=args.pool,
        dry_run=args.dry_run,
        strict_central_only=True if args.strict_central_only else None,
    )
    print(res.model_dump_json(indent=2))
    return 0 if res.ok else 1


def _all_tracks_config_error_json(reason: str, *, config_path: str | None = None) -> str:
    return json.dumps(
        {
            "ok": False,
            "error": reason,
            "harness_all_tracks": True,
            "parallel_mode_used": "single_chat_sequential_dual",
            **({"config_path": config_path} if config_path else {}),
        },
        indent=2,
    )


def cmd_plan_all_tracks(vault_root: Path, args: argparse.Namespace) -> int:
    """Emit eat_queue_run_plan.json for each ``parallel_execution.tracks[]`` row (sequential v1)."""
    if args.lane or args.queue or args.parallel_context_file or args.parallel_context_yaml:
        print(
            "harness plan: --all-tracks cannot be combined with --lane, --queue, "
            "--parallel-context-file, or --parallel-context-yaml",
            file=sys.stderr,
        )
        return 2
    if args.emit is not None:
        print(
            "harness plan: omit --emit when using --all-tracks (each track writes beside its PQ)",
            file=sys.stderr,
        )
        return 2
    cfg_path = args.resolved_config
    enabled, legacy, tracks = parallel_execution_tracks_enabled(cfg_path)
    if not enabled or legacy or not tracks:
        print(_all_tracks_config_error_json("dual_track_unavailable", config_path=str(cfg_path)), file=sys.stderr)
        return 1

    base_prid = args.parent_run_id or "eatq-local-all"
    run_suffix = uuid.uuid4().hex[:8]
    track_results: list[dict[str, Any]] = []
    exit_code = 0
    for track in tracks:
        lane = str(track.get("lane") or track.get("id") or "").strip().lower()
        if not lane or not validate_lane_filter_token(lane, FALLBACK_ALLOWED_LANES):
            track_results.append({"lane": lane or "?", "ok": False, "error": "invalid_lane_in_config_track"})
            exit_code = 1
            continue
        parallel = parallel_context_from_config_track(track)
        qpath, emit = resolve_queue_and_plan_paths(vault_root, queue=None, parallel=parallel)
        emit = emit.resolve()
        dlog = emit.parent / "eat-queue-decisions.jsonl"
        try:
            entries = load_queue_file(qpath)
            hs_plan = effective_harness_settings(vault_root.resolve(), lane)
            plan, decisions = build_plan(
                entries,
                f"{base_prid}-{run_suffix}-{lane}",
                lane_filter=lane,
                queue_type_order_enabled=hs_plan.queue_type_order_enabled,
                queue_type_order=hs_plan.queue_type_order,
            )
            emit_plan_json(plan, emit)
            append_decisions(dlog, decisions)
        except (OSError, ValueError) as e:
            track_results.append({"lane": lane, "ok": False, "error": str(e)})
            exit_code = 1
            continue
        track_results.append(
            {
                "lane": lane,
                "ok": True,
                "prompt_queue": _rel_vault(vault_root, qpath),
                "emit": _rel_vault(vault_root, emit),
                "decisions_log": _rel_vault(vault_root, dlog),
                "plan_intents_count": len(plan.intents) if hasattr(plan, "intents") else 0,
            }
        )
    agg = {
        "ok": exit_code == 0,
        "harness_all_tracks": True,
        "parallel_mode_used": "single_chat_sequential_dual",
        "config_path": str(cfg_path),
        "tracks": track_results,
    }
    print(json.dumps(agg, indent=2, ensure_ascii=False))
    return exit_code


def cmd_full_cycle_all_tracks(vault_root: Path, args: argparse.Namespace) -> int:
    """Run ``run_full_eat_queue_cycle`` once per Config track (sequential v1)."""
    if args.lane or args.queue or args.parallel_context_file or args.parallel_context_yaml:
        print(
            "harness full_cycle: --all-tracks cannot be combined with --lane, --queue, "
            "--parallel-context-file, or --parallel-context-yaml",
            file=sys.stderr,
        )
        return 2
    if args.emit is not None:
        print(
            "harness full_cycle: omit --emit when using --all-tracks (each track uses its bundle path)",
            file=sys.stderr,
        )
        return 2
    cfg_path = args.resolved_config
    enabled, legacy, tracks = parallel_execution_tracks_enabled(cfg_path)
    if not enabled or legacy or not tracks:
        print(_all_tracks_config_error_json("dual_track_unavailable", config_path=str(cfg_path)), file=sys.stderr)
        return 1

    cpf: bool | None = None
    if args.no_central_pool_fanout:
        cpf = False
    elif args.central_pool_fanout:
        cpf = True

    base_pr = args.parent_run_id or f"eatq-fullcycle-{uuid.uuid4().hex[:12]}"
    track_outputs: list[dict[str, Any]] = []
    exit_code = 0
    for track in tracks:
        lane = str(track.get("lane") or track.get("id") or "").strip().lower()
        if not lane or not validate_lane_filter_token(lane, FALLBACK_ALLOWED_LANES):
            track_outputs.append({"lane": lane or "?", "ok": False, "error": "invalid_lane_in_config_track"})
            exit_code = 1
            continue
        parallel = parallel_context_from_config_track(track)
        qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=None, parallel=parallel)
        emit = qpath.parent / "eat_queue_run_plan.json"
        dlog = qpath.parent / "eat-queue-decisions.jsonl"
        raw_lp = parallel.get("lane_project_id")
        lane_project_id = raw_lp.strip() if isinstance(raw_lp, str) and raw_lp.strip() else None
        try:
            result = run_full_eat_queue_cycle(
                initial_action=args.action,
                initial_profile=args.profile,
                max_passes=args.max_passes,
                strict_mode=args.strict_mode,
                vault_root=vault_root.resolve(),
                queue_path=qpath,
                plan_path=emit,
                decisions_path=dlog,
                parent_run_id=f"{base_pr}-{lane}",
                lane_filter=lane,
                apply_cleanup=args.apply_cleanup,
                central_pool_fanout=cpf,
                lane_project_id=lane_project_id,
                emit_watcher_result=getattr(args, "emit_watcher_result", False),
                config_path=args.resolved_config,
            )
        except (OSError, ValueError) as e:
            track_outputs.append({"lane": lane, "ok": False, "error": str(e)})
            exit_code = 1
            continue
        lv = result.ledger_validation
        lv_ok = lv is None or bool(getattr(lv, "ok", False))
        if not lv_ok:
            exit_code = 1
        track_outputs.append(
            {
                "lane": lane,
                "ok": lv_ok,
                "parent_run_id": result.parent_run_id,
                "prompt_queue": _rel_vault(vault_root, qpath),
                "result": json.loads(result.model_dump_json()),
            }
        )
    agg: dict[str, Any] = {
        "ok": exit_code == 0,
        "harness_all_tracks": True,
        "parallel_mode_used": "single_chat_sequential_dual",
        "config_path": str(cfg_path),
        "tracks": track_outputs,
    }
    print(json.dumps(agg, indent=2, ensure_ascii=False))
    return exit_code


def cmd_plan(vault_root: Path, args: argparse.Namespace) -> int:
    if getattr(args, "all_tracks", False):
        return cmd_plan_all_tracks(vault_root, args)
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, emit = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    if args.emit is None:
        print("harness plan: --emit is required unless --all-tracks", file=sys.stderr)
        return 2
    if args.emit:
        emit = args.emit if args.emit.is_absolute() else (vault_root / args.emit)
    dlog = args.decisions_log
    if dlog is None:
        dlog = qpath.parent / "eat-queue-decisions.jsonl"
    elif not dlog.is_absolute():
        dlog = vault_root / dlog
    lane_filter: str | None = None
    if args.lane is not None:
        token = args.lane.strip().lower()
        if not validate_lane_filter_token(token, FALLBACK_ALLOWED_LANES):
            print(f"harness plan: invalid lane {token!r}", file=sys.stderr)
            return 1
        lane_filter = token
    try:
        entries = load_queue_file(qpath)
        hs_plan = effective_harness_settings(vault_root.resolve(), lane_filter)
        plan, decisions = build_plan(
            entries,
            args.parent_run_id,
            lane_filter=lane_filter,
            queue_type_order_enabled=hs_plan.queue_type_order_enabled,
            queue_type_order=hs_plan.queue_type_order,
        )
        emit_plan_json(plan, emit)
        append_decisions(dlog, decisions)
    except (OSError, ValueError) as e:
        print(f"harness plan error: {e}", file=sys.stderr)
        return 1
    print_plan_success_summary(plan, dlog)
    if args.verbose:
        print(plan.model_dump_json(indent=2))
    return 0


def cmd_full_cycle(vault_root: Path, args: argparse.Namespace) -> int:
    """Delegate to full_cycle.run_full_eat_queue_cycle; print JSON result."""
    if getattr(args, "all_tracks", False):
        return cmd_full_cycle_all_tracks(vault_root, args)
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    emit = args.emit
    if emit is None:
        emit = qpath.parent / "eat_queue_run_plan.json"
    elif not emit.is_absolute():
        emit = vault_root / emit
    dlog = args.decisions_log
    if dlog is None:
        dlog = qpath.parent / "eat-queue-decisions.jsonl"
    elif not dlog.is_absolute():
        dlog = vault_root / dlog

    lane_filter: str | None = None
    lane_project_id: str | None = None
    if args.lane is not None:
        token = args.lane.strip().lower()
        if not validate_lane_filter_token(token, FALLBACK_ALLOWED_LANES):
            print(f"harness full_cycle: invalid lane {token!r}", file=sys.stderr)
            return 1
        lane_filter = token
    raw_lane_project_id = parallel.get("lane_project_id")
    if isinstance(raw_lane_project_id, str) and raw_lane_project_id.strip():
        lane_project_id = raw_lane_project_id.strip()

    cpf: bool | None = None
    if args.no_central_pool_fanout:
        cpf = False
    elif args.central_pool_fanout:
        cpf = True

    try:
        result = run_full_eat_queue_cycle(
            initial_action=args.action,
            initial_profile=args.profile,
            max_passes=args.max_passes,
            strict_mode=args.strict_mode,
            vault_root=vault_root.resolve(),
            queue_path=qpath,
            plan_path=emit,
            decisions_path=dlog,
            parent_run_id=args.parent_run_id,
            lane_filter=lane_filter,
            apply_cleanup=args.apply_cleanup,
            central_pool_fanout=cpf,
            lane_project_id=lane_project_id,
            emit_watcher_result=getattr(args, "emit_watcher_result", False),
            config_path=args.resolved_config,
        )
    except (OSError, ValueError) as e:
        print(f"harness full_cycle error: {e}", file=sys.stderr)
        return 1
    print(result.model_dump_json(indent=2))
    return 0


def cmd_memory_compact(vault_root: Path, args: argparse.Namespace) -> int:
    """Trim lane MEMORY.md to agent_continuity.memory_max_chars (curator upgrade stub)."""
    lane = (getattr(args, "lane", None) or "curator").strip().lower()
    parallel = resolve_parallel_context(
        vault_root,
        lane=lane,
        parallel_context_file=getattr(args, "parallel_context_file", None),
        parallel_context_yaml=getattr(args, "parallel_context_yaml", None),
        config_path=getattr(args, "resolved_config", None),
    )
    bundle = Path(vault_root) / (parallel.get("technical_bundle_root") or f".technical/parallel/{lane}")
    memory_path = bundle / "MEMORY.md"
    max_chars = 8000
    cfg_path = getattr(args, "resolved_config", None)
    if cfg_path and Path(cfg_path).is_file():
        try:
            raw = Path(cfg_path).read_text(encoding="utf-8", errors="replace")
            if "memory_max_chars:" in raw:
                for line in raw.splitlines():
                    if "memory_max_chars:" in line:
                        max_chars = int(line.split(":", 1)[1].strip())
                        break
        except (ValueError, OSError):
            pass
    trimmed = False
    before = 0
    after = 0
    if memory_path.is_file():
        text = memory_path.read_text(encoding="utf-8", errors="replace")
        before = len(text)
        if before > max_chars:
            text = text[-max_chars:]
            memory_path.write_text(text, encoding="utf-8")
            trimmed = True
        after = len(text)
    out = {
        "ok": True,
        "cmd": "memory_compact",
        "lane": lane,
        "memory_path": str(memory_path.relative_to(vault_root)),
        "max_chars": max_chars,
        "before_chars": before,
        "after_chars": after,
        "trimmed": trimmed,
    }
    print(json.dumps(out))
    return 0


def cmd_mcp_postedit_validate(vault_root: Path, args: argparse.Namespace) -> int:
    """Track C — post-MCP validation receipt → maintenance + lane mirror jsonl."""
    from .weave.mcp_postedit_validate import run_mcp_postedit_validate

    try:
        out = run_mcp_postedit_validate(
            vault_root,
            lane=str(getattr(args, "lane", "") or "").strip(),
            project_id=str(getattr(args, "project_id", "") or "").strip(),
            engine_adapter=str(getattr(args, "engine_adapter", "") or "").strip(),
            milestone_id=str(getattr(args, "milestone_id", "") or "").strip(),
            repo_root=getattr(args, "repo_root", None),
            status=str(getattr(args, "status", "pass") or "pass"),
            message=str(getattr(args, "message", "") or ""),
            debug_output=getattr(args, "debug_output", None),
            smoke=bool(getattr(args, "smoke", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_memory_pass(vault_root: Path, args: argparse.Namespace) -> int:
    """Merge receipt into continuity/MEMORY; run skill-gap scan."""
    from .continuity_bridge import run_memory_pass

    lane = (getattr(args, "lane", None) or "curator").strip().lower()
    receipt_path = getattr(args, "receipt_json", None)
    receipt: dict[str, Any] | None = None
    if receipt_path:
        try:
            receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
            return 1
    try:
        out = run_memory_pass(vault_root, lane=lane, receipt=receipt)
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_queue_neighbor_prep(vault_root: Path, args: argparse.Namespace) -> int:
    """Pre-pack semantic_neighbors for curator PQ lines with source_file."""
    lane = str(getattr(args, "lane", None) or "curator")
    try:
        out = write_queue_neighbor_prep(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            lane=lane,
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_nav_color_refresh(vault_root: Path, args: argparse.Namespace) -> int:
    """Build or patch .technical/visual/nav-color-index.jsonl."""
    paths = None
    raw = getattr(args, "paths", None)
    if raw:
        paths = [p.strip() for p in str(raw).split(",") if p.strip()]
    try:
        out = write_nav_color_index(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            paths=paths,
            populate_vault=bool(getattr(args, "populate_vault", False)),
            use_pq_defaults=bool(getattr(args, "use_pq_defaults", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1



def cmd_syncthing_sync_policy(vault_root: Path, args: argparse.Namespace) -> int:
    out = run_syncthing_sync_policy(
        vault_root,
        force_bulk_unpause=bool(getattr(args, "force_bulk_unpause", False)),
        dry_run=bool(getattr(args, "dry_run", False)),
    )
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1

def cmd_l4_offline_replay(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.adaptive_policy import run_offline_replay

    try:
        out = run_offline_replay(vault_root)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_l4_bandit_update(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.adaptive_policy import bandit_update

    try:
        out = bandit_update(vault_root)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_l4_propose_promotion(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.adaptive_policy import propose_policy_promotion

    try:
        out = propose_policy_promotion(vault_root)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) else 1


def cmd_l5_arm(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l5_sandbox import arm_l5_sandbox

    days = getattr(args, "days", None)
    try:
        out = arm_l5_sandbox(
            vault_root,
            days=int(days) if days is not None else None,
            force=bool(getattr(args, "force", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_l5_kill(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l5_sandbox import kill_l5_sandbox

    out = kill_l5_sandbox(vault_root, reason=str(getattr(args, "reason", "operator_kill") or "operator_kill"))
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_l5_release(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l5_sandbox import release_l5_kill

    out = release_l5_kill(vault_root)
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_l5_status(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l5_sandbox import l5_status

    print(json.dumps(l5_status(vault_root), indent=2))
    return 0


def cmd_l5_sandbox_tick(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l5_sandbox import run_sandbox_tick

    try:
        out = run_sandbox_tick(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            force_eat=bool(getattr(args, "force_eat", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) and not out.get("downgraded") else 1


def cmd_lane_status_board(vault_root: Path, args: argparse.Namespace) -> int:
    """Refresh Ingest/Weave-Status-Board.md (factory-first operator surface)."""
    try:
        out = write_lane_status_board(vault_root)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) else 1


cmd_weave_status_board = cmd_lane_status_board


def cmd_trinity_pack_preview(vault_root: Path, args: argparse.Namespace) -> int:
    """Wave 2.5c — emit trinity_pack YAML for a card (envelope preview)."""
    from .weave.trinity_pack import build_trinity_pack, format_trinity_pack_yaml, resolve_trinity_id

    tid = resolve_trinity_id(
        vault_root,
        trinity_id=getattr(args, "trinity_id", None),
        concept=getattr(args, "concept", None),
        lane=getattr(args, "lane", None),
    )
    if not tid:
        print(json.dumps({"ok": False, "error": "trinity_id_unresolved"}), file=sys.stderr)
        return 1
    try:
        pack = build_trinity_pack(
            vault_root,
            tid,
            concept=getattr(args, "concept", None),
        )
        yaml_text = "\n".join(format_trinity_pack_yaml(pack))
    except (OSError, ValueError, FileNotFoundError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    out = {"ok": True, "trinity_id": tid, "yaml": yaml_text, "pack": pack}
    print(json.dumps(out, indent=2))
    return 0


def cmd_trinity_align(vault_root: Path, args: argparse.Namespace) -> int:
    """Wave 2.5d — goal/impetus/touch align + pilot disconnect rules."""
    from .weave.trinity_align import run_trinity_align

    ids_raw = getattr(args, "trinity_id", None)
    trinity_ids = [s.strip() for s in str(ids_raw).split(",") if s.strip()] if ids_raw else None
    try:
        out = run_trinity_align(
            vault_root,
            trinity_ids=trinity_ids,
            pilot_only=not bool(getattr(args, "all_cards", False)),
            update_meta=not bool(getattr(args, "no_meta_update", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) or out.get("skipped") else 1


def cmd_trinity_transcript_route(vault_root: Path, args: argparse.Namespace) -> int:
    """Plan index + transcript scout for Trinity conceptual polish."""
    from .weave.trinity_transcript_routing import (
        GOVERNANCE_SET2_LOCKED_IDS,
        HARNESS_SPINE_IDS,
        run_transcript_routing_pilot,
    )

    troot = getattr(args, "transcript_root", None)
    transcript_root = Path(troot).expanduser() if troot else None
    tid = getattr(args, "trinity_id", None) or None
    ids = [tid] if tid else list(HARNESS_SPINE_IDS) + list(GOVERNANCE_SET2_LOCKED_IDS)

    try:
        out = run_transcript_routing_pilot(
            vault_root,
            trinity_ids=ids,
            transcript_root=transcript_root,
            rebuild_index=not bool(getattr(args, "no_rebuild_index", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_spine_cascade(vault_root: Path, args: argparse.Namespace) -> int:
    """Spine cascade — polish stub Conceptual from locked production corpus."""
    from .weave.trinity_spine_cascade import run_trinity_spine_cascade

    try:
        out = run_trinity_spine_cascade(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            stamp=getattr(args, "stamp", None),
            trinity_id=getattr(args, "trinity_id", None) or None,
            write_in_place=bool(getattr(args, "write_in_place", False)),
            extend_only=bool(getattr(args, "extend_only", False)),
            fix_legs=bool(getattr(args, "fix_legs", False)),
            write_packs=not bool(getattr(args, "no_packs", False)),
            governance_stubs_only=bool(getattr(args, "governance_stubs_only", False)),
            proposal_stamp=getattr(args, "proposal_stamp", None) or None,
            include_unlocked_production=bool(
                getattr(args, "include_unlocked_production", False)
            ),
            force_machine_voice=bool(getattr(args, "force_machine_voice", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_promote_proposals(vault_root: Path, args: argparse.Namespace) -> int:
    """Promote reviewed stubs → component-proposals/ (provisional; not locked)."""
    from .weave.trinity_promote import run_trinity_promote_proposals

    try:
        out = run_trinity_promote_proposals(
            vault_root,
            stamp=getattr(args, "stamp", None) or "I-did-it-right",
            dry_run=bool(getattr(args, "dry_run", False)),
            force=bool(getattr(args, "force", False)),
            trinity_id=getattr(args, "trinity_id", None) or None,
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_lock_card(vault_root: Path, args: argparse.Namespace) -> int:
    """Operator gate — provisional component-proposals → locked components/."""
    from .weave.trinity_promote import run_trinity_lock_card

    tid = getattr(args, "trinity_id", None) or ""
    if not tid.strip():
        print(json.dumps({"ok": False, "error": "trinity_id required"}), file=sys.stderr)
        return 1
    from .weave.trinity_dual_lock import operator_mutation_ctx

    try:
        out = run_trinity_lock_card(
            vault_root,
            tid.strip(),
            dry_run=bool(getattr(args, "dry_run", False)),
            lock_kind=str(getattr(args, "lock_kind", None) or "full"),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_catchup_sweep(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 3 — partition-aware catch-up sweep (bones / bridges / provisionals)."""
    from .weave.trinity_catchup_sweep import run_trinity_catchup_sweep

    try:
        curate_non_core = None
        if getattr(args, "no_curate", False):
            curate_non_core = False
        elif getattr(args, "curate_non_core", False):
            curate_non_core = True
        out = run_trinity_catchup_sweep(
            vault_root,
            include_provisional=bool(getattr(args, "include_provisional", False)),
            maintenance_only=not bool(getattr(args, "all_cards", False)),
            dry_run=bool(getattr(args, "dry_run", False)),
            queue_actions=not bool(getattr(args, "no_queue", False)),
            max_escalations=getattr(args, "max_escalations", None),
            write_report=not bool(getattr(args, "no_report", False)),
            curate_non_core=curate_non_core,
        )
    except (OSError, ValueError, FileNotFoundError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    if out.get("skipped"):
        return 0
    return 0 if out.get("ok") else 1


def cmd_trinity_bridge_consolidate(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 7 — merge provisional bridges sharing tunnel_via into one locked bridge."""
    from .weave.trinity_bridge_consolidate import run_trinity_bridge_consolidate

    tv = str(getattr(args, "tunnel_via", None) or "").strip()
    if not tv:
        print(json.dumps({"ok": False, "error": "tunnel_via required"}), file=sys.stderr)
        return 1
    try:
        out = run_trinity_bridge_consolidate(
            vault_root,
            tunnel_via=tv,
            output_id=getattr(args, "output_id", None),
            dry_run=bool(getattr(args, "dry_run", False)),
            force=bool(getattr(args, "force", False)),
            lock_kind=str(getattr(args, "lock_kind", None) or "full"),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_assess_trinity_card_backlog(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 7 — ranked Trinity backlog (drift × usage)."""
    from .weave.trinity_card_backlog import assess_trinity_card_backlog

    try:
        out = assess_trinity_card_backlog(
            vault_root,
            maintenance_only=not bool(getattr(args, "all_cards", False)),
            top_n=getattr(args, "top_n", None),
            write_report=not bool(getattr(args, "no_report", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_stamp_core_cards(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 8 — stamp maintenance core YAMLs (lock_kind, system_mutable, doctrine)."""
    from .weave.trinity_vault_compensation import run_trinity_stamp_core_cards

    ids_raw = getattr(args, "trinity_id", None)
    trinity_ids = [s.strip() for s in str(ids_raw).split(",") if s.strip()] if ids_raw else None
    try:
        out = run_trinity_stamp_core_cards(
            vault_root,
            trinity_ids=trinity_ids,
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_expand_self(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 14 — expand_self scoped delta wrap."""
    from .weave.trinity_expand_self import parse_scope_ids, run_expand_self_delta_wrap

    scope = parse_scope_ids(getattr(args, "scope_ids", None))
    try:
        out = run_expand_self_delta_wrap(
            vault_root,
            scope_ids=scope or None,
            corps_cluster=getattr(args, "corps_cluster", None),
            operator_override_scope=bool(getattr(args, "operator_override_scope", False)),
            operator_mutation_on_core=bool(getattr(args, "operator_mutation", False)),
            dry_run=bool(getattr(args, "dry_run", False)),
            skip_align=bool(getattr(args, "skip_align", False)),
            skip_corps=bool(getattr(args, "skip_corps", False)),
            skip_enforce=bool(getattr(args, "skip_enforce", False)),
            skip_unclog=bool(getattr(args, "skip_unclog", False)),
            skip_observe=bool(getattr(args, "skip_observe", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    op = out.get("operator_outcome") or {}
    summary = op.get("summary")
    if summary:
        print(f"\n=== trinity_expand_self ===\n{summary}\n", file=sys.stderr)
        for step in op.get("next_steps") or []:
            print(f"  • {step}", file=sys.stderr)
        print("", file=sys.stderr)
    print(json.dumps(out, indent=2))
    if bool(out.get("dry_run")):
        return 0
    if not op.get("cycle_ok", True):
        return 1
    if op.get("pass_gate_ok"):
        return 0
    return 2


def cmd_trinity_weave_self_wrap(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 9+10 — align → unclog → corps sweep → enforce → observe."""
    if bool(getattr(args, "expand_self", False)):
        from .weave.trinity_expand_self import parse_scope_ids, run_expand_self_delta_wrap

        scope = parse_scope_ids(getattr(args, "scope_ids", None))
        try:
            out = run_expand_self_delta_wrap(
                vault_root,
                scope_ids=scope or None,
                corps_cluster=getattr(args, "corps_cluster", None),
                operator_override_scope=bool(getattr(args, "operator_override_scope", False)),
                operator_mutation_on_core=bool(
                    getattr(args, "operator_mutation", False)
                    or getattr(args, "operator_mutation_on_core", False)
                ),
                dry_run=bool(getattr(args, "dry_run", False)),
                skip_align=bool(getattr(args, "skip_align", False)),
                skip_corps=bool(getattr(args, "skip_corps", False)),
                skip_enforce=bool(getattr(args, "skip_enforce", False)),
                skip_unclog=bool(getattr(args, "skip_unclog", False)),
                skip_observe=bool(getattr(args, "skip_observe", False)),
                write_report=not bool(getattr(args, "no_report", False)),
            )
        except (OSError, ValueError) as e:
            print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
            return 1
    else:
        from .weave.trinity_weave_self_wrap import run_trinity_weave_self_wrap

        try:
            out = run_trinity_weave_self_wrap(
                vault_root,
                dry_run=bool(getattr(args, "dry_run", False)),
                skip_align=bool(getattr(args, "skip_align", False)),
                skip_enforce=bool(getattr(args, "skip_enforce", False)),
                skip_unclog=bool(getattr(args, "skip_unclog", False)),
                skip_corps=bool(getattr(args, "skip_corps", False)),
                skip_observe=bool(getattr(args, "skip_observe", False)),
                operator_mutation_on_core=bool(
                    getattr(args, "operator_mutation", False)
                    or getattr(args, "operator_mutation_on_core", False)
                ),
                write_graph=not bool(getattr(args, "no_graph", False)),
                write_report=not bool(getattr(args, "no_report", False)),
                corps_cluster=getattr(args, "corps_cluster", None),
                corps_full_corpus=True if getattr(args, "full_corpus", False) else None,
                corps_sample_only=bool(getattr(args, "corps_sample_only", False)),
                corps_max_laps=getattr(args, "max_laps", None),
                corps_max_llm_laps=getattr(args, "max_llm_laps", None),
                corps_auto_repair=False if getattr(args, "no_auto_repair", False) else None,
                corps_llm_repair=True if getattr(args, "enable_llm_repair", False) else None,
                corps_llm_repair_force=bool(getattr(args, "llm_repair_force", False)),
                corps_speed_mode=getattr(args, "speed_mode", None),
                regenerate_complete=bool(getattr(args, "regenerate_complete", False)),
                meta_lens_force_align=bool(getattr(args, "meta_lens_force_align", False)),
                host_weld_bootstrap_all=bool(getattr(args, "host_weld_bootstrap_all", False)),
            )
        except (OSError, ValueError) as e:
            print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
            return 1
    op = out.get("operator_outcome") or {}
    summary = op.get("summary")
    if summary:
        print(f"\n=== trinity_weave_self_wrap ===\n{summary}\n", file=sys.stderr)
        for step in op.get("next_steps") or []:
            print(f"  • {step}", file=sys.stderr)
        print("", file=sys.stderr)
    print(json.dumps(out, indent=2))
    if bool(out.get("dry_run")):
        return 0
    if not op.get("cycle_ok", True):
        return 1
    if op.get("pass_gate_ok"):
        return 0
    return 2


def cmd_trinity_llm_repair_trial(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 10c — scoped LLM T1 trial (balance profile + corps-cluster scope)."""
    from .weave.corps_llm_repair import assess_llm_repair_trial, run_llm_repair_trial

    cluster = getattr(args, "corps_cluster", None) or getattr(args, "cluster", None)
    if not cluster:
        print(json.dumps({"ok": False, "error": "cluster_required (--corps-cluster)"}))
        return 1
    speed_mode = str(getattr(args, "speed_mode", None) or "balance")
    dry_run = bool(getattr(args, "dry_run", False))
    assess = bool(getattr(args, "assess", False))
    try:
        if assess:
            out = assess_llm_repair_trial(
                vault_root,
                cluster=cluster,
                speed_mode=speed_mode,
                dry_run=True,
            )
        else:
            out = run_llm_repair_trial(
                vault_root,
                cluster=cluster,
                speed_mode=speed_mode,
                trinity_id=getattr(args, "trinity_id", None),
                dry_run=dry_run,
                write_artifact=not dry_run,
                trial_weaken_id=getattr(args, "trial_weaken_id", None),
                ensure_fixture=bool(getattr(args, "ensure_fixture", False)),
                restore_after=bool(getattr(args, "restore_after", False)),
            )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) else 1


def cmd_trinity_knob_parity(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 16 — factory × knob-option parity matrix proofs."""
    from .weave.trinity_knob_parity import run_knob_parity_proofs

    try:
        out = run_knob_parity_proofs(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            write_artifact=not bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_honesty_anchor(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 16 — honesty anchor claim-tier matrix proofs."""
    from .weave.trinity_honesty_anchor import run_honesty_anchor_proofs

    try:
        out = run_honesty_anchor_proofs(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            write_artifact=not bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_stub_honesty_fold(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 16b — bootstrap stub honesty invariants + closure audit."""
    from .weave.stub_honesty import activate_stub_honesty_invariants, run_stub_honesty_audit

    try:
        out: dict[str, Any] = {}
        if bool(getattr(args, "bootstrap", True)):
            out["fold"] = activate_stub_honesty_invariants(vault_root)
        out["audit"] = run_stub_honesty_audit(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            write_artifact=not bool(getattr(args, "dry_run", False)),
            trace_open=not bool(getattr(args, "dry_run", False)),
        )
        out["ok"] = bool(out.get("audit", {}).get("ok")) and (
            out.get("fold", {}).get("ok", True) if "fold" in out else True
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_integration_vet(vault_root: Path, args: argparse.Namespace) -> int:
    """Read-only Trinity integration vet — charter, honesty, stub, operator path, runtime contract."""
    from .weave.harness_runtime_contract import (
        run_operator_path_conduct,
        run_runtime_contract_parity,
    )
    from .weave.stub_honesty import run_stub_honesty_audit
    from .weave.trinity_core_charter_audit import run_core_charter_audit
    from .weave.trinity_honesty_anchor import run_honesty_anchor_proofs

    dry = bool(getattr(args, "dry_run", False))
    report: dict[str, Any] = {"phase": "trinity_integration_vet", "dry_run": dry, "steps": {}}

    try:
        report["steps"]["core_charter"] = run_core_charter_audit(
            vault_root, write_artifact=not dry
        )
        report["steps"]["honesty_anchor"] = run_honesty_anchor_proofs(
            vault_root, dry_run=dry, write_artifact=not dry
        )
        report["steps"]["stub_honesty"] = run_stub_honesty_audit(
            vault_root,
            dry_run=dry,
            write_artifact=not dry,
            trace_open=not dry,
        )
        report["steps"]["runtime_contract_parity"] = run_runtime_contract_parity(vault_root)
        report["steps"]["operator_path_conduct"] = run_operator_path_conduct(vault_root)
        charter_ok = all(
            bool((report["steps"].get(k) or {}).get("ok"))
            for k in ("core_charter", "honesty_anchor", "stub_honesty")
        )
        integration_ok = all(
            bool((report["steps"].get(k) or {}).get("ok"))
            for k in ("runtime_contract_parity", "operator_path_conduct")
        )
        report["integration_ok"] = integration_ok
        report["ok"] = charter_ok and integration_ok
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e), "partial": report}, indent=2), file=sys.stderr)
        return 1

    if not dry:
        from datetime import datetime, timezone

        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_path = vault_root / ".technical/weave/validation" / f"trinity-integration-vet-{stamp}.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["artifact_path"] = str(out_path.relative_to(vault_root))

    print(json.dumps(report, indent=2))
    return 0 if report.get("ok") else 1


def cmd_trinity_redesign_factory(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 16 — redesign_factory A/B structural compare (no auto-deprecate)."""
    from .weave.trinity_redesign_factory import run_redesign_factory

    legacy = getattr(args, "legacy_factory_id", None) or "queue_dispatch"
    candidate = getattr(args, "candidate_factory_id", None) or "queue_dispatch_v2"
    matrix_raw = getattr(args, "speed_mode_matrix", None) or ""
    speed_modes = tuple(x.strip() for x in str(matrix_raw).split(",") if x.strip()) or None

    try:
        out = run_redesign_factory(
            vault_root,
            legacy_factory_id=legacy,
            candidate_factory_id=candidate,
            ab_mode=str(getattr(args, "ab_mode", "parallel") or "parallel"),
            speed_mode_matrix=speed_modes,
            operator_deprecate_ack=bool(getattr(args, "operator_deprecate_ack", False)),
            dry_run=bool(getattr(args, "dry_run", False)),
            write_artifact=not bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_usage_proven(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 15 — assess or stamp usage_proven earned freeze."""
    from .weave.trinity_usage_proven import (
        assess_usage_proven_batch,
        run_usage_proven_report,
        stamp_usage_proven,
        unfreeze_usage_proven,
    )

    tid = getattr(args, "trinity_id", None)
    dry_run = bool(getattr(args, "dry_run", False))
    try:
        if getattr(args, "unfreeze", False):
            if not tid:
                print(json.dumps({"ok": False, "error": "trinity_id required for --unfreeze"}))
                return 1
            out = unfreeze_usage_proven(
                vault_root,
                tid,
                dry_run=dry_run,
                operator_override=True,
            )
        elif getattr(args, "stamp", False):
            if not tid:
                print(json.dumps({"ok": False, "error": "trinity_id required for --stamp"}))
                return 1
            out = stamp_usage_proven(
                vault_root,
                tid,
                dry_run=dry_run,
                operator_force=bool(getattr(args, "operator_force", False)),
            )
        elif getattr(args, "assess", False):
            ids = [tid] if tid else None
            out = assess_usage_proven_batch(
                vault_root,
                trinity_ids=ids,
                stamp_ready=bool(getattr(args, "stamp_ready", False)),
                dry_run=dry_run,
            )
        else:
            out = run_usage_proven_report(vault_root, write_artifact=True)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) else 1


def cmd_trinity_conduct_repair_apply_trial(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 10g — bounded conduct repair apply trial."""
    from .weave.corps_conduct_repair_apply import run_conduct_repair_apply_trial

    try:
        out = run_conduct_repair_apply_trial(
            vault_root,
            trinity_id=getattr(args, "trinity_id", None),
            max_apply=getattr(args, "max_apply", None),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_type2_verify(vault_root: Path, args: argparse.Namespace) -> int:
    """Type-2 verify — full-corpus self-wrap without regenerate-complete."""
    from .weave.trinity_type2_verify import run_type2_verify

    try:
        out = run_type2_verify(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            skip_observe=bool(getattr(args, "skip_observe", False)),
            write_artifact=not bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_llm_repair_trial_gate(vault_root: Path, args: argparse.Namespace) -> int:
    """Alternative C — LLM repair trial assess + fixture trials + cutover gate."""
    from .weave.trinity_llm_repair_trial_gate import run_llm_repair_trial_track

    try:
        out = run_llm_repair_trial_track(
            vault_root,
            cluster=getattr(args, "corps_cluster", None) or "harness_*",
            speed_mode=str(getattr(args, "speed_mode", None) or "balance"),
            run_fixture_trials=not bool(getattr(args, "skip_fixtures", False)),
            write_artifact=not bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_core_charter_audit(vault_root: Path, args: argparse.Namespace) -> int:
    """Alternative A — maintenance core vs finalized meta (read-only)."""
    from .weave.trinity_core_charter_audit import run_core_charter_audit

    try:
        out = run_core_charter_audit(
            vault_root,
            write_artifact=not bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_roadmap_organize_paths(vault_root: Path, args: argparse.Namespace) -> int:
    """Repath flat roadmap notes into canonical nested folders (content-preserving)."""
    from .weave.roadmap.roadmap_repath_organize import organize_roadmap_paths
    from .weave.roadmap.roadmap_path_resolver import scan_structural_path_violations

    project_id = str(getattr(args, "project_id", "") or "").strip()
    if not project_id:
        print(json.dumps({"ok": False, "error": "project_id_required"}), file=sys.stderr)
        return 1
    dry_run = bool(getattr(args, "dry_run", False))
    if getattr(args, "scan_only", False):
        rows = scan_structural_path_violations(vault_root, project_id)
        print(json.dumps({"ok": True, "violations": rows, "count": len(rows)}, indent=2))
        return 0
    try:
        out = organize_roadmap_paths(vault_root, project_id, dry_run=dry_run)
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_roadmap_clean_nav(vault_root: Path, args: argparse.Namespace) -> int:
    """Fix secondary Dataview scopes and minor roadmap nav hygiene."""
    from .weave.roadmap.roadmap_nav_clean import clean_roadmap_navigation

    project_id = str(getattr(args, "project_id", "") or "").strip()
    if not project_id:
        print(json.dumps({"ok": False, "error": "project_id_required"}), file=sys.stderr)
        return 1
    try:
        out = clean_roadmap_navigation(
            vault_root, project_id, dry_run=bool(getattr(args, "dry_run", False))
        )
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_graduation_evaluator(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 17 — evidence-gated graduation (trial→global promotion matrix)."""
    from .schedule_config import load_schedule_planes_config
    from .schedule_state import load_schedule_state
    from .weave.trinity_graduation_evaluator import run_graduation_evaluator

    try:
        cfg = load_schedule_planes_config(vault_root)
        state = load_schedule_state(vault_root)
        out = run_graduation_evaluator(
            vault_root,
            cfg,
            maintain_wrap_streak=int(state.get("maintain_wrap_streak") or 0),
            apply=bool(getattr(args, "apply", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_host_weld_sync(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 13 — surgical host-weld/live sync from locked meta."""
    from .weave.trinity_host_weld_sync import run_host_weld_sync

    try:
        out = run_host_weld_sync(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            full_corpus=True,
            bootstrap_all=bool(getattr(args, "host_weld_bootstrap_all", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_apply_card_identity_doctrine(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.trinity_card_11a import apply_card_identity_doctrine

    try:
        out = apply_card_identity_doctrine(vault_root, dry_run=bool(getattr(args, "dry_run", False)))
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_corpus_restore_from_archive(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.trinity_corpus_restore import restore_cards_from_archive

    try:
        out = restore_cards_from_archive(
            vault_root,
            stamp=getattr(args, "stamp", None),
            dry_run=bool(getattr(args, "dry_run", False)),
            target=str(getattr(args, "target", "proposals")),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_card_identity_status(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.trinity_card_11a import load_11a_status

    out = load_11a_status(vault_root)
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_corps_overnight_batch(vault_root: Path, args: argparse.Namespace) -> int:
    """Overnight corps batches — offset pagination, resilient writes."""
    from .weave.corps_overnight_batch import run_corps_overnight_batches

    try:
        out = run_corps_overnight_batches(
            vault_root,
            start_offset=getattr(args, "start_offset", None),
            batch_size=getattr(args, "batch_size", None),
            stop_on_write_error=bool(getattr(args, "stop_on_write_error", False)),
            auto_smoke_tests=not bool(getattr(args, "no_auto_smoke_tests", False)),
            write_status=not bool(getattr(args, "no_status_file", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2, default=str))
    return 0 if out.get("ok") else 1


def cmd_trinity_provisional_corps_sweep(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 10 — provisional corps sweep + nerve test."""
    from .weave.trinity_provisional_corps_sweep import run_trinity_provisional_corps_sweep

    try:
        out = run_trinity_provisional_corps_sweep(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            cluster=getattr(args, "cluster", None),
            apply_hygiene=True if getattr(args, "apply_hygiene", False) else None,
            nerve_test_only=bool(getattr(args, "nerve_test_only", False)),
            skip_sweep=bool(getattr(args, "skip_sweep", False)),
            skip_nerve_test=bool(getattr(args, "skip_nerve_test", False)),
            full_corpus=bool(getattr(args, "full_corpus", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_phase8_vault_compensation(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 8 — full vault compensation (stamp, D stubs, harness retier, touch, board smoke)."""
    from .weave.trinity_vault_compensation import run_phase8_vault_compensation

    try:
        out = run_phase8_vault_compensation(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            skip_touch_refresh=bool(getattr(args, "skip_touch_refresh", False)),
            skip_board_smoke=bool(getattr(args, "skip_board_smoke", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_boundary_audit(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 0 — read-only component/bridge boundary overlap audit."""
    from .weave.trinity_boundary_audit import run_trinity_boundary_audit

    ids_raw = getattr(args, "trinity_id", None)
    trinity_ids = [s.strip() for s in str(ids_raw).split(",") if s.strip()] if ids_raw else None
    try:
        out = run_trinity_boundary_audit(
            vault_root,
            partition=str(getattr(args, "partition", None) or "maintenance"),
            trinity_ids=trinity_ids,
            write_report=not bool(getattr(args, "no_report", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_card_generate(vault_root: Path, args: argparse.Namespace) -> int:
    """Wave 3 — discover + draft Trinity cards to proposals folder (no lock stamps)."""
    from .weave.trinity_card_generate import run_trinity_card_generate

    try:
        out = run_trinity_card_generate(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            include_locked=bool(getattr(args, "include_locked", False)),
            stamp=getattr(args, "stamp", None),
            wide_net=not bool(getattr(args, "narrow", False)),
            skip_rule_orphans=bool(getattr(args, "skip_rule_orphans", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_trinity_touch_refresh(vault_root: Path, args: argparse.Namespace) -> int:
    """Wave 2.5b — refresh Trinity card touch hashes; propose behavior_signals."""
    from .weave.trinity_dual_lock import operator_mutation_ctx
    from .weave.trinity_touch_refresh import run_trinity_touch_refresh

    ids_raw = getattr(args, "trinity_id", None)
    trinity_ids = [s.strip() for s in str(ids_raw).split(",") if s.strip()] if ids_raw else None
    if trinity_ids is None and bool(getattr(args, "maintenance_set", False)):
        from .weave.trinity_partition import load_maintenance_trinity_ids

        trinity_ids = list(load_maintenance_trinity_ids(vault_root).all)
    token = operator_mutation_ctx.set(bool(getattr(args, "operator_mutation", False)))
    try:
        out = run_trinity_touch_refresh(
            vault_root,
            trinity_ids=trinity_ids,
            dry_run=bool(getattr(args, "dry_run", False)),
            apply_behavior_signals=bool(getattr(args, "apply_behavior_signals", False)),
            pilot_only=not bool(getattr(args, "all_cards", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    finally:
        operator_mutation_ctx.reset(token)
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) or out.get("skipped") else 1

def cmd_pseudo_clock_tick(vault_root: Path, args: argparse.Namespace) -> int:
    """Weave/harness background heartbeat — evaluate thresholds and run housekeeping."""
    return _cmd_schedule_tick_impl(vault_root, args)


def cmd_schedule_tick(vault_root: Path, args: argparse.Namespace) -> int:
    """Phase 17 schedule planes — listener / scheduled / reactive / graduation."""
    return _cmd_schedule_tick_impl(vault_root, args)


def _cmd_schedule_tick_impl(vault_root: Path, args: argparse.Namespace) -> int:
    inc = getattr(args, "increment_eat", False)
    pq_c = int(getattr(args, "pq_consumed", 0) or 0)
    try:
        out = run_schedule_tick(
            vault_root,
            config_path=getattr(args, "resolved_config", None),
            increment_eat=inc,
            pq_consumed=pq_c,
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) else 1


def cmd_vault_scan(vault_root: Path, args: argparse.Namespace) -> int:
    """Write Watcher-Advisory.md; optional headless-eat signal file."""
    write_signal = None
    if getattr(args, "write_signal", None) is True:
        write_signal = True
    elif getattr(args, "no_write_signal", False):
        write_signal = False
    try:
        out = vault_scan(vault_root, write_signal=write_signal)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_skill_gap_scan(vault_root: Path, args: argparse.Namespace) -> int:
    lane = str(getattr(args, "lane", "curator") or "curator")
    try:
        out = scan_and_stub(vault_root, lane=lane)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_maintenance_eat(vault_root: Path, args: argparse.Namespace) -> int:
    from .maintenance_handlers import process_maintenance_queue
    from .lane_status_board import write_lane_status_board

    try:
        out = process_maintenance_queue(
            vault_root,
            max_entries=int(getattr(args, "max_entries", 5) or 5),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
        if not getattr(args, "dry_run", False):
            write_lane_status_board(vault_root)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_implementation_eat(vault_root: Path, args: argparse.Namespace) -> int:
    from .layer1_implementation import run_layer1_implementation_pass
    from .lane_status_board import write_lane_status_board

    lane = str(getattr(args, "lane", "godot") or "godot").strip().lower()
    try:
        if bool(getattr(args, "replay_seats", False)):
            from .weave.factory.factory_lane_recovery import replay_factory_lane_by_job_id

            job_id = str(getattr(args, "job_id", "") or "").strip()
            if not job_id:
                print(json.dumps({"ok": False, "error": "job_id required with --replay-seats"}, indent=2))
                return 1
            out = replay_factory_lane_by_job_id(
                vault_root,
                lane,
                job_id,
                agent_log_path=getattr(args, "agent_log", None),
                complete_if_ok=not bool(getattr(args, "seats_only", False)),
            )
        else:
            out = run_layer1_implementation_pass(
                vault_root,
                lane,
                max_entries=int(getattr(args, "max_entries", 1) or 1),
                dry_run=bool(getattr(args, "dry_run", False)),
                skip_agent=bool(getattr(args, "skip_agent", False)),
                skip_preflight=bool(getattr(args, "skip_preflight", False)),
                agent_log_path=getattr(args, "agent_log", None),
                resume_from=getattr(args, "resume_from", None),
            )
        if not getattr(args, "dry_run", False):
            write_lane_status_board(vault_root)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_warning_ledger_rollup(vault_root: Path, args: argparse.Namespace) -> int:
    from .warning_ledger import rollup_warnings_to_maintenance

    try:
        out = rollup_warnings_to_maintenance(vault_root)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_ghost_skill_audit(vault_root: Path, args: argparse.Namespace) -> int:
    from .ghost_skill_audit import run_ghost_skill_audit
    from .lane_clock import record_lane_event

    append_pq = not bool(getattr(args, "no_append", False))
    try:
        out = run_ghost_skill_audit(vault_root, append_pq=append_pq, source="harness_cli")
        record_lane_event(vault_root, "maintenance", "ghost_audit", counter="ghost_audits")
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_record_little_val_block(vault_root: Path, args: argparse.Namespace) -> int:
    from .memory_gap_hooks import record_little_val_hard_block

    try:
        out = record_little_val_hard_block(
            vault_root,
            origin_lane=str(getattr(args, "origin_lane", "curator") or "curator"),
            primary_code=str(getattr(args, "primary_code", "") or ""),
            report_path=getattr(args, "report_path", None),
            source_file=getattr(args, "source_file", None),
            queue_entry_id=getattr(args, "queue_entry_id", None),
            detail=str(getattr(args, "detail", "") or ""),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("maintenance", {}).get("ok", True) else 1


def cmd_record_missing_qr(vault_root: Path, args: argparse.Namespace) -> int:
    from .memory_gap_hooks import record_missing_qr

    try:
        out = record_missing_qr(
            vault_root,
            origin_lane=str(getattr(args, "origin_lane", "curator") or "curator"),
            note_path=str(getattr(args, "note_path", "") or ""),
            pipeline=str(getattr(args, "pipeline", "distill") or "distill"),
            detail=str(getattr(args, "detail", "") or ""),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_audit_museum_qr(vault_root: Path, args: argparse.Namespace) -> int:
    from .museum_qr_check import audit_museum_note, audit_museum_notes

    paths_raw = str(getattr(args, "paths", "") or "")
    paths = [p.strip() for p in paths_raw.split(",") if p.strip()]
    origin = str(getattr(args, "origin_lane", "curator") or "curator")
    pipeline = str(getattr(args, "pipeline", "distill") or "distill")
    try:
        if len(paths) == 1:
            out = audit_museum_note(vault_root, paths[0], origin_lane=origin, pipeline=pipeline)
        else:
            out = audit_museum_notes(vault_root, paths, origin_lane=origin, pipeline=pipeline)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", out.get("has_quick_reference")) else 1


def cmd_daemon(vault_root: Path, args: argparse.Namespace) -> int:
    from .harness_daemon import daemon_cycle_once, run_daemon

    once = not bool(getattr(args, "loop", False))
    dry_run = bool(getattr(args, "dry_run", False))
    interval = getattr(args, "interval_seconds", None)
    max_cycles = getattr(args, "max_cycles", None)
    try:
        if once:
            out = daemon_cycle_once(
                vault_root,
                dry_run=dry_run,
                config_path=getattr(args, "resolved_config", None),
            )
        else:
            out = run_daemon(
                vault_root,
                once=False,
                interval_seconds=interval,
                dry_run=dry_run,
                config_path=getattr(args, "resolved_config", None),
                max_cycles=max_cycles,
            )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") or out.get("skipped") else 1


def cmd_skill_trial_activate(vault_root: Path, args: argparse.Namespace) -> int:
    try:
        out = activate_trial(
            vault_root,
            slug=args.slug,
            production_skill=args.production_skill,
            trial_type=getattr(args, "trial_type", "new"),
            min_runs=int(getattr(args, "min_runs", 3)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_operator_inbox_sweep(vault_root: Path, args: argparse.Namespace) -> int:
    from .operator_inbox import sweep_reviewed_operator_inbox

    try:
        out = sweep_reviewed_operator_inbox(vault_root)
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_migrate_institute_lane(vault_root: Path, args: argparse.Namespace) -> int:
    from .institute_migration import migrate_curator_to_institute

    try:
        out = migrate_curator_to_institute(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_council_memory_pass(vault_root: Path, args: argparse.Namespace) -> int:
    from .council_memory_pass import run_council_memory_pass

    try:
        out = run_council_memory_pass(
            vault_root,
            session_id=str(getattr(args, "session_id", "") or ""),
            subject_lane=str(getattr(args, "lane", "sandbox") or "sandbox"),
            architect_decision=str(getattr(args, "architect_decision", "proceed") or "proceed"),
            council_context=str(getattr(args, "council_context", "") or ""),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_lane_recovery_retry(vault_root: Path, args: argparse.Namespace) -> int:
    from .lane_recovery import run_recovery_cycle

    try:
        out = run_recovery_cycle(
            vault_root,
            str(getattr(args, "lane", "sandbox") or "sandbox"),
            architect_decision=str(getattr(args, "architect_decision", "proceed") or "proceed"),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_l3_validation_drill(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l3_validation_drill import run_l3_validation_drill

    try:
        out = run_l3_validation_drill(
            vault_root,
            str(getattr(args, "lane", "institute") or "institute"),
            drill=str(getattr(args, "drill", "all") or "all"),
            dry_run=bool(getattr(args, "dry_run", False)),
            write_report=not bool(getattr(args, "no_report", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_l1_validation_drill(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l1_validation_drill import run_l1_validation_drill

    try:
        out = run_l1_validation_drill(
            vault_root,
            dry_run=bool(getattr(args, "dry_run", False)),
            write_report=not bool(getattr(args, "no_report", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_l2_validation_drill(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l2_validation_drill import run_l2_validation_drill

    try:
        out = run_l2_validation_drill(
            vault_root,
            drill=str(getattr(args, "drill", "all") or "all"),
            dry_run=bool(getattr(args, "dry_run", False)),
            write_report=not bool(getattr(args, "no_report", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_l4_validation_drill(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l4_validation_drill import run_l4_validation_drill

    try:
        out = run_l4_validation_drill(
            vault_root,
            drill=str(getattr(args, "drill", "all") or "all"),
            dry_run=bool(getattr(args, "dry_run", False)),
            write_report=not bool(getattr(args, "no_report", False)),
            governance_live_apply=bool(getattr(args, "governance_live_apply", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_phase_a_validation(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.l1_validation_drill import run_l1_validation_drill
    from .weave.l2_validation_drill import run_l2_validation_drill
    from .weave.l3_validation_drill import run_l3_validation_drill
    from .weave.l4_validation_drill import run_l4_validation_drill

    lane = str(getattr(args, "lane", "institute") or "institute")
    dry_run = bool(getattr(args, "dry_run", False))
    write_report = not bool(getattr(args, "no_report", False))
    layers_raw = str(getattr(args, "layers", "all") or "all").strip().lower()
    layer_tokens = {t.strip() for t in layers_raw.replace(",", " ").split() if t.strip()}
    run_all = "all" in layer_tokens or not layer_tokens
    try:
        results: dict[str, Any] = {"ok": True, "phase": "A", "layers": {}, "timestamp": None}
        if run_all or "l1" in layer_tokens:
            results["layers"]["L1"] = run_l1_validation_drill(vault_root, dry_run=dry_run, write_report=write_report)
        if run_all or "l2" in layer_tokens:
            results["layers"]["L2"] = run_l2_validation_drill(
                vault_root, drill="all", dry_run=dry_run, write_report=write_report
            )
        if run_all or "l3" in layer_tokens:
            results["layers"]["L3"] = run_l3_validation_drill(
                vault_root, lane=lane, drill="all", dry_run=dry_run, write_report=write_report
            )
        if run_all or "l4" in layer_tokens:
            results["layers"]["L4"] = run_l4_validation_drill(
                vault_root, drill="all", dry_run=dry_run, write_report=write_report
            )
        results["ok"] = all(layer.get("ok") for layer in results["layers"].values())
        from datetime import datetime, timezone

        results["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(results, indent=2))
    return 0 if results.get("ok") else 1


def cmd_trinity_validation_drill(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.trinity_validation_drill import run_trinity_validation_drill

    try:
        out = run_trinity_validation_drill(
            vault_root,
            drill=str(getattr(args, "drill", "all") or "all"),
            profile=str(getattr(args, "profile", "pilot") or "pilot"),
            dry_run=bool(getattr(args, "dry_run", False)),
            write_report=not bool(getattr(args, "no_report", False)),
            skip_touch_refresh=bool(getattr(args, "skip_touch_refresh", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_phase_b_validation(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.trinity_validation_drill import run_trinity_validation_drill

    dry_run = bool(getattr(args, "dry_run", False))
    write_report = not bool(getattr(args, "no_report", False))
    skip_touch_refresh = bool(getattr(args, "skip_touch_refresh", False))
    try:
        results = run_trinity_validation_drill(
            vault_root,
            drill="all",
            profile=str(getattr(args, "profile", "maintenance_set") or "maintenance_set"),
            dry_run=dry_run,
            write_report=write_report,
            skip_touch_refresh=skip_touch_refresh,
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(results, indent=2))
    return 0 if results.get("ok") else 1


def cmd_backbone_promotion(vault_root: Path, args: argparse.Namespace) -> int:
    from .backbone_promotion import run_backbone_promotion

    paths_raw = getattr(args, "paths", None)
    paths = [p.strip() for p in str(paths_raw).split(",") if p.strip()] if paths_raw else None
    try:
        out = run_backbone_promotion(
            vault_root,
            paths=paths,
            goal_packet_path=getattr(args, "goal_authority", None),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") or out.get("skipped") else 1


def cmd_stall_compensate(vault_root: Path, args: argparse.Namespace) -> int:
    from .stall_compensator import stall_compensate

    lanes = [x.strip() for x in str(getattr(args, "lanes", "sandbox")).split(",") if x.strip()]
    try:
        out = stall_compensate(vault_root, lanes=lanes, dry_run=getattr(args, "dry_run", False))
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_headless_eat(vault_root: Path, args: argparse.Namespace) -> int:
    """Single-lane headless EAT via headless_orchestrator (one lane per process)."""
    from .headless_orchestrator import headless_eat as ho_eat
    from .headless_single_lane import parse_lane_tokens

    lanes_raw = getattr(args, "lanes", None) or ""
    lanes = parse_lane_tokens(str(lanes_raw)) or None
    try:
        out = ho_eat(
            vault_root,
            lanes=lanes,
            dry_run=getattr(args, "dry_run", False),
            force=getattr(args, "force", False),
            config_path=getattr(args, "resolved_config", None),
            max_parallel=getattr(args, "max_parallel", None),
            orchestrator_run_id=getattr(args, "orchestrator_run_id", None),
            operator_declared_backlog=bool(getattr(args, "declared_backlog", False)),
            max_queue_entries=getattr(args, "max_queue_entries", None),
            goal_authority_path=getattr(args, "goal_authority", None),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    if out.get("error") == "headless_single_lane_required":
        return 2
    return 0 if out.get("ok") or out.get("skipped") else 1


def cmd_headless_architect(vault_root: Path, args: argparse.Namespace) -> int:
    """Architect L0 pass — goal packet validation, receipt, optional headless_eat."""
    lane = str(getattr(args, "lane", None) or "sandbox").strip()
    if not lane or "," in lane:
        print(
            json.dumps({"ok": False, "error": "headless_architect requires single --lane"}),
            file=sys.stderr,
        )
        return 2
    if bool(getattr(args, "overnight", False)):
        return cmd_headless_overnight(vault_root, args)

    from .headless_architect import headless_architect as ha_run

    try:
        out = ha_run(
            vault_root,
            lane,
            goal_authority_path=getattr(args, "goal_authority", None),
            council_forced=bool(getattr(args, "council_forced", False)),
            launch_eat=not bool(getattr(args, "no_eat", False)),
            dry_run=bool(getattr(args, "dry_run", False)),
            heuristic_council_only=bool(getattr(args, "heuristic_council", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_headless_overnight(vault_root: Path, args: argparse.Namespace) -> int:
    """Overnight session — multi-pass eat until soft deadline or implementation gate."""
    from .headless_overnight import headless_overnight as ho_run

    lane = str(getattr(args, "lane", None) or "sandbox").strip()
    if not lane or "," in lane:
        print(
            json.dumps({"ok": False, "error": "headless_overnight requires single --lane"}),
            file=sys.stderr,
        )
        return 2
    try:
        out = ho_run(
            vault_root,
            lane,
            dry_run=bool(getattr(args, "dry_run", False)),
            force=bool(getattr(args, "force", True)),
            max_passes=getattr(args, "max_passes", None),
            max_queue_entries=getattr(args, "max_queue_entries", None),
            goal_authority_path=getattr(args, "goal_authority", None),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) else 1


def cmd_ingest_age_scan(vault_root: Path, args: argparse.Namespace) -> int:
    from .ingest_age_scan import run_ingest_age_scan

    try:
        out = run_ingest_age_scan(vault_root, dry_run=bool(getattr(args, "dry_run", False)))
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) else 1


def cmd_pool_drain(vault_root: Path, args: argparse.Namespace) -> int:
    from .pool_drain import drain_central_pool

    try:
        out = drain_central_pool(vault_root, dry_run=bool(getattr(args, "dry_run", False)))
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_architect_ingest_pickup(vault_root: Path, args: argparse.Namespace) -> int:
    from .architect_ingest_pickup import run_architect_ingest_pickup

    lane = str(getattr(args, "lane", None) or "institute").strip().lower()
    try:
        out = run_architect_ingest_pickup(
            vault_root, lane=lane, dry_run=bool(getattr(args, "dry_run", False))
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok", True) else 1


def cmd_headless_fanout(vault_root: Path, args: argparse.Namespace) -> int:
    """Multi-lane launcher — one headless_eat subprocess per lane (fan-out cap default 3)."""
    from .headless_fanout import headless_fanout as ho_fanout
    from .headless_single_lane import parse_lane_tokens

    subject_lane = getattr(args, "subject_lane", None)
    lanes_raw = getattr(args, "lanes", None) or ""
    lanes = parse_lane_tokens(str(lanes_raw)) if lanes_raw else []
    if not subject_lane and not lanes:
        print(json.dumps({"ok": False, "error": "lanes_or_subject_lane_required"}), file=sys.stderr)
        return 2
    try:
        out = ho_fanout(
            vault_root,
            lanes=lanes or None,
            subject_lane=subject_lane,
            max_parallel=getattr(args, "max_parallel", None),
            dry_run=getattr(args, "dry_run", False),
            force=getattr(args, "force", False),
            background=not getattr(args, "wait", False),
            wait=getattr(args, "wait", False),
            fanout_run_id=getattr(args, "fanout_run_id", None),
            declared_backlog=bool(getattr(args, "declared_backlog", False)),
            max_queue_entries=getattr(args, "max_queue_entries", None),
            heuristic_council_only=bool(getattr(args, "heuristic_council", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    if out.get("error") == "no_runnable_lanes":
        return 2
    return 0 if out.get("ok") else 1


def cmd_cli_eat(vault_root: Path, args: argparse.Namespace) -> int:
    """Headless EAT via local Cursor CLI (single --lane or comma-separated)."""
    try:
        lane = getattr(args, "lane", None) or "curator"
        lanes_arg = getattr(args, "lanes", None)
        out = cli_eat(
            vault_root,
            lane=lane,
            lanes=lanes_arg,
            dry_run=getattr(args, "dry_run", False),
            config_path=getattr(args, "resolved_config", None),
            force=getattr(args, "force", False),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") or out.get("skipped") else 1


def cmd_weave_public_sync(vault_root: Path, args: argparse.Namespace) -> int:
    """Publish allowlisted weave slice to Trinity-Weave (no project bleed)."""
    result = run_weave_public_sync(
        vault_root,
        args.resolved_config,
        push=not getattr(args, "no_push", False),
        dry_run=getattr(args, "dry_run", False),
        summary=getattr(args, "summary", "") or "",
        use_lock=not getattr(args, "no_lock", False),
    )
    print(json.dumps(result.payload, indent=2))
    return result.exit_code


def cmd_post_queue_weave_publish(vault_root: Path, args: argparse.Namespace) -> int:
    """Optional post-queue Trinity-Weave publish after clean maintenance."""
    try:
        if getattr(args, "handoff_file", None) is not None:
            handoff = load_handoff_json(args.handoff_file, None)
        else:
            handoff = load_handoff_json(None, sys.stdin.read())
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "error": f"handoff: {e}"}), file=sys.stderr)
        return 1
    result = run_post_queue_weave_publish(vault_root, handoff, args.resolved_config)
    print(result.to_json())
    return result.exit_code


def cmd_git_push_policy(vault_root: Path, args: argparse.Namespace) -> int:
    """Print master git.push_enabled policy from live config."""
    from .git_push_policy import policy_snapshot

    snap = policy_snapshot(vault_root, config_path=getattr(args, "resolved_config", None))
    print(json.dumps(snap, indent=2))
    return 0 if snap.get("push_enabled") else 1


def cmd_project_bridge_sync(vault_root: Path, args: argparse.Namespace) -> int:
    """Regenerate project indexes and sync to Trinity-Weave project branch (local commit)."""
    result = run_project_bridge_sync(
        vault_root,
        args.resolved_config,
        project_id=getattr(args, "project_id", None),
        push=getattr(args, "push", False),
        use_lock=not getattr(args, "no_lock", False),
    )
    print(json.dumps(result.payload, indent=2))
    return result.exit_code


def cmd_project_bridge_push(vault_root: Path, args: argparse.Namespace) -> int:
    """Budgeted push of Trinity-Weave main or project branch."""
    result = run_project_bridge_push(
        vault_root,
        args.resolved_config,
        branch=getattr(args, "branch", None),
        force=getattr(args, "force", False),
        use_lock=not getattr(args, "no_lock", False),
    )
    print(json.dumps(result.payload, indent=2))
    return result.exit_code


def cmd_grok_bridge_status(vault_root: Path, args: argparse.Namespace) -> int:
    """Write Grok-Bridge-Status.md + .json from export checkout state."""
    out = write_grok_bridge_status(vault_root, args.resolved_config)
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_grok_fulfill_broker(vault_root: Path, args: argparse.Namespace) -> int:
    """Tier C mediated fulfill — fail-closed; requires --operator-ack."""
    raw: str | dict
    if getattr(args, "request_file", None):
        raw = Path(args.request_file).read_text(encoding="utf-8")
    elif getattr(args, "request_json", None):
        raw = args.request_json
    else:
        print(json.dumps({"ok": False, "error": "provide --request-file or --request-json"}), file=sys.stderr)
        return 1
    result = run_grok_fulfill_broker(
        vault_root,
        args.resolved_config,
        request_raw=raw,
        operator_ack=getattr(args, "operator_ack", False),
        write_pack=not getattr(args, "no_write_pack", False),
    )
    print(json.dumps(result.payload, indent=2))
    return result.exit_code


def cmd_post_queue_gitforge(vault_root: Path, args: argparse.Namespace) -> int:
    """Layer 1 post–A.7 deterministic GitForge (lock, vault git, optional export, audit)."""
    try:
        if getattr(args, "handoff_file", None) is not None:
            handoff = load_handoff_json(args.handoff_file, None)
        else:
            handoff = load_handoff_json(None, sys.stdin.read())
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "error": f"handoff: {e}"}), file=sys.stderr)
        return 1
    result = run_post_queue_gitforge(vault_root, handoff, args.resolved_config)
    print(result.to_json())
    return result.exit_code


def cmd_post_queue_memory_pass(vault_root: Path, args: argparse.Namespace) -> int:
    """Layer 1 post–A.7 agent continuity (MEMORY.md, continuity.md, skill_gap)."""
    try:
        if getattr(args, "handoff_file", None) is not None:
            handoff = load_memory_handoff_json(args.handoff_file, None)
        else:
            handoff = load_memory_handoff_json(None, sys.stdin.read())
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "error": f"handoff: {e}"}), file=sys.stderr)
        return 1
    lane = getattr(args, "lane", None)
    if lane and not handoff.get("queue_lane_filter"):
        handoff["queue_lane_filter"] = str(lane).strip().lower()
    result = run_post_queue_memory_pass(
        vault_root, handoff, config_path=args.resolved_config
    )
    print(result.to_json())
    return result.exit_code


def cmd_user_story_rollout(vault_root: Path, args: argparse.Namespace) -> int:
    """SET_ROLLOUT_BUDGET harness — write slice-depth-budget + optional beat auto-gen."""
    from .weave.user_story.rollout_slicer import run_rollout_slicer

    assignments_raw = getattr(args, "assignments_json", None) or "[]"
    try:
        assignments = json.loads(assignments_raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"invalid_assignments_json:{e}"}), file=sys.stderr)
        return 1
    if not isinstance(assignments, list):
        print(json.dumps({"ok": False, "error": "assignments_must_be_list"}), file=sys.stderr)
        return 1

    out = run_rollout_slicer(
        vault_root,
        project_id=str(getattr(args, "project_id", "genesis-mythos-master")),
        rollout_version=getattr(args, "rollout_version", None),
        row_assignments=assignments,
        generate_beats=not getattr(args, "no_beats", False),
    )
    print(json.dumps(out.to_dict(), indent=2))
    return 0 if out.ok else 1


def cmd_user_story_beats(vault_root: Path, args: argparse.Namespace) -> int:
    """BEAT_GENERATE harness — auto-generate beats from budget without reslicing."""
    from .weave.user_story.beat_auto_generate import run_beat_auto_generate

    out = run_beat_auto_generate(
        vault_root,
        project_id=str(getattr(args, "project_id", "genesis-mythos-master")),
    )
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_depth_slice(vault_root: Path, args: argparse.Namespace) -> int:
    """DEPTH_SLICE — L5 complete vision → L4..L1 scope files (top-down)."""
    from .weave.user_story.depth_slicer import run_depth_slicer

    row_id = getattr(args, "row_id", None)
    row_ids_raw = getattr(args, "row_ids", None)
    row_ids = [x.strip() for x in row_ids_raw.split(",") if x.strip()] if row_ids_raw else None
    out = run_depth_slicer(
        vault_root,
        project_id=str(getattr(args, "project_id", "genesis-mythos-master")),
        row_id=row_id,
        row_ids=row_ids,
        bootstrap_l5=not getattr(args, "no_bootstrap", False),
    )
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_factory_bom(vault_root: Path, args: argparse.Namespace) -> int:
    """FACTORY_BOM — evaluate Product Factory BOM checklist."""
    from .weave.factory.factory_bom import evaluate_factory_bom

    sections_raw = getattr(args, "sections", None)
    sections = tuple(x.strip() for x in sections_raw.split(",") if x.strip()) if sections_raw else None
    out = evaluate_factory_bom(
        vault_root,
        project_id=str(getattr(args, "project_id", "genesis-mythos-master")),
        sections=sections,
    )
    print(json.dumps(out.to_dict(), indent=2))
    return 0 if out.ok else 1


def cmd_factory_bom_brief(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.factory.factory_bom_brief import write_factory_bom_brief

    out = write_factory_bom_brief(
        vault_root,
        project_id=str(getattr(args, "project_id", "genesis-mythos-master")),
    )
    print(json.dumps(out.to_dict(), indent=2))
    return 0 if out.ok else 1


def cmd_catalog_coverage(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.user_story.catalog_coverage import run_catalog_coverage

    planned = getattr(args, "planned_rows", None)
    planned_tuple = tuple(x.strip() for x in planned.split(",") if x.strip()) if planned else None
    out = run_catalog_coverage(
        vault_root,
        project_id=str(getattr(args, "project_id", "genesis-mythos-master")),
        planned_row_ids=planned_tuple,
    )
    print(json.dumps(out.to_dict(), indent=2))
    return 0 if out.ok else 1


def cmd_conceptual_feed_gate(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.user_story.conceptual_factory_feed import conceptual_factory_feed_report

    out = conceptual_factory_feed_report(
        vault_root,
        str(getattr(args, "project_id", "genesis-mythos-master")),
        mint_batch=getattr(args, "mint_batch", None) or None,
    )
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_reconcile_conceptual_telemetry(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.user_story.conceptual_dispatch_authority import (
        reconcile_workflow_state_telemetry,
    )

    out = reconcile_workflow_state_telemetry(
        vault_root,
        str(getattr(args, "project_id", "genesis-mythos-master")),
    )
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_catalog_freeze_gate(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.user_story.catalog_coverage import run_catalog_freeze_gate

    out = run_catalog_freeze_gate(
        vault_root,
        project_id=str(getattr(args, "project_id", "genesis-mythos-master")),
    )
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_catalog_mint_pack_emit(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.user_story.catalog_mint_pack import emit_catalog_mint_pack

    out = emit_catalog_mint_pack(
        vault_root,
        project_id=str(getattr(args, "project_id", "genesis-mythos-master")),
        set_active=not bool(getattr(args, "no_set_active", False)),
    )
    print(json.dumps(out.to_dict(), indent=2))
    return 0 if out.ok else 1


def cmd_catalog_mint_receipt_validate(vault_root: Path, args: argparse.Namespace) -> int:
    from .weave.user_story.catalog_mint_receipt import validate_catalog_mint_receipt

    receipt_file = getattr(args, "receipt_file", None)
    receipt_yaml = getattr(args, "receipt_yaml", None)
    if receipt_file:
        raw = Path(receipt_file).read_text(encoding="utf-8")
    elif receipt_yaml:
        raw = str(receipt_yaml)
    else:
        print(
            json.dumps({"ok": False, "error": "need --receipt-file or --receipt-yaml"}),
            file=sys.stderr,
        )
        return 2
    out = validate_catalog_mint_receipt(
        vault_root,
        project_id=str(getattr(args, "project_id", "genesis-mythos-master")),
        receipt=raw,
    )
    print(json.dumps(out.to_dict(), indent=2))
    return 0 if out.ok else 1


def cmd_slice_producer_eat(vault_root: Path, args: argparse.Namespace) -> int:
    from .layer1_slice_producer import run_layer1_slice_producer_pass

    lane = str(getattr(args, "lane", "godot") or "godot").strip().lower()
    try:
        out = run_layer1_slice_producer_pass(
            vault_root,
            lane,
            max_entries=int(getattr(args, "max_entries", 2) or 2),
            dry_run=bool(getattr(args, "dry_run", False)),
            harness_fallback=bool(getattr(args, "harness_fallback", False)),
            invoke_pm_agent=bool(getattr(args, "invoke_pm_agent", False))
            or (
                not bool(getattr(args, "harness_fallback", False))
                and not bool(getattr(args, "dry_run", False))
            ),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def cmd_roadmap_factory_eat(vault_root: Path, args: argparse.Namespace) -> int:
    from .layer1_roadmap_factory import run_layer1_roadmap_factory_pass

    lane = str(getattr(args, "lane", "godot") or "godot").strip().lower()
    try:
        out = run_layer1_roadmap_factory_pass(
            vault_root,
            lane,
            max_entries=int(getattr(args, "max_entries", 3) or 3),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--vault-root", type=Path, default=None, help="Vault root (default: cwd)")
    common.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Second-Brain-Config.md path (default: Docs/Core or legacy paths)",
    )
    # Common flags live on each subparser only so ``harness snapshot --vault-root .`` works.
    p = argparse.ArgumentParser(
        prog="eat_queue_core.harness",
        description="EAT-QUEUE harness (PQ single writer)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_parallel(s: argparse.ArgumentParser) -> None:
        s.add_argument("--queue", type=Path, default=None, help="prompt-queue.jsonl (override parallel context)")
        s.add_argument(
            "--lane",
            type=str,
            default=None,
            help="Queue lane (godot, sandbox, …): synthetic parallel_track + PQ path when context file is missing",
        )
        s.add_argument(
            "--parallel-context-file",
            type=Path,
            default=None,
            help="JSON/YAML with resolved_prompt_queue_path / technical_bundle_root",
        )
        s.add_argument("--parallel-context-yaml", default=None, help="Inline JSON object string for parallel context")

    sp = sub.add_parser(
        "snapshot",
        help="SHA256 + line counts for PQ (and central pool when fanout)",
        parents=[common],
    )
    add_parallel(sp)
    sp.set_defaults(func=cmd_snapshot)

    vp = sub.add_parser(
        "verify",
        help="Compare current PQ bytes to a prior snapshot JSON",
        parents=[common],
    )
    add_parallel(vp)
    vp.add_argument("--expected-snapshot", type=Path, required=True, help="JSON file from harness snapshot")
    vp.set_defaults(func=cmd_verify)

    rp = sub.add_parser(
        "rewrite_consumed",
        help="Remove consumed ids from PQ (and central pool when dual-track)",
        parents=[common],
    )
    add_parallel(rp)
    rp.add_argument("--ids", default=None, help="Comma-separated queue entry ids to remove")
    rp.add_argument("--plan", type=Path, default=None, help="eat_queue_run_plan.json (queue_rewrite_ids / consumed_ids)")
    rp.add_argument(
        "--single-pool",
        action="store_true",
        help="Only rewrite the track PQ, not the central pool",
    )
    rp.set_defaults(func=cmd_rewrite_consumed)

    _APPEND_ENTRIES_EPILOG = """
Examples — JSONL must come from stdin (heredoc/pipe) or --lines-file:

  Dry-run + snapshot gate:
    PYTHONPATH=. python3 -m scripts.eat_queue_core.harness append_entries \\
      --vault-root . --lane godot --dry-run \\
      --require-snapshot-json /tmp/godot-pq-snapshot.json <<'EOF'
    {"id":"x","mode":"HANDOFF_AUDIT_REPAIR","params":{"origin_request_id":"o","user_guidance":"y"}}
    EOF

  Search eat_queue_core (run as its own command — never append grep to append_entries):
    grep -rE "dedupe|TELEMETRY_CONTRACT" scripts/eat_queue_core/ --include='*.py' --include='*.md'
"""

    ap = sub.add_parser(
        "append_entries",
        help="Append JSONL lines to PQ with A.5b.0z dedupe, audit + intent_actual_receipt telemetry (Step 0 / A.5x)",
        parents=[common],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_APPEND_ENTRIES_EPILOG,
    )
    add_parallel(ap)
    ap.add_argument(
        "--current-midrun-count",
        type=int,
        default=0,
        help="Appends already done this EAT-QUEUE run (default 0)",
    )
    ap.add_argument("--lines-file", type=Path, default=None, help="Path to JSONL lines (alternative to stdin)")
    ap.add_argument("--parent-run-id", default="eatq-append", help="Telemetry parent_run_id for audit/comms rows")
    ap.add_argument(
        "--emit-audit",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Append a5b_enqueue_dedupe rows to prompt-queue-audit.jsonl (default: true)",
    )
    ap.add_argument(
        "--emit-intent-receipt",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Append intent_actual_receipt rows to task-handoff-comms.jsonl (default: true)",
    )
    ap.add_argument(
        "--emit-watcher-result",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Append harness telemetry lines to canonical Watcher-Result.md (default: true)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print JSON outcome only; do not write PQ, audit, comms, or Watcher",
    )
    ap.add_argument(
        "--require-snapshot",
        "--require-snapshot-json",
        dest="require_snapshot_json",
        type=Path,
        default=None,
        metavar="PATH",
        help="JSON from harness snapshot; refuse append if PQ/pool sha256 mismatch",
    )
    ap.add_argument(
        "--inline-pass3-repair-count",
        type=int,
        default=0,
        help="Pass3 repair intents already consumed this run (overrides eat-queue-run-plan when >0)",
    )
    ap.add_argument(
        "--eat-queue-run-plan",
        type=Path,
        default=None,
        help="eat_queue_run_plan.json to count pass3 repair rows (default: next to PQ)",
    )
    ap.add_argument(
        "--origin-dedupe-window-hours",
        type=float,
        default=None,
        help="Override config origin dedupe window (hours)",
    )
    ap.add_argument(
        "--use-gitforge-lock",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Acquire gitforge lock around PQ append (default: false)",
    )
    ap.set_defaults(func=cmd_append_entries)

    ps = sub.add_parser(
        "pool_sync",
        help="Central pool → track PQ hydration",
        parents=[common],
    )
    ps.add_argument("--lane", type=str, required=True)
    ps.add_argument("--target-pq", type=Path, required=True)
    ps.add_argument("--pool", type=Path, default=None)
    ps.add_argument("--strict-central-only", action="store_true")
    ps.add_argument("--dry-run", action="store_true")
    ps.set_defaults(func=cmd_pool_sync)

    pd = sub.add_parser(
        "pool_drain",
        help="Drain legacy central prompt-queue into per-lane PQs (one-time)",
        parents=[common],
    )
    pd.add_argument("--dry-run", action="store_true")
    pd.set_defaults(func=cmd_pool_drain)

    pl = sub.add_parser("plan", help="Emit eat_queue_run_plan.json", parents=[common])
    add_parallel(pl)
    pl.add_argument(
        "--emit",
        type=Path,
        default=None,
        help="eat_queue_run_plan.json output path (required unless --all-tracks)",
    )
    pl.add_argument(
        "--all-tracks",
        action="store_true",
        help="Emit plan for every parallel_execution.tracks[] row (sequential; omit --emit/--lane)",
    )
    pl.add_argument("--decisions-log", type=Path, default=None)
    pl.add_argument("--parent-run-id", default="eatq-local")
    pl.add_argument("--verbose", action="store_true")
    pl.set_defaults(func=cmd_plan)

    fc = sub.add_parser(
        "full_cycle",
        help="Reactive multi-pass plan (run_full_eat_queue_cycle)",
        parents=[common],
    )
    add_parallel(fc)
    fc.add_argument("--emit", type=Path, default=None)
    fc.add_argument("--decisions-log", type=Path, default=None)
    fc.add_argument("--parent-run-id", default=None)
    fc.add_argument("--action", default="deepen")
    fc.add_argument("--profile", default="balance")
    fc.add_argument("--max-passes", type=int, default=2)
    fc.add_argument("--strict-mode", action=argparse.BooleanOptionalAction, default=True)
    fc.add_argument("--apply-cleanup", action="store_true")
    fc.add_argument("--central-pool-fanout", action="store_true")
    fc.add_argument("--no-central-pool-fanout", action="store_true")
    fc.add_argument(
        "--emit-watcher-result",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Append plan-level telemetry to Watcher-Result when intent receipts enabled (default: false)",
    )
    fc.add_argument(
        "--all-tracks",
        action="store_true",
        help="Run full_cycle for every parallel_execution.tracks[] row (sequential v1; omit --emit/--lane)",
    )
    fc.set_defaults(func=cmd_full_cycle)

    pg = sub.add_parser(
        "post_queue_gitforge",
        help="Post–A.7 GitForge: lock, vault git, optional export sync, audit log",
        parents=[common],
    )
    add_parallel(pg)
    pg.add_argument(
        "--handoff-file",
        type=Path,
        default=None,
        help="JSON hand-off (A.7a). If omitted, read JSON object from stdin.",
    )
    pg.set_defaults(func=cmd_post_queue_gitforge)

    gpp = sub.add_parser(
        "git_push_policy",
        help="Resolve master git.push_enabled from live config",
        parents=[common],
    )
    gpp.set_defaults(func=cmd_git_push_policy)

    wps = sub.add_parser(
        "weave_public_sync",
        help="Publish allowlisted weave slice to Trinity-Weave (Grok public context)",
        parents=[common],
    )
    add_parallel(wps)
    wps.add_argument("--no-push", action="store_true", help="Sync only; do not git push")
    wps.add_argument("--no-lock", action="store_true", help="Skip gitforge lock (tests/debug)")
    wps.add_argument("--dry-run", action="store_true", help="Sync to export checkout without commit/push")
    wps.add_argument("--summary", default="", help="Commit message suffix")
    wps.set_defaults(func=cmd_weave_public_sync)

    pbs = sub.add_parser(
        "project_bridge_sync",
        help="Grok bridge: regen project indexes + sync to Trinity-Weave project/* branch",
        parents=[common],
    )
    add_parallel(pbs)
    pbs.add_argument("--project-id", default=None, help="Project id under 1-Projects/ (default pilot from config)")
    pbs.add_argument("--push", action="store_true", help="Also run budgeted push after sync")
    pbs.add_argument("--no-lock", action="store_true", help="Skip gitforge lock (tests/debug)")
    pbs.set_defaults(func=cmd_project_bridge_sync)

    pbp = sub.add_parser(
        "project_bridge_push",
        help="Grok bridge: budgeted push of main or project branch on Trinity-Weave",
        parents=[common],
    )
    add_parallel(pbp)
    pbp.add_argument("--branch", default=None, help="Branch to push (default pilot project branch)")
    pbp.add_argument("--force", action="store_true", help="Skip cooldown (not git.push_enabled)")
    pbp.add_argument("--no-lock", action="store_true", help="Skip gitforge lock")
    pbp.set_defaults(func=cmd_project_bridge_push)

    gbs = sub.add_parser(
        "grok_bridge_status",
        help="Write Grok-Bridge-Status.md + .json",
        parents=[common],
    )
    add_parallel(gbs)
    gbs.set_defaults(func=cmd_grok_bridge_status)

    gfb = sub.add_parser(
        "grok_fulfill_broker",
        help="Tier C mediated fulfill pack (requires --operator-ack)",
        parents=[common],
    )
    add_parallel(gfb)
    gfb.add_argument("--request-file", type=Path, default=None, help="YAML/JSON fulfill request file")
    gfb.add_argument("--request-json", default=None, help="Inline JSON request")
    gfb.add_argument("--operator-ack", action="store_true", help="Bone pilot approved this fulfill")
    gfb.add_argument("--no-write-pack", action="store_true", help="Audit only; do not write pack file")
    gfb.set_defaults(func=cmd_grok_fulfill_broker)

    pwp = sub.add_parser(
        "post_queue_weave_publish",
        help="Post-queue Trinity-Weave publish (after clean maintenance)",
        parents=[common],
    )
    add_parallel(pwp)
    pwp.add_argument(
        "--handoff-file",
        type=Path,
        default=None,
        help="JSON hand-off. If omitted, read JSON object from stdin.",
    )
    pwp.set_defaults(func=cmd_post_queue_weave_publish)

    pym = sub.add_parser(
        "post_queue_memory_pass",
        help="Post–A.7 continuity: MEMORY.md, continuity.md, skill_gap scan (A.7y)",
        parents=[common],
    )
    add_parallel(pym)
    pym.add_argument(
        "--handoff-file",
        type=Path,
        default=None,
        help="JSON hand-off (A.7y). If omitted, read JSON object from stdin.",
    )
    pym.set_defaults(func=cmd_post_queue_memory_pass)

    mc = sub.add_parser(
        "memory_compact",
        help="Trim lane MEMORY.md to agent_continuity.memory_max_chars",
        parents=[common],
    )
    add_parallel(mc)
    mc.set_defaults(func=cmd_memory_compact)

    mpv = sub.add_parser(
        "mcp_postedit_validate",
        help="Track C — write MCP implementation validation receipt (maintenance + lane mirror)",
        parents=[common],
    )
    mpv.add_argument("--lane", required=True)
    mpv.add_argument("--project-id", required=True)
    mpv.add_argument("--engine-adapter", required=True)
    mpv.add_argument("--milestone-id", required=True)
    mpv.add_argument("--repo-root", default=None)
    mpv.add_argument("--status", default="pass", choices=["pass", "fail", "provisional"])
    mpv.add_argument("--message", default="")
    mpv.add_argument("--debug-output", default=None)
    mpv.add_argument("--smoke", action="store_true", help="Run M0 structural checks when milestone is M0")
    mpv.set_defaults(func=cmd_mcp_postedit_validate)

    qnp = sub.add_parser(
        "queue_neighbor_prep",
        help="Pre-pack semantic_neighbors for curator PQ source_file lines (default Q prep)",
        parents=[common],
    )
    add_parallel(qnp)
    qnp.add_argument("--dry-run", action="store_true")
    qnp.set_defaults(lane="curator", func=cmd_queue_neighbor_prep)

    ncr = sub.add_parser(
        "nav_color_refresh",
        help="Build nav-color-index.jsonl from semantic similarity (Phase A)",
        parents=[common],
    )
    add_parallel(ncr)
    ncr.add_argument("--dry-run", action="store_true", help="Preview rows without writing index")
    ncr.add_argument("--paths", default=None, help="Comma-separated vault-relative paths to refresh")
    ncr.add_argument(
        "--populate-vault",
        action="store_true",
        help="Walk full vault_knowledge in batches (not default; merges into index)",
    )
    ncr.add_argument(
        "--use-pq-defaults",
        action="store_true",
        help="Refresh paths from curator PQ source_file only (default Weave tick behavior)",
    )
    ncr.set_defaults(func=cmd_nav_color_refresh)


    stp = sub.add_parser(
        "syncthing_sync_policy",
        help="Pause/resume Syncthing sync partitions (Ops/Vault/Bulk schedule)",
        parents=[common],
    )
    stp.add_argument(
        "--force-bulk-unpause",
        action="store_true",
        help="Unpause Bulk until idle, then re-pause if outside 06:00-09:00 window",
    )
    stp.add_argument("--dry-run", action="store_true")
    stp.set_defaults(func=cmd_syncthing_sync_policy)

    lsb = sub.add_parser(
        "lane_status_board",
        help="Refresh Ingest/Weave-Status-Board.md (alias: weave_status_board)",
        parents=[common],
    )
    add_parallel(lsb)
    lsb.set_defaults(func=cmd_lane_status_board)

    wsb = sub.add_parser(
        "weave_status_board",
        help="Refresh Ingest/Weave-Status-Board.md (factory-first operator surface)",
        parents=[common],
    )
    add_parallel(wsb)
    wsb.set_defaults(func=cmd_weave_status_board)

    tal = sub.add_parser(
        "trinity_align",
        help="Wave 2.5d — Trinity leg checks + pilot disconnect (precedence_collapse, error_narrative_drift)",
        parents=[common],
    )
    tal.add_argument(
        "--trinity-id",
        default=None,
        help="Comma-separated card ids (default: N2 pilot trio)",
    )
    tal.add_argument(
        "--all-cards",
        action="store_true",
        help="Check all cards under .technical/weave/components/ (not pilot-only)",
    )
    tal.add_argument(
        "--no-meta-update",
        action="store_true",
        help="Do not write meta.last_disconnect on cards",
    )
    tal.set_defaults(func=cmd_trinity_align)

    ttr = sub.add_parser(
        "trinity_touch_refresh",
        help="Wave 2.5b — refresh Trinity touch_content_hash; propose behavior_signals",
        parents=[common],
    )
    ttr.add_argument(
        "--trinity-id",
        default=None,
        help="Comma-separated card ids (default: N2 pilot trio)",
    )
    ttr.add_argument("--dry-run", action="store_true", help="Compute only; do not write cards")
    ttr.add_argument(
        "--apply-behavior-signals",
        action="store_true",
        help="Merge proposed test names into touch.behavior_signals (operator confirm)",
    )
    ttr.add_argument(
        "--all-cards",
        action="store_true",
        help="Refresh all cards under .technical/weave/components/ (not pilot-only)",
    )
    ttr.add_argument(
        "--operator-mutation",
        action="store_true",
        help="Allow writes to maintenance-core cards (operator-only)",
    )
    ttr.add_argument(
        "--maintenance-set",
        action="store_true",
        help="Refresh all 18 maintenance partition ids (components + bridges + meta in registry)",
    )
    ttr.set_defaults(func=cmd_trinity_touch_refresh)

    tcg = sub.add_parser(
        "trinity_card_generate",
        help="Wave 3 — batch-generate Trinity card proposals (inventory + orphan scan)",
        parents=[common],
    )
    tcg.add_argument(
        "--dry-run",
        action="store_true",
        help="Discover only; do not write proposals folder",
    )
    tcg.add_argument(
        "--include-locked",
        action="store_true",
        help="Include production-locked cards in partial/inventory output",
    )
    tcg.add_argument(
        "--stamp",
        default=None,
        help="Proposals subfolder name (default: YYYY-MM-DD-wide-net or YYYY-MM-DD-narrow-net)",
    )
    tcg.add_argument(
        "--narrow",
        action="store_true",
        help="Narrow scan (inventory + aggregate orphans only); default is wide net",
    )
    tcg.add_argument(
        "--skip-rule-orphans",
        action="store_true",
        help="Omit per-rule stubs (wide net) and aggregate maintenance-rule orphan (narrow)",
    )
    tcg.set_defaults(func=cmd_trinity_card_generate)

    tsc = sub.add_parser(
        "trinity_spine_cascade",
        help="Spine cascade — forward-grow Conceptual on stubs from locked corpus (touch/rules unchanged)",
        parents=[common],
    )
    tsc.add_argument("--dry-run", action="store_true", help="List targets only; no writes")
    tsc.add_argument(
        "--stamp",
        default=None,
        help="Output folder under proposals/ (default: YYYY-MM-DD-spine-cascade)",
    )
    tsc.add_argument("--trinity-id", default=None, help="Single target trinity_id")
    tsc.add_argument(
        "--write-in-place",
        action="store_true",
        help="Overwrite source stub paths instead of proposals/<stamp>/stubs/",
    )
    tsc.add_argument(
        "--extend-only",
        action="store_true",
        help="Include targets that already have conceptual_confirmed_at on stub",
    )
    tsc.add_argument(
        "--fix-legs",
        action="store_true",
        help="Reserved: also refresh touch/rules (default leaves legs unchanged)",
    )
    tsc.add_argument(
        "--no-packs",
        action="store_true",
        help="Skip writing packs/<id>.md LLM hand-off files",
    )
    tsc.add_argument(
        "--governance-stubs-only",
        action="store_true",
        help="Only governance-set-v1/stubs/*.yaml (smaller batch than all proposals)",
    )
    tsc.add_argument(
        "--proposal-stamp",
        default=None,
        metavar="DIR",
        help="Limit to .technical/weave/proposals/<DIR>/stubs/ (e.g. wide-net-v2-2)",
    )
    tsc.add_argument(
        "--include-unlocked-production",
        action="store_true",
        help="Also regen Conceptual on production components without lock stamps",
    )
    tsc.add_argument(
        "--force-machine-voice",
        action="store_true",
        help="Include stubs with prior spine-cascade v1 / backfill voice even if 'polished'",
    )
    tsc.set_defaults(func=cmd_trinity_spine_cascade)

    tpr = sub.add_parser(
        "trinity_promote_proposals",
        help="Promote reviewed proposal stubs to component-proposals/ (provisional tier)",
        parents=[common],
    )
    tpr.add_argument(
        "--stamp",
        default="I-did-it-right",
        help="Proposal folder under .technical/weave/proposals/<stamp>/stubs/",
    )
    tpr.add_argument("--dry-run", action="store_true", help="Report actions only")
    tpr.add_argument("--force", action="store_true", help="Overwrite existing provisional cards")
    tpr.add_argument("--trinity-id", default=None, help="Promote single id")
    tpr.set_defaults(func=cmd_trinity_promote_proposals)

    tlk = sub.add_parser(
        "trinity_lock_card",
        help="Operator gate: move provisional card to locked components/",
        parents=[common],
    )
    tlk.add_argument("--trinity-id", required=True, help="trinity_id to lock")
    tlk.add_argument("--dry-run", action="store_true", help="Preview lock move")
    tlk.add_argument(
        "--lock-kind",
        default="full",
        choices=("full", "conceptual_spine", "maintenance_core"),
        help="Lock stamp: full | conceptual_spine | maintenance_core",
    )
    tlk.set_defaults(func=cmd_trinity_lock_card)

    tba = sub.add_parser(
        "trinity_boundary_audit",
        help="Phase 0 — read-only Trinity component/bridge boundary audit",
        parents=[common],
    )
    tba.add_argument(
        "--partition",
        default="maintenance",
        help="Registry partition (default: maintenance)",
    )
    tba.add_argument(
        "--trinity-id",
        default=None,
        help="Comma-separated ids (default: all maintenance components in registry)",
    )
    tba.add_argument(
        "--no-report",
        action="store_true",
        help="Skip writing .technical/weave/validation/trinity-boundary-*.json",
    )
    tba.set_defaults(func=cmd_trinity_boundary_audit)

    tcs = sub.add_parser(
        "trinity_catchup_sweep",
        help="Phase 3 — partition-aware Trinity catch-up (bones/bridges/provisionals)",
        parents=[common],
    )
    tcs.add_argument(
        "--include-provisional",
        action="store_true",
        help="Include component-proposals/ provisionals in sweep + escalations",
    )
    tcs.add_argument(
        "--all-cards",
        action="store_true",
        help="Sweep all locked+provisional cards (not maintenance partition only)",
    )
    tcs.add_argument("--dry-run", action="store_true", help="Analyze only; do not queue or refresh")
    tcs.add_argument(
        "--no-queue",
        action="store_true",
        help="Run align grouping without enqueueing playbook actions",
    )
    tcs.add_argument(
        "--max-escalations",
        type=int,
        default=None,
        help="Cap provisional escalation notes per run (default from playbook/config)",
    )
    tcs.add_argument("--no-report", action="store_true")
    tcs.add_argument(
        "--curate-non-core",
        action="store_true",
        help="Force stale-touch auto curation on non-core cards (default from config)",
    )
    tcs.add_argument(
        "--no-curate",
        action="store_true",
        help="Disable stale-touch auto curation; playbook queue only",
    )
    tcs.set_defaults(func=cmd_trinity_catchup_sweep)

    tbc = sub.add_parser(
        "trinity_bridge_consolidate",
        help="Phase 7 — merge provisional bridges sharing tunnel_via → locked bridge + registry",
        parents=[common],
    )
    tbc.add_argument(
        "--tunnel-via",
        required=True,
        help="Core trinity_id all provisional bridges must tunnel_via (e.g. lane_status_board)",
    )
    tbc.add_argument(
        "--output-id",
        default=None,
        help="Locked bridge trinity_id (default: <tunnel_via>_bridge_consolidated)",
    )
    tbc.add_argument("--dry-run", action="store_true")
    tbc.add_argument(
        "--force",
        action="store_true",
        help="Allow single-source merge or overwrite existing locked output",
    )
    tbc.add_argument(
        "--lock-kind",
        default="full",
        choices=["full", "conceptual_spine"],
        help="Lock stamp after consolidate (not maintenance_core)",
    )
    tbc.set_defaults(func=cmd_trinity_bridge_consolidate)

    atb = sub.add_parser(
        "assess_trinity_card_backlog",
        help="Phase 7 — rank maintenance Trinity cards by drift × usage",
        parents=[common],
    )
    atb.add_argument(
        "--all-cards",
        action="store_true",
        help="Include all locked+provisional cards (not maintenance partition only)",
    )
    atb.add_argument("--top-n", type=int, default=None, help="Max ranked rows (config default 8)")
    atb.add_argument("--no-report", action="store_true")
    atb.set_defaults(func=cmd_assess_trinity_card_backlog)

    tsc = sub.add_parser(
        "trinity_stamp_core_cards",
        help="Phase 8 — stamp maintenance core YAMLs (lock_kind maintenance_core, doctrine)",
        parents=[common],
    )
    tsc.add_argument(
        "--trinity-id",
        default=None,
        help="Comma-separated core ids (default: all maintenance_core registry ids)",
    )
    tsc.add_argument("--dry-run", action="store_true")
    tsc.set_defaults(func=cmd_trinity_stamp_core_cards)

    tp8 = sub.add_parser(
        "trinity_phase8_vault_compensation",
        help="Phase 8 — stamp core, deploy D bridge stubs, retier harness_*, touch refresh, board smoke",
        parents=[common],
    )
    tp8.add_argument("--dry-run", action="store_true")
    tp8.add_argument("--skip-touch-refresh", action="store_true")
    tp8.add_argument("--skip-board-smoke", action="store_true")
    tp8.set_defaults(func=cmd_trinity_phase8_vault_compensation)

    tw9 = sub.add_parser(
        "trinity_weave_self_wrap",
        help="Phase 9+10 — align, unclog, corps sweep, enforce, observe (board)",
        parents=[common],
    )
    tw9.add_argument("--dry-run", action="store_true")
    tw9.add_argument("--skip-align", action="store_true")
    tw9.add_argument("--skip-enforce", action="store_true")
    tw9.add_argument("--skip-unclog", action="store_true")
    tw9.add_argument("--skip-corps", action="store_true")
    tw9.add_argument("--skip-observe", action="store_true")
    tw9.add_argument("--operator-mutation", action="store_true")
    tw9.add_argument("--corps-cluster", default=None, help="e.g. architect_* (optional batch filter)")
    tw9.add_argument(
        "--full-corpus",
        action="store_true",
        help="Nerve-test all provisionals (9+10 pass gate; default from Config)",
    )
    tw9.add_argument(
        "--corps-sample-only",
        action="store_true",
        help="Legacy: first N provisionals only (trinity_corps_cluster_batch_size)",
    )
    tw9.add_argument(
        "--max-laps",
        type=int,
        default=None,
        help="Outer lap cycles (T0→spine→T1→T2 poke + between-lap repair; default trinity_corps_max_laps)",
    )
    tw9.add_argument(
        "--max-llm-laps",
        type=int,
        default=None,
        help="LLM semantic attempts per card per lap at T1 (default trinity_corps_max_llm_laps)",
    )
    tw9.add_argument(
        "--enable-llm-repair",
        action="store_true",
        help="Request 10c T1 LLM-pack mode (trial scope: --corps-cluster + balance profile)",
    )
    tw9.add_argument(
        "--llm-repair-force",
        action="store_true",
        help="Operator override: LLM mode for in-cluster cards (still requires --corps-cluster)",
    )
    tw9.add_argument(
        "--speed-mode",
        default=None,
        help="Profile gate for 10c trial (default balance when trial active)",
    )
    tw9.add_argument(
        "--no-auto-repair",
        action="store_true",
        help="Disable between-lap deterministic corps repair",
    )
    tw9.add_argument(
        "--regenerate-complete",
        action="store_true",
        help="Phase 10e — archive unlocked corpus + anchored regen (overrides trinity_corps_regenerate_complete_enabled: false)",
    )
    tw9.add_argument(
        "--meta-lens-force-align",
        action="store_true",
        help="Phase 10e/13 — with --regenerate-complete, merge locked meta doctrine into Rules/Touch on regen (Conceptual preserved)",
    )
    tw9.add_argument(
        "--host-weld-bootstrap-all",
        action="store_true",
        help="Phase 13 — force mint all manifest slugs (discouraged bootstrap)",
    )
    tw9.add_argument("--no-graph", action="store_true")
    tw9.add_argument("--no-report", action="store_true")
    tw9.set_defaults(func=cmd_trinity_weave_self_wrap)

    tes = sub.add_parser(
        "trinity_expand_self",
        help="Phase 14 — expand_self delta wrap (scoped onboarding)",
        parents=[common],
    )
    tes.add_argument("--scope-ids", default=None, help="Comma-separated provisional trinity ids")
    tes.add_argument("--corps-cluster", default=None, help="Glob filter when scope-ids omitted")
    tes.add_argument("--operator-override-scope", action="store_true")
    tes.add_argument("--operator-mutation", action="store_true")
    tes.add_argument("--dry-run", action="store_true")
    tes.add_argument("--skip-align", action="store_true")
    tes.add_argument("--skip-corps", action="store_true")
    tes.add_argument("--skip-enforce", action="store_true")
    tes.add_argument("--skip-unclog", action="store_true")
    tes.add_argument("--skip-observe", action="store_true")
    tes.set_defaults(func=cmd_trinity_expand_self)

    thws = sub.add_parser(
        "trinity_host_weld_sync",
        help="Phase 13 — surgical host-weld/live sync from locked meta",
        parents=[common],
    )
    thws.add_argument("--dry-run", action="store_true")
    thws.add_argument(
        "--host-weld-bootstrap-all",
        action="store_true",
        help="Force mint all manifest slugs (discouraged)",
    )
    thws.set_defaults(func=cmd_trinity_host_weld_sync)

    tkp = sub.add_parser(
        "trinity_knob_parity",
        help="Phase 16 — knob parity matrix proofs (factory × knob-option)",
        parents=[common],
    )
    tkp.add_argument("--dry-run", action="store_true")
    tkp.set_defaults(func=cmd_trinity_knob_parity)

    tha = sub.add_parser(
        "trinity_honesty_anchor",
        help="Phase 16 — honesty anchor claim-tier matrix proofs",
        parents=[common],
    )
    tha.add_argument("--dry-run", action="store_true")
    tha.set_defaults(func=cmd_trinity_honesty_anchor)

    tshf = sub.add_parser(
        "trinity_stub_honesty_fold",
        help="Phase 16b — bootstrap stub honesty invariants + trace closure stubs",
        parents=[common],
    )
    tshf.add_argument("--dry-run", action="store_true")
    tshf.add_argument("--no-bootstrap", dest="bootstrap", action="store_false")
    tshf.set_defaults(func=cmd_trinity_stub_honesty_fold, bootstrap=True)

    tiv = sub.add_parser(
        "trinity_integration_vet",
        help="Trinity integration vet — charter + honesty + stub honesty (read-only)",
        parents=[common],
    )
    tiv.add_argument("--dry-run", action="store_true")
    tiv.set_defaults(func=cmd_trinity_integration_vet)

    tup = sub.add_parser(
        "trinity_usage_proven",
        help="Phase 15 — usage_proven assess/stamp/unfreeze",
        parents=[common],
    )
    tup.add_argument("--trinity-id", default=None)
    tup.add_argument("--assess", action="store_true", help="Assess candidacy (default: report)")
    tup.add_argument("--stamp", action="store_true", help="Stamp one id when criteria met")
    tup.add_argument("--stamp-ready", action="store_true", help="With --assess: stamp all ready")
    tup.add_argument("--unfreeze", action="store_true", help="Operator unfreeze usage_proven id")
    tup.add_argument("--operator-force", action="store_true", help="Stamp without criteria (operator)")
    tup.add_argument("--dry-run", action="store_true")
    tup.set_defaults(func=cmd_trinity_usage_proven)

    tcra = sub.add_parser(
        "trinity_conduct_repair_apply_trial",
        help="Phase 10g — bounded conduct repair apply trial",
        parents=[common],
    )
    tcra.add_argument("--trinity-id", default=None)
    tcra.add_argument("--max-apply", type=int, default=None)
    tcra.add_argument("--dry-run", action="store_true")
    tcra.set_defaults(func=cmd_trinity_conduct_repair_apply_trial)

    tt2 = sub.add_parser(
        "trinity_type2_verify",
        help="Type-2 verify — full-corpus self-wrap (no regenerate-complete)",
        parents=[common],
    )
    tt2.add_argument("--dry-run", action="store_true")
    tt2.add_argument("--skip-observe", action="store_true")
    tt2.set_defaults(func=cmd_trinity_type2_verify)

    tlg = sub.add_parser(
        "trinity_llm_repair_trial_gate",
        help="Alternative C — 10c/10g trial track + cutover gate report",
        parents=[common],
    )
    tlg.add_argument(
        "--corps-cluster",
        "--cluster",
        dest="corps_cluster",
        default="harness_*",
        help="Cluster assess scope (default harness_*)",
    )
    tlg.add_argument("--speed-mode", default="balance")
    tlg.add_argument("--skip-fixtures", action="store_true")
    tlg.add_argument("--dry-run", action="store_true")
    tlg.set_defaults(func=cmd_trinity_llm_repair_trial_gate)

    tca = sub.add_parser(
        "trinity_core_charter_audit",
        help="Alternative A — maintenance core vs finalized meta (read-only)",
        parents=[common],
    )
    tca.add_argument("--dry-run", action="store_true")
    tca.set_defaults(func=cmd_trinity_core_charter_audit)

    tge = sub.add_parser(
        "trinity_graduation_evaluator",
        help="Phase 17 — graduation plane (evidence-gated promotion matrix)",
        parents=[common],
    )
    tge.add_argument(
        "--apply",
        action="store_true",
        help="Write graduation-overrides.yaml when eligible (requires graduation_enabled)",
    )
    tge.set_defaults(func=cmd_trinity_graduation_evaluator)

    tlr = sub.add_parser(
        "trinity_llm_repair_trial",
        help="Phase 10c — scoped LLM T1 trial (balance + corps-cluster, cap 7/run)",
        parents=[common],
    )
    tlr.add_argument(
        "--corps-cluster",
        "--cluster",
        dest="corps_cluster",
        required=True,
        help="Glob filter for trial scope (required), e.g. harness_*",
    )
    tlr.add_argument("--trinity-id", default=None, help="Single-card poke (must match cluster)")
    tlr.add_argument("--speed-mode", default="balance", help="Profile gate (default balance)")
    tlr.add_argument("--assess", action="store_true", help="Preview would_llm candidates only")
    tlr.add_argument("--dry-run", action="store_true")
    tlr.add_argument(
        "--trial-weaken-id",
        default=None,
        help="Intentionally weaken T1 semantic on this id before trial (backs up conceptual)",
    )
    tlr.add_argument(
        "--ensure-fixture",
        action="store_true",
        help="Create harness_llm_repair_trial fixture (semantic-weak) before run",
    )
    tlr.add_argument(
        "--restore-after",
        action="store_true",
        help="Restore conceptual from trial backup after single-card run",
    )
    tlr.set_defaults(func=cmd_trinity_llm_repair_trial)

    trf = sub.add_parser(
        "trinity_redesign_factory",
        help="Phase 16 — redesign_factory A/B structural compare",
        parents=[common],
    )
    trf.add_argument("--legacy-factory-id", default="queue_dispatch")
    trf.add_argument("--candidate-factory-id", default="queue_dispatch_v2")
    trf.add_argument("--ab-mode", default="parallel", choices=("parallel", "sequential"))
    trf.add_argument(
        "--speed-mode-matrix",
        default="",
        help="Comma-separated speed_mode values (advisory; matrix uses all canonical options)",
    )
    trf.add_argument("--operator-deprecate-ack", action="store_true")
    trf.add_argument("--dry-run", action="store_true")
    trf.set_defaults(func=cmd_trinity_redesign_factory)

    tp10 = sub.add_parser(
        "trinity_provisional_corps_sweep",
        help="Phase 10 — corps hygiene + nerve test on component-proposals/",
        parents=[common],
    )
    tp10.add_argument("--dry-run", action="store_true")
    tp10.add_argument("--cluster", default=None, help="Glob filter e.g. architect_*")
    tp10.add_argument("--apply-hygiene", action="store_true")
    tp10.add_argument("--nerve-test-only", action="store_true")
    tp10.add_argument("--skip-sweep", action="store_true")
    tp10.add_argument("--skip-nerve-test", action="store_true")
    tp10.add_argument(
        "--full-corpus",
        action="store_true",
        help="Hygiene + nerve test all provisionals (not batch of 7)",
    )
    tp10.set_defaults(func=cmd_trinity_provisional_corps_sweep)

    cob = sub.add_parser(
        "corps_overnight_batch",
        help="Overnight corps hygiene+nerve batches (offset pagination, resilient writes)",
        parents=[common],
    )
    cob.add_argument(
        "--start-offset",
        type=int,
        default=None,
        help="Skip first N provisionals (default 7 or CORPS_START_OFFSET env)",
    )
    cob.add_argument("--batch-size", type=int, default=None)
    cob.add_argument(
        "--stop-on-write-error",
        action="store_true",
        help="Abort on first write_trinity_card failure (default: log and continue)",
    )
    cob.add_argument(
        "--no-auto-smoke-tests",
        action="store_true",
        help="Skip auto-generating test_<module>.py stubs for strict conduct",
    )
    cob.add_argument(
        "--no-status-file",
        action="store_true",
        help="Do not write .technical/weave/corps-overnight-status.json / .md",
    )
    cob.set_defaults(func=cmd_corps_overnight_batch)

    t11a = sub.add_parser(
        "trinity_apply_card_identity_doctrine",
        help="Phase 11a (Grok B) — merge card_kind doctrine into trinity_card_authoring",
        parents=[common],
    )
    t11a.add_argument("--dry-run", action="store_true")
    t11a.set_defaults(func=cmd_trinity_apply_card_identity_doctrine)

    tcr = sub.add_parser(
        "trinity_corpus_restore_from_archive",
        help="Grok A rollback — restore cards from 4-Archives/Weave/Trinity-Corpus/<stamp>/cards/",
        parents=[common],
    )
    tcr.add_argument("--stamp", default=None, help="Archive folder name (default: latest)")
    tcr.add_argument("--dry-run", action="store_true")
    tcr.add_argument(
        "--target",
        choices=("proposals", "components"),
        default="proposals",
    )
    tcr.set_defaults(func=cmd_trinity_corpus_restore_from_archive)

    t11s = sub.add_parser(
        "trinity_card_identity_status",
        help="Check Phase 11a doctrine present on trinity_card_authoring",
        parents=[common],
    )
    t11s.set_defaults(func=cmd_trinity_card_identity_status)

    ttr = sub.add_parser(
        "trinity_transcript_route",
        help="Index vault plans + rank agent-transcripts per trinity_id (pilot routing)",
        parents=[common],
    )
    ttr.add_argument(
        "--no-rebuild-index",
        action="store_true",
        help="Reuse .technical/weave/transcript-routing/plan-index.json",
    )
    ttr.add_argument(
        "--transcript-root",
        default=None,
        help="Override agent-transcripts root (default: Cursor project folder)",
    )
    ttr.add_argument(
        "--trinity-id",
        default=None,
        help="Route one id only (default: harness spine 10 + governance set2 locked 9)",
    )
    ttr.add_argument(
        "--pilot-only",
        action="store_true",
        help="Default cohort only (explicit; same as default when no --trinity-id)",
    )
    ttr.set_defaults(func=cmd_trinity_transcript_route)

    tpp = sub.add_parser(
        "trinity_pack_preview",
        help="Wave 2.5c — preview trinity_pack YAML for context_envelope",
        parents=[common],
    )
    tpp.add_argument("--trinity-id", default=None)
    tpp.add_argument("--concept", default=None)
    tpp.add_argument("--lane", default=None, help="e.g. maintenance → default lane_status_board")
    tpp.set_defaults(func=cmd_trinity_pack_preview)

    l4r = sub.add_parser(
        "l4_offline_replay",
        help="L4 G1 — offline replay over weave metrics (no live policy change)",
        parents=[common],
    )
    l4r.set_defaults(func=cmd_l4_offline_replay)

    l4b = sub.add_parser(
        "l4_bandit_update",
        help="L4 G2 — bandit state update + profile recommendation (observe-only)",
        parents=[common],
    )
    l4b.set_defaults(func=cmd_l4_bandit_update)

    l4p = sub.add_parser(
        "l4_propose_promotion",
        help="L4 G2 — queue ADAPTIVE_POLICY_REVIEW when uplift exceeds threshold",
        parents=[common],
    )
    l4p.set_defaults(func=cmd_l4_propose_promotion)

    l5a = sub.add_parser(
        "l5_arm",
        help="H2 — arm L5 sandbox experiment (sandbox lane only, AC2 timebox)",
        parents=[common],
    )
    l5a.add_argument("--days", type=int, default=None, help="AC2 timebox days (default from Config)")
    l5a.add_argument("--force", action="store_true", help="Arm even if L3-green gate fails")
    l5a.set_defaults(func=cmd_l5_arm)

    l5k = sub.add_parser("l5_kill", help="H2 — hard kill switch for L5 sandbox", parents=[common])
    l5k.add_argument("--reason", default="operator_kill")
    l5k.set_defaults(func=cmd_l5_kill)

    l5r = sub.add_parser(
        "l5_release",
        help="Clear L5 kill switch (status idle; re-arm with l5_arm)",
        parents=[common],
    )
    l5r.set_defaults(func=cmd_l5_release)

    l5s = sub.add_parser("l5_status", help="H2 — L5 sandbox state + readiness", parents=[common])
    l5s.set_defaults(func=cmd_l5_status)

    l5t = sub.add_parser(
        "l5_sandbox_tick",
        help="H2 — one closed-loop tick (audit→repair→eat) on sandbox lane only",
        parents=[common],
    )
    l5t.add_argument("--dry-run", action="store_true")
    l5t.add_argument("--force-eat", action="store_true", help="Force headless_eat even when policy headless_eat false")
    l5t.set_defaults(func=cmd_l5_sandbox_tick)

    pct = sub.add_parser(
        "pseudo_clock_tick",
        help="Museum pseudo-clock: merge pending PQ, evaluate thresholds",
        parents=[common],
    )
    add_parallel(pct)
    pct.add_argument(
        "--increment-eat",
        action="store_true",
        help="Increment eat_queue_completions counter before threshold check",
    )
    pct.add_argument("--pq-consumed", type=int, default=0, help="Add to pq_lines_consumed")
    pct.set_defaults(func=cmd_pseudo_clock_tick)

    st = sub.add_parser(
        "schedule_tick",
        help="Phase 17 schedule planes: listener / scheduled / reactive / graduation",
        parents=[common],
    )
    add_parallel(st)
    st.add_argument(
        "--increment-eat",
        action="store_true",
        help="Increment eat_queue_completions counter before threshold check",
    )
    st.add_argument("--pq-consumed", type=int, default=0, help="Add to pq_lines_consumed")
    st.set_defaults(func=cmd_schedule_tick)

    vs = sub.add_parser(
        "vault_scan",
        help="Write 3-Resources/Watcher-Advisory.md (T0/T1); optional headless signal",
        parents=[common],
    )
    add_parallel(vs)
    vs.add_argument(
        "--write-signal",
        action="store_true",
        help="Write .technical/watcher-request-headless-eat.json when knobs allow",
    )
    vs.add_argument("--no-write-signal", action="store_true", help="Never write signal file")
    vs.set_defaults(func=cmd_vault_scan)

    ce = sub.add_parser(
        "cli_eat",
        help="Headless EAT-QUEUE lane curator via local cursor/agent CLI",
        parents=[common],
    )
    add_parallel(ce)
    ce.add_argument(
        "--lanes",
        default=None,
        help="Exactly one lane; comma-separated values are rejected (use separate processes)",
    )
    ce.add_argument("--dry-run", action="store_true", help="Print hand-off only; no CLI invoke")
    ce.add_argument(
        "--force",
        action="store_true",
        help="Run even when headless_eat is false in curator-knobs.yaml",
    )
    ce.set_defaults(func=cmd_cli_eat)

    ha = sub.add_parser(
        "headless_architect",
        help="Architect L0 — goal authority, receipt, optional headless_eat for lane",
        parents=[common],
    )
    add_parallel(ha)
    ha.add_argument(
        "--goal-authority",
        default=None,
        help="Path to goal-authority.json (default .technical/parallel/<lane>/goal-authority.json)",
    )
    ha.add_argument("--council-forced", action="store_true")
    ha.add_argument("--no-eat", action="store_true", help="Receipt only; do not invoke headless_eat")
    ha.add_argument(
        "--heuristic-council",
        action="store_true",
        help="Skip agent -p seat calls; use deterministic opinions only",
    )
    ha.add_argument("--dry-run", action="store_true")
    ha.add_argument(
        "--overnight",
        action="store_true",
        help="Run headless_overnight session for this lane (alias for headless_overnight subcommand)",
    )
    ha.set_defaults(func=cmd_headless_architect)

    ho = sub.add_parser(
        "headless_overnight",
        help="Overnight session — soft deadline, multi-pass headless_eat, PQ hold/stage",
        parents=[common],
    )
    add_parallel(ho)
    ho.add_argument(
        "--goal-authority",
        default=None,
        help="Path to goal-authority.json (default .technical/parallel/<lane>/goal-authority.json)",
    )
    ho.add_argument("--dry-run", action="store_true")
    ho.add_argument("--force", action="store_true", default=True)
    ho.add_argument(
        "--max-passes",
        type=int,
        default=None,
        help="Max eat passes (default overnight_max_passes_per_lane from config)",
    )
    ho.add_argument(
        "--max-queue-entries",
        type=int,
        default=None,
        help="Max queue entries per eat pass (default overnight_max_queue_entries)",
    )
    ho.set_defaults(func=cmd_headless_overnight)

    he = sub.add_parser(
        "headless_eat",
        help="Single-lane headless EAT (one lane per process; writes completion receipts)",
        parents=[common],
    )
    add_parallel(he)
    he.add_argument(
        "--lanes",
        default="curator",
        help="Exactly one lane token (e.g. curator). Multi-lane = separate processes.",
    )
    he.add_argument(
        "--max-parallel",
        type=int,
        default=None,
        help="Deprecated — must be 1; use separate headless_eat per lane",
    )
    he.add_argument("--dry-run", action="store_true")
    he.add_argument("--force", action="store_true")
    he.add_argument(
        "--declared-backlog",
        action="store_true",
        help="Mark run as operator-declared backlog (burst exempt on health board)",
    )
    he.add_argument(
        "--max-queue-entries",
        type=int,
        default=None,
        help="Cap PQ lines consumed this run (overflow restored after eat; default from orchestrator-policy batch_max_entries_per_headless_run)",
    )
    he.add_argument(
        "--orchestrator-run-id",
        default=None,
        help="Stable run id for registry/receipts (fan-out children pass parent-prefixed ids)",
    )
    he.add_argument(
        "--goal-authority",
        default=None,
        help="Path to goal-authority.json (default .technical/parallel/<lane>/goal-authority.json)",
    )
    he.set_defaults(func=cmd_headless_eat)

    hf = sub.add_parser(
        "headless_fanout",
        help="Fan-out: spawn one headless_eat subprocess per lane (max 3 concurrent starts)",
        parents=[common],
    )
    add_parallel(hf)
    hf.add_argument(
        "--lanes",
        default="",
        help="Comma- or space-separated lanes (optional when --subject-lane set)",
    )
    hf.add_argument(
        "--subject-lane",
        default=None,
        help="Subject lane for Architect orchestration (reads goal-authority.json)",
    )
    hf.add_argument(
        "--heuristic-council",
        action="store_true",
        help="Skip agent -p seat calls; use deterministic opinions only",
    )
    hf.add_argument(
        "--max-parallel",
        type=int,
        default=None,
        help="Max child processes starting at once (default headless_fanout_max_parallel=3)",
    )
    hf.add_argument("--dry-run", action="store_true")
    hf.add_argument("--force", action="store_true")
    hf.add_argument(
        "--wait",
        action="store_true",
        help="Block until all children exit (default: detach/background)",
    )
    hf.add_argument(
        "--fanout-run-id",
        default=None,
        help="Optional stable fanout_run_id for registry parent row",
    )
    hf.add_argument("--declared-backlog", action="store_true")
    hf.add_argument("--max-queue-entries", type=int, default=None)
    hf.set_defaults(func=cmd_headless_fanout)

    mp = sub.add_parser(
        "memory_pass",
        help="Update continuity/MEMORY from receipt; run skill-gap scan",
        parents=[common],
    )
    add_parallel(mp)
    mp.add_argument(
        "--receipt-json",
        default=None,
        help="Optional path to receipt JSON file",
    )
    mp.set_defaults(func=cmd_memory_pass, lane="curator")

    ois = sub.add_parser(
        "operator_inbox_sweep",
        help="Archive Ingest/Agent-Output notes with user_reviewed: true",
        parents=[common],
    )
    ois.set_defaults(func=cmd_operator_inbox_sweep)

    ias = sub.add_parser(
        "ingest_age_scan",
        help="Hash-stable Ingest scan → institute INGEST batch + optional headless_architect",
        parents=[common],
    )
    ias.add_argument("--dry-run", action="store_true")
    ias.set_defaults(func=cmd_ingest_age_scan)

    aip = sub.add_parser(
        "architect_ingest_pickup",
        help="Architect intent thread pickup (submit/debounce/promote) for institute lane",
        parents=[common],
    )
    add_parallel(aip)
    aip.add_argument("--dry-run", action="store_true")
    aip.set_defaults(func=cmd_architect_ingest_pickup, lane="institute")

    sc = sub.add_parser(
        "stall_compensate",
        help="Deterministic stall compensation (append hygiene / audit lines)",
        parents=[common],
    )
    add_parallel(sc)
    sc.add_argument("--lanes", default="sandbox", help="Comma-separated watch lanes (paused_lanes skipped)")
    sc.add_argument("--dry-run", action="store_true")
    sc.set_defaults(func=cmd_stall_compensate)

    mil = sub.add_parser(
        "migrate_institute_lane",
        help="Copy .technical/parallel/curator → institute (no delete)",
        parents=[common],
    )
    mil.add_argument("--dry-run", action="store_true")
    mil.set_defaults(func=cmd_migrate_institute_lane)

    cmp = sub.add_parser(
        "council_memory_pass",
        help="Append institute MEMORY.md line for council session",
        parents=[common],
    )
    add_parallel(cmp)
    cmp.add_argument("--session-id", required=True)
    cmp.add_argument("--architect-decision", default="proceed")
    cmp.add_argument("--council-context", default="")
    cmp.add_argument("--dry-run", action="store_true")
    cmp.set_defaults(func=cmd_council_memory_pass, lane="sandbox")

    lrr = sub.add_parser(
        "lane_recovery_retry",
        help="Run recoverable handler + headless_eat for lane stall (max 3)",
        parents=[common],
    )
    add_parallel(lrr)
    lrr.add_argument("--architect-decision", default="proceed")
    lrr.add_argument("--dry-run", action="store_true")
    lrr.set_defaults(func=cmd_lane_recovery_retry, lane="sandbox")

    l3d = sub.add_parser(
        "l3_validation_drill",
        help="Phase A L3 fault-injection drills (stale lock, live wait, missing bundle)",
        parents=[common],
    )
    add_parallel(l3d)
    l3d.add_argument(
        "--drill",
        default="all",
        choices=("all", "stale_pq_lock", "live_pq_lock_wait", "missing_pq_bundle"),
        help="Which drill to run (default: all)",
    )
    l3d.add_argument("--dry-run", action="store_true")
    l3d.add_argument("--no-report", action="store_true", help="Skip JSON report + metric row")
    l3d.set_defaults(func=cmd_l3_validation_drill, lane="institute")

    l1d = sub.add_parser(
        "l1_validation_drill",
        help="Phase A L1 integrity fault drill (board break → O1 OPERATOR_SURFACE_REPAIR)",
        parents=[common],
    )
    l1d.add_argument("--dry-run", action="store_true")
    l1d.add_argument("--no-report", action="store_true")
    l1d.set_defaults(func=cmd_l1_validation_drill)

    l2d = sub.add_parser(
        "l2_validation_drill",
        help="Phase A L2 predictive + symbolic gate drills",
        parents=[common],
    )
    l2d.add_argument(
        "--drill",
        default="all",
        choices=("all", "predictive_critical_block", "symbolic_registry_block", "live_risk_tier"),
    )
    l2d.add_argument("--dry-run", action="store_true")
    l2d.add_argument("--no-report", action="store_true")
    l2d.set_defaults(func=cmd_l2_validation_drill)

    l4d = sub.add_parser(
        "l4_validation_drill",
        help="Phase A L4 adaptive policy drills (replay, bandit, promotion, governance)",
        parents=[common],
    )
    l4d.add_argument(
        "--drill",
        default="all",
        choices=(
            "all",
            "offline_replay",
            "bandit_update",
            "promotion_proposal",
            "governance_promotion",
            "config_board_reconcile",
        ),
    )
    l4d.add_argument("--dry-run", action="store_true")
    l4d.add_argument("--no-report", action="store_true")
    l4d.add_argument(
        "--governance-live-apply",
        action="store_true",
        help="Approve promotion with live_apply=true (leaves active policy; skips restore)",
    )
    l4d.set_defaults(func=cmd_l4_validation_drill, governance_live_apply=False)

    pav = sub.add_parser(
        "phase_a_validation",
        help="Run Phase A L1–L4 validation drills",
        parents=[common],
    )
    add_parallel(pav)
    pav.add_argument("--layers", default="all", help="all | l1 | l2 | l3 | l4 (comma-separated ok)")
    pav.add_argument("--dry-run", action="store_true")
    pav.add_argument("--no-report", action="store_true")
    pav.set_defaults(func=cmd_phase_a_validation, lane="institute")

    tvd = sub.add_parser(
        "trinity_validation_drill",
        help="Phase B Trinity validation drills (schema, touch, align, pack, enforcement)",
        parents=[common],
    )
    tvd.add_argument(
        "--drill",
        default="all",
        choices=(
            "all",
            "schema_v2",
            "touch_refresh",
            "align_green",
            "pack_envelope",
            "conceptual_refs",
            "enforcement_fault",
            "component_scope",
        ),
    )
    tvd.add_argument("--dry-run", action="store_true")
    tvd.add_argument("--no-report", action="store_true")
    tvd.add_argument(
        "--skip-touch-refresh",
        action="store_true",
        help="Omit touch_refresh drill (cards must already be fresh for align_green)",
    )
    tvd.add_argument(
        "--profile",
        default="pilot",
        choices=("pilot", "maintenance_set"),
        help="Card set: pilot (3 gauge cards) or maintenance_set (partition registry)",
    )
    tvd.set_defaults(func=cmd_trinity_validation_drill, skip_touch_refresh=False)

    pbv = sub.add_parser(
        "phase_b_validation",
        help="Run Phase B Trinity validation drill sequence (all drills)",
        parents=[common],
    )
    pbv.add_argument("--dry-run", action="store_true")
    pbv.add_argument("--no-report", action="store_true")
    pbv.add_argument("--skip-touch-refresh", action="store_true")
    pbv.add_argument(
        "--profile",
        default="maintenance_set",
        choices=("pilot", "maintenance_set"),
        help="Default maintenance_set for Phase 2 weave integration exit",
    )
    pbv.set_defaults(func=cmd_phase_b_validation, skip_touch_refresh=False)

    bbp = sub.add_parser(
        "backbone_promotion",  # DEPRECATED 2026-07-21: vestigial .cursor/sync
        help="Gated sync rules/skills to .cursor/sync (Phase E)",
        parents=[common],
    )
    bbp.add_argument("--goal-authority", default=None, help="Goal packet path for gate check")
    bbp.add_argument("--paths", default=None, help="Comma-separated rule/skill paths")
    bbp.add_argument("--dry-run", action="store_true")
    bbp.set_defaults(func=cmd_backbone_promotion)

    bbs = sub.add_parser(
        "backbone_sync",  # DEPRECATED 2026-07-21: vestigial .cursor/sync
        help="Gated sync rules/skills to .cursor/sync (canonical name)",
        parents=[common],
    )
    bbs.add_argument("--goal-authority", default=None, help="Goal packet path for gate check")
    bbs.add_argument("--paths", default=None, help="Comma-separated rule/skill paths")
    bbs.add_argument("--dry-run", action="store_true")
    bbs.set_defaults(func=cmd_backbone_promotion)

    sgs = sub.add_parser(
        "skill_gap_scan",
        help="Scan MEMORY gap patterns; write skill-proposals stubs",
        parents=[common],
    )
    add_parallel(sgs)
    sgs.set_defaults(func=cmd_skill_gap_scan)

    me = sub.add_parser(
        "maintenance_eat",
        help="Process maintenance-lane PQ via light handlers (no Task subagent)",
        parents=[common],
    )
    add_parallel(me)
    me.add_argument("--max-entries", type=int, default=5, help="Max PQ lines to consume (default 5)")
    me.add_argument("--dry-run", action="store_true")
    me.set_defaults(func=cmd_maintenance_eat, lane="maintenance")

    ie = sub.add_parser(
        "implementation_eat",
        help="Process godot implementation_milestone PQ via IMPLEMENT_SLICE harness",
        parents=[common],
    )
    add_parallel(ie)
    ie.add_argument("--max-entries", type=int, default=1, help="Max milestones per pass (default 1)")
    ie.add_argument("--dry-run", action="store_true")
    ie.add_argument("--skip-agent", action="store_true", help="Skip Cursor agent (M1 vault_doc still runs)")
    ie.add_argument("--skip-preflight", action="store_true", help="Skip MCP/engine preflight (repo already verified)")
    ie.add_argument("--replay-seats", action="store_true", help="Replay lane seats for a jammed job (requires --job-id)")
    ie.add_argument("--job-id", type=str, default=None, help="Factory PQ entry id for replay-seats")
    ie.add_argument("--agent-log", type=str, default=None, help="Agent telemetry log path (vault-relative)")
    ie.add_argument("--resume-from", type=str, default=None, choices=("interpretation", "preflight", "agent", "seats"))
    ie.add_argument(
        "--seats-only",
        action="store_true",
        help="With --replay-seats: run seats only without mark_lane_complete / slice rollup",
    )
    ie.set_defaults(func=cmd_implementation_eat, lane="godot")

    spe = sub.add_parser(
        "slice_producer_eat",
        help="Validate PM compose/review receipts or harness fallback for SLICE_PRODUCER_* PQ lines",
        parents=[common],
    )
    add_parallel(spe)
    spe.add_argument("--max-entries", type=int, default=2, help="Max compose/review lines per pass (default 2)")
    spe.add_argument("--dry-run", action="store_true")
    spe.add_argument(
        "--harness-fallback",
        action="store_true",
        help="Run harness compose/review when PM agent artifacts missing (headless / smoke)",
    )
    spe.add_argument(
        "--invoke-pm-agent",
        action="store_true",
        help="Run agent -p for SLICE_PRODUCER_* before validation (default when not --harness-fallback)",
    )
    spe.set_defaults(func=cmd_slice_producer_eat, lane="godot")

    wr = sub.add_parser(
        "warning_ledger_rollup",
        help="Roll up harness soft warnings into maintenance PQ MAINTENANCE_EVAL lines",
        parents=[common],
    )
    wr.set_defaults(func=cmd_warning_ledger_rollup)

    gs = sub.add_parser(
        "ghost_skill_audit",
        help="Scan skill-proposals + MEMORY gaps; append GHOST_SKILL_AUDIT to maintenance PQ when findings exist",
        parents=[common],
    )
    gs.add_argument("--no-append", action="store_true", help="Scan only; do not append maintenance PQ line")
    gs.set_defaults(func=cmd_ghost_skill_audit)

    rlv = sub.add_parser(
        "record_little_val_block",
        help="Pipeline hook: little_val hard block → MEMORY gap + maintenance REPAIR_PLAYBOOK",
        parents=[common],
    )
    rlv.add_argument("--origin-lane", default="curator")
    rlv.add_argument("--primary-code", required=True)
    rlv.add_argument("--report-path", default=None)
    rlv.add_argument("--source-file", default=None)
    rlv.add_argument("--queue-entry-id", default=None)
    rlv.add_argument("--detail", default="")
    rlv.set_defaults(func=cmd_record_little_val_block)

    rqr = sub.add_parser(
        "record_missing_qr",
        help="Pipeline hook: missing Quick Reference → MEMORY gap + soft warning ledger",
        parents=[common],
    )
    rqr.add_argument("--origin-lane", default="curator")
    rqr.add_argument("--note-path", required=True)
    rqr.add_argument("--pipeline", default="distill")
    rqr.add_argument("--detail", default="")
    rqr.set_defaults(func=cmd_record_missing_qr)

    aqr = sub.add_parser(
        "audit_museum_qr",
        help="Verify Quick Reference on Code-Exhibit notes; record missing_qr gaps when absent",
        parents=[common],
    )
    aqr.add_argument("--paths", required=True, help="Comma-separated note paths under vault root")
    aqr.add_argument("--origin-lane", default="curator")
    aqr.add_argument("--pipeline", default="distill")
    aqr.set_defaults(func=cmd_audit_museum_qr)

    dm = sub.add_parser(
        "daemon",
        help="Tier 4 daemon: curator headless (tier 1) then maintenance tail (tier 2); no project-lane autopilot",
        parents=[common],
    )
    dm.add_argument(
        "--loop",
        action="store_true",
        help="Run continuous loop until interrupted",
    )
    dm.add_argument(
        "--interval-seconds",
        type=float,
        default=None,
        help="Sleep between cycles in loop mode (default from harness_daemon config)",
    )
    dm.add_argument(
        "--max-cycles",
        type=int,
        default=None,
        help="Stop loop after N cycles (loop mode only)",
    )
    dm.add_argument("--dry-run", action="store_true")
    dm.set_defaults(func=cmd_daemon)

    sta = sub.add_parser(
        "skill_trial_activate",
        help="Set registry pilot to trialing for a production skill slug",
        parents=[common],
    )
    sta.add_argument("--slug", required=True)
    sta.add_argument("--production-skill", required=True)
    sta.add_argument("--trial-type", default="new", choices=["new", "upgrade"])
    sta.add_argument("--min-runs", type=int, default=3)
    sta.set_defaults(func=cmd_skill_trial_activate)

    usr = sub.add_parser(
        "user_story_rollout",
        help="Write slice-depth-budget from operator row assignments (SET_ROLLOUT_BUDGET)",
        parents=[common],
    )
    usr.add_argument("--project-id", default="genesis-mythos-master")
    usr.add_argument("--rollout-version", type=int, default=None)
    usr.add_argument(
        "--assignments-json",
        required=True,
        help='JSON list e.g. [{"row_id":"ui_presentation_shell","target_depth":2}]',
    )
    usr.add_argument("--no-beats", action="store_true", help="Skip beat auto-generation")
    usr.set_defaults(func=cmd_user_story_rollout)

    usb = sub.add_parser(
        "user_story_beats",
        help="Auto-generate beats from slice-depth-budget (BEAT_GENERATE)",
        parents=[common],
    )
    usb.add_argument("--project-id", default="genesis-mythos-master")
    usb.set_defaults(func=cmd_user_story_beats)

    ds = sub.add_parser(
        "depth_slice",
        help="Top-down depth slicer — L5 complete → L4..L1 scope files (DEPTH_SLICE)",
        parents=[common],
    )
    ds.add_argument("--project-id", default="genesis-mythos-master")
    ds.add_argument("--row-id", default=None, help="Single catalog row id")
    ds.add_argument("--row-ids", default=None, help="Comma-separated row ids")
    ds.add_argument("--no-bootstrap", action="store_true", help="Do not bootstrap L5 scaffold")
    ds.set_defaults(func=cmd_depth_slice)

    fbom = sub.add_parser(
        "factory_bom",
        help="Evaluate Product Factory BOM (setup checklist → Product)",
        parents=[common],
    )
    fbom.add_argument("--project-id", default="genesis-mythos-master")
    fbom.add_argument("--sections", default=None, help="Comma-separated BOM sections")
    fbom.set_defaults(func=cmd_factory_bom)

    fbb = sub.add_parser(
        "factory_bom_brief",
        help="Write operator Factory BOM brief markdown",
        parents=[common],
    )
    fbb.add_argument("--project-id", default="genesis-mythos-master")
    fbb.set_defaults(func=cmd_factory_bom_brief)

    cc = sub.add_parser(
        "catalog_coverage",
        help="Validate slice-catalog completeness and execution pins",
        parents=[common],
    )
    cc.add_argument("--project-id", default="genesis-mythos-master")
    cc.add_argument("--planned-rows", default=None, help="Comma-separated expected row ids")
    cc.set_defaults(func=cmd_catalog_coverage)

    cfg = sub.add_parser(
        "catalog_freeze_gate",
        help="Loop 2 levels gate — catalog signed, depth charter, influence deck",
        parents=[common],
    )
    cfg.add_argument("--project-id", default="genesis-mythos-master")
    cfg.set_defaults(func=cmd_catalog_freeze_gate)

    cmpe = sub.add_parser(
        "catalog_mint_pack_emit",
        help="Emit Docs/catalog-mint/<project_id>/ pack (conceptual + stack + pins + manifest)",
        parents=[common],
    )
    cmpe.add_argument("--project-id", default="genesis-mythos-master")
    cmpe.add_argument(
        "--no-set-active",
        action="store_true",
        help="Do not rewrite Docs/catalog-mint/ACTIVE.md",
    )
    cmpe.set_defaults(func=cmd_catalog_mint_pack_emit)

    cmrv = sub.add_parser(
        "catalog_mint_receipt_validate",
        help="Fail-closed validate one catalog mint YAML receipt against pack",
        parents=[common],
    )
    cmrv.add_argument("--project-id", default="genesis-mythos-master")
    cmrv.add_argument("--receipt-file", default=None)
    cmrv.add_argument("--receipt-yaml", default=None)
    cmrv.set_defaults(func=cmd_catalog_mint_receipt_validate)

    cfeed = sub.add_parser(
        "conceptual_feed_gate",
        help="Rung 1 factory feed readiness (mint-batch-scoped)",
        parents=[common],
    )
    cfeed.add_argument("--project-id", default="genesis-mythos-master")
    cfeed.add_argument("--mint-batch", default=None, help="pmg_phases | presentation_first")
    cfeed.set_defaults(func=cmd_conceptual_feed_gate)

    ctele = sub.add_parser(
        "reconcile_conceptual_telemetry",
        help="Demote legacy workflow_state rollup closed stamps when feed gate is red",
        parents=[common],
    )
    ctele.add_argument("--project-id", default="genesis-mythos-master")
    ctele.set_defaults(func=cmd_reconcile_conceptual_telemetry)

    rfe = sub.add_parser(
        "roadmap_factory_eat",
        help="Process roadmap-factory PQ modes (SET_ROLLOUT_BUDGET, ROADMAP_FACTORY_BOOTSTRAP, …)",
        parents=[common],
    )
    add_parallel(rfe)
    rfe.add_argument("--max-entries", type=int, default=3)
    rfe.add_argument("--dry-run", action="store_true")
    rfe.set_defaults(func=cmd_roadmap_factory_eat, lane="godot")

    rop = sub.add_parser(
        "roadmap_organize_paths",
        help="Repath flat roadmap notes to canonical Phase-N-M-* folders",
        parents=[common],
    )
    rop.add_argument("--project-id", required=True)
    rop.add_argument("--dry-run", action="store_true", help="Plan moves only (default: apply)")
    rop.add_argument(
        "--scan-only",
        action="store_true",
        help="Report structural path violations without moving",
    )
    rop.set_defaults(func=cmd_roadmap_organize_paths)

    rcn = sub.add_parser(
        "roadmap_clean_nav",
        help="Fix secondary Dataview FROM scopes after path organize",
        parents=[common],
    )
    rcn.add_argument("--project-id", required=True)
    rcn.add_argument("--dry-run", action="store_true")
    rcn.set_defaults(func=cmd_roadmap_clean_nav)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    # Catch common copy-paste: append_entries … --inline-grep … (grep is not a harness flag).
    if "append_entries" in argv and "--inline-grep" in argv:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "merged_grep_with_append_entries",
                    "hint": "Do not paste grep into the append_entries line. Run append_entries "
                    "with a heredoc, pipe, or --lines-file, then run grep as a separate command. "
                    "See: python3 -m scripts.eat_queue_core.harness append_entries --help",
                }
            ),
            file=sys.stderr,
        )
        return 2
    p = build_parser()
    args = p.parse_args(argv)
    vault_root = Path(args.vault_root or Path.cwd()).resolve()
    args.resolved_config = resolve_harness_config_path(
        vault_root, getattr(args, "config", None)
    )

    fn = args.func
    return int(fn(vault_root, args))


if __name__ == "__main__":
    raise SystemExit(main())
