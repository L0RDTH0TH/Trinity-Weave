"""Operator feedback artifacts — kinesthetic playtest_gate rows (structured YAML)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .proof_tiers import (
    is_proxy_pass_as_kinesthetic,
    normalize_source,
    source_may_ship_kinesthetic,
)

DEFAULT_FEEDBACK_REL = (
    "1-Projects/godot-genesis-mythos-master/Factory-DRB/operator-feedback/godot-closed-alpha-kinesthetic.yaml"
)

KINESTHETIC_CHECKLIST_IDS: tuple[str, ...] = (
    "Nav_LookWhileMove_FP",
    "Nav_LookWhileMove_DM",
    "Flow_Launch",
    "Flow_DM_Mode",
    "Flow_Ortho_Tabletop",
    "Anti_DevOnlyHUD",
    "Anti_HarnessSubstitutesPlaytest",
)

# Human-operate rows (Tier B kinesthetic) — operator playtest required at stage 3.
KINESTHETIC_HUMAN_IDS: tuple[str, ...] = tuple(
    cid for cid in KINESTHETIC_CHECKLIST_IDS if cid != "Anti_HarnessSubstitutesPlaytest"
)


@dataclass(frozen=True)
class FeedbackRow:
    checklist_id: str
    pass_: bool | None
    notes: str
    drb_ref: str
    source: str = ""
    kinesthetic: bool = True
    operator_confirmed: bool = False
    structural_hint: bool | None = None

    @property
    def decided(self) -> bool:
        return self.pass_ is not None

    @property
    def normalized_source(self) -> str:
        return normalize_source(self.source)


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore[import-untyped]

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_operator_feedback(vault_root: Path, rel: str = DEFAULT_FEEDBACK_REL) -> tuple[FeedbackRow, ...]:
    path = vault_root / rel
    if not path.is_file():
        return ()
    data = _load_yaml(path)
    rows_raw = data.get("feedback") or []
    out: list[FeedbackRow] = []
    if not isinstance(rows_raw, list):
        return ()
    for item in rows_raw:
        if not isinstance(item, dict) or "checklist_id" not in item:
            continue
        raw_pass = item.get("pass")
        pass_val: bool | None
        if raw_pass is None:
            pass_val = None
        else:
            pass_val = bool(raw_pass)
        hint_raw = item.get("structural_hint")
        hint: bool | None = bool(hint_raw) if hint_raw is not None else None
        kin = item.get("kinesthetic")
        kinesthetic = True if kin is None else bool(kin)
        out.append(
            FeedbackRow(
                checklist_id=str(item["checklist_id"]),
                pass_=pass_val,
                notes=str(item.get("notes") or ""),
                drb_ref=str(item.get("drb_ref") or ""),
                source=str(item.get("source") or ""),
                kinesthetic=kinesthetic,
                operator_confirmed=bool(item.get("operator_confirmed")),
                structural_hint=hint,
            )
        )
    return tuple(out)


def validate_kinesthetic_feedback(
    vault_root: Path,
    *,
    required_ids: tuple[str, ...],
    feedback_rel: str = DEFAULT_FEEDBACK_REL,
) -> list[str]:
    """Return violations (empty = ok). Enforces proof tiers — no proxy kinesthetic pass."""
    path = vault_root / feedback_rel
    violations: list[str] = []
    if not path.is_file():
        return [f"missing_operator_feedback:{feedback_rel}"]

    rows = load_operator_feedback(vault_root, feedback_rel)
    by_id = {r.checklist_id: r for r in rows}

    for cid in required_ids:
        row = by_id.get(cid)
        if row is None:
            violations.append(f"kinesthetic_feedback_missing:{cid}")
            continue
        # Structural checklist rows (kinesthetic: false) — pass/fail only, not operator proof tier.
        if not row.kinesthetic:
            if not row.decided:
                violations.append(f"checklist_feedback_undecided:{cid}")
            elif row.pass_ is not True:
                violations.append(f"checklist_feedback_fail:{cid}")
            continue
        if is_proxy_pass_as_kinesthetic(
            kinesthetic=row.kinesthetic,
            pass_val=row.pass_,
            source=row.source,
            operator_confirmed=row.operator_confirmed,
        ):
            violations.append(f"proxy_pass_as_kinesthetic:{cid}")
            continue
        if not row.decided:
            violations.append(f"kinesthetic_feedback_undecided:{cid}")
            continue
        if row.pass_ is False:
            violations.append(f"kinesthetic_feedback_fail:{cid}")
            continue
        if row.kinesthetic and not source_may_ship_kinesthetic(
            row.source,
            operator_confirmed=row.operator_confirmed,
        ):
            violations.append(f"invalid_proof_tier_for_pass:{cid}")

    return violations
