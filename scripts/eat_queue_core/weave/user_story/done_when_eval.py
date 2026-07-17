"""Canonical goal-packet done_when evaluation — Half A loop 2 machine gate."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, user_story_paths
from .conceptual_track_ready import conceptual_factory_handoff_ready
from .depth_scope import scope_path
from .loop2_prep import is_placeholder_l5
from .product_factory_state import load_product_factory, normalize_completed_phases, save_product_factory

OPERATOR_LOOP_2_DONE_WHEN_TOKENS: frozenset[str] = frozenset(
    {
        "operator_loop_2_blocked",
        "operator_loop_2_catalog_levels",
        "loop_2_catalog_levels",
        "l5_manual_gate",
        "operator_loop_2",
        "operator_loop_2_pending_sign_off",
    }
)


def _normalize_done_when_token(raw: Any) -> str:
    return str(raw or "").strip().lower().replace(" ", "_").replace("-", "_")


def done_when_requests_operator_loop_2(packet: dict[str, Any]) -> bool:
    criteria = packet.get("done_when") or []
    if not isinstance(criteria, list):
        return False
    for raw in criteria:
        key = _normalize_done_when_token(raw)
        if not key:
            continue
        if key in OPERATOR_LOOP_2_DONE_WHEN_TOKENS:
            return True
        if "operator_loop_2" in key or key.startswith("loop_2"):
            return True
    return False


def roadmap_tree_complete(vault_root: Path, project_id: str) -> bool:
    from .conceptual_track_ready import roadmap_tree_complete as _rtc

    return _rtc(vault_root, project_id)

LOOP_2_BLOCKED_AT = "operator_loop_2_catalog_levels"
LOOP_2_PENDING_SIGN_OFF = "operator_loop_2_pending_sign_off"
LOOP_2_PARK_BLOCKED_AT = frozenset({LOOP_2_BLOCKED_AT, LOOP_2_PENDING_SIGN_OFF})
FACTORY_STAGED_BLOCKED_PENDING_LOOP_2 = "blocked_pending_loop_2"
LOOP2_EVIDENCE_MACHINE_PREPARED = "machine_prepared_pending_operator_stamp"


class ExitClass(str, Enum):
    CLEAN = "clean_exit"
    OPERATOR_GATE = "operator_gate"
    FAILURE = "failure"


@dataclass(frozen=True)
class DoneWhenResult:
    matched: bool
    token: str = ""
    reason: str = ""
    exit_class: ExitClass = ExitClass.CLEAN
    evidence: dict[str, Any] = field(default_factory=dict)


def _operator_loop_at_2(pf: dict[str, Any]) -> bool:
    op = pf.get("operator_loop")
    if op in (2, "2"):
        return True
    normalized = str(op or "").strip().lower().replace("-", "_")
    return normalized in {"pending_human_sign_off", "operator_loop_2"}


def _conductor_parked_at_loop2(pf: dict[str, Any]) -> bool:
    if pf.get("loop2_exit_eligible") is True:
        return True
    blocked = str(pf.get("blocked_at") or "")
    if blocked not in LOOP_2_PARK_BLOCKED_AT:
        return False
    return _operator_loop_at_2(pf)


def operator_loop_2_pending(vault_root: Path, project_id: str) -> bool:
    """True when conductor is honestly parked at human Loop 2 (strict conceptual frozen first)."""
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return False

    strict_ok, _ = conceptual_factory_handoff_ready(vault_root, pid)
    if not strict_ok:
        return False

    paths = user_story_paths(vault_root, pid)
    if paths["state"].is_file():
        text = paths["state"].read_text(encoding="utf-8", errors="replace")
        if text.startswith("---"):
            end = text.find("\n---", 4)
            block = text[4:end] if end > 0 else ""
            if "operator_loop_2: pending_human_sign_off" in block:
                return True
            if f"blocked_at: {LOOP_2_PENDING_SIGN_OFF}" in block:
                return True
            if "blocked_at: operator_loop_2_pending_sign_off" in block:
                return True

    pf = load_product_factory(vault_root, pid)
    if pf.get("loop2_exit_eligible") is True:
        return True
    blocked = str(pf.get("blocked_at") or "")
    if blocked in (
        LOOP_2_PENDING_SIGN_OFF,
        "operator_loop_2_pending_sign_off",
        LOOP_2_BLOCKED_AT,
    ):
        return True
    op = pf.get("operator_loop")
    if op in (2, "2", "pending_human_sign_off"):
        return True
    return False


def _catalog_row_ids(vault_root: Path, project_id: str) -> list[str]:
    paths = user_story_paths(vault_root, project_id)
    if not paths["catalog"].is_file():
        return []
    catalog = load_yaml(paths["catalog"])
    by_id = catalog_rows_by_id(catalog)
    row_ids = [rid for rid, r in by_id.items() if r.get("planned") is not False]
    if not row_ids:
        row_ids = list(by_id.keys())
    return row_ids


def loop2_machine_artifacts_ready(
    vault_root: Path,
    project_id: str,
) -> tuple[bool, str, dict[str, Any]]:
    """
    Machine Loop 2 deliverables on disk — catalog + substantive L5 per row.

    Excludes budget, L1–L4, and operator catalog_signed_at.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return False, "no_project_id", {}

    if not roadmap_tree_complete(vault_root, pid):
        return False, "roadmap_tree_incomplete", {}

    strict_ok, strict_reason = conceptual_factory_handoff_ready(vault_root, pid)
    if not strict_ok:
        return False, f"conceptual_map_incomplete:{strict_reason}", {}

    paths = user_story_paths(vault_root, pid)
    if not paths["catalog"].is_file():
        return False, "catalog_missing", {}

    row_ids = _catalog_row_ids(vault_root, pid)
    if not row_ids:
        return False, "catalog_empty", {}

    l5_rows: list[str] = []
    for rid in row_ids:
        l5_path = scope_path(vault_root, pid, rid, 5)
        if not l5_path.is_file():
            return False, f"l5_missing:{rid}", {"row_ids": row_ids}
        text = l5_path.read_text(encoding="utf-8", errors="replace")
        if is_placeholder_l5(text):
            return False, f"l5_placeholder:{rid}", {"row_ids": row_ids}
        l5_rows.append(rid)

    evidence = {
        "project_id": pid,
        "catalog_rows": row_ids,
        "l5_rows": l5_rows,
    }
    return True, "loop2_machine_artifacts_ready", evidence


