"""Phase 16 — honesty anchor claim-tier matrix proofs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .trinity_card_paths import load_trinity_card

MATRIX_ARTIFACT = Path(".technical/weave/validation/honesty-anchor-matrix.json")

CLAIM_TIERS = ("structural", "inferred", "narrative")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _divergence_codes(payload: dict[str, Any]) -> list[str]:
    raw = payload.get("divergence_codes")
    if isinstance(raw, list):
        return [str(x) for x in raw]
    trace = payload.get("trace")
    if isinstance(trace, dict):
        inner = trace.get("divergence_codes")
        if isinstance(inner, list):
            return [str(x) for x in inner]
    return []


def _has_structural_proof(payload: dict[str, Any]) -> bool:
    if payload.get("structural_proof") is True:
        return True
    if payload.get("provisional_success"):
        return bool(_divergence_codes(payload))
    conduct_ok = payload.get("conduct_ok")
    if conduct_ok is False:
        return False
    if payload.get("pass_gate_ok") and conduct_ok is True:
        counts = payload.get("counts") or payload.get("summary")
        report = payload.get("report_path") or payload.get("artifact_path")
        return bool(counts) and bool(report)
    return False


def classify_claim(payload: dict[str, Any]) -> str:
    """Return claim tier: structural | inferred | narrative."""
    if _has_structural_proof(payload):
        return "structural"
    if payload.get("uncertainty_block") or payload.get("claim_class") == "inferred":
        return "inferred"
    return "narrative"


def evaluate_claim(payload: dict[str, Any]) -> tuple[bool, list[str], str]:
    """Apply maintenance_honesty_anchor rules to a receipt/outcome payload."""
    errors: list[str] = []
    tier = classify_claim(payload)

    claims_success = bool(payload.get("claimed_success"))
    if payload.get("pass_gate_ok"):
        if payload.get("conduct_ok") is False:
            claims_success = False
        else:
            claims_success = True
    if payload.get("status") == "success" and payload.get("conduct_ok") is not False:
        if not payload.get("provisional_success"):
            claims_success = claims_success or payload.get("status") == "success"

    if claims_success and tier == "narrative":
        errors.append("narrative cannot claim success/pass_gate without structural proof")

    if payload.get("provisional_success") and not _divergence_codes(payload):
        errors.append("provisional_success requires divergence_codes in trace")

    if payload.get("mid_band") and tier == "inferred" and not payload.get("uncertainty_block"):
        errors.append("mid-band inferred claim requires uncertainty_block")

    if payload.get("import_only_smoke") and payload.get("claimed_structural"):
        errors.append("import-only smoke cannot claim structural conduct")

    if payload.get("merge_narrative_into_guidance"):
        errors.append("forbidden: merge narrative into user_guidance as human-authored")

    ok = len(errors) == 0
    return ok, errors, tier


def scenario_fixtures() -> list[dict[str, Any]]:
    """Built-in matrix scenarios aligned with maintenance_honesty_anchor meta."""
    return [
        {
            "id": "structural_pass_gate",
            "description": "pass_gate green with conduct counts and report path",
            "payload": {
                "pass_gate_ok": True,
                "conduct_ok": True,
                "counts": {"green": 121, "red": 0},
                "report_path": ".technical/weave/receipts/trinity-weave-self-wrap.json",
            },
            "expect_ok": True,
            "expect_tier": "structural",
        },
        {
            "id": "provisional_success_with_divergence",
            "description": "provisional_success allowed when divergence_codes present",
            "payload": {
                "provisional_success": True,
                "status": "success",
                "divergence_codes": ["missing_option_evaluation"],
            },
            "expect_ok": True,
            "expect_tier": "structural",
        },
        {
            "id": "narrative_success_fail",
            "description": "narrative-only success claim must fail",
            "payload": {
                "claimed_success": True,
                "status": "success",
                "message": "All good!",
            },
            "expect_ok": False,
            "expect_tier": "narrative",
        },
        {
            "id": "provisional_without_divergence_fail",
            "description": "provisional_success without divergence_codes fails",
            "payload": {
                "provisional_success": True,
                "status": "success",
            },
            "expect_ok": False,
            "expect_tier": "narrative",
        },
        {
            "id": "inferred_mid_band_ok",
            "description": "mid-band inferred with uncertainty block passes",
            "payload": {
                "mid_band": True,
                "claim_class": "inferred",
                "uncertainty_block": "Would change if conduct report missing.",
            },
            "expect_ok": True,
            "expect_tier": "inferred",
        },
        {
            "id": "import_smoke_structural_fail",
            "description": "import-only smoke cannot claim structural",
            "payload": {
                "import_only_smoke": True,
                "claimed_structural": True,
                "conduct_ok": True,
            },
            "expect_ok": False,
            "expect_tier": "narrative",
        },
        {
            "id": "conduct_fail_no_structural",
            "description": "conduct_ok false blocks structural tier",
            "payload": {
                "pass_gate_ok": True,
                "conduct_ok": False,
                "counts": {"green": 0},
                "report_path": "x.json",
            },
            "expect_ok": True,
            "expect_tier": "narrative",
        },
    ]


def load_meta_honesty_touch(vault_root: Path) -> dict[str, Any] | None:
    try:
        card = load_trinity_card(vault_root, "maintenance_honesty_anchor", prefer="locked")
    except (OSError, ValueError):
        return None
    touch = card.get("touch")
    return touch if isinstance(touch, dict) else None


def run_honesty_anchor_proofs(
    vault_root: Path,
    *,
    dry_run: bool = False,
    write_artifact: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)

    if not getattr(cfg, "honesty_anchor_enabled", True):
        return {"ok": True, "skipped": True, "reason": "honesty_anchor_disabled"}

    meta_touch = load_meta_honesty_touch(vault_root)
    scenarios_out: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []

    for fix in scenario_fixtures():
        ok, errors, tier = evaluate_claim(fix["payload"])
        row = {
            "id": fix["id"],
            "description": fix["description"],
            "expect_ok": fix["expect_ok"],
            "expect_tier": fix["expect_tier"],
            "actual_ok": ok,
            "actual_tier": tier,
            "ok": ok == fix["expect_ok"] and tier == fix["expect_tier"],
            "errors": errors,
        }
        scenarios_out.append(row)
        if not row["ok"]:
            mismatches.append(row)

    green = sum(1 for s in scenarios_out if s.get("ok"))
    red = len(scenarios_out) - green

    report: dict[str, Any] = {
        "ok": red == 0,
        "dry_run": dry_run,
        "generated_at": _now_iso(),
        "claim_tiers": list(CLAIM_TIERS),
        "meta_card_readable": meta_touch is not None,
        "meta_touch_claim_tiers": (meta_touch or {}).get("claim_tiers"),
        "meta_touch_honesty_tiers": (meta_touch or {}).get("honesty_tiers"),
        "scenarios": scenarios_out,
        "summary": {"total": len(scenarios_out), "green": green, "red": red},
        "artifact_path": str(MATRIX_ARTIFACT),
    }

    if mismatches:
        report["mismatches"] = mismatches
        report["ok"] = False

    if not dry_run and write_artifact:
        out_path = vault_root / MATRIX_ARTIFACT
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["written"] = True

    return report
