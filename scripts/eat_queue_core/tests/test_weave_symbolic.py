"""Phase 4.5 neuro-symbolic tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.invariant_registry import (
    activate_invariant,
    bootstrap_n2_invariants,
    list_invariants,
    load_invariant,
)
from eat_queue_core.weave.symbolic_conflict import evaluate_symbolic_conflict


class SymbolicRegistryTest(unittest.TestCase):
    def test_bootstrap_n2_creates_invariants(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = bootstrap_n2_invariants(root)
            self.assertTrue(out.get("ok"))
            self.assertGreaterEqual(out.get("active_count", 0), 3)
            active = list_invariants(root, status="active")
            ids = {e.id for e in active}
            self.assertIn("lane_run_no_receipt_inference", ids)

    def test_medium_invariant_requires_counselor(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bootstrap_n2_invariants(root)
            ent = load_invariant(root, "registry_reconcile_pre_read")
            self.assertIsNotNone(ent)
            assert ent is not None
            self.assertEqual(ent.status, "pending_counselor")
            bad = activate_invariant(root, ent.id, counselor_approved=False)
            self.assertFalse(bad.get("ok"))
            good = activate_invariant(root, ent.id, counselor_approved=True)
            self.assertTrue(good.get("ok"))

    def test_forbidden_flag_blocks_when_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bootstrap_n2_invariants(root)
            # observe-only default — not blocked
            d = evaluate_symbolic_conflict(
                root,
                context={"forbidden_flags": ["infer_run_from_receipt"]},
                risk_tier="high",
            )
            self.assertFalse(d.blocked)
            self.assertIn(d.decision, ("block", "needs_human_resolution"))

    def test_clean_context_proceeds(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bootstrap_n2_invariants(root)
            d = evaluate_symbolic_conflict(
                root,
                context={
                    "pre_read_steps": ["reconcile_launch_registry"],
                    "kernel_used": "build_lane_snapshots",
                },
                risk_tier="low",
            )
            self.assertEqual(d.decision, "proceed")


if __name__ == "__main__":
    unittest.main()
