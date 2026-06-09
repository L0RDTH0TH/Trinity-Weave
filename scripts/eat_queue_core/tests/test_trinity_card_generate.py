"""Trinity card batch generator — discovery and proposals."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_card_generate import (
    LOCKED_SKIP_IDS,
    build_draft_card,
    parse_inventory_table,
    run_trinity_card_generate,
    slug_trinity_id,
)


class TestTrinityCardGenerate(unittest.TestCase):
    def test_slug_trinity_id(self) -> None:
        self.assertEqual(slug_trinity_id("L3 self-healing", "scripts/x.py"), "l3_self_healing")

    def test_draft_never_has_lock_stamps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts/eat_queue_core").mkdir(parents=True)
            (root / "scripts/eat_queue_core/foo.py").write_text("# x\n", encoding="utf-8")
            card, _, _ = build_draft_card(
                root,
                trinity_id="foo",
                component="Foo",
                primary_path="scripts/eat_queue_core/foo.py",
                source_kind="inventory_row",
                anchors=[],
            )
            meta = card.get("meta") or {}
            self.assertNotIn("conceptual_confirmed_at", meta)
            self.assertNotIn("rules_confirmed_at", meta)
            self.assertIn("source", meta)

    def test_run_generate_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inv = root / "3-Resources/Second-Brain/Docs"
            inv.mkdir(parents=True)
            inv.joinpath("Weave-Component-Inventory.md").write_text(
                """# Inv

| Component | Current path | `trinity_card` | Decision | Phase 0 note |
|---|---|---|---|---|
| Widget | `scripts/eat_queue_core/widget.py` | | `wrap` | note |
""",
                encoding="utf-8",
            )
            (root / "scripts/eat_queue_core").mkdir(parents=True)
            (root / "scripts/eat_queue_core/widget.py").write_text("x=1\n", encoding="utf-8")
            weave = root / ".technical/weave/components"
            weave.mkdir(parents=True)
            out = run_trinity_card_generate(root, dry_run=False, stamp="teststamp")
            self.assertTrue(out.get("ok"))
            self.assertGreaterEqual(out.get("total", 0), 1)
            prop = root / ".technical/weave/proposals/teststamp"
            self.assertTrue((prop / "manifest.json").is_file())
            self.assertTrue((prop / "index.md").is_file())
            manifest = json.loads((prop / "manifest.json").read_text(encoding="utf-8"))
            for p in manifest.get("proposals") or []:
                path = prop / p["output_path"]
                if path.is_file():
                    text = path.read_text(encoding="utf-8")
                    self.assertNotIn("conceptual_confirmed_at:", text)

    def test_parse_inventory_skips_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / "inv.md"
            p.write_text(
                "| Component | Current path | `trinity_card` | Decision | x |\n"
                "|---|---|---|---|---|\n"
                "| Foo | `a/b.py` | `foo` | `wrap` | n |\n",
                encoding="utf-8",
            )
            text = p.read_text()
            rows = []
            import re

            from eat_queue_core.weave import trinity_card_generate as tcg

            orig = tcg.INVENTORY_REL
            try:
                tcg.INVENTORY_REL = Path("inv.md")
                (root / "inv.md").write_text(text, encoding="utf-8")
                rows = tcg.parse_inventory_table(root)
            finally:
                tcg.INVENTORY_REL = orig
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0].trinity_id, "foo")

    def test_resolve_stamp_human_readable(self) -> None:
        from eat_queue_core.weave.trinity_card_generate import _default_stamp_dir

        self.assertTrue(_default_stamp_dir(True).endswith("-wide-net"))
        self.assertTrue(_default_stamp_dir(False).endswith("-narrow-net"))
        self.assertRegex(_default_stamp_dir(True), r"^\d{4}-\d{2}-\d{2}-wide-net$")


if __name__ == "__main__":
    unittest.main()
