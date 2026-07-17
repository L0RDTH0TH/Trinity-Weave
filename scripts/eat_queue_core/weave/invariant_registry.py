"""K3 symbolic invariant registry — machine YAML under .technical/weave/invariants/."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .governance import append_metric_row, weave_dir

InvariantRisk = Literal["low", "medium", "high"]
InvariantStatus = Literal["active", "pending_counselor", "draft", "retired"]

N2_BOOTSTRAP_MODULES = (
    "lane_status_board",
    "lane_activity",
    "launch_registry_reconcile",
)

# N2 — initial invariant definitions (machine + bootstrap)
BOOTSTRAP_INVARIANTS: tuple[dict[str, Any], ...] = (
    {
        "id": "lane_run_no_receipt_inference",
        "module": "lane_status_board",
        "risk": "low",
        "check": "forbidden_context_flag",
        "flag": "infer_run_from_receipt",
        "message": "Run state must not be inferred from receipt tail",
    },
    {
        "id": "lane_run_authoritative_activity",
        "module": "lane_activity",
        "risk": "low",
        "check": "required_resolver",
        "resolver": "resolve_lane_activity",
        "message": "Run classification must use resolve_lane_activity after pre-read",
    },
    {
        "id": "registry_reconcile_pre_read",
        "module": "launch_registry_reconcile",
        "risk": "medium",
        "check": "required_pre_read",
        "step": "reconcile_launch_registry",
        "message": "Launch registry reconcile required before run/activity reads",
    },
    {
        "id": "cq_lanesnapshot_canonical",
        "module": "lane_snapshot",
        "risk": "low",
        "check": "required_kernel",
        "kernel": "build_lane_snapshots",
        "message": "Board health/run must flow through LaneSnapshot kernel (CQ #43)",
    },
    {
        "id": "cq_no_implicit_global_state",
        "module": "weave",
        "risk": "medium",
        "check": "forbidden_context_flag",
        "flag": "implicit_global_mutation",
        "message": "Governance modules must not use implicit global mutable state (CQ #45)",
    },
    {
        "id": "cq_test_parity_on_weave_change",
        "module": "weave",
        "risk": "medium",
        "check": "required_test_touch",
        "pattern": "test_weave",
        "message": "Weave functional changes require test update (CQ #44)",
    },
)

# Phase 16b — stub honesty fold (core law; corps cannot suppress to go green)
PHASE16_INVARIANTS: tuple[dict[str, Any], ...] = (
    {
        "id": "closure_no_stub_completion",
        "module": "stub_honesty",
        "risk": "high",
        "check": "forbidden_stub_completion",
        "message": "Cannot claim success or pass_gate with untraced stubs in closure paths",
    },
    {
        "id": "forbidden_suppress_stub_check",
        "module": "stub_honesty",
        "risk": "high",
        "check": "forbidden_context_flag",
        "flag": "suppress_stub_check",
        "message": "Stub honesty check cannot be suppressed without operator mutation",
    },
    {
        "id": "forbidden_import_only_conduct_complete",
        "module": "stub_honesty",
        "risk": "high",
        "check": "forbidden_context_flag",
        "flag": "import_only_as_conduct_complete",
        "message": "Import-only conduct-repair stub cannot count as structural completion",
    },
)

# Phase 9 — weave spine enforcement (pack + locked spine writes)
PHASE9_INVARIANTS: tuple[dict[str, Any], ...] = (
    {
        "id": "trinity_pack_consumable_only",
        "module": "trinity_pack",
        "risk": "medium",
        "check": "consumable_trinity_id_only",
        "message": "Maintenance PQ trinity_pack must resolve consumable ids only",
    },
    {
        "id": "respects_locked_spine_on_write",
        "module": "trinity_card_paths",
        "risk": "high",
        "check": "respects_locked_spine",
        "message": "Card writes must pass respects_locked_spine against maintenance core",
    },
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def invariants_dir(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "invariants"


def registry_index_path(vault_root: Path) -> Path:
    return invariants_dir(vault_root) / "registry_index.json"


@dataclass(frozen=True)
class InvariantEntry:
    id: str
    module: str
    risk: InvariantRisk
    status: InvariantStatus
    check: str
    message: str
    meta: dict[str, Any]

    # blast-radius: low


def _load_yaml_or_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore[import-untyped]

            raw = yaml.safe_load(text)
            return raw if isinstance(raw, dict) else None
        except Exception:
            return None
    try:
        raw = json.loads(text)
        return raw if isinstance(raw, dict) else None
    except json.JSONDecodeError:
        return None


def _save_entry(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml  # type: ignore[import-untyped]

        path.write_text(
            yaml.safe_dump(entry, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    except Exception:
        path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")


def entry_from_dict(raw: dict[str, Any]) -> InvariantEntry:
    return InvariantEntry(
        id=str(raw.get("id") or ""),
        module=str(raw.get("module") or ""),
        risk=str(raw.get("risk") or "medium"),  # type: ignore[arg-type]
        status=str(raw.get("status") or "draft"),  # type: ignore[arg-type]
        check=str(raw.get("check") or ""),
        message=str(raw.get("message") or ""),
        meta={k: v for k, v in raw.items() if k not in ("id", "module", "risk", "status", "check", "message")},
    )


def list_invariants(vault_root: Path, *, status: str | None = None) -> list[InvariantEntry]:
    base = invariants_dir(vault_root)
    if not base.is_dir():
        return []
    out: list[InvariantEntry] = []
    for path in sorted(base.glob("*.yaml")) + sorted(base.glob("*.json")):
        if path.name == "registry_index.json":
            continue
        raw = _load_yaml_or_json(path)
        if not raw:
            continue
        ent = entry_from_dict(raw)
        if status and ent.status != status:
            continue
        out.append(ent)
    return out


def load_invariant(vault_root: Path, invariant_id: str) -> InvariantEntry | None:
    base = invariants_dir(vault_root)
    for ext in (".yaml", ".json"):
        p = base / f"{invariant_id}{ext}"
        raw = _load_yaml_or_json(p)
        if raw:
            return entry_from_dict(raw)
    return None


def save_invariant(vault_root: Path, entry: dict[str, Any]) -> Path:
    iid = str(entry.get("id") or "")
    if not iid:
        raise ValueError("invariant id required")
    path = invariants_dir(vault_root) / f"{iid}.yaml"
    _save_entry(path, entry)
    _refresh_index(vault_root)
    return path


def _refresh_index(vault_root: Path) -> None:
    entries = list_invariants(vault_root)
    idx = {
        "updated_at": _now_iso(),
        "count": len(entries),
        "active": [e.id for e in entries if e.status == "active"],
        "pending_counselor": [e.id for e in entries if e.status == "pending_counselor"],
    }
    registry_index_path(vault_root).write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")


def bootstrap_n2_invariants(vault_root: Path, *, force: bool = False) -> dict[str, Any]:
    """N2 — seed registry with fixed module invariants + CQ rules (M2 auto-activate low)."""
    vault_root = vault_root.resolve()
    invariants_dir(vault_root).mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    skipped: list[str] = []
    activated: list[str] = []

    for spec in BOOTSTRAP_INVARIANTS:
        iid = str(spec["id"])
        existing = load_invariant(vault_root, iid)
        if existing and not force:
            skipped.append(iid)
            continue
        risk = str(spec.get("risk") or "low")
        # M2: low-risk auto-active; medium+ pending until counselor (Q3)
        status: InvariantStatus = "active" if risk == "low" else "pending_counselor"
        row = {
            **spec,
            "status": status,
            "bootstrapped_at": _now_iso(),
            "bootstrap_module": spec.get("module"),
        }
        save_invariant(vault_root, row)
        created.append(iid)
        if status == "active":
            activated.append(iid)

    append_metric_row(
        vault_root,
        {
            "metric_type": "invariant_registry_bootstrap",
            "created": created,
            "skipped": skipped,
            "activated": activated,
        },
    )
    return {
        "ok": True,
        "created": created,
        "skipped": skipped,
        "activated": activated,
        "active_count": len(list_invariants(vault_root, status="active")),
    }


def bootstrap_phase9_invariants(vault_root: Path, *, force: bool = False) -> dict[str, Any]:
    """Phase 9 — seed pack/spine invariants (medium+ pending until counselor)."""
    vault_root = vault_root.resolve()
    invariants_dir(vault_root).mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    skipped: list[str] = []

    for spec in PHASE9_INVARIANTS:
        iid = str(spec["id"])
        existing = load_invariant(vault_root, iid)
        if existing and not force:
            skipped.append(iid)
            continue
        risk = str(spec.get("risk") or "medium")
        status: InvariantStatus = "active" if risk == "low" else "pending_counselor"
        row = {
            **spec,
            "status": status,
            "bootstrapped_at": _now_iso(),
            "bootstrap_phase": 9,
        }
        save_invariant(vault_root, row)
        created.append(iid)

    append_metric_row(
        vault_root,
        {
            "metric_type": "invariant_registry_bootstrap",
            "phase": 9,
            "created": created,
            "skipped": skipped,
        },
    )
    return {"ok": True, "created": created, "skipped": skipped, "phase": 9}


def bootstrap_phase16_invariants(vault_root: Path, *, force: bool = False) -> dict[str, Any]:
    """Phase 16b — seed stub honesty invariants (high risk; activate via counselor)."""
    vault_root = vault_root.resolve()
    invariants_dir(vault_root).mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    skipped: list[str] = []

    for spec in PHASE16_INVARIANTS:
        iid = str(spec["id"])
        existing = load_invariant(vault_root, iid)
        if existing and not force:
            skipped.append(iid)
            continue
        risk = str(spec.get("risk") or "high")
        status: InvariantStatus = "active" if risk == "low" else "pending_counselor"
        row = {
            **spec,
            "status": status,
            "bootstrapped_at": _now_iso(),
            "bootstrap_phase": 16,
            "core_immutable": True,
        }
        save_invariant(vault_root, row)
        created.append(iid)

    append_metric_row(
        vault_root,
        {
            "metric_type": "invariant_registry_bootstrap",
            "phase": 16,
            "created": created,
            "skipped": skipped,
        },
    )
    return {"ok": True, "created": created, "skipped": skipped, "phase": 16}


def activate_invariant(
    vault_root: Path,
    invariant_id: str,
    *,
    counselor_approved: bool = False,
) -> dict[str, Any]:
    """M2 — activate entry; medium+ requires counselor_approved (Q3)."""
    ent = load_invariant(vault_root, invariant_id)
    if not ent:
        return {"ok": False, "error": "not_found", "id": invariant_id}
    if ent.risk in ("medium", "high") and not counselor_approved:
        return {
            "ok": False,
            "error": "counselor_approval_required",
            "id": invariant_id,
            "risk": ent.risk,
        }
    path = invariants_dir(vault_root) / f"{invariant_id}.yaml"
    raw = _load_yaml_or_json(path) or {}
    raw["status"] = "active"
    raw["activated_at"] = _now_iso()
    if counselor_approved:
        raw["counselor_approved"] = True
    save_invariant(vault_root, raw)
    return {"ok": True, "id": invariant_id, "status": "active"}
