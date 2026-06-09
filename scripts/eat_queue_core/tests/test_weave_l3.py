"""Wave 3 — L3 self-healing rollout and handlers."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.recoverable_codes import classify_primary_code
from eat_queue_core.recoverable_handlers import run_recoverable_handler
from eat_queue_core.weave.config import load_l3_config
from eat_queue_core.weave.l3_self_heal import (
    F2_HANDLER_ALLOWLIST,
    handler_permitted,
    lane_auto_heal_permitted,
    normalize_rollout,
)
from eat_queue_core.weave.verifier import REQUIRED_SECTIONS


class TestWeaveL3(unittest.TestCase):
    def test_f2_handler_catalog(self) -> None:
        self.assertIn("reconcile_launch_registry", F2_HANDLER_ALLOWLIST)
        self.assertIn("rebuild_board_snapshot", F2_HANDLER_ALLOWLIST)
        self.assertEqual(len(F2_HANDLER_ALLOWLIST), 6)

    def test_rollout_f2_blocks_sandbox_lane(self) -> None:
        from eat_queue_core.weave.config import L3Config

        cfg = L3Config(enabled=True, rollout_phase="f2")
        self.assertFalse(lane_auto_heal_permitted("sandbox", cfg))
        self.assertTrue(lane_auto_heal_permitted("maintenance", cfg))

    def test_rollout_f4_all_lanes(self) -> None:
        from eat_queue_core.weave.config import L3Config

        cfg = L3Config(enabled=True, rollout_phase="f4")
        self.assertTrue(lane_auto_heal_permitted("godot", cfg))
        self.assertTrue(handler_permitted("ghost_skill_audit", "godot", cfg))

    def test_f2_blocks_ghost_handler(self) -> None:
        from eat_queue_core.weave.config import L3Config

        cfg = L3Config(enabled=True, rollout_phase="f2")
        self.assertFalse(handler_permitted("ghost_skill_audit", "maintenance", cfg))
        self.assertTrue(handler_permitted("reconcile_launch_registry", "maintenance", cfg))

    def test_registry_stale_code_maps_handler(self) -> None:
        c = classify_primary_code("registry_stale")
        self.assertEqual(c["handler"], "reconcile_launch_registry")

    def test_handler_blocked_under_f2_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg_path = root / "3-Resources" / "Second-Brain-Config.md"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text(
                "weave:\n  l3_self_heal_enabled: true\n  l3_rollout_phase: f2\n",
                encoding="utf-8",
            )
            (root / ".technical" / "parallel" / "sandbox").mkdir(parents=True)
            l3 = load_l3_config(root)
            self.assertEqual(normalize_rollout(l3.rollout_phase), "f2")
            out = run_recoverable_handler("ghost_skill_audit", root, "sandbox")
            self.assertFalse(out.get("ok"))
            self.assertEqual(out.get("error"), "l3_rollout_blocked")

    def test_verifier_requires_l3_section(self) -> None:
        self.assertIn("## L3 self-healing", REQUIRED_SECTIONS)


if __name__ == "__main__":
    unittest.main()