def _loop2_beats_satisfied(
    vault_root: Path,
    project_id: str,
    pf: dict[str, Any],
) -> tuple[bool, str]:
    if pf.get("loop2_exit_eligible") is True:
        return True, "loop2_exit_eligible"

    strict_ok, strict_reason = conceptual_factory_handoff_ready(vault_root, project_id)
    if not strict_ok:
        return False, f"conceptual_map_incomplete:{strict_reason}"

    completed = {str(x) for x in (pf.get("completed_phases") or [])}

    if "conceptual_deepen" not in completed and not roadmap_tree_complete(vault_root, project_id):
        return False, "conceptual_deepen_incomplete"

    paths = user_story_paths(vault_root, project_id)
    if "catalog_mint" not in completed and not paths["catalog"].is_file():
        return False, "catalog_mint_incomplete"

    if "loop2_prep" not in completed:
        arts_ok, art_reason, _ = loop2_machine_artifacts_ready(vault_root, project_id)
        if not arts_ok:
            return False, art_reason if art_reason.startswith("l5_") else "loop2_prep_incomplete"
        if pf.get("loop2_evidence_pack_status") or pf.get("l5_scope_path"):
            return True, "loop2_prep_inferred"
        return False, "loop2_prep_incomplete"

    return True, "loop2_beats_ok"


