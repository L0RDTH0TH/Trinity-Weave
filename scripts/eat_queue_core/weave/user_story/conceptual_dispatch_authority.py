"""Dispatch authority for conceptual factory deepen — feed gate over rollup telemetry."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .conceptual_factory_feed import (
    conceptual_factory_feed_ready,
    conceptual_factory_feed_report,
    resolve_feed_mint_batch,
)
from .conceptual_track_ready import load_conceptual_gate_config

AUTHORITY_ID = "factory_feed_gate"

_NOOP_MARKERS = ("deepen_noop", "noop")


@dataclass
class ConceptualDispatchVerdict:
    authority: str = AUTHORITY_ID
    ready: bool = False
    reason: str = ""
    mint_batch: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    deepen_required: bool = False
    forbid_deepen_noop: bool = False
    material_change_required: bool = False
    deepen_target: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "ready": self.ready,
            "reason": self.reason,
            "mint_batch": self.mint_batch,
            "evidence": dict(self.evidence),
            "deepen_required": self.deepen_required,
            "forbid_deepen_noop": self.forbid_deepen_noop,
            "material_change_required": self.material_change_required,
            "deepen_target": self.deepen_target,
        }


def _read_note_fm(path: Path) -> tuple[dict[str, Any], str]:
    if not path.is_file():
        return {}, ""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    fm = yaml.safe_load(text[4:end]) or {}
    body = text[end + 4 :].lstrip("\n")
    return (fm if isinstance(fm, dict) else {}), body


def _write_note_fm(path: Path, fm: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dumped = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{dumped}\n---\n\n{body.lstrip()}", encoding="utf-8")


def workflow_state_path(vault_root: Path, project_id: str) -> Path:
    return vault_root / "1-Projects" / project_id / "Roadmap" / "workflow_state.md"


def parse_deepen_target(reason: str) -> str:
    """Human/machine hint from feed gate reason (e.g. phase_1_secondary_tree)."""
    raw = str(reason or "").strip()
    if not raw:
        return ""
    m = re.search(r":phase_(\d+)", raw)
    if m:
        phase = m.group(1)
        if "secondary" in raw:
            return f"phase_{phase}_secondary_tree"
        if "tertiary" in raw:
            return f"phase_{phase}_tertiary_tree"
        if "primary" in raw:
            return f"phase_{phase}_primary"
        return f"phase_{phase}"
    if raw.startswith("feedstock_incomplete:"):
        return raw.split(":", 1)[-1]
    return raw


def build_conceptual_dispatch_verdict(
    vault_root: Path,
    project_id: str,
    goal_packet: dict[str, Any] | None = None,
) -> ConceptualDispatchVerdict:
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    packet = goal_packet if isinstance(goal_packet, dict) else {}
    gate = load_conceptual_gate_config(vault_root)
    mode = str(gate.get("mode") or "factory_feed_ready").lower().strip()
    batch = resolve_feed_mint_batch(vault_root, goal_packet=packet)
    report = conceptual_factory_feed_report(
        vault_root, pid, mint_batch=batch, goal_packet=packet
    )
    ready = bool(report.get("ok"))
    reason = str(report.get("reason") or "")
    evidence = report.get("evidence") if isinstance(report.get("evidence"), dict) else {}
    deepen_required = mode == "factory_feed_ready" and not ready
    return ConceptualDispatchVerdict(
        authority=AUTHORITY_ID if mode == "factory_feed_ready" else "conceptual_map_complete",
        ready=ready,
        reason=reason,
        mint_batch=batch,
        evidence=evidence,
        deepen_required=deepen_required,
        forbid_deepen_noop=deepen_required,
        material_change_required=deepen_required,
        deepen_target=parse_deepen_target(reason),
    )


def stamp_harness_gate_params(
    params: dict[str, Any],
    verdict: ConceptualDispatchVerdict,
) -> dict[str, Any]:
    """Merge harness dispatch law into RESUME_ROADMAP conceptual params."""
    out = dict(params)
    out["harness_gate_authority"] = verdict.authority
    out["harness_gate_ready"] = verdict.ready
    out["harness_gate_reason"] = verdict.reason
    out["harness_gate_mint_batch"] = verdict.mint_batch
    out["harness_forbid_deepen_noop"] = verdict.forbid_deepen_noop
    out["harness_material_change_required"] = verdict.material_change_required
    if verdict.deepen_target:
        out["harness_deepen_target"] = verdict.deepen_target
    if verdict.deepen_required:
        out["user_guidance"] = (
            f"Harness authority `{verdict.authority}` — feed gate RED "
            f"(`{verdict.reason}`). Deepen Roadmap/Phase-* feedstock until "
            f"`conceptual_factory_feed_ready` passes for mint_batch "
            f"`{verdict.mint_batch}`. Target: `{verdict.deepen_target or 'see gate reason'}`. "
            "Do NOT deepen_noop from legacy workflow_state `conceptual_map_complete: "
            "closed` or `conceptual_map_strict_gate` — those are rollup telemetry only. "
            "Do NOT deepen factory/l5 or User-Story/scopes/*/L5.md."
        )
    return out


def workflow_state_contradicts_feed_gate(vault_root: Path, project_id: str) -> bool:
    """True when workflow_state claims closed but live feed gate is red."""
    pid = str(project_id or "").strip()
    if not pid:
        return False
    gate = load_conceptual_gate_config(vault_root)
    if str(gate.get("mode") or "").lower().strip() != "factory_feed_ready":
        return False
    ready, _ = conceptual_factory_feed_ready(vault_root, pid)
    if ready:
        return False
    wf_path = workflow_state_path(vault_root, pid)
    fm, _ = _read_note_fm(wf_path)
    if not fm:
        return False
    closed_vals = {"closed", "complete", "done"}
    rollup_closed = str(fm.get("conceptual_map_complete") or "").lower() in closed_vals
    strict_pass = str(fm.get("conceptual_map_strict_gate") or "").lower() in {
        "pass",
        "passed",
        "complete",
    }
    return rollup_closed or strict_pass


def reconcile_workflow_state_telemetry(
    vault_root: Path,
    project_id: str,
    goal_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Demote legacy rollup completion stamps when factory_feed_gate is red.

    Opens conceptual_map_complete and records feed gate authority on workflow_state FM.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return {"ok": False, "reason": "no_project_id"}
    verdict = build_conceptual_dispatch_verdict(vault_root, pid, goal_packet)
    if verdict.ready:
        return {"ok": True, "changed": False, "reason": "feed_gate_ready"}
    wf_path = workflow_state_path(vault_root, pid)
    if not wf_path.is_file():
        return {"ok": True, "changed": False, "reason": "no_workflow_state"}
    fm, body = _read_note_fm(wf_path)
    if not fm:
        return {"ok": True, "changed": False, "reason": "empty_frontmatter"}

    closed_vals = {"closed", "complete", "done"}
    was_closed = str(fm.get("conceptual_map_complete") or "").lower() in closed_vals
    had_strict = str(fm.get("conceptual_map_strict_gate") or "").strip() != ""
    if not was_closed and not had_strict:
        return {"ok": True, "changed": False, "reason": "no_legacy_rollup_stamps"}

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fm["conceptual_map_complete"] = "open"
    fm["conceptual_map_strict_gate"] = "superseded_by_factory_feed_gate"
    fm["factory_feed_gate_authority"] = AUTHORITY_ID
    fm["factory_feed_gate_status"] = "red"
    fm["factory_feed_gate_reason"] = verdict.reason
    fm["factory_feed_gate_mint_batch"] = verdict.mint_batch
    if verdict.deepen_target:
        fm["conceptual_map_reconcile_cursor"] = verdict.deepen_target
    if str(fm.get("status") or "").lower() == "complete":
        fm["status"] = "generating"

    stamp = (
        f"| {now} | harness_reconcile | workflow_state | feed_gate | - | - | - | - | - | 90 | "
        f"Demoted legacy rollup closed stamps; authority={AUTHORITY_ID}; "
        f"reason={verdict.reason}; deepen_target={verdict.deepen_target or '-'} |"
    )
    if "## Log" in body and "| Timestamp |" in body:
        body = body.rstrip() + "\n" + stamp + "\n"
    else:
        body = body.rstrip() + "\n\n## Log\n\n" + stamp + "\n"

    _write_note_fm(wf_path, fm, body)
    return {
        "ok": True,
        "changed": True,
        "reason": verdict.reason,
        "deepen_target": verdict.deepen_target,
        "path": str(wf_path.relative_to(vault_root)),
    }


def _effective_action_noop(params: dict[str, Any]) -> bool:
    for key in (
        "effective_action",
        "pipeline_return",
        "chosen_action",
        "params_action_effective",
    ):
        val = str(params.get(key) or "").lower()
        if val and any(m in val for m in _NOOP_MARKERS):
            return True
    if str(params.get("reason_code") or "").lower().startswith("deepen_noop"):
        return True
    action = str(params.get("action") or "").lower()
    if "noop" in action:
        return True
    return False


def evaluate_feed_gate_consume_block(
    params: dict[str, Any],
    *,
    vault_root: Path | None = None,
) -> tuple[bool, list[str]]:
    """
    Return (block_consume, violations).

    When harness stamped forbid_deepen_noop and feed gate is still red, block noop
    and false-green consumes; allow real deepen with material change.
    """
    if not params.get("harness_forbid_deepen_noop"):
        return False, []

    track = str(params.get("roadmap_track") or "").lower()
    if track != "conceptual":
        return False, []

    pid = str(params.get("project_id") or "").strip()
    ready = params.get("harness_gate_ready") is True
    if vault_root is not None and pid:
        live_ready, live_reason = conceptual_factory_feed_ready(vault_root, pid)
        ready = live_ready
        if not ready:
            params = {**params, "harness_gate_ready": False, "harness_gate_reason": live_reason}

    if ready:
        return False, []

    if _effective_action_noop(params):
        return True, ["harness_gate_deepen_noop_forbidden"]

    material_required = params.get("harness_material_change_required") is True
    if material_required:
        asserted = params.get("material_state_change_asserted")
        if asserted is not True and str(asserted).lower() not in {"true", "1"}:
            return True, ["harness_gate_material_change_required"]

    return False, []


def reconcile_guidance_for_planner(verdict: ConceptualDispatchVerdict) -> str:
    if not verdict.deepen_required:
        return ""
    return (
        f"Factory cursor reconcile — `{verdict.authority}` RED (`{verdict.reason}`); "
        f"deepen Roadmap/Phase-* feedstock for mint_batch `{verdict.mint_batch}` "
        f"(target `{verdict.deepen_target or 'see harness_gate_reason'}`). "
        "Ignore legacy workflow_state conceptual_map_complete closed / strict_gate pass. "
        "Do NOT deepen_noop. Do NOT deepen factory/l5 or User-Story/scopes/*/L5.md."
    )
