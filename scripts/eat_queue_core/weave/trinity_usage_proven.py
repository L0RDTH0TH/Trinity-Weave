"""Phase 15 — usage_proven earned freeze (pseudo-clock or explicit harness stamp)."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from ..lane_board_drilldown import append_maintenance_decision
from .config import load_trinity_config
from .corps_repair_audit import corps_repair_audit_path
from .governance import append_metric_row, ensure_weave_paths
from .trinity_card_backlog import count_trinity_usage
from .trinity_card_paths import (
    component_proposals_dir,
    components_dir,
    load_trinity_card,
    list_provisional_trinity_card_ids,
    write_trinity_card,
)
from .trinity_dual_lock import (
    apply_usage_proven_to_card,
    is_consumable_for_pack,
    is_maintenance_core_id,
    is_usage_proven_id,
    lock_kind_from_card,
)
from .trinity_provisional_corps_sweep import load_corps_nerve_map, run_nerve_test_one

STREAK_REL = Path(".technical/weave/usage-proven-streak.json")
ARTIFACT_DIR = Path(".technical/weave/validation")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def streak_path(vault_root: Path) -> Path:
    return vault_root.resolve() / STREAK_REL


def load_streak_state(vault_root: Path) -> dict[str, Any]:
    path = streak_path(vault_root)
    if not path.is_file():
        return {"cards": {}}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"cards": {}}
    if not isinstance(raw, dict):
        return {"cards": {}}
    if "cards" not in raw or not isinstance(raw["cards"], dict):
        raw["cards"] = {}
    return raw


def save_streak_state(vault_root: Path, state: dict[str, Any]) -> None:
    path = streak_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = _now_iso()
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _nerve_conduct_ok(vault_root: Path, trinity_id: str) -> bool | None:
    nmap = load_corps_nerve_map(vault_root)
    for row in nmap.get("nerves") or []:
        if isinstance(row, dict) and row.get("trinity_id") == trinity_id:
            tier = row.get("tier") or {}
            if row.get("status") == "green":
                return bool(tier.get("conduct_ok", True))
            if row.get("status") == "red":
                return False
            return None
    row = run_nerve_test_one(vault_root, trinity_id, dry_run=True)
    tier = row.get("tier") or {}
    if row.get("status") == "green":
        return bool(tier.get("conduct_ok", True))
    if row.get("status") == "red":
        return False
    return None


def update_streak_for_card(vault_root: Path, trinity_id: str, *, conduct_ok: bool | None) -> dict[str, Any]:
    state = load_streak_state(vault_root)
    cards = state.setdefault("cards", {})
    prev = cards.get(trinity_id) if isinstance(cards.get(trinity_id), dict) else {}
    streak = int(prev.get("green_streak") or 0)
    if conduct_ok is True:
        streak += 1
    elif conduct_ok is False:
        streak = 0
    entry = {
        "green_streak": streak,
        "last_conduct_ok": conduct_ok,
        "last_updated": _now_iso(),
    }
    cards[trinity_id] = entry
    save_streak_state(vault_root, state)
    return entry


def has_recent_repair_failure(
    vault_root: Path,
    trinity_id: str,
    *,
    lookback_days: int = 14,
) -> bool:
    path = corps_repair_audit_path(vault_root)
    if not path.is_file():
        return False
    cutoff = datetime.now(timezone.utc) - timedelta(days=max(1, lookback_days))
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[-400:]:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if str(row.get("trinity_id") or "") != trinity_id:
            continue
        if row.get("event") not in ("corps_repair", "conduct_repair_apply_10g"):
            continue
        if row.get("proofs_ok") is False or row.get("changed") is True:
            ts_raw = str(row.get("ts") or row.get("at") or "")
            try:
                ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            except ValueError:
                continue
            if ts >= cutoff:
                return True
    return False


def is_eligible_lock_kind(card: dict[str, Any], *, vault_root: Path, trinity_id: str) -> tuple[bool, str]:
    if is_maintenance_core_id(vault_root, trinity_id):
        return False, "maintenance_core"
    kind = lock_kind_from_card(card)
    if kind == "usage_proven":
        return False, "already_usage_proven"
    if kind in ("full", "conceptual_spine"):
        return False, f"ineligible_lock_kind:{kind}"
    if kind == "maintenance_core":
        return False, "maintenance_core"
    return True, "eligible"


def evaluate_usage_proven_candidacy(
    vault_root: Path,
    trinity_id: str,
    *,
    update_streak: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    tid = str(trinity_id).strip()

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError):
        try:
            card = load_trinity_card(vault_root, tid, prefer="locked")
        except (OSError, ValueError, FileNotFoundError) as e:
            return {"ok": False, "trinity_id": tid, "error": str(e)}

    eligible, reason = is_eligible_lock_kind(card, vault_root=vault_root, trinity_id=tid)
    if not eligible:
        return {"ok": True, "trinity_id": tid, "eligible": False, "reason": reason}

    lookback = int(getattr(cfg, "usage_proven_lookback_days", 30))
    min_usage = int(getattr(cfg, "usage_proven_min_usage_count", 3))
    min_streak = int(getattr(cfg, "usage_proven_min_green_streak", 3))

    usage_counts = count_trinity_usage(vault_root, lookback_days=lookback)
    usage_count = int(usage_counts.get(tid, 0))
    config_bound = is_consumable_for_pack(vault_root, tid) and usage_count >= min_usage

    conduct_ok = _nerve_conduct_ok(vault_root, tid)
    streak_entry = (
        update_streak_for_card(vault_root, tid, conduct_ok=conduct_ok)
        if update_streak
        else (load_streak_state(vault_root).get("cards") or {}).get(tid, {})
    )
    green_streak = int(streak_entry.get("green_streak") or 0)
    repair_fail = has_recent_repair_failure(vault_root, tid, lookback_days=lookback)

    ready = (
        config_bound
        and conduct_ok is True
        and green_streak >= min_streak
        and not repair_fail
    )

    return {
        "ok": True,
        "trinity_id": tid,
        "eligible": True,
        "ready_to_stamp": ready,
        "usage_count": usage_count,
        "config_bound": config_bound,
        "conduct_ok": conduct_ok,
        "green_streak": green_streak,
        "min_usage": min_usage,
        "min_streak": min_streak,
        "recent_repair_failure": repair_fail,
    }


def stamp_usage_proven(
    vault_root: Path,
    trinity_id: str,
    *,
    evidence: dict[str, Any] | None = None,
    dry_run: bool = False,
    operator_force: bool = False,
) -> dict[str, Any]:
    """Stamp usage_proven on eligible card; moves provisional → components/."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    eval_out = evaluate_usage_proven_candidacy(vault_root, tid, update_streak=False)

    if not eval_out.get("eligible"):
        return {"ok": False, "trinity_id": tid, "error": eval_out.get("reason", "ineligible")}
    if not operator_force and not eval_out.get("ready_to_stamp"):
        return {
            "ok": False,
            "trinity_id": tid,
            "error": "criteria_not_met",
            "evaluation": eval_out,
        }

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
        tier = "provisional"
    except (OSError, ValueError, FileNotFoundError):
        card = load_trinity_card(vault_root, tid, prefer="locked")
        tier = "locked"

    ev = dict(evidence or {})
    ev.setdefault("evaluation", eval_out)
    ev.setdefault("stamped_by", "operator_force" if operator_force else "criteria_met")

    stamped = apply_usage_proven_to_card(card, evidence=ev, now_iso=_now_iso())

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "trinity_id": tid,
            "would_tier": "locked",
            "evaluation": eval_out,
        }

    write_trinity_card(
        vault_root,
        tid,
        stamped,
        tier="locked",
        mutation_action="stamp_usage_proven",
        operator_override=True,
    )
    prov_path = component_proposals_dir(vault_root) / f"{tid}.yaml"
    if tier == "provisional" and prov_path.is_file():
        prov_path.unlink()

    append_metric_row(
        vault_root,
        {
            "metric_type": "usage_proven_stamped",
            "trinity_id": tid,
            "usage_count": eval_out.get("usage_count"),
            "green_streak": eval_out.get("green_streak"),
        },
    )
    append_maintenance_decision(
        vault_root,
        event="usage_proven_stamped",
        lane="maintenance",
        detail=f"trinity_id={tid} streak={eval_out.get('green_streak')} usage={eval_out.get('usage_count')}",
    )

    return {
        "ok": True,
        "trinity_id": tid,
        "stamped": True,
        "path": str((components_dir(vault_root) / f"{tid}.yaml").relative_to(vault_root)),
        "evaluation": eval_out,
    }


