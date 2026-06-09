"""Overnight corps batch driver — hygiene + nerve test with offset pagination."""

from __future__ import annotations

import copy
import json
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .governance import ensure_weave_paths
from .trinity_align import check
from .trinity_card_paths import (
    list_provisional_trinity_card_ids,
    load_trinity_card,
    write_trinity_card,
)
from .trinity_catchup_sweep import curate_stale_non_core
from .trinity_dual_lock import is_maintenance_core_id
from .corps_smoke_test import ensure_smoke_test_file
from .trinity_provisional_corps_sweep import (
    apply_corps_precedence_hygiene,
    run_nerve_test_one,
    write_corps_nerve_map,
    _wire_tests_if_missing,
)

CORPS_OVERNIGHT_STATUS_JSON = Path(".technical/weave/corps-overnight-status.json")
CORPS_OVERNIGHT_STATUS_MD = Path(".technical/weave/corps-overnight-status.md")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(msg: str) -> None:
    print(f"[{_now_iso()}] {msg}", flush=True, file=sys.stderr)


def _apply_progress_fields(status: dict[str, Any]) -> None:
    """Mutate status with summary + progress_pct (in-memory + file)."""
    status["summary"] = _status_summary(status)
    if status.get("batch_total"):
        cur = int(status.get("batch_current") or 0)
        status["progress_pct"] = round(100.0 * cur / int(status["batch_total"]), 1)
    else:
        status["progress_pct"] = 0.0


def _terminal_progress(status: dict[str, Any]) -> None:
    """One grep-friendly line for `tail -f` on nohup logs (stderr)."""
    cum = status.get("cumulative_counts") or {}
    card = status.get("current_trinity_id") or "-"
    idx = status.get("card_index_in_batch")
    in_batch = status.get("cards_in_batch")
    card_pos = f" card {idx}/{in_batch}" if idx and in_batch else ""
    line = (
        f"CORPS_PROGRESS run={status.get('run_state')} "
        f"batch={status.get('batch_current')}/{status.get('batch_total')} "
        f"({status.get('progress_pct', 0)}%) "
        f"phase={status.get('phase')}{card_pos} "
        f"id={card} "
        f"green={cum.get('green', 0)} yellow={cum.get('yellow', 0)} red={cum.get('red', 0)} "
        f"failures={status.get('red_failures_total', 0)} "
        f"write_err={status.get('write_errors_total', 0)}"
    )
    print(line, flush=True, file=sys.stderr)


def _batch_total(card_count: int, start_offset: int, batch_size: int) -> int:
    if card_count <= start_offset or batch_size <= 0:
        return 0
    remaining = card_count - start_offset
    return (remaining + batch_size - 1) // batch_size


def _status_summary(status: dict[str, Any]) -> str:
    run = status.get("run_state") or "unknown"
    cur = status.get("batch_current") or 0
    tot = status.get("batch_total") or 0
    phase = status.get("phase") or ""
    tid = status.get("current_trinity_id") or ""
    g = (status.get("cumulative_counts") or {}).get("green", 0)
    r = (status.get("cumulative_counts") or {}).get("red", 0)
    base = f"{run} — batch {cur}/{tot}"
    if phase:
        base += f" — {phase}"
    if tid:
        base += f" — {tid}"
    base += f" — cumulative green={g} red={r}"
    return base


