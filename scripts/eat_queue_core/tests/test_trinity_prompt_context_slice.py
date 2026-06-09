"""Tests for Phase 11b + 13 trinity_prompt_context_slice and MVL lens."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

VAULT_ROOT = Path(__file__).resolve().parents[3]


class TestTrinityRoute(unittest.TestCase):
    def test_eat_queue_routes_weave_cycle(self) -> None:
        from eat_queue_core.weave.trinity_prompt_context_slice import resolve_trinity_route

        r = resolve_trinity_route(Path("."), "EAT-QUEUE lane godot")
        self.assertEqual(r.trigger_class, "weave_cycle")
        self.assertEqual(r.task_kind, "weave_cycle")
        self.assertEqual(r.lane, "godot")
        self.assertIsNone(r.trinity_id)
        self.assertEqual(r.ingress_class, "command")

    def test_prompt_crafter_trigger(self) -> None:
        from eat_queue_core.weave.trinity_prompt_context_slice import resolve_trinity_route

        r = resolve_trinity_route(Path("."), "We are making a ROADMAP prompt")
        self.assertEqual(r.trigger_class, "prompt_crafter")
        self.assertEqual(r.task_kind, "prompt_crafter")

    def test_conduct_repair_extracts_harness_id(self) -> None:
        from eat_queue_core.weave.trinity_prompt_context_slice import resolve_trinity_route

        r = resolve_trinity_route(
            Path("."),
            "Fix conduct on harness_l3_validation_drill",
        )
        self.assertEqual(r.task_kind, "conduct_repair")
        self.assertEqual(r.trinity_id, "harness_l3_validation_drill")

    def test_ambiguous_asks_clarifying_question(self) -> None:
        from eat_queue_core.weave.trinity_prompt_context_slice import resolve_trinity_route

        r = resolve_trinity_route(Path("."), "hello there")
        self.assertEqual(r.trigger_class, "ambiguous_chat")
        self.assertIsNotNone(r.clarifying_question)

    def test_nerve_status_routes_query(self) -> None:
        from eat_queue_core.weave.trinity_prompt_context_slice import resolve_trinity_route

        r = resolve_trinity_route(Path("."), "Which harness cards are conduct red?")
        self.assertEqual(r.trigger_class, "weave_query")
        self.assertEqual(r.task_kind, "weave_query")
        self.assertEqual(r.query_kind, "nerve_status")
        self.assertEqual(r.ingress_class, "question")
        self.assertIsNone(r.trinity_id)


class TestPromptPull(unittest.TestCase):
    def test_pull_conduct_repair_includes_contract(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prop = root / ".technical" / "weave" / "component-proposals"
            prop.mkdir(parents=True)
            card = {
                "id": "demo_card",
                "conceptual": {"outcome": "claim", "summary": "principle"},
                "touch": {"primary_paths": ["scripts/eat_queue_core/demo.py"]},
                "rules": {"precedence": ["policy: test"]},
                "contract": {"proof": ["scripts/eat_queue_core/tests/test_demo.py"]},
            }
            (prop / "demo_card.yaml").write_text(
                yaml.safe_dump(card),
                encoding="utf-8",
            )
            from eat_queue_core.weave.trinity_prompt_context_slice import (
                resolve_prompt_context,
            )

            bundle = resolve_prompt_context(root, "demo_card", "conduct_repair")
            self.assertIn("contract", bundle.legs)
            self.assertIn("touch", bundle.legs)
            self.assertEqual(bundle.write_scope, "contract_proof_paths_only")


class TestMvlLens(unittest.TestCase):
    def test_locked_lens_prepend_includes_knob_parity(self) -> None:
        if not (VAULT_ROOT / ".technical/weave/components/trinity_prompt_context.yaml").is_file():
            self.skipTest("vault components not present")
        from eat_queue_core.weave.trinity_prompt_context_slice import resolve_prompt_context

        bundle = resolve_prompt_context(
            VAULT_ROOT,
            "trinity_spine_maintenance",
            "regen_burn",
            prefer="locked",
        )
        self.assertEqual(bundle.lens_source, "locked")
        self.assertIn("config_knob_parity", bundle.meta_prepend)
        self.assertIn("maintenance_honesty_anchor", bundle.meta_prepend)
        self.assertIn("host_execution_safety_contract", bundle.meta_prepend)
        self.assertIn("config_knob_parity", bundle.meta_legs)

    def test_query_readonly_no_write_scope(self) -> None:
        if not (VAULT_ROOT / ".technical/weave/components/trinity_prompt_context.yaml").is_file():
            self.skipTest("vault components not present")
        from eat_queue_core.weave.trinity_prompt_context_slice import resolve_trinity_query

        q = resolve_trinity_query(VAULT_ROOT, "consumable_check")
        self.assertEqual(q.write_scope, "read_only")
        self.assertIn("pull_write_scope", q.forbidden)
        self.assertIn("maintenance_honesty_anchor", q.meta_prepend)

    def test_mvl_probe_ok_on_vault(self) -> None:
        if not (VAULT_ROOT / ".technical/weave/components/trinity_prompt_context.yaml").is_file():
            self.skipTest("vault components not present")
        from eat_queue_core.weave.trinity_mvl_lens import probe_mvl_lens

        out = probe_mvl_lens(VAULT_ROOT)
        self.assertTrue(out.get("ok"))
        self.assertEqual(out.get("lens_source"), "locked")
        self.assertIn("config_knob_parity", out.get("meta_prepend_order") or [])


if __name__ == "__main__":
    unittest.main()
