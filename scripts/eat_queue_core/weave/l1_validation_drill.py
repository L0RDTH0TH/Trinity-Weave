"""Phase A — L1 integrity fault drill (controlled board break → O1 maintenance PQ)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..lane_board_integrity import validate_lane_board_integrity
from ..lane_status_board import BOARD_REL, write_lane_status_board
from ..maintenance_io import append_maintenance_entry, maintenance_pq_path, pq_has_fingerprint
from .governance import append_metric_row, ensure_weave_paths
from .verifier import REQUIRED_SECTIONS, verify_operator_surface_integrity


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass
class BoardSnapshot:
    content: bytes


def _snapshot_board(board_path: Path) -> BoardSnapshot:
    if board_path.is_file():
        return BoardSnapshot(board_path.read_bytes())
    return BoardSnapshot(b"")


def _restore_board(board_path: Path, snap: BoardSnapshot) -> None:
    board_path.parent.mkdir(parents=True, exist_ok=True)
    if snap.content:
        board_path.write_bytes(snap.content)
    elif board_path.is_file():
        board_path.unlink()


def _inject_integrity_fault(text: str, *, fault: str = "remove_section") -> str:
    if fault == "remove_token":
        return text.replace("operator_surface: lane_board", "operator_surface: lane_board_broken")
    section = "## Audit trail"
    if section in text:
        idx = text.index(section)
        return text[:idx].rstrip() + "\n"
    for sec in reversed(REQUIRED_SECTIONS):
        if sec in text:
            idx = text.index(sec)
            return text[:idx].rstrip() + "\n"
    return text.replace("## L3 self-healing", "## L3 self-healing-removed")


def probe_integrity_failure(
    vault_root: Path,
    board_path: Path,
    *,
    drill_fingerprint: str,
    source: str = "l1_validation_drill",
) -> dict[str, Any]:
    """
    Mirror write_lane_status_board integrity gate — fail closed, enqueue O1, no false-green.
    """
    vault_root = vault_root.resolve()
    v = verify_operator_surface_integrity(board_path)
    structural = validate_lane_board_integrity(vault_root, board_path)
    integrity_ok = bool(v.ok) and structural.ok
    integrity_reason = v.detail if v.ok else v.detail
    if not structural.ok:
        integrity_reason = f"{integrity_reason}; {structural.detail}".strip("; ")

    o1: dict[str, Any] = {"skipped": True}
    if not integrity_ok:
        o1 = append_maintenance_entry(
            vault_root,
            mode="OPERATOR_SURFACE_REPAIR",
            params={
                "meta_only": True,
                "recovery_handler": "operator_surface_repair",
                "retry_eligible": False,
                "detail": f"{v.code}: {integrity_reason}"[:400],
                "source_file": str(BOARD_REL),
                "fingerprint": drill_fingerprint,
            },
            source=source,
        )

    return {
        "integrity_ok": integrity_ok,
        "verifier": {"ok": v.ok, "code": v.code, "detail": v.detail},
        "structural": {
            "ok": structural.ok,
            "code": structural.code,
            "detail": structural.detail,
            "failures": list(structural.checks),
        },
        "operator_surface_repair": o1,
        "claim_success_allowed": integrity_ok,
    }


def drill_l1_integrity_fault(
    vault_root: Path,
    *,
    dry_run: bool = False,
    fault: str = "remove_section",
) -> dict[str, Any]:
    """Inject controlled board fault; confirm block + OPERATOR_SURFACE_REPAIR; restore + re-verify."""
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    board_path = vault_root / BOARD_REL
    drill_fp = f"l1-drill-integrity-{_utc_stamp()}"
    checks: list[dict[str, Any]] = []

    if dry_run:
        return {
            "drill_id": "l1_integrity_fault",
            "passed": True,
            "checks": [{"name": "dry_run", "ok": True}],
            "detail": {"would": "corrupt board, probe fail, O1 PQ, restore, refresh"},
            "timestamp": _utc_iso(),
        }

    if not board_path.is_file():
        checks.append({"name": "board_exists", "ok": False})
        return {
            "drill_id": "l1_integrity_fault",
            "passed": False,
            "checks": checks,
            "timestamp": _utc_iso(),
        }

    snap = _snapshot_board(board_path)

    try:
        original = board_path.read_text(encoding="utf-8")
        corrupted = _inject_integrity_fault(original, fault=fault)
        checks.append({"name": "fault_injected", "ok": corrupted != original})
        board_path.write_text(corrupted, encoding="utf-8")

        probe = probe_integrity_failure(vault_root, board_path, drill_fingerprint=drill_fp)
        checks.append({"name": "integrity_ok_false", "ok": probe.get("integrity_ok") is False})
        checks.append(
            {
                "name": "no_false_green",
                "ok": probe.get("claim_success_allowed") is False,
            }
        )
        checks.append(
            {
                "name": "verifier_or_structural_failed",
                "ok": not probe["verifier"]["ok"] or not probe["structural"]["ok"],
            }
        )

        o1 = probe.get("operator_surface_repair") or {}
        checks.append(
            {
                "name": "operator_surface_repair_queued",
                "ok": bool(o1.get("ok")) and not o1.get("skipped"),
                "o1": o1,
            }
        )
        checks.append(
            {
                "name": "maintenance_pq_fingerprint",
                "ok": pq_has_fingerprint(vault_root, drill_fp),
                "fingerprint": drill_fp,
            }
        )

        _restore_board(board_path, snap)
        checks.append({"name": "board_restored", "ok": board_path.read_bytes() == snap.content})

        refresh = write_lane_status_board(vault_root)
        checks.append(
            {
                "name": "post_restore_integrity_ok",
                "ok": bool(refresh.get("integrity_ok")),
                "integrity_reason": refresh.get("integrity_reason"),
            }
        )

        passed = all(c.get("ok") for c in checks)
        return {
            "drill_id": "l1_integrity_fault",
            "passed": passed,
            "checks": checks,
            "detail": {"probe": probe, "refresh": {"integrity_ok": refresh.get("integrity_ok")}, "fingerprint": drill_fp},
            "timestamp": _utc_iso(),
        }
    except Exception as exc:
        _restore_board(board_path, snap)
        raise exc


def run_l1_validation_drill(
    vault_root: Path,
    *,
    dry_run: bool = False,
    write_report: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    result = drill_l1_integrity_fault(vault_root, dry_run=dry_run)
    report = {
        "ok": bool(result.get("passed")),
        "phase": "A",
        "layer": "L1",
        "dry_run": dry_run,
        "drills": [result],
        "summary": {
            "total": 1,
            "passed": 1 if result.get("passed") else 0,
            "failed": 0 if result.get("passed") else 1,
        },
        "timestamp": _utc_iso(),
    }
    if write_report and not dry_run:
        out_dir = vault_root / ".technical" / "weave" / "validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"l1-drill-{_utc_stamp()}.json"
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(out_path)
        append_metric_row(
            vault_root,
            {
                "metric_type": "l1_validation_drill",
                "ok": report["ok"],
                "passed": report["summary"]["passed"],
                "failed": report["summary"]["failed"],
                "report_path": str(out_path),
            },
        )
    return report
