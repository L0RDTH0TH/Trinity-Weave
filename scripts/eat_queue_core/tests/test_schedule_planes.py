"""Schedule planes + graduation unit tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from eat_queue_core.schedule_config import SchedulePlanesConfig, load_schedule_planes_config
from eat_queue_core.schedule_state import load_schedule_state, schedule_path, save_schedule_state
from eat_queue_core.schedule_tick import run_schedule_tick
from eat_queue_core.weave.trinity_graduation_evaluator import (
    evaluate_promotion,
    run_graduation_evaluator,
)


class ScheduleStateTest(unittest.TestCase):
    def test_migrate_legacy_clock(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bundle = root / ".technical" / "parallel" / "institute"
            bundle.mkdir(parents=True)
            legacy = {
                "version": 1,
                "counters": {"eat_queue_completions": 2},
                "last_actions": [{"action": "lane_status_board"}],
            }
            (bundle / "pseudo-clock.json").write_text(json.dumps(legacy), encoding="utf-8")
            state = load_schedule_state(root)
            self.assertEqual(state["version"], 2)
            self.assertEqual(state["counters"]["eat_queue_completions"], 2)
            self.assertTrue(state["last_actions_by_plane"]["listener"])

    def test_save_writes_schedule_and_legacy(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bundle = root / ".technical" / "parallel" / "institute"
            bundle.mkdir(parents=True)
            state = load_schedule_state(root)
            state["tick_count"] = 5
            save_schedule_state(root, state)
            self.assertTrue(schedule_path(root).is_file())
            self.assertTrue((bundle / "pseudo-clock.json").is_file())


class ScheduleTickTest(unittest.TestCase):
    def _minimal_vault(self, root: Path) -> None:
        (root / "3-Resources").mkdir(parents=True)
        (root / "3-Resources" / "Second-Brain-Config.md").write_text(
            "```yaml\n"
            "curator_pseudo_clock:\n"
            "  enabled: true\n"
            "schedule_planes:\n"
            "  listener_enabled: true\n"
            "  scheduled_enabled: false\n"
            "  reactive_enabled: false\n"
            "  graduation_enabled: false\n"
            "  maintain_wrap_every_n_ticks: 999\n"
            "```\n",
            encoding="utf-8",
        )
        bundle = root / ".technical" / "parallel" / "institute"
        bundle.mkdir(parents=True)
        (bundle / "curator-knobs.yaml").write_text(
            "memory_compact_after_eat_completions: 100\npq_depth_map_refresh_threshold: 99\n",
            encoding="utf-8",
        )
        (bundle / "prompt-queue.jsonl").write_text("", encoding="utf-8")

    def test_tick_increments_tick_count(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._minimal_vault(root)
            with mock.patch(
                "eat_queue_core.schedule_planes.run_listener_plane",
                return_value=[{"action": "lane_status_board", "plane": "listener"}],
            ):
                out = run_schedule_tick(root)
            self.assertTrue(out.get("ok"))
            self.assertEqual(out.get("surface"), "schedule_tick")
            state = load_schedule_state(root)
            self.assertEqual(state["tick_count"], 1)
            self.assertIn("actions_by_plane", out)

    def test_schedule_planes_config_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = load_schedule_planes_config(root)
            self.assertTrue(cfg.listener_enabled)
            self.assertFalse(cfg.graduation_enabled)
            self.assertEqual(cfg.maintain_wrap_every_n_ticks, 24)


class GraduationEvaluatorTest(unittest.TestCase):
    def test_promotion_requires_streak(self) -> None:
        from eat_queue_core.schedule_config import GraduationPromotion

        promo = GraduationPromotion(
            name="test",
            requires={"maintain_wrap_streak_min": 3, "type2.pass_gate_ok": True},
            sets={"trinity_corps_llm_repair_host_apply_enabled": True},
            rollback_on={"type2.pass_gate_ok": False},
        )
        ctx = {
            "maintain_wrap_streak": 1,
            "type2": {"pass_gate_ok": True},
        }
        ev = evaluate_promotion(Path("."), promo, ctx)
        self.assertFalse(ev["eligible"])

    def test_graduation_disabled_skips_apply(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = SchedulePlanesConfig(graduation_enabled=False)
            out = run_graduation_evaluator(root, cfg)
            self.assertTrue(out.get("ok"))
            self.assertEqual(out.get("applied"), [])


if __name__ == "__main__":
    unittest.main()
