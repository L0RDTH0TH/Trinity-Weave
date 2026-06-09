"""Tests for Phase 13 lens-informed align and Phase 11 meta corpus charter."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[3]


class TestMetaCorpusCharter(unittest.TestCase):
    def test_charter_default_off(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "3-Resources").mkdir(parents=True)
            (root / "3-Resources" / "Second-Brain-Config.md").write_text(
                "weave:\n  trinity_meta_corpus_enabled: false\n"
                "  trinity_meta_corpus_charter_enabled: false\n"
                "  trinity_queue_payload_meta_deferred: true\n",
                encoding="utf-8",
            )
            from eat_queue_core.weave.trinity_meta_corpus import (
                meta_corpus_charter_status,
                resolve_meta_generation_load_ids,
            )

            status = meta_corpus_charter_status(root)
            self.assertTrue(status["ok"])
            self.assertFalse(status["trinity_meta_corpus_enabled"])
            self.assertFalse(status["trinity_meta_corpus_charter_enabled"])
            self.assertTrue(status["bulk_promote_deferred"])
            self.assertEqual(status["reason"], "charter_bulk_promote_off")
            self.assertEqual(resolve_meta_generation_load_ids(root), [])

    def test_charter_active_when_both_on(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "3-Resources").mkdir(parents=True)
            (root / "3-Resources" / "Second-Brain-Config.md").write_text(
                "weave:\n  trinity_meta_corpus_enabled: true\n"
                "  trinity_meta_corpus_charter_enabled: true\n",
                encoding="utf-8",
            )
            from eat_queue_core.weave.trinity_meta_corpus import (
                DEFAULT_META_GENERATION_LOAD_IDS,
                meta_corpus_charter_status,
                resolve_meta_generation_load_ids,
            )

            status = meta_corpus_charter_status(root)
            self.assertTrue(status["bulk_promote_active"])
            self.assertEqual(status["reason"], "charter_active")
            load_ids = resolve_meta_generation_load_ids(root)
            self.assertIn("maintenance_honesty_anchor", load_ids)
            self.assertIn("config_knob_parity", load_ids)
            self.assertEqual(len(load_ids), len(DEFAULT_META_GENERATION_LOAD_IDS))


class TestLensInformedAlign(unittest.TestCase):
    def test_load_mvl_bundle_skipped_when_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "3-Resources").mkdir(parents=True)
            (root / "3-Resources" / "Second-Brain-Config.md").write_text(
                "weave:\n  trinity_mvl_conductor_enabled: false\n",
                encoding="utf-8",
            )
            from eat_queue_core.weave.trinity_lens_informed_align import load_mvl_bundle

            out = load_mvl_bundle(root)
            self.assertTrue(out.get("skipped"))
            self.assertEqual(out.get("reason"), "mvl_conductor_disabled")

    def test_wiring_verification_detects_missing_prepend(self) -> None:
        from eat_queue_core.weave.trinity_lens_informed_align import (
            verify_meta_corpus_harness_wiring,
        )
        from eat_queue_core.weave.trinity_mvl_lens import LensContract

        lens = LensContract(
            source="locked",
            meta_prepend_order=("conceptual_style_guide",),
            task_meta_faces={},
            pull_leg_inclusion={},
            query_leg_inclusion={},
            forbidden=(),
            query_kinds=(),
        )
        wiring = verify_meta_corpus_harness_wiring(
            VAULT_ROOT, lens=lens, meta_legs={}
        )
        self.assertFalse(wiring["ok"])
        self.assertIn("maintenance_honesty_anchor", wiring["missing_prepend"])

    def test_load_mvl_bundle_on_vault(self) -> None:
        if not (VAULT_ROOT / ".technical/weave/components/trinity_prompt_context.yaml").is_file():
            self.skipTest("vault components not present")
        from eat_queue_core.weave.trinity_lens_informed_align import (
            load_mvl_bundle,
            run_lens_informed_align_gate,
        )

        bundle = load_mvl_bundle(VAULT_ROOT)
        self.assertTrue(bundle.get("ok"))
        self.assertTrue(bundle.get("wiring_ok"))
        self.assertEqual(bundle.get("lens_source"), "locked")
        self.assertIn("config_knob_parity", bundle.get("meta_prepend_order") or [])

        gate = run_lens_informed_align_gate(VAULT_ROOT)
        self.assertTrue(gate.get("ok"))
        self.assertTrue(gate.get("lens_informed_align"))

    def test_config_slice_includes_meta_corpus_flags(self) -> None:
        if not (VAULT_ROOT / "3-Resources/Second-Brain-Config.md").is_file():
            self.skipTest("config not present")
        from eat_queue_core.weave.trinity_mvl_lens import resolve_config_slice

        sl = resolve_config_slice(VAULT_ROOT)
        self.assertIn("trinity_meta_corpus_enabled", sl)
        self.assertIn("lens_informed_align_enabled", sl)
        self.assertFalse(sl["trinity_meta_corpus_enabled"])


if __name__ == "__main__":
    unittest.main()
