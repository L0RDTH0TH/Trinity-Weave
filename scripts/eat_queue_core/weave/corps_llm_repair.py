"""Tier 1 (semantic) repair at nerve poke — up to max_llm_laps attempts per card per lap.

Global ``corps_llm_repair_enabled`` (default off) or **profile-scoped trial** (balance +
``--corps-cluster`` + per-run cap) enables LLM-pack mode at T1. When LLM mode is off,
uses host apply from pack (10c-B) when enabled, else heuristic conceptual synth fallback.
"""

from __future__ import annotations

import copy
import fnmatch
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .corps_repair_audit import append_corps_repair_audit
from .governance import append_metric_row, ensure_weave_paths
from .trinity_align import check_conceptual_leg, check_pilot_disconnects, check_rules_leg
from .trinity_card_paths import load_trinity_card, write_trinity_card
from .trinity_conceptual_doctrine import build_conceptual_regen_pack_markdown
from .trinity_dual_lock import corps_repair_skip_reason

ARTIFACT_DIR = Path(".technical/weave/validation")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass
class LlmRepairRunContext:
    """Per self-wrap / trial run — shared trial budget and scope."""

    cluster: str | None = None
    speed_mode: str | None = None
    harness_enable_llm: bool = False
    harness_force: bool = False
    trial_cards_used: int = 0
    llm_trial_card_ids: set[str] = field(default_factory=set)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cluster": self.cluster,
            "speed_mode": self.speed_mode,
            "harness_enable_llm": self.harness_enable_llm,
            "harness_force": self.harness_force,
            "trial_cards_used": self.trial_cards_used,
            "llm_trial_card_ids": sorted(self.llm_trial_card_ids),
        }


def card_matches_cluster(trinity_id: str, cluster: str | None) -> bool:
    if not cluster:
        return True
    tid = str(trinity_id or "").strip()
    pat = cluster.strip()
    if pat.endswith("*") or "*" in pat or "?" in pat:
        return fnmatch.fnmatch(tid, pat)
    return tid == pat or tid.startswith(f"{pat}_")


def llm_repair_global_enabled(cfg: Any) -> bool:
    return bool(getattr(cfg, "corps_llm_repair_enabled", False))


def llm_repair_trial_enabled(cfg: Any) -> bool:
    return bool(getattr(cfg, "corps_llm_repair_trial_enabled", False))


def _trial_profiles(cfg: Any) -> tuple[str, ...]:
    raw = getattr(cfg, "corps_llm_repair_trial_profiles", ("balance",))
    if isinstance(raw, str):
        return tuple(x.strip().lower() for x in raw.split(",") if x.strip())
    return tuple(str(x).strip().lower() for x in raw if str(x).strip())


def resolve_llm_mode_for_card(
    vault_root: Path,
    trinity_id: str,
    cfg: Any,
    ctx: LlmRepairRunContext | None,
    *,
    explicit_llm: bool | None = None,
) -> tuple[bool, str]:
    """Return (use_llm_pack_mode, reason_token)."""
    tid = str(trinity_id or "").strip()
    skip = corps_repair_skip_reason(vault_root, tid)
    if skip:
        return False, skip

    if explicit_llm is False:
        return False, "explicit_off"
    if ctx and ctx.harness_force:
        if ctx.cluster and not card_matches_cluster(tid, ctx.cluster):
            return False, "outside_cluster"
        return True, "operator_force"

    if explicit_llm is True or llm_repair_global_enabled(cfg):
        if ctx and ctx.cluster and not card_matches_cluster(tid, ctx.cluster):
            return False, "outside_cluster"
        return True, "global" if llm_repair_global_enabled(cfg) else "harness"

    if ctx is None:
        return False, "disabled"

    if not llm_repair_trial_enabled(cfg):
        return False, "trial_disabled"

    if not ctx.harness_enable_llm:
        return False, "trial_not_requested"

    if not ctx.cluster:
        return False, "trial_requires_cluster"

    if not card_matches_cluster(tid, ctx.cluster):
        return False, "outside_cluster"

    mode = (ctx.speed_mode or "balance").strip().lower()
    profiles = _trial_profiles(cfg)
    if mode not in profiles:
        return False, f"profile_not_allowed:{mode}"

    max_per_run = int(getattr(cfg, "corps_llm_repair_trial_max_cards_per_run", 7))
    if tid not in ctx.llm_trial_card_ids and ctx.trial_cards_used >= max_per_run:
        return False, "trial_cap_exhausted"

    return True, "trial"