def loop2_machine_ready(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """Machine Loop 2 surface ready for overnight exit — artifacts + conductor park."""
    pid = str(project_id or "").strip()
    if not pid:
        return False, "no_project_id"

    pf = load_product_factory(vault_root, pid)
    strict_ok, strict_reason = conceptual_factory_handoff_ready(vault_root, pid)
    if not strict_ok:
        return False, f"conceptual_map_incomplete:{strict_reason}"

    arts_ok, art_reason, _ = loop2_machine_artifacts_ready(vault_root, pid)
    if not arts_ok:
        return False, art_reason

    if pf.get("loop2_exit_eligible") is True:
        return True, "loop2_exit_eligible"

    beats_ok, beats_reason = _loop2_beats_satisfied(vault_root, pid, pf)
    if not beats_ok:
        return False, beats_reason

    if not _conductor_parked_at_loop2(pf):
        return False, "conductor_not_at_loop_2"

    return True, "loop2_machine_ready"


def loop2_exit_eligible_for_project(vault_root: Path, project_id: str) -> bool:
    """Raw disk flag — use loop2_exit_honestly_eligible for routing/overnight exit."""
    pf = load_product_factory(vault_root, str(project_id or "").strip())
    return pf.get("loop2_exit_eligible") is True


def loop2_exit_honestly_eligible(vault_root: Path, project_id: str) -> bool:
    """Disk flag + live gate chain — safe for overnight exit and queue routing."""
    ok, _ = loop2_machine_ready(vault_root, project_id)
    return ok


def park_loop2_machine_ready(vault_root: Path, project_id: str) -> dict[str, Any]:
    """
    Atomically normalize conductor state when machine Loop 2 prep is on disk.

    Sets loop2_exit_eligible, completed_phases beats, and pending sign-off park.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return {"ok": False, "reason": "no_project_id"}

    strict_ok, strict_reason = conceptual_factory_handoff_ready(vault_root, pid)
    if not strict_ok:
        return {"ok": False, "reason": f"conceptual_map_incomplete:{strict_reason}"}

    arts_ok, reason, evidence = loop2_machine_artifacts_ready(vault_root, pid)
    if not arts_ok:
        return {"ok": False, "reason": reason, "evidence": evidence}

    pf = load_product_factory(vault_root, pid)
    if pf.get("loop2_exit_eligible") is True and _conductor_parked_at_loop2(pf):
        return {"ok": True, "reason": "already_parked", "evidence": evidence}

    completed = normalize_completed_phases(list(pf.get("completed_phases") or []))
    for beat in ("conceptual_deepen", "catalog_mint", "loop2_prep"):
        if beat not in completed:
            completed.append(beat)

    updates = {
        **pf,
        "operator_loop": 2,
        "blocked_at": LOOP_2_PENDING_SIGN_OFF,
        "loop2_exit_eligible": True,
        "completed_phases": completed,
        "factory_staged_dispatch": FACTORY_STAGED_BLOCKED_PENDING_LOOP_2,
    }
    if not pf.get("loop2_evidence_pack_status"):
        updates["loop2_evidence_pack_status"] = LOOP2_EVIDENCE_MACHINE_PREPARED

    save_product_factory(vault_root, pid, updates)
    return {"ok": True, "reason": "parked_loop2_machine_ready", "evidence": evidence}


def evaluate_done_when(
    vault_root: Path,
    packet: dict[str, Any],
    *,
    project_id: str | None = None,
) -> DoneWhenResult:
    """Single canonical gate — when matched=True, Half A overnight must stop."""
    if not done_when_requests_operator_loop_2(packet):
        return DoneWhenResult(matched=False)

    pid = str(project_id or packet.get("project_id") or "").strip()
    if not pid:
        return DoneWhenResult(matched=False, reason="no_project_id")

    criteria = packet.get("done_when") or []
    token = ""
    if isinstance(criteria, list):
        for raw in criteria:
            key = _normalize_done_when_token(raw)
            if key:
                token = key
                break

    ok, reason = loop2_machine_ready(vault_root, pid)
    _, _, evidence = loop2_machine_artifacts_ready(vault_root, pid)
    if ok:
        return DoneWhenResult(
            matched=True,
            token=token or "l5_manual_gate",
            reason=reason,
            exit_class=ExitClass.OPERATOR_GATE,
            evidence=evidence,
        )
    return DoneWhenResult(
        matched=False,
        token=token,
        reason=reason,
        exit_class=ExitClass.FAILURE,
        evidence=evidence,
    )
