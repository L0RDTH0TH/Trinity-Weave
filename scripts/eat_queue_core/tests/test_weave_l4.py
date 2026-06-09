"""Wave 4 — L4 adaptive policy offline replay and bandit."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.adaptive_policy import (
    collect_replay_episodes,
    compute_episode_reward,
    propose_policy_promotion,
    run_offline_replay,
    bandit_update,
    recommend_profile,
)
from eat_queue_core.weave.config import load_l4_config
from eat_queue_core.weave.governance import append_metric_row, weave_dir
from eat_queue_core.weave.verifier import REQUIRED_SECTIONS


class TestWeaveL4(unittest.TestCase):
    def test_reward_integrity_ok_positive(self) -> None:
        r = compute_episode_reward({"integrity_ok": True, "system_attention": "green"})
        self.assertGreater(r, 0.5)

    def test_offline_replay_insufficient(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            weave_dir(root).mkdir(parents=True, exist_ok=True)
            cfg_path = root / "3-Resources" / "Second-Brain-Config.md"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text("weave:\n  l4_replay_min_episodes: 5\n", encoding="utf-8")
            out = run_offline_replay(root)
            self.assertFalse(out.get("ok"))
            self.assertEqual(out.get("reason"), "insufficient_episodes")

    def test_replay_and_bandit_with_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg_path = root / "3-Resources" / "Second-Brain-Config.md"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text(
                "weave:\n  l4_replay_min_episodes: 3\n  l4_min_uplift_for_proposal: 0.0\n",
                encoding="utf-8",
            )
            for i in range(5):
                append_metric_row(
                    root,
                    {
                        "metric_type": "lane_board_refresh",
                        "integrity_ok": i % 2 == 0,
                        "system_attention": "yellow",
                    },
                )
            replay = run_offline_replay(root)
            self.assertTrue(replay.get("ok"))
            self.assertIn("recommended_arm", replay)
            upd = bandit_update(root)
            self.assertTrue(upd.get("ok"))
            rec = recommend_profile(root)
            self.assertIn(rec.get("arm"), ("quality", "balance", "speed"))

    def test_propose_promotion_queues_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".technical" / "parallel" / "maintenance").mkdir(parents=True)
            cfg_path = root / "3-Resources" / "Second-Brain-Config.md"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text(
                "weave:\n  l4_replay_min_episodes: 2\n  l4_min_uplift_for_proposal: -1\n",
                encoding="utf-8",
            )
            for _ in range(4):
                append_metric_row(
                    root,
                    {"metric_type": "lane_board_refresh", "integrity_ok": True},
                )
            out = propose_policy_promotion(root)
            self.assertTrue(out.get("ok"))
            pq = root / ".technical" / "parallel" / "maintenance" / "prompt-queue.jsonl"
            self.assertTrue(pq.is_file())
            line = pq.read_text(encoding="utf-8").strip().splitlines()[-1]
            entry = json.loads(line)
            self.assertEqual(entry.get("mode"), "ADAPTIVE_POLICY_REVIEW")

    def test_verifier_requires_l4_section(self) -> None:
        self.assertIn("## L4 adaptive pilot", REQUIRED_SECTIONS)


if __name__ == "__main__":
    unittest.main()
