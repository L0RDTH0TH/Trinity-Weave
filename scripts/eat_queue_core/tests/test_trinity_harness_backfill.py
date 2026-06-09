"""Harness-backward extrapolation for Trinity proposals."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_card_generate import build_draft_card
from eat_queue_core.weave.trinity_harness_backfill import (
    analyze_module,
    resolve_primary_path_for_trinity_id,
)


class TestTrinityHarnessBackfill(unittest.TestCase):
    def test_resolve_harness_cmd_to_module(self) -> None:
        root = Path(__file__).resolve().parents[3]
        rel = resolve_primary_path_for_trinity_id(
            root,
            "harness_pseudo_clock_tick",
            "scripts/eat_queue_core/harness.py#cmd:pseudo_clock_tick",
        )
        self.assertEqual(rel, "scripts/eat_queue_core/pseudo_clock.py")

    def test_analyze_pseudo_clock_has_enforcement(self) -> None:
        root = Path(__file__).resolve().parents[3]
        bf = analyze_module(root, "scripts/eat_queue_core/pseudo_clock.py")
        self.assertIsNotNone(bf)
        assert bf is not None
        self.assertIn("pseudo_clock_tick", bf.harness_commands)
        self.assertTrue(any("pseudo-clock" in b.lower() or "Harness" in b for b in bf.enforcement_bullets))

    def test_analyze_rewrite_consumed_dual_track(self) -> None:
        from eat_queue_core.weave.trinity_harness_backfill import analyze_harness_command

        root = Path(__file__).resolve().parents[3]
        bf = analyze_harness_command(root, "rewrite_consumed")
        self.assertIsNotNone(bf)
        assert bf is not None
        self.assertEqual(bf.harness_commands, ["rewrite_consumed"])
        self.assertIn("full_cycle.py", bf.module_path)
        self.assertTrue(any("dual" in b.lower() or "filter" in b.lower() for b in bf.enforcement_bullets))

    def test_build_draft_card_applies_backfill(self) -> None:
        root = Path(__file__).resolve().parents[3]
        card, legs, _ = build_draft_card(
            root,
            trinity_id="harness_pseudo_clock_tick",
            component="pseudo_clock_tick",
            primary_path="scripts/eat_queue_core/harness.py#cmd:pseudo_clock_tick",
            source_kind="harness_cmd",
            anchors=[],
        )
        self.assertTrue(card["meta"]["source"].get("backfill_applied"))
        self.assertNotIn("TODO — operator", card["conceptual"]["outcome"])
        self.assertEqual(legs.conceptual, "draft")
        self.assertEqual(legs.rules, "present")

    def test_minimal_module_gets_generic_forbidden(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts/eat_queue_core").mkdir(parents=True)
            (root / "scripts/eat_queue_core/harness.py").write_text(
                "from .tiny import run as tiny_run\n"
                "def cmd_tiny(vault_root, args):\n"
                '    """Tiny cmd."""\n'
                "    tiny_run(vault_root)\n",
                encoding="utf-8",
            )
            (root / "scripts/eat_queue_core/tiny.py").write_text(
                '"""Tiny weave."""\ndef run(v):\n    return {"ok": True}\n',
                encoding="utf-8",
            )
            card, _, _ = build_draft_card(
                root,
                trinity_id="harness_tiny",
                component="tiny",
                primary_path="scripts/eat_queue_core/harness.py#cmd:tiny",
                source_kind="harness_cmd",
                anchors=[],
            )
            self.assertIn("Tiny", card["conceptual"]["outcome"])
            self.assertIn("tiny", card["touch"]["harness_commands"])


if __name__ == "__main__":
    unittest.main()
