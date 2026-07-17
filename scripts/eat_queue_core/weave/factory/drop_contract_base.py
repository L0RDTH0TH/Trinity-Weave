"""Drop contracts — ADC/TAC/CDC/PDC/AuDC shared schema, validation, receipts."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

DROP_CONTRACTS: dict[str, str] = {
    "adc": "assets/_factory/manifest.yaml",
    "tac": "assets/_techart/_factory/manifest.yaml",
    "cdc": "content/_factory/manifest.yaml",
    "pdc": "UI/_factory/manifest.yaml",
    "audc": "audio/_factory/manifest.yaml",
}

LANE_DROP_TYPE: dict[str, str] = {
    "asset": "adc",
    "techart": "tac",
    "content": "cdc",
    "presentation": "pdc",
    "audio": "audc",
}

REQUIRED_DROP_FIELDS = (
    "schema_version",
    "contract_type",
    "drops",
    "generated_by_receipt_id",
)


@dataclass
class DropEntry:
    drop_id: str
    path: str
    slice_id: str
    lane_id: str
    receipt_id: str
    license_spdx: str = "CC0-1.0"
    source_url: str = ""
    supersedes: str | None = None
    retired_at: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "drop_id": self.drop_id,
            "path": self.path,
            "slice_id": self.slice_id,
            "lane_id": self.lane_id,
            "receipt_id": self.receipt_id,
            "license_spdx": self.license_spdx,
        }
        if self.source_url:
            out["source_url"] = self.source_url
        if self.supersedes:
            out["supersedes"] = self.supersedes
        if self.retired_at:
            out["retired_at"] = self.retired_at
        out.update(self.extra)
        return out


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def manifest_path(game_repo: Path, contract_type: str) -> Path:
    rel = DROP_CONTRACTS.get(contract_type.lower())
    if not rel:
        raise ValueError(f"unknown_contract_type:{contract_type}")
    return game_repo / rel


def load_drop_manifest(game_repo: Path, contract_type: str) -> dict[str, Any]:
    path = manifest_path(game_repo, contract_type)
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def validate_drop_manifest(data: dict[str, Any], *, contract_type: str) -> list[str]:
    violations: list[str] = []
    for key in REQUIRED_DROP_FIELDS:
        if key not in data:
            violations.append(f"missing_field:{key}")
    if str(data.get("contract_type") or "").lower() != contract_type.lower():
        violations.append("contract_type_mismatch")
    drops = data.get("drops")
    if not isinstance(drops, list):
        violations.append("drops_not_list")
    elif drops:
        for i, row in enumerate(drops):
            if not isinstance(row, dict):
                violations.append(f"drop_{i}_not_object")
                continue
            for req in ("drop_id", "path", "slice_id", "lane_id", "receipt_id"):
                if not row.get(req):
                    violations.append(f"drop_{i}_missing_{req}")
    return violations


def ensure_drop_manifest_skeleton(game_repo: Path, contract_type: str) -> Path:
    path = manifest_path(game_repo, contract_type)
    if path.is_file():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "contract_type": contract_type.upper(),
        "drops": [],
        "generated_by_receipt_id": "bootstrap",
        "license_spdx": "CC0-1.0",
        "ai_generated_content_policy": "operator_review_required",
    }
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def bootstrap_all_drop_manifests(game_repo: Path) -> list[str]:
    created: list[str] = []
    for ctype in DROP_CONTRACTS:
        path = manifest_path(game_repo, ctype)
        if not path.is_file():
            ensure_drop_manifest_skeleton(game_repo, ctype)
            created.append(str(path))
    canon = game_repo / "content/_factory/canon-index.yaml"
    if not canon.is_file():
        canon.parent.mkdir(parents=True, exist_ok=True)
        canon.write_text(
            yaml.safe_dump(
                {"schema_version": 1, "entries": [], "generated_by_receipt_id": "bootstrap"},
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        created.append(str(canon))
    spine = game_repo / "REPO_SPINE.md"
    if not spine.is_file():
        spine.write_text(
            "# REPO_SPINE\n\nFactory zone map — see FACTORY_ZONES in vault Factory-DRB.\n",
            encoding="utf-8",
        )
        created.append(str(spine))
    return created


def list_drop_ids(game_repo: Path, contract_types: tuple[str, ...] | None = None) -> set[str]:
    types = contract_types or tuple(DROP_CONTRACTS.keys())
    out: set[str] = set()
    for ctype in types:
        data = load_drop_manifest(game_repo, ctype)
        for row in data.get("drops") or []:
            if isinstance(row, dict) and row.get("drop_id"):
                if not row.get("retired_at"):
                    out.add(str(row["drop_id"]))
    return out


def register_lane_drop(
    game_repo: Path,
    *,
    lane_id: str,
    slice_id: str,
    receipt_id: str,
    paths: list[str],
    license_spdx: str = "CC0-1.0",
) -> dict[str, Any]:
    ctype = LANE_DROP_TYPE.get(lane_id)
    if not ctype:
        return {"ok": False, "error": f"no_drop_contract_for_lane:{lane_id}"}
    ensure_drop_manifest_skeleton(game_repo, ctype)
    path = manifest_path(game_repo, ctype)
    data = load_drop_manifest(game_repo, ctype)
    existing_ids = {str(r.get("drop_id")) for r in (data.get("drops") or []) if isinstance(r, dict)}
    new_rows: list[dict[str, Any]] = []
    for rel in paths:
        drop_id = f"{ctype}-{slice_id}-{lane_id}-{uuid.uuid4().hex[:8]}"
        while drop_id in existing_ids:
            drop_id = f"{ctype}-{slice_id}-{lane_id}-{uuid.uuid4().hex[:8]}"
        row = DropEntry(
            drop_id=drop_id,
            path=rel,
            slice_id=slice_id,
            lane_id=lane_id,
            receipt_id=receipt_id,
            license_spdx=license_spdx,
        ).to_dict()
        new_rows.append(row)
        existing_ids.add(drop_id)
    drops = list(data.get("drops") or [])
    drops.extend(new_rows)
    data["drops"] = drops
    data["generated_by_receipt_id"] = receipt_id
    data["updated_at"] = _utc_iso()
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return {"ok": True, "contract_type": ctype, "registered": new_rows, "manifest": str(path)}


def check_depends_on_drops(
    game_repo: Path,
    depends_on: list[str],
    *,
    pinned_receipt_ids: list[str] | None = None,
) -> tuple[bool, list[str]]:
    """Return (ok, violations). depends_on: drop_id, contract_type, or contract_type:drop_id."""
    violations: list[str] = []
    all_ids = list_drop_ids(game_repo)
    for dep in depends_on:
        dep_s = str(dep).strip().lower()
        if ":" in dep_s:
            ctype, drop_part = dep_s.split(":", 1)
            if drop_part not in all_ids:
                violations.append(f"missing_drop:{dep_s}")
            continue
        if dep_s in DROP_CONTRACTS:
            data = load_drop_manifest(game_repo, dep_s)
            active = [
                r
                for r in (data.get("drops") or [])
                if isinstance(r, dict) and not r.get("retired_at")
            ]
            if not active:
                violations.append(f"missing_drop_contract:{dep_s}")
            continue
        if dep_s not in all_ids:
            violations.append(f"missing_drop:{dep_s}")
    if pinned_receipt_ids:
        for ctype in DROP_CONTRACTS:
            data = load_drop_manifest(game_repo, ctype)
            receipts = {
                str(r.get("receipt_id"))
                for r in (data.get("drops") or [])
                if isinstance(r, dict) and r.get("receipt_id")
            }
            for pin in pinned_receipt_ids:
                if pin and pin not in receipts and pin != "bootstrap":
                    violations.append(f"pinned_receipt_not_found:{pin}")
    return len(violations) == 0, violations
