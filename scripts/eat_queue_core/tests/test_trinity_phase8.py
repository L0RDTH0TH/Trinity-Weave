"""Phase 8 — vault compensation (stamp core, D stubs, harness retier)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from eat_queue_core.weave.trinity_card_generate import build_provisional_bridge_stub
from eat_queue_core.weave.trinity_vault_compensation import (
    CORE_FORBIDDEN_SHORT,
    deploy_phase8_bridge_stubs,
    retier_harness_cards_to_proposals,
    stamp_maintenance_core_card,
)


class TestStampCore(unittest.TestCase):
    def test_stamp_adds_lock_kind_and_forbidden(self) -> None:
        card = {
            "id": "lane_status_board",
            "meta": {"conceptual_confirmed_at": "x", "rules_confirmed_at": "y"},
            "conceptual": {"summary": "board"},
            "rules": {"forbidden": []},
            "touch": {"behavior_signals": ["test_lane_status_board.py"]},
        }
        out = stamp_maintenance_core_card(card, trinity_id="lane_status_board")
        self.assertEqual(out["meta"]["lock_kind"], "maintenance_core")
        self.assertFalse(out["meta"]["system_mutable"])
        forb = out["rules"]["forbidden"]
        self.assertIn(CORE_FORBIDDEN_SHORT, forb)
        self.assertTrue(any("policy: Phase 8 dual-lock" in p for p in out["rules"].get("precedence") or []))

    def test_stamp_keeps_existing_forbidden_when_at_test_guard_cap(self) -> None:
        card = {
            "id": "lane_status_board",
            "meta": {},
            "conceptual": {"summary": "board"},
            "rules": {"forbidden": ["existing"]},
            "touch": {"behavior_signals": ["test_lane_status_board.py"]},
        }
        out = stamp_maintenance_core_card(card, trinity_id="lane_status_board")
        forb = out["rules"]["forbidden"]
        self.assertIn("existing", forb)
        self.assertNotIn(CORE_FORBIDDEN_SHORT, forb)
        self.assertTrue(any("policy: Phase 8 dual-lock" in p for p in out["rules"].get("precedence") or []))

    def test_zero_tests_uses_precedence_only(self) -> None:
        card = {
            "id": "l4_adaptive_policy",
            "meta": {},
            "conceptual": {},
            "rules": {"forbidden": []},
            "touch": {"behavior_signals": ["scripts/eat_queue_core/weave/adaptive_policy.py"]},
        }
        out = stamp_maintenance_core_card(card, trinity_id="l4_adaptive_policy")
        self.assertNotIn(CORE_FORBIDDEN_SHORT, out["rules"].get("forbidden") or [])
        self.assertTrue(any("Phase 8 dual-lock" in p for p in out["rules"].get("precedence") or []))

    def test_bridge_doctrine_appended(self) -> None:
        card = {
            "id": "trinity_spine_maintenance",
            "meta": {},
            "conceptual": {"summary": "spine"},
            "rules": {"forbidden": []},
            "touch": {},
        }
        out = stamp_maintenance_core_card(
            card, trinity_id="trinity_spine_maintenance"
        )
        self.assertIn("Dual-lock", out["conceptual"]["summary"])


class TestPhase8Deploy(unittest.TestCase):
    def test_deploy_d_stubs_tunnel_via_bridge_b(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            weave = root / ".technical/weave"
            weave.mkdir(parents=True)
            (weave / "trinity-partition-registry.yaml").write_text(
                "schema_version: 1\nmaintenance_core:\n  ids: []\npartitions:\n  maintenance:\n    components: []\n",
                encoding="utf-8",
            )
            out = deploy_phase8_bridge_stubs(root, dry_run=False)
            self.assertTrue(out.get("ok"))
            self.assertGreaterEqual(len(out.get("written") or []), 2)
            catchup = yaml.safe_load(
                (weave / "component-proposals" / "catchup_corpus_tunnel.yaml").read_text()
            )
            self.assertEqual(
                catchup["touch"]["tunnel_via"], "trinity_spine_maintenance"
            )
            self.assertNotEqual(catchup["touch"]["tunnel_via"], "lane_status_board")

    def test_retier_moves_harness_out_of_components(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            comp = root / ".technical/weave/components"
            comp.mkdir(parents=True)
            (comp / "harness_foo.yaml").write_text(
                yaml.dump({"id": "harness_foo", "meta": {}, "touch": {}}),
                encoding="utf-8",
            )
            (root / ".technical/weave/trinity-partition-registry.yaml").write_text(
                "schema_version: 1\nmaintenance_core:\n  ids: []\npartitions:\n  maintenance:\n    components: []\n",
                encoding="utf-8",
            )
            out = retier_harness_cards_to_proposals(root, dry_run=False)
            self.assertIn("harness_foo", out.get("moved") or [])
            self.assertFalse((comp / "harness_foo.yaml").is_file())
            self.assertTrue(
                (root / ".technical/weave/component-proposals/harness_foo.yaml").is_file()
            )


if __name__ == "__main__":
    unittest.main()
