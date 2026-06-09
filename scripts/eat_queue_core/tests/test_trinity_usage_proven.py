"""Phase 15 — usage_proven earned freeze tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_dual_lock import (
    apply_usage_proven_to_card,
    corps_repair_skip_reason,
    is_usage_proven_id,
    lock_kind_from_card,
    system_may_mutate,
)
from eat_queue_core.weave.trinity_usage_proven import (
    evaluate_usage_proven_candidacy,
    stamp_usage_proven,
    unfreeze_usage_proven,
)

VAULT_ROOT = Path(__file__).resolve().parents[3]


class TestUsageProvenDualLock(unittest.TestCase):
    def test_apply_usage_proven_meta(self) -> None:
        card = {"id": "demo_card", "meta": {"provisional": True}}
        out = apply_usage_proven_to_card(card, evidence={"usage_count": 5}, now_iso="2026-06-02T00:00:00Z")
        self.assertEqual(lock_kind_from_card(out), "usage_proven")
        self.assertFalse(out["meta"]["system_mutable"])

    def test_system_may_not_mutate_usage_proven(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prop = root / ".technical/weave/components"
            prop.mkdir(parents=True)
            yaml_text = """id: up_demo
meta:
  lock_kind: usage_proven
  system_mutable: false
"""
            (prop / "up_demo.yaml").write_text(yaml_text, encoding="utf-8")
            self.assertTrue(is_usage_proven_id(root, "up_demo"))
            self.assertFalse(system_may_mutate(root, "up_demo", "write_trinity_card"))

    def test_corps_skip_usage_proven(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prop = root / ".technical/weave/components"
            prop.mkdir(parents=True)
            (prop / "up_demo.yaml").write_text(
                "id: up_demo\nmeta:\n  lock_kind: usage_proven\n",
                encoding="utf-8",
            )
            self.assertEqual(corps_repair_skip_reason(root, "up_demo"), "usage_proven")


class TestUsageProvenEvaluate(unittest.TestCase):
    def test_ineligible_maintenance_core(self) -> None:
        from eat_queue_core.weave.trinity_dual_lock import load_maintenance_core_policy

        policy = load_maintenance_core_policy(VAULT_ROOT)
        if not policy.ids:
            self.skipTest("no maintenance core ids")
        tid = sorted(policy.ids)[0]
        out = evaluate_usage_proven_candidacy(VAULT_ROOT, tid, update_streak=False)
        self.assertTrue(out.get("ok"))
        self.assertFalse(out.get("eligible"))

    def test_stamp_dry_run_provisional(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proposals = root / ".technical/weave/component-proposals"
            proposals.mkdir(parents=True)
            (proposals / "trial_card.yaml").write_text(
                "id: trial_card\nmeta:\n  provisional: true\ncontract:\n  proof: []\n",
                encoding="utf-8",
            )
            out = stamp_usage_proven(
                root,
                "trial_card",
                dry_run=True,
                operator_force=True,
            )
            self.assertTrue(out.get("ok"))
            self.assertTrue(out.get("dry_run"))


class TestUsageProvenUnfreeze(unittest.TestCase):
    def test_unfreeze_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            comp = root / ".technical/weave/components"
            comp.mkdir(parents=True)
            (comp / "up_demo.yaml").write_text(
                "id: up_demo\nmeta:\n  lock_kind: usage_proven\n  system_mutable: false\n",
                encoding="utf-8",
            )
            out = unfreeze_usage_proven(root, "up_demo", dry_run=True)
            self.assertTrue(out.get("ok"))


if __name__ == "__main__":
    unittest.main()
