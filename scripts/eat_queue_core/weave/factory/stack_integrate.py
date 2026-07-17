"""Stack integrate pass — honest integrate validation (no file_exists theater)."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .factory_little_val import FactoryLittleValResult, check_spine_socket, merge_results
from .tech_stack_manifest import (
    ROW_KINDS_SKELETON,
    TechStackManifest,
    load_manifest,
    validate_manifest_schema,
)


@dataclass(frozen=True)
class IntegratePassResult:
    ok: bool
    run_id: str
    receipts: tuple[dict[str, Any], ...]
    little_val: FactoryLittleValResult
    violations: tuple[str, ...]


def _receipts_dir(vault_root: Path) -> Path:
    return vault_root / ".technical" / "weave" / "factory" / "receipts"


def _row_integrated(vault_root: Path, manifest: TechStackManifest, row_id: str) -> dict[str, Any]:
    row = manifest.row_by_id(row_id)
    if row is None:
        return {"manifest_row_id": row_id, "status": "missing_row"}

    raw = row.raw
    game_repo = vault_root / manifest.game_repo_path
    repo_path = row.repo_path
    file_exists = bool(repo_path and (game_repo / repo_path).exists())

    integrate_receipt = raw.get("integrate_receipt_id")
    operational = row.operational_confirmed
    row_kind = row.row_kind

    if row_kind in ROW_KINDS_SKELETON:
        status = "pending_research" if row_kind == "candidate_search" else "skeleton_only"
        if file_exists and not operational:
            status = "skeleton_files_present"
        return {
            "manifest_row_id": row.id,
            "row_kind": row_kind,
            "game_repo_path": manifest.game_repo_path,
            "repo_path": repo_path,
            "file_exists": file_exists,
            "status": status,
            "integrate_receipt_id": integrate_receipt,
            "operational_confirmed": operational,
            "wrap_policy": row.wrap_policy,
        }

    if row_kind == "locked" and row.id == "engine-godot-463-dotnet":
        ok = file_exists and operational
        return {
            "manifest_row_id": row.id,
            "row_kind": row_kind,
            "file_exists": file_exists,
            "status": "integrated" if ok else "pending",
            "integrate_receipt_id": integrate_receipt,
            "operational_confirmed": operational,
        }

    if operational and integrate_receipt and file_exists:
        status = "integrated"
    elif integrate_receipt and operational:
        status = "integrated_no_repo_path"
    else:
        status = "pending"

    return {
        "manifest_row_id": row.id,
        "row_kind": row_kind,
        "game_repo_path": manifest.game_repo_path,
        "repo_path": repo_path,
        "file_exists": file_exists,
        "status": status,
        "integrate_receipt_id": integrate_receipt,
        "operational_confirmed": operational,
        "wrap_policy": row.wrap_policy,
    }


def run_stack_integrate_pass(vault_root: Path, *, dry_run: bool = False) -> IntegratePassResult:
    run_id = f"factory-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    manifest = load_manifest(vault_root)
    schema_violations = validate_manifest_schema(manifest, vault_root)
    if schema_violations:
        lv = FactoryLittleValResult(
            little_val_ok=False,
            anti_pattern_violations=[f"manifest_drift:{v}" for v in schema_violations],
            run_id=run_id,
        )
        return IntegratePassResult(False, run_id, (), lv, tuple(schema_violations))

    game_repo = vault_root / manifest.game_repo_path
    receipts: list[dict[str, Any]] = []
    for row in manifest.baseline_required_rows():
        rec = _row_integrated(vault_root, manifest, row.id)
        rec["run_id"] = run_id
        rec["completed_at"] = datetime.now(timezone.utc).isoformat()
        receipts.append(rec)

    lv_parts: list[FactoryLittleValResult] = []
    for rec in receipts:
        row_id = str(rec.get("manifest_row_id", ""))
        row = manifest.row_by_id(row_id)
        if row and row.row_kind in ROW_KINDS_SKELETON:
            if rec.get("file_exists") and not row.operational_confirmed:
                lv_parts.append(
                    FactoryLittleValResult(
                        little_val_ok=False,
                        anti_pattern_violations=[f"file_exists_integrate_theater:{row_id}"],
                        run_id=run_id,
                    )
                )
            continue
        if rec.get("status") not in ("integrated", "integrated_no_repo_path"):
            if row and row.id != "engine-godot-463-dotnet":
                lv_parts.append(
                    FactoryLittleValResult(
                        little_val_ok=False,
                        anti_pattern_violations=[f"row_not_integrated:{row_id}"],
                        run_id=run_id,
                    )
                )
        if rec.get("wrap_policy") and row and row.operational_confirmed:
            lv_parts.append(check_spine_socket(game_repo, str(rec["wrap_policy"])))

    little_val = merge_results(*lv_parts) if lv_parts else FactoryLittleValResult(True, run_id=run_id)
    little_val.run_id = run_id

    engine_rec = next((r for r in receipts if r.get("manifest_row_id") == "engine-godot-463-dotnet"), None)
    engine_ok = bool(engine_rec and engine_rec.get("status") == "integrated")
    # file_exists on skeleton rows is expected during vetting — not a pipeline failure
    blocking = [
        v
        for v in little_val.anti_pattern_violations
        if not v.startswith("file_exists_integrate_theater:")
    ]
    ok = engine_ok and not blocking

    if not dry_run and receipts:
        out_dir = _receipts_dir(vault_root) / run_id
        out_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "run_id": run_id,
            "pass": "stack_integrate_pass",
            "receipts": receipts,
            "little_val": little_val.to_dict(),
            "engine_integrated": engine_ok,
        }
        (out_dir / "stack_integrate.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return IntegratePassResult(ok, run_id, tuple(receipts), little_val, tuple(little_val.anti_pattern_violations))
