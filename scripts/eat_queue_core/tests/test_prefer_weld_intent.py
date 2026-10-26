"""Unit tests — Gate B₂ weld intent hostile (post-weld)."""

from __future__ import annotations

from eat_queue_core.weave.factory.prefer_weld_intent import (
    PLACE_BEHAVIOR_KEYS,
    assert_no_prefer_rewrite,
    build_evidence_pack,
    evaluate_behavior_evidence,
    is_factory_bypass,
    post_weld_keep_latch,
    scan_chat_hotfix_receipt,
    validate_weld_intent_latch,
    weld_intent_hostile_ok,
)


def _b2_ok() -> dict:
    return {
        "map_fidelity_hostile_ok": True,
        "map_fidelity_hostile": {"ok": True, "source": "harness_b1"},
        "weld_intent_hostile_ok": True,
        "weld_intent_hostile": {
            "ok": True,
            "source": "harness_b2",
            "verdict": "pass",
            "pass_basis": "behavior",
        },
    }


def _honest_place_behavior() -> dict:
    return {k: True for k in PLACE_BEHAVIOR_KEYS}


def _honest_place_pack(**kwargs):
    return build_evidence_pack(
        prefer_class="place",
        behavior=_honest_place_behavior(),
        pass_basis="behavior",
        **kwargs,
    )


def test_piggyback_tagged_success_fails_even_when_log_says_keep():
    """Guard 1 — logs/tags cannot acquit. Piggyback fixture fails B₂."""
    pack = build_evidence_pack(
        prefer_class="place",
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
    assert any(
        "forbidden_pass_basis" in v or "logs_cannot_acquit" in v for v in result.violations
    )
    assert any("update_four_skipped" in v for v in result.violations)


def test_honest_place_behavior_can_pass_mechanical():
    """Honest place-shaped fixture — B₂ mechanical can pass (still needs F5)."""
    pack = _honest_place_pack(
        prefer_success="grey ghost → LMB → permanent opaque Full on same seat",
        prefer_refuses=["piggyback_as_place_success"],
        proof_tags=[],
    )
    result = evaluate_behavior_evidence(pack)
    assert result.ok is True, result.violations
    assert pack["tags_are_not_pass_evidence"] is True


def test_string_match_prefer_to_methods_fails():
    pack = build_evidence_pack(
        prefer_class="place",
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
    assert is_factory_bypass(None, receipt) is True


def test_bypass_without_ack_fails():
    """Bare factory_bypass: true without operator ack quote must not skip B₂."""
    receipt = {
        "factory_bypass": True,
        "factory_greenlit": False,
        "live_weld_landed": True,
        "claim_class": "staging_awaiting_f5",
    }
    result = validate_weld_intent_latch(None, receipt=receipt)
    assert result.ok is False
    assert any("bypass_missing_operator_ack" in v for v in result.violations)
    assert is_factory_bypass(None, receipt) is False


def test_bypass_with_greenlit_fails():
    receipt = {
        "factory_bypass": True,
        "factory_bypass_ack": "operator said skip factory",
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


def test_bare_hostile_ok_without_evidence_fails():
    """Hand-stamped weld_intent_hostile_ok: true without behavior pack = fail."""
    armed = {
        "slice_id": "alpha0_stalberg_dual_place_product_r1",
        "claim_class": "staging_awaiting_f5",
        "factory_greenlit": True,
        "live_weld_landed": True,
    }
    result = validate_weld_intent_latch(armed, prefer_result=_b2_ok())
    assert result.ok is False
    assert any("missing_evidence_pack" in v for v in result.violations)


def test_place_behavior_missing_update_four_fails():
    """Place-class partial behavior (omit update_four_ran) must fail, not pass."""
    partial = {
        "same_seat_ghost_eq_commit": True,
        "coast_gate_ran": True,
        "full_survives_neighbor_rebuild": True,
        "prefer_refuses_not_violated_in_live": True,
        # update_four_ran intentionally missing
    }
    pack = build_evidence_pack(
        prefer_class="place",
        behavior=partial,
        pass_basis="behavior",
    )
    result = evaluate_behavior_evidence(
        pack,
        armed={"slice_id": "alpha0_stalberg_dual_place_product_r1"},
    )
    assert result.ok is False
    assert any("behavior_key_missing:update_four_ran" in v for v in result.violations)


def test_greenlit_with_b2_ok():
    armed = {
        "slice_id": "alpha0_stalberg_dual_place_product_r1",
        "claim_class": "staging_awaiting_f5",
        "factory_greenlit": True,
        "live_weld_landed": True,
        "prefer_class": "place",
    }
    pack = _honest_place_pack()
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


def test_chat_receipt_embedded_on_armed_is_scanned():
    """Wired path — chat_hotfix_receipt on armed feeds the latch."""
    armed = {
        "slice_id": "x_place_y",
        "factory_greenlit": True,
        "live_weld_landed": True,
        "claim_class": "staging_awaiting_f5",
        "chat_hotfix_receipt": {
            "factory_greenlit": True,
            "live_weld_landed": True,
            "claim_class": "keep",
        },
    }
    result = validate_weld_intent_latch(
        armed,
        prefer_result=_b2_ok(),
        receipt=armed["chat_hotfix_receipt"],
        evidence_pack=_honest_place_pack(),
    )
    # Receipt alone does not supply stamp on prefer_result — latch uses prefer_result stamp + pack
    assert result.ok is True, result.violations


def test_weld_intent_hostile_ok_helper():
    assert weld_intent_hostile_ok(None) is False
    assert weld_intent_hostile_ok({"weld_intent_hostile_ok": True}) is False
    assert weld_intent_hostile_ok({"weld_intent_hostile": {"ok": True}}) is False
    assert weld_intent_hostile_ok(
        {"weld_intent_hostile": {"ok": True, "source": "harness_b2"}}
    ) is True
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
        "slice_id": "x_place_y",
        "factory_greenlit": True,
        "live_weld_landed": True,
        "claim_class": "ask_success",
        "prefer_class": "place",
    }
    r = post_weld_keep_latch(armed, prefer_result=None, operator_f5_ok=False)
    assert r.ok is False
    r2 = post_weld_keep_latch(
        armed,
        prefer_result=_b2_ok(),
        evidence_pack=_honest_place_pack(),
        operator_f5_ok=True,
    )
    assert r2.ok is True, r2.violations


def test_verify_mcp_only_refuse():
    pack = _honest_place_pack(mcp_attest_only=True)
    result = evaluate_behavior_evidence(pack)
    assert result.ok is False
    assert any("verify_mcp_only" in v for v in result.violations)


def test_unknown_prefer_class_fail_closed():
    pack = build_evidence_pack(
        prefer_class="mystery_widget",
        behavior={"play_path_matches_prefer_success": True},
        pass_basis="behavior",
    )
    result = evaluate_behavior_evidence(pack)
    assert result.ok is False
    assert any("unknown_prefer_class_fail_closed" in v for v in result.violations)


def test_wb_auth_place_does_not_inherit_dual_grid_place_class():
    """Substring 'place' in ticket id must not force PLACE-product B₂ keys."""
    from eat_queue_core.weave.factory.prefer_weld_intent import (
        resolve_prefer_behavior_class,
    )

    assert (
        resolve_prefer_behavior_class({"ticket_map_id": "WB-auth-place"}) == "unknown"
    )
    assert (
        resolve_prefer_behavior_class(
            {"ticket_map_id": "WB-auth-place", "prefer_class": "place"}
        )
        == "place"
    )
    assert (
        resolve_prefer_behavior_class({"ticket_map_id": "PLACE-product"}) == "place"
    )
