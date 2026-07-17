"""Drain factory_run_escalation.jsonl via Architect-layer council helper."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ...council_chamber import run_council_session
from ...goal_authority_io import load_goal_authority
from ...headless_architect import load_architect_config, situation_scan
from .factory_correlation import factory_escalation_path


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_escalation_rows(path: Path) -> list[dict[str, Any]]:
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
    return rows


def _write_escalation_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
    path.write_text(text + ("\n" if text else ""), encoding="utf-8")


def drain_receipt_path(vault_root: Path) -> Path:
    return vault_root / ".technical" / "factory" / "factory_escalation_drain_receipts.jsonl"


def run_factory_escalation_council(
    vault_root: Path,
    lane: str,
    row: dict[str, Any],
    *,
    packet: dict[str, Any] | None = None,
    run_id: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Map one escalation row to run_council_session (Architect layer — not persona Task)."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    packet = packet or load_goal_authority(vault_root, lane, require_confirmed=False) or {}
    _, fc_cfg = load_architect_config(vault_root)
    situation = situation_scan(vault_root, lane, packet)
    situation = {
        **situation,
        "factory_escalation": {
            "failure_class": row.get("failure_class"),
            "slice_id": row.get("slice_id"),
            "project_id": row.get("project_id"),
            "message": row.get("message"),
        },
    }
    ctx_override = str(row.get("council_context") or row.get("failure_class") or "cross_domain")
    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "council_context": ctx_override,
            "escalation_row": row,
        }
    council = run_council_session(
        vault_root,
        lane,
        packet,
        situation,
        fc_cfg,
        council_forced=True,
        dry_run=False,
        council_context_override=ctx_override,
    )
    decision = str(council.get("architect_decision") or "operator_pause")
    return {
        "ok": decision in ("proceed", "convene_cross_domain"),
        "architect_decision": decision,
        "council": council,
        "escalation_row": row,
        "drain_run_id": run_id,
    }


def drain_factory_escalations(
    vault_root: Path,
    lane: str,
    *,
    run_id: str | None = None,
    dry_run: bool = False,
    max_rows: int = 5,
) -> dict[str, Any]:
    """Consume pending request_council rows from factory_run_escalation.jsonl."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    path = factory_escalation_path(vault_root)
    rows = _read_escalation_rows(path)
    packet = load_goal_authority(vault_root, lane, require_confirmed=False)
    drained: list[dict[str, Any]] = []
    pending = 0

    for i, row in enumerate(rows):
        if row.get("consumed_at"):
            continue
        if not row.get("request_council"):
            continue
        pending += 1
        if len(drained) >= max(1, int(max_rows)):
            break
        out = run_factory_escalation_council(
            vault_root,
            lane,
            row,
            packet=packet if isinstance(packet, dict) else None,
            run_id=run_id,
            dry_run=dry_run,
        )
        if not dry_run:
            row["consumed_at"] = _utc_iso()
            row["drain_run_id"] = run_id or ""
            row["drain_architect_decision"] = out.get("architect_decision")
            rows[i] = row
            receipt = {
                "ts": _utc_iso(),
                "lane": lane,
                "drain_run_id": run_id,
                "failure_class": row.get("failure_class"),
                "slice_id": row.get("slice_id"),
                **{k: out.get(k) for k in ("ok", "architect_decision") if k in out},
            }
            rpath = drain_receipt_path(vault_root)
            rpath.parent.mkdir(parents=True, exist_ok=True)
            with rpath.open("a", encoding="utf-8") as f:
                f.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        drained.append(out)

    if not dry_run and drained:
        _write_escalation_rows(path, rows)

    return {
        "ok": True,
        "lane": lane,
        "pending_request_council": pending,
        "drained": len(drained),
        "results": drained,
        "dry_run": dry_run,
    }