def _reserve_trial_card(ctx: LlmRepairRunContext | None, trinity_id: str) -> None:
    if ctx is None:
        return
    tid = str(trinity_id).strip()
    if tid in ctx.llm_trial_card_ids:
        return
    ctx.llm_trial_card_ids.add(tid)
    ctx.trial_cards_used = len(ctx.llm_trial_card_ids)


def evaluate_semantic_tier(
    vault_root: Path,
    card: dict[str, Any],
    *,
    run_behavior_proofs: bool = False,
) -> dict[str, Any]:
    """Tier 1 semantic eval without inline repair."""
    conceptual_ok, conceptual_issues = check_conceptual_leg(card)
    rules_ok, rules_issues = check_rules_leg(card)
    disconnects = check_pilot_disconnects(
        vault_root,
        card,
        run_behavior_proofs=run_behavior_proofs,
    )
    semantic_disconnects = [
        d
        for d in disconnects
        if d.kind
        not in (
            "touch_conceptual_gap",
        )
    ]
    semantic_ok = (
        conceptual_ok
        and rules_ok
        and len(semantic_disconnects) == 0
    )
    return {
        "semantic_ok": semantic_ok,
        "conceptual_ok": conceptual_ok,
        "rules_ok": rules_ok,
        "conceptual_issues": conceptual_issues,
        "rules_issues": rules_issues,
        "semantic_disconnects": [d.kind for d in semantic_disconnects],
        "hard_fail": not semantic_ok,
    }


