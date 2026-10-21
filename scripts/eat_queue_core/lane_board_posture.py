"""Half 1 — Factory floor (G/Y/R callouts). Half 2 — Lanes by project."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .lane_board_factory_detail import km_metrics
from .lane_board_goal_packets import scan_expeditions
from .lane_registry import LaneRegistry, active_lane_ids
from .lane_snapshot import LaneSnapshot
from .lane_health_signals import lane_display_health
from .lane_status_board import _run_badge, _status_dot, worst_status
from .weave.user_story.product_factory_state import load_product_factory

WAREHOUSE_TRACK = "institute"
LIBRARY_OPERATOR = "Curator"
MUSEUM_OPERATOR = "Museum"


def _resolve_primary_project(registry: LaneRegistry, expeditions: list[Any]) -> str:
    for ex in expeditions:
        if ex.kind == "overnight" and ex.lifecycle == "active":
            pid = str((ex.packet or {}).get("project_id") or "").strip()
            if pid and pid in registry.displayed_projects:
                return pid
    for pg in registry.projects:
        if pg.tracks:
            return pg.project_id
    if registry.displayed_projects:
        return registry.displayed_projects[0]
    for ex in expeditions:
        if ex.kind == "overnight" and ex.packet:
            pid = str(ex.packet.get("project_id") or "").strip()
            if pid:
                return pid
    return ""


def _snap(registry: LaneRegistry, snapshots: dict[str, LaneSnapshot], lane: str) -> LaneSnapshot | None:
    return snapshots.get(lane)


def _health_dot_band(snap: LaneSnapshot | None, *, cfg: dict[str, Any]) -> str:
    if not snap:
        return "_no signal_"
    from .lane_health_signals import glow_strength

    score, band, _ = lane_display_health(snap, cfg)
    glow = glow_strength(score)
    return _status_dot(band, score=score, glow=glow).strip()


def _aggregate_snap(snaps: list[LaneSnapshot | None], *, cfg: dict[str, Any]) -> LaneSnapshot | None:
    present = [s for s in snaps if s is not None]
    if not present:
        return None
    bands = {
        str(i): lane_display_health(s, cfg)[1]
        for i, s in enumerate(present)
    }
    band = worst_status(bands)
    ranked = sorted(
        present,
        key=lambda s: {"red": 0, "yellow": 1, "green": 2}.get(lane_display_health(s, cfg)[1], 9),
    )
    return ranked[0]


def _ingest_batch_in_use(vault_root: Path) -> str:
    from .ingest_autopilot_config import INGEST_BATCH_GA_REL

    batch_path = vault_root / INGEST_BATCH_GA_REL
    if not batch_path.is_file():
        return "no ingest_batch"
    try:
        import json

        batch = json.loads(batch_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return "ingest_batch unreadable"
    if isinstance(batch, dict) and batch.get("confirmed_by_operator"):
        rid = str(batch.get("run_id") or "—")[:32]
        return f"ingest_batch armed · `{rid}`"
    return "ingest_batch draft"


def _warehouse_library_in_use(vault_root: Path, km: dict[str, int]) -> str:
    batch = _ingest_batch_in_use(vault_root)
    if "armed" in batch:
        return batch
    return f"backlog **{km['ingest_backlog']}** · stable **{km['stable_pending']}**"


def _warehouse_museum_in_use(
    vault_root: Path,
    registry: LaneRegistry,
    snapshots: dict[str, LaneSnapshot],
) -> str:
    from .lane_activity import resolve_lane_activity

    row = registry.rows.get(WAREHOUSE_TRACK)
    depth = row.pq_depth if row else 0
    activity = resolve_lane_activity(vault_root, WAREHOUSE_TRACK)
    focus = str(activity.get("focus_line") or "").strip()
    if focus:
        return focus
    snap = snapshots.get(WAREHOUSE_TRACK)
    att = (snap.run_attention or snap.run) if snap else "idle"
    if depth:
        return f"PQ depth **{depth}** · {att}"
    return att or "idle"


def _health_line(snap: LaneSnapshot | None, *, run_label: str = "") -> str:
    if not snap:
        return "_no signal_"
    from .lane_health_signals import glow_strength

    glow = glow_strength(snap.health_score)
    att = snap.run_attention or snap.run
    dot = _status_dot(snap.health_band, score=snap.health_score, glow=glow)
    run = _run_badge(snap.run, attention=att)
    extra = f" · {run_label}" if run_label else f" · {run}"
    return f"{dot}{extra}"


def build_weave_posture(
    vault_root: Path,
    registry: LaneRegistry,
    snapshots: dict[str, LaneSnapshot],
    *,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = cfg or {}
    active_ids = set(active_lane_ids(registry))
    active_snaps = {ln: snapshots[ln] for ln in active_ids if ln in snapshots}
    attention = (
        worst_status({ln: lane_display_health(s, cfg)[1] for ln, s in active_snaps.items()})
        if active_snaps
        else "green"
    )

    km = km_metrics(vault_root)
    expeditions = scan_expeditions(vault_root, registry=registry)
    primary_exp = next((ex for ex in expeditions if ex.primary), None)
    project_id = _resolve_primary_project(registry, expeditions)
    pf = load_product_factory(vault_root, project_id)
    cell = pf.get("implementation_cell") if isinstance(pf.get("implementation_cell"), dict) else {}
    impl_half = str(cell.get("phase") or "idle")
    half_a_phase = str(pf.get("phase") or "idle")
    blocked = str(pf.get("blocked_at") or "") or "—"
    op_loop = pf.get("operator_loop") or "—"

    council_required = [c["seat"] for c in registry.council if c.get("required_by")]
    council_last = ""
    for c in registry.council:
        if c.get("last_memory_line"):
            council_last = str(c["last_memory_line"])[:100]
            break

    dormant_count = len(registry.dormant.tracks)
    drift = [r.lane for r in registry.rows.values() if r.config_drift]
    primary_pg = next((p for p in registry.projects if p.project_id == project_id), None)
    impl_snap = _aggregate_snap(
        [snapshots.get(r.lane) for r in (primary_pg.seats if primary_pg else [])],
        cfg=cfg,
    )

    return {
        "system_attention": attention,
        "half_a": {"phase": half_a_phase, "operator_loop": op_loop, "blocked_at": blocked},
        "implementation": {"phase": impl_half, "project_id": project_id},
        "km": km,
        "overnight": {
            "lane": primary_exp.lane if primary_exp else "—",
            "status": primary_exp.status if primary_exp else "vacant",
            "run_id": str((primary_exp.packet or {}).get("run_id") or "—")[:40] if primary_exp else "—",
        },
        "council_required": council_required,
        "council_last": council_last,
        "dormant_bundle_count": dormant_count,
        "config_drift_lanes": drift,
        "active_project_count": len(registry.displayed_projects),
        "detected_project_count": len(registry.active_projects),
        "maintenance_snap": _snap(registry, snapshots, "maintenance"),
        "institute_snap": _snap(registry, snapshots, "institute"),
        "godot_snap": _snap(registry, snapshots, "godot"),
        "half_a_snap": _snap(registry, snapshots, "godot"),
        "impl_snap": impl_snap,
    }


def render_factory_floor_section(
    posture: dict[str, Any],
    registry: LaneRegistry,
    snapshots: dict[str, LaneSnapshot],
    *,
    cfg: dict[str, Any],
    vault_root: Path | None = None,
) -> str:
    att = posture["system_attention"]
    att_dot = _status_dot(att, score=None, glow={"green": 0.85, "yellow": 0.6, "red": 0.2}.get(att, 0.5))

    km = posture["km"]
    inst_snap = posture.get("institute_snap")
    lib_in_use = _warehouse_library_in_use(vault_root, km) if vault_root else f"backlog **{km['ingest_backlog']}**"
    museum_in_use = (
        _warehouse_museum_in_use(vault_root, registry, snapshots)
        if vault_root
        else "—"
    )
    lines = [
        f"> [!summary] Factory floor · active capacity {att_dot}",
        f"> **{posture['active_project_count']}** project(s) with lanes · "
        f"**{posture['detected_project_count']}** detected in `1-Projects/`",
        "",
        "> [!info] Weave engine · infrastructure only",
        f"> Lane `maintenance` · {_health_line(posture.get('maintenance_snap'))}",
        "",
        "> [!info] Knowledge Warehouse",
        f"> **Library** · **{LIBRARY_OPERATOR}** · track `{WAREHOUSE_TRACK}` · "
        f"{_health_dot_band(inst_snap, cfg=cfg)} · {lib_in_use}",
        f"> **Museum** · **{MUSEUM_OPERATOR}** · track `{WAREHOUSE_TRACK}` · "
        f"{_health_dot_band(inst_snap, cfg=cfg)} · {museum_in_use}",
    ]

    primary_pg = next((p for p in registry.projects if p.project_id == posture["implementation"]["project_id"]), None)
    has_displayed = bool(registry.displayed_projects)
    if has_displayed and primary_pg:
        half_a_dot = _health_dot_band(posture.get("half_a_snap"), cfg=cfg)
        impl_dot = _health_dot_band(posture.get("impl_snap"), cfg=cfg)
        lines.extend(
            [
                "",
                f"> [!info] Software Warehouse · `{posture['implementation']['project_id']}`",
                f"> **Half A (Roadmap)** · {half_a_dot} · `{posture['half_a']['phase']}` · "
                f"blocked `{posture['half_a']['blocked_at']}`",
                f"> **Half B (Implementation)** · {impl_dot} · `{posture['implementation']['phase']}`",
            ]
        )
    elif has_displayed:
        half_a_dot = _health_dot_band(posture.get("half_a_snap"), cfg=cfg)
        impl_dot = _health_dot_band(posture.get("impl_snap"), cfg=cfg)
        lines.extend(
            [
                "",
                f"> [!info] Software Warehouse · `{posture['implementation']['project_id']}`",
                f"> **Half A (Roadmap)** · {half_a_dot} · `{posture['half_a']['phase']}` · "
                f"blocked `{posture['half_a']['blocked_at']}`",
                f"> **Half B (Implementation)** · {impl_dot} · `{posture['implementation']['phase']}`",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "> [!info] Software Warehouse · _no project with bound lanes_",
                "> Detected folders in `1-Projects/` have no active track or seat binding.",
            ]
        )

    lines.extend(
        [
            "",
            f"> [!info] Overnight · `{posture['overnight']['lane']}` · **{posture['overnight']['status']}** · `{posture['overnight']['run_id']}`",
        ]
    )

    if posture["config_drift_lanes"]:
        lines.extend(
            [
                "",
                f"> [!warning] Config drift · lanes `{', '.join(posture['config_drift_lanes'])}` · "
                "Config `lane_project_id` ≠ live packet / `1-Projects/`",
            ]
        )

    return "\n".join(lines)


def render_lanes_by_project_section(
    registry: LaneRegistry,
    snapshots: dict[str, LaneSnapshot],
    *,
    vault_root: Path,
    cfg: dict[str, Any],
) -> str:
    from .lane_activity import resolve_lane_activity
    from .lane_board_drilldown import drilldown_link
    from .lane_health_signals import glow_strength

    sections: list[str] = []

    def _table_rows(group_lanes: list) -> list[str]:
        from .lane_status_board import (
            format_est_drain_display,
            format_norm,
            lane_receipts,
            last_success_iso,
        )

        header = (
            "| Factory / lane | Health | Run | Depth | Norm | Est. drain | Last success | Drill |"
        )
        sep = "|----------------|--------|-----|-------|------|------------|--------------|-------|"
        rows = [header, sep]
        for reg_row in group_lanes:
            ln = reg_row.lane
            if ln not in snapshots:
                continue
            snap = snapshots[ln]
            att = snap.run_attention or snap.run
            h_score, h_band, _ = lane_display_health(snap, cfg)
            glow = glow_strength(h_score)
            signals = snap.signals or {}
            rec = lane_receipts(vault_root, ln)
            norm = format_norm(signals.get("baseline_median"), snap.depth)
            est = format_est_drain_display(signals, in_flight=(att == "running"), cfg=cfg)
            last = last_success_iso(rec)
            drill = drilldown_link(ln, in_table=True, label="open")
            label = reg_row.visual
            if reg_row.lane_class == "system_operational":
                label = f"Weave engine · {ln}"
            elif reg_row.lane_class == "orchestration":
                label = f"Warehouse · {ln}"
            rows.append(
                f"| {label} | {_status_dot(h_band, score=h_score, glow=glow)} | "
                f"{_run_badge(snap.run, attention=att, cfg=cfg)} | {snap.depth} | {norm} | {est} | {last} | {drill} |"
            )
        return rows

    def _warehouse_table(vault_root: Path) -> str:
        inst_row = registry.rows.get(WAREHOUSE_TRACK)
        inst_snap = snapshots.get(WAREHOUSE_TRACK)
        if not inst_row or not inst_snap:
            return "_No warehouse track signal._"
        att = inst_snap.run_attention or inst_snap.run
        h_score, h_band, _ = lane_display_health(inst_snap, cfg)
        glow = glow_strength(h_score)
        drill = drilldown_link(WAREHOUSE_TRACK, in_table=True, label="open")
        km = km_metrics(vault_root)
        lib_use = _warehouse_library_in_use(vault_root, km)
        museum_use = _warehouse_museum_in_use(vault_root, registry, snapshots)
        header = (
            "| Sub-factory | Operator | Track | Health | Run | Depth | Est. drain | In use | Drill |"
        )
        sep = "|-------------|----------|-------|--------|-----|-------|------------|--------|-------|"
        from .lane_status_board import format_est_drain_display

        signals = inst_snap.signals or {}
        est = format_est_drain_display(signals, in_flight=(att == "running"), cfg=cfg)
        depth = inst_snap.depth
        dot = _status_dot(h_band, score=h_score, glow=glow)
        run = _run_badge(inst_snap.run, attention=att, cfg=cfg)
        rows = [
            header,
            sep,
            f"| Library | {LIBRARY_OPERATOR} | `{WAREHOUSE_TRACK}` | {dot} | {run} | {depth} | {est} | {lib_use} | {drill} |",
            f"| Museum | {MUSEUM_OPERATOR} | `{WAREHOUSE_TRACK}` | {dot} | {run} | {depth} | {est} | {museum_use} | {drill} |",
        ]
        return "\n".join(rows)

    maint = [r for r in registry.system.tracks if r.lane == "maintenance"]

    sections.append("### Weave engine\n")
    sections.append("\n".join(_table_rows(maint)) if maint else "_No engine lane._")

    sections.append("\n### Knowledge Warehouse\n")
    sections.append(
        "> [!info] **Library** = preserved information (Curator) · "
        "**Museum** = presentation · shared execution track `institute`."
    )
    sections.append("\n" + _warehouse_table(vault_root))

    for pg in registry.projects:
        sections.append(f"\n### Software Warehouse · `{pg.project_id}`\n")
        sections.append("#### Half A · Roadmap\n")
        if pg.tracks:
            sections.append("\n".join(_table_rows(pg.tracks)))
        else:
            sections.append("_No Half A track bound._")
        sections.append("\n#### Half B · Implementation\n")
        if pg.seats:
            sections.append("\n".join(_table_rows(pg.seats)))
        else:
            sections.append("_No Half B seats bound._")

    return "\n".join(sections)
