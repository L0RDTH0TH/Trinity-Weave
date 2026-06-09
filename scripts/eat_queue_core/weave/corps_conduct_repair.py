"""Phase 10d — intent-conduct repair: sync behavior_signals and wire proof paths.

Fixes conduct-tier reds (touch_conceptual_gap) without green-washing via import-only
smoke tests. Routes stale or missing behavior_signal names to discovered proof tests.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .corps_repair_audit import audit_card_repair
from .corps_smoke_test import ensure_smoke_test_file
from .governance import append_metric_row
from .trinity_behavior_proof import (
    find_test_file_for_signal,
    find_unittest_target,
    run_card_behavior_proofs,
)
from .trinity_card import get_touch
from .trinity_card_paths import load_trinity_card, write_trinity_card
from .trinity_dual_lock import corps_repair_skip_reason
from .trinity_provisional_corps_sweep import _wire_tests_if_missing
from .trinity_spine_guard import respects_locked_spine
from .trinity_touch_refresh import merge_behavior_signals, propose_behavior_signals


def behavior_signal_resolves(
    vault_root: Path,
    card: dict[str, Any],
    signal: str,
) -> bool:
    """True when signal maps to a def test_* in linked proof paths."""
    name = str(signal).strip()
    if not name.startswith("test_"):
        return False
    if find_test_file_for_signal(vault_root, card, name):
        return True
    return find_unittest_target(vault_root, card, name) is not None


def prune_unresolved_behavior_signals(
    vault_root: Path,
    card: dict[str, Any],
) -> tuple[dict[str, Any], bool, list[str]]:
    """Drop behavior_signals that do not resolve to a proof test (respect locked)."""
    touch = get_touch(card)
    locked = {str(x).strip() for x in (touch.get("locked_behavior_signals") or []) if str(x).strip()}
    existing = [str(x).strip() for x in (touch.get("behavior_signals") or []) if str(x).strip()]
    kept: list[str] = []
    dropped: list[str] = []
    for sig in existing:
        if sig in locked:
            kept.append(sig)
            continue
        if behavior_signal_resolves(vault_root, card, sig):
            kept.append(sig)
        else:
            dropped.append(sig)
    if kept == existing:
        return card, False, []
    out = copy.deepcopy(card)
    out.setdefault("touch", {})["behavior_signals"] = kept
    return out, True, dropped


def sync_behavior_signals_from_proofs(
    vault_root: Path,
    card: dict[str, Any],
    *,
    apply: bool = True,
) -> tuple[dict[str, Any], bool, list[str]]:
    """Merge proposed proof test names into touch.behavior_signals."""
    touch = get_touch(card)
    locked = list(touch.get("locked_behavior_signals") or [])
    existing = list(touch.get("behavior_signals") or [])
    proposed = propose_behavior_signals(vault_root, card)
    merged, new_only = merge_behavior_signals(
        existing,
        locked,
        proposed,
        apply_proposed=apply,
    )
    if merged == existing:
        return card, False, []
    out = copy.deepcopy(card)
    out.setdefault("touch", {})["behavior_signals"] = merged
    return out, True, new_only


def repair_conduct_card(
    vault_root: Path,
    trinity_id: str,
    *,
    nerve_row: dict[str, Any] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """10d conduct repair for one provisional card."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    rec: dict[str, Any] = {"trinity_id": tid, "applied": [], "changed": False}

    skip = corps_repair_skip_reason(vault_root, tid)
    if skip:
        rec["skipped"] = skip
        return rec

    guard = respects_locked_spine(vault_root, tid)
    if not guard.ok:
        rec["skipped"] = "respects_locked_spine"
        rec["violations"] = [v.kind for v in guard.violations][:6]
        return rec

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError) as e:
        rec["error"] = str(e)
        return rec

    working = copy.deepcopy(card)

    for raw_path in get_touch(working).get("primary_paths") or []:
        ensure_smoke_test_file(vault_root, str(raw_path))
    working = _wire_tests_if_missing(vault_root, working)
    rec["applied"].append("wire_smoke_tests")

    working, pruned, dropped = prune_unresolved_behavior_signals(vault_root, working)
    if pruned:
        rec["applied"].append("prune_unresolved_behavior_signals")
        rec["dropped_behavior_signals"] = dropped[:16]

    working, synced, new_sigs = sync_behavior_signals_from_proofs(
        vault_root,
        working,
        apply=True,
    )
    if synced:
        rec["applied"].append("sync_behavior_signals")
        rec["new_behavior_signals"] = new_sigs[:12]

    changed = working != card
    rec["changed"] = changed
    if changed and not dry_run:
        try:
            write_trinity_card(vault_root, tid, working, tier="provisional")
            working = load_trinity_card(vault_root, tid, prefer="provisional")
        except (OSError, ValueError) as e:
            rec["write_error"] = str(e)
            rec["changed"] = False
            append_metric_row(
                vault_root,
                {
                    "metric_type": "corps_conduct_repair_write_failed",
                    "trinity_id": tid,
                    "error": str(e)[:400],
                },
            )
            return rec

    proofs = run_card_behavior_proofs(vault_root, working)
    rec["proof_results"] = [p.to_dict() for p in proofs]
    rec["proofs_ok"] = all(p.ok for p in proofs) if proofs else True
    rec["proofs_failed"] = [p.test_name for p in proofs if not p.ok][:8]

    conduct = (nerve_row or {}).get("conduct") or {}
    rec["prior_disconnects"] = list(conduct.get("disconnects") or [])[:6]
    if changed or rec.get("dropped_behavior_signals"):
        audit_card_repair(
            vault_root,
            trinity_id=tid,
            repair_type="conduct_10d",
            disconnect_kind="touch_conceptual_gap",
            before_card=card,
            after_card=working if changed else None,
            changed=changed,
            extra={
                "proofs_ok": rec.get("proofs_ok"),
                "dropped_signals": (rec.get("dropped_behavior_signals") or [])[:8],
            },
        )
    return rec


def _route_conduct_only(tid: str, nerve_row: dict[str, Any] | None) -> bool:
    """True when card is conduct-tier red only (shape/spine/semantic already green)."""
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


def run_corps_conduct_repair_batch(
    vault_root: Path,
    *,
    red_ids: list[str],
    nerves_by_id: dict[str, dict[str, Any]] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Repair conduct-tier reds; returns counts for lap termination."""
    cfg = load_trinity_config(vault_root)
    if not getattr(cfg, "corps_conduct_repair_enabled", True):
        return {
            "ok": True,
            "skipped": True,
            "reason": "corps_conduct_repair_disabled",
            "attempted": 0,
            "changed_count": 0,
            "repairs": [],
        }

    repairs: list[dict[str, Any]] = []
    changed = 0
    for tid in red_ids:
        row = (nerves_by_id or {}).get(tid)
        if not _route_conduct_only(tid, row):
            continue
        rec = repair_conduct_card(
            vault_root,
            tid,
            nerve_row=row,
            dry_run=dry_run,
        )
        repairs.append(rec)
        if rec.get("changed"):
            changed += 1

    append_metric_row(
        vault_root,
        {
            "metric_type": "corps_conduct_repair_batch",
            "attempted": len(repairs),
            "changed_count": changed,
        },
    )
    return {
        "ok": True,
        "attempted": len(repairs),
        "changed_count": changed,
        "repairs": repairs,
    }
