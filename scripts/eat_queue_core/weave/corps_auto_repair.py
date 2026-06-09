"""Deterministic corps repair for non-maintenance-core provisionals (no LLM).

Runs inside self-wrap repair laps: hygiene, smoke tests, conceptual synth, stale touch.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .corps_smoke_test import ensure_smoke_test_file
from .governance import append_metric_row
from .trinity_align import (
    check,
    check_conceptual_leg,
    reconcile_forbidden_with_primary_code,
)
from .trinity_card import get_rules, get_touch, normalize_card
from .trinity_card_paths import load_trinity_card, write_trinity_card
from .trinity_catchup_sweep import curate_stale_non_core
from .trinity_dual_lock import corps_repair_skip_reason
from .trinity_provisional_corps_sweep import (
    _wire_tests_if_missing,
    apply_corps_precedence_hygiene,
    build_corps_pass_gate,
    run_trinity_provisional_corps_sweep,
    touch_behavior_signals,
)
from .trinity_spine_guard import respects_locked_spine


def _is_conduct_only_red(nerve_row: dict[str, Any] | None) -> bool:
    tier = (nerve_row or {}).get("tier") or {}
    if tier.get("shape_ok") is False:
        return False
    if tier.get("spine_ok") is False:
        return False
    if tier.get("semantic_ok") is False:
        return False
    if tier.get("conduct_skipped"):
        return False
    return tier.get("conduct_ok") is False


def _split_red_ids_for_repair(
    red_ids: list[str],
    nerves_by_id: dict[str, dict[str, Any]] | None,
) -> tuple[list[str], list[str]]:
    conduct: list[str] = []
    other: list[str] = []
    for tid in red_ids:
        row = (nerves_by_id or {}).get(tid)
        if _is_conduct_only_red(row):
            conduct.append(tid)
        else:
            other.append(tid)
    return conduct, other


def _needs_conceptual_repair(card: dict[str, Any]) -> bool:
    ok, issues = check_conceptual_leg(card)
    if ok:
        return False
    return any("primary_case" in i or "summary" in i for i in issues)


def _apply_conceptual_synth(
    vault_root: Path,
    trinity_id: str,
    card: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    from .trinity_conceptual_doctrine import synthesize_conceptual_human_vantage

    out = copy.deepcopy(card)
    out["conceptual"] = synthesize_conceptual_human_vantage(
        vault_root,
        trinity_id,
        card,
        neighbor_ids=[],
        corpus={trinity_id: card},
    )
    return out, out.get("conceptual") != card.get("conceptual")


def _card_precedence_collapse(card: dict[str, Any]) -> bool:
    rules = get_rules(card)
    forbidden_n = len(rules.get("forbidden") or [])
    tests = sum(1 for s in touch_behavior_signals(card) if str(s).startswith("test_"))
    return forbidden_n > 0 and forbidden_n > tests


def _spine_violation_kinds(vault_root: Path, trinity_id: str, card: dict[str, Any]) -> set[str]:
    guard = respects_locked_spine(vault_root, trinity_id, card=normalize_card(card))
    return {v.kind for v in guard.violations}


def _should_apply_precedence_hygiene(
    card: dict[str, Any],
    *,
    shape: dict[str, Any],
    disconnects: list[str],
    spine_violations: set[str],
) -> bool:
    if shape.get("precedence_collapse"):
        return True
    if "precedence_collapse" in disconnects:
        return True
    if "disconnect_precedence_collapse" in spine_violations:
        return True
    return _card_precedence_collapse(card)


def _should_wire_smoke_tests(
    *,
    nerve_row: dict[str, Any],
    shape: dict[str, Any],
    disconnects: list[str],
    spine_violations: set[str],
    card: dict[str, Any],
) -> bool:
    test_count = int((nerve_row.get("signal_in") or {}).get("test_guard_count") or 0)
    tier = nerve_row.get("tier") or {}
    if test_count == 0 or shape.get("conduct_pending"):
        return True
    if tier.get("shape_ok") is False or tier.get("spine_ok") is False:
        return True
    if "disconnect_precedence_collapse" in spine_violations:
        return True
    if _card_precedence_collapse(card):
        return True
    if shape.get("precedence_collapse") or "precedence_collapse" in disconnects:
        return True
    return False


def _should_apply_forbidden_drift_repair(
    *,
    disconnects: list[str],
    spine_violations: set[str],
    card: dict[str, Any],
    vault_root: Path,
) -> bool:
    if "error_narrative_drift" in disconnects:
        return True
    if "disconnect_error_narrative_drift" in spine_violations:
        return True
    from .trinity_align import forbidden_phrase_hits_primary_code

    rules = get_rules(card)
    forbidden = rules.get("forbidden") or []
    if not isinstance(forbidden, list):
        return False
    return any(
        forbidden_phrase_hits_primary_code(vault_root, card, str(p).strip())
        for p in forbidden
        if str(p).strip()
    )


def repair_provisional_card(
    vault_root: Path,
    trinity_id: str,
    *,
    nerve_row: dict[str, Any] | None = None,
    dry_run: bool = False,
    use_conceptual_synth: bool = True,
) -> dict[str, Any]:
    """Best-effort deterministic repair for one non-core provisional."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    rec: dict[str, Any] = {"trinity_id": tid, "applied": [], "changed": False}

    skip = corps_repair_skip_reason(vault_root, tid)
    if skip:
        rec["skipped"] = skip
        return rec

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError) as e:
        rec["error"] = str(e)
        return rec

    nerve_row = nerve_row or {}
    conduct = nerve_row.get("conduct") or {}
    shape = nerve_row.get("shape") or {}
    tier = nerve_row.get("tier") or {}
    semantic = nerve_row.get("semantic") or {}
    disconnects = list(conduct.get("disconnects") or [])

    working = copy.deepcopy(card)
    pre_violations = _spine_violation_kinds(vault_root, tid, working)
    if pre_violations:
        rec["pre_repair_spine_violations"] = sorted(pre_violations)[:6]

    if _should_apply_precedence_hygiene(
        working,
        shape=shape,
        disconnects=disconnects,
        spine_violations=pre_violations,
    ):
        before = normalize_card(copy.deepcopy(working))
        working = apply_corps_precedence_hygiene(working)
        if normalize_card(working) != before:
            rec["applied"].append("precedence_hygiene")

    if _should_apply_forbidden_drift_repair(
        disconnects=disconnects,
        spine_violations=pre_violations,
        card=working,
        vault_root=vault_root,
    ):
        before = normalize_card(copy.deepcopy(working))
        working, migrated = reconcile_forbidden_with_primary_code(vault_root, working)
        if migrated:
            rec["applied"].append("error_narrative_drift_reconcile")
            rec["drift_migrated_forbidden"] = migrated[:8]

    if _should_wire_smoke_tests(
        nerve_row=nerve_row,
        shape=shape,
        disconnects=disconnects,
        spine_violations=pre_violations,
        card=working,
    ):
        for raw_path in get_touch(working).get("primary_paths") or []:
            ensure_smoke_test_file(vault_root, str(raw_path))
        before = normalize_card(copy.deepcopy(working))
        working = _wire_tests_if_missing(vault_root, working)
        if normalize_card(working) != before:
            rec["applied"].append("wire_smoke_tests")

    if use_conceptual_synth and (
        _needs_conceptual_repair(working)
        or tier.get("semantic_ok") is False
        or semantic.get("hard_fail")
    ):
        working, synth_changed = _apply_conceptual_synth(vault_root, tid, working)
        if synth_changed:
            rec["applied"].append("conceptual_synth")

    align = check(vault_root, tid, run_behavior_proofs=False)
    if align.stale_touch and not dry_run:
        crec = curate_stale_non_core(vault_root, tid, align, dry_run=False)
        if crec.get("curated"):
            rec["applied"].append("stale_touch_curate")
            working = load_trinity_card(vault_root, tid, prefer="provisional")

    post_violations = _spine_violation_kinds(vault_root, tid, working)
    if post_violations:
        rec["post_repair_spine_violations"] = sorted(post_violations)[:6]

    changed = normalize_card(working) != normalize_card(card)
    rec["changed"] = changed
    shape_ladder = {
        "precedence_hygiene",
        "wire_smoke_tests",
        "error_narrative_drift_reconcile",
    } & set(rec["applied"])
    use_repair_override = bool(shape_ladder) or (bool(pre_violations) and bool(rec["applied"]))

    if changed and not dry_run:
        try:
            write_trinity_card(
                vault_root,
                tid,
                working,
                tier="provisional",
                mutation_action="corps_auto_repair_shape",
                operator_override=use_repair_override or None,
            )
            rec["repair_write_override"] = use_repair_override
        except (OSError, ValueError) as e:
            rec["write_error"] = str(e)
            rec["changed"] = False
            append_metric_row(
                vault_root,
                {
                    "metric_type": "corps_auto_repair_write_failed",
                    "trinity_id": tid,
                    "error": str(e)[:400],
                },
            )
    elif changed and dry_run:
        rec["would_write"] = True
        rec["repair_write_override"] = use_repair_override

    return rec


