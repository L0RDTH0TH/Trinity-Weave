"""interpretation_pass — Stack-Charter + DRB/IIB gate before factory lane work."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .factory_little_val import FactoryLittleValResult
from .lane_charters import load_lane_charter

STACK_CHARTER_REL = "1-Projects/genesis-mythos-master/Factory-DRB/Stack-Charter-v0.md"
SPINE_HOST_REL = "1-Projects/genesis-mythos-master/Factory-DRB/Spine-Host-Contract-v0.md"
CONSTITUTION_REL = "1-Projects/genesis-mythos-master/Factory-DRB/Implementation-Factory-Constitution.md"


@dataclass(frozen=True)
class InterpretationPassResult:
    ok: bool
    little_val: FactoryLittleValResult
    detail: str
    drb_ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "detail": self.detail,
            "drb_ref": self.drb_ref,
            "violations": list(self.little_val.anti_pattern_violations),
        }


def _charter_raw(vault_root: Path, lane_id: str) -> dict[str, Any]:
    ch = load_lane_charter(vault_root, lane_id)
    if ch is None:
        return {}
    raw = yaml.safe_load(ch.path.read_text(encoding="utf-8")) or {}
    return raw if isinstance(raw, dict) else {}


def run_interpretation_pass(
    vault_root: Path,
    *,
    lane_id: str | None = None,
    job: dict[str, Any] | None = None,
    require_drb: bool | None = None,
) -> InterpretationPassResult:
    vault_root = vault_root.resolve()
    violations: list[str] = []

    for rel, label in (
        (STACK_CHARTER_REL, "stack_charter_v0"),
        (SPINE_HOST_REL, "spine_host_contract"),
        (CONSTITUTION_REL, "implementation_factory_constitution"),
    ):
        if not (vault_root / rel).is_file():
            violations.append(f"missing_signed_artifact:{label}")

    lid = lane_id or str((job or {}).get("lane_id") or "")
    fields = _charter_raw(vault_root, lid) if lid else {}
    drb_ref = str(fields.get("drb_ref") or (job or {}).get("drb_ref") or "")
    interpretation_required = fields.get("interpretation_required", True)
    if require_drb is not None:
        interpretation_required = require_drb

    if interpretation_required and lid:
        if not drb_ref:
            violations.append("missing_drb_ref_on_charter")
        elif not (vault_root / drb_ref).is_file():
            violations.append(f"drb_ref_not_found:{drb_ref}")

    for req in ("requires_adc", "requires_tac", "requires_cdc", "requires_pdc", "requires_audc"):
        if fields.get(req):
            # Consumer lane declares dependency — interpretation pass records intent
            pass

    ok = len(violations) == 0
    lv = FactoryLittleValResult(ok, violations, "interpretation_pass")
    detail = "; ".join(violations) if violations else "interpretation_pass_ok"
    return InterpretationPassResult(ok, lv, detail, drb_ref=drb_ref or None)
