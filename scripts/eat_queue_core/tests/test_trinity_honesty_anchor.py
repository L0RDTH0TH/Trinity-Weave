"""Phase 16 — honesty anchor claim-tier matrix proofs."""

from __future__ import annotations

import unittest
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[3]


class TestTrinityHonestyAnchor(unittest.TestCase):
    def test_classify_structural_pass_gate(self) -> None:
        from eat_queue_core.weave.trinity_honesty_anchor import classify_claim

        tier = classify_claim(
            {
                "pass_gate_ok": True,
                "conduct_ok": True,
                "counts": {"green": 1},
                "report_path": "r.json",
            }
        )
        self.assertEqual(tier, "structural")

    def test_narrative_success_fails_rules(self) -> None:
        from eat_queue_core.weave.trinity_honesty_anchor import evaluate_claim

        ok, errors, tier = evaluate_claim({"claimed_success": True, "status": "success"})
        self.assertFalse(ok)
        self.assertEqual(tier, "narrative")
        self.assertTrue(errors)

    def test_scenario_matrix_all_green(self) -> None:
        from eat_queue_core.weave.trinity_honesty_anchor import (
            evaluate_claim,
            scenario_fixtures,
        )

        for fix in scenario_fixtures():
            ok, _errors, tier = evaluate_claim(fix["payload"])
            self.assertEqual(ok, fix["expect_ok"], fix["id"])
            self.assertEqual(tier, fix["expect_tier"], fix["id"])

    def test_run_proofs_writes_artifact(self) -> None:
        import tempfile

        from eat_queue_core.weave.trinity_honesty_anchor import (
            MATRIX_ARTIFACT,
            run_honesty_anchor_proofs,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".technical/weave/components").mkdir(parents=True)
            src = VAULT_ROOT / ".technical/weave/components/maintenance_honesty_anchor.yaml"
            if src.is_file():
                (root / ".technical/weave/components/maintenance_honesty_anchor.yaml").write_text(
                    src.read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            out = run_honesty_anchor_proofs(root, dry_run=False, write_artifact=True)
            self.assertTrue(out.get("ok"), out.get("mismatches"))
            self.assertTrue((root / MATRIX_ARTIFACT).is_file())


class TestTrinityRedesignFactory(unittest.TestCase):
    def test_rust_grade_low_when_all_green(self) -> None:
        from eat_queue_core.weave.trinity_knob_parity import build_matrix_cells
        from eat_queue_core.weave.trinity_redesign_factory import rust_grade_factory

        cells = build_matrix_cells()
        grade = rust_grade_factory("queue_dispatch", cells)
        self.assertTrue(grade["known"])
        self.assertEqual(grade["rust_grade"], "low")
        self.assertTrue(grade["surgical_sufficient"])

    def test_ab_compare_alias_candidate(self) -> None:
        from eat_queue_core.weave.trinity_knob_parity import build_matrix_cells
        from eat_queue_core.weave.trinity_redesign_factory import compare_ab_structural

        cells = build_matrix_cells()
        out = compare_ab_structural("queue_dispatch", "queue_dispatch_v2", cells)
        self.assertTrue(out.get("ok"), out.get("error"))
        self.assertEqual(out.get("winner_structural"), "tie")
        self.assertTrue(out.get("candidate_is_alias"))

    def test_deprecate_requires_ack(self) -> None:
        import tempfile

        from eat_queue_core.weave.trinity_redesign_factory import run_redesign_factory

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = run_redesign_factory(
                root,
                legacy_factory_id="queue_dispatch",
                candidate_factory_id="queue_dispatch_v2",
                dry_run=True,
                operator_deprecate_ack=False,
            )
            self.assertIn("deprecate_skipped", out)

    def test_unknown_legacy_fails(self) -> None:
        from eat_queue_core.weave.trinity_knob_parity import build_matrix_cells
        from eat_queue_core.weave.trinity_redesign_factory import compare_ab_structural

        out = compare_ab_structural("not_a_factory", "queue_dispatch", build_matrix_cells())
        self.assertFalse(out.get("ok"))


if __name__ == "__main__":
    unittest.main()
