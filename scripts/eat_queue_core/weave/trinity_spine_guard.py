"""Phase 6 — respects_locked_spine + provisional core recommendations."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .trinity_align import TrinityAlignResult, check, check_pilot_disconnects
from .trinity_card import normalize_card
from .trinity_boundary_audit import run_trinity_boundary_audit
from .trinity_card import get_touch
from .trinity_card_paths import (
    is_provisional_card,
    list_locked_trinity_card_ids,
    load_trinity_card,
)
from .trinity_dual_lock import is_maintenance_core_id

PROVISIONAL_CORE_RECOMMENDATIONS_REL = Path(
    ".technical/weave/provisional-core-recommendations.jsonl"
)

SPINE_VIOLATION_DISCONNECTS = frozenset(
    {
        "precedence_collapse",
        "error_narrative_drift",
        "touch_conceptual_gap",
        "rules_conceptual_gap",
    }
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _normalize_path(p: str) -> str:
    return str(p).strip().replace("\\", "/").lstrip("./")


def _primary_paths(card: dict[str, Any]) -> set[str]:
    touch = get_touch(card)
    raw = touch.get("primary_paths")
    if not isinstance(raw, list):
        return set()
    return {_normalize_path(str(x)) for x in raw if str(x).strip()}


def _tunnel_via(card: dict[str, Any]) -> str:
    touch = get_touch(card)
    for key in ("tunnel_via", "tunnel_target"):
        v = str(touch.get(key) or "").strip()
        if v:
            return v
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    return str(meta.get("tunnel_via") or "").strip()


def _pairs_with(card: dict[str, Any]) -> set[str]:
    touch = get_touch(card)
    raw = touch.get("pairs_with") or touch.get("bridges")
    if not isinstance(raw, list):
        return set()
    return {str(x).strip() for x in raw if str(x).strip()}


def is_harness_shadow_card(trinity_id: str, card: dict[str, Any] | None = None) -> bool:
    """Corps-layer harness_* cards shadow harness modules (Phase 8 retier)."""
    tid = str(trinity_id or (card or {}).get("id") or "").strip()
    return tid.startswith("harness_")


def allows_provisional_primary_path_overlap(
    trinity_id: str,
    peer_core_id: str,
    card: dict[str, Any] | None = None,
) -> bool:
    """Corps provisionals may document the same module path as a locked core (shadow)."""
    tid = str(trinity_id or (card or {}).get("id") or "").strip()
    peer = str(peer_core_id or "").strip()
    if not tid or not peer:
        return False
    if is_harness_shadow_card(tid, card):
        return True
    if tid.endswith("_mapping") and tid.removesuffix("_mapping") == peer:
        return True
    if tid == "pseudo_clock" and peer == "l4_adaptive_policy":
        return True
    meta = (card or {}).get("meta") if isinstance((card or {}).get("meta"), dict) else {}
    if meta.get("card_class") in ("promoted_provisional", "provisional_bridge"):
        if str(meta.get("shadow_of") or "").strip() == peer:
            return True
        pairs = (card or {}).get("touch", {})
        if isinstance(pairs, dict):
            pw = pairs.get("pairs_with") or []
            if peer in [str(x) for x in pw]:
                return True
    return False


@dataclass
class SpineViolation:
    kind: str
    detail: str
    peer_id: str = ""
    paths: list[str] = field(default_factory=list)


@dataclass
class SpineGuardResult:
    ok: bool
    trinity_id: str
    violations: list[SpineViolation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "trinity_id": self.trinity_id,
            "violations": [
                {
                    "kind": v.kind,
                    "detail": v.detail,
                    "peer_id": v.peer_id,
                    "paths": v.paths,
                }
                for v in self.violations
            ],
        }


def _locked_core_cards(vault_root: Path) -> dict[str, dict[str, Any]]:
    """Maintenance core ids with locked component YAML."""
    out: dict[str, dict[str, Any]] = {}
    for tid in list_locked_trinity_card_ids(vault_root):
        if not is_maintenance_core_id(vault_root, tid):
            continue
        try:
            card = load_trinity_card(vault_root, tid, prefer="locked")
            out[tid] = card
        except (OSError, ValueError, FileNotFoundError):
            continue
    return out


def respects_locked_spine(
    vault_root: Path,
    trinity_id: str,
    *,
    card: dict[str, Any] | None = None,
) -> SpineGuardResult:
    """True when a non-core card does not collide with locked maintenance core."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id or "").strip()
    if not tid:
        return SpineGuardResult(ok=False, trinity_id=tid, violations=[
            SpineViolation("missing_id", "trinity_id required"),
        ])

    if is_maintenance_core_id(vault_root, tid):
        return SpineGuardResult(ok=True, trinity_id=tid)

    violations: list[SpineViolation] = []

    if card is not None:
        card = normalize_card(card)
    else:
        try:
            card = load_trinity_card(vault_root, tid)
        except (OSError, ValueError, FileNotFoundError) as e:
            return SpineGuardResult(
                ok=False,
                trinity_id=tid,
                violations=[SpineViolation("card_missing", str(e))],
            )

    core_cards = _locked_core_cards(vault_root)
    my_paths = _primary_paths(card)
    tunnel = _tunnel_via(card)

    for core_tid, core_card in core_cards.items():
        if core_tid == tid:
            continue
        core_paths = _primary_paths(core_card)
        overlap = my_paths & core_paths
        if overlap and not allows_provisional_primary_path_overlap(tid, core_tid, card):
            violations.append(
                SpineViolation(
                    kind="primary_path_overlap_core",
                    detail=f"Shares primary_paths with maintenance core {core_tid}",
                    peer_id=core_tid,
                    paths=sorted(overlap)[:8],
                )
            )
        if tunnel and tunnel == core_tid:
            # Provisional bridge D stubs intentionally tunnel_via orchestrator B
            # (e.g. trinity_spine_maintenance) — not direct corps edits on core A.
            if not is_provisional_bridge_card(card):
                violations.append(
                    SpineViolation(
                        kind="tunnel_via_core",
                        detail=f"tunnel_via points at maintenance core {core_tid}",
                        peer_id=core_tid,
                    )
                )

    pairs = _pairs_with(card)
    for core_tid in core_cards:
        if core_tid in pairs:
            continue
        if pairs & {core_tid}:
            pass

    try:
        audit = run_trinity_boundary_audit(
            vault_root,
            partition="maintenance",
            trinity_ids=[tid],
            write_report=False,
        )
        for row in audit.get("cards") or []:
            if str(row.get("trinity_id")) != tid:
                continue
            for f in row.get("findings") or []:
                if not isinstance(f, dict):
                    continue
                kind = str(f.get("kind") or "")
                sev = str(f.get("severity") or "")
                peer = str(f.get("peer_id") or "")
                if sev in ("error", "warn") and (
                    "collision" in kind
                    or "overlap" in kind
                    or (peer and is_maintenance_core_id(vault_root, peer))
                ):
                    violations.append(
                        SpineViolation(
                            kind=kind,
                            detail=str(f.get("detail") or kind),
                            peer_id=peer,
                            paths=list(f.get("paths") or [])[:8],
                        )
                    )
    except (OSError, ValueError):
        pass

    disconnects = check_pilot_disconnects(
        vault_root, card, run_behavior_proofs=False
    )
    for d in disconnects:
        if d.kind in SPINE_VIOLATION_DISCONNECTS:
            violations.append(
                SpineViolation(
                    kind=f"disconnect_{d.kind}",
                    detail=d.detail or d.kind,
                )
            )

    return SpineGuardResult(ok=not violations, trinity_id=tid, violations=violations)


