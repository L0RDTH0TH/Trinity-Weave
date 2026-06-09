"""Phase A — L3 fault-injection drills (controlled proof, institute/maintenance lanes)."""

from __future__ import annotations

import json
import os
import shutil
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from ..handoff_build import bundle_dir_for_lane
from ..lane_recovery import (
    load_lane_stall,
    primary_code_from_eat_result,
    record_lane_stall,
    run_recovery_cycle,
    write_lane_stall,
)
from ..pq_lock import acquire, read_lock, release, wait_for_lock_available
from ..recoverable_codes import classify_primary_code
from ..recoverable_handlers import run_recoverable_handler
from .governance import append_metric_row, ensure_weave_paths
from .l3_self_heal import latest_l3_metric


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass
class BundleSnapshot:
    lock_bytes: bytes | None = None
    stall_bytes: bytes | None = None
    file_backups: dict[str, bytes] = field(default_factory=dict)
    removed_paths: list[str] = field(default_factory=list)


def _snapshot_bundle(bundle: Path) -> BundleSnapshot:
    snap = BundleSnapshot()
    lock = bundle / "pq.lock"
    stall = bundle / "lane-stall.json"
    if lock.is_file():
        snap.lock_bytes = lock.read_bytes()
    if stall.is_file():
        snap.stall_bytes = stall.read_bytes()
    return snap


def _restore_bundle(bundle: Path, snap: BundleSnapshot) -> None:
    lock = bundle / "pq.lock"
    stall = bundle / "lane-stall.json"
    if snap.lock_bytes is None:
        lock.unlink(missing_ok=True)
    else:
        lock.write_bytes(snap.lock_bytes)
    if snap.stall_bytes is None:
        stall.unlink(missing_ok=True)
    else:
        stall.write_bytes(snap.stall_bytes)
    for rel, content in snap.file_backups.items():
        p = bundle / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
    for rel in snap.removed_paths:
        p = bundle / rel
        if not p.exists() and rel not in snap.file_backups:
            pass


def _count_l3_metrics(vault_root: Path) -> int:
    path = vault_root / ".technical" / "weave" / "metrics.jsonl"
    if not path.is_file():
        return 0
    n = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and row.get("metric_type") == "l3_self_heal":
            n += 1
    return n


def _result(
    drill_id: str,
    *,
    passed: bool,
    checks: list[dict[str, Any]],
    detail: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "drill_id": drill_id,
        "passed": passed,
        "checks": checks,
        "detail": detail or {},
        "timestamp": _utc_iso(),
    }


