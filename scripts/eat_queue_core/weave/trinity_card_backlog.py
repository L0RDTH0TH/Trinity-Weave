"""Phase 7 — ranked Trinity card backlog (drift × usage)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .governance import append_metric_row, ensure_weave_paths, metrics_path
from .trinity_align import check


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass
class BacklogEntry:
    trinity_id: str
    drift_score: float
    usage_count: int
    priority_score: float
    stale_touch: bool
    disconnect_kinds: list[str]
    align_ok: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "trinity_id": self.trinity_id,
            "drift_score": round(self.drift_score, 2),
            "usage_count": self.usage_count,
            "priority_score": round(self.priority_score, 2),
            "stale_touch": self.stale_touch,
            "disconnect_kinds": self.disconnect_kinds,
            "align_ok": self.align_ok,
        }


def _parse_metric_ts(raw: str) -> datetime | None:
    s = str(raw or "").strip()
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def count_trinity_usage(
    vault_root: Path,
    *,
    max_lines: int = 8000,
    lookback_days: int | None = 30,
) -> dict[str, int]:
    """Count metric rows mentioning each trinity_id (bounded tail read)."""
    path = metrics_path(vault_root)
    if not path.is_file():
        return {}
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if len(lines) > max_lines:
        lines = lines[-max_lines:]
    cutoff: datetime | None = None
    if lookback_days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=max(1, lookback_days))
    counts: dict[str, int] = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        tid = str(row.get("trinity_id") or "").strip()
        if not tid:
            continue
        if cutoff is not None:
            ts = _parse_metric_ts(str(row.get("timestamp") or ""))
            if ts is not None and ts < cutoff:
                continue
        counts[tid] = counts.get(tid, 0) + 1
    return counts


def _drift_score_for_align(align: Any) -> float:
    score = 0.0
    if not align.ok:
        score += 10.0
    if align.stale_touch:
        score += 5.0
    score += float(len(align.disconnects)) * 3.0
    for leg, ok in (align.legs or {}).items():
        if leg != "touch_fresh" and not ok:
            score += 2.0
    return score


def _scope_trinity_ids(vault_root: Path, *, maintenance_only: bool) -> list[str]:
    if maintenance_only:
        from .trinity_partition import load_maintenance_trinity_ids

        bundle = load_maintenance_trinity_ids(vault_root)
        return list(bundle.all)
    from .trinity_card_paths import list_trinity_card_ids

    return list_trinity_card_ids(vault_root, pilot_only=False, include_provisional=True)


def assess_trinity_card_backlog(
    vault_root: Path,
    *,
    maintenance_only: bool = True,
    top_n: int | None = None,
    write_report: bool = True,
    metrics_max_lines: int = 8000,
    lookback_days: int | None = 30,
) -> dict[str, Any]:
    """Rank cards by priority_score = drift × (1 + usage_weight)."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled:
        return {"ok": True, "skipped": True, "reason": "trinity_disabled"}

    cap = int(top_n if top_n is not None else cfg.backlog_top_n)
    usage = count_trinity_usage(
        vault_root,
        max_lines=metrics_max_lines,
        lookback_days=lookback_days,
    )
    usage_weight = float(cfg.backlog_usage_weight)

    ranked: list[BacklogEntry] = []
    for tid in _scope_trinity_ids(vault_root, maintenance_only=maintenance_only):
        align = check(vault_root, tid, run_behavior_proofs=False)
        drift = _drift_score_for_align(align)
        u = int(usage.get(tid, 0))
        priority = drift * (1.0 + min(u, 100) * usage_weight)
        if drift <= 0 and u <= 0:
            continue
        ranked.append(
            BacklogEntry(
                trinity_id=tid,
                drift_score=drift,
                usage_count=u,
                priority_score=priority,
                stale_touch=align.stale_touch,
                disconnect_kinds=[d.kind for d in align.disconnects],
                align_ok=align.ok,
            )
        )

    ranked.sort(key=lambda e: (-e.priority_score, -e.drift_score, e.trinity_id))
    top = ranked[:cap]

    report: dict[str, Any] = {
        "ok": True,
        "timestamp": _now_iso(),
        "maintenance_only": maintenance_only,
        "top_n": cap,
        "candidates": len(ranked),
        "ranked": [e.to_dict() for e in top],
        "all_scores": [e.to_dict() for e in ranked[: min(len(ranked), cap * 3)]],
    }

    if write_report:
        ensure_weave_paths(vault_root)
        out_dir = vault_root / ".technical" / "weave" / "validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"trinity-card-backlog-{_stamp()}.json"
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(out_path)
        append_metric_row(
            vault_root,
            {
                "metric_type": "trinity_card_backlog",
                "ok": True,
                "top_n": cap,
                "candidates": len(ranked),
                "top_id": top[0].trinity_id if top else None,
                "report_path": str(out_path),
            },
        )

    return report


def format_backlog_board_hint(ranked: list[dict[str, Any]], *, max_rows: int = 5) -> str:
    """Markdown lines for lane board Trinity spine subsection."""
    if not ranked:
        return "> **Backlog:** no drift/usage candidates.\n"
    lines = [
        f"> **Backlog** (drift × usage, top {min(max_rows, len(ranked))}):",
        "",
        "| trinity_id | priority | drift | usage | disconnect |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in ranked[:max_rows]:
        disc = ", ".join(row.get("disconnect_kinds") or []) or "none"
        if len(disc) > 40:
            disc = disc[:37] + "…"
        lines.append(
            f"| `{row.get('trinity_id')}` | {row.get('priority_score', 0):.1f} "
            f"| {row.get('drift_score', 0):.1f} | {row.get('usage_count', 0)} | {disc} |"
        )
    lines.append("")
    lines.append(
        "> Harness: `assess_trinity_card_backlog --vault-root .` · "
        "PQ hint: `params.trinity_backlog_top` from ranked ids."
    )
    return "\n".join(lines) + "\n"


def maybe_backlog_on_pseudo_clock(vault_root: Path) -> dict[str, Any] | None:
    """Bounded backlog assess on pseudo-clock tick (optional)."""
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled or not cfg.backlog_on_pseudo_clock:
        return None
    return assess_trinity_card_backlog(
        vault_root,
        maintenance_only=True,
        top_n=cfg.backlog_top_n,
        write_report=False,
    )


def backlog_hint_for_params(
    vault_root: Path,
    *,
    top_n: int = 3,
    min_priority: float = 8.0,
) -> dict[str, Any]:
    """Optional maintenance PQ params overlay (advisory ids only)."""
    bl = assess_trinity_card_backlog(
        vault_root,
        maintenance_only=True,
        top_n=top_n,
        write_report=False,
    )
    ranked = bl.get("ranked") or []
    ids = [
        str(r["trinity_id"])
        for r in ranked
        if float(r.get("priority_score") or 0) >= min_priority
    ]
    if not ids:
        return {}
    return {"trinity_backlog_top": ids[:top_n]}