def _apply_heuristic_conceptual(
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


def _one_semantic_attempt(
    vault_root: Path,
    trinity_id: str,
    card: dict[str, Any],
    *,
    lap: int,
    attempt: int,
    llm_enabled: bool,
    nerve_row: dict[str, Any] | None,
    dry_run: bool,
    llm_reason: str = "",
) -> dict[str, Any]:
    """Single T1 repair attempt; returns attempt record."""
    rec: dict[str, Any] = {
        "lap": lap,
        "attempt": attempt,
        "mode": "llm_pack" if llm_enabled else "heuristic",
        "llm_reason": llm_reason or None,
        "changed": False,
    }
    before = evaluate_semantic_tier(vault_root, card)
    if before["semantic_ok"]:
        rec["skipped"] = "already_semantic_ok"
        return rec

    working = copy.deepcopy(card)
    host_applied = False
    changed = False
    if llm_enabled:
        from .config import load_trinity_config as _load_cfg
        from .corps_semantic_repair_apply import (
            apply_semantic_regen_pack,
            semantic_host_apply_enabled,
            write_semantic_regen_pack,
            write_semantic_regen_pack_json,
        )

        cfg = _load_cfg(vault_root)
        pack = build_conceptual_regen_pack_markdown(
            vault_root,
            trinity_id,
            card,
            neighbor_ids=[],
            corpus={trinity_id: card},
        )
        ts = _stamp()
        pack_path = write_semantic_regen_pack(
            vault_root, trinity_id, pack, timestamp=ts
        )
        write_semantic_regen_pack_json(
            vault_root, trinity_id, pack_md_path=pack_path, timestamp=ts
        )
        append_corps_repair_audit(
            vault_root,
            {
                "event": "semantic_regen_pack",
                "trinity_id": trinity_id,
                "lap": lap,
                "attempt": attempt,
                "pack_chars": len(pack),
                "pack_path": str(pack_path.relative_to(vault_root)),
                "nerve_status": (nerve_row or {}).get("status"),
                "llm_reason": llm_reason,
            },
        )
        rec["audit"] = "semantic_regen_pack"
        rec["pack_path"] = str(pack_path.relative_to(vault_root))
        append_metric_row(
            vault_root,
            {
                "metric_type": "llm_patch_proposed",
                "trinity_id": trinity_id,
                "lap": lap,
                "attempt": attempt,
                "llm_reason": llm_reason,
            },
        )

        host_changed = False
        if semantic_host_apply_enabled(cfg) and not dry_run:
            apply_rec = apply_semantic_regen_pack(
                vault_root,
                trinity_id,
                pack_path=pack_path,
                dry_run=False,
            )
            rec["host_apply"] = apply_rec
            host_changed = bool(apply_rec.get("changed"))
            host_applied = host_changed
            rec["mode"] = "host_apply_10c"
        elif semantic_host_apply_enabled(cfg) and dry_run:
            rec["mode"] = "host_apply_10c_dry_run"

        if host_changed:
            try:
                card = load_trinity_card(vault_root, trinity_id, prefer="provisional")
                working = copy.deepcopy(card)
                changed = True
            except (OSError, ValueError, FileNotFoundError):
                changed = False
        else:
            working, changed = _apply_heuristic_conceptual(vault_root, trinity_id, working)
            if llm_enabled and not host_changed:
                rec["mode"] = rec.get("mode") or "heuristic_fallback"
    else:
        working, changed = _apply_heuristic_conceptual(vault_root, trinity_id, working)

    rec["changed"] = changed
    if changed and not dry_run and not host_applied:
        try:
            write_trinity_card(vault_root, trinity_id, working, tier="provisional")
            card = load_trinity_card(vault_root, trinity_id, prefer="provisional")
        except (OSError, ValueError) as e:
            rec["write_error"] = str(e)
            rec["changed"] = False

    after = evaluate_semantic_tier(vault_root, card)
    rec["semantic_ok_after"] = after["semantic_ok"]
    rec["conceptual_issues_after"] = after.get("conceptual_issues") or []
    if llm_enabled and after["semantic_ok"]:
        append_metric_row(
            vault_root,
            {
                "metric_type": "llm_patch_accepted",
                "trinity_id": trinity_id,
                "lap": lap,
                "attempt": attempt,
            },
        )
    elif llm_enabled and not after["semantic_ok"]:
        append_metric_row(
            vault_root,
            {
                "metric_type": "llm_patch_rejected",
                "trinity_id": trinity_id,
                "lap": lap,
                "attempt": attempt,
            },
        )
    return rec


def poke_semantic_tier_with_repair(
    vault_root: Path,
    trinity_id: str,
    *,
    lap: int = 1,
    max_llm_attempts: int | None = None,
    llm_enabled: bool | None = None,
    llm_repair_context: LlmRepairRunContext | None = None,
    nerve_row: dict[str, Any] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """T1 poke: evaluate semantic; up to max_llm_attempts inline repairs per lap."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    cfg = load_trinity_config(vault_root)
    attempts_cap = max(
        int(
            max_llm_attempts
            if max_llm_attempts is not None
            else getattr(cfg, "corps_max_llm_laps", 2)
        ),
        0,
    )

    skip = corps_repair_skip_reason(vault_root, tid)
    if skip:
        return {
            "semantic_ok": True,
            "skipped": skip,
            "attempts": [],
            "hard_fail": False,
        }

    do_llm, llm_reason = resolve_llm_mode_for_card(
        vault_root,
        tid,
        cfg,
        llm_repair_context,
        explicit_llm=llm_enabled,
    )
    if do_llm and llm_reason == "trial":
        _reserve_trial_card(llm_repair_context, tid)

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError) as e:
        return {
            "semantic_ok": False,
            "error": str(e),
            "attempts": [],
            "hard_fail": True,
        }

    eval0 = evaluate_semantic_tier(vault_root, card)
    if eval0["semantic_ok"]:
        return {
            **eval0,
            "attempts": [],
            "attempt_count": 0,
            "llm_mode": do_llm,
            "llm_reason": llm_reason,
        }

    attempts: list[dict[str, Any]] = []
    if attempts_cap == 0:
        return {
            **eval0,
            "attempts": [],
            "attempt_count": 0,
            "llm_mode": do_llm,
            "llm_reason": llm_reason,
        }

    for attempt in range(1, attempts_cap + 1):
        att = _one_semantic_attempt(
            vault_root,
            tid,
            card,
            lap=lap,
            attempt=attempt,
            llm_enabled=do_llm,
            nerve_row=nerve_row,
            dry_run=dry_run,
            llm_reason=llm_reason,
        )
        attempts.append(att)
        try:
            card = load_trinity_card(vault_root, tid, prefer="provisional")
        except (OSError, ValueError, FileNotFoundError):
            break
        eval_n = evaluate_semantic_tier(vault_root, card)
        if eval_n["semantic_ok"]:
            append_metric_row(
                vault_root,
                {
                    "metric_type": "corps_semantic_repair_ok",
                    "trinity_id": tid,
                    "lap": lap,
                    "attempt": attempt,
                    "llm_enabled": do_llm,
                    "llm_reason": llm_reason,
                },
            )
            return {
                **eval_n,
                "attempts": attempts,
                "attempt_count": attempt,
                "hard_fail": False,
                "llm_mode": do_llm,
                "llm_reason": llm_reason,
            }

    final = evaluate_semantic_tier(vault_root, card)
    return {
        **final,
        "attempts": attempts,
        "attempt_count": len(attempts),
        "hard_fail": not final["semantic_ok"],
        "llm_mode": do_llm,
        "llm_reason": llm_reason,
    }


def assess_llm_repair_trial(
    vault_root: Path,
    *,
    cluster: str,
    speed_mode: str = "balance",
    dry_run: bool = True,
) -> dict[str, Any]:
    """Preview which provisionals would receive LLM-pack mode under trial rules."""
    from .trinity_provisional_corps_sweep import _resolve_provisional_candidate_ids

    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    ctx = LlmRepairRunContext(
        cluster=cluster,
        speed_mode=speed_mode,
        harness_enable_llm=True,
    )
    raw_ids = _resolve_provisional_candidate_ids(vault_root, cluster=cluster)
    max_per_run = int(getattr(cfg, "corps_llm_repair_trial_max_cards_per_run", 7))

    candidates: list[dict[str, Any]] = []
    for tid in raw_ids:
        would_llm, reason = resolve_llm_mode_for_card(
            vault_root, tid, cfg, ctx, explicit_llm=None
        )
        if would_llm:
            _reserve_trial_card(ctx, tid)
        candidates.append(
            {
                "trinity_id": tid,
                "would_llm": would_llm,
                "reason": reason,
            }
        )
        if ctx.trial_cards_used >= max_per_run and not would_llm:
            if reason == "trial_cap_exhausted":
                continue

    would_count = sum(1 for c in candidates if c.get("would_llm"))
    return {
        "ok": True,
        "dry_run": dry_run,
        "trial_enabled": llm_repair_trial_enabled(cfg),
        "global_enabled": llm_repair_global_enabled(cfg),
        "cluster": cluster,
        "speed_mode": speed_mode,
        "trial_profiles": list(_trial_profiles(cfg)),
        "max_cards_per_run": max_per_run,
        "would_llm_count": would_count,
        "candidates": candidates[:32],
        "run_context": ctx.to_dict(),
    }


def run_llm_repair_trial(
    vault_root: Path,
    *,
    cluster: str,
    speed_mode: str = "balance",
    trinity_id: str | None = None,
    dry_run: bool = False,
    write_artifact: bool = True,
    trial_weaken_id: str | None = None,
    ensure_fixture: bool = False,
    restore_after: bool = False,
) -> dict[str, Any]:
    """Run scoped T1 trial on cluster (or single id) with balance profile gate."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not llm_repair_trial_enabled(cfg) and not llm_repair_global_enabled(cfg):
        return {
            "ok": False,
            "error": "llm_repair_disabled",
            "hint": "Enable trinity_corps_llm_repair_trial_enabled",
        }
    if not cluster:
        return {"ok": False, "error": "cluster_required"}

    ctx = LlmRepairRunContext(
        cluster=cluster,
        speed_mode=speed_mode,
        harness_enable_llm=True,
    )

    fixture_meta: dict[str, Any] = {}
    if ensure_fixture:
        from .corps_semantic_repair_apply import ensure_semantic_trial_fixture

        fixture_meta["ensure_fixture"] = ensure_semantic_trial_fixture(vault_root)
        if not trinity_id:
            trinity_id = "harness_llm_repair_trial"

    weaken_meta: dict[str, Any] | None = None
    if trial_weaken_id:
        from .corps_semantic_repair_apply import weaken_conceptual_for_trial

        weaken_meta = weaken_conceptual_for_trial(vault_root, trial_weaken_id)
        if trinity_id is None:
            trinity_id = trial_weaken_id

    if trinity_id:
        if not card_matches_cluster(trinity_id, cluster):
            return {"ok": False, "error": "outside_cluster", "trinity_id": trinity_id}
        out = poke_semantic_tier_with_repair(
            vault_root,
            trinity_id,
            llm_repair_context=ctx,
            dry_run=dry_run,
        )
        report: dict[str, Any] = {
            "ok": True,
            "trial": True,
            "cluster": cluster,
            "speed_mode": speed_mode,
            "results": [out],
            "run_context": ctx.to_dict(),
            "dry_run": dry_run,
            "fixture_meta": fixture_meta or None,
            "weaken_meta": weaken_meta,
        }
        if restore_after and trial_weaken_id and not dry_run:
            from .corps_semantic_repair_apply import restore_conceptual_from_trial_backup

            report["restore_meta"] = restore_conceptual_from_trial_backup(
                vault_root, trial_weaken_id
            )
    else:
        from .trinity_provisional_corps_sweep import run_nerve_test_batch

        nerve = run_nerve_test_batch(
            vault_root,
            cluster=cluster,
            full_corpus=True,
            lap=1,
            llm_repair_context=ctx,
            dry_run=dry_run,
        )
        report = {
            "ok": bool(nerve.get("ok")),
            "trial": True,
            "cluster": cluster,
            "speed_mode": speed_mode,
            "nerve_test": nerve,
            "run_context": ctx.to_dict(),
            "dry_run": dry_run,
            "fixture_meta": fixture_meta or None,
            "weaken_meta": weaken_meta,
        }
        if restore_after and trial_weaken_id and not dry_run:
            from .corps_semantic_repair_apply import restore_conceptual_from_trial_backup

            report["restore_meta"] = restore_conceptual_from_trial_backup(
                vault_root, trial_weaken_id
            )

    report["generated_at"] = _now_iso()
    if write_artifact and not dry_run:
        ensure_weave_paths(vault_root)
        path = vault_root / ARTIFACT_DIR / f"llm-repair-trial-{_stamp()}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["artifact_path"] = str(path.relative_to(vault_root))

    append_metric_row(
        vault_root,
        {
            "metric_type": "llm_repair_trial_run",
            "cluster": cluster,
            "speed_mode": speed_mode,
            "trial_cards_used": ctx.trial_cards_used,
            "dry_run": dry_run,
        },
    )
    return report
