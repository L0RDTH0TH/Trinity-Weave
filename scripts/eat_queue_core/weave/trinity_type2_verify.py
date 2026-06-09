"""Type-2 verify — full-corpus self-wrap without regenerate-complete (steady-state audit)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ARTIFACT_DIR = Path(".technical/weave/validation")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run_type2_verify(
    vault_root: Path,
    *,
    dry_run: bool = False,
    skip_observe: bool = False,
    write_artifact: bool = True,
) -> dict[str, Any]:
    """Run trinity_weave_self_wrap --full-corpus without --regenerate-complete."""
    vault_root = vault_root.resolve()
    started = _now_iso()

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "phase": "type2_verify",
            "hint": "Run without --dry-run to execute full-corpus self-wrap",
            "command": "trinity_weave_self_wrap --full-corpus (no --regenerate-complete)",
        }

    from .trinity_weave_self_wrap import run_trinity_weave_self_wrap

    wrap = run_trinity_weave_self_wrap(
        vault_root,
        dry_run=False,
        corps_full_corpus=True,
        regenerate_complete=False,
        skip_observe=skip_observe,
        write_report=True,
    )

    op = wrap.get("operator_outcome") or {}
    pg = wrap.get("pass_gate") or {}

    report: dict[str, Any] = {
        "ok": bool(op.get("cycle_ok")) and bool(op.get("pass_gate_ok")),
        "phase": "type2_verify",
        "started_at": started,
        "completed_at": _now_iso(),
        "regenerate_complete": False,
        "cycle_ok": op.get("cycle_ok"),
        "pass_gate_ok": op.get("pass_gate_ok"),
        "operator_mode": op.get("operator_mode"),
        "summary": op.get("summary"),
        "counts": op.get("counts"),
        "red_ids": op.get("red_ids"),
        "infra_failures": op.get("infra_failures"),
        "report_path": wrap.get("report_path"),
        "self_wrap_ok": wrap.get("ok"),
    }

    steps = {
        k: wrap.get(k)
        for k in (
            "host_weld_sync",
            "knob_parity",
            "honesty_anchor",
            "pass_gate",
            "corps_sweep",
        )
        if wrap.get(k)
    }
    report["step_summaries"] = {
        k: {"ok": (v or {}).get("ok"), "skipped": (v or {}).get("skipped")}
        for k, v in steps.items()
    }
    report["pass_gate_detail"] = {
        "ok": pg.get("ok"),
        "conduct_ok": pg.get("conduct_ok"),
        "counts": pg.get("counts"),
        "red_count": pg.get("red_count"),
    }

    if write_artifact:
        out_dir = vault_root / ARTIFACT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)
        artifact = out_dir / f"type2-verify-{_stamp()}.json"
        artifact.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["artifact_path"] = str(artifact.relative_to(vault_root))

    append_row = {
        "metric_type": "type2_verify",
        "ok": report.get("ok"),
        "pass_gate_ok": report.get("pass_gate_ok"),
        "cycle_ok": report.get("cycle_ok"),
    }
    from .governance import append_metric_row

    append_metric_row(vault_root, append_row)

    return report
