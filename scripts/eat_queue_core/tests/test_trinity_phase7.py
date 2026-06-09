"""Phase 7 — bridge consolidate + card backlog."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from eat_queue_core.weave.trinity_bridge_consolidate import (
    find_provisional_bridges_for_tunnel,
    merge_bridge_cards,
    run_trinity_bridge_consolidate,
)
from eat_queue_core.weave.trinity_card_backlog import (
    assess_trinity_card_backlog,
    count_trinity_usage,
    format_backlog_board_hint,
)
from eat_queue_core.weave.trinity_card_generate import build_provisional_bridge_stub
from eat_queue_core.weave.trinity_partition import upsert_registry_bridge


class TestBridgeConsolidate(unittest.TestCase):
    def test_find_and_merge_provisional_bridges(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prop = root / ".technical/weave/component-proposals"
            prop.mkdir(parents=True)
            for name in ("bridge_a", "bridge_b"):
                card = build_provisional_bridge_stub(
                    name, tunnel_via="lane_status_board"
                )
                (prop / f"{name}.yaml").write_text(
                    yaml.dump(card, sort_keys=False), encoding="utf-8"
                )
            found = find_provisional_bridges_for_tunnel(root, "lane_status_board")
            self.assertEqual(len(found), 2)
            merged = merge_bridge_cards(
                [c for _, _, c in found],
                output_id="merged_bridge",
                tunnel_via="lane_status_board",
            )
            self.assertEqual(merged["touch"]["tunnel_via"], "lane_status_board")
            self.assertIn("lane_status_board", merged["touch"]["pairs_with"])

    def test_consolidate_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            weave = root / ".technical/weave"
            prop = weave / "component-proposals"
            weave.mkdir(parents=True, exist_ok=True)
            prop.mkdir(parents=True, exist_ok=True)
            (weave / "trinity-partition-registry.yaml").write_text(
                "schema_version: 1\npartitions:\n  maintenance:\n    bridges: []\n",
                encoding="utf-8",
            )
            for name in ("bridge_a", "bridge_b"):
                card = build_provisional_bridge_stub(
                    name, tunnel_via="lane_status_board"
                )
                (prop / f"{name}.yaml").write_text(
                    yaml.dump(card, sort_keys=False), encoding="utf-8"
                )
            out = run_trinity_bridge_consolidate(
                root,
                tunnel_via="lane_status_board",
                dry_run=True,
            )
            self.assertTrue(out.get("ok"))
            self.assertTrue(out.get("dry_run"))
            self.assertEqual(len(out.get("merged_from") or []), 2)


class TestRegistryUpsert(unittest.TestCase):
    def test_upsert_bridge_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            weave = root / ".technical/weave"
            weave.mkdir(parents=True)
            (weave / "trinity-partition-registry.yaml").write_text(
                "schema_version: 1\npartitions:\n  maintenance:\n    bridges: []\n",
                encoding="utf-8",
            )
            out = upsert_registry_bridge(
                root, trinity_id="test_bridge", dry_run=True
            )
            self.assertTrue(out.get("dry_run"))


class TestCardBacklog(unittest.TestCase):
    def test_usage_count_from_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            metrics = root / ".technical/weave/metrics.jsonl"
            metrics.parent.mkdir(parents=True)
            metrics.write_text(
                json.dumps({"trinity_id": "lane_status_board", "metric_type": "x"})
                + "\n"
                + json.dumps({"trinity_id": "lane_status_board", "metric_type": "y"})
                + "\n",
                encoding="utf-8",
            )
            counts = count_trinity_usage(root, lookback_days=None)
            self.assertEqual(counts.get("lane_status_board"), 2)

    def test_assess_skipped_when_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with mock.patch(
                "eat_queue_core.weave.trinity_card_backlog.load_trinity_config"
            ) as mcfg:
                mcfg.return_value.enabled = False
                out = assess_trinity_card_backlog(root, write_report=False)
            self.assertTrue(out.get("skipped"))

    def test_format_board_hint(self) -> None:
        md = format_backlog_board_hint(
            [{"trinity_id": "x", "priority_score": 12, "drift_score": 10, "usage_count": 2, "disconnect_kinds": []}]
        )
        self.assertIn("x", md)
        self.assertIn("priority", md)


if __name__ == "__main__":
    unittest.main()