def run_corps_auto_repair_batch(
    vault_root: Path,
    *,
    red_ids: list[str],
    nerves_by_id: dict[str, dict[str, Any]] | None = None,
    dry_run: bool = False,
    use_conceptual_synth: bool = True,
) -> dict[str, Any]:
    """Repair a batch of red nerve ids; returns counts for lap termination."""
    repairs: list[dict[str, Any]] = []
    changed = 0
    for tid in red_ids:
        row = (nerves_by_id or {}).get(tid)
        rec = repair_provisional_card(
            vault_root,
            tid,
            nerve_row=row,
            dry_run=dry_run,
            use_conceptual_synth=use_conceptual_synth,
        )
        repairs.append(rec)
        if rec.get("changed"):
            changed += 1
    return {
        "ok": True,
        "attempted": len(red_ids),
        "changed_count": changed,
        "repairs": repairs,
    }


def _summarize_red_ids_by_tier(nerves: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Group red nerve rows by first failing tier (shape → spine → semantic → conduct)."""
    out: dict[str, list[str]] = {
        "shape": [],
        "spine": [],
        "semantic": [],
        "conduct": [],
        "unknown": [],
    }
    for n in nerves:
        if not isinstance(n, dict) or n.get("status") != "red":
            continue
        tid = str(n.get("trinity_id") or "").strip()
        if not tid:
            continue
        tier = n.get("tier") or {}
        if tier.get("shape_ok") is False:
            out["shape"].append(tid)
        elif tier.get("spine_ok") is False:
            out["spine"].append(tid)
        elif tier.get("semantic_ok") is False:
            out["semantic"].append(tid)
        elif tier.get("conduct_ok") is False and not tier.get("conduct_skipped"):
            out["conduct"].append(tid)
        else:
            out["unknown"].append(tid)
    return out


def _build_gen_red_baseline(
    pass_gate: dict[str, Any],
    nerves: list[dict[str, Any]],
) -> dict[str, Any]:
    counts = dict(pass_gate.get("counts") or {})
    red_n = int(pass_gate.get("red_count") or counts.get("red") or 0)
    green_n = int(counts.get("green") or 0)
    tested = int(pass_gate.get("tested") or 0)
    denom = max(tested, green_n + red_n, 1)
    return {
        "red_count": red_n,
        "green_count": green_n,
        "tested": tested,
        "gen_green_pct": round(100.0 * green_n / denom, 1),
        "red_ids": list(pass_gate.get("red_ids") or [])[:64],
        "red_ids_by_tier": _summarize_red_ids_by_tier(nerves),
        "tier_failures": dict(pass_gate.get("tier_failures") or {}),
        "pass_gate_ok": bool(pass_gate.get("ok")),
    }


def run_corps_sweep_with_repair_loop(
    vault_root: Path,
    *,
    dry_run: bool = False,
    cluster: str | None = None,
    scope_ids: tuple[str, ...] | None = None,
    apply_hygiene: bool | None = None,
    full_corpus: bool = True,
    scope_locked: bool = False,
    max_laps: int | None = None,
    max_llm_laps: int | None = None,
    auto_repair: bool | None = None,
    llm_repair_enabled: bool | None = None,
    llm_repair_context: Any | None = None,
    llm_repair_speed_mode: str | None = None,
    llm_repair_force: bool = False,
    use_conceptual_synth: bool = True,
    write_map: bool = True,
    capture_gen_red_baseline: bool = False,
) -> dict[str, Any]:
    """Corps sweep + one-lap nerve poke per iteration until green or max_laps / no progress."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    laps_cap = max(
        int(
            max_laps
            if max_laps is not None
            else getattr(cfg, "corps_max_laps", getattr(cfg, "corps_self_wrap_max_laps", 3))
        ),
        1,
    )
    llm_cap = max(
        int(
            max_llm_laps
            if max_llm_laps is not None
            else getattr(cfg, "corps_max_llm_laps", 2)
        ),
        0,
    )
    do_repair = (
        bool(getattr(cfg, "corps_auto_repair_enabled", True))
        if auto_repair is None
        else bool(auto_repair)
    )
    from .corps_llm_repair import LlmRepairRunContext

    llm_ctx = llm_repair_context
    if llm_ctx is None:
        harness_llm = (
            bool(llm_repair_enabled)
            if llm_repair_enabled is not None
            else False
        )
        llm_ctx = LlmRepairRunContext(
            cluster=cluster,
            speed_mode=llm_repair_speed_mode or "balance",
            harness_enable_llm=harness_llm,
            harness_force=bool(llm_repair_force),
        )
    elif llm_repair_enabled is True:
        llm_ctx.harness_enable_llm = True
    elif llm_repair_enabled is False:
        llm_ctx.harness_enable_llm = False

    laps: list[dict[str, Any]] = []
    last: dict[str, Any] = {}
    stop_reason = "max_laps"
    gen_red_baseline: dict[str, Any] | None = None

    for lap in range(1, laps_cap + 1):
        sweep = run_trinity_provisional_corps_sweep(
            vault_root,
            dry_run=dry_run,
            cluster=cluster,
            scope_ids=scope_ids,
            apply_hygiene=apply_hygiene if lap == 1 else False,
            full_corpus=full_corpus,
            scope_locked=scope_locked,
            write_map=write_map,
            lap=lap,
            max_llm_attempts=llm_cap,
            llm_repair_enabled=None,
            llm_repair_context=llm_ctx,
        )
        pass_gate = sweep.get("pass_gate") or build_corps_pass_gate(
            sweep.get("nerve_test"),
            full_corpus=full_corpus,
        )
        lap_rec: dict[str, Any] = {
            "lap": lap,
            "ok": bool(pass_gate.get("ok")),
            "pass_gate": pass_gate,
            "corps_sweep": sweep.get("corps_sweep"),
            "nerve_test": {
                "counts": (sweep.get("nerve_test") or {}).get("counts"),
                "tier_failures": (sweep.get("nerve_test") or {}).get("tier_failures"),
                "tested": (sweep.get("nerve_test") or {}).get("tested"),
            },
            "repair": None,
        }
        laps.append(lap_rec)
        last = sweep

        if capture_gen_red_baseline and lap == 1 and gen_red_baseline is None:
            nerves = (sweep.get("nerve_test") or {}).get("nerves") or []
            gen_red_baseline = _build_gen_red_baseline(pass_gate, nerves)

        if pass_gate.get("ok"):
            stop_reason = "pass_gate_green"
            break

        red_ids = list(pass_gate.get("red_ids") or [])
        if not red_ids:
            stop_reason = "no_reds_unexpected_fail"
            break
        if not do_repair or dry_run:
            stop_reason = "repair_disabled_or_dry_run"
            break

        nerves = (sweep.get("nerve_test") or {}).get("nerves") or []
        by_id = {
            str(n.get("trinity_id")): n
            for n in nerves
            if isinstance(n, dict) and n.get("trinity_id")
        }
        conduct_reds, shape_reds = _split_red_ids_for_repair(red_ids, by_id)
        repair_meta: dict[str, Any] = {"card_yaml": None, "test_code": None, "shape": None}
        changed_total = 0

        if conduct_reds:
            from .corps_conduct_repair import run_corps_conduct_repair_batch

            conduct_repair = run_corps_conduct_repair_batch(
                vault_root,
                red_ids=conduct_reds,
                nerves_by_id=by_id,
                dry_run=dry_run,
            )
            repair_meta["card_yaml"] = {
                "attempted": conduct_repair.get("attempted"),
                "changed_count": conduct_repair.get("changed_count"),
            }
            changed_total += int(conduct_repair.get("changed_count") or 0)

            cfg = load_trinity_config(vault_root)
            if getattr(cfg, "corps_test_code_repair_enabled", True):
                from .corps_test_code_repair import run_test_code_conduct_repair_batch

                test_code_repair = run_test_code_conduct_repair_batch(
                    vault_root,
                    red_ids=conduct_reds,
                    nerves_by_id=by_id,
                    dry_run=dry_run,
                    allow_llm=bool(llm_ctx.harness_enable_llm),
                )
                repair_meta["test_code"] = {
                    "attempted": test_code_repair.get("attempted"),
                    "changed_count": test_code_repair.get("changed_count"),
                    "manual_required_ids": test_code_repair.get("manual_required_ids"),
                }
                changed_total += int(test_code_repair.get("changed_count") or 0)

            # Legacy alias for dashboards
            repair_meta["conduct"] = repair_meta["card_yaml"]

        if shape_reds:
            repair = run_corps_auto_repair_batch(
                vault_root,
                red_ids=shape_reds,
                nerves_by_id=by_id,
                dry_run=dry_run,
                use_conceptual_synth=use_conceptual_synth,
            )
            repair_meta["shape"] = {
                "attempted": repair.get("attempted"),
                "changed_count": repair.get("changed_count"),
            }
            changed_total += int(repair.get("changed_count") or 0)

        lap_rec["repair"] = {
            "attempted": len(red_ids),
            "changed_count": changed_total,
            **repair_meta,
        }
        if changed_total == 0:
            tc_meta = repair_meta.get("test_code") or {}
            manual_ids = list(tc_meta.get("manual_required_ids") or [])
            stop_reason = (
                "repair_stuck_test_manual_required"
                if manual_ids
                else "repair_stuck_no_changes"
            )
            if manual_ids:
                lap_rec["repair"]["manual_required_ids"] = manual_ids
            break
    else:
        stop_reason = "max_laps"

    final_gate = laps[-1]["pass_gate"] if laps else {}
    ok = bool(final_gate.get("ok"))
    out = dict(last)
    out["ok"] = ok
    out["repair_loop"] = {
        "max_laps": laps_cap,
        "max_llm_laps": llm_cap,
        "auto_repair": do_repair,
        "llm_repair_run_context": llm_ctx.to_dict(),
        "full_corpus": full_corpus,
        "lap_count": len(laps),
        "stop_reason": stop_reason,
        "laps": laps,
        "gen_red_baseline": gen_red_baseline,
    }
    out["pass_gate"] = final_gate
    append_metric_row(
        vault_root,
        {
            "metric_type": "corps_repair_loop",
            "ok": ok,
            "lap_count": len(laps),
            "stop_reason": stop_reason,
            "red_count": final_gate.get("red_count"),
        },
    )
    from .corps_repair_audit import append_corps_repair_audit

    for lap_rec in laps:
        repair = lap_rec.get("repair") or {}
        append_corps_repair_audit(
            vault_root,
            {
                "event": "repair_loop_lap",
                "lap": lap_rec.get("lap"),
                "pass_gate_ok": lap_rec.get("ok"),
                "changed_count": (repair.get("changed_count") if isinstance(repair, dict) else None),
                "stop_reason": stop_reason if lap_rec == laps[-1] else None,
                "red_count": (lap_rec.get("pass_gate") or {}).get("red_count"),
            },
        )
    return out