def drill_stale_pq_lock(vault_root: Path, lane: str, *, dry_run: bool = False) -> dict[str, Any]:
    """Dead PID on pq.lock → release_pq_lock → recovery cycle → l3_self_heal metric."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    bundle = bundle_dir_for_lane(vault_root, lane)
    checks: list[dict[str, Any]] = []

    if dry_run:
        return _result(
            "stale_pq_lock",
            passed=True,
            checks=[{"name": "dry_run", "ok": True}],
            detail={"would": "inject dead PID lock, run recovery cycle"},
        )

    snap = _snapshot_bundle(bundle)
    metrics_before = _count_l3_metrics(vault_root)
    drill_run_id = f"l3-drill-stale-{_utc_stamp()}"

    try:
        ok, _ = acquire(bundle, holder="l3_drill_stale")
        checks.append({"name": "acquire_test_lock", "ok": ok})
        lock_path = bundle / "pq.lock"
        text = lock_path.read_text(encoding="utf-8")
        lock_path.write_text(text.replace(str(os.getpid()), "999999999"), encoding="utf-8")
        lock_data = read_lock(bundle)
        checks.append(
            {
                "name": "inject_dead_pid",
                "ok": lock_data is not None and str(lock_data.get("pid")) == "999999999",
            }
        )

        handler_out = run_recoverable_handler("release_pq_lock", vault_root, lane, {})
        checks.append(
            {
                "name": "handler_clears_stale_lock",
                "ok": bool(handler_out.get("cleared")) or handler_out.get("clear_reason") == "stale_or_dead_pid",
                "handler_out": handler_out,
            }
        )
        checks.append({"name": "lock_cleared_by_handler", "ok": read_lock(bundle) is None})

        ok2, _ = acquire(bundle, holder="l3_drill_stale")
        lock_path.write_text(
            lock_path.read_text(encoding="utf-8").replace(str(os.getpid()), "999999999"),
            encoding="utf-8",
        )
        checks.append({"name": "reinject_for_recovery_cycle", "ok": ok2 and read_lock(bundle) is not None})

        classification = classify_primary_code("pq_locked")
        checks.append(
            {
                "name": "handler_is_release_pq_lock",
                "ok": classification.get("handler") == "release_pq_lock",
                "handler": classification.get("handler"),
            }
        )

        recorded = record_lane_stall(
            vault_root,
            lane,
            "pq_locked",
            receipt={"ok": False, "error": "pq_locked", "detail": "locked_by:l3_drill_stale"},
            extra={"drill_run_id": drill_run_id},
        )
        checks.append({"name": "stall_recorded", "ok": bool(recorded.get("ok"))})

        recovery = run_recovery_cycle(
            vault_root, lane, architect_decision="proceed", dry_run=False, eat_retry=False
        )
        checks.append(
            {
                "name": "recovery_ok",
                "ok": bool(recovery.get("ok")),
                "handler": recovery.get("handler"),
                "reason": recovery.get("reason"),
            }
        )
        checks.append(
            {
                "name": "lock_cleared_after_recovery",
                "ok": read_lock(bundle) is None,
            }
        )

        metrics_after = _count_l3_metrics(vault_root)
        metric_delta = metrics_after - metrics_before
        last_metric = latest_l3_metric(vault_root)
        checks.append(
            {
                "name": "l3_self_heal_metric_appended",
                "ok": metric_delta >= 1,
                "delta": metric_delta,
                "last_handler": (last_metric or {}).get("handler"),
            }
        )

        passed = all(c.get("ok") for c in checks)
        return _result(
            "stale_pq_lock",
            passed=passed,
            checks=checks,
            detail={"recovery": recovery, "recorded": recorded, "drill_run_id": drill_run_id},
        )
    finally:
        _restore_bundle(bundle, snap)
        release(bundle)


def drill_live_pq_lock_wait(vault_root: Path, lane: str, *, dry_run: bool = False) -> dict[str, Any]:
    """Live holder → wait (not instant wrong handler); release_pq_lock skips alive holder."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    bundle = bundle_dir_for_lane(vault_root, lane)
    checks: list[dict[str, Any]] = []

    if dry_run:
        return _result(
            "live_pq_lock_wait",
            passed=True,
            checks=[{"name": "dry_run", "ok": True}],
            detail={"would": "hold live lock, verify wait + handler skip"},
        )

    snap = _snapshot_bundle(bundle)
    try:
        ok, _ = acquire(bundle, holder="l3_drill_live")
        checks.append({"name": "acquire_live_lock", "ok": ok})

        handler_out = run_recoverable_handler("release_pq_lock", vault_root, lane, {})
        checks.append(
            {
                "name": "release_skips_live_holder",
                "ok": bool(handler_out.get("skipped")) and handler_out.get("reason") == "holder_alive",
                "handler_out": handler_out,
            }
        )
        checks.append({"name": "lock_still_held", "ok": read_lock(bundle) is not None})

        wait_out = wait_for_lock_available(
            bundle,
            timeout_seconds=2.0,
            poll_seconds=0.5,
            clear_stale=False,
        )
        checks.append(
            {
                "name": "wait_times_out_on_live_holder",
                "ok": wait_out.get("reason") == "wait_timeout" and not wait_out.get("available"),
                "wait_out": wait_out,
            }
        )

        eat_fail = {
            "ok": False,
            "error": "pq_locked",
            "detail": wait_out.get("reason", "wait_timeout") + ":locked_by:l3_drill_live",
        }
        primary = primary_code_from_eat_result(eat_fail)
        mapped = classify_primary_code(primary)
        checks.append(
            {
                "name": "wait_timeout_maps_to_pq_locked",
                "ok": primary == "pq_locked",
                "primary_code": primary,
            }
        )
        checks.append(
            {
                "name": "not_refresh_lane_board_regression",
                "ok": mapped.get("handler") == "release_pq_lock",
                "handler": mapped.get("handler"),
            }
        )

        passed = all(c.get("ok") for c in checks)
        return _result("live_pq_lock_wait", passed=passed, checks=checks, detail={"wait_out": wait_out})
    finally:
        release(bundle)
        _restore_bundle(bundle, snap)


