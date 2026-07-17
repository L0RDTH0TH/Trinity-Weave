"""Factory-Run-Summary rollup from correlation logs + dispatch."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .factory_correlation import FactoryRunContext, factory_run_log_path, gate_log_path

DISPATCH_DIR_REL = ".technical/factory/dispatch"
SUMMARIES_DIR_REL = ".technical/factory/summaries"


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_jsonl(path: Path, limit: int = 200) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines()[-limit:]:
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def write_factory_run_summary(
    vault_root: Path,
    *,
    run_id: str | None = None,
    lanes: tuple[str, ...] = ("godot", "asset", "techart", "content", "presentation", "audio", "module"),
) -> Path:
    vault_root = vault_root.resolve()
    out_dir = vault_root / ".technical" / "factory"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = run_id or f"factory-run-{stamp}"
    path = out_dir / f"Factory-Run-Summary-{stamp}.md"

    dispatch: dict[str, Any] = {}
    latest = out_dir / "dispatch" / "latest.json"
    if latest.is_file():
        dispatch = json.loads(latest.read_text(encoding="utf-8"))

    gate_rows = _read_jsonl(gate_log_path(vault_root))
    lane_events: dict[str, list[dict[str, Any]]] = {}
    for lane in lanes:
        lane_events[lane] = _read_jsonl(factory_run_log_path(vault_root, lane))

    lines = [
        "---",
        f"title: Factory Run Summary — {stamp}",
        f"created: {stamp[:10]}",
        "tags: [factory, correlation]",
        "para-type: Resource",
        "---",
        "",
        f"# Factory Run Summary",
        "",
        f"**run_id:** `{run_id}`  ",
        f"**generated:** {_utc_iso()}",
        "",
        "## Dispatch",
        "",
        f"- active_slice: `{dispatch.get('active_slice', {}).get('id', 'n/a')}`",
        f"- jobs: {len(dispatch.get('jobs') or [])}",
        f"- ok_to_implement: `{dispatch.get('ok_to_implement')}`",
        "",
        "## Gate log (recent)",
        "",
    ]
    for row in gate_rows[-15:]:
        lines.append(
            f"- `{row.get('pass_name')}` ok={row.get('ok')} slice={row.get('slice_id')} "
            f"violations={row.get('violations')}"
        )
    lines.append("")
    lines.append("## Lane events (recent)")
    lines.append("")
    for lane, events in lane_events.items():
        if not events:
            continue
        lines.append(f"### {lane}")
        for ev in events[-5:]:
            lines.append(
                f"- `{ev.get('event')}` status={ev.get('status')} "
                f"factory_lane={ev.get('factory_lane')} slice={ev.get('slice_id')}"
            )
        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _seat_lines(passes: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for name, info in passes.items():
        if isinstance(info, dict):
            ok = info.get("ok")
            detail = info.get("detail", "")
        else:
            ok = getattr(info, "ok", False)
            detail = getattr(info, "detail", "")
        lines.append(f"- `{name}` ok={ok} — {detail}")
    return lines


def write_lane_run_summary(
    vault_root: Path,
    *,
    ctx: FactoryRunContext,
    receipt_id: str,
    lane_seats: dict[str, Any],
    changed_paths: tuple[str, ...] = (),
    agent_ok: bool = True,
) -> Path:
    """Scoped summary after one factory_lane job completes."""
    vault_root = vault_root.resolve()
    out_dir = vault_root / SUMMARIES_DIR_REL
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = f"lane-{ctx.slice_id}-{ctx.factory_lane}-{stamp}.md"
    path = out_dir / fname

    passes = lane_seats.get("passes", lane_seats) if isinstance(lane_seats, dict) else {}
    seat_summary = {
        k: {"ok": v.ok, "detail": v.detail}
        if hasattr(v, "ok")
        else v
        for k, v in (passes.items() if isinstance(passes, dict) else {})
    }

    lines = [
        "---",
        f"title: Lane Run — {ctx.slice_id}/{ctx.factory_lane}",
        f"created: {stamp[:10]}",
        "tags: [factory, lane-summary]",
        "para-type: Resource",
        "---",
        "",
        f"# Lane run — `{ctx.factory_lane}` @ `{ctx.slice_id}`",
        "",
        f"**run_id:** `{ctx.run_id}`  ",
        f"**chain_id:** `{ctx.chain_id}`  ",
        f"**receipt_id:** `{receipt_id}`  ",
        f"**agent_ok:** `{agent_ok}`  ",
        f"**generated:** {_utc_iso()}",
        "",
        "## Changed paths",
        "",
    ]
    if changed_paths:
        for p in changed_paths:
            lines.append(f"- `{p}`")
    else:
        lines.append("- _(none detected)_")
    lines.append("")
    lines.append("## Lane seats")
    lines.append("")
    lines.extend(_seat_lines(seat_summary))
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    latest = out_dir / "latest-lane.md"
    latest.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return path


def write_slice_run_summary(
    vault_root: Path,
    *,
    ctx: FactoryRunContext,
    receipt_id: str,
    slice_exit_gates: dict[str, Any],
    all_lanes_done: bool,
    slice_complete: bool,
    advance: dict[str, Any] | None = None,
    playtest_brief: dict[str, Any] | None = None,
) -> Path | None:
    """Slice rollup when all lanes finish (even if exit gates block advance)."""
    if not all_lanes_done:
        return None

    vault_root = vault_root.resolve()
    out_dir = vault_root / SUMMARIES_DIR_REL
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = f"slice-{ctx.slice_id}-{stamp}.md"
    path = out_dir / fname

    passes = slice_exit_gates.get("passes", {}) if isinstance(slice_exit_gates, dict) else {}
    seat_summary = {
        k: {"ok": v.ok, "detail": v.detail}
        if hasattr(v, "ok")
        else v
        for k, v in passes.items()
    }

    lines = [
        "---",
        f"title: Slice Run — {ctx.slice_id}",
        f"created: {stamp[:10]}",
        "tags: [factory, slice-summary]",
        "para-type: Resource",
        "---",
        "",
        f"# Slice run — `{ctx.slice_id}`",
        "",
        f"**run_id:** `{ctx.run_id}`  ",
        f"**chain_id:** `{ctx.chain_id}`  ",
        f"**receipt_id:** `{receipt_id}`  ",
        f"**all_lanes_done:** `{all_lanes_done}`  ",
        f"**slice_exit_gates_pass:** `{slice_complete}`  ",
        f"**generated:** {_utc_iso()}",
        "",
        "## Slice exit gates",
        "",
    ]
    lines.extend(_seat_lines(seat_summary))
    if advance:
        lines.extend(["", "## Advance", "", f"- advanced: `{advance.get('advanced')}`", f"- reason: {advance.get('reason', '')}"])
    if playtest_brief and not playtest_brief.get("skipped"):
        lines.extend(["", "## Playtest brief", "", f"- path: `{playtest_brief.get('path', 'n/a')}`"])
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    latest = out_dir / "latest-slice.md"
    latest.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return path
