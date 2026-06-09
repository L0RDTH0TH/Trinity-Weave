"""Trinity card v2 schema helpers and legacy v1 normalization."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_card import (
    contract_proof_paths,
    get_conceptual,
    get_rules,
    normalize_card,
    rules_forbidden_strings,
)


class TestTrinityCard(unittest.TestCase):
    def test_v2_card_passthrough(self) -> None:
        card = {
            "id": "x",
            "conceptual": {"summary": "s", "primary_case": "p"},
            "touch": {"primary_paths": ["a.py"]},
            "rules": {"forbidden": ["no foo"]},
            "contract": {"proof": ["a.py"]},
        }
        n = normalize_card(card)
        self.assertEqual(n["conceptual"]["summary"], "s")
        self.assertEqual(rules_forbidden_strings(n), ["no foo"])

    def test_v1_legacy_normalized(self) -> None:
        card = {
            "id": "x",
            "goal": {
                "invariant": "outcome line",
                "precedence_clauses": ["p1"],
                "proof": ["scripts/t.py"],
            },
            "impetus": {"summary": "s", "primary_case": "p"},
            "touch": {
                "primary_paths": ["a.py"],
                "behavior_signals": ["forbidden: bad thing", "test_x"],
            },
        }
        n = normalize_card(card)
        self.assertEqual(get_conceptual(n)["outcome"], "outcome line")
        self.assertIn("bad thing", rules_forbidden_strings(n))
        self.assertEqual(get_rules(n)["precedence"], ["p1"])
        self.assertEqual(contract_proof_paths(n), ["scripts/t.py"])


if __name__ == "__main__":
    unittest.main()
