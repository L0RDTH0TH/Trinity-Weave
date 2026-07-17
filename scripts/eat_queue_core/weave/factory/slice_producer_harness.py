"""Slice Producer harness — compose SIB/LMB/CDP from pillar_packet; structural PM review."""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..user_story.product_factory_state import (
    default_implementation_cell,
    load_product_factory,
    update_implementation_cell,
)
from ..user_story.work_order_translate import assemble_pillar_packet
from ..persona_handoff import (
    reject_synthetic_on_agent_path,
    synthetic_persona_attestation,
    validate_lane_receipt_persona,
    validate_persona_attestation,
    validate_producer_review_persona,
    validate_provenance_for_compose,
    validate_producer_review_tier_b,
)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def technical_slice_dir(vault_root: Path, slice_id: str) -> Path:
    return vault_root / ".technical" / "factory" / "slice-briefs" / slice_id


def drb_slice_dir(vault_root: Path, project_id: str, slice_id: str) -> Path:
    return vault_root / "1-Projects" / project_id / "Factory-DRB" / "slice-briefs" / slice_id


def _extract_ux_bullets(text: str, max_bullets: int = 8) -> list[dict[str, str]]:
    bullets: list[dict[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        m = re.match(r"^[-*]\s+(.+)$", stripped)
        if m:
            bullets.append({"id": f"UX-{len(bullets) + 1}", "text": m.group(1).strip()})
        elif re.match(r"^\d+\.\s+", stripped):
            bullets.append({"id": f"UX-{len(bullets) + 1}", "text": re.sub(r"^\d+\.\s+", "", stripped)})
        if len(bullets) >= max_bullets:
            break
    if not bullets and text.strip():
        bullets.append({"id": "UX-1", "text": text.strip()[:400]})
    return bullets


def _assign_bullets_to_lanes(
    lane_ids: list[str],
    bullets: list[dict[str, str]],
) -> dict[str, list[str]]:
    if not lane_ids:
        return {}
    out: dict[str, list[str]] = {lid: [] for lid in lane_ids}
    for i, b in enumerate(bullets):
        lid = lane_ids[i % len(lane_ids)]
        out[lid].append(b["id"])
    return out


def compose_slice_briefs_from_packet(
    vault_root: Path,
    packet: dict[str, Any],
    *,
    producer_run_id: str,
) -> dict[str, Any]:
    """Deterministic harness compose — writes SIB, LMBs, CDP, producer-receipt."""
    vault_root = vault_root.resolve()
    project_id = str(packet.get("project_id") or "")
    slice_id = str(packet.get("slice_id") or "")
    row_id = str(packet.get("catalog_row_id") or "")
    dispatch_depth = int(packet.get("dispatch_depth") or 0)
    target_depth = int(packet.get("target_depth") or 0)
    lane_ids = [str(x) for x in (packet.get("lane_roster") or []) if x]

    ux = packet.get("ux") if isinstance(packet.get("ux"), dict) else {}
    conceptual = packet.get("conceptual") if isinstance(packet.get("conceptual"), dict) else {}
    execution = packet.get("execution") if isinstance(packet.get("execution"), dict) else {}

    dispatch_body = str(ux.get("dispatch_body") or "")
    l5_body = str(ux.get("l5_body") or "")
    bullets = _extract_ux_bullets(dispatch_body or l5_body)
    bullet_assignments = _assign_bullets_to_lanes(lane_ids, bullets)

    drb_dir = drb_slice_dir(vault_root, project_id, slice_id)
    missions_dir = drb_dir / "missions"
    missions_dir.mkdir(parents=True, exist_ok=True)
    tech_dir = technical_slice_dir(vault_root, slice_id)
    tech_dir.mkdir(parents=True, exist_ok=True)

    sib_rel = f"1-Projects/{project_id}/Factory-DRB/slice-briefs/{slice_id}.md"
    sib_path = vault_root / sib_rel
    sib_path.parent.mkdir(parents=True, exist_ok=True)

    bullet_block = "\n".join(f"- **{b['id']}:** {b['text']}" for b in bullets)
    sib_body = (
        f"---\n"
        f"slice_id: {slice_id}\n"
        f"catalog_row_id: {row_id}\n"
        f"dispatch_depth: {dispatch_depth}\n"
        f"target_depth: {target_depth}\n"
        f"producer_run_id: {producer_run_id}\n"
        f"pillar_packet_hash: {packet.get('pillar_packet_hash', '')}\n"
        f"composed_at: {_utc_iso()}\n"
        f"---\n\n"
        f"# Slice Implementation Brief — {packet.get('row_label', row_id)}\n\n"
        f"## 1. Product goal (UX)\n\n"
        f"**North star (L5):**\n{l5_body[:2000] or '(see scope files)'}\n\n"
        f"**Dispatch depth L{dispatch_depth} bar:**\n{dispatch_body[:2000] or '(see scope files)'}\n\n"
        f"### UX bullets\n{bullet_block or '- **UX-1:** Deliver slice at depth ' + str(dispatch_depth)}\n\n"
        f"## 2. Shape lock (Conceptual)\n\n"
        f"{conceptual.get('body', '(no conceptual pin resolved)')[:2500]}\n\n"
        f"## 3. Realization (Execution)\n\n"
        f"{execution.get('acceptance_excerpt', '(no execution excerpt)')[:2500]}\n\n"
        f"## 4. Cell roster\n\n"
        + "\n".join(f"- `{lid}` — crew for {packet.get('dimension', 'slice')}" for lid in lane_ids)
        + "\n"
    )
    sib_path.write_text(sib_body, encoding="utf-8")

    mission_paths: list[str] = []
    lane_missions: dict[str, Any] = {}
    for lid in lane_ids:
        owned = bullet_assignments.get(lid) or []
        owned_lines = "\n".join(
            f"- **{bid}:** {next((b['text'] for b in bullets if b['id'] == bid), '')}"
            for bid in owned
        )
        mission_rel = f"1-Projects/{project_id}/Factory-DRB/slice-briefs/{slice_id}/missions/{lid}.md"
        mission_paths.append(mission_rel)
        mission_body = (
            f"---\n"
            f"lane_id: {lid}\n"
            f"slice_id: {slice_id}\n"
            f"producer_run_id: {producer_run_id}\n"
            f"ux_bullet_ids: {json.dumps(owned)}\n"
            f"---\n\n"
            f"# Lane Mission — {lid}\n\n"
            f"## Mission\n"
            f"Deliver your lane contribution for `{row_id}` at depth {dispatch_depth}.\n\n"
            f"## UX bullets you own\n{owned_lines or '- (shared slice goal)'}\n\n"
            f"## Shape context\nSee SIB §2 — do not relitigate conceptual lock.\n\n"
            f"## Realization notes\nSee SIB §3 — crosswalk acceptance to your UX bullets.\n\n"
            f"## Done when\n"
            f"- Build passes\n"
            f"- Lane receipt cites UX bullet ids satisfied\n"
        )
        (vault_root / mission_rel).write_text(mission_body, encoding="utf-8")
        lane_missions[lid] = {
            "mission_path": mission_rel,
            "ux_bullet_ids": owned,
            "blocked_by": [],
        }

    cdp_rel = f"1-Projects/{project_id}/Factory-DRB/slice-briefs/{slice_id}/cell_dispatch_plan.json"
    cdp = {
        "schema_version": 1,
        "slice_id": slice_id,
        "producer_run_id": producer_run_id,
        "sib_path": sib_rel,
        "waves": [
            {
                "wave": 1,
                "parallel": True,
                "lanes": lane_ids,
            }
        ],
        "lane_missions": lane_missions,
    }
    cdp_path = vault_root / cdp_rel
    cdp_path.parent.mkdir(parents=True, exist_ok=True)
    cdp_path.write_text(json.dumps(cdp, indent=2) + "\n", encoding="utf-8")

    receipt = {
        "ok": True,
        "violations": [],
        "escalate_to_architect": False,
        "producer_run_id": producer_run_id,
        "sib_path": sib_rel,
        "cdp_path": cdp_rel,
        "mission_paths": mission_paths,
        "composed_at": _utc_iso(),
        "persona_attestation": synthetic_persona_attestation(
            "half_b.slice_producer_pm",
            [sib_rel, cdp_rel, *mission_paths],
        ),
    }
    receipt_path = tech_dir / "producer-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    packet_path = tech_dir / "pillar_packet.json"
    packet_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")

    return {
        "ok": True,
        "producer_run_id": producer_run_id,
        "sib_path": sib_rel,
        "cdp_path": cdp_rel,
        "mission_paths": mission_paths,
        "receipt_path": str(receipt_path.relative_to(vault_root)),
        "pillar_packet_path": str(packet_path.relative_to(vault_root)),
    }


def validate_producer_receipt(
    vault_root: Path,
    receipt: dict[str, Any],
    *,
    agent_path: bool = False,
) -> tuple[bool, list[str]]:
    violations: list[str] = []
    if not receipt.get("ok"):
        violations.append("receipt_not_ok")
    sib_rel = str(receipt.get("sib_path") or "")
    if sib_rel and not (vault_root / sib_rel).is_file():
        violations.append(f"sib_missing:{sib_rel}")
    cdp_rel = str(receipt.get("cdp_path") or "")
    if cdp_rel and not (vault_root / cdp_rel).is_file():
        violations.append(f"cdp_missing:{cdp_rel}")
    for mp in receipt.get("mission_paths") or []:
        if mp and not (vault_root / str(mp)).is_file():
            violations.append(f"mission_missing:{mp}")
    if not receipt.get("mission_paths"):
        violations.append("no_lane_missions")
    violations.extend(
        validate_persona_attestation(
            receipt.get("persona_attestation"),
            expected_persona_id="half_b.slice_producer_pm",
        )
    )
    violations.extend(
        reject_synthetic_on_agent_path(receipt.get("persona_attestation"), agent_path=agent_path)
    )
    prov = receipt.get("half_a_provenance")
    if isinstance(prov, dict):
        violations.extend(validate_provenance_for_compose(prov))
    return not violations, violations


def validate_producer_review(
    vault_root: Path,
    review: dict[str, Any],
    *,
    lane_receipts: list[dict[str, Any]] | None = None,
) -> tuple[bool, list[str]]:
    violations: list[str] = []
    if not review.get("ok") and review.get("verdict") not in ("rework", "blocked"):
        violations.append("review_not_ok")
    violations.extend(validate_producer_review_persona(review))
    violations.extend(validate_producer_review_tier_b(review, lane_receipts=lane_receipts))
    return not violations, violations


def load_producer_receipt(vault_root: Path, slice_id: str) -> dict[str, Any] | None:
    path = technical_slice_dir(vault_root, slice_id) / "producer-receipt.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def load_cell_dispatch_plan(vault_root: Path, cdp_rel: str) -> dict[str, Any] | None:
    path = vault_root / cdp_rel
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def run_slice_producer_compose(
    vault_root: Path,
    *,
    project_id: str,
    run_id: str,
    active_slice: dict[str, Any] | None = None,
    force: bool = False,
) -> dict[str, Any]:
    """Assemble pillar_packet and compose SIB/LMB/CDP (harness v1)."""
    vault_root = vault_root.resolve()
    producer_run_id = f"sp-{run_id[:8]}-{uuid.uuid4().hex[:6]}"
    packet = assemble_pillar_packet(
        vault_root,
        project_id=project_id,
        producer_run_id=producer_run_id,
        active_slice=active_slice,
    )
    if packet is None:
        return {"ok": False, "error": "assemble_pillar_packet_failed"}

    slice_id = str(packet.get("slice_id") or "")
    existing = load_producer_receipt(vault_root, slice_id)
    if existing and existing.get("ok") and not force:
        ok, violations = validate_producer_receipt(vault_root, existing)
        if ok:
            update_implementation_cell(
                vault_root,
                project_id,
                {
                    "factory_beat_id": slice_id,
                    "phase": "composed",
                    "producer_run_id": existing.get("producer_run_id", producer_run_id),
                    "sib_path": existing.get("sib_path", ""),
                    "cdp_path": existing.get("cdp_path", ""),
                    "pm_review_status": "idle",
                },
            )
            return {"ok": True, "skipped": True, "reused": True, **existing}

    composed = compose_slice_briefs_from_packet(
        vault_root, packet, producer_run_id=producer_run_id
    )
    receipt_path = technical_slice_dir(vault_root, slice_id) / "producer-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    ok, violations = validate_producer_receipt(vault_root, receipt)
    if not ok:
        receipt["ok"] = False
        receipt["violations"] = violations
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        return {"ok": False, "violations": violations, "slice_id": slice_id}

    cell = default_implementation_cell(slice_id=slice_id, producer_run_id=producer_run_id)
    cell.update(
        {
            "phase": "composed",
            "sib_path": composed["sib_path"],
            "cdp_path": composed["cdp_path"],
        }
    )
    pf = load_product_factory(vault_root, project_id)
    save_pf = {**pf, "implementation_cell": cell}
    from ..user_story.product_factory_state import save_product_factory

    save_product_factory(vault_root, project_id, save_pf)

    try:
        from ..user_story.implementation_artifact_ledger import record_implementation_artifact

        for rel_key, event_type in (
            ("sib_path", "sib_compose"),
            ("cdp_path", "cdp_compose"),
        ):
            rel = str(composed.get(rel_key) or "")
            if rel:
                record_implementation_artifact(
                    vault_root,
                    project_id,
                    artifact_path=rel.lstrip("/"),
                    event_type=event_type,
                    slice_id=slice_id,
                    product_factory_run_id=producer_run_id,
                )
        record_implementation_artifact(
            vault_root,
            project_id,
            artifact_path=str(receipt_path.relative_to(vault_root.resolve())),
            event_type="producer_receipt",
            slice_id=slice_id,
            product_factory_run_id=producer_run_id,
        )
    except (OSError, ValueError):
        pass

    return {"ok": True, "slice_id": slice_id, **composed, "receipt": receipt}


def run_slice_producer_review(
    vault_root: Path,
    *,
    project_id: str,
    slice_id: str,
    queue_lane: str,
    current_wave: int = 1,
) -> dict[str, Any]:
    """Structural PM review v1 — lane receipts + wave completeness."""
    vault_root = vault_root.resolve()
    receipt = load_producer_receipt(vault_root, slice_id)
    if not receipt or not receipt.get("ok"):
        return {
            "ok": False,
            "verdict": "blocked",
            "failure_class": "system_invariant",
            "violations": ["producer_receipt_missing"],
        }

    cdp = load_cell_dispatch_plan(vault_root, str(receipt.get("cdp_path") or ""))
    if not cdp:
        return {
            "ok": False,
            "verdict": "blocked",
            "failure_class": "system_invariant",
            "violations": ["cdp_missing"],
        }

    waves = cdp.get("waves") or []
    wave_def = next(
        (w for w in waves if isinstance(w, dict) and int(w.get("wave") or 0) == current_wave),
        None,
    )
    if not isinstance(wave_def, dict):
        return {
            "ok": False,
            "verdict": "blocked",
            "failure_class": "system_invariant",
            "violations": [f"wave_missing:{current_wave}"],
        }

    wave_lanes = [str(x) for x in (wave_def.get("lanes") or []) if x]
    if not wave_lanes:
        return {
            "ok": False,
            "verdict": "blocked",
            "failure_class": "system_invariant",
            "violations": ["wave_lanes_empty"],
        }

    violations: list[str] = []
    persona_drift_findings: list[dict[str, str]] = []
    lane_receipt_objs: list[dict[str, Any]] = []
    receipts_dir = technical_slice_dir(vault_root, slice_id) / "receipts"
    for lid in wave_lanes:
        lane_receipt_path = receipts_dir / f"{lid}.json"
        if not lane_receipt_path.is_file():
            violations.append(f"lane_receipt_missing:{lid}")
            persona_drift_findings.append(
                {
                    "lane_id": lid,
                    "ux_bullet_id": "n/a",
                    "evidence_path": f"lane_receipt_missing:{lid}",
                }
            )
            continue
        lr = json.loads(lane_receipt_path.read_text(encoding="utf-8"))
        if isinstance(lr, dict):
            lane_receipt_objs.append(lr)
        if not lr.get("ok", True):
            violations.append(f"lane_receipt_not_ok:{lid}")
            persona_drift_findings.append(
                {
                    "lane_id": lid,
                    "ux_bullet_id": "n/a",
                    "evidence_path": f"lane_receipt_not_ok:{lid}",
                }
            )
        lane_persona_v = validate_lane_receipt_persona(lr, lane_id=lid)
        if lane_persona_v:
            violations.extend(lane_persona_v)
            persona_drift_findings.append(
                {
                    "lane_id": lid,
                    "ux_bullet_id": "n/a",
                    "evidence_path": ";".join(lane_persona_v),
                }
            )

    if violations:
        verdict = "rework"
        failure_class = "implementation_rework"
        review_ok = False
    else:
        verdict = "pass"
        failure_class = None
        review_ok = True

    last_wave = max(int(w.get("wave") or 0) for w in waves if isinstance(w, dict)) if waves else 1
    more_waves = current_wave < last_wave

    review_doc = {
        "ok": review_ok,
        "verdict": verdict,
        "failure_class": failure_class,
        "slice_id": slice_id,
        "current_wave": current_wave,
        "more_waves": more_waves,
        "violations": violations,
        "persona_drift_findings": persona_drift_findings,
        "reviewed_at": _utc_iso(),
    }
    review_path = technical_slice_dir(vault_root, slice_id) / "producer-review.json"
    review_path.write_text(json.dumps(review_doc, indent=2) + "\n", encoding="utf-8")

    struct_ok, struct_violations = validate_producer_review(
        vault_root, review_doc, lane_receipts=lane_receipt_objs
    )
    if not struct_ok:
        review_doc["ok"] = False
        review_doc["violations"] = list(dict.fromkeys(violations + struct_violations))
        review_path.write_text(json.dumps(review_doc, indent=2) + "\n", encoding="utf-8")
        return {
            "ok": False,
            "verdict": "blocked",
            "failure_class": "system_invariant",
            "violations": struct_violations,
        }

    if review_ok:
        phase = "wave_complete" if more_waves else "cell_complete"
        update_implementation_cell(
            vault_root,
            project_id,
            {
                "phase": phase,
                "pm_review_status": "pass",
                "current_wave": current_wave,
            },
        )
    else:
        update_implementation_cell(
            vault_root,
            project_id,
            {"phase": "rework", "pm_review_status": "rework"},
        )

    return review_doc


def sib_content_hash(vault_root: Path, sib_rel: str) -> str:
    path = vault_root / sib_rel
    if not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