def write_corps_overnight_status(vault_root: Path, status: dict[str, Any]) -> Path:
    """Persist live progress (JSON + short Markdown for operators)."""
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    status["updated_at"] = _now_iso()
    _apply_progress_fields(status)

    json_path = vault_root / CORPS_OVERNIGHT_STATUS_JSON
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    md_path = vault_root / CORPS_OVERNIGHT_STATUS_MD
    lines = [
        "---",
        "title: Corps overnight status",
        f"run_state: {status.get('run_state')}",
        f"updated_at: {status.get('updated_at')}",
        "---",
        "",
        f"**{status.get('summary')}**",
        "",
        f"- **PID:** `{status.get('pid')}`",
        f"- **Started:** {status.get('started_at')}",
        f"- **Progress:** {status.get('progress_pct', 0)}% — batch {status.get('batch_current')} / {status.get('batch_total')}",
        f"- **Offset:** {status.get('offset')} (batch size {status.get('batch_size')})",
        f"- **Phase:** {status.get('phase')}",
        f"- **Current card:** `{status.get('current_trinity_id') or '—'}`",
        f"- **This batch:** {status.get('chunk_ids')}",
        f"- **Batch counts:** {status.get('batch_counts')}",
        f"- **Cumulative:** {status.get('cumulative_counts')}",
        f"- **Red failures so far:** {status.get('red_failures_total', 0)}",
        f"- **Write errors so far:** {status.get('write_errors_total', 0)}",
        "",
        f"JSON: `{CORPS_OVERNIGHT_STATUS_JSON.as_posix()}`",
    ]
    if status.get("error"):
        lines.extend(["", f"**Error:** {status.get('error')}"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path


def _publish_status(
    vault_root: Path,
    status: dict[str, Any],
    *,
    write_status: bool,
    terminal: bool = True,
) -> None:
    _apply_progress_fields(status)
    if terminal:
        _terminal_progress(status)
    if write_status:
        write_corps_overnight_status(vault_root, status)


def _install_stop_handlers(
    vault_root: Path,
    status: dict[str, Any],
    *,
    write_status: bool,
) -> None:
    """On SIGINT/SIGTERM, mark status stopped and flush before exit."""

    def _on_stop(signum: int, _frame: object) -> None:
        status.update(
            {
                "run_state": "stopped",
                "phase": "stopped",
                "error": f"signal {signum}",
            }
        )
        _publish_status(vault_root, status, write_status=write_status, terminal=True)
        _log(f"STOPPED by signal {signum}")
        raise SystemExit(128 + (signum if signum < 128 else 0))

    signal.signal(signal.SIGINT, _on_stop)
    signal.signal(signal.SIGTERM, _on_stop)


def run_corps_overnight_batches(
    vault_root: Path,
    *,
    start_offset: int | None = None,
    batch_size: int | None = None,
    stop_on_write_error: bool = False,
    auto_smoke_tests: bool = True,
    write_status: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    batch_size = batch_size or int(cfg.corps_cluster_batch_size or 7)
    if start_offset is None:
        start_offset = int(os.environ.get("CORPS_START_OFFSET", "0"))

    all_ids = list_provisional_trinity_card_ids(vault_root)
    batch_total = _batch_total(len(all_ids), start_offset, batch_size)
    started_at = _now_iso()
    cumulative = {"green": 0, "yellow": 0, "red": 0}

    status: dict[str, Any] = {
        "run_state": "running",
        "pid": os.getpid(),
        "started_at": started_at,
        "provisionals_total": len(all_ids),
        "start_offset": start_offset,
        "batch_size": batch_size,
        "batch_total": batch_total,
        "batch_current": 0,
        "offset": start_offset,
        "phase": "starting",
        "current_trinity_id": None,
        "chunk_ids": [],
        "batch_counts": {},
        "cumulative_counts": dict(cumulative),
        "red_failures_total": 0,
        "write_errors_total": 0,
        "status_json": CORPS_OVERNIGHT_STATUS_JSON.as_posix(),
        "status_md": CORPS_OVERNIGHT_STATUS_MD.as_posix(),
    }
    _install_stop_handlers(vault_root, status, write_status=write_status)
    _publish_status(vault_root, status, write_status=write_status)
    _log(
        f"START pid={os.getpid()} provisionals={len(all_ids)} "
        f"batches={batch_total} batch_size={batch_size} start_offset={start_offset}"
    )

    failures: list[dict[str, Any]] = []
    write_errors: list[dict[str, Any]] = []
    smoke_tests_created: list[str] = []
    batch_num = 0

    try:
        for offset in range(start_offset, len(all_ids), batch_size):
            chunk = all_ids[offset : offset + batch_size]
            if not chunk:
                break
            batch_num += 1
            status.update(
                {
                    "batch_current": batch_num,
                    "offset": offset,
                    "phase": "hygiene",
                    "current_trinity_id": None,
                    "chunk_ids": chunk,
                    "batch_counts": {},
                }
            )
            _publish_status(vault_root, status, write_status=write_status)
            _log(f"=== batch {batch_num}/{batch_total} offset={offset} ids={chunk} ===")
            hygiene_applied: list[str] = []

            for i, tid in enumerate(chunk):
                status["current_trinity_id"] = tid
                status["card_index_in_batch"] = i + 1
                status["cards_in_batch"] = len(chunk)
                _publish_status(vault_root, status, write_status=write_status)

                if is_maintenance_core_id(vault_root, tid):
                    continue
                try:
                    card = load_trinity_card(vault_root, tid, prefer="provisional")
                except (OSError, ValueError, FileNotFoundError) as e:
                    _log(f"  skip {tid}: {e}")
                    continue
                before = copy.deepcopy(card)
                if auto_smoke_tests:
                    for raw_path in (card.get("touch") or {}).get("primary_paths") or []:
                        rel = ensure_smoke_test_file(vault_root, str(raw_path))
                        if rel and rel not in smoke_tests_created:
                            smoke_tests_created.append(rel)
                new_card = _wire_tests_if_missing(
                    vault_root, apply_corps_precedence_hygiene(before)
                )
                if new_card != card:
                    try:
                        write_trinity_card(vault_root, tid, new_card, tier="provisional")
                        hygiene_applied.append(tid)
                    except (OSError, ValueError) as e:
                        write_errors.append(
                            {
                                "batch": batch_num,
                                "offset": offset,
                                "trinity_id": tid,
                                "error": str(e),
                            }
                        )
                        status["write_errors_total"] = len(write_errors)
                        _publish_status(vault_root, status, write_status=write_status)
                        _log(f"  WRITE_FAIL {tid}: {e}")
                        if stop_on_write_error:
                            raise
                align = check(vault_root, tid, run_behavior_proofs=False)
                if align.stale_touch:
                    curate_stale_non_core(vault_root, tid, align, dry_run=False)

            _log(f"  hygiene_applied={hygiene_applied}")

            nerves: list[dict[str, Any]] = []
            counts = {"green": 0, "yellow": 0, "red": 0}
            status["phase"] = "nerve_test"
            _publish_status(vault_root, status, write_status=write_status)

            for i, tid in enumerate(chunk):
                status["current_trinity_id"] = tid
                status["card_index_in_batch"] = i + 1
                _publish_status(vault_root, status, write_status=write_status)

                row = run_nerve_test_one(vault_root, tid, conduct_pending_ok=False)
                nerves.append(row)
                st = str(row.get("status") or "red")
                counts[st] = counts.get(st, 0) + 1
                cumulative[st] = cumulative.get(st, 0) + 1
                if st == "red":
                    failures.append(
                        {"batch": batch_num, "offset": offset, "trinity_id": tid, "row": row}
                    )
                    _log(f"  RED {tid}: {row.get('conduct', {}).get('disconnects')}")

            status["batch_counts"] = counts
            status["cumulative_counts"] = dict(cumulative)
            status["red_failures_total"] = len(failures)
            status["write_errors_total"] = len(write_errors)
            status["phase"] = "batch_complete"
            status["current_trinity_id"] = None
            _publish_status(vault_root, status, write_status=write_status)
            _log(f"  counts={counts}")

            write_corps_nerve_map(
                vault_root,
                {
                    "generated_at": _now_iso(),
                    "batch": batch_num,
                    "batch_total": batch_total,
                    "offset": offset,
                    "counts": counts,
                    "nerves": nerves,
                },
            )
            status["phase"] = "between_batches"
            _publish_status(vault_root, status, write_status=write_status)
            time.sleep(1)

        ok = len(failures) == 0 and len(write_errors) == 0
        status.update(
            {
                "run_state": "completed" if ok else "completed_with_failures",
                "phase": "done",
                "current_trinity_id": None,
                "ok": ok,
            }
        )
        _publish_status(vault_root, status, write_status=write_status)
        _log(
            f"DONE ok={ok} batches={batch_num}/{batch_total} "
            f"red_failures={len(failures)} write_errors={len(write_errors)}"
        )
        return {
            "ok": ok,
            "batches": batch_num,
            "batch_total": batch_total,
            "red_failures": failures,
            "write_errors": write_errors,
            "smoke_tests_created": smoke_tests_created,
            "start_offset": start_offset,
            "batch_size": batch_size,
            "status_json": str(vault_root / CORPS_OVERNIGHT_STATUS_JSON),
            "status_md": str(vault_root / CORPS_OVERNIGHT_STATUS_MD),
        }
    except BaseException as e:
        status.update(
            {
                "run_state": "failed",
                "phase": "failed",
                "error": str(e)[:500],
            }
        )
        _publish_status(vault_root, status, write_status=write_status)
        raise


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Corps overnight batch hygiene + nerve test")
    p.add_argument("--vault-root", default=".", type=Path)
    p.add_argument("--start-offset", type=int, default=None)
    p.add_argument("--batch-size", type=int, default=None)
    p.add_argument("--stop-on-write-error", action="store_true")
    p.add_argument(
        "--no-auto-smoke-tests",
        action="store_true",
        help="Skip auto-generating test_<module>.py stubs for strict conduct",
    )
    p.add_argument(
        "--no-status-file",
        action="store_true",
        help="Do not write corps-overnight-status.json / .md",
    )
    args = p.parse_args(argv)
    out = run_corps_overnight_batches(
        args.vault_root,
        start_offset=args.start_offset,
        batch_size=args.batch_size,
        stop_on_write_error=args.stop_on_write_error,
        auto_smoke_tests=not args.no_auto_smoke_tests,
        write_status=not args.no_status_file,
    )
    if out.get("red_failures"):
        _log("FAILURE_SUMMARY " + json.dumps(out["red_failures"][:30], default=str))
    if out.get("write_errors"):
        _log("WRITE_ERRORS " + json.dumps(out["write_errors"][:30], default=str))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
