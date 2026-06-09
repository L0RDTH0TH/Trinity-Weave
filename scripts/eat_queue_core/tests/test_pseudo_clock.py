"""pseudo_clock + pq_lock unit tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.pq_lock import acquire, is_locked, merge_pending_into_pq, release
from eat_queue_core.pseudo_clock import (
    curator_bundle_dir,
    load_clock,
    load_knobs,
    pq_path,
    tick,
)


class PseudoClockTest(unittest.TestCase):
    def test_knobs_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            knobs = load_knobs(root)
            self.assertFalse(knobs["headless_eat"])
            self.assertEqual(knobs["memory_compact_after_eat_completions"], 10)

    def test_pq_lock_acquire_release(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            bundle = Path(td) / "bundle"
            ok, _ = acquire(bundle, holder="test")
            self.assertTrue(ok)
            self.assertTrue(is_locked(bundle))
            release(bundle)
            self.assertFalse(is_locked(bundle))

    def test_merge_pending(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            bundle = Path(td) / "bundle"
            bundle.mkdir()
            pq = bundle / "prompt-queue.jsonl"
            pq.write_text('{"id":"a","mode":"INGEST_MODE"}\n', encoding="utf-8")
            pend = bundle / "prompt-queue-pending.jsonl"
            pend.write_text('{"id":"b","mode":"MAP_REFRESH"}\n', encoding="utf-8")
            n = merge_pending_into_pq(bundle, pq)
            self.assertEqual(n, 1)
            text = pq.read_text(encoding="utf-8")
            self.assertIn('"id":"a"', text.replace(" ", ""))
            self.assertIn('"id":"b"', text.replace(" ", ""))
            self.assertFalse(pend.exists())

    def test_tick_writes_clock(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "3-Resources").mkdir(parents=True)
            (root / "3-Resources" / "Second-Brain-Config.md").write_text(
                "```yaml\n"
                "curator_pseudo_clock:\n"
                "  enabled: true\n"
                "```\n",
                encoding="utf-8",
            )
            bundle = curator_bundle_dir(root)
            bundle.mkdir(parents=True)
            (bundle / "curator-knobs.yaml").write_text(
                "memory_compact_after_eat_completions: 100\npq_depth_map_refresh_threshold: 99\n",
                encoding="utf-8",
            )
            pq_path(root).write_text("", encoding="utf-8")
            out = tick(root, increment_eat=True)
            self.assertTrue(out.get("ok"))
            self.assertFalse(out.get("skipped"))
            clock = load_clock(root)
            self.assertEqual(clock["counters"]["eat_queue_completions"], 1)


if __name__ == "__main__":
    unittest.main()