def unfreeze_usage_proven(
    vault_root: Path,
    trinity_id: str,
    *,
    dry_run: bool = False,
    operator_override: bool = True,
) -> dict[str, Any]:
    """Operator explicit unfreeze — revert lock_kind to provisional in components."""
    tid = str(trinity_id).strip()
    if not is_usage_proven_id(vault_root, tid):
        return {"ok": False, "error": "not_usage_proven", "trinity_id": tid}
    card = load_trinity_card(vault_root, tid, prefer="locked")
    meta = dict(card.get("meta") or {})
    meta.pop("lock_kind", None)
    meta["system_mutable"] = True
    meta["usage_proven_unfrozen_at"] = _now_iso()
    meta.pop("usage_proven_at", None)
    meta.pop("usage_proven_evidence", None)
    card["meta"] = meta
    if dry_run:
        return {"ok": True, "dry_run": True, "trinity_id": tid}
    write_trinity_card(
        vault_root,
        tid,
        card,
        tier="locked",
        mutation_action="unfreeze_usage_proven",
        operator_override=operator_override,
    )
    append_maintenance_decision(
        vault_root,
        event="usage_proven_unfrozen",
        lane="maintenance",
        detail=f"trinity_id={tid}",
    )
    return {"ok": True, "trinity_id": tid, "unfrozen": True}


