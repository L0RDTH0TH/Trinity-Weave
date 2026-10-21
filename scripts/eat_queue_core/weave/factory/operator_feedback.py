"""Operator feedback artifacts — playtest ids from proof-catalog only."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bindings import BindingMissingError, load_family, require_project_id
from .proof_tiers import (
    is_proxy_pass_as_kinesthetic,
    normalize_source,
    source_may_ship_kinesthetic,
)


def default_feedback_rel(project_id: str) -> str:
    from .bindings import factory_drb_rel

    return factory_drb_rel(project_id, "operator-feedback", "kinesthetic.yaml")


DEFAULT_FEEDBACK_REL = ""  # use default_feedback_rel(project_id)


def required_playtest_ids(vault_root: Path, project_id: str) -> tuple[str, ...]:
    """Sole home: proof-catalog.yaml required_playtest_ids. Missing key → ()."""
    pid = require_project_id(project_id)
    try:
        data = load_family(vault_root, pid, "proof-catalog")
    except BindingMissingError:
        return ()
    raw = data.get("required_playtest_ids")
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise BindingMissingError(
            "binding_missing", "proof-catalog:required_playtest_ids_not_list"
        )
    return tuple(str(x).strip() for x in raw if str(x).strip())


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


def load_operator_feedback(
    vault_root: Path,
    *,
    feedback_rel: str = "",
    project_id: str | None = None,
) -> list[FeedbackRow]:
    import yaml

    pid = str(project_id or "").strip()
    rel = feedback_rel or (default_feedback_rel(pid) if pid else "")
    if not rel:
        return []
    path = vault_root / rel
    if not path.is_file():
        return []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rows: list[FeedbackRow] = []
    for item in raw.get("feedback") or []:
        if not isinstance(item, dict):
            continue
        cid = str(item.get("checklist_id") or "").strip()
        if not cid:
            continue
        rows.append(
            FeedbackRow(
                checklist_id=cid,
                pass_=item.get("pass"),
                notes=str(item.get("notes") or ""),
                drb_ref=str(item.get("drb_ref") or ""),
                source=str(item.get("source") or ""),
                kinesthetic=item.get("kinesthetic") is not False,
                operator_confirmed=item.get("operator_confirmed") is True,
                structural_hint=item.get("structural_hint"),
            )
        )
    return rows


def validate_kinesthetic_feedback(
    vault_root: Path,
    *,
    required_ids: tuple[str, ...] | None = None,
    feedback_rel: str = "",
    project_id: str | None = None,
) -> list[str]:
    pid = str(project_id or "").strip()
    ids = required_ids
    if ids is None:
        ids = required_playtest_ids(vault_root, pid) if pid else ()
    if not ids:
        return []
    rows = {
        r.checklist_id: r
        for r in load_operator_feedback(
            vault_root, feedback_rel=feedback_rel, project_id=pid or None
        )
    }
    violations: list[str] = []
    for cid in ids:
        row = rows.get(cid)
        if row is None:
            violations.append(f"playtest_missing:{cid}")
            continue
        if not source_may_ship_kinesthetic(row.source) and is_proxy_pass_as_kinesthetic(
            row.source
        ):
            violations.append(f"playtest_proxy_source:{cid}:{normalize_source(row.source)}")
        if row.pass_ is not True:
            violations.append(f"playtest_not_pass:{cid}")
    return violations
