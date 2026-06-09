"""Trinity alignment — Conceptual / Touch / Rules legs + harness contract (Wave 2.5d v2)."""

from __future__ import annotations

import copy
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import TrinityConfig, load_trinity_config
from .governance import append_metric_row, ensure_weave_paths
from .trinity_card import (
    DISCONNECT_TOUCH_CONCEPTUAL_GAP,
    get_conceptual,
    get_rules,
    get_touch,
    normalize_card,
    rules_forbidden_strings,
    touch_behavior_signals,
    contract_proof_paths,
)
from .trinity_card_paths import write_trinity_card
from .trinity_touch_refresh import (
    _dump_yaml,
    _now_iso,
    build_closure_manifest,
    list_trinity_card_ids,
    load_trinity_card,
)

PILOT_TRINITY_IDS = (
    "lane_status_board",
    "lane_activity",
    "launch_registry_reconcile",
)

PILOT_DISCONNECT_KINDS = frozenset(
    {
        "precedence_collapse",
        "error_narrative_drift",
        "rules_conceptual_gap",
        "touch_conceptual_gap",
        "goal_impetus_gap",
        "touch_impetus_gap",
    }
)

_CODE_SCAN_EXTENSIONS = {".py"}

_FORBIDDEN_CODE_HINTS: dict[str, tuple[str, ...]] = {
    "infer_run_from_receipt": ("infer_run_from_receipt",),
    "receipt tail alone implies run": (
        "infer_run_from_receipt",
        "receipt tail",
    ),
}


@dataclass(frozen=True)
class DisconnectRecord:
    kind: str
    detail: str
    alter_candidates: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "detail": self.detail,
            "alter_candidates": list(self.alter_candidates),
            "evidence": list(self.evidence),
        }


@dataclass
class TrinityAlignResult:
    trinity_id: str
    ok: bool
    stale_touch: bool = False
    legs: dict[str, bool] = field(default_factory=dict)
    disconnects: list[DisconnectRecord] = field(default_factory=list)
    misalignments: list[str] = field(default_factory=list)
    touch_content_hash: str | None = None
    stored_touch_hash: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "trinity_id": self.trinity_id,
            "ok": self.ok,
            "stale_touch": self.stale_touch,
            "legs": dict(self.legs),
            "disconnects": [d.to_dict() for d in self.disconnects],
            "misalignments": list(self.misalignments),
            "touch_content_hash": self.touch_content_hash,
            "stored_touch_hash": self.stored_touch_hash,
            "error": self.error,
        }


def _alter_candidates(card: dict[str, Any], limit: int = 3) -> tuple[str, ...]:
    touch = get_touch(card)
    primary = {str(p).strip() for p in (touch.get("primary_paths") or []) if str(p).strip()}
    inbound = touch.get("inbound") if isinstance(touch.get("inbound"), list) else []
    out: list[str] = []
    for raw in inbound:
        s = str(raw).strip()
        if s and s not in primary and s not in out:
            out.append(s)
        if len(out) >= limit:
            break
    return tuple(out)


def _primary_py_paths(vault_root: Path, card: dict[str, Any]) -> list[Path]:
    touch = get_touch(card)
    paths: list[Path] = []
    for raw in touch.get("primary_paths") or []:
        rel = str(raw).strip()
        if not rel:
            continue
        p = vault_root / rel
        if p.is_file() and p.suffix in _CODE_SCAN_EXTENSIONS:
            paths.append(p)
    return paths


def _forbidden_grep_substrings(card: dict[str, Any]) -> list[str]:
    subs: list[str] = []
    seen: set[str] = set()
    for phrase in rules_forbidden_strings(card):
        subs.extend(_grep_substrings_for_phrase(phrase, seen))
    return subs


