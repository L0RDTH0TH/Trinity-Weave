"""Anti-meta and experiential voice for Conceptual synthesis."""

from __future__ import annotations

import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_conceptual_doctrine import (
    conceptual_has_meta_contamination,
    synthesize_conceptual_human_vantage,
)


class TestTrinityConceptualDoctrine(unittest.TestCase):
    def test_synthesis_avoids_meta_terms(self) -> None:
        card = {
            "id": "decision_matrix_crafter",
            "conceptual": {"summary": "Backward extrapolation."},
            "touch": {
                "primary_paths": ["scripts/eat_queue_core/weave/foo.py"],
                "queue_modes": ["MAINTENANCE_CHECKLIST"],
            },
            "rules": {"forbidden": ["rm -rf", "inline pipeline"]},
        }
        leg = synthesize_conceptual_human_vantage(Path("."), "decision_matrix_crafter", card, [], {})
        blob = " ".join(str(leg.get(k) or "") for k in ("outcome", "summary", "primary_case"))
        self.assertFalse(conceptual_has_meta_contamination({"conceptual": leg}))
        self.assertNotIn("Touch", blob)
        self.assertNotIn("Rules", blob)
        self.assertNotIn("blast radius", blob.lower())
        self.assertTrue(len(leg.get("outcome", "")) > 20)

    def test_harness_eat_beats_match_gold_pattern(self) -> None:
        card = {"id": "harness_headless_eat", "touch": {}, "rules": {}}
        leg = synthesize_conceptual_human_vantage(Path("."), "harness_headless_eat", card, [], {})
        self.assertIn("stay free", leg["outcome"].lower())
        self.assertFalse(conceptual_has_meta_contamination({"conceptual": leg}))


if __name__ == "__main__":
    unittest.main()
