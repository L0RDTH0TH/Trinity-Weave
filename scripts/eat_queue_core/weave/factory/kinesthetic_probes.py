"""Prefer structural probes — engine-neutral via proof_runner + project proof-catalog.

No baked probe ids, scene names, or engine smokes in production Python.
Empty checklist → nothing runs. Unknown probe id → UnknownProbeError.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .operator_feedback import DEFAULT_FEEDBACK_REL
from .product_kinesthetic_honesty import row_is_protected_override
from .proof_runner import UnknownProbeError, run_named_probes
from .proof_tiers import normalize_source


@dataclass(frozen=True)
class ProbeResult:
    checklist_id: str
    pass_: bool
    source: str
    evidence: str
    kinesthetic: bool = True

    def to_feedback_row(self) -> dict[str, Any]:
        row: dict[str, Any] = {
            "checklist_id": self.checklist_id,
            "kinesthetic": self.kinesthetic,
            "source": "structural_lint",
            "probed_at": datetime.now(timezone.utc).isoformat(),
            "notes": self.evidence[:500],
            "drb_ref": "",
        }
        if self.kinesthetic:
            row["pass"] = None
            row["structural_hint"] = self.pass_
        else:
            row["pass"] = self.pass_
        return row


def run_kinesthetic_probes(
    vault_root: Path,
    *,
    run_smokes: bool = True,
    project_id: str | None = None,
    checklist_ids: tuple[str, ...] | None = None,
    map_ticket: bool = False,
    proof_shape: str | None = None,
) -> tuple[ProbeResult, ...]:
    del run_smokes  # smokes are project commands in proof-catalog, not harness defaults
    # Map / contract: None does not mean run every probe.
    if map_ticket and checklist_ids is None:
        checklist_ids = ()
    if str(proof_shape or "").strip().lower() == "contract" and checklist_ids is None:
        checklist_ids = ()

    if checklist_ids is None:
        # Legacy non-map bare call: run nothing (no catalog iteration).
        return ()
    if not checklist_ids:
        return ()

    pid = str(project_id or "").strip()
    if not pid:
        return tuple(
            ProbeResult(str(cid), False, "static", "project_id_missing")
            for cid in checklist_ids
            if str(cid).strip()
        )

    try:
        outcomes = run_named_probes(vault_root, pid, list(checklist_ids))
    except UnknownProbeError as exc:
        return (ProbeResult(exc.probe_id, False, "static", f"unknown_probe:{exc.probe_id}"),)

    return tuple(
        ProbeResult(o.probe_id, o.ok, "static", o.detail) for o in outcomes
    )


def write_operator_feedback_from_probes(
    vault_root: Path,
    probes: tuple[ProbeResult, ...],
    *,
    feedback_rel: str = DEFAULT_FEEDBACK_REL,
    respect_operator_override: bool = True,
    project_id: str | None = None,
) -> Path:
    from .factory_drb_paths import factory_drb_dir, resolve_project_id

    pid = resolve_project_id(vault_root, project_id)
    out_path = vault_root / feedback_rel
    existing: dict[str, Any] = {}
    if out_path.is_file():
        existing = yaml.safe_load(out_path.read_text(encoding="utf-8")) or {}

    prior_rows: dict[str, dict[str, Any]] = {}
    for row in existing.get("feedback") or []:
        if isinstance(row, dict) and "checklist_id" in row:
            prior_rows[str(row["checklist_id"])] = row

    merged: list[dict[str, Any]] = []
    for probe in probes:
        prior = prior_rows.get(probe.checklist_id, {})
        prior_source = str(prior.get("source") or "")
        if respect_operator_override and row_is_protected_override(prior_source):
            if prior.get("operator_confirmed") or normalize_source(prior_source) == "operator":
                merged.append(prior)
                continue
        merged.append(probe.to_feedback_row())

    doc: dict[str, Any] = {
        "schema_version": 1,
        "project_id": pid,
        "release_tier": "",
        "playtest_gate": "structural_lint_and_trace",
        "last_probe_run": datetime.now(timezone.utc).isoformat(),
        "drb_refs": [],
        "feedback": merged,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")
    return out_path


def run_and_sync_probes(
    vault_root: Path,
    *,
    run_smokes: bool = True,
    write_feedback: bool = True,
    project_id: str | None = None,
    checklist_ids: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    probes = run_kinesthetic_probes(
        vault_root,
        run_smokes=run_smokes,
        project_id=project_id,
        checklist_ids=checklist_ids if checklist_ids is not None else (),
    )
    out_path = None
    if write_feedback:
        out_path = write_operator_feedback_from_probes(
            vault_root, probes, project_id=project_id
        )

    all_ok = all(p.pass_ for p in probes if p.kinesthetic) if probes else True
    return {
        "all_ok": all_ok,
        "feedback_path": str(out_path) if out_path else None,
        "probes": [
            {
                "checklist_id": p.checklist_id,
                "pass": p.pass_,
                "source": p.source,
                "evidence": p.evidence,
                "kinesthetic": p.kinesthetic,
            }
            for p in probes
        ],
    }
