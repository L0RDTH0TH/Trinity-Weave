"""Wave 2.5b — trinity_touch_refresh harness and card updates."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.config import load_trinity_config
from eat_queue_core.weave.trinity_touch_refresh import (
    build_closure_manifest,
    load_trinity_card,
    merge_behavior_signals,
    propose_behavior_signals,
    refresh_trinity_card,
    run_trinity_touch_refresh,
)


def _write_config(root: Path) -> None:
    cfg = root / "3-Resources/Second-Brain-Config.md"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(
        """
```yaml
weave:
  enabled: true
  trinity_enabled: true
  trinity_checks_enabled: false
  trinity_max_closure_paths: 21
  trinity_max_closure_hops: 3
```
""",
        encoding="utf-8",
    )


def _write_min_card(root: Path) -> None:
    comp = root / ".technical/weave/components"
    comp.mkdir(parents=True, exist_ok=True)
    (comp / "lane_status_board.yaml").write_text(
        """
id: lane_status_board
conceptual:
  summary: s
  primary_case: p
touch:
  primary_paths:
    - scripts/eat_queue_core/lane_snapshot.py
  behavior_signals:
    - test_fm_matches_table_run
  behavior_signals_locked:
    - test_fm_matches_table_run
rules:
  forbidden:
  - receipt tail alone implies Run
  precedence:
  - one rule
contract:
  proof:
    - scripts/eat_queue_core/tests/test_board_fixtures.py
meta:
  touch_content_hash: null
  touch_refreshed_at: null
  schema_version: 2
""",
        encoding="utf-8",
    )
    br = root / ".technical/weave/blast-radius"
    br.mkdir(parents=True, exist_ok=True)
    (br / "lane-run-status.yaml").write_text(
        "concept: lane_run_status\nconsumers:\n  - scripts/eat_queue_core/lane_snapshot.py\n",
        encoding="utf-8",
    )
    (root / "scripts/eat_queue_core/lane_snapshot.py").parent.mkdir(parents=True, exist_ok=True)
    (root / "scripts/eat_queue_core/lane_snapshot.py").write_text("# stub\n", encoding="utf-8")
    tests = root / "scripts/eat_queue_core/tests"
    tests.mkdir(parents=True, exist_ok=True)
    (tests / "test_board_fixtures.py").write_text(
        "def test_receipt_success_only_idle_not_running():\n    pass\n",
        encoding="utf-8",
    )


class TrinityTouchRefreshTests(unittest.TestCase):
    def test_build_closure_manifest_hashes_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_min_card(root)
            card = load_trinity_card(root, "lane_status_board")
            m1 = build_closure_manifest(root, card, max_hops=1, max_paths=21)
            self.assertTrue(m1["touch_content_hash"])
            self.assertGreater(len(m1["must_read"]), 0)
            m2 = build_closure_manifest(root, card, max_hops=1, max_paths=21)
            self.assertEqual(m1["touch_content_hash"], m2["touch_content_hash"])

    def test_dry_run_does_not_write_hash_to_disk(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_config(root)
            _write_min_card(root)
            cfg = load_trinity_config(root)
            before = load_trinity_card(root, "lane_status_board")
            self.assertIsNone(before.get("meta", {}).get("touch_content_hash"))
            r = refresh_trinity_card(root, "lane_status_board", cfg, dry_run=True)
            self.assertTrue(r.ok)
            after = load_trinity_card(root, "lane_status_board")
            self.assertIsNone(after.get("meta", {}).get("touch_content_hash"))

    def test_refresh_writes_meta_hash(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_config(root)
            _write_min_card(root)
            cfg = load_trinity_config(root)
            r = refresh_trinity_card(root, "lane_status_board", cfg, dry_run=False)
            self.assertTrue(r.ok)
            card = load_trinity_card(root, "lane_status_board")
            self.assertTrue(card["meta"]["touch_content_hash"])
            self.assertTrue(card["meta"]["touch_refreshed_at"])

    def test_merge_respects_locked_signals(self) -> None:
        merged, new = merge_behavior_signals(
            ["test_fm_matches_table_run"],
            ["test_fm_matches_table_run"],
            ["test_receipt_success_only_idle_not_running"],
            apply_proposed=False,
        )
        self.assertIn("test_fm_matches_table_run", merged)
        self.assertEqual(new, ["test_receipt_success_only_idle_not_running"])

    def test_propose_behavior_signals_from_proof(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_min_card(root)
            card = load_trinity_card(root, "lane_status_board")
            props = propose_behavior_signals(root, card)
            self.assertIn("test_receipt_success_only_idle_not_running", props)

    def test_run_refresh_emits_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_config(root)
            _write_min_card(root)
            out = run_trinity_touch_refresh(root, pilot_only=True, dry_run=False)
            self.assertTrue(out.get("ok"))
            metrics = root / ".technical/weave/metrics.jsonl"
            self.assertTrue(metrics.is_file())
            last = metrics.read_text(encoding="utf-8").strip().splitlines()[-1]
            row = json.loads(last)
            self.assertEqual(row.get("event"), "trinity_touch_refresh")


if __name__ == "__main__":
    unittest.main()
