"""Headless / harness path — invoke Slice Producer via `agent -p` before Layer 1 validation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ...host_runner import HostInvokeRequest, rel_log_path, resolve_host_runner
from ...pseudo_clock import load_knobs
from ...task_handoff_comms import append_agent_handoff_pair
from ..factory.slice_producer_harness import (
    load_producer_receipt,
    technical_slice_dir,
    validate_producer_receipt,
    validate_producer_review,
)
from .slice_producer_handlers import (
    SLICE_PRODUCER_MODES,
    _normalize_mode,
    build_slice_producer_handoff,
)
from ..persona_handoff import format_persona_block, load_pillar_packet_half_a_provenance

PM_AGENT_MAX_RETRIES = 2


def _entry_params(entry: dict[str, Any]) -> dict[str, Any]:
    raw = entry.get("params")
    return raw if isinstance(raw, dict) else {}


def _slice_id(entry: dict[str, Any]) -> str:
    return str(_entry_params(entry).get("slice_id") or "").strip()


def _review_needs_agent(vault_root: Path, slice_id: str) -> tuple[bool, list[str]]:
    review_path = technical_slice_dir(vault_root, slice_id) / "producer-review.json"
    if not review_path.is_file():
        return True, ["producer_review_missing"]
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return True, ["producer_review_invalid_json"]
    if not isinstance(review, dict):
        return True, ["producer_review_not_object"]
    ok, violations = validate_producer_review(vault_root, review)
    return not ok, violations


def needs_pm_agent_artifacts(vault_root: Path, entry: dict[str, Any]) -> bool:
    """True when compose/review artifacts are still missing or invalid for this PQ line."""
    mode = _normalize_mode(str(entry.get("mode") or ""))
    if mode not in SLICE_PRODUCER_MODES:
        return False
    slice_id = _slice_id(entry)
    if not slice_id:
        return True
    if mode == "SLICE_PRODUCER_COMPOSE":
        receipt = load_producer_receipt(vault_root, slice_id)
        if not receipt:
            return True
        ok, _ = validate_producer_receipt(vault_root, receipt, agent_path=True)
        return not ok
    need, _ = _review_needs_agent(vault_root, slice_id)
    return need


def build_slice_producer_agent_prompt(vault_root: Path, entry: dict[str, Any]) -> str:
    """Markdown hand-off for `agent -p` / Cursor Task(slice-producer)."""
    handoff = build_slice_producer_handoff(entry, vault_root)
    mode = str(handoff.get("agent_mode") or "compose")
    params = _entry_params(entry)
    eid = str(entry.get("id") or "")
    project_id = str(handoff.get("project_id") or "")
    slice_id = str(handoff.get("slice_id") or "")
    lane = str(handoff.get("queue_lane") or "godot")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ph = handoff.get("persona_handoff")
    persona_block = format_persona_block(ph if isinstance(ph, dict) else {})

    lines = [
        persona_block,
        "# Slice Producer — Implementation Cell PM",
        "",
        f"You are the **slice-producer** agent (`agent_mode: {mode}`).",
        "Follow `.cursor/agents/slice-producer.md` exactly.",
        "",
        "## Telemetry",
        "",
        f"- queue_entry_id: {eid}",
        f"- project_id: {project_id}",
        f"- queue_lane: {lane}",
        f"- slice_id: {slice_id}",
        f"- started_at: {stamp}",
        "",
        "## Queue entry",
        "",
        "```json",
        json.dumps(entry, indent=2),
        "```",
        "",
        "## Hand-off",
        "",
        "```yaml",
    ]
    for key, val in handoff.items():
        if isinstance(val, (dict, list)):
            lines.append(f"{key}: {json.dumps(val)}")
        else:
            lines.append(f"{key}: {val}")
    lines.append("```")
    lines.append("")

    if mode == "compose":
        packet = str(params.get("pillar_packet_path") or "")
        lines.extend(
            [
                "## Compose deliverables",
                "",
                f"Read pillar packet: `{packet}`",
                "",
                "Write:",
                f"- SIB + LMBs under `1-Projects/{project_id}/Factory-DRB/`",
                f"- CDP + `producer-receipt.json` under `.technical/factory/slice-briefs/{slice_id}/`",
                "",
                "Set `ok: true` on receipt only when UX crosswalk + all LMBs exist.",
                "Include `persona_attestation` on producer-receipt.json (not synthetic).",
                "",
            ]
        )
    else:
        wave = handoff.get("wave", 1)
        lines.extend(
            [
                "## Review deliverables",
                "",
                f"Review wave **{wave}** lane receipts for slice `{slice_id}`.",
                "",
                f"Write `.technical/factory/slice-briefs/{slice_id}/producer-review.json`",
                "with `ok`, `verdict`, `current_wave`, `more_waves`, `violations`,",
                "and `persona_drift_findings[]` (lane_id, ux_bullet_id, evidence_path).",
                "Use `persona_drift_clear: true` only when UX bullets were audited with evidence.",
                "",
            ]
        )

    lines.append("Do not append to PQ. Do not edit `.cursor/rules/**`.")
    return "\n".join(lines)


def run_slice_producer_agent(
    vault_root: Path,
    entry: dict[str, Any],
    *,
    dry_run: bool = False,
    timeout: int = 3600,
    log_path: Path | None = None,
    parent_run_id: str | None = None,
) -> dict[str, Any]:
    """Run HostRunner for one SLICE_PRODUCER_* line."""
    vault_root = vault_root.resolve()
    prompt = build_slice_producer_agent_prompt(vault_root, entry)
    runner = resolve_host_runner(vault_root)
    if not runner.available():
        probe = runner.invoke(
            HostInvokeRequest(vault_root=vault_root, handoff="", model="auto", role="slice_producer")
        )
        return {
            "ok": False,
            "error": probe.error or "cursor_or_agent_cli_not_found",
            "invoked": False,
        }
    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "invoked": False,
            "handoff_preview": prompt[:800],
        }

    params = _entry_params(entry)
    lane = str(entry.get("queue_lane") or params.get("queue_lane") or "godot")
    ph = params.get("persona_handoff") if isinstance(params.get("persona_handoff"), dict) else {}
    persona_id = str(ph.get("active_persona_id") or "") or None

    knobs = load_knobs(vault_root)
    model = str(knobs.get("headless_agent_model") or "auto").strip()

    if log_path is None:
        eid = str(entry.get("id") or "sp")[:24]
        log_dir = vault_root / ".technical/Run-Telemetry"
        log_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        log_path = log_dir / f"slice-producer-{eid}-{stamp}.log"

    hr = runner.invoke(
        HostInvokeRequest(
            vault_root=vault_root,
            handoff=prompt,
            model=model,
            timeout_sec=timeout,
            log_path=log_path,
            role="slice_producer",
        )
    )
    if hr.error and hr.exit_code is None:
        return {
            "ok": False,
            "error": hr.error,
            "invoked": True,
            "log_path": rel_log_path(vault_root, hr.log_path),
        }

    rel_log = rel_log_path(vault_root, hr.log_path or log_path) or str(log_path)
    return_body = rel_log if hr.ok else f"exit_code={hr.exit_code}\nsee {rel_log}"
    try:
        append_agent_handoff_pair(
            vault_root,
            lane=lane,
            queue_entry_id=str(entry.get("id") or ""),
            subagent_type="slice-producer",
            prompt=prompt,
            return_body=return_body,
            persona_id=persona_id,
            parent_run_id=str(parent_run_id or params.get("product_factory_run_id") or "-"),
            project_id=str(params.get("project_id") or entry.get("project_id") or "-"),
        )
    except OSError:
        pass

    return {
        "ok": bool(hr.ok),
        "invoked": True,
        "exit_code": hr.exit_code,
        "log_path": rel_log,
        "implementation_path": "agent_p",
    }


def ensure_pm_agent_artifacts(
    vault_root: Path,
    entry: dict[str, Any],
    *,
    dry_run: bool = False,
    timeout: int = 3600,
    log_path: Path | None = None,
    parent_run_id: str | None = None,
) -> dict[str, Any]:
    """Invoke PM agent when artifacts missing/invalid; retry up to PM_AGENT_MAX_RETRIES."""
    if not needs_pm_agent_artifacts(vault_root, entry):
        return {"ok": True, "invoked": False, "detail": "artifacts_present"}

    params = dict(_entry_params(entry))
    retries = int(params.get("pm_agent_retry_count") or 0)
    last_out: dict[str, Any] = {}

    while retries <= PM_AGENT_MAX_RETRIES:
        agent_out = run_slice_producer_agent(
            vault_root,
            entry,
            dry_run=dry_run,
            timeout=timeout,
            log_path=log_path,
            parent_run_id=parent_run_id,
        )
        last_out = agent_out
        if dry_run:
            return agent_out
        if not agent_out.get("ok"):
            return {**agent_out, "detail": "pm_agent_invoke_failed", "pm_agent_retry_count": retries}
        if not needs_pm_agent_artifacts(vault_root, entry):
            return {
                "ok": True,
                "invoked": True,
                "detail": "pm_agent_artifacts_ready",
                "pm_agent_retry_count": retries,
                **agent_out,
            }
        retries += 1
        entry = {**entry, "params": {**params, "pm_agent_retry_count": retries}}

    slice_id = _slice_id(entry)
    _, violations = (
        _review_needs_agent(vault_root, slice_id)
        if _normalize_mode(str(entry.get("mode") or "")) == "SLICE_PRODUCER_REVIEW"
        else (True, ["compose_receipt_invalid"])
    )
    return {
        "ok": False,
        "invoked": True,
        "detail": "pm_agent_ran_artifacts_still_missing",
        "pm_agent_retry_count": retries,
        "violations": violations,
        **last_out,
    }
