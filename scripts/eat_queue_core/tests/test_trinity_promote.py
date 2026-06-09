"""Trinity provisional promotion and operator lock gate."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from eat_queue_core.weave.trinity_card_paths import (
    component_proposals_dir,
    components_dir,
    list_provisional_trinity_card_ids,
    load_trinity_card,
)
from eat_queue_core.weave.trinity_promote import (
    prepare_provisional_card,
    run_trinity_lock_card,
    run_trinity_promote_proposals,
)


class TestTrinityPromote(unittest.TestCase):
    def test_promote_writes_provisional_not_locked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            locked_dir = components_dir(root)
            locked_dir.mkdir(parents=True)
            locked = {
                "id": "anchor",
                "conceptual": {"outcome": "x"},
                "meta": {
                    "conceptual_confirmed_at": "Z",
                    "rules_confirmed_at": "Z",
                },
            }
            (locked_dir / "anchor.yaml").write_text(yaml.dump(locked, sort_keys=False), encoding="utf-8")

            stub_dir = root / ".technical/weave/proposals/batch/stubs"
            stub_dir.mkdir(parents=True)
            (stub_dir / "widget.yaml").write_text(
                yaml.dump(
                    {
                        "id": "widget",
                        "conceptual": {"outcome": "You win."},
                        "touch": {"primary_paths": []},
                        "meta": {"conceptual_confirmed_at": "SHOULD_STRIP"},
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

            out = run_trinity_promote_proposals(root, stamp="batch")
            self.assertTrue(out.get("ok"))
            self.assertEqual(out.get("promoted_count"), 1)

            prov = component_proposals_dir(root) / "widget.yaml"
            self.assertTrue(prov.is_file())
            card = yaml.safe_load(prov.read_text(encoding="utf-8"))
            self.assertTrue(card["meta"].get("provisional"))
            self.assertEqual(card["meta"].get("promotion_tier"), "provisional")
            self.assertNotIn("conceptual_confirmed_at", card["meta"])

            out2 = run_trinity_promote_proposals(root, stamp="batch")
            self.assertEqual(out2.get("skipped_locked"), 0)
            self.assertEqual(out2.get("skipped_exists"), 1)

    def test_lock_moves_to_components(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prov_dir = component_proposals_dir(root)
            prov_dir.mkdir(parents=True)
            card = prepare_provisional_card(
                {"id": "widget", "conceptual": {"outcome": "a"}, "touch": {}, "rules": {}},
                stamp="batch",
                source_rel="proposals/batch/stubs/widget.yaml",
            )
            (prov_dir / "widget.yaml").write_text(yaml.dump(card, sort_keys=False), encoding="utf-8")

            lock_out = run_trinity_lock_card(root, "widget")
            self.assertTrue(lock_out.get("ok"))
            self.assertTrue((components_dir(root) / "widget.yaml").is_file())
            self.assertFalse((prov_dir / "widget.yaml").is_file())
            locked = load_trinity_card(root, "widget", prefer="locked")
            self.assertTrue(locked["meta"].get("conceptual_confirmed_at"))


if __name__ == "__main__":
    unittest.main()
