"""Factory persona registry + handoff envelope for Half A / Half B."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

COUNCIL_ESCALATION_TOOLS: dict[str, Any] = {
    "council_request": {
        "available": True,
        "forbidden": [
            "nested_task_librarian_council",
            "nested_task_curator_council",
            "nested_task_technical_weave",
        ],
        "how": "append_factory_escalation",
        "when_to_use": [
            "unresolvable_pillar_conflict",
            "preservation_risk",
            "cross_domain_concern",
        ],
        "when_not": ["routine_deepen", "pseudo_code_gap", "lane_rework"],
    }
}


@dataclass(frozen=True)
class PersonaSpec:
    persona_id: str
    label: str
    factory_half: str
    factory_phase: str
    voice_summary: str
    writes: str
    must_not: str


HALF_A_PERSONAS: dict[str, PersonaSpec] = {
    "half_a.conceptual_architect": PersonaSpec(
        persona_id="half_a.conceptual_architect",
        label="Conceptual Architect",
        factory_half="half_a",
        factory_phase="conceptual_deepen",
        voice_summary="Product architect — shape, nouns, PMG fidelity",
        writes="Conceptual roadmap notes, CDRs",
        must_not="Pseudo-code, implementation paths, game-repo edits",
    ),
    "half_a.catalog_ux_indexer": PersonaSpec(
        persona_id="half_a.catalog_ux_indexer",
        label="Catalog UX Indexer",
        factory_half="half_a",
        factory_phase="catalog_mint",
        voice_summary="UX indexer — deliverable rows, dimensions, L5 draft assist",
        writes="slice-catalog.yaml, scope drafts",
        must_not="Task sprawl, catalog_signed_at, execution pins as truth, RESUME_ROADMAP L5 deepen",
    ),
    "half_a.execution_tech_lead": PersonaSpec(
        persona_id="half_a.execution_tech_lead",
        label="Execution Tech Lead",
        factory_half="half_a",
        factory_phase="execution_deepen",
        voice_summary="Junior-dev tech lead — interfaces, pseudo-code, ux_context crosswalk",
        writes="Execution roadmap notes, pin targets",
        must_not="UX redefinition, game-repo edits",
    ),
}

LANE_PERSONA_VOICE: dict[str, str] = {
    "presentation": "Player-facing shell, HUD, input affordance; kinesthetic honesty",
    "content": "Copy, data tables, narrative stubs; no scene graph ownership",
    "module": "Systems/C# services; no UI polish",
    "asset": "Art/audio asset integration per charter; no gameplay systems",
    "techart": "Shaders, VFX, rendering hooks per charter",
    "audio": "Audio buses, cues, mix stubs per charter",
}

HALF_B_PM_COMPOSE = PersonaSpec(
    persona_id="half_b.slice_producer_pm",
    label="Slice Producer PM (compose)",
    factory_half="half_b",
    factory_phase="pm_compose",
    voice_summary="UX-first PM — crosswalk L5 to lanes, tradeoffs",
    writes="SIB, LMBs, CDP, producer-receipt.json",
    must_not="Game-repo edits, direct PQ append",
)

HALF_B_PM_REVIEW = PersonaSpec(
    persona_id="half_b.slice_producer_pm",
    label="Slice Producer PM (review)",
    factory_half="half_b",
    factory_phase="pm_review",
    voice_summary="Hostile PM auditor — did lanes honor UX bullets?",
    writes="producer-review.json, rework proposals",
    must_not="Implement lane work, retro-rationalize lane diffs",
)


def persona_id_for_half_a_params(params: dict[str, Any]) -> str | None:
    linked = str(params.get("linked_phase") or "").lower()
    track = str(params.get("roadmap_track") or "execution").lower()
    if linked in ("conceptual", "conceptual_deepen") or track == "conceptual":
        return "half_a.conceptual_architect"
    if linked in ("catalog_mint", "catalog"):
        return "half_a.catalog_ux_indexer"
    if linked in ("execution", "execution_deepen") or track == "execution":
        if params.get("product_factory_run_id"):
            return "half_a.execution_tech_lead"
    return None


def persona_spec_for_id(persona_id: str) -> PersonaSpec | None:
    if persona_id in HALF_A_PERSONAS:
        return HALF_A_PERSONAS[persona_id]
    if persona_id == "half_b.slice_producer_pm":
        return HALF_B_PM_COMPOSE
    if persona_id.startswith("half_b.lane."):
        lane_id = persona_id.split(".", 2)[-1]
        voice = LANE_PERSONA_VOICE.get(lane_id, "Factory lane discipline per charter")
        return PersonaSpec(
            persona_id=persona_id,
            label=f"Lane {lane_id}",
            factory_half="half_b",
            factory_phase="lane_implement",
            voice_summary=voice,
            writes="Game repo under zone_write only",
            must_not="RESUME_ROADMAP, redefining L5, editing vault roadmap",
        )
    return None


def _default_interrogation() -> dict[str, Any]:
    return {
        "mode": "external_audit",
        "forbidden": ["retro_rationalize_upstream", "merge_personas"],
        "required_questions": [
            "Which upstream artifact claims justify this change?",
            "If this contradicts active_persona constraints, flag persona_drift — do not explain it away.",
        ],
    }


def _upstream_half_a_chain(persona_id: str) -> list[dict[str, Any]]:
    order = [
        "half_a.conceptual_architect",
        "half_a.catalog_ux_indexer",
        "half_a.execution_tech_lead",
    ]
    upstream: list[dict[str, Any]] = []
    specs = {
        "half_a.conceptual_architect": (
            "Roadmap/ conceptual phase notes",
            "Shape and nouns; no pseudo-code",
        ),
        "half_a.catalog_ux_indexer": (
            "Roadmap/User-Story/slice-catalog.yaml",
            "Deliverable rows + dimensions",
        ),
        "half_a.execution_tech_lead": (
            "Roadmap/Execution/",
            "Pseudo-code and pins against UX scopes",
        ),
    }
    try:
        idx = order.index(persona_id)
    except ValueError:
        return upstream
    for pid in order[:idx]:
        paths, summary = specs[pid]
        upstream.append(
            {
                "actor": pid,
                "artifact_paths": [paths],
                "contract_summary": summary,
            }
        )
    return upstream


def build_persona_envelope(
    *,
    persona_id: str,
    upstream: list[dict[str, Any]] | None = None,
    interrogation_mode: str = "owner_write",
    half_a_provenance: dict[str, Any] | None = None,
    sibling_lane_status: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    spec = persona_spec_for_id(persona_id)
    if spec is None:
        return {}

    if upstream is None and persona_id.startswith("half_a."):
        upstream = _upstream_half_a_chain(persona_id)

    interrogation = _default_interrogation()
    if interrogation_mode == "owner_write":
        interrogation = {
            **interrogation,
            "mode": "owner_write",
            "note": "You own the write; helpers audit only — do not let helpers co-author.",
        }

    envelope: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "active_persona_id": spec.persona_id,
        "active_persona_label": spec.label,
        "factory_half": spec.factory_half,
        "factory_phase": spec.factory_phase,
        "voice_summary": spec.voice_summary,
        "writes": spec.writes,
        "must_not": spec.must_not,
        "upstream": upstream or [],
        "interrogation_contract": interrogation,
        "escalation_tools": COUNCIL_ESCALATION_TOOLS,
        "return_contract": {
            "persona_attestation": {
                "persona_id": spec.persona_id,
                "wrote_paths": [],
                "persona_violations": [],
            },
            "optional_escalation": {
                "request_council": False,
                "council_context": None,
                "failure_class": None,
            },
        },
    }
    if half_a_provenance:
        envelope["half_a_provenance"] = half_a_provenance
    if sibling_lane_status:
        envelope["sibling_lane_status"] = sibling_lane_status
    return envelope


def merge_persona_into_params(params: dict[str, Any]) -> dict[str, Any]:
    """Attach persona_handoff to queue params when product-factory scoped."""
    merged = dict(params)
    if merged.get("persona_handoff"):
        return merged

    pid = persona_id_for_half_a_params(merged)
    if pid:
        merged["persona_handoff"] = build_persona_envelope(persona_id=pid)
        return merged

    lane_id = str(merged.get("lane_id") or "")
    if lane_id and str(merged.get("action") or "").lower() in ("factory_lane", "implement_slice"):
        upstream_pm: list[dict[str, Any]] = []
        sib = str(merged.get("slice_brief_path") or "")
        lmb = str(merged.get("lane_mission_path") or "")
        if sib or lmb:
            upstream_pm.append(
                {
                    "actor": "half_b.slice_producer_pm",
                    "artifact_paths": [p for p in (sib, lmb) if p],
                    "contract_summary": "SIB/LMB from PM compose",
                }
            )
        merged["persona_handoff"] = build_persona_envelope(
            persona_id=f"half_b.lane.{lane_id}",
            upstream=upstream_pm,
            interrogation_mode="owner_write",
            half_a_provenance=merged.get("half_a_provenance")
            if isinstance(merged.get("half_a_provenance"), dict)
            else None,
            sibling_lane_status=merged.get("sibling_lane_status")
            if isinstance(merged.get("sibling_lane_status"), list)
            else None,
        )
    return merged


def build_pm_persona_envelope(
    *,
    agent_mode: str,
    half_a_provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    mode = agent_mode.lower()
    spec = HALF_B_PM_REVIEW if mode == "review" else HALF_B_PM_COMPOSE
    upstream: list[dict[str, Any]] = []
    if half_a_provenance:
        arts = half_a_provenance.get("artifacts") if isinstance(half_a_provenance.get("artifacts"), dict) else {}
        paths = [str(v) for v in arts.values() if v]
        personas = half_a_provenance.get("personas") or []
        upstream.append(
            {
                "actor": ",".join(str(p) for p in personas) if personas else "half_a",
                "artifact_paths": paths,
                "contract_summary": "Operator-attested Half A scopes and execution pins",
            }
        )
    interrogation = "external_audit" if mode == "review" else "owner_write"
    env = build_persona_envelope(
        persona_id=spec.persona_id,
        upstream=upstream,
        interrogation_mode=interrogation,
        half_a_provenance=half_a_provenance,
    )
    if mode == "review":
        env["factory_phase"] = "pm_review"
        env["active_persona_label"] = HALF_B_PM_REVIEW.label
        env["voice_summary"] = HALF_B_PM_REVIEW.voice_summary
        env["writes"] = HALF_B_PM_REVIEW.writes
        env["must_not"] = HALF_B_PM_REVIEW.must_not
    return env


def build_validator_persona_supplement(params: dict[str, Any]) -> dict[str, Any]:
    """Extra fields for nested Task(validator) when factory persona_handoff is active."""
    ph = params.get("persona_handoff")
    if not isinstance(ph, dict) or not ph.get("active_persona_id"):
        return {}
    return {
        "persona_fidelity_check": True,
        "persona_handoff": ph,
        "interrogation_contract": ph.get("interrogation_contract") or _default_interrogation(),
        "validator_instruction": (
            "You did not write the upstream artifacts. Audit persona fidelity: "
            "flag persona_drift or upstream_unattested_claim — do not retro-rationalize for the writer."
        ),
        "reason_codes_hint": ["persona_drift", "upstream_unattested_claim"],
    }


def format_persona_block(envelope: dict[str, Any]) -> str:
    """Markdown block prepended to agent prompts."""
    if not envelope:
        return ""
    lines = [
        "## context_envelope",
        "",
        "```yaml",
        json.dumps({"persona_handoff": envelope}, indent=2, ensure_ascii=False),
        "```",
        "",
        f"**Active persona:** {envelope.get('active_persona_label')} (`{envelope.get('active_persona_id')}`)",
        "",
        f"- **Voice:** {envelope.get('voice_summary')}",
        f"- **Writes:** {envelope.get('writes')}",
        f"- **Must NOT:** {envelope.get('must_not')}",
        "",
    ]
    upstream = envelope.get("upstream") or []
    if upstream:
        lines.append("### Upstream (interrogate — do not inherit their voice)")
        for u in upstream:
            if isinstance(u, dict):
                lines.append(
                    f"- `{u.get('actor')}`: {u.get('contract_summary')} — "
                    f"{', '.join(u.get('artifact_paths') or [])}"
                )
        lines.append("")

    prov = envelope.get("half_a_provenance")
    if isinstance(prov, dict) and prov.get("artifacts"):
        lines.append("### Half A provenance")
        lines.append("```yaml")
        lines.append(json.dumps(prov, indent=2, ensure_ascii=False))
        lines.append("```")
        lines.append("")

    ic = envelope.get("interrogation_contract") if isinstance(envelope.get("interrogation_contract"), dict) else {}
    if ic.get("mode") == "external_audit":
        lines.append(
            "**Auditor mode:** You did not produce the upstream artifacts. "
            "Ask why they did what they did; flag persona_drift instead of explaining it away."
        )
        lines.append("")

    esc = envelope.get("escalation_tools") if isinstance(envelope.get("escalation_tools"), dict) else {}
    cr = esc.get("council_request") if isinstance(esc.get("council_request"), dict) else {}
    if cr.get("available"):
        lines.append(
            "**Council escalation (optional):** append `factory_run_escalation.jsonl` with "
            "`request_council: true` — never nested Task(council seats)."
        )
        lines.append("")

    lines.append(
        "**Return:** include `persona_attestation` in your structured return "
        "(persona_id, wrote_paths, persona_violations)."
    )
    lines.append("")
    return "\n".join(lines)


def load_pillar_packet_half_a_provenance(
    vault_root: Path, packet_path: str
) -> dict[str, Any] | None:
    path = vault_root / packet_path if not Path(packet_path).is_absolute() else Path(packet_path)
    if not path.is_file():
        return None
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(packet, dict):
        return None
    if packet.get("half_a_provenance"):
        prov = packet.get("half_a_provenance")
        return prov if isinstance(prov, dict) else None
    return build_half_a_provenance_from_packet(
        packet,
        vault_root=vault_root,
        project_id=str(packet.get("project_id") or ""),
    )


def validate_persona_attestation(
    attestation: Any,
    *,
    expected_persona_id: str,
    field_name: str = "persona_attestation",
) -> list[str]:
    """Structural gate — missing or invalid attestation fails harness validation."""
    violations: list[str] = []
    if not isinstance(attestation, dict):
        violations.append(f"{field_name}_missing")
        return violations
    pid = str(attestation.get("persona_id") or "")
    if not pid:
        violations.append(f"{field_name}_persona_id_missing")
    elif pid != expected_persona_id:
        violations.append(f"{field_name}_persona_id_mismatch:{pid}!={expected_persona_id}")
    wrote = attestation.get("wrote_paths")
    if not isinstance(wrote, list) or not wrote:
        violations.append(f"{field_name}_wrote_paths_empty")
    elif not all(isinstance(p, str) and p.strip() for p in wrote):
        violations.append(f"{field_name}_wrote_paths_invalid")
    if "persona_violations" not in attestation:
        violations.append(f"{field_name}_persona_violations_missing")
    elif not isinstance(attestation.get("persona_violations"), list):
        violations.append(f"{field_name}_persona_violations_not_list")
    return violations


def validate_lane_receipt_persona(lane_receipt: dict[str, Any], *, lane_id: str) -> list[str]:
    expected = f"half_b.lane.{lane_id}"
    att = lane_receipt.get("lane_persona_attestation")
    return validate_persona_attestation(
        att,
        expected_persona_id=expected,
        field_name="lane_persona_attestation",
    )


def validate_producer_review_persona(review: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    if "persona_drift_findings" not in review:
        violations.append("persona_drift_findings_missing")
    elif not isinstance(review.get("persona_drift_findings"), list):
        violations.append("persona_drift_findings_not_list")
    else:
        for i, item in enumerate(review.get("persona_drift_findings") or []):
            if not isinstance(item, dict):
                violations.append(f"persona_drift_findings[{i}]_not_object")
                continue
            for key in ("lane_id", "ux_bullet_id", "evidence_path"):
                if not str(item.get(key) or "").strip():
                    violations.append(f"persona_drift_findings[{i}]_{key}_missing")
    return violations


def synthetic_persona_attestation(
    persona_id: str,
    wrote_paths: list[str],
    *,
    persona_violations: list[str] | None = None,
) -> dict[str, Any]:
    """Harness fallback attestation when agent did not write one."""
    return {
        "persona_id": persona_id,
        "wrote_paths": [p for p in wrote_paths if p],
        "persona_violations": list(persona_violations or []),
        "synthetic": True,
    }


def is_overnight_orchestrator_run(orchestrator_run_id: str | None) -> bool:
    rid = str(orchestrator_run_id or "")
    return rid.startswith("ho-overnight-")


def allow_persona_harness_fallback(params: dict[str, Any]) -> bool:
    hints = params.get("planner_hints") if isinstance(params.get("planner_hints"), dict) else {}
    return bool(params.get("harness_fallback") or params.get("skip_pm_agent") or hints.get("allow_persona_harness_fallback"))


def should_force_pm_agent_invoke(
    *,
    orchestrator_run_id: str | None = None,
    params: dict[str, Any] | None = None,
) -> bool:
    """Overnight implementation track always invokes PM agent unless explicit packet override."""
    p = params or {}
    if allow_persona_harness_fallback(p):
        return False
    if is_overnight_orchestrator_run(orchestrator_run_id):
        return True
    if str(p.get("effective_track") or "").lower() == "implementation":
        return not bool(p.get("slice_producer_harness_fallback"))
    return True


def reject_synthetic_on_agent_path(attestation: Any, *, agent_path: bool) -> list[str]:
    if not agent_path or not isinstance(attestation, dict):
        return []
    if attestation.get("synthetic") is True:
        return ["persona_attestation_synthetic_on_agent_path"]
    return []


def validate_attestation_wrote_paths_in_repo(
    attestation: dict[str, Any],
    *,
    repo_prefix: str,
    zone_write: list[str] | None = None,
    field_name: str = "lane_persona_attestation",
) -> list[str]:
    """Tier A: lane wrote_paths should touch repo/zone when work occurred."""
    violations: list[str] = []
    wrote = attestation.get("wrote_paths") or []
    if not isinstance(wrote, list):
        return violations
    repo = repo_prefix.strip("/")
    zones = [str(z).strip("/") for z in (zone_write or []) if z]
    for p in wrote:
        if not isinstance(p, str):
            continue
        norm = p.strip("/")
        if repo and norm.startswith(repo):
            return violations
        for z in zones:
            if z and (norm.startswith(z) or f"/{z}/" in f"/{norm}/"):
                return violations
    if zones or repo:
        violations.append(f"{field_name}_wrote_paths_not_under_repo_or_zone")
    return violations


def evaluate_half_a_consume_gate(params: dict[str, Any]) -> tuple[bool, list[str]]:
    """Block queue consume when factory persona envelope present but attestation missing."""
    ph = params.get("persona_handoff")
    if not isinstance(ph, dict) or not ph.get("active_persona_id"):
        return True, []
    if not params.get("product_factory_run_id"):
        return True, []
    expected = str(ph.get("active_persona_id") or "")
    att = params.get("persona_attestation")
    violations = validate_persona_attestation(att, expected_persona_id=expected)
    return not violations, violations


def persona_validator_blocks_consume(params: dict[str, Any]) -> tuple[bool, list[str]]:
    """When validator reported persona drift codes at high severity, retain entry."""
    if not params.get("validator_persona_supplement") and not params.get("persona_handoff"):
        return False, []
    primary = str(params.get("validator_primary_code") or "")
    severity = str(params.get("validator_severity") or "").lower()
    rec = str(params.get("validator_recommended_action") or "").lower()
    persona_codes = {"persona_drift", "upstream_unattested_claim"}
    if primary in persona_codes and severity == "high":
        return True, [f"persona_validator_block:{primary}"]
    if primary in persona_codes and rec in {"hard_block", "block_destructive"}:
        return True, [f"persona_validator_block:{primary}"]
    return False, []


def provenance_sidecar_path(vault_root: Path, project_id: str, phase: str) -> Path:
    safe_phase = phase.replace("/", "_").replace(" ", "_")
    return (
        vault_root
        / ".technical"
        / "factory"
        / "provenance"
        / project_id
        / f"{safe_phase}.json"
    )


def save_half_a_provenance_sidecar(
    vault_root: Path,
    *,
    project_id: str,
    phase: str,
    persona_attestation: dict[str, Any],
    artifacts: dict[str, str] | None = None,
) -> Path:
    path = provenance_sidecar_path(vault_root, project_id, phase)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "project_id": project_id,
        "phase": phase,
        "persona_attestation": persona_attestation,
        "artifacts": artifacts or {},
    }
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    return path


def load_half_a_provenance_sidecars(vault_root: Path, project_id: str) -> dict[str, dict[str, Any]]:
    base = vault_root / ".technical" / "factory" / "provenance" / project_id
    if not base.is_dir():
        return {}
    out: dict[str, dict[str, Any]] = {}
    for p in sorted(base.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict):
            out[p.stem] = data
    return out


def build_half_a_provenance_from_packet(
    packet: dict[str, Any],
    *,
    vault_root: Path | None = None,
    project_id: str | None = None,
) -> dict[str, Any]:
    ux = packet.get("ux") if isinstance(packet.get("ux"), dict) else {}
    execution = packet.get("execution") if isinstance(packet.get("execution"), dict) else {}
    pin_paths = execution.get("pin_paths") or []
    exec_pin = pin_paths[0] if pin_paths else ""
    artifacts = {
        "catalog_row": str(packet.get("catalog_row_id") or ""),
        "l5_path": str(ux.get("l5_scope_path") or ""),
        "scope_path": str(ux.get("dispatch_scope_path") or ""),
        "execution_pin": str(exec_pin),
    }
    prov: dict[str, Any] = {
        "personas": ["half_a.catalog_ux_indexer", "half_a.execution_tech_lead"],
        "artifacts": artifacts,
        "unattested_artifacts": [],
    }
    pid = project_id or str(packet.get("project_id") or "")
    if vault_root is not None and pid:
        sidecars = load_half_a_provenance_sidecars(vault_root, pid)
        attested_keys: set[str] = set()
        for sc in sidecars.values():
            att = sc.get("persona_attestation") if isinstance(sc.get("persona_attestation"), dict) else {}
            if att.get("persona_id"):
                for k, v in (sc.get("artifacts") or {}).items():
                    if v:
                        attested_keys.add(str(k))
        for key, path in artifacts.items():
            if path and key not in attested_keys:
                prov["unattested_artifacts"].append({"artifact_key": key, "path": path})
        if sidecars:
            prov["sidecar_phases"] = sorted(sidecars.keys())
    return prov


def validate_provenance_for_compose(provenance: dict[str, Any] | None) -> list[str]:
    if not isinstance(provenance, dict):
        return ["half_a_provenance_missing"]
    unattested = provenance.get("unattested_artifacts") or []
    if isinstance(unattested, list) and unattested:
        return [f"unattested_artifact:{u.get('artifact_key')}" for u in unattested if isinstance(u, dict)]
    return []


def validate_producer_review_tier_b(
    review: dict[str, Any],
    *,
    lane_receipts: list[dict[str, Any]] | None = None,
) -> list[str]:
    """Semantic: UX bullets claimed require drift findings or explicit clear."""
    violations: list[str] = []
    if not review.get("ok"):
        return violations
    if review.get("persona_drift_clear"):
        return violations
    has_ux = False
    for lr in lane_receipts or []:
        if not isinstance(lr, dict):
            continue
        ux = lr.get("ux_bullet_ids") or []
        if isinstance(ux, list) and ux:
            has_ux = True
            break
    findings = review.get("persona_drift_findings")
    if has_ux and isinstance(findings, list) and not findings:
        violations.append("persona_drift_findings_empty_with_ux_bullets")
    return violations


def extract_lane_attestation_from_agent(agent_out: dict[str, Any]) -> dict[str, Any] | None:
    for key in ("lane_persona_attestation", "persona_attestation"):
        raw = agent_out.get(key)
        if isinstance(raw, dict) and raw.get("persona_id"):
            return raw
    return None


def merge_lane_persona_attestation(
    *,
    lane_id: str,
    agent_out: dict[str, Any] | None,
    changed_paths: list[str],
    receipt_rel_path: str,
) -> tuple[dict[str, Any], str]:
    """Prefer valid agent attestation; else harness synthetic."""
    expected = f"half_b.lane.{lane_id}"
    if agent_out:
        att = extract_lane_attestation_from_agent(agent_out)
        if att:
            v = validate_persona_attestation(att, expected_persona_id=expected, field_name="lane_persona_attestation")
            if not v:
                return att, "agent"
    paths = [p for p in changed_paths if p] or [receipt_rel_path]
    return synthetic_persona_attestation(expected, paths), "harness"
