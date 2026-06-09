"""Phase 3 predictive maintenance tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.governance import append_metric_row, metrics_path
from eat_queue_core.weave.predictive import (
    assess_maintenance_risk,
    calibrate_predictive_tiers,
    check_patch_scope,
    load_calibration,
)


class PredictiveTest(unittest.TestCase):
    def _seed_metrics(self, root: Path, n: int, *, integrity_ok: bool = True) -> None:
        for i in range(n):
            append_metric_row(
                root,
                {
                    "metric_type": "lane_board_refresh",
                    "system_attention": "red" if i % 2 == 0 else "yellow",
                    "integrity_ok": integrity_ok,
                    "lane_health_score": {"maintenance": 85, "institute": 30},
                },
            )

    def test_calibration_requires_valid_runs(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_metrics(root, 5)
            cal = calibrate_predictive_tiers(root)
            self.assertFalse(cal.calibrated)
            self.assertEqual(cal.valid_runs_in_window, 5)

    def test_calibration_completes_at_window(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_metrics(root, 14)
            cal = calibrate_predictive_tiers(root)
            self.assertTrue(cal.calibrated)
            self.assertTrue(load_calibration(root).calibrated)

    def test_assess_red_attention_high_tier(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_metrics(root, 14)
            calibrate_predictive_tiers(root)
            a = assess_maintenance_risk(
                root,
                context={
                    "system_attention": "red",
                    "lane_health_score": {"institute": 20, "sandbox": 10},
                },
            )
            self.assertGreaterEqual(a.maintenance_risk_score, 40)
            self.assertIn(a.risk_tier, ("medium", "high", "critical"))

    def test_patch_scope_critical_blocks_when_enforced(self) -> None:
        r = check_patch_scope("critical", files_count=2, lines_count=50, enforcement_active=True)
        self.assertFalse(r.ok)
        self.assertIn("critical", r.reason)

    def test_patch_scope_high_caps(self) -> None:
        r = check_patch_scope("high", files_count=4, lines_count=250, enforcement_active=True)
        self.assertFalse(r.ok)
        r2 = check_patch_scope("high", files_count=2, lines_count=100, enforcement_active=True)
        self.assertTrue(r2.ok)

    def test_enforcement_observe_only_when_disabled(self) -> None:
        r = check_patch_scope("critical", files_count=10, lines_count=500, enforcement_active=False)
        self.assertTrue(r.ok)


if __name__ == "__main__":
    unittest.main()