def assert_respects_locked_spine(
    vault_root: Path,
    trinity_id: str,
    *,
    card: dict[str, Any] | None = None,
) -> None:
    result = respects_locked_spine(vault_root, trinity_id, card=card)
    if result.ok:
        return
    kinds = ", ".join(v.kind for v in result.violations[:4])
    raise ValueError(
        f"respects_locked_spine failed for {trinity_id!r}: {kinds}"
    )


def provisional_core_recommendations_path(vault_root: Path) -> Path:
    return vault_root / PROVISIONAL_CORE_RECOMMENDATIONS_REL


def append_provisional_core_recommendation(
    vault_root: Path,
    *,
    target_trinity_id: str,
    rationale: str,
    suggested_action: str = "operator_review_core",
    disconnect_kinds: list[str] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Advisory JSONL only — never mutates core YAML."""
    vault_root = vault_root.resolve()
    if not is_maintenance_core_id(vault_root, target_trinity_id):
        return {
            "ok": False,
            "error": "not_maintenance_core_id",
            "trinity_id": target_trinity_id,
        }

    row = {
        "timestamp": _now_iso(),
        "target_trinity_id": target_trinity_id,
        "kind": "provisional_core_recommendation",
        "rationale": rationale[:2000],
        "suggested_action": suggested_action,
        "disconnect_kinds": disconnect_kinds or [],
        "consumable": False,
        "promotion": "never",
    }
    if dry_run:
        return {"ok": True, "dry_run": True, "row": row}

    path = provisional_core_recommendations_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return {"ok": True, "path": str(PROVISIONAL_CORE_RECOMMENDATIONS_REL)}


def maybe_recommend_provisional_core(
    vault_root: Path,
    trinity_id: str,
    align: TrinityAlignResult,
    *,
    dry_run: bool = False,
) -> dict[str, Any] | None:
    """Emit recommendation when core align fails for reasons operator must fix."""
    if not is_maintenance_core_id(vault_root, trinity_id):
        return None
    if align.ok and not align.stale_touch:
        return None
    kinds = [d.kind for d in align.disconnects]
    if align.stale_touch and "stale_touch" not in kinds:
        kinds.append("stale_touch")
    if not kinds:
        return None
    if kinds == ["stale_touch"]:
        return None
    rationale = (
        f"Core card {trinity_id} align not clean: "
        + ", ".join(kinds[:6])
        + ". Operator may edit core with trinity_touch_refresh --operator-mutation "
        "or add a provisional bridge tunnel."
    )
    return append_provisional_core_recommendation(
        vault_root,
        target_trinity_id=trinity_id,
        rationale=rationale,
        disconnect_kinds=kinds,
        dry_run=dry_run,
    )


def is_provisional_bridge_card(card: dict[str, Any]) -> bool:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    if str(meta.get("card_class") or "") == "provisional_bridge":
        return True
    if is_provisional_card(card) and _tunnel_via(card):
        return True
    return False


def normalize_provisional_bridge_card(card: dict[str, Any]) -> dict[str, Any]:
    """Ensure tunnel_via / pairs_with / bridge_scope on provisional bridge stubs."""
    from .trinity_card import normalize_card

    out = normalize_card(dict(card))
    meta = out.setdefault("meta", {})
    if not isinstance(meta, dict):
        meta = {}
        out["meta"] = meta
    meta.setdefault("anatomy", "bridge")
    meta.setdefault("provisional", True)
    meta.setdefault("promotion_tier", "provisional")
    meta.setdefault("card_class", "provisional_bridge")
    touch = out.setdefault("touch", {})
    if not isinstance(touch, dict):
        touch = {}
        out["touch"] = touch
    touch.setdefault("bridge_scope", True)
    if touch.get("tunnel_via") and not touch.get("pairs_with"):
        tv = str(touch["tunnel_via"]).strip()
        touch["pairs_with"] = [tv]
    return out
