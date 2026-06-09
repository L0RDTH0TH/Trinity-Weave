"""Trinity card schema helpers — Conceptual / Touch / Rules (+ harness contract).

Cards describe **weave code sections** (components), not project lanes.
Schema v2: conceptual, touch, rules, contract; legacy goal/impetus normalized in memory.
"""

from __future__ import annotations

from typing import Any

SCHEMA_VERSION = 2

DISCONNECT_RULES_CONCEPTUAL_GAP = "rules_conceptual_gap"
DISCONNECT_TOUCH_CONCEPTUAL_GAP = "touch_conceptual_gap"
# Legacy metric names (pre-v2)
DISCONNECT_GOAL_IMPETUS_GAP = "goal_impetus_gap"
DISCONNECT_TOUCH_IMPETUS_GAP = "touch_impetus_gap"


def _as_dict(raw: Any) -> dict[str, Any]:
    return raw if isinstance(raw, dict) else {}


def _as_str_list(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    return [str(x).strip() for x in raw if str(x).strip()]


def get_conceptual(card: dict[str, Any]) -> dict[str, Any]:
    if "conceptual" in card:
        return _as_dict(card["conceptual"])
    impetus = _as_dict(card.get("impetus"))
    goal = _as_dict(card.get("goal"))
    out = dict(impetus)
    if goal.get("invariant") and not out.get("outcome"):
        out["outcome"] = goal.get("invariant")
    return out


def get_rules(card: dict[str, Any]) -> dict[str, Any]:
    if "rules" in card:
        return _as_dict(card["rules"])
    goal = _as_dict(card.get("goal"))
    touch = _as_dict(card.get("touch"))
    forbidden: list[str] = []
    for sig in _as_str_list(touch.get("behavior_signals")):
        if sig.lower().startswith("forbidden:"):
            forbidden.append(sig.split(":", 1)[1].strip())
    return {
        "forbidden": forbidden,
        "fixtures": [],
        "precedence": _as_str_list(goal.get("precedence_clauses")),
        "acceptance": _as_str_list(goal.get("acceptance")),
    }


def get_contract(card: dict[str, Any]) -> dict[str, Any]:
    if "contract" in card:
        return _as_dict(card["contract"])
    goal = _as_dict(card.get("goal"))
    return {
        "proof": _as_str_list(goal.get("proof")),
        "invariant_ids": _as_str_list(goal.get("invariant_ids")),
    }


def get_touch(card: dict[str, Any]) -> dict[str, Any]:
    return _as_dict(card.get("touch"))


def rules_forbidden_strings(card: dict[str, Any]) -> list[str]:
    """Plain forbidden phrases for grep / disconnect (agent Rules leg)."""
    rules = get_rules(card)
    out = _as_str_list(rules.get("forbidden"))
    touch = get_touch(card)
    for sig in _as_str_list(touch.get("behavior_signals")):
        if sig.lower().startswith("forbidden:"):
            phrase = sig.split(":", 1)[1].strip()
            if phrase and phrase not in out:
                out.append(phrase)
    return out


def touch_behavior_signals(card: dict[str, Any]) -> list[str]:
    """Run-alignment signals on Touch leg (tests + structural names; not LLM rules)."""
    touch = get_touch(card)
    return _as_str_list(touch.get("behavior_signals"))


def contract_proof_paths(card: dict[str, Any]) -> list[str]:
    return _as_str_list(get_contract(card).get("proof"))


def normalize_card(card: dict[str, Any]) -> dict[str, Any]:
    """Return card with v2 top-level keys populated (does not remove legacy keys)."""
    if card.get("conceptual") and card.get("rules") and card.get("contract"):
        return card
    normalized = dict(card)
    normalized.setdefault("conceptual", get_conceptual(card))
    normalized.setdefault("rules", get_rules(card))
    normalized.setdefault("contract", get_contract(card))
    meta = _as_dict(normalized.get("meta"))
    if meta.get("schema_version") is None:
        meta["schema_version"] = 1 if "conceptual" not in card else SCHEMA_VERSION
    normalized["meta"] = meta
    return normalized
