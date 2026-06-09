"""Phase 2 — maintenance weave integration (trinity_pack anatomy, mode map, drill profile)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_pack import (
    enrich_maintenance_params,
    resolve_trinity_id,
    resolve_trinity_id_for_mode,
)
from eat_queue_core.weave.trinity_validation_drill import drill_profile_for


class TrinityPhase2WeaveTests(unittest.TestCase):
    def test_mode_resolves_bridge_and_bone(self) -> None:
        root = Path("/home/darth/Documents/Second-Brain")
        if not (root / ".technical/weave/trinity-partition-registry.yaml").is_file():
            self.skipTest("vault registry missing")
        self.assertEqual(
            resolve_trinity_id_for_mode(root, "GOVERNANCE_REVIEW"),
            "invariant_registry",
        )
        self.assertEqual(
            resolve_trinity_id_for_mode(root, "TRINITY_SPINE_CATCHUP"),
            "trinity_spine_maintenance",
        )
        self.assertEqual(
            resolve_trinity_id_for_mode(root, "GHOST_SKILL_AUDIT"),
            "ghost_skill_audit",
        )
        self.assertEqual(
            resolve_trinity_id(root, queue_mode="REFRESH_LANE_BOARD", lane="maintenance"),
            "lane_status_board",
        )

    def test_enrich_maintenance_params_sets_trinity_id(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".technical/weave").mkdir(parents=True)
            (root / ".technical/weave/concept-trinity-map.yaml").write_text(
                "version: 1\nconcepts:\n  shared_law:\n"
                "    trinity_id: invariant_registry\n"
                "    maintainer_modes: [GOVERNANCE_REVIEW]\n",
                encoding="utf-8",
            )
            comp = root / ".technical/weave/components"
            comp.mkdir(parents=True)
            comp.joinpath("invariant_registry.yaml").write_text(
                "id: invariant_registry\nmeta:\n  lock_kind: full\n"
                "  conceptual_confirmed_at: '2026-01-01'\n"
                "  rules_confirmed_at: '2026-01-01'\n"
                "conceptual: {}\nrules: {}\ntouch: {}\n",
                encoding="utf-8",
            )
            p = enrich_maintenance_params(root, "GOVERNANCE_REVIEW", {"meta_only": True})
            self.assertEqual(p.get("trinity_id"), "invariant_registry")

    def test_maintenance_set_profile_counts(self) -> None:
        root = Path("/home/darth/Documents/Second-Brain")
        reg = root / ".technical/weave/trinity-partition-registry.yaml"
        if not reg.is_file():
            self.skipTest("vault registry missing")
        ctx = drill_profile_for(root, "maintenance_set")
        self.assertEqual(ctx.name, "maintenance_set")
        self.assertEqual(len(ctx.component_ids), 14)
        self.assertEqual(len(ctx.bridge_ids), 2)
        self.assertEqual(len(ctx.all_ids), 16)


if __name__ == "__main__":
    unittest.main()
