"""Phase 16 — redesign_factory A/B replacement harness (no auto-deprecate)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..lane_board_drilldown import append_maintenance_decision
from .config import load_trinity_config
from .trinity_honesty_anchor import classify_claim, evaluate_claim
from .trinity_knob_parity import FACTORY_REGISTRY, build_matrix_cells

ARTIFACT_DIR = Path(".technical/weave/validation")
ARCHIVE_ROOT = Path("4-Archives/Weave/Factory-Lifecycle")

# Provisional candidate ids map to legacy check until v2 factories land in registry.
CANDIDATE_ALIASES: dict[str, str] = {
    "queue_dispatch_v2": "queue_dispatch",
    "roadmap_resume_v2": "roadmap_resume",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def resolve_factory_id(factory_id: str) -> tuple[str | None, str | None]:
    """Return (registry_key, alias_of) — registry_key None when unknown."""
    if factory_id in FACTORY_REGISTRY:
        return factory_id, None
    alias = CANDIDATE_ALIASES.get(factory_id)
    if alias and alias in FACTORY_REGISTRY:
        return alias, alias
    return None, None


def rust_grade_factory(factory_id: str, cells: list[dict[str, Any]]) -> dict[str, Any]:
    """Heuristic rust grade from knob-parity red cells for a factory."""
    factory_cells = [c for c in cells if c.get("factory") == factory_id]
    if not factory_cells:
        return {
            "factory_id": factory_id,
            "known": False,
            "rust_grade": "unknown",
            "red_cell_count": 0,
            "total_cells": 0,
            "red_ratio": 0.0,
            "surgical_sufficient": False,
            "recommend_ab": False,
        }
    red = [c for c in factory_cells if not c.get("ok")]
    total = len(factory_cells)
    ratio = len(red) / total
    if ratio == 0:
        grade = "low"
    elif ratio < 0.2:
        grade = "medium"
    else:
        grade = "high"
    surgical = ratio == 0
    return {
        "factory_id": factory_id,
        "known": True,
        "rust_grade": grade,
        "red_cell_count": len(red),
        "total_cells": total,
        "red_ratio": round(ratio, 4),
        "surgical_sufficient": surgical,
        "recommend_ab": not surgical,
        "red_cells": red[:5],
    }


def _factory_cell_summary(factory_id: str, cells: list[dict[str, Any]]) -> dict[str, Any]:
    fc = [c for c in cells if c.get("factory") == factory_id]
    green = sum(1 for c in fc if c.get("ok"))
    red = len(fc) - green
    return {
        "factory_id": factory_id,
        "total": len(fc),
        "green": green,
        "red": red,
    }


def compare_ab_structural(
    legacy_id: str,
    candidate_id: str,
    cells: list[dict[str, Any]],
) -> dict[str, Any]:
    """Structural compare only — no narrative winner."""
    leg_key, _ = resolve_factory_id(legacy_id)
    cand_key, cand_alias = resolve_factory_id(candidate_id)

    if leg_key is None:
        return {
            "ok": False,
            "error": f"legacy factory unknown: {legacy_id!r}",
        }

    legacy_summary = _factory_cell_summary(leg_key, cells)
    legacy_rust = rust_grade_factory(leg_key, cells)

    candidate_in_registry = candidate_id in FACTORY_REGISTRY
    candidate_is_alias = candidate_id in CANDIDATE_ALIASES

    if candidate_in_registry:
        cand_summary = _factory_cell_summary(candidate_id, cells)
    elif cand_alias:
        cand_summary = _factory_cell_summary(cand_key or legacy_id, cells)
        cand_summary["factory_id"] = candidate_id
        cand_summary["alias_of"] = cand_alias
    else:
        return {
            "ok": False,
            "error": f"candidate factory unknown: {candidate_id!r}",
            "legacy": legacy_summary,
            "legacy_rust": legacy_rust,
        }

    leg_green = legacy_summary["green"]
    cand_green = cand_summary["green"]
    if cand_green > leg_green:
        winner = "candidate"
    elif leg_green > cand_green:
        winner = "legacy"
    else:
        winner = "tie"

    return {
        "ok": True,
        "legacy_id": legacy_id,
        "candidate_id": candidate_id,
        "legacy": legacy_summary,
        "candidate": cand_summary,
        "legacy_rust": legacy_rust,
        "candidate_in_registry": candidate_in_registry,
        "candidate_is_alias": candidate_is_alias,
        "winner_structural": winner,
        "claim_tier": "structural",
        "skip_ab_recommended": legacy_rust.get("surgical_sufficient") and candidate_is_alias,
    }


def _append_ab_telemetry(
    vault_root: Path,
    *,
    legacy_id: str,
    candidate_id: str,
    comparison: dict[str, Any],
    ab_mode: str,
) -> None:
    detail = (
        f"legacy={legacy_id} candidate={candidate_id} mode={ab_mode} "
        f"winner={comparison.get('winner_structural')} "
        f"legacy_green={comparison.get('legacy', {}).get('green')} "
        f"candidate_green={comparison.get('candidate', {}).get('green')}"
    )
    append_maintenance_decision(
        vault_root,
        event="redesign_factory_ab",
        lane="maintenance",
        detail=detail[:500],
    )


def _deprecate_archive_stub(
    vault_root: Path,
    *,
    legacy_id: str,
    candidate_id: str,
    dry_run: bool,
) -> dict[str, Any]:
    """Operator-ack only — writes manifest stub; never deletes cards."""
    stamp = _stamp()
    archive_dir = vault_root / ARCHIVE_ROOT / stamp
    manifest = {
        "archived_at": _now_iso(),
        "legacy_factory_id": legacy_id,
        "candidate_factory_id": candidate_id,
        "action": "operator_deprecate_ack_stub",
        "note": "Archive path placeholder — operator moves cards/tests manually",
    }
    if dry_run:
        return {"ok": True, "dry_run": True, "would_write": str(archive_dir / "manifest.json")}
    archive_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = archive_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    append_maintenance_decision(
        vault_root,
        event="redesign_factory_deprecate_ack",
        lane="maintenance",
        detail=f"legacy={legacy_id} archived_stub={manifest_path}",
    )
    return {"ok": True, "archive_manifest": str(manifest_path)}


def run_redesign_factory(
    vault_root: Path,
    *,
    legacy_factory_id: str,
    candidate_factory_id: str,
    ab_mode: str = "parallel",
    speed_mode_matrix: tuple[str, ...] | None = None,
    operator_deprecate_ack: bool = False,
    dry_run: bool = False,
    write_artifact: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    load_trinity_config(vault_root)  # ensure vault config readable

    cells = build_matrix_cells()
    comparison = compare_ab_structural(legacy_factory_id, candidate_factory_id, cells)
    if not comparison.get("ok"):
        return {"ok": False, **comparison}

    # Honesty envelope on the comparison outcome (structural telemetry only).
    honesty_payload = {
        "structural_proof": True,
        "counts": comparison.get("legacy"),
        "report_path": str(ARTIFACT_DIR / f"redesign-factory-ab-{_stamp()}.json"),
        "pass_gate_ok": comparison.get("winner_structural") in ("candidate", "tie"),
    }
    h_ok, h_errors, h_tier = evaluate_claim(honesty_payload)

    report: dict[str, Any] = {
        "ok": h_ok,
        "dry_run": dry_run,
        "generated_at": _now_iso(),
        "legacy_factory_id": legacy_factory_id,
        "candidate_factory_id": candidate_factory_id,
        "ab_mode": ab_mode,
        "speed_mode_matrix": list(speed_mode_matrix or ()),
        "comparison": comparison,
        "honesty": {
            "claim_tier": h_tier,
            "classify": classify_claim(honesty_payload),
            "ok": h_ok,
            "errors": h_errors,
        },
        "auto_deprecate": False,
    }

    if comparison.get("skip_ab_recommended"):
        report["advisory"] = "legacy surgical_sufficient; A/B optional for alias candidate"

    artifact_name = f"redesign-factory-ab-{_stamp()}.json"
    artifact_rel = ARTIFACT_DIR / artifact_name
    report["artifact_path"] = str(artifact_rel)

    if not dry_run:
        _append_ab_telemetry(
            vault_root,
            legacy_id=legacy_factory_id,
            candidate_id=candidate_factory_id,
            comparison=comparison,
            ab_mode=ab_mode,
        )

    if operator_deprecate_ack:
        report["deprecate"] = _deprecate_archive_stub(
            vault_root,
            legacy_id=legacy_factory_id,
            candidate_id=candidate_factory_id,
            dry_run=dry_run,
        )
    else:
        report["deprecate_skipped"] = "operator_deprecate_ack required for archive stub"

    if not dry_run and write_artifact:
        out_path = vault_root / artifact_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["written"] = True

    if not h_ok:
        report["ok"] = False

    return report