def drill_missing_pq_bundle(vault_root: Path, lane: str, *, dry_run: bool = False) -> dict[str, Any]:
    """Missing PQ bundle files → ensure_lane_bundle restores allowlisted files."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    bundle = bundle_dir_for_lane(vault_root, lane)
    targets = (
        "prompt-queue.jsonl",
        "queue-continuation.jsonl",
        "prompt-queue-audit.jsonl",
    )
    checks: list[dict[str, Any]] = []

    if dry_run:
        return _result(
            "missing_pq_bundle",
            passed=True,
            checks=[{"name": "dry_run", "ok": True}],
            detail={"would": "remove bundle files, run ensure_lane_bundle"},
        )

    snap = _snapshot_bundle(bundle)
    try:
        for name in targets:
            p = bundle / name
            if p.is_file():
                snap.file_backups[name] = p.read_bytes()
                p.unlink()
                snap.removed_paths.append(name)

        classification = classify_primary_code("missing_pq_parent")
        checks.append(
            {
                "name": "handler_is_ensure_lane_bundle",
                "ok": classification.get("handler") == "ensure_lane_bundle",
                "handler": classification.get("handler"),
            }
        )

        patch = run_recoverable_handler("ensure_lane_bundle", vault_root, lane, {})
        checks.append({"name": "ensure_handler_ok", "ok": bool(patch.get("ok")), "patch": patch})

        recreated = all((bundle / name).is_file() for name in targets)
        checks.append({"name": "bundle_files_recreated", "ok": recreated})

        recorded = record_lane_stall(
            vault_root,
            lane,
            "missing_pq_parent",
            receipt={"ok": False, "error": "missing_pq_parent"},
            extra={"drill": "missing_pq_bundle"},
        )
        stall = load_lane_stall(vault_root, lane) or {}
        stall["recovery_attempt"] = 0
        stall["l3_heal_attempts"] = 0
        stall["stall_id"] = str(uuid.uuid4())
        write_lane_stall(vault_root, lane, stall)

        recovery = run_recovery_cycle(
            vault_root, lane, architect_decision="proceed", dry_run=False, eat_retry=False
        )
        checks.append(
            {
                "name": "recovery_cycle_ok",
                "ok": bool(recovery.get("ok")) or recovery.get("reason") == "not_recoverable",
                "recovery": recovery,
            }
        )

        passed = all(
            c.get("ok")
            for c in checks
            if c["name"] in ("handler_is_ensure_lane_bundle", "ensure_handler_ok", "bundle_files_recreated")
        )
        return _result(
            "missing_pq_bundle",
            passed=passed,
            checks=checks,
            detail={"patch": patch, "recovery": recovery, "recorded": recorded},
        )
    finally:
        _restore_bundle(bundle, snap)


DRILL_FUNCS: dict[str, Callable[..., dict[str, Any]]] = {
    "stale_pq_lock": drill_stale_pq_lock,
    "live_pq_lock_wait": drill_live_pq_lock_wait,
    "missing_pq_bundle": drill_missing_pq_bundle,
}


def run_l3_validation_drill(
    vault_root: Path,
    lane: str = "institute",
    *,
    drill: str = "all",
    dry_run: bool = False,
    write_report: bool = True,
) -> dict[str, Any]:
    """Run one or all L3 drills; write JSON evidence under .technical/weave/validation/."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    ensure_weave_paths(vault_root)

    names = list(DRILL_FUNCS.keys()) if drill.strip().lower() == "all" else [drill.strip().lower()]
    unknown = [n for n in names if n not in DRILL_FUNCS]
    if unknown:
        return {
            "ok": False,
            "error": "unknown_drill",
            "unknown": unknown,
            "valid": list(DRILL_FUNCS.keys()),
        }

    bundle = bundle_dir_for_lane(vault_root, lane)
    if read_lock(bundle) is not None:
        return {"ok": False, "error": "lane_locked", "lane": lane, "hint": "clear pq.lock before drill"}

    results: list[dict[str, Any]] = []
    for name in names:
        results.append(DRILL_FUNCS[name](vault_root, lane, dry_run=dry_run))

    all_passed = all(r.get("passed") for r in results)
    report = {
        "ok": all_passed,
        "phase": "A",
        "layer": "L3",
        "lane": lane,
        "dry_run": dry_run,
        "drills": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r.get("passed")),
            "failed": sum(1 for r in results if not r.get("passed")),
        },
        "timestamp": _utc_iso(),
    }

    if write_report and not dry_run:
        out_dir = vault_root / ".technical" / "weave" / "validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"l3-drill-{_utc_stamp()}.json"
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(out_path)
        append_metric_row(
            vault_root,
            {
                "metric_type": "l3_validation_drill",
                "lane": lane,
                "ok": all_passed,
                "passed": report["summary"]["passed"],
                "failed": report["summary"]["failed"],
                "report_path": str(out_path),
            },
        )

    return report
