"""Unit tests — Gate B₂ weld intent hostile (post-weld)."""

from __future__ import annotations

from eat_queue_core.weave.factory.prefer_weld_intent import (
    PLACE_BEHAVIOR_KEYS,
    assert_no_prefer_rewrite,
    build_evidence_pack,
    evaluate_behavior_evidence,
    post_weld_keep_latch,
    scan_chat_hotfix_receipt,
    validate_weld_intent_latch,
    weld_intent_hostile_ok,
)


def _b2_ok() -> dict:
    return {
        "map_fidelity_hostile_ok": True,
        "weld_intent_hostile_ok": True,
        "weld_intent_hostile": {"ok": True, "verdict": "pass"},
    }


def _honest_place_behavior() -> dict:
    return {k: True for k in PLACE_BEHAVIOR_KEYS}


def test_piggyback_tagged_success_fails_even_when_log_says_keep():
    """Guard 1 — logs/tags cannot acquit. Piggyback fixture fails B₂."""
    pack = build_evidence_pack(
        prefer_success="grey ghost → LMB → permanent opaque Full",
        prefer_refuses=["piggyback_as_place_success", "piggyback_skip_update_four"],
        proof_tags=["piggyback_place_v1"],
        factory_log_excerpts=["piggyback_place_v1 Success", "KEEP ready"],
        keep_headers=["KEEP — place product"],
        behavior={
            "same_seat_ghost_eq_commit": False,
            "update_four_ran": False,
            "coast_gate_ran": False,
            "full_survives_neighbor_rebuild": False,
            "prefer_refuses_not_violated_in_live": False,
        },
        pass_basis="proof_tag",  # wrong — must fail
    )
    result = evaluate_behavior_evidence(pack)
    assert result.ok is False
    assert any("piggyback_indict" in v for v in result.violations)
    assert any("forbidden_pass_basis" in v or "logs_cannot_acquit" in v for v in result.violations)
    assert any("update_four_skipped" in v for v in result.violations)


def test_honest_place_behavior_can_pass_mechanical():
    """Honest place-shaped fixture — B₂ mechanical can pass (still needs F5)."""
    pack = build_evidence_pack(
        prefer_success="grey ghost → LMB → permanent opaque Full on same seat",
        prefer_refuses=["piggyback_as_place_success"],
        proof_tags=[],  # tags empty — behavior is pass basis
        behavior=_honest_place_behavior(),
        pass_basis="behavior",
    )
    result = evaluate_behavior_evidence(pack)
    assert result.ok is True, result.violations
    assert pack["tags_are_not_pass_evidence"] is True


def test_string_match_prefer_to_methods_fails():
    pack = build_evidence_pack(
        prefer_success="UpdateFour and CoastGate",
        string_match_hits=["UpdateFour", "CoastGate", "TrySeatPolygon"],
        pass_basis="prefer_word_method_name_match",
        behavior=_honest_place_behavior(),
    )
    result = evaluate_behavior_evidence(pack)
    assert result.ok is False
    assert any("string_match_as_pass" in v for v in result.violations)
    assert any("forbidden_pass_basis" in v for v in result.violations)


def test_bypass_without_greenlit_allowed():
    receipt = {
        "factory_bypass": True,
        "factory_greenlit": False,
        "claim_class": "staging",
        "operator_ack": "yes skip factory for this hotfix",
    }
    result = validate_weld_intent_latch(None, receipt=receipt)
    assert result.ok is True
    assert result.bypass is True
    assert result.applicable is False


def test_bypass_with_greenlit_fails():
    receipt = {
        "factory_bypass": True,
        "factory_greenlit": True,
        "claim_class": "staging",
    }
    result = validate_weld_intent_latch(None, receipt=receipt)
    assert result.ok is False
    assert any("bypass_must_not_claim_greenlit" in v for v in result.violations)


def test_greenlit_without_b2_fails():
    armed = {
        "slice_id": "alpha0_stalberg_dual_place_product_r1",
        "claim_class": "staging_awaiting_f5",
        "factory_greenlit": True,
        "live_weld_landed": True,
    }
    result = validate_weld_intent_latch(armed, prefer_result={"map_fidelity_hostile_ok": True})
    assert result.ok is False
    assert any(
        "hostile_required_before_success" in v or "greenlit_without_b2" in v
        for v in result.violations
    )


def test_greenlit_with_b2_ok():
    armed = {
        "slice_id": "alpha0_stalberg_dual_place_product_r1",
        "claim_class": "staging_awaiting_f5",
        "factory_greenlit": True,
        "live_weld_landed": True,
    }
    pack = build_evidence_pack(
        behavior=_honest_place_behavior(),
        pass_basis="behavior",
    )
    result = validate_weld_intent_latch(
        armed, prefer_result=_b2_ok(), evidence_pack=pack
    )
    assert result.ok is True, result.violations


def test_chat_receipt_scanner_greenlit_without_b2():
    text = """---
factory_greenlit: true
live_weld_landed: true
claim_class: staging_awaiting_f5
proof_tag: piggyback_place_v1
---
Hotfix welded LIVE without factory.
"""
    result = scan_chat_hotfix_receipt(text)
    assert result.ok is False
    assert any(
        "hostile_required" in v or "greenlit_without_b2" in v for v in result.violations
    )


def test_weld_intent_hostile_ok_helper():
    assert weld_intent_hostile_ok(None) is False
    assert weld_intent_hostile_ok({"weld_intent_hostile_ok": True}) is True
    assert weld_intent_hostile_ok({"weld_intent_hostile": {"ok": True}}) is True
    assert weld_intent_hostile_ok({"map_fidelity_hostile_ok": True}) is False


def test_b2_does_not_rewrite_prefer_success():
    before = "Grey ghost → LMB → permanent opaque Full on same seat"
    after = before
    assert assert_no_prefer_rewrite(before, after) == []
    assert assert_no_prefer_rewrite(before, "thinner rewrite") == [
        "weld_intent:prefer_success_rewritten_by_b2"
    ]


def test_post_weld_keep_latch_needs_b1_b2_f5():
    armed = {
        "slice_id": "x",
        "factory_greenlit": True,
        "live_weld_landed": True,
        "claim_class": "ask_success",
    }
    r = post_weld_keep_latch(armed, prefer_result=None, operator_f5_ok=False)
    assert r.ok is False
    r2 = post_weld_keep_latch(
        armed,
        prefer_result=_b2_ok(),
        evidence_pack=build_evidence_pack(
            behavior=_honest_place_behavior(), pass_basis="behavior"
        ),
        operator_f5_ok=True,
    )
    assert r2.ok is True, r2.violations


def test_verify_mcp_only_refuse():
    pack = build_evidence_pack(
        behavior=_honest_place_behavior(),
        pass_basis="behavior",
        mcp_attest_only=True,
    )
    result = evaluate_behavior_evidence(pack)
    assert result.ok is False
    assert any("verify_mcp_only" in v for v in result.violations)
