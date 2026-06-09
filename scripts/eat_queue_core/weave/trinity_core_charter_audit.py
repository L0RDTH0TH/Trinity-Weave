"""Alternative A — maintenance core charter audit vs finalized MVL meta (read-only)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .trinity_align import check
from .trinity_card import get_rules, get_touch
from .trinity_card_paths import load_trinity_card
from .trinity_dual_lock import load_maintenance_core_policy
from .trinity_lens_informed_align import verify_meta_corpus_harness_wiring
from .trinity_meta_corpus import DEFAULT_META_GENERATION_LOAD_IDS
from .trinity_mvl_lens import get_lens_contract, probe_mvl_lens

ARTIFACT_DIR = Path(".technical/weave/validation")

# Finalized meta set (post scorched-earth / Phase 11+13+16) — not starting-era subset.
FINALIZED_META_IDS: tuple[str, ...] = DEFAULT_META_GENERATION_LOAD_IDS + (
    "host_execution_safety_contract",
    "conceptual_style_guide",
    "trinity_card_authoring",
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _card_lock_kind(card: dict[str, Any]) -> str:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    return str(meta.get("lock_kind") or "").strip()


def _norm_audit_rel(rel: str) -> str:
    s = str(rel).strip().replace("\\", "/")
    if s.startswith("./"):
        return s[2:]
    return s


def _path_exists(vault_root: Path, rel: str) -> bool:
    p = vault_root / _norm_audit_rel(rel)
    return p.is_file() or p.is_dir()


def _is_meta_doctrine_card(trinity_id: str, card: dict[str, Any]) -> bool:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    if str(meta.get("card_kind") or "").strip().lower() == "meta":
        return True
    return trinity_id in FINALIZED_META_IDS


def _audit_one_core_card(vault_root: Path, trinity_id: str) -> dict[str, Any]:
    tid = str(trinity_id).strip()
    rec: dict[str, Any] = {
        "trinity_id": tid,
        "issues": [],
        "gaps": [],
        "ok": True,
        "is_meta_doctrine": False,
    }
    try:
        card = load_trinity_card(vault_root, tid, prefer="locked")
    except (OSError, ValueError, FileNotFoundError) as e:
        return {
            "trinity_id": tid,
            "ok": False,
            "issues": [f"load_failed:{e}"],
            "severity": "high",
        }

    is_meta = _is_meta_doctrine_card(tid, card)
    rec["is_meta_doctrine"] = is_meta

    lock = _card_lock_kind(card)
    if lock not in ("maintenance_core", "conceptual_spine", "usage_proven", ""):
        rec["issues"].append(f"unexpected_lock_kind:{lock or 'missing'}")
    if lock == "usage_proven":
        rec["gaps"].append("usage_proven_on_core_registry_id_review")

    run_proofs = not is_meta
    align = check(vault_root, tid, run_behavior_proofs=run_proofs)
    rec["align_ok"] = align.ok
    rec["stale_touch"] = align.stale_touch
    rec["disconnects"] = [d.kind for d in align.disconnects]
    if not align.ok and not is_meta:
        rec["ok"] = False
        rec["issues"].append("align_not_ok")
    if align.stale_touch:
        rec["gaps"].append("stale_touch")
    for dk in rec["disconnects"]:
        if is_meta and dk in ("precedence_collapse", "touch_conceptual_gap"):
            rec["gaps"].append(f"disconnect:{dk}")
        elif not is_meta:
            rec["issues"].append(f"disconnect:{dk}")

    touch = get_touch(card)
    rules = get_rules(card)
    missing_paths: list[str] = []
    legacy_host_paths: list[str] = []
    for raw in touch.get("primary_paths") or []:
        rel = str(raw).strip()
        if not rel:
            continue
        if not _path_exists(vault_root, rel):
            missing_paths.append(rel)
            if rel.startswith(".cursor/rules/") and "host-weld-bridge" not in rel:
                legacy_host_paths.append(rel)
    if legacy_host_paths:
        rec["gaps"].append("legacy_host_path_stale")
        rec["legacy_host_paths"] = legacy_host_paths[:8]
    elif missing_paths and not is_meta:
        rec["ok"] = False
        rec["missing_primary_paths"] = missing_paths[:8]
        rec["issues"].append("missing_primary_paths")
    elif missing_paths and is_meta:
        rec["gaps"].append("missing_primary_paths")
        rec["missing_primary_paths"] = missing_paths[:8]

    if is_meta:
        lens = get_lens_contract(vault_root)
        if tid not in set(lens.meta_prepend_order):
            rec["gaps"].append("meta_not_in_lens_prepend_order")
        if rules.get("meta_lens_force_align"):
            rec["gaps"].append("meta_lens_force_align_on_locked_meta_review")
    else:
        if rules.get("meta_lens_forbidden_code_filtered"):
            rec["gaps"].append("regen_mint_artifact_on_core_review")

    if rec["issues"]:
        rec["severity"] = "high"
    elif rec["gaps"]:
        rec["severity"] = "medium"
    else:
        rec["severity"] = "none"
    return rec


def _reconcile_core_touch_after_metrics_churn(
    vault_root: Path,
    core_ids: list[str],
) -> list[str]:
    """Re-hash maintenance core *component* cards when metrics.jsonl churn stale-only touch."""
    from .config import load_trinity_config
    from .trinity_align import _sync_stored_touch_hash, check

    cfg = load_trinity_config(vault_root)
    reconciled: list[str] = []
    for tid in core_ids:
        try:
            card = load_trinity_card(vault_root, tid, prefer="locked")
        except (OSError, ValueError, FileNotFoundError):
            continue
        if _is_meta_doctrine_card(tid, card):
            continue
        result = check(vault_root, tid, run_behavior_proofs=False)
        if result.stale_touch and not result.disconnects:
            _sync_stored_touch_hash(vault_root, tid, cfg)
            reconciled.append(tid)
    return reconciled


def run_core_charter_audit(
    vault_root: Path,
    *,
    write_artifact: bool = True,
) -> dict[str, Any]:
    """Read-only audit of maintenance_core registry vs finalized meta wiring."""
    vault_root = vault_root.resolve()
    started = _now_iso()
    policy = load_maintenance_core_policy(vault_root)
    core_ids = sorted(policy.ids)

    touch_pre = _reconcile_core_touch_after_metrics_churn(vault_root, core_ids)

    mvl_probe = probe_mvl_lens(vault_root)
    wiring = verify_meta_corpus_harness_wiring(vault_root)
    lens = get_lens_contract(vault_root)
    prepend = list(lens.meta_prepend_order)
    missing_finalized = [mid for mid in FINALIZED_META_IDS if mid not in prepend]

    per_card = [_audit_one_core_card(vault_root, tid) for tid in core_ids]
    failing = [r for r in per_card if not r.get("ok")]
    gaps = [r for r in per_card if r.get("gaps")]
    legacy_host = [
        r["trinity_id"]
        for r in per_card
        if "legacy_host_path_stale" in (r.get("gaps") or [])
    ]

    report: dict[str, Any] = {
        "ok": len(failing) == 0 and wiring.get("ok") and mvl_probe.get("ok"),
        "charter_aligned": len(failing) == 0 and not missing_finalized and not legacy_host,
        "phase": "alternative_a_core_charter_audit",
        "started_at": started,
        "completed_at": _now_iso(),
        "maintenance_core_count": len(core_ids),
        "finalized_meta_ids": list(FINALIZED_META_IDS),
        "mvl_probe": {
            "ok": mvl_probe.get("ok"),
            "lens_source": mvl_probe.get("lens_source"),
            "missing_meta_cards": mvl_probe.get("missing_meta_cards"),
        },
        "meta_wiring": wiring,
        "lens_prepend_missing_finalized": missing_finalized,
        "per_card": per_card,
        "failing_ids": [r["trinity_id"] for r in failing],
        "gap_ids": [r["trinity_id"] for r in gaps],
        "legacy_host_path_ids": legacy_host,
        "next_steps": _audit_next_steps(failing, gaps, missing_finalized, legacy_host),
    }

    if write_artifact:
        out_dir = vault_root / ARTIFACT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)
        artifact = out_dir / f"core-charter-audit-{_stamp()}.json"
        artifact.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["artifact_path"] = str(artifact.relative_to(vault_root))

    from .governance import append_metric_row

    append_metric_row(
        vault_root,
        {
            "metric_type": "core_charter_audit",
            "ok": report.get("ok"),
            "failing_count": len(failing),
            "gap_count": len(gaps),
        },
    )
    touch_post = _reconcile_core_touch_after_metrics_churn(vault_root, core_ids)
    if touch_pre or touch_post:
        report["touch_hash_reconciled"] = {
            "pre_audit": touch_pre,
            "post_metrics": touch_post,
        }
    return report


def _audit_next_steps(
    failing: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    missing_prepend: list[str],
    legacy_host: list[str],
) -> list[str]:
    steps: list[str] = []
    if legacy_host:
        steps.append(
            "Operator --operator-mutation: refresh meta Touch paths from archived host-weld "
            "→ host-weld/live/ + 3-Resources docs (starting-era .cursor/rules paths are stale)."
        )
        steps.append(f"Legacy host paths: {', '.join(legacy_host[:8])}")
    if missing_prepend:
        steps.append(
            "Update trinity_prompt_context prepend order for finalized meta: "
            + ", ".join(missing_prepend)
        )
    if failing:
        steps.append(
            "Operator review failing maintenance components with --operator-mutation."
        )
        steps.append(f"Failing: {', '.join(r['trinity_id'] for r in failing[:12])}")
    if gaps and not legacy_host:
        steps.append(f"Charter gaps (medium): {', '.join(r['trinity_id'] for r in gaps[:12])}")
    if not failing:
        steps.append("Run type2_verify (no regen) to confirm steady-state green.")
    return steps
