"""Operator confirm flow — set pass + operator_confirmed on kinesthetic feedback rows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .operator_feedback import DEFAULT_FEEDBACK_REL, KINESTHETIC_CHECKLIST_IDS, load_operator_feedback
from .proof_tiers import source_may_ship_kinesthetic

VALID_SOURCES = frozenset({"operator", "playtest_trace"})


@dataclass(frozen=True)
class OperatorConfirmResult:
    ok: bool
    rows_updated: int
    detail: str
    checklist_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "rows_updated": self.rows_updated,
            "detail": self.detail,
            "checklist_ids": list(self.checklist_ids),
        }


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _load_doc(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"feedback": []}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {"feedback": []}


def list_pending_confirmations(
    vault_root: Path,
    *,
    feedback_rel: str = DEFAULT_FEEDBACK_REL,
) -> list[dict[str, Any]]:
    rows = load_operator_feedback(vault_root, feedback_rel)
    pending: list[dict[str, Any]] = []
    for row in rows:
        if not row.kinesthetic:
            continue
        needs = not row.decided or not row.operator_confirmed
        if row.pass_ is True and row.normalized_source == "operator":
            continue
        if needs or (row.pass_ is True and row.normalized_source == "playtest_trace" and not row.operator_confirmed):
            pending.append(
                {
                    "checklist_id": row.checklist_id,
                    "pass": row.pass_,
                    "source": row.normalized_source,
                    "operator_confirmed": row.operator_confirmed,
                    "notes": row.notes[:120],
                }
            )
    return pending


def confirm_operator_feedback_row(
    vault_root: Path,
    *,
    checklist_id: str,
    pass_: bool,
    notes: str = "",
    source: str = "operator",
    feedback_rel: str = DEFAULT_FEEDBACK_REL,
    operator_confirmed: bool = True,
) -> OperatorConfirmResult:
    vault_root = vault_root.resolve()
    cid = checklist_id.strip()
    if not cid:
        return OperatorConfirmResult(False, 0, "missing_checklist_id", ())

    src = source.strip().lower() or "operator"
    if src not in VALID_SOURCES:
        return OperatorConfirmResult(False, 0, f"invalid_source:{src}", (cid,))

    if pass_ and not source_may_ship_kinesthetic(src, operator_confirmed=operator_confirmed):
        return OperatorConfirmResult(False, 0, f"proof_tier_blocks_pass:{src}", (cid,))

    out_path = vault_root / feedback_rel
    doc = _load_doc(out_path)
    rows_raw = list(doc.get("feedback") or [])
    updated = 0
    found = False
    merged: list[dict[str, Any]] = []

    for item in rows_raw:
        if not isinstance(item, dict) or "checklist_id" not in item:
            merged.append(item)
            continue
        if str(item["checklist_id"]) != cid:
            merged.append(item)
            continue
        found = True
        merged.append(
            {
                **item,
                "checklist_id": cid,
                "kinesthetic": True,
                "pass": pass_,
                "source": src,
                "operator_confirmed": operator_confirmed,
                "notes": notes or item.get("notes") or "",
                "confirmed_at": _utc_iso(),
            }
        )
        updated += 1

    if not found:
        merged.append(
            {
                "checklist_id": cid,
                "kinesthetic": True,
                "pass": pass_,
                "source": src,
                "operator_confirmed": operator_confirmed,
                "notes": notes,
                "confirmed_at": _utc_iso(),
            }
        )
        updated += 1

    doc["feedback"] = merged
    doc["last_operator_confirm"] = _utc_iso()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")

    return OperatorConfirmResult(True, updated, "operator_confirm_ok", (cid,))


def confirm_from_playtest_ingest(
    vault_root: Path,
    *,
    feedback_rel: str = DEFAULT_FEEDBACK_REL,
    only_window_pass: bool = True,
    dry_run: bool = False,
) -> OperatorConfirmResult:
    """
    Confirm playtest_trace rows where operator agrees with window_pass aggregation.

    Sets operator_confirmed true; pass mirrors playtest_window_pass when only_window_pass.
    """
    rows = load_operator_feedback(vault_root, feedback_rel)
    targets: list[tuple[str, bool, str]] = []
    for row in rows:
        if row.normalized_source != "playtest_trace":
            continue
        if row.operator_confirmed:
            continue
        win = "window_pass=true" in row.notes or "window_pass=True" in row.notes
        if only_window_pass and not win:
            continue
        if "window_pass=false" in row.notes.lower():
            if only_window_pass:
                continue
            targets.append((row.checklist_id, False, row.notes))
        else:
            targets.append((row.checklist_id, True, row.notes))

    if dry_run:
        return OperatorConfirmResult(
            True,
            len(targets),
            "dry_run",
            tuple(t[0] for t in targets),
        )

    total = 0
    ids: list[str] = []
    for cid, pass_val, notes in targets:
        r = confirm_operator_feedback_row(
            vault_root,
            checklist_id=cid,
            pass_=pass_val,
            notes=notes,
            source="playtest_trace",
            feedback_rel=feedback_rel,
            operator_confirmed=True,
        )
        if r.ok:
            total += r.rows_updated
            ids.extend(r.checklist_ids)

    return OperatorConfirmResult(
        bool(total or not targets),
        total,
        "confirm_from_ingest_ok" if total else "no_ingest_rows_to_confirm",
        tuple(ids),
    )


def confirm_all_kinesthetic_operator(
    vault_root: Path,
    *,
    pass_: bool,
    feedback_rel: str = DEFAULT_FEEDBACK_REL,
    notes: str = "",
) -> OperatorConfirmResult:
    """Bulk operator source confirm for all kinesthetic checklist IDs."""
    total = 0
    ids: list[str] = []
    for cid in KINESTHETIC_CHECKLIST_IDS:
        r = confirm_operator_feedback_row(
            vault_root,
            checklist_id=cid,
            pass_=pass_,
            notes=notes,
            source="operator",
            feedback_rel=feedback_rel,
            operator_confirmed=True,
        )
        if r.ok:
            total += r.rows_updated
            ids.append(cid)
    return OperatorConfirmResult(True, total, "bulk_operator_confirm", tuple(ids))
