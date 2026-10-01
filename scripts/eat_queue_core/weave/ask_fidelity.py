"""Ask fidelity — structural check: foundation ≠ house; substitutes ≠ ask_success."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence


CLAIM_STAGING = "staging"
CLAIM_ASK_SUCCESS = "ask_success"
VALID_CLAIM_CLASSES = frozenset({CLAIM_STAGING, CLAIM_ASK_SUCCESS})

# Markers that indicate a forbidden substitute when claim_class is ask_success
DEFAULT_SUBSTITUTE_MARKERS: dict[str, tuple[str, ...]] = {
    "demo": (
        "front_door_spine_only",
        "table_chrome_only",
        "staging_checkpoints_as_demo",
        "spine_only",
    ),
    "horizon_demo": (
        "front_door_spine_only",
        "table_chrome_only",
        "staging_checkpoints_as_demo",
        "spine_only",
    ),
    "horizon_demo_investor": (
        "front_door_spine_only",
        "table_chrome_only",
        "staging_checkpoints_as_demo",
        "spine_only",
    ),
    "character_creation": (
        "single_dropdown_stub",
        "option_button_only",
        "pick_preset_menu_without_authoring",
        "dropdown_only",
    ),
    "ux_player_character_creation": (
        "single_dropdown_stub",
        "option_button_only",
        "pick_preset_menu_without_authoring",
        "dropdown_only",
    ),
    "chargen": (
        "single_dropdown_stub",
        "option_button_only",
        "pick_preset_menu_without_authoring",
        "dropdown_only",
    ),
    "rules_resolution": ("hardcoded_ok_bypass_rules_host",),
    "rules_min_pf1": ("hardcoded_ok_bypass_rules_host",),
}


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, Sequence):
        return [str(x) for x in value if str(x).strip()]
    return [str(value)]


def evaluate_ask_fidelity(
    handoff: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Return little-val-shaped result for ask fidelity.

    handoff: ask_id, done_when, forbidden_substitutes (optional), foundation_checkpoint_ids
    receipt: claim_class, done_when_quote, substitute_markers_present (optional list),
             evidence_paths (optional)
    """
    missing: list[str] = []
    ask_id = str(handoff.get("ask_id") or "").strip()
    done_when = str(handoff.get("done_when") or "").strip()
    forbidden = _as_list(handoff.get("forbidden_substitutes"))
    if not forbidden and ask_id in DEFAULT_SUBSTITUTE_MARKERS:
        forbidden = list(DEFAULT_SUBSTITUTE_MARKERS[ask_id])

    if not ask_id:
        missing.append("handoff.ask_id required")
    if not done_when:
        missing.append("handoff.done_when required (experience bar / house)")

    claim = str(receipt.get("claim_class") or "").strip()
    if claim not in VALID_CLAIM_CLASSES:
        missing.append(
            f"receipt.claim_class must be one of {sorted(VALID_CLAIM_CLASSES)} (got {claim!r})"
        )

    quote = str(receipt.get("done_when_quote") or "").strip()
    markers = _as_list(receipt.get("substitute_markers_present"))
    # Also scan evidence note / summary for marker tokens if provided
    blob = " ".join(
        [
            quote,
            str(receipt.get("summary") or ""),
            " ".join(_as_list(receipt.get("evidence_paths"))),
            " ".join(markers),
        ]
    ).lower()

    if claim == CLAIM_STAGING:
        # Staging may omit full house evidence; still require ask identity on handoff
        if missing:
            return {
                "ok": False,
                "missing": missing,
                "hint": "Normalize ask_id + done_when on hand-off; label claim_class staging for foundation work.",
                "category": "ask_fidelity_handoff",
                "reject_code": None,
            }
        return {
            "ok": True,
            "missing": [],
            "hint": "",
            "category": "ask_fidelity_staging",
            "reject_code": None,
        }

    # ask_success path
    if not quote:
        missing.append("receipt.done_when_quote required when claim_class=ask_success")
    elif done_when and done_when.lower() not in quote.lower() and quote.lower() not in done_when.lower():
        # soft: quote should overlap done_when text
        missing.append(
            "receipt.done_when_quote must quote/overlap handoff.done_when (house bar)"
        )

    hit_subs: list[str] = []
    for sub in forbidden:
        token = sub.lower().replace("-", "_")
        if token in blob or sub in markers:
            hit_subs.append(sub)
    # common vernacular
    vernacular = {
        "spine": ["front_door_spine_only", "spine_only"],
        "dropdown": ["single_dropdown_stub", "dropdown_only", "option_button_only"],
    }
    for word, mapped in vernacular.items():
        if word in blob:
            for m in mapped:
                if m in forbidden or ask_id in DEFAULT_SUBSTITUTE_MARKERS:
                    if m not in hit_subs and (
                        m in forbidden
                        or m in DEFAULT_SUBSTITUTE_MARKERS.get(ask_id, ())
                    ):
                        hit_subs.append(m)

    if hit_subs:
        missing.append(
            f"forbidden substitute markers present under ask_success: {sorted(set(hit_subs))}"
        )

    if missing:
        return {
            "ok": False,
            "missing": missing,
            "hint": (
                "Do not claim ask_success for foundation/substitutes. "
                "Either finish the house (done_when) or set claim_class=staging. "
                "Reject: fidelity_miss."
            ),
            "category": "ask_fidelity_miss",
            "reject_code": "fidelity_miss",
        }

    return {
        "ok": True,
        "missing": [],
        "hint": "",
        "category": "ask_fidelity_ask_success",
        "reject_code": None,
    }


def normalize_chat_ask(
    ask_id: str,
    done_when: str,
    *,
    forbidden_substitutes: Sequence[str] | None = None,
    foundation_checkpoint_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Build required hand-off fidelity params from a chat/operator ask."""
    ask_id = ask_id.strip()
    forbidden = list(forbidden_substitutes or [])
    if not forbidden and ask_id in DEFAULT_SUBSTITUTE_MARKERS:
        forbidden = list(DEFAULT_SUBSTITUTE_MARKERS[ask_id])
    out: MutableMapping[str, Any] = {
        "ask_id": ask_id,
        "done_when": done_when.strip(),
        "forbidden_substitutes": forbidden,
        "foundation_checkpoint_ids": list(foundation_checkpoint_ids or []),
    }
    return dict(out)
