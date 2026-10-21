"""Goal-packet scan and expandable overnight expedition sections."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .goal_authority_io import (
    architect_orchestration_active,
    default_ttl_hours,
    goal_authority_path_for_lane,
    load_goal_authority,
    load_orchestration_state,
    packet_is_stale,
)
from .handoff_build import bundle_dir_for_lane
from .ingest_autopilot_config import INGEST_BATCH_GA_REL
from .lane_activity import resolve_lane_activity
from .lane_registry import SKIP_BUNDLE_LANES

MONITORED_EXPEDITION_LANES_DEFAULT = ("godot", "institute")
STATUS_PRIORITY = {"running": 0, "armed": 1, "blocked": 2, "draft_only": 3, "stale": 4, "vacant": 5, "dormant": 6}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_jsonl_tail(path: Path, n: int = 5) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows[-n:]


def _factory_profile(packet: dict[str, Any]) -> str:
    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    warehouse = str(hints.get("warehouse") or "").strip().lower()
    subfactory = str(hints.get("subfactory") or "").strip().lower()
    if warehouse and subfactory:
        return f"{warehouse}/{subfactory}"
    fp = str(hints.get("factory_profile") or "").strip().lower()
    if fp:
        return fp
    if hints.get("effective_track") == "implementation" or hints.get("feed_authority") == "vault_roadmap":
        return "implementation"
    if hints.get("product_factory") or hints.get("primary_mode") == "ROADMAP_MODE":
        return "half_a"
    early = packet.get("early_stop_policy") if isinstance(packet.get("early_stop_policy"), dict) else {}
    if early.get("implementation_gate"):
        return "half_a"
    return "half_a"


def _soft_deadline_display(packet: dict[str, Any]) -> str:
    local = str(packet.get("operator_soft_deadline_local") or "")
    tz = str(packet.get("operator_soft_deadline_tz") or "")
    if local and tz:
        return f"{local} {tz}"
    return local or "—"


def _latest_wind_down_link(vault_root: Path, lane: str) -> str | None:
    out_dir = vault_root / "Ingest" / "Agent-Output"
    if not out_dir.is_dir():
        return None
    matches = sorted(out_dir.glob(f"overnight-*-{lane}-*.md"), reverse=True)
    if not matches:
        return None
    rel = matches[0].relative_to(vault_root).as_posix()
    return rel


@dataclass
class ExpeditionRow:
    lane: str
    kind: str
    status: str
    primary: bool = False
    path: str = ""
    packet: dict[str, Any] = field(default_factory=dict)
    factory_profile: str = ""
    last_session: dict[str, Any] = field(default_factory=dict)
    wind_down_rel: str | None = None
    lifecycle: str = "active"

    def to_dict(self) -> dict[str, Any]:
        return {
            "lane": self.lane,
            "kind": self.kind,
            "status": self.status,
            "primary": self.primary,
            "path": self.path,
            "packet": self.packet,
            "factory_profile": self.factory_profile,
            "last_session": self.last_session,
            "wind_down_rel": self.wind_down_rel,
            "lifecycle": self.lifecycle,
        }


def _classify_overnight_packet(
    vault_root: Path,
    lane: str,
    packet: dict[str, Any] | None,
    *,
    draft: dict[str, Any] | None,
    ttl: float,
) -> str:
    activity = resolve_lane_activity(vault_root, lane)
    if str(activity.get("run_status")) == "running" or architect_orchestration_active(vault_root, lane):
        return "running"
    if packet and not packet_is_stale(packet, ttl):
        exit_reason = _read_jsonl_tail(bundle_dir_for_lane(vault_root, lane) / "overnight-session-receipts.jsonl", 1)
        if exit_reason:
            er = str(exit_reason[-1].get("exit_reason") or "")
            if "operator_loop" in er or "gate" in er:
                return "blocked"
        return "armed"
    if packet and packet_is_stale(packet, ttl):
        return "stale"
    if draft:
        return "draft_only"
    return "vacant"


def _monitored_lanes(vault_root: Path, registry: Any | None) -> tuple[str, ...]:
    if registry is not None:
        lanes: list[str] = []
        for ln, row in registry.rows.items():
            if ln in SKIP_BUNDLE_LANES:
                continue
            if row.lane_class in ("execution_track", "orchestration") and row.bundle_exists:
                lanes.append(ln)
        return tuple(sorted(set(lanes)))
    return MONITORED_EXPEDITION_LANES_DEFAULT


def scan_expeditions(vault_root: Path, *, registry: Any | None = None) -> list[ExpeditionRow]:
    vault_root = vault_root.resolve()
    ttl = default_ttl_hours(vault_root)
    rows: list[ExpeditionRow] = []

    for lane in _monitored_lanes(vault_root, registry):
        reg_row = registry.rows.get(lane) if registry else None
        lifecycle = reg_row.lifecycle if reg_row else "active"
        ga_path = goal_authority_path_for_lane(vault_root, lane)
        rel = ga_path.relative_to(vault_root).as_posix() if ga_path.is_file() else str(ga_path)
        packet = load_goal_authority(vault_root, lane, require_confirmed=True)
        draft_path = ga_path.parent / "goal-authority.draft.json"
        draft: dict[str, Any] | None = None
        if draft_path.is_file():
            try:
                draft = json.loads(draft_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                draft = None
        if lifecycle in ("orphan_bundle", "archived"):
            status = "dormant"
        else:
            status = _classify_overnight_packet(vault_root, lane, packet, draft=draft, ttl=ttl)
        sess_path = bundle_dir_for_lane(vault_root, lane) / "overnight-session-receipts.jsonl"
        last_sess = _read_jsonl_tail(sess_path, 1)
        last_session = last_sess[-1] if last_sess else {}
        pkt_copy = dict(packet) if packet else (dict(draft) if draft else {})
        rows.append(
            ExpeditionRow(
                lane=lane,
                kind="overnight",
                status=status,
                path=rel if packet or draft_path.is_file() else "",
                packet=pkt_copy,
                factory_profile=_factory_profile(pkt_copy) if pkt_copy else "",
                last_session=last_session,
                wind_down_rel=_latest_wind_down_link(vault_root, lane),
                lifecycle=lifecycle,
            )
        )

    batch_path = vault_root / INGEST_BATCH_GA_REL
    if batch_path.is_file():
        try:
            batch = json.loads(batch_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            batch = None
        if isinstance(batch, dict):
            rows.append(
                ExpeditionRow(
                    lane="institute",
                    kind="ingest_batch",
                    status="armed" if batch.get("confirmed_by_operator") else "draft_only",
                    path=INGEST_BATCH_GA_REL.as_posix(),
                    packet=batch,
                    factory_profile="km",
                )
            )

    active_indices = [
        i
        for i, r in enumerate(rows)
        if r.lifecycle not in ("orphan_bundle", "archived") and r.status != "dormant"
    ]
    if active_indices:
        primary_idx = min(active_indices, key=lambda i: STATUS_PRIORITY.get(rows[i].status, 99))
        rows[primary_idx].primary = True
    return rows


def resolve_active_project_id(vault_root: Path, expeditions: list[ExpeditionRow]) -> str:
    for ex in expeditions:
        if ex.kind == "overnight" and ex.packet:
            pid = str(ex.packet.get("project_id") or "").strip()
            if pid:
                return pid
    return ""


def render_expeditions_section(expeditions: list[ExpeditionRow], *, compact: bool = True) -> str:
    visible = [
        ex
        for ex in expeditions
        if ex.lifecycle not in ("orphan_bundle", "archived") and ex.status != "dormant"
    ]
    if not visible:
        return "_No monitored expeditions._"

    summary_lines = [
        "| Lane | Kind | Status | Lifecycle | Packet id | Profile | Deadline |",
        "|------|------|--------|-----------|-----------|---------|----------|",
    ]

    wind_down = ""
    for ex in visible:
        pkt = ex.packet
        run_id = str(pkt.get("run_id") or "—")[:40]
        deadline = _soft_deadline_display(pkt) if pkt else "—"
        summary_lines.append(
            f"| {ex.lane} | {ex.kind} | **{ex.status}** | {ex.lifecycle} | `{run_id}` | {ex.factory_profile or '—'} | {deadline} |"
        )
        if ex.wind_down_rel and ex.primary:
            wind_down = f"\n\nPrimary wind-down: [[{ex.wind_down_rel}]]"

    body = "\n".join(summary_lines) + wind_down
    if compact:
        return body
    return body
