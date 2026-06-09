"""Tests for trinity boundary audit (Phase 0)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_boundary_audit import run_trinity_boundary_audit
from eat_queue_core.weave.trinity_partition import load_partition_registry


class TrinityBoundaryAuditTests(unittest.TestCase):
    def test_load_partition_registry_maintenance_scope(self) -> None:
        root = Path(__file__).resolve().parents[3]
        reg = load_partition_registry(root)
        ids = reg.maintenance_component_ids()
        self.assertIn("lane_status_board", ids)
        self.assertIn("l3_self_heal", ids)
        self.assertNotIn("l5_sandbox", ids)
        self.assertIn("l5_sandbox", reg.deferred)

    def test_run_audit_on_maintenance_components(self) -> None:
        root = Path(__file__).resolve().parents[3]
        out = run_trinity_boundary_audit(root, write_report=False)
        self.assertEqual(out["summary"]["cards_audited"], 14)
        self.assertIn("rows", out)
        self.assertIn("known_overlap_risks", out)


if __name__ == "__main__":
    unittest.main()
