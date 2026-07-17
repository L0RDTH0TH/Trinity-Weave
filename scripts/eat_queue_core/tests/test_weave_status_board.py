"""Tests for Weave Status Board PREVIEW (warehouse / factory model)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from eat_queue_core.lane_registry import build_lane_registry
from eat_queue_core.weave_status_board import PREVIEW_BOARD_REL, write_preview_weave_status_board
from eat_queue_core.weave_status_run import resolve_roadmap_run
from eat_queue_core.weave_status_snapshot import build_weave_status_snapshot


def _policy(root: Path, *, paused: list[str] | None = None) -> None:
    for lane in ("institute", "godot", "maintenance"):
        pol = root / ".technical" / "parallel" / lane / "orchestrator-policy.yaml"
        pol.parent.mkdir(parents=True, exist_ok=True)
        paused_lanes = paused or []
        pol.write_text(
            f"paused_lanes: {paused_lanes!r}\nstall_watch_lanes: []\n",
            encoding="utf-8",
        )


def _minimal_bundles(root: Path, lanes: tuple[str, ...] = ("maintenance", "institute", "godot")) -> None:
    for lane in lanes:
        b = root / ".technical" / "parallel" / lane
        b.mkdir(parents=True, exist_ok=True)
        (b / "prompt-queue.jsonl").write_text("", encoding="utf-8")


class WeaveStatusBoardPreviewTest(unittest.TestCase):
    def test_preview_sections(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _policy(root)
            (root / "1-Projects" / "demo").mkdir(parents=True)
            _minimal_bundles(root)
            result = write_preview_weave_status_board(root)
            self.assertTrue(result["ok"])
            text = (root / PREVIEW_BOARD_REL).read_text(encoding="utf-8")
            self.assertIn("## At a glance", text)
            self.assertIn("## Warehouses", text)
            self.assertIn("Maintenance warehouse", text)
            self.assertIn("CODE PARA warehouse", text)
            self.assertIn("Software warehouse", text)
            self.assertNotIn("## Lanes by project", text)
            self.assertIn("## Health history", text)
            self.assertIn("## Adaptive policy", text)
            self.assertNotIn("Knowledge Warehouse", text)
            sc = json.loads(
                (root / ".technical/weave/weave-status-snapshot-preview.json").read_text(encoding="utf-8")
            )
            self.assertEqual(sc["schema_version"], 3)
            self.assertIn("warehouses", sc)

    def test_dormant_sandbox_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _policy(root)
            (root / "1-Projects" / "live").mkdir(parents=True)
            _minimal_bundles(root, ("maintenance", "institute", "godot"))
            sb = root / ".technical" / "parallel" / "sandbox"
            sb.mkdir(parents=True, exist_ok=True)
            (sb / "prompt-queue.jsonl").write_text('{"id":"x","mode":"INGEST_MODE"}\n', encoding="utf-8")
            snap = build_weave_status_snapshot(root, preview=True)
            self.assertNotIn("sandbox", snap["active_lane_ids"])

    def test_roadmap_run_beats_stale_pause(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _policy(root, paused=["godot"])
            _minimal_bundles(root)
            with mock.patch(
                "eat_queue_core.weave_status_run._lane_has_live_activity",
                return_value=True,
            ):
                run, note = resolve_roadmap_run(root, execution_track="godot", expedition_status=None)
            self.assertEqual(run, "running")
            self.assertIsNone(note)

    def test_factory_rows_not_lane_seats(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _policy(root)
            (root / "1-Projects" / "genesis-mythos-master").mkdir(parents=True)
            _minimal_bundles(root)
            write_preview_weave_status_board(root)
            text = (root / PREVIEW_BOARD_REL).read_text(encoding="utf-8")
            self.assertIn("| Roadmap |", text)
            self.assertIn("| Implementation |", text)
            self.assertIn("| RE bench |", text)
            reg = build_lane_registry(root)
            for seat in ("module", "content", "presentation"):
                self.assertNotIn(f"| {seat} |", text.split("## Overnight")[0])

    def test_health_history_factory_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _policy(root)
            (root / "1-Projects" / "demo").mkdir(parents=True)
            for lane in ("maintenance", "institute", "godot"):
                b = root / ".technical/parallel" / lane
                b.mkdir(parents=True, exist_ok=True)
                (b / "prompt-queue.jsonl").write_text("", encoding="utf-8")
                samples = b / "lane_health_samples.jsonl"
                samples.write_text(
                    "\n".join(
                        [
                            '{"ts":"2026-06-25T10:00:00Z","health_score":80,"depth":1}',
                            '{"ts":"2026-06-26T10:00:00Z","health_score":70,"depth":2}',
                        ]
                    )
                    + "\n",
                    encoding="utf-8",
                )
            write_preview_weave_status_board(root)
            text = (root / PREVIEW_BOARD_REL).read_text(encoding="utf-8")
            self.assertIn("## Health history", text)
            self.assertIn("Weave maintenance", text)
            self.assertIn("CODE PARA", text)
            self.assertIn("Roadmap", text)
            history = text.split("## Health history")[1].split("## Audit")[0]
            self.assertNotIn("#### godot", history)
            self.assertNotIn("#### institute", history)
            self.assertNotIn("#### maintenance", history)


if __name__ == "__main__":
    unittest.main()