def _grep_substrings_for_phrase(phrase: str, seen: set[str] | None = None) -> list[str]:
    """Substrings to grep in primary code for one rules.forbidden phrase."""
    subs: list[str] = []
    local_seen = seen if seen is not None else set()
    pl = str(phrase or "").strip().lower()
    if not pl:
        return subs
    for key, hints in _FORBIDDEN_CODE_HINTS.items():
        if key in pl or pl in key:
            for h in hints:
                if h not in local_seen:
                    local_seen.add(h)
                    subs.append(h)
    if pl not in local_seen:
        local_seen.add(pl)
        subs.append(str(phrase).strip())
    return subs


def forbidden_phrase_hits_primary_code(
    vault_root: Path,
    card: dict[str, Any],
    phrase: str,
) -> bool:
    """True when phrase (or mapped code hints) appears in touch primary_paths .py files."""
    subs = _grep_substrings_for_phrase(phrase)
    if not subs:
        return False
    for py_path in _primary_py_paths(vault_root, card):
        try:
            text = py_path.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        for sub in subs:
            if sub.lower() in text:
                return True
    return False


def reconcile_forbidden_with_primary_code(
    vault_root: Path,
    card: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    """Move rules.forbidden entries that already appear in primary code to precedence.

    Clears ``error_narrative_drift`` without mutating implementation files — Rules leg
    stops claiming code violates patterns that are already present in live modules.
    Returns (updated_card, migrated_phrases).
    """
    out = normalize_card(copy.deepcopy(card))
    rules = out.setdefault("rules", {})
    if not isinstance(rules, dict):
        rules = {}
        out["rules"] = rules
    forbidden_raw = rules.get("forbidden") or []
    if not isinstance(forbidden_raw, list):
        return card, []
    forbidden = [str(x).strip() for x in forbidden_raw if str(x).strip()]
    precedence = list(rules.get("precedence") or [])
    if not isinstance(precedence, list):
        precedence = []

    kept: list[str] = []
    migrated: list[str] = []
    policy_lines: list[str] = []
    for phrase in forbidden:
        if forbidden_phrase_hits_primary_code(vault_root, out, phrase):
            migrated.append(phrase)
            policy_lines.append(
                f"policy: narrative/forbidden — present in primary code (monitor): {phrase}"
            )
        else:
            kept.append(phrase)

    if not migrated:
        return card, []

    seen_prec = {str(x).strip() for x in precedence if str(x).strip()}
    for line in policy_lines:
        if line not in seen_prec:
            precedence.append(line)
            seen_prec.add(line)
    rules["forbidden"] = kept
    rules["precedence"] = precedence
    return out, migrated


def filter_forbidden_list_for_primary_code(
    vault_root: Path,
    card: dict[str, Any],
    forbidden: list[str],
) -> tuple[list[str], list[str]]:
    """Mint-time filter — drop phrases that would immediately trigger narrative drift."""
    kept: list[str] = []
    dropped: list[str] = []
    for phrase in forbidden:
        s = str(phrase).strip()
        if not s:
            continue
        if forbidden_phrase_hits_primary_code(vault_root, card, s):
            dropped.append(s)
        else:
            kept.append(s)
    return kept, dropped


def check_contract_leg(vault_root: Path, card: dict[str, Any]) -> tuple[bool, list[str]]:
    missing: list[str] = []
    for raw in contract_proof_paths(card):
        p = vault_root / raw
        if not p.exists():
            missing.append(raw)
    return len(missing) == 0, missing


def check_goal_leg(vault_root: Path, card: dict[str, Any]) -> tuple[bool, list[str]]:
    """Legacy alias — harness contract proofs."""
    return check_contract_leg(vault_root, card)


def check_conceptual_leg(card: dict[str, Any]) -> tuple[bool, list[str]]:
    conceptual = get_conceptual(card)
    issues: list[str] = []
    if not str(conceptual.get("summary") or "").strip():
        issues.append("conceptual.summary empty")
    if not str(conceptual.get("primary_case") or "").strip():
        issues.append("conceptual.primary_case empty")
    return len(issues) == 0, issues


def check_impetus_leg(card: dict[str, Any]) -> tuple[bool, list[str]]:
    """Legacy alias."""
    return check_conceptual_leg(card)


def check_rules_leg(card: dict[str, Any]) -> tuple[bool, list[str]]:
    rules = get_rules(card)
    issues: list[str] = []
    forbidden = rules.get("forbidden") if isinstance(rules.get("forbidden"), list) else []
    precedence = rules.get("precedence") if isinstance(rules.get("precedence"), list) else []
    if not forbidden and not precedence:
        issues.append("rules.forbidden and rules.precedence both empty")
    return len(issues) == 0, issues


def check_touch_stale(
    vault_root: Path,
    card: dict[str, Any],
    cfg: TrinityConfig,
) -> tuple[bool, str, str]:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    stored = str(meta.get("touch_content_hash") or "").strip() or None
    manifest = build_closure_manifest(
        vault_root,
        card,
        max_hops=cfg.max_closure_hops,
        max_paths=cfg.max_closure_paths,
    )
    fresh = str(manifest.get("touch_content_hash") or "")
    if not stored:
        return False, stored or "", fresh
    return stored != fresh, stored or "", fresh


def _disconnect_precedence_profile(card: dict[str, Any]) -> DisconnectRecord | None:
    rules = get_rules(card)
    forbidden_n = len(rules.get("forbidden") or [])
    tests = sum(1 for s in touch_behavior_signals(card) if s.startswith("test_"))
    if forbidden_n > 0 and forbidden_n > tests:
        return DisconnectRecord(
            kind="precedence_collapse",
            detail=(
                f"rules.forbidden: {forbidden_n} vs {tests} touch guard tests — "
                "forbidden profile dominates conceptual primary_case"
            ),
            alter_candidates=_alter_candidates(card),
            evidence=(f"forbidden_count={forbidden_n}", f"test_count={tests}"),
        )
    return None


def _disconnect_lane_board_legacy_classifier(
    vault_root: Path,
    card: dict[str, Any],
) -> DisconnectRecord | None:
    if str(card.get("id") or "") != "lane_status_board":
        return None
    from ..lane_health_signals import load_lane_board_config

    cfg = load_lane_board_config(vault_root)
    if not cfg.get("use_legacy_classifier"):
        return None
    conceptual = get_conceptual(card)
    primary = str(conceptual.get("primary_case") or "").lower()
    if "lanesnapshot" not in primary and "snapshot" not in primary:
        return None
    return DisconnectRecord(
        kind="precedence_collapse",
        detail=(
            "lane_board.use_legacy_classifier=true conflicts with conceptual primary_case "
            "(LaneSnapshot kernel); legacy classifier must not be primary gate"
        ),
        alter_candidates=_alter_candidates(card),
        evidence=("config:use_legacy_classifier",),
    )


def _disconnect_error_narrative_drift(
    vault_root: Path,
    card: dict[str, Any],
) -> DisconnectRecord | None:
    bans = _forbidden_grep_substrings(card)
    if not bans:
        return None
    hits: list[str] = []
    for py_path in _primary_py_paths(vault_root, card):
        try:
            text = py_path.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        rel = py_path.relative_to(vault_root).as_posix()
        for sub in bans:
            if sub.lower() in text:
                hits.append(f"{rel}: contains '{sub}'")
    if not hits:
        return None
    return DisconnectRecord(
        kind="error_narrative_drift",
        detail="Primary touch code contains forbidden patterns from rules.forbidden",
        alter_candidates=_alter_candidates(card),
        evidence=tuple(hits[:8]),
    )


def _disconnect_lane_activity_receipt_run(card: dict[str, Any], vault_root: Path) -> DisconnectRecord | None:
    if str(card.get("id") or "") != "lane_activity":
        return None
    py_path = vault_root / "scripts/eat_queue_core/lane_activity.py"
    if not py_path.is_file():
        return None
    try:
        text = py_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if re.search(r"receipt.*run_status|run_status.*receipt", text, re.IGNORECASE):
        return DisconnectRecord(
            kind="error_narrative_drift",
            detail="lane_activity.py couples receipt signals to run_status (rules forbid receipt→run)",
            alter_candidates=_alter_candidates(card),
            evidence=(str(py_path.relative_to(vault_root)),),
        )
    return None


def _disconnect_touch_conceptual_gap(
    vault_root: Path,
    card: dict[str, Any],
    *,
    run_proofs: bool,
) -> DisconnectRecord | None:
    """External leg — touch.behavior_signals must pass (system matches Conceptual/Rules)."""
    if not run_proofs:
        return None
    test_names = [s for s in touch_behavior_signals(card) if s.startswith("test_")]
    if not test_names:
        return None
    from .trinity_behavior_proof import run_card_behavior_proofs

    results = run_card_behavior_proofs(vault_root, card)
    failed = [r for r in results if not r.ok]
    if not failed:
        return None
    evidence = tuple(
        f"{r.test_name}: {r.detail or r.target or 'failed'}"[:200] for r in failed[:8]
    )
    return DisconnectRecord(
        kind=DISCONNECT_TOUCH_CONCEPTUAL_GAP,
        detail=(
            f"touch.behavior_signals failed ({len(failed)}/{len(results)}) — "
            "implementation violates Conceptual/Rules contract"
        ),
        alter_candidates=_alter_candidates(card),
        evidence=evidence,
    )


def check_pilot_disconnects(
    vault_root: Path,
    card: dict[str, Any],
    *,
    run_behavior_proofs: bool = True,
) -> list[DisconnectRecord]:
    out: list[DisconnectRecord] = []
    seen_kinds: set[str] = set()

    def add(rec: DisconnectRecord | None) -> None:
        if rec is None or rec.kind in seen_kinds:
            return
        seen_kinds.add(rec.kind)
        out.append(rec)

    add(_disconnect_precedence_profile(card))
    add(_disconnect_lane_board_legacy_classifier(vault_root, card))
    add(_disconnect_error_narrative_drift(vault_root, card))
    add(_disconnect_lane_activity_receipt_run(card, vault_root))
    add(_disconnect_touch_conceptual_gap(vault_root, card, run_proofs=run_behavior_proofs))
    return out


def _sync_stored_touch_hash(vault_root: Path, trinity_id: str, cfg: TrinityConfig) -> None:
    """Persist closure manifest hash after volatile neighbors (e.g. metrics.jsonl) changed."""
    card = load_trinity_card(vault_root, trinity_id)
    manifest = build_closure_manifest(
        vault_root,
        card,
        max_hops=cfg.max_closure_hops,
        max_paths=cfg.max_closure_paths,
    )
    meta = card.setdefault("meta", {})
    if isinstance(meta, dict):
        meta["touch_content_hash"] = manifest["touch_content_hash"]
        meta["touch_refreshed_at"] = _now_iso()
        meta["closure_must_read_count"] = len(manifest["must_read"])
    write_trinity_card(
        vault_root,
        trinity_id,
        card,
        mutation_action="gate_hash_reconcile",
    )


def check(
    vault_root: Path,
    trinity_id: str,
    *,
    run_behavior_proofs: bool | None = None,
) -> TrinityAlignResult:
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    try:
        card = normalize_card(load_trinity_card(vault_root, trinity_id))
    except (OSError, ValueError, FileNotFoundError) as e:
        return TrinityAlignResult(trinity_id=trinity_id, ok=False, error=str(e))

    contract_ok, contract_missing = check_contract_leg(vault_root, card)
    conceptual_ok, conceptual_issues = check_conceptual_leg(card)
    rules_ok, rules_issues = check_rules_leg(card)
    stale, stored_hash, fresh_hash = check_touch_stale(vault_root, card, cfg)
    if run_behavior_proofs is None:
        run_proofs = bool(cfg.enabled and cfg.run_behavior_proofs)
    else:
        run_proofs = run_behavior_proofs
    disconnects = check_pilot_disconnects(
        vault_root,
        card,
        run_behavior_proofs=run_proofs,
    )
    external_proof_ok = not any(
        d.kind == DISCONNECT_TOUCH_CONCEPTUAL_GAP for d in disconnects
    )

    legs = {
        "conceptual": conceptual_ok,
        "rules": rules_ok,
        "contract": contract_ok,
        "touch_fresh": not stale,
        "external_proof": external_proof_ok,
    }
    misalignments: list[str] = []
    if contract_missing:
        misalignments.append(f"contract proof missing: {', '.join(contract_missing[:6])}")
    misalignments.extend(conceptual_issues)
    misalignments.extend(rules_issues)

    ok = (
        contract_ok
        and conceptual_ok
        and rules_ok
        and not stale
        and external_proof_ok
        and len(disconnects) == 0
    )
    return TrinityAlignResult(
        trinity_id=trinity_id,
        ok=ok,
        stale_touch=stale,
        legs=legs,
        disconnects=disconnects,
        misalignments=misalignments,
        touch_content_hash=fresh_hash,
        stored_touch_hash=stored_hash or None,
    )


def _persist_last_disconnect(
    vault_root: Path,
    trinity_id: str,
    disconnects: list[DisconnectRecord],
) -> None:
    card = load_trinity_card(vault_root, trinity_id)
    meta = card.setdefault("meta", {})
    if not isinstance(meta, dict):
        meta = {}
        card["meta"] = meta
    if disconnects:
        meta["last_disconnect"] = disconnects[0].to_dict()
    else:
        meta["last_disconnect"] = None
    write_trinity_card(vault_root, trinity_id, card)


def _append_align_metrics(vault_root: Path, result: TrinityAlignResult) -> None:
    kinds = Counter(d.kind for d in result.disconnects)
    append_metric_row(
        vault_root,
        {
            "metric_type": "trinity_align",
            "event": "trinity_align",
            "trinity_id": result.trinity_id,
            "ok": result.ok,
            "stale_touch": result.stale_touch,
            "disconnect_count": len(result.disconnects),
            "trinity_disconnect_by_kind": dict(kinds),
            "trinity_cards_stale_count": 1 if result.stale_touch else 0,
            "trinity_disconnect_rate": (
                float(len(result.disconnects)) if result.disconnects else 0.0
            ),
            "legs": result.legs,
        },
    )
    for d in result.disconnects:
        append_metric_row(
            vault_root,
            {
                "metric_type": "trinity_disconnect",
                "event": "trinity_disconnect",
                "trinity_id": result.trinity_id,
                "kind": d.kind,
                "detail": d.detail,
                "alter_candidates": list(d.alter_candidates),
            },
        )


def apply_trinity_align_gate(
    vault_root: Path,
    trinity_id: str,
    *,
    update_meta: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled or not cfg.checks_enabled:
        return {"ok": True, "skipped": True, "checks_enabled": False}

    from .trinity_dual_lock import is_maintenance_core_id

    core_readonly = is_maintenance_core_id(vault_root, trinity_id)

    result = check(vault_root, trinity_id)
    ensure_weave_paths(vault_root)
    if update_meta and not core_readonly:
        from .trinity_spine_guard import respects_locked_spine

        spine = respects_locked_spine(vault_root, trinity_id)
        if spine.ok:
            try:
                _persist_last_disconnect(vault_root, trinity_id, result.disconnects)
            except (OSError, ValueError):
                pass
    _append_align_metrics(vault_root, result)

    # metrics.jsonl is often in touch closure — re-hash stale-only rows (same as run_trinity_align).
    # Core: allow hash-only reconciliation after metrics (gate churn), not general touch refresh.
    if result.stale_touch and not result.disconnects:
        try:
            _sync_stored_touch_hash(vault_root, trinity_id, cfg)
            result = check(vault_root, trinity_id, run_behavior_proofs=False)
            if update_meta and not core_readonly:
                try:
                    _persist_last_disconnect(vault_root, trinity_id, result.disconnects)
                except (OSError, ValueError):
                    pass
        except (OSError, ValueError):
            pass

    blocked = False
    if result.stale_touch and cfg.block_on_stale_touch:
        blocked = True
    if result.disconnects and cfg.block_on_disconnect:
        blocked = True
    for leg in ("conceptual", "rules", "contract", "external_proof"):
        if not result.legs.get(leg, True):
            blocked = True

    gate_ok = result.ok and not blocked
    detail_parts: list[str] = []
    if result.stale_touch:
        detail_parts.append("stale_touch")
    if result.disconnects:
        detail_parts.append(
            "disconnect: " + ", ".join(d.kind for d in result.disconnects)
        )
    if result.misalignments:
        detail_parts.append("; ".join(result.misalignments[:4]))

    return {
        "ok": gate_ok,
        "skipped": False,
        "blocked": blocked,
        "detail": "; ".join(detail_parts) if detail_parts else "trinity align ok",
        "align": result.to_dict(),
        "disconnect_count": len(result.disconnects),
        "stale_touch": result.stale_touch,
    }


def check_spine_bridge_status(vault_root: Path) -> dict[str, Any]:
    """Advisory align on corpus bridge only (Phase 2 — not merged into handler bone)."""
    vault_root = vault_root.resolve()
    try:
        from .trinity_partition import load_maintenance_trinity_ids

        bridges = load_maintenance_trinity_ids(vault_root).bridges
    except (FileNotFoundError, OSError, ValueError):
        return {"ok": True, "skipped": True, "reason": "partition_registry_missing"}

    if not bridges:
        return {"ok": True, "skipped": True, "reason": "no_bridge_ids"}

    bid = bridges[0]
    result = check(vault_root, bid, run_behavior_proofs=False)
    summary = {
        "ok": result.ok,
        "trinity_id": bid,
        "stale_touch": result.stale_touch,
        "disconnects": [d.kind for d in result.disconnects],
        "legs": result.legs,
    }
    try:
        append_metric_row(
            vault_root,
            {"metric_type": "spine_bridge_status", **summary},
        )
    except OSError:
        pass
    return summary


def apply_maintenance_trinity_align_gate(
    vault_root: Path,
    *,
    update_meta: bool = True,
) -> dict[str, Any]:
    """Phase 2 gate — maintenance partition (bones + bridges) must align on board refresh."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled or not cfg.checks_enabled:
        return {"ok": True, "skipped": True, "checks_enabled": False}

    try:
        from .trinity_partition import load_maintenance_trinity_ids

        ids = list(load_maintenance_trinity_ids(vault_root).all)
    except (FileNotFoundError, OSError, ValueError) as e:
        return {
            "ok": False,
            "skipped": False,
            "blocked": True,
            "detail": f"maintenance_partition: {e}",
            "maintenance_results": [],
            "checks_enabled": True,
        }

    maint_results: list[dict[str, Any]] = []
    blocked = False
    bone_failures: list[str] = []
    bridge_failures: list[str] = []
    try:
        from .trinity_partition import load_partition_registry

        reg = load_partition_registry(vault_root)
    except (FileNotFoundError, OSError, ValueError):
        reg = None

    for tid in ids:
        gate = apply_trinity_align_gate(vault_root, tid, update_meta=update_meta)
        maint_results.append({"trinity_id": tid, **gate})
        if gate.get("blocked") or not gate.get("ok", True):
            blocked = True
            if reg and reg.anatomy_for(tid) == "bridge":
                bridge_failures.append(tid)
            else:
                bone_failures.append(tid)

    detail_parts: list[str] = []
    if bone_failures:
        detail_parts.append("bones: " + ", ".join(bone_failures[:6]))
    if bridge_failures:
        detail_parts.append("bridges: " + ", ".join(bridge_failures[:4]))
    if not detail_parts:
        for row in maint_results:
            if not row.get("ok", True) and not row.get("skipped"):
                detail_parts.append(f"{row['trinity_id']}: {row.get('detail') or 'align failed'}")

    return {
        "ok": not blocked,
        "skipped": False,
        "blocked": blocked,
        "detail": "; ".join(detail_parts) if detail_parts else "maintenance trinity align ok",
        "maintenance_results": maint_results,
        "bone_failures": bone_failures,
        "bridge_failures": bridge_failures,
        "checks_enabled": True,
        "profile": "maintenance_set",
    }


def apply_pilot_trinity_align_gate(
    vault_root: Path,
    *,
    update_meta: bool = True,
) -> dict[str, Any]:
    """P2 gate — all pilot operator-surface cards must align (incl. external proof)."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled or not cfg.checks_enabled:
        return {"ok": True, "skipped": True, "checks_enabled": False}

    pilot_results: list[dict[str, Any]] = []
    blocked = False
    for tid in PILOT_TRINITY_IDS:
        gate = apply_trinity_align_gate(vault_root, tid, update_meta=update_meta)
        pilot_results.append({"trinity_id": tid, **gate})
        if gate.get("blocked") or not gate.get("ok", True):
            blocked = True

    detail_parts: list[str] = []
    for row in pilot_results:
        if row.get("skipped"):
            continue
        if not row.get("ok", True):
            detail_parts.append(f"{row['trinity_id']}: {row.get('detail') or 'align failed'}")

    return {
        "ok": not blocked,
        "skipped": False,
        "blocked": blocked,
        "detail": "; ".join(detail_parts) if detail_parts else "pilot trinity align ok",
        "pilot_results": pilot_results,
        "checks_enabled": True,
    }


def run_trinity_align(
    vault_root: Path,
    *,
    trinity_ids: list[str] | None = None,
    pilot_only: bool = True,
    update_meta: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled:
        return {"ok": True, "skipped": True, "reason": "trinity_disabled"}

    from .trinity_dual_lock import is_maintenance_core_id

    ids = trinity_ids or list_trinity_card_ids(vault_root, pilot_only=pilot_only)
    results: list[dict[str, Any]] = []
    any_fail = False
    for tid in ids:
        r = check(vault_root, tid)
        core_readonly = is_maintenance_core_id(vault_root, tid)
        if update_meta and not core_readonly:
            try:
                _persist_last_disconnect(vault_root, tid, r.disconnects)
            except (OSError, ValueError):
                pass
        _append_align_metrics(vault_root, r)
        results.append(r.to_dict())
        if not r.ok:
            any_fail = True

    # Align metrics append updates metrics.jsonl — often in touch closure; re-hash stale-only rows.
    for i, tid in enumerate(ids):
        rdict = results[i]
        if not rdict.get("stale_touch") or rdict.get("disconnects"):
            continue
        if is_maintenance_core_id(vault_root, tid):
            continue
        try:
            _sync_stored_touch_hash(vault_root, tid, cfg)
            r2 = check(vault_root, tid, run_behavior_proofs=False)
            if update_meta:
                try:
                    _persist_last_disconnect(vault_root, tid, r2.disconnects)
                except (OSError, ValueError):
                    pass
            results[i] = r2.to_dict()
        except (OSError, ValueError):
            pass

    any_fail = any(not row.get("ok") for row in results)

    return {
        "ok": not any_fail,
        "checked": len(ids),
        "results": results,
        "checks_enabled": cfg.checks_enabled,
    }
