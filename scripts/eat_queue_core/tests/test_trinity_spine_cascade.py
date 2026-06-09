"""Trinity spine cascade — conceptual forward growth from locked corpus."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from eat_queue_core.weave.trinity_conceptual_doctrine import (
    conceptual_has_meta_contamination,
    conceptual_needs_experiential_rewrite,
)
from eat_queue_core.weave.trinity_spine_cascade import (
    discover_cascade_targets,
    load_conceptual_corpus,
    run_trinity_spine_cascade,
    synthesize_conceptual_leg,
)


def _locked_card(tid: str, outcome: str) -> dict:
    return {
        "id": tid,
        "conceptual": {
            "outcome": outcome,
            "summary": f"Validated doctrine for {tid}.",
            "primary_case": "Operator locked this anchor.",
            "edge_cases": ["edge a"],
            "misread_risks": ["misread a"],
            "pairs_with": ["invariant_registry"],
        },
        "touch": {"primary_paths": [f"scripts/eat_queue_core/{tid}.py"]},
        "rules": {"forbidden": ["x"]},
        "contract": {"proof": []},
        "meta": {
            "conceptual_confirmed_at": "2026-06-01T00:00:00Z",
            "rules_confirmed_at": "2026-06-01T00:00:00Z",
        },
    }


class TestTrinitySpineCascade(unittest.TestCase):
    def test_corpus_loads_locked_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            comp = root / ".technical/weave/components"
            comp.mkdir(parents=True)
            (comp / "anchor.yaml").write_text(
                yaml.dump(_locked_card("anchor", "Anchor outcome."), sort_keys=False),
                encoding="utf-8",
            )
            draft = _locked_card("draft_only", "x")
            draft["meta"] = {}
            (comp / "draft_only.yaml").write_text(yaml.dump(draft, sort_keys=False), encoding="utf-8")
            corpus = load_conceptual_corpus(root)
            self.assertIn("anchor", corpus)
            self.assertNotIn("draft_only", corpus)

    def test_discovers_backfill_stub(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            comp = root / ".technical/weave/components"
            comp.mkdir(parents=True)
            (comp / "anchor.yaml").write_text(
                yaml.dump(_locked_card("anchor", "Anchor."), sort_keys=False),
                encoding="utf-8",
            )
            stub_dir = root / ".technical/weave/proposals/governance-set-v1/stubs"
            stub_dir.mkdir(parents=True)
            stub = {
                "id": "widget",
                "conceptual": {
                    "summary": "Backward extrapolation from implementation.",
                    "pairs_with": ["anchor"],
                },
                "touch": {"primary_paths": ["scripts/eat_queue_core/widget.py"]},
                "rules": {},
                "meta": {"card_class": "incomplete"},
            }
            (stub_dir / "widget.yaml").write_text(yaml.dump(stub, sort_keys=False), encoding="utf-8")
            (root / "scripts/eat_queue_core").mkdir(parents=True)
            (root / "scripts/eat_queue_core/widget.py").write_text('"""Widget module."""\n', encoding="utf-8")
            targets = discover_cascade_targets(root)
            self.assertEqual(len(targets), 1)
            self.assertEqual(targets[0].trinity_id, "widget")

    def test_run_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            comp = root / ".technical/weave/components"
            comp.mkdir(parents=True)
            (comp / "anchor.yaml").write_text(
                yaml.dump(_locked_card("anchor", "Anchor outcome."), sort_keys=False),
                encoding="utf-8",
            )
            stub_dir = root / ".technical/weave/proposals/governance-set-v1/stubs"
            stub_dir.mkdir(parents=True)
            (stub_dir / "widget.yaml").write_text(
                yaml.dump(
                    {
                        "id": "widget",
                        "conceptual": {"summary": "Backward extrapolation.", "pairs_with": ["anchor"]},
                        "touch": {"primary_paths": ["scripts/eat_queue_core/widget.py"]},
                        "meta": {"card_class": "incomplete"},
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            (root / "scripts/eat_queue_core").mkdir(parents=True)
            (root / "scripts/eat_queue_core/widget.py").write_text("# w\n", encoding="utf-8")
            out = run_trinity_spine_cascade(root, stamp="test-cascade", write_packs=False)
            self.assertTrue(out.get("ok"))
            self.assertEqual(out.get("written_count"), 1)
            prop = root / ".technical/weave/proposals/test-cascade"
            self.assertTrue((prop / "manifest.json").is_file())
            card = yaml.safe_load((prop / "stubs/widget.yaml").read_text(encoding="utf-8"))
            self.assertFalse(conceptual_needs_experiential_rewrite(card))
            self.assertFalse(conceptual_has_meta_contamination(card))
            self.assertFalse(conceptual_has_meta_contamination(card))
            self.assertIn("you", card["conceptual"].get("outcome", "").lower())
            self.assertNotIn("Backward extrapolation", card["conceptual"]["summary"])
            self.assertNotIn("conceptual_confirmed_at", card.get("meta") or {})
            sc = (card.get("meta") or {}).get("source", {}).get("spine_cascade", {})
            self.assertEqual(sc.get("voice"), "experiential_vantage")

    def test_synthesize_does_not_copy_backfill_marker(self) -> None:
        corpus = {"anchor": _locked_card("anchor", "A")["conceptual"]}
        card = {
            "id": "x",
            "conceptual": {"summary": "Backward extrapolation", "pairs_with": ["anchor"]},
            "touch": {"primary_paths": []},
        }
        leg = synthesize_conceptual_leg(Path("."), "x", card, ["anchor"], corpus)
        self.assertNotIn("Backward extrapolation", leg.get("summary", ""))
        self.assertNotIn("spine cascade", leg.get("summary", "").lower())
        self.assertTrue(leg.get("outcome"))


if __name__ == "__main__":
    unittest.main()
