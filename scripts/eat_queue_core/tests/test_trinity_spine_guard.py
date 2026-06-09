"""Phase 6 — respects_locked_spine, consumable pack resolution, provisional core advisory."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from eat_queue_core.weave.trinity_card_generate import build_provisional_bridge_stub
from eat_queue_core.weave.trinity_dual_lock import is_consumable_for_pack
from eat_queue_core.weave.trinity_pack import enrich_maintenance_params, resolve_consumable_trinity_id
from eat_queue_core.weave.trinity_spine_guard import (
    PROVISIONAL_CORE_RECOMMENDATIONS_REL,
    append_provisional_core_recommendation,
    is_provisional_bridge_card,
    maybe_recommend_provisional_core,
    respects_locked_spine,
)


class TestProvisionalBridgeStub(unittest.TestCase):
    def test_build_stub_has_tunnel_fields(self) -> None:
        card = build_provisional_bridge_stub(
            "bridge_to_board",
            tunnel_via="lane_status_board",
        )
        self.assertTrue(is_provisional_bridge_card(card))
        self.assertEqual(card["touch"]["tunnel_via"], "lane_status_board")
        self.assertIn("lane_status_board", card["touch"]["pairs_with"])
        self.assertTrue(card["touch"].get("bridge_scope"))


class TestRespectsLockedSpine(unittest.TestCase):
    def test_mapping_shadow_may_share_primary_path_with_core(self) -> None:
        from eat_queue_core.weave.trinity_spine_guard import allows_provisional_primary_path_overlap

        self.assertTrue(
            allows_provisional_primary_path_overlap(
                "skill_gap_mapping", "skill_gap", None
            )
        )
        self.assertTrue(
            allows_provisional_primary_path_overlap(
                "pseudo_clock", "l4_adaptive_policy", None
            )
        )

    def test_harness_shadow_may_share_primary_path_with_core(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module = "scripts/eat_queue_core/ghost_skill_audit.py"
            card = {
                "id": "harness_ghost_skill_audit",
                "meta": {"card_class": "promoted_provisional"},
                "touch": {"primary_paths": [module]},
                "rules": {"forbidden": [], "precedence": []},
                "conceptual": {"outcome": "shadow"},
                "contract": {"proof": [module]},
            }
            core_card = {
                "id": "ghost_skill_audit",
                "touch": {"primary_paths": [module]},
            }
            with mock.patch(
                "eat_queue_core.weave.trinity_spine_guard.is_maintenance_core_id",
                side_effect=lambda _v, tid: tid == "ghost_skill_audit",
            ), mock.patch(
                "eat_queue_core.weave.trinity_spine_guard._locked_core_cards",
                return_value={"ghost_skill_audit": core_card},
            ), mock.patch(
                "eat_queue_core.weave.trinity_spine_guard.run_trinity_boundary_audit",
                return_value={"cards": []},
            ), mock.patch(
                "eat_queue_core.weave.trinity_spine_guard.check_pilot_disconnects",
                return_value=[],
            ):
                r = respects_locked_spine(
                    root, "harness_ghost_skill_audit", card=card
                )
            overlap = [v for v in r.violations if v.kind == "primary_path_overlap_core"]
            self.assertEqual(overlap, [])

    def test_provisional_bridge_may_tunnel_via_core_orchestrator(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            card = build_provisional_bridge_stub(
                "catchup_corpus_tunnel",
                tunnel_via="trinity_spine_maintenance",
            )
            with mock.patch(
                "eat_queue_core.weave.trinity_spine_guard.is_maintenance_core_id",
                return_value=True,
            ), mock.patch(
                "eat_queue_core.weave.trinity_spine_guard._locked_core_cards",
                return_value={"trinity_spine_maintenance": card},
            ), mock.patch(
                "eat_queue_core.weave.trinity_spine_guard.run_trinity_boundary_audit",
                return_value={"cards": []},
            ), mock.patch(
                "eat_queue_core.weave.trinity_spine_guard.check_pilot_disconnects",
                return_value=[],
            ):
                r = respects_locked_spine(
                    root, "catchup_corpus_tunnel", card=card
                )
            tunnel_violations = [
                v for v in r.violations if v.kind == "tunnel_via_core"
            ]
            self.assertEqual(tunnel_violations, [])

    def test_core_id_passes_guard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch(
                "eat_queue_core.weave.trinity_spine_guard.is_maintenance_core_id",
                return_value=True,
            ):
                r = respects_locked_spine(root, "lane_status_board")
            self.assertTrue(r.ok)


class TestConsumablePackResolution(unittest.TestCase):
    def test_enrich_omits_non_consumable_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch(
                "eat_queue_core.weave.trinity_dual_lock.is_consumable_for_pack",
                side_effect=lambda _v, tid: tid == "lane_status_board",
            ), mock.patch(
                "eat_queue_core.weave.trinity_pack.resolve_trinity_id",
                return_value="lane_status_board",
            ):
                p = enrich_maintenance_params(
                    root,
                    "GOVERNANCE_REVIEW",
                    {"trinity_id": "some_provisional_stub"},
                )
            self.assertEqual(p.get("trinity_id"), "lane_status_board")
            self.assertEqual(p.get("trinity_id_advisory"), "some_provisional_stub")

    def test_resolve_consumable_returns_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch(
                "eat_queue_core.weave.trinity_dual_lock.is_consumable_for_pack",
                return_value=False,
            ), mock.patch(
                "eat_queue_core.weave.trinity_pack.resolve_trinity_id",
                return_value="stub_only",
            ):
                tid, extras = resolve_consumable_trinity_id(
                    root, trinity_id="stub_only"
                )
            self.assertIsNone(tid)
            self.assertEqual(extras.get("trinity_id_advisory"), "stub_only")


class TestProvisionalCoreRecommendations(unittest.TestCase):
    def test_append_recommendation_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch(
                "eat_queue_core.weave.trinity_spine_guard.is_maintenance_core_id",
                return_value=True,
            ):
                out = append_provisional_core_recommendation(
                    root,
                    target_trinity_id="lane_status_board",
                    rationale="test disconnect",
                )
            self.assertTrue(out.get("ok"))
            path = root / PROVISIONAL_CORE_RECOMMENDATIONS_REL
            self.assertTrue(path.is_file())
            row = json.loads(path.read_text(encoding="utf-8").strip().splitlines()[-1])
            self.assertEqual(row["promotion"], "never")
            self.assertFalse(row["consumable"])

    def test_maybe_recommend_skips_stale_only(self) -> None:
        from eat_queue_core.weave.trinity_align import TrinityAlignResult

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            align = TrinityAlignResult(
                trinity_id="lane_status_board",
                ok=False,
                stale_touch=True,
            )
            with mock.patch(
                "eat_queue_core.weave.trinity_spine_guard.is_maintenance_core_id",
                return_value=True,
            ):
                rec = maybe_recommend_provisional_core(root, "lane_status_board", align)
            self.assertIsNone(rec)


if __name__ == "__main__":
    unittest.main()
