"""Wave 5 H2 — L5 sandbox lane isolation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.config import load_l5_config
from eat_queue_core.weave.governance import append_metric_row
from eat_queue_core.weave.l5_sandbox import (
    SANDBOX_LANE,
    arm_l5_sandbox,
    assert_sandbox_lane,
    kill_l5_sandbox,
    load_l5_state,
    run_sandbox_tick,
    l5_status,
)
from eat_queue_core.weave.verifier import REQUIRED_SECTIONS


class TestWeaveL5(unittest.TestCase):
    def test_sandbox_lane_only(self) -> None:
        with self.assertRaises(ValueError):
            assert_sandbox_lane("godot")
        assert_sandbox_lane("sandbox")
        assert_sandbox_lane("gmm-mirror")

    def test_arm_and_tick_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg_path = root / "3-Resources" / "Second-Brain-Config.md"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text("weave:\n  l5_sandbox_enabled: true\n  l5_ac2_timebox_days: 1\n", encoding="utf-8")
            arm = arm_l5_sandbox(root, days=1)
            self.assertTrue(arm.get("ok"))
            self.assertEqual(arm.get("lane"), SANDBOX_LANE)
            tick = run_sandbox_tick(root, dry_run=True)
            self.assertTrue(tick.get("ok"))
            self.assertEqual(tick.get("lane"), SANDBOX_LANE)
            st = load_l5_state(root)
            self.assertEqual(st.get("status"), "armed")

    def test_kill_blocks_tick(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg_path = root / "3-Resources" / "Second-Brain-Config.md"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text("weave:\n  l5_sandbox_enabled: true\n", encoding="utf-8")
            arm_l5_sandbox(root, days=1)
            kill_l5_sandbox(root)
            tick = run_sandbox_tick(root, dry_run=True)
            self.assertTrue(tick.get("skipped"))
            self.assertEqual(tick.get("reason"), "kill_switch")

    def test_l3_green_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg_path = root / "3-Resources" / "Second-Brain-Config.md"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text(
                "weave:\n  l5_require_l3_green: true\n  l5_l3_green_min_pass_rate: 0.99\n",
                encoding="utf-8",
            )
            for i in range(5):
                append_metric_row(
                    root,
                    {"metric_type": "lane_board_refresh", "integrity_ok": i % 2 == 0},
                )
            arm = arm_l5_sandbox(root, days=1)
            self.assertFalse(arm.get("ok"))
            self.assertEqual(arm.get("error"), "l3_not_green")

    def test_status_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg_path = root / "3-Resources" / "Second-Brain-Config.md"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text("weave:\n  l5_sandbox_enabled: true\n", encoding="utf-8")
            st = l5_status(root)
            self.assertEqual(st.get("lane"), SANDBOX_LANE)
            self.assertTrue(load_l5_config(root).enabled)

    def test_verifier_requires_l5_section(self) -> None:
        self.assertIn("## L5 autonomous lab (H2)", REQUIRED_SECTIONS)


if __name__ == "__main__":
    unittest.main()
