"""Phase 9 — weave self-wrap, spine enforcement graph, invariants, catchup delegate."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.invariant_registry import (
    PHASE9_INVARIANTS,
    bootstrap_phase9_invariants,
    load_invariant,
)
from eat_queue_core.weave.trinity_catchup_sweep import run_spine_catchup_handler
from eat_queue_core.weave.trinity_weave_self_wrap import (
    SPINE_ENFORCEMENT_GRAPH,
    assert_weave_entry_point,
    build_spine_enforcement_graph,
    maybe_pre_render_weave_hygiene,
    run_trinity_weave_self_wrap,
    write_spine_enforcement_graph,
)


class TestPhase9Graph(unittest.TestCase):
    def test_build_graph_has_entry_points(self) -> None:
        g = build_spine_enforcement_graph()
        self.assertEqual(g.get("phase"), 9)
        eps = g.get("entry_points") or []
        self.assertGreaterEqual(len(eps), 4)
        ids = {e.get("id") for e in eps if isinstance(e, dict)}
        self.assertIn("write_lane_status_board", ids)
        self.assertIn("headless_fanout_launch", ids)

    def test_write_graph_creates_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".technical" / "weave").mkdir(parents=True)
            out = write_spine_enforcement_graph(root, dry_run=False)
            path = root / out["path"]
            self.assertTrue(path.is_file())
            text = path.read_text(encoding="utf-8")
            self.assertIn("write_lane_status_board", text)


class TestPhase9Invariants(unittest.TestCase):
    def test_bootstrap_phase9_creates_rows(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = bootstrap_phase9_invariants(root)
            self.assertTrue(out.get("ok"))
            self.assertEqual(len(out.get("created") or []), len(PHASE9_INVARIANTS))
            for spec in PHASE9_INVARIANTS:
                ent = load_invariant(root, str(spec["id"]))
                self.assertIsNotNone(ent)


class TestPhase9SelfWrap(unittest.TestCase):
    def test_dry_run_skips_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(
                "weave:\n  trinity_enabled: true\n"
                "  trinity_weave_self_wrap_enabled: false\n",
                encoding="utf-8",
            )
            out = run_trinity_weave_self_wrap(root, dry_run=True)
            self.assertTrue(out.get("skipped"))

    def test_dry_run_align_only_when_partition_missing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text("weave:\n  trinity_enabled: true\n", encoding="utf-8")
            out = run_trinity_weave_self_wrap(
                root,
                dry_run=True,
                skip_enforce=True,
                skip_unclog=True,
                skip_observe=True,
                write_graph=True,
            )
            self.assertIn("graph", out)
            align = out.get("align_spine") or {}
            self.assertFalse(align.get("ok", True) is False and "error" not in align)

    def test_catchup_delegates_to_weave_wrap(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(
                "weave:\n  trinity_enabled: true\n"
                "  trinity_weave_self_wrap_enabled: false\n",
                encoding="utf-8",
            )
            out = run_spine_catchup_handler(
                root, {"handler": "run_trinity_weave_self_wrap", "dry_run": True}
            )
            self.assertIn("weave_self_wrap", out)
            self.assertTrue(out.get("ok"))


class TestPhase9Hooks(unittest.TestCase):
    def test_assert_entry_point_skipped_when_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text("weave:\n  trinity_enabled: false\n", encoding="utf-8")
            gate = assert_weave_entry_point(root, "headless_fanout_launch")
            self.assertTrue(gate.get("skipped"))

    def test_maybe_pre_render_none_when_clog_pass_off(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(
                "weave:\n  trinity_enabled: true\n"
                "  trinity_clog_pass_before_board: false\n",
                encoding="utf-8",
            )
            self.assertIsNone(maybe_pre_render_weave_hygiene(root))


class TestSpineEnforcementGraphStatic(unittest.TestCase):
    def test_charter_present(self) -> None:
        self.assertIn("locked spine", SPINE_ENFORCEMENT_GRAPH.get("charter", ""))
