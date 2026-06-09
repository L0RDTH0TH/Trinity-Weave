"""Tests for meta-lens force-align on regenerate-complete."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

VAULT_ROOT = Path(__file__).resolve().parents[3]


class TestMetaLensRegen(unittest.TestCase):
    def test_gate_fails_without_prompt_context_card(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            from eat_queue_core.weave.trinity_meta_lens_regen import (
                validate_meta_lens_regen_prerequisites,
            )

            out = validate_meta_lens_regen_prerequisites(root)
            self.assertFalse(out.get("ok"))

    def test_gate_passes_on_vault(self) -> None:
        if not (VAULT_ROOT / ".technical/weave/components/trinity_prompt_context.yaml").is_file():
            self.skipTest("vault meta not present")
        from eat_queue_core.weave.trinity_meta_lens_regen import (
            validate_meta_lens_regen_prerequisites,
        )

        out = validate_meta_lens_regen_prerequisites(VAULT_ROOT)
        self.assertTrue(out.get("ok"))

    def test_apply_injects_precedence_and_card_kind(self) -> None:
        if not (VAULT_ROOT / ".technical/weave/components/trinity_prompt_context.yaml").is_file():
            self.skipTest("vault meta not present")
        from eat_queue_core.weave.trinity_meta_lens_regen import apply_meta_lens_force_align

        archived = {
            "id": "harness_demo_x",
            "conceptual": {"outcome": "keep me", "summary": "archived narrative"},
            "touch": {"primary_paths": ["scripts/eat_queue_core/harness.py"]},
            "rules": {"precedence": ["policy: archived local"]},
        }
        draft = {
            "id": "harness_demo_x",
            "conceptual": {"outcome": "generated"},
            "touch": {"primary_paths": ["scripts/eat_queue_core/wrong.py"]},
            "rules": {"precedence": ["policy: generator default"]},
            "meta": {"source": {}},
        }
        out = apply_meta_lens_force_align(VAULT_ROOT, draft, archived, "harness_demo_x")
        out.pop("_meta_lens_overlay", None)
        self.assertEqual(out["conceptual"]["outcome"], "keep me")
        self.assertEqual(out["touch"]["primary_paths"], archived["touch"]["primary_paths"])
        self.assertEqual(out["meta"]["card_kind"], "harness_entrypoint")
        self.assertTrue(out["rules"].get("meta_lens_force_align"))
        prec = out["rules"].get("precedence") or []
        self.assertTrue(any("meta_lens_force_align" in str(p) for p in prec))
        self.assertTrue(any("lens/config_knob_parity" in str(p) for p in prec))

    def test_regenerate_dry_run_with_lens_flag(self) -> None:
        if not (VAULT_ROOT / ".technical/weave/components/trinity_prompt_context.yaml").is_file():
            self.skipTest("vault meta not present")
        from eat_queue_core.weave.corps_corpus_regenerate import run_regenerate_complete

        out = run_regenerate_complete(
            VAULT_ROOT,
            dry_run=True,
            cli_requested=True,
            meta_lens_force_align=True,
        )
        self.assertTrue(out.get("meta_lens_force_align"))
        if out.get("would_archive_ids"):
            self.assertIn("meta_lens_sample", out)
            self.assertGreater(
                out["meta_lens_sample"]["delta"].get("precedence_added_count", 0),
                0,
            )


if __name__ == "__main__":
    unittest.main()
