"""Phase 11a — card identity doctrine on trinity_card_authoring (Grok B)."""

from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .trinity_card import normalize_card
from .trinity_card_paths import META_CARD_ID, load_trinity_card, write_trinity_card
from .trinity_dual_lock import operator_mutation_ctx

PHASE_11A_MARKER = "phase_11a_card_identity_v1"

PHASE_11A_PRECEDENCE: tuple[str, ...] = (
    "policy: One card per responsibility, not per CLI surface.",
    "policy: harness_* is an exception (card_kind harness_entrypoint), not a default.",
    "policy: Same root module in primary_paths → one component card; CLI via touch.harness_commands.",
    "policy: behavior_signals must resolve to def test_* in contract.proof paths.",
    "policy: Merge harness_{cmd} + {module} duplicates → component + harness_commands.",
    "policy: card_kind: component | harness_entrypoint | provisional_bridge | meta.",
)

CARD_KIND_TABLE = """
| card_kind | trinity_id pattern | When |
| --- | --- | --- |
| component | ^[a-z][a-z0-9_]*$ (no harness_ prefix) | One card per module/skill/gauge |
| harness_entrypoint | ^harness_[a-z][a-z0-9_]*$ | CLI slice only when no sibling component |
| provisional_bridge | *_tunnel | D cards; tunnel_via required |
| meta | fixed doctrine ids | trinity_card_authoring, conceptual_style_guide, … |
"""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def doctrine_present_in_card(card: dict[str, Any]) -> tuple[bool, str]:
    """Check A-meta trinity_card_authoring for Phase 11a markers."""
    blob = json.dumps(
        {
            "conceptual": card.get("conceptual"),
            "touch": card.get("touch"),
            "rules": card.get("rules"),
            "meta": card.get("meta"),
        },
        default=str,
    ).lower()
    if PHASE_11A_MARKER in blob:
        return True, "phase_11a_marker"
    markers = ("card_kind", "harness_entrypoint", "one card per", "harness_commands")
    if sum(1 for m in markers if m in blob) >= 3:
        return True, "doctrine_markers"
    return False, "card_kind_doctrine_incomplete"


def load_11a_status(vault_root: Path) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    try:
        card = load_trinity_card(vault_root, META_CARD_ID, prefer="locked")
    except (OSError, ValueError, FileNotFoundError) as e:
        return {"ok": False, "loaded": False, "detail": str(e)}
    present, detail = doctrine_present_in_card(card)
    return {
        "ok": present,
        "loaded": True,
        "detail": detail,
        "trinity_id": META_CARD_ID,
        "path": "components/trinity_card_authoring.yaml",
    }


def apply_card_identity_doctrine(
    vault_root: Path,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Merge Phase 11a precedence into trinity_card_authoring (operator-mutation)."""
    vault_root = vault_root.resolve()
    try:
        card = load_trinity_card(vault_root, META_CARD_ID, prefer="locked")
    except (OSError, ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}

    present, _ = doctrine_present_in_card(card)
    if present:
        return {"ok": True, "skipped": True, "reason": "doctrine_already_present"}

    out = copy.deepcopy(card)
    rules = out.setdefault("rules", {})
    if not isinstance(rules, dict):
        rules = {}
        out["rules"] = rules
    prec = list(rules.get("precedence") or [])
    for line in PHASE_11A_PRECEDENCE:
        if line not in prec:
            prec.append(line)
    rules["precedence"] = prec
    touch = out.setdefault("touch", {})
    if isinstance(touch, dict):
        ref = touch.get("reference_sections") or {}
        if not isinstance(ref, dict):
            ref = {}
        ref["phase_11a_card_kind_table"] = CARD_KIND_TABLE.strip()
        touch["reference_sections"] = ref
    meta = out.setdefault("meta", {})
    if isinstance(meta, dict):
        meta["phase_11a_card_identity"] = PHASE_11A_MARKER
        meta["phase_11a_applied_at"] = _now_iso()

    out = normalize_card(out)
    rec: dict[str, Any] = {
        "ok": True,
        "dry_run": dry_run,
        "trinity_id": META_CARD_ID,
        "precedence_lines_added": len(PHASE_11A_PRECEDENCE),
    }
    if dry_run:
        rec["would_write"] = True
        return rec

    token = operator_mutation_ctx.set(True)
    try:
        path = write_trinity_card(
            vault_root,
            META_CARD_ID,
            out,
            tier="locked",
            mutation_action="phase_11a_card_identity",
            operator_override=True,
        )
    finally:
        operator_mutation_ctx.reset(token)
    rec["path"] = str(path)
    present_after, detail = doctrine_present_in_card(
        load_trinity_card(vault_root, META_CARD_ID, prefer="locked")
    )
    rec["verified"] = present_after
    rec["detail"] = detail
    if not present_after:
        rec["ok"] = False
    return rec
