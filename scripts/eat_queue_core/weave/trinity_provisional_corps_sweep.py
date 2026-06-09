"""Phase 10 — provisional corps sweep + nerve test (peripheral nervous system)."""

from __future__ import annotations

import copy
import fnmatch
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .config import load_trinity_config
from .governance import append_metric_row, ensure_weave_paths
from .trinity_align import check, check_conceptual_leg, check_contract_leg, check_rules_leg
from .trinity_card import get_rules, get_touch, normalize_card, touch_behavior_signals
from .trinity_card_paths import (
    component_proposals_dir,
    list_provisional_trinity_card_ids,
    load_trinity_card,
    write_trinity_card,
)
from .trinity_catchup_sweep import curate_stale_non_core
from .trinity_dual_lock import corps_repair_skip_reason, is_maintenance_core_id
from .trinity_spine_guard import respects_locked_spine
from .trinity_touch_refresh import propose_behavior_signals

NERVE_MAP_REL = Path(".technical/weave/corps-nerve-map.json")
NerveStatus = Literal["green", "yellow", "red"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def nerve_map_path(vault_root: Path) -> Path:
    return vault_root / NERVE_MAP_REL


def load_corps_nerve_map(vault_root: Path) -> dict[str, Any]:
    path = nerve_map_path(vault_root)
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _append_unique(lines: list[str], extra: tuple[str, ...]) -> list[str]:
    seen = {str(x).strip() for x in lines if str(x).strip()}
    out = list(lines)
    for item in extra:
        s = str(item).strip()
        if s and s not in seen:
            out.append(s)
            seen.add(s)
    return out


def apply_corps_precedence_hygiene(card: dict[str, Any]) -> dict[str, Any]:
    """Move excess rules.forbidden → rules.precedence policy lines (Phase 8 pattern for corps)."""
    out = normalize_card(copy.deepcopy(card))
    rules = out.setdefault("rules", {})
    if not isinstance(rules, dict):
        rules = {}
        out["rules"] = rules
    forbidden = [str(x).strip() for x in (rules.get("forbidden") or []) if str(x).strip()]
    precedence = list(rules.get("precedence") or [])
    tests = sum(1 for s in touch_behavior_signals(out) if s.startswith("test_"))
    if len(forbidden) <= tests:
        return out
    keep = forbidden[:tests] if tests > 0 else []
    migrate = forbidden[tests:] if tests > 0 else forbidden
    policy_lines = tuple(f"policy: {line}" for line in migrate)
    rules["forbidden"] = keep
    rules["precedence"] = _append_unique(precedence, policy_lines)
    return out


def _discover_test_signals(vault_root: Path, primary_path: str) -> list[str]:
    """Best-effort test_* behavior_signals for a primary module path."""
    vault_root = vault_root.resolve()
    rel = str(primary_path or "").strip().replace("\\", "/").lstrip("./")
    if not rel.endswith(".py"):
        return []
    stem = Path(rel).stem
    candidates: list[str] = []
    for pattern in (
        f"scripts/eat_queue_core/tests/test_{stem}.py",
        f"scripts/eat_queue_core/tests/test_{stem.replace('_', '')}.py",
    ):
        if (vault_root / pattern).is_file():
            candidates.append(pattern)
    return candidates[:1]


def _wire_tests_if_missing(vault_root: Path, card: dict[str, Any]) -> dict[str, Any]:
    """Add contract proof + test_* behavior_signals when a matching test module exists."""
    out = normalize_card(copy.deepcopy(card))
    touch = out.setdefault("touch", {})
    if not isinstance(touch, dict):
        touch = {}
        out["touch"] = touch
    signals = list(touch.get("behavior_signals") or [])
    if any(str(s).startswith("test_") for s in signals):
        return out
    test_files: list[str] = []
    for path in touch.get("primary_paths") or []:
        test_files.extend(_discover_test_signals(vault_root, str(path)))
    if not test_files:
        return out
    contract = out.setdefault("contract", {})
    if not isinstance(contract, dict):
        contract = {}
        out["contract"] = contract
    proof = list(contract.get("proof") or [])
    for tf in test_files:
        if tf not in proof:
            proof.append(tf)
    contract["proof"] = proof
    proposed = propose_behavior_signals(vault_root, out)
    if proposed:
        touch["behavior_signals"] = _append_unique(signals, tuple(proposed))
    return out


def _filter_cluster_ids(ids: list[str], cluster: str | None) -> list[str]:
    if not cluster:
        return ids
    pat = cluster.strip()
    if pat.endswith("*"):
        return [tid for tid in ids if fnmatch.fnmatch(tid, pat)]
    if "*" in pat or "?" in pat:
        return [tid for tid in ids if fnmatch.fnmatch(tid, pat)]
    return [tid for tid in ids if tid == pat or tid.startswith(f"{pat}_")]


PASS_GATE_ARTICULATION = (
    "Spine aligned on maintenance core; every non-maintenance-core provisional has "
    "touch, rules, and conduct (behavior proofs) aligned to its card; enforce "
    "confirms spine guards on the nerve map sample."
)


def _limit_provisional_ids(
    ids: list[str],
    *,
    full_corpus: bool,
    max_cards: int | None,
    batch_size: int,
    scope_locked: bool = False,
) -> tuple[list[str], dict[str, Any]]:
    """Apply batch cap unless full_corpus or scope_locked (expand_self delta)."""
    meta: dict[str, Any] = {
        "full_corpus": full_corpus,
        "scope_locked": scope_locked,
        "total_candidates": len(ids),
    }
    if full_corpus or scope_locked:
        meta["tested_count"] = len(ids)
        return ids, meta
    cap = batch_size if max_cards is None else max_cards
    meta["batch_cap"] = cap
    if cap > 0:
        limited = ids[:cap]
    else:
        limited = ids
    meta["tested_count"] = len(limited)
    return limited, meta


def build_corps_pass_gate(
    nerve_test: dict[str, Any] | None,
    *,
    full_corpus: bool,
    scope_locked: bool = False,
    proof_adequacy_strict: bool = False,
) -> dict[str, Any]:
    """Pass gate for Phase 9+10: tier booleans + full-corpus green requirement."""
    strict_scope = full_corpus or scope_locked
    if not nerve_test:
        return {
            "articulation": PASS_GATE_ARTICULATION,
            "full_corpus": full_corpus,
            "scope_locked": scope_locked,
            "non_core_must_be_green": strict_scope,
            "ok": not strict_scope,
            "reason": "no_nerve_test" if strict_scope else "sample_mode",
            "shape_ok": not strict_scope,
            "spine_ok": not strict_scope,
            "semantic_ok": not strict_scope,
            "conduct_ok": not strict_scope,
        }
    counts = dict(nerve_test.get("counts") or {})
    nerves = nerve_test.get("nerves") or []
    tier_failures = nerve_test.get("tier_failures") or {}

    red_ids = [
        str(n.get("trinity_id"))
        for n in nerves
        if isinstance(n, dict) and n.get("status") == "red" and n.get("trinity_id")
    ]
    yellow_ids = [
        str(n.get("trinity_id"))
        for n in nerves
        if isinstance(n, dict) and n.get("status") == "yellow" and n.get("trinity_id")
    ]
    strict = not bool(nerve_test.get("conduct_pending_ok"))
    ok = bool(nerve_test.get("ok"))
    if full_corpus and strict:
        ok = counts.get("red", 0) == 0 and counts.get("yellow", 0) == 0

    shape_ok = int(tier_failures.get("shape", 0)) == 0
    spine_ok = int(tier_failures.get("spine", 0)) == 0
    semantic_ok = int(tier_failures.get("semantic", 0)) == 0
    conduct_ok = int(tier_failures.get("conduct", 0)) == 0
    if full_corpus and strict:
        ok = ok and shape_ok and spine_ok and semantic_ok and conduct_ok

    adequacy_summary: dict[str, Any] = {}
    if nerves:
        from .corps_proof_adequacy import summarize_adequacy_from_nerves

        adequacy_summary = summarize_adequacy_from_nerves(nerves)
    if proof_adequacy_strict and int(adequacy_summary.get("low_adequacy_count") or 0) > 0:
        ok = False

    return {
        "articulation": PASS_GATE_ARTICULATION,
        "full_corpus": full_corpus,
        "scope_locked": scope_locked,
        "non_core_must_be_green": strict_scope,
        "ok": ok,
        "shape_ok": shape_ok,
        "spine_ok": spine_ok,
        "semantic_ok": semantic_ok,
        "conduct_ok": conduct_ok,
        "counts": counts,
        "tier_failures": tier_failures,
        "tested": nerve_test.get("tested"),
        "red_ids": red_ids,
        "yellow_ids": yellow_ids,
        "red_count": len(red_ids),
        "proof_adequacy": adequacy_summary,
    }


def classify_nerve_status(
    *,
    shape_ok: bool,
    spine_ok: bool,
    semantic_ok: bool,
    conduct_ok: bool | None,
    conduct_skipped: bool,
    conduct_pending_ok: bool,
) -> NerveStatus:
    """Classify nerve poke result from tier booleans (poke order T0→spine→T1→T2)."""
    if not shape_ok or not spine_ok or not semantic_ok:
        return "red"
    if conduct_skipped:
        return "red"
    if conduct_ok is True:
        return "green"
    if conduct_ok is False:
        return "red"
    # conduct not evaluated — unverified conduct
    return "yellow" if conduct_pending_ok else "red"


def _evaluate_t0_shape(vault_root: Path, card: dict[str, Any]) -> dict[str, Any]:
    """Tier 0 — structural shape (non-empty legs, precedence collapse)."""
    touch = get_touch(card)
    rules = get_rules(card)
    signals = touch_behavior_signals(card)
    tests = sum(1 for s in signals if s.startswith("test_"))
    forbidden_n = len(rules.get("forbidden") or [])
    precedence_collapse = forbidden_n > 0 and forbidden_n > tests
    contract_ok, contract_missing = check_contract_leg(vault_root, card)
    conceptual_ok, conceptual_issues = check_conceptual_leg(card)
    rules_ok, rules_issues = check_rules_leg(card)
    shape_ok = (
        contract_ok
        and conceptual_ok
        and rules_ok
        and not precedence_collapse
    )
    return {
        "shape_ok": shape_ok,
        "precedence_collapse": precedence_collapse,
        "contract_ok": contract_ok,
        "contract_missing": contract_missing[:6],
        "conceptual_issues": conceptual_issues,
        "rules_issues": rules_issues,
        "test_guard_count": tests,
        "forbidden_count": forbidden_n,
    }


def run_nerve_test_one(
    vault_root: Path,
    trinity_id: str,
    *,
    conduct_pending_ok: bool = True,
    lap: int = 1,
    max_llm_attempts: int | None = None,
    llm_repair_enabled: bool | None = None,
    llm_repair_context: Any | None = None,
    skip_conduct_on_semantic_fail: bool | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Poke one provisional nerve: T0 → spine → T1 (≤ max_llm_laps) → T2."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    tid = str(trinity_id).strip()
    row: dict[str, Any] = {"trinity_id": tid, "lap": lap}
    skip = corps_repair_skip_reason(vault_root, tid)
    if skip:
        row["status"] = "skipped"
        row["reason"] = skip
        row["tier"] = {
            "shape_ok": True,
            "spine_ok": True,
            "semantic_ok": True,
            "conduct_ok": True,
            "conduct_skipped": False,
        }
        return row

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError) as e:
        row["status"] = "red"
        row["error"] = str(e)
        row["tier"] = {
            "shape_ok": False,
            "spine_ok": False,
            "semantic_ok": False,
            "conduct_ok": None,
            "conduct_skipped": True,
        }
        return row

    touch = get_touch(card)
    rules = get_rules(card)

    # Tier 0 — shape
    t0 = _evaluate_t0_shape(vault_root, card)
    shape_ok = bool(t0["shape_ok"])

    # Spine guard (safety, not numbered tier)
    guard = respects_locked_spine(vault_root, tid)
    spine_ok = bool(guard.ok)

    # Tier 1 — semantic (inline repair up to max_llm_laps per lap)
    from .corps_llm_repair import poke_semantic_tier_with_repair

    if skip_conduct_on_semantic_fail is None:
        skip_conduct = bool(getattr(cfg, "corps_skip_conduct_on_semantic_fail", True))
    else:
        skip_conduct = bool(skip_conduct_on_semantic_fail)

    semantic_block: dict[str, Any] = {"semantic_ok": False, "hard_fail": True}
    if shape_ok and spine_ok:
        semantic_block = poke_semantic_tier_with_repair(
            vault_root,
            tid,
            lap=lap,
            max_llm_attempts=max_llm_attempts,
            llm_enabled=llm_repair_enabled,
            llm_repair_context=llm_repair_context,
            dry_run=dry_run,
        )
    elif not shape_ok:
        semantic_block = {
            "semantic_ok": False,
            "hard_fail": True,
            "skipped": "t0_shape_fail",
            "attempts": [],
        }
    else:
        semantic_block = {
            "semantic_ok": False,
            "hard_fail": True,
            "skipped": "spine_fail",
            "attempts": [],
        }

    semantic_ok = bool(semantic_block.get("semantic_ok"))
    semantic_hard_fail = bool(semantic_block.get("hard_fail"))

    # Tier 2 — conduct (skip when T1 hard fail)
    conduct_skipped = semantic_hard_fail and skip_conduct
    conduct_ok: bool | None = None
    align = None
    if conduct_skipped:
        conduct_ok = None
    elif shape_ok and spine_ok and semantic_ok:
        tests = int(t0.get("test_guard_count") or 0)
        align = check(vault_root, tid, run_behavior_proofs=tests > 0)
        if tests == 0:
            conduct_ok = None
        else:
            conduct_ok = bool(align.ok)
    elif shape_ok and spine_ok:
        tests = int(t0.get("test_guard_count") or 0)
        if tests > 0:
            align = check(vault_root, tid, run_behavior_proofs=True)
            conduct_ok = bool(align.ok)
        else:
            conduct_ok = None

    tier = {
        "shape_ok": shape_ok,
        "spine_ok": spine_ok,
        "semantic_ok": semantic_ok,
        "conduct_ok": conduct_ok,
        "conduct_skipped": conduct_skipped,
    }
    status = classify_nerve_status(
        shape_ok=shape_ok,
        spine_ok=spine_ok,
        semantic_ok=semantic_ok,
        conduct_ok=conduct_ok,
        conduct_skipped=conduct_skipped,
        conduct_pending_ok=conduct_pending_ok,
    )

    row.update(
        {
            "status": status,
            "tier": tier,
            "signal_in": {
                "primary_paths": list(touch.get("primary_paths") or [])[:3],
                "forbidden_count": t0.get("forbidden_count"),
                "test_guard_count": t0.get("test_guard_count"),
            },
            "semantic": {
                "semantic_ok": semantic_ok,
                "hard_fail": semantic_hard_fail,
                "attempt_count": semantic_block.get("attempt_count", 0),
                "conceptual_issues": semantic_block.get("conceptual_issues") or [],
                "semantic_disconnects": semantic_block.get("semantic_disconnects") or [],
                "attempts": semantic_block.get("attempts") or [],
            },
            "conduct": {
                "align_ok": align.ok if align else None,
                "stale_touch": align.stale_touch if align else None,
                "disconnects": [d.kind for d in align.disconnects][:5] if align else [],
                "behavior_proofs_ran": bool(
                    align and int(t0.get("test_guard_count") or 0) > 0
                ),
                "conduct_skipped": conduct_skipped,
            },
            "signal_out": {
                "respects_locked_spine": guard.ok,
                "violations": [v.kind for v in guard.violations][:4],
            },
            "shape": {
                "precedence_collapse": t0.get("precedence_collapse"),
                "conduct_pending": int(t0.get("test_guard_count") or 0) == 0
                and not t0.get("precedence_collapse"),
                "contract_missing": t0.get("contract_missing") or [],
            },
        }
    )
    try:
        from .corps_proof_adequacy import score_proof_adequacy

        row["proof_adequacy"] = score_proof_adequacy(vault_root, card)
    except Exception:
        row["proof_adequacy"] = {"proof_adequacy_score": 0, "low_adequacy": True}
    return row


def _resolve_provisional_candidate_ids(
    vault_root: Path,
    *,
    cluster: str | None,
    scope_ids: tuple[str, ...] | None = None,
) -> list[str]:
    raw = list_provisional_trinity_card_ids(vault_root)
    if scope_ids:
        wanted = {s.strip() for s in scope_ids if s.strip()}
        raw = [tid for tid in raw if tid in wanted]
    return _filter_cluster_ids(raw, cluster)


def run_corps_sweep(
    vault_root: Path,
    *,
    cluster: str | None = None,
    scope_ids: tuple[str, ...] | None = None,
    apply_hygiene: bool | None = None,
    dry_run: bool = False,
    max_cards: int | None = None,
    full_corpus: bool = False,
    scope_locked: bool = False,
) -> dict[str, Any]:
    """Hygiene pass on component-proposals/ (mutable corps only)."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if apply_hygiene is None:
        apply_hygiene = bool(cfg.corps_sweep_auto_hygiene)

    raw_ids = _resolve_provisional_candidate_ids(
        vault_root, cluster=cluster, scope_ids=scope_ids
    )
    ids, limit_meta = _limit_provisional_ids(
        raw_ids,
        full_corpus=full_corpus,
        max_cards=max_cards,
        batch_size=cfg.corps_cluster_batch_size,
        scope_locked=scope_locked,
    )

    hygiene_applied: list[str] = []
    stale_curated: list[str] = []
    skipped = 0

    for tid in ids:
        if corps_repair_skip_reason(vault_root, tid):
            skipped += 1
            continue
        try:
            card = load_trinity_card(vault_root, tid, prefer="provisional")
        except (OSError, ValueError, FileNotFoundError):
            skipped += 1
            continue

        changed = False
        new_card = card
        if apply_hygiene and not dry_run:
            before = copy.deepcopy(card)
            new_card = apply_corps_precedence_hygiene(before)
            new_card = _wire_tests_if_missing(vault_root, new_card)
            changed = new_card != card
            if changed:
                try:
                    write_trinity_card(vault_root, tid, new_card, tier="provisional")
                    hygiene_applied.append(tid)
                except (OSError, ValueError) as e:
                    skipped += 1
                    if not dry_run:
                        append_metric_row(
                            vault_root,
                            {
                                "metric_type": "corps_hygiene_write_failed",
                                "trinity_id": tid,
                                "error": str(e)[:400],
                            },
                        )

        align = check(vault_root, tid, run_behavior_proofs=False)
        if align.stale_touch and not dry_run:
            crec = curate_stale_non_core(vault_root, tid, align, dry_run=False)
            if crec.get("curated"):
                stale_curated.append(tid)

    return {
        "ok": True,
        "dry_run": dry_run,
        "cluster": cluster,
        "full_corpus": full_corpus,
        "limit": limit_meta,
        "candidates": len(ids),
        "hygiene_applied": hygiene_applied,
        "stale_curated": stale_curated,
        "skipped": skipped,
        "apply_hygiene": apply_hygiene,
    }


def run_nerve_test_batch(
    vault_root: Path,
    *,
    cluster: str | None = None,
    scope_ids: tuple[str, ...] | None = None,
    max_cards: int | None = None,
    conduct_pending_ok: bool | None = None,
    full_corpus: bool = False,
    scope_locked: bool = False,
    lap: int = 1,
    max_llm_attempts: int | None = None,
    llm_repair_enabled: bool | None = None,
    llm_repair_context: Any | None = None,
    skip_conduct_on_semantic_fail: bool | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    cfg = load_trinity_config(vault_root)
    if conduct_pending_ok is None:
        conduct_pending_ok = bool(cfg.corps_conduct_pending_ok)

    raw_ids = _resolve_provisional_candidate_ids(
        vault_root, cluster=cluster, scope_ids=scope_ids
    )
    ids, limit_meta = _limit_provisional_ids(
        raw_ids,
        full_corpus=full_corpus,
        max_cards=max_cards,
        batch_size=cfg.corps_cluster_batch_size,
        scope_locked=scope_locked,
    )

    nerves: list[dict[str, Any]] = []
    counts = {"green": 0, "yellow": 0, "red": 0, "skipped": 0}
    tier_failures = {"shape": 0, "spine": 0, "semantic": 0, "conduct": 0}
    for tid in ids:
        row = run_nerve_test_one(
            vault_root,
            tid,
            conduct_pending_ok=bool(conduct_pending_ok),
            lap=lap,
            max_llm_attempts=max_llm_attempts,
            llm_repair_enabled=llm_repair_enabled,
            llm_repair_context=llm_repair_context,
            skip_conduct_on_semantic_fail=skip_conduct_on_semantic_fail,
            dry_run=dry_run,
        )
        nerves.append(row)
        st = str(row.get("status") or "red")
        counts[st] = counts.get(st, 0) + 1
        tier = row.get("tier") or {}
        if tier.get("shape_ok") is False:
            tier_failures["shape"] += 1
        if tier.get("spine_ok") is False:
            tier_failures["spine"] += 1
        if tier.get("semantic_ok") is False:
            tier_failures["semantic"] += 1
        if tier.get("conduct_skipped"):
            pass
        elif tier.get("conduct_ok") is False:
            tier_failures["conduct"] += 1
        elif tier.get("conduct_ok") is None and st == "red":
            tier_failures["conduct"] += 1

    failing_red = counts.get("red", 0)
    pending_yellow = counts.get("yellow", 0)
    ok = failing_red == 0 and (conduct_pending_ok or pending_yellow == 0)
    return {
        "ok": ok,
        "conduct_pending_ok": conduct_pending_ok,
        "unverified_conduct": pending_yellow,
        "cluster": cluster,
        "lap": lap,
        "counts": counts,
        "tier_failures": tier_failures,
        "nerves": nerves,
        "tested": len(nerves),
    }


def write_corps_nerve_map(vault_root: Path, payload: dict[str, Any]) -> Path:
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    path = nerve_map_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def run_trinity_provisional_corps_sweep(
    vault_root: Path,
    *,
    dry_run: bool = False,
    cluster: str | None = None,
    scope_ids: tuple[str, ...] | None = None,
    scope_locked: bool = False,
    apply_hygiene: bool | None = None,
    nerve_test_only: bool = False,
    skip_sweep: bool = False,
    skip_nerve_test: bool = False,
    max_cards: int | None = None,
    full_corpus: bool = False,
    write_map: bool = True,
    lap: int = 1,
    max_llm_attempts: int | None = None,
    llm_repair_enabled: bool | None = None,
    llm_repair_context: Any | None = None,
    skip_conduct_on_semantic_fail: bool | None = None,
) -> dict[str, Any]:
    """Phase 10 — corps sweep then nerve test."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not cfg.corps_sweep_enabled:
        return {"ok": True, "skipped": True, "reason": "corps_sweep_disabled", "phase": 10}

    report: dict[str, Any] = {
        "ok": True,
        "phase": 10,
        "dry_run": dry_run,
        "started_at": _now_iso(),
        "cluster": cluster,
        "scope_ids": list(scope_ids or ()),
        "scope_locked": scope_locked,
        "full_corpus": full_corpus,
    }

    if not skip_sweep and not nerve_test_only:
        report["corps_sweep"] = run_corps_sweep(
            vault_root,
            cluster=cluster,
            scope_ids=scope_ids,
            apply_hygiene=apply_hygiene,
            dry_run=dry_run,
            max_cards=max_cards,
            full_corpus=full_corpus,
            scope_locked=scope_locked,
        )

    if not skip_nerve_test and cfg.corps_nerve_test_enabled and not dry_run:
        report["nerve_test"] = run_nerve_test_batch(
            vault_root,
            cluster=cluster,
            scope_ids=scope_ids,
            max_cards=max_cards,
            full_corpus=full_corpus,
            scope_locked=scope_locked,
            lap=lap,
            max_llm_attempts=max_llm_attempts,
            llm_repair_enabled=llm_repair_enabled,
            llm_repair_context=llm_repair_context,
            skip_conduct_on_semantic_fail=skip_conduct_on_semantic_fail,
            dry_run=dry_run,
        )
        if llm_repair_context is not None:
            report["llm_repair_run_context"] = llm_repair_context.to_dict()
        report["pass_gate"] = build_corps_pass_gate(
            report["nerve_test"],
            full_corpus=full_corpus,
            scope_locked=scope_locked,
            proof_adequacy_strict=bool(getattr(cfg, "corps_proof_adequacy_strict", False)),
        )
        if not report["pass_gate"].get("ok"):
            report["ok"] = False
        elif not report["nerve_test"].get("ok"):
            report["ok"] = False

    if write_map and not dry_run and report.get("nerve_test"):
        map_payload = {
            "generated_at": _now_iso(),
            "cluster": cluster,
            "counts": report["nerve_test"].get("counts"),
            "nerves": report["nerve_test"].get("nerves"),
        }
        path = write_corps_nerve_map(vault_root, map_payload)
        report["nerve_map_path"] = str(path.relative_to(vault_root))

    append_metric_row(
        vault_root,
        {
            "metric_type": "trinity_provisional_corps_sweep",
            "ok": report.get("ok"),
            "cluster": cluster,
            "dry_run": dry_run,
        },
    )
    report["completed_at"] = _now_iso()
    return report
