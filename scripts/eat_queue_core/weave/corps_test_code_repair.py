"""Phase 10f — test-code conduct surgery (bounded second phase after 10d card YAML).

North star enforcement: self-wrap does not stop at card YAML when behavior proofs
still fail. This phase runs stale-touch curation, re-runs 10d wiring, and records
remaining proof failures for LLM (when enabled) or operator escalation.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .corps_conduct_repair import repair_conduct_card
from .corps_repair_audit import audit_card_repair
from .governance import append_metric_row
from .trinity_align import apply_trinity_align_gate, check
from .trinity_behavior_proof import run_card_behavior_proofs
from .trinity_card_paths import load_trinity_card, write_trinity_card
from .trinity_catchup_sweep import curate_stale_non_core
from .trinity_dual_lock import corps_repair_skip_reason
from .trinity_spine_guard import respects_locked_spine


def _failure_class(detail: str) -> str:
    d = (detail or "").lower()
    if "timeout" in d:
        return "timeout"
    if "not found" in d or "behavior_signal test not found" in d:
        return "not_found"
    if "fail:" in d or "assertion" in d:
        return "assert_fail"
    return "unknown"


def repair_test_code_card(
    vault_root: Path,
    trinity_id: str,
    *,
    nerve_row: dict[str, Any] | None = None,
    dry_run: bool = False,
    allow_llm: bool = False,
    allow_conduct_apply: bool = True,
) -> dict[str, Any]:
    """Bounded test-code surgery for one conduct-red card."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    rec: dict[str, Any] = {
        "trinity_id": tid,
        "phase": "test_code",
        "applied": [],
        "changed": False,
        "proofs_ok": None,
        "manual_required": False,
    }

    skip = corps_repair_skip_reason(vault_root, tid)
    if skip:
        rec["skipped"] = skip
        return rec

    guard = respects_locked_spine(vault_root, tid)
    if not guard.ok:
        rec["skipped"] = "respects_locked_spine"
        return rec

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError) as e:
        rec["error"] = str(e)
        return rec

    working = copy.deepcopy(card)
    align_pre = check(vault_root, tid, run_behavior_proofs=False)
    if align_pre.stale_touch and not dry_run:
        crec = curate_stale_non_core(vault_root, tid, align_pre, dry_run=False)
        if crec.get("curated"):
            rec["applied"].append("stale_touch_curate")
            working = load_trinity_card(vault_root, tid, prefer="provisional")

    if not dry_run:
        gate = apply_trinity_align_gate(vault_root, tid, update_meta=True)
        if gate.get("ok") and not gate.get("stale_touch"):
            rec["applied"].append("align_gate_meta_sync")

    yaml_rec = repair_conduct_card(
        vault_root,
        tid,
        nerve_row=nerve_row,
        dry_run=dry_run,
    )
    if yaml_rec.get("changed"):
        rec["applied"].append("conduct_yaml_repass")
        rec["changed"] = True

    post_card = load_trinity_card(vault_root, tid, prefer="provisional")
    proofs = run_card_behavior_proofs(vault_root, post_card)
    rec["proof_results"] = [p.to_dict() for p in proofs]
    failed = [p for p in proofs if not p.ok]
    rec["proofs_ok"] = len(failed) == 0
    rec["proofs_failed"] = [p.test_name for p in failed][:8]
    rec["failure_classes"] = {
        p.test_name: _failure_class(p.detail or "") for p in failed[:8]
    }

    if failed and allow_llm and not dry_run:
        from .corps_llm_repair import poke_semantic_tier_with_repair

        llm = poke_semantic_tier_with_repair(
            vault_root,
            tid,
            lap=1,
            max_llm_attempts=1,
            llm_enabled=True,
            dry_run=False,
        )
        rec["llm_attempt"] = {
            "semantic_ok": llm.get("semantic_ok"),
            "attempt_count": llm.get("attempt_count"),
        }
        if llm.get("semantic_ok"):
            proofs = run_card_behavior_proofs(vault_root, load_trinity_card(vault_root, tid, prefer="provisional"))
            failed = [p for p in proofs if not p.ok]
            rec["proofs_ok"] = len(failed) == 0
            rec["proofs_failed"] = [p.test_name for p in failed][:8]
            rec["applied"].append("llm_semantic_repair")

    if failed:
        cfg = load_trinity_config(vault_root)
        pack_enabled = bool(getattr(cfg, "corps_conduct_repair_pack_enabled", True))
        if pack_enabled and not dry_run:
            from .corps_conduct_repair_pack import (
                build_conduct_repair_pack_markdown,
                write_conduct_repair_pack,
            )

            pack_md = build_conduct_repair_pack_markdown(
                vault_root,
                tid,
                card=post_card,
                proof_results=rec.get("proof_results"),
                nerve_row=nerve_row,
            )
            pack_path = write_conduct_repair_pack(vault_root, tid, pack_md)
            from .corps_conduct_repair_apply import (
                write_conduct_repair_pack_json,
            )

            write_conduct_repair_pack_json(
                vault_root,
                tid,
                proof_paths=[
                    str(p).strip()
                    for p in ((post_card.get("contract") or {}).get("proof") or [])
                    if str(p).strip()
                ],
                failed_proofs=[p.to_dict() for p in failed],
                write_scope="contract_proof_paths_only",
                pack_md_path=pack_path,
            )
            rec["conduct_pack_built"] = True
            rec["conduct_repair_pack_path"] = str(pack_path.relative_to(vault_root))
            rec["applied"].append("conduct_repair_pack_10g")

            if allow_conduct_apply:
                from .corps_conduct_repair_apply import (
                    apply_conduct_repair_pack,
                    conduct_apply_enabled,
                )

                if conduct_apply_enabled(cfg):
                    apply_rec = apply_conduct_repair_pack(
                        vault_root,
                        tid,
                        pack_path=pack_path,
                        dry_run=dry_run,
                    )
                    rec["conduct_apply_10g"] = apply_rec
                    if apply_rec.get("proofs_ok"):
                        rec["proofs_ok"] = True
                        rec["proofs_failed"] = []
                        rec["manual_required"] = False
                        rec["escalation"] = "conduct_repair_apply_green"
                        rec["applied"].append("conduct_repair_apply_10g")
                    elif apply_rec.get("changed"):
                        rec["applied"].append("conduct_repair_apply_partial")
        rec["manual_required"] = True
        rec["escalation"] = (
            "conduct_repair_pack_ready"
            if rec.get("conduct_pack_built")
            else "operator_test_fix_or_llm"
        )
    elif rec["proofs_ok"]:
        rec["manual_required"] = False

    align_post = check(vault_root, tid, run_behavior_proofs=True)
    rec["align_ok_after"] = align_post.ok
    if align_post.ok and not rec.get("changed"):
        rec["changed"] = True
        rec["applied"].append("proofs_green")

    if rec.get("changed") and not dry_run:
        audit_card_repair(
            vault_root,
            trinity_id=tid,
            repair_type="test_code_10f",
            disconnect_kind="touch_conceptual_gap",
            before_card=card,
            after_card=post_card,
            changed=True,
            extra={
                "proofs_ok": rec.get("proofs_ok"),
                "proofs_failed": rec.get("proofs_failed"),
                "failure_classes": rec.get("failure_classes"),
                "manual_required": rec.get("manual_required"),
            },
        )

    return rec