def assess_usage_proven_batch(
    vault_root: Path,
    *,
    trinity_ids: list[str] | None = None,
    stamp_ready: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    ids = trinity_ids or list_provisional_trinity_card_ids(vault_root)
    candidates: list[dict[str, Any]] = []
    stamped: list[str] = []
    for tid in ids:
        if is_usage_proven_id(vault_root, tid):
            continue
        ev = evaluate_usage_proven_candidacy(vault_root, tid)
        candidates.append(ev)
        if stamp_ready and ev.get("ready_to_stamp") and not dry_run:
            out = stamp_usage_proven(vault_root, tid, evidence={"source": "assess_batch"})
            if out.get("ok") and out.get("stamped"):
                stamped.append(tid)

    ready = [c for c in candidates if c.get("ready_to_stamp")]
    return {
        "ok": True,
        "assessed": len(candidates),
        "ready_count": len(ready),
        "stamped": stamped,
        "candidates": candidates,
        "dry_run": dry_run,
    }


def maybe_usage_proven_on_pseudo_clock(vault_root: Path) -> dict[str, Any] | None:
    """Pseudo-clock hook — evaluate streaks; stamp when criteria met."""
    cfg = load_trinity_config(vault_root)
    if not getattr(cfg, "usage_proven_on_pseudo_clock", False):
        return None
    if not cfg.enabled:
        return None
    return assess_usage_proven_batch(vault_root, stamp_ready=True, dry_run=False)


def run_usage_proven_report(
    vault_root: Path,
    *,
    write_artifact: bool = True,
) -> dict[str, Any]:
    report = assess_usage_proven_batch(vault_root, stamp_ready=False, dry_run=True)
    report["generated_at"] = _now_iso()
    if write_artifact:
        ensure_weave_paths(vault_root)
        out = vault_root / ARTIFACT_DIR / f"usage-proven-assess-{_stamp()}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["artifact_path"] = str(out.relative_to(vault_root))
    return report
