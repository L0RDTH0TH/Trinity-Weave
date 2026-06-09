"""Trinity transcript routing — plan index smoke tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_transcript_routing import (
    HARNESS_SPINE_IDS,
    build_plan_index,
    route_trinity_id,
)


class TestTrinityTranscriptRouting(unittest.TestCase):
    def test_build_plan_index_finds_harness_in_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plans = root / ".cursor/plans"
            plans.mkdir(parents=True)
            plans.joinpath("harness_test.plan.md").write_text(
                """---
name: Harness eat test
overview: headless_eat institute curator
---
# Plan
See `scripts/eat_queue_core/headless_orchestrator.py` and harness_headless_eat.
""",
                encoding="utf-8",
            )
            idx = build_plan_index(root)
            self.assertGreaterEqual(idx["plan_count"], 1)
            bucket = idx["by_trinity_id"].get("harness_headless_eat") or {}
            self.assertTrue(bucket.get("plans"))

    def test_route_empty_transcripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            idx = {"by_trinity_id": {}}
            r = route_trinity_id("harness_verify", idx, root / "missing")
            self.assertEqual(r.trinity_id, "harness_verify")


if __name__ == "__main__":
    unittest.main()
