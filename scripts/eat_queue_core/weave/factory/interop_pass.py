"""Cross-domain interoperability pass."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .factory_little_val import FactoryLittleValResult
from .stack_domain_registry import load_stack_domain_registry
from .tech_stack_manifest import ROW_KINDS_SKELETON, load_manifest


@dataclass(frozen=True)
class InteropPassResult:
    ok: bool
    little_val: FactoryLittleValResult
    detail: str
    pending_domains: tuple[str, ...]


def _interop_receipts_dir(vault_root: Path) -> Path:
    return vault_root / ".technical" / "weave" / "factory" / "interop_receipts"


def _interop_receipt_exists(vault_root: Path, interop_id: str) -> bool:
    """Resolve interop receipt — JSON harness file or vault markdown receipt."""
    if not interop_id:
        return False
    if "/" in interop_id or interop_id.endswith(".md"):
        return (vault_root / interop_id).is_file()
    json_path = _interop_receipts_dir(vault_root) / f"{interop_id}.json"
    return json_path.is_file()


def run_interop_pass(vault_root: Path) -> InteropPassResult:
    manifest = load_manifest(vault_root)
    registry = load_stack_domain_registry(vault_root)
    violations: list[str] = []
    pending: list[str] = []
    checked_interop: set[str] = set()

    for row in manifest.baseline_required_rows():
        if row.id == "engine-godot-463-dotnet":
            continue
        if row.row_kind in ROW_KINDS_SKELETON or not row.operational_confirmed:
            pending.append(row.stack_domain_id or row.id)
            continue
        interop_id = row.raw.get("interop_receipt_id")
        if row.interop_required and not interop_id:
            violations.append(f"missing_interop_receipt:{row.id}")
        if interop_id and interop_id not in checked_interop:
            checked_interop.add(interop_id)
            if not _interop_receipt_exists(vault_root, str(interop_id)):
                violations.append(f"interop_receipt_file_missing:{interop_id}")

    if registry.interop_gate_required:
        for domain in registry.domains:
            if not domain.baseline_required:
                continue
            row = manifest.row_by_stack_domain(domain.id)
            if row is None:
                violations.append(f"manifest_missing_domain:{domain.id}")
                continue
            if row.operational_confirmed and row.interop_required and not row.raw.get("interop_receipt_id"):
                violations.append(f"missing_interop_receipt:{row.id}")

    # Expected state while vetting: pending domains, no violations except missing receipts on claimed operational rows
    ok = len(violations) == 0
    detail = f"pending_domains={len(pending)} violations={len(violations)}"
    lv = FactoryLittleValResult(
        little_val_ok=ok,
        anti_pattern_violations=violations,
        detail="interop_pass",
    )
    return InteropPassResult(ok, lv, detail, tuple(pending))


def write_interop_receipt(
    vault_root: Path,
    *,
    receipt_id: str,
    domains: list[str],
    smoke_description: str,
    ok: bool,
) -> Path:
    out_dir = _interop_receipts_dir(vault_root)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{receipt_id}.json"
    payload: dict[str, Any] = {
        "receipt_id": receipt_id,
        "domains": domains,
        "smoke_description": smoke_description,
        "ok": ok,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
