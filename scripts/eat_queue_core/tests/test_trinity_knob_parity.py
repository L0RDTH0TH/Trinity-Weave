"""Phase 16 — config_resolve_profile + knob parity matrix proofs."""

from __future__ import annotations

import unittest
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[3]


class TestConfigResolveProfile(unittest.TestCase):
    def test_default_bundle_expansion(self) -> None:
        from eat_queue_core.config_resolve_profile import resolve_profile

        res = resolve_profile({})
        self.assertEqual(res.familial["speed_mode"], "balance")
        self.assertEqual(res.expanded_flat.get("pipeline_mode"), "balance")
        self.assertEqual(
            res.expanded_flat.get("queue", {}).get("roadmap_pass_order"),
            "repair_first",
        )
        self.assertTrue(res.expanded_flat.get("validator", {}).get("tiered_blocks_enabled"))

    def test_combo_string_parsing(self) -> None:
        from eat_queue_core.config_resolve_profile import resolve_profile

        res = resolve_profile(
            {"speed_mode": "extreme + repair_strategy: forward_first + aggressive"}
        )
        self.assertEqual(res.familial["speed_mode"], "extreme")
        self.assertEqual(res.familial["repair_strategy"], "forward_first")
        self.assertEqual(res.familial["validator_tier"], "aggressive")
        self.assertEqual(res.expanded_flat.get("pipeline_mode"), "extreme")
        self.assertEqual(
            res.expanded_flat.get("queue", {}).get("roadmap_pass_order"),
            "forward_first",
        )

    def test_fast_gitforge_speed_mode(self) -> None:
        from eat_queue_core.config_resolve_profile import resolve_profile

        res = resolve_profile({"speed_mode": "fast"})
        self.assertEqual(res.expanded_flat.get("gitforge_effective_mode"), "speed")

    def test_single_knob_sweep_count(self) -> None:
        from eat_queue_core.config_resolve_profile import (
            CANONICAL_KNOB_FAMILIES,
            all_single_knob_sweeps,
        )

        expected = sum(len(v) for v in CANONICAL_KNOB_FAMILIES.values())
        self.assertEqual(len(all_single_knob_sweeps()), expected)


class TestTrinityKnobParity(unittest.TestCase):
    def test_matrix_all_green(self) -> None:
        from eat_queue_core.weave.trinity_knob_parity import build_matrix_cells

        cells = build_matrix_cells()
        self.assertGreater(len(cells), 0)
        red = [c for c in cells if not c.get("ok")]
        self.assertEqual(red, [], red)

    def test_run_proofs_writes_artifact(self) -> None:
        import tempfile

        from eat_queue_core.weave.trinity_knob_parity import (
            MATRIX_ARTIFACT,
            run_knob_parity_proofs,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".technical/weave/components").mkdir(parents=True)
            src = VAULT_ROOT / ".technical/weave/components/config_knob_parity.yaml"
            if src.is_file():
                (root / ".technical/weave/components/config_knob_parity.yaml").write_text(
                    src.read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            out = run_knob_parity_proofs(root, dry_run=False, write_artifact=True)
            self.assertTrue(out.get("ok"), out.get("red_cells"))
            self.assertTrue((root / MATRIX_ARTIFACT).is_file())

    def test_meta_drift_empty_on_live_vault(self) -> None:
        if not (VAULT_ROOT / ".technical/weave/components/config_knob_parity.yaml").is_file():
            self.skipTest("config_knob_parity not present")
        from eat_queue_core.weave.trinity_knob_parity import meta_knob_drift

        drift = meta_knob_drift(VAULT_ROOT)
        self.assertEqual(drift, [], drift)


if __name__ == "__main__":
    unittest.main()
