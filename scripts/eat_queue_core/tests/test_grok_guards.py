"""Grok A–G guard modules — unit tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.corps_proof_adequacy import score_proof_adequacy
from eat_queue_core.weave.corps_repair_audit import card_content_hash
from eat_queue_core.weave.trinity_card_11a import doctrine_present_in_card, PHASE_11A_MARKER
from eat_queue_core.weave.corps_corpus_regenerate import run_regenerate_complete
from eat_queue_core.weave.trinity_corpus_restore import restore_cards_from_archive
from eat_queue_core.weave.trinity_provisional_corps_sweep import build_corps_pass_gate
from eat_queue_core.weave.weave_dry_run_preview import build_weave_dry_run_preview


class GrokGuardsTest(unittest.TestCase):
    def test_card_content_hash_stable(self) -> None:
        card = {"trinity_id": "x", "touch": {"primary_paths": ["a.py"]}}
        self.assertEqual(card_content_hash(card), card_content_hash(card))

    def test_11a_doctrine_detect(self) -> None:
        card = {
            "rules": {"precedence": ["policy: card_kind component"]},
            "meta": {PHASE_11A_MARKER: "v1"},
        }
        ok, _ = doctrine_present_in_card(card)
        self.assertTrue(ok)

    def test_restore_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            stamp = "20260101T120000Z"
            bundle = root / "4-Archives/Weave/Trinity-Corpus" / stamp / "cards"
            bundle.mkdir(parents=True)
            (bundle / "demo_card.yaml").write_text("trinity_id: demo_card\n", encoding="utf-8")
            out = restore_cards_from_archive(root, stamp=stamp, dry_run=True)
            self.assertTrue(out.get("ok"))
            self.assertIn("demo_card", out.get("restored_ids", []))

    def test_pass_gate_includes_proof_adequacy(self) -> None:
        nerve = {
            "ok": False,
            "counts": {"red": 1, "green": 1},
            "tier_failures": {"conduct": 1},
            "nerves": [
                {
                    "trinity_id": "a",
                    "status": "red",
                    "proof_adequacy": {"proof_adequacy_score": 0, "low_adequacy": True},
                },
                {
                    "trinity_id": "b",
                    "status": "green",
                    "proof_adequacy": {"proof_adequacy_score": 3, "low_adequacy": False},
                },
            ],
        }
        gate = build_corps_pass_gate(nerve, full_corpus=True)
        self.assertIn("proof_adequacy", gate)
        self.assertEqual(gate["proof_adequacy"].get("low_adequacy_count"), 1)

    def test_dry_run_preview_no_nerve_map(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = build_weave_dry_run_preview(Path(td), full_corpus=True)
            self.assertTrue(out.get("ok"))
            self.assertEqual((out.get("pass_gate") or {}).get("reason"), "no_corps_nerve_map")

    def test_adequacy_empty_card(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sc = score_proof_adequacy(Path(td), {"touch": {}, "conceptual": {}})
            self.assertEqual(sc["proof_adequacy_score"], 0)

    def test_regenerate_complete_cli_overrides_config_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            off = run_regenerate_complete(root, cli_requested=False)
            self.assertEqual(off.get("reason"), "corps_regenerate_complete_disabled")
            on = run_regenerate_complete(root, cli_requested=True, dry_run=True)
            self.assertNotEqual(on.get("reason"), "corps_regenerate_complete_disabled")


if __name__ == "__main__":
    unittest.main()