def run_test_code_conduct_repair_batch(
    vault_root: Path,
    *,
    red_ids: list[str],
    nerves_by_id: dict[str, dict[str, Any]] | None = None,
    dry_run: bool = False,
    allow_llm: bool | None = None,
) -> dict[str, Any]:
    """Phase 10f batch — run after 10d when conduct reds remain."""
    cfg = load_trinity_config(vault_root)
    if not getattr(cfg, "corps_test_code_repair_enabled", True):
        return {
            "ok": True,
            "skipped": True,
            "reason": "corps_test_code_repair_disabled",
            "attempted": 0,
            "changed_count": 0,
            "repairs": [],
        }

    do_llm = (
        bool(getattr(cfg, "corps_llm_repair_enabled", False))
        if allow_llm is None
        else bool(allow_llm)
    )
    max_cards = int(getattr(cfg, "corps_max_test_code_repair_cards", 12))
    global_apply = bool(getattr(cfg, "corps_conduct_repair_auto_apply_enabled", False))
    trial_enabled = bool(getattr(cfg, "corps_conduct_repair_auto_apply_trial_enabled", False))
    max_trial = int(getattr(cfg, "corps_conduct_repair_auto_apply_trial_max_per_run", 3))
    trial_applied = 0

    repairs: list[dict[str, Any]] = []
    changed = 0
    manual: list[str] = []

    for tid in red_ids[:max_cards]:
        allow_apply = global_apply or (
            trial_enabled and trial_applied < max_trial
        )
        row = (nerves_by_id or {}).get(tid)
        rec = repair_test_code_card(
            vault_root,
            tid,
            nerve_row=row,
            dry_run=dry_run,
            allow_llm=do_llm,
            allow_conduct_apply=allow_apply,
        )
        apply_rec = rec.get("conduct_apply_10g")
        if (
            isinstance(apply_rec, dict)
            and not apply_rec.get("skipped")
            and trial_enabled
            and not global_apply
        ):
            trial_applied += 1
        repairs.append(rec)
        if rec.get("changed") or rec.get("align_ok_after"):
            changed += 1
        if rec.get("manual_required"):
            manual.append(tid)

    append_metric_row(
        vault_root,
        {
            "metric_type": "corps_test_code_repair_batch",
            "attempted": len(repairs),
            "changed_count": changed,
            "manual_required_count": len(manual),
            "trial_applied": trial_applied,
        },
    )
    return {
        "ok": True,
        "attempted": len(repairs),
        "changed_count": changed,
        "manual_required_ids": manual[:16],
        "trial_applied": trial_applied,
        "repairs": repairs[:20],
    }
