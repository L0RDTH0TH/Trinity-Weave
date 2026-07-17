"""Operator feedback for user-story experiential gate (mirrors kinesthetic operator_feedback)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from ..factory.factory_output_gate import parse_factory_orchestrator_yaml
from .catalog_io import load_json, user_story_paths


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def default_feedback_rel(project_id: str) -> str:
    return f"1-Projects/{project_id}/Factory-DRB/operator-feedback/user-story-operator-feedback.yaml"


def resolve_feedback_path(vault_root: Path, project_id: str) -> Path:
    cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
    rf = cfg.get("roadmap_factory") if isinstance(cfg.get("roadmap_factory"), dict) else {}
    rel = str(rf.get("operator_feedback_rel") or default_feedback_rel(project_id))
    if not rel.startswith("1-Projects/"):
        rel = f"1-Projects/{project_id}/{rel.lstrip('/')}"
    return vault_root / rel


@dataclass(frozen=True)
class UserStoryFeedbackRow:
    row_id: str
    beat_ref: str
    experiential_pass: bool | None
    operator_confirmed: bool
    scopes_validated: bool
    notes: str
    source: str

    @property
    def decided(self) -> bool:
        return self.experiential_pass is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_id": self.row_id,
            "beat_ref": self.beat_ref,
            "experiential_pass": self.experiential_pass,
            "operator_confirmed": self.operator_confirmed,
            "scopes_validated": self.scopes_validated,
            "notes": self.notes,
            "source": self.source,
        }


def load_user_story_feedback(vault_root: Path, project_id: str) -> list[UserStoryFeedbackRow]:
    path = resolve_feedback_path(vault_root, project_id)
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rows = data.get("rows") if isinstance(data, dict) else []
    out: list[UserStoryFeedbackRow] = []
    if not isinstance(rows, list):
        return out
    for row in rows:
        if not isinstance(row, dict) or not row.get("row_id"):
            continue
        ep = row.get("experiential_pass")
        if ep is not None and not isinstance(ep, bool):
            ep = str(ep).lower() in ("true", "1", "yes")
        out.append(
            UserStoryFeedbackRow(
                row_id=str(row["row_id"]),
                beat_ref=str(row.get("beat_ref") or ""),
                experiential_pass=ep if isinstance(ep, bool) else None,
                operator_confirmed=bool(row.get("operator_confirmed")),
                scopes_validated=bool(row.get("scopes_validated", False)),
                notes=str(row.get("notes") or ""),
                source=str(row.get("source") or "operator"),
            )
        )
    return out


def save_user_story_feedback(
    vault_root: Path,
    project_id: str,
    rows: list[dict[str, Any]],
    *,
    catalog_signed_at: str | None = None,
) -> Path:
    path = resolve_feedback_path(vault_root, project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc: dict[str, Any] = {
        "schema_version": 1,
        "project_id": project_id,
        "updated_at": _utc_iso(),
        "rows": rows,
    }
    if catalog_signed_at:
        doc["catalog_signed_at"] = catalog_signed_at
    path.write_text(yaml.dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def list_pending_user_story_confirmations(
    vault_root: Path,
    project_id: str,
) -> list[dict[str, Any]]:
    pending: list[dict[str, Any]] = []
    for row in load_user_story_feedback(vault_root, project_id):
        if not row.operator_confirmed or row.experiential_pass is None:
            pending.append(row.to_dict())
    return pending


def scope_levels_for_validation(target_depth: int) -> list[int]:
    """Levels operator must read: L5 down through target_depth (inclusive)."""
    td = max(1, min(5, int(target_depth)))
    return list(range(5, td - 1, -1))


def row_target_depth(vault_root: Path, project_id: str, row_id: str) -> int:
    budget = load_json(user_story_paths(vault_root, project_id)["budget"])
    for br in budget.get("rows") or []:
        if isinstance(br, dict) and str(br.get("row_id")) == row_id:
            return int(br.get("target_depth") or 2)
    return 2


def row_scope_files_missing(
    vault_root: Path,
    project_id: str,
    row_id: str,
    *,
    target_depth: int | None = None,
) -> list[int]:
    """Machine pre-check: scope files that must exist before operator attestation."""
    from .depth_scope import scope_path

    td = target_depth if target_depth is not None else row_target_depth(vault_root, project_id, row_id)
    missing: list[int] = []
    for level in scope_levels_for_validation(td):
        path = scope_path(vault_root, project_id, row_id, level)
        if not path.is_file() or len(path.read_text(encoding="utf-8", errors="replace").strip()) < 40:
            missing.append(level)
    return missing


def all_rows_scopes_validated(vault_root: Path, project_id: str, row_ids: list[str]) -> bool:
    if not row_ids:
        return True
    by_id = {r.row_id: r for r in load_user_story_feedback(vault_root, project_id)}
    for rid in row_ids:
        r = by_id.get(rid)
        if r is None or not r.scopes_validated:
            return False
        if row_scope_files_missing(vault_root, project_id, rid):
            return False
    return True


def all_rows_operator_confirmed(vault_root: Path, project_id: str, row_ids: list[str]) -> bool:
    if not row_ids:
        return True
    by_id = {r.row_id: r for r in load_user_story_feedback(vault_root, project_id)}
    for rid in row_ids:
        r = by_id.get(rid)
        if r is None or not r.operator_confirmed or r.experiential_pass is not True:
            return False
    return True


def sync_feedback_from_budget(vault_root: Path, project_id: str) -> list[dict[str, Any]]:
    """Ensure feedback rows exist for active budget rows."""
    from .catalog_io import catalog_rows_by_id, load_json, load_yaml

    paths = user_story_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    catalog = load_yaml(paths["catalog"])
    catalog_by_id = catalog_rows_by_id(catalog)
    existing = {r.row_id: r for r in load_user_story_feedback(vault_root, project_id)}
    out_rows: list[dict[str, Any]] = []
    for br in budget.get("rows") or []:
        if not isinstance(br, dict):
            continue
        row_id = str(br.get("row_id") or "")
        if not row_id:
            continue
        cat = catalog_by_id.get(row_id) or {}
        prev = existing.get(row_id)
        out_rows.append(
            prev.to_dict()
            if prev
            else {
                "row_id": row_id,
                "beat_ref": str(cat.get("beat_ref") or ""),
                "experiential_pass": None,
                "operator_confirmed": False,
                "scopes_validated": False,
                "notes": "",
                "source": "sync",
            }
        )
    save_user_story_feedback(vault_root, project_id, out_rows)
    return out_rows
