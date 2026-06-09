"""Wave 2.5c — trinity_pack in context envelope."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.continuity_handoff import (
    append_context_envelope_to_handoff,
    build_context_envelope_yaml,
)
from eat_queue_core.handoff_build import build_handoff
from eat_queue_core.weave.trinity_pack import (
    build_trinity_pack,
    resolve_trinity_id,
    trinity_pack_from_queue_entry,
    trinity_pack_required,
)


def _write_config(root: Path) -> None:
    cfg = root / "3-Resources/Second-Brain-Config.md"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(
        """
```yaml
agent_continuity:
  enabled: true
weave:
  enabled: true
  trinity_enabled: true
  trinity_pack_mandatory_on_maintenance_lane: true
  trinity_max_closure_paths: 21
  trinity_max_closure_hops: 3
```
""",
        encoding="utf-8",
    )


def _write_cards(root: Path) -> None:
    from eat_queue_core.tests.test_weave_trinity_touch_refresh import _write_min_card

    _write_config(root)
    _write_min_card(root)
    meta = root / ".technical/weave/components/lane_status_board.yaml"
    text = meta.read_text(encoding="utf-8")
    text = text.replace("touch_content_hash: null", "touch_content_hash: abc123")
    text = text.replace("touch_refreshed_at: null", "touch_refreshed_at: '2026-05-30T00:00:00Z'")
    meta.write_text(text, encoding="utf-8")


class TrinityPackTests(unittest.TestCase):
    def test_resolve_maintenance_default(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_config(root)
            tid = resolve_trinity_id(root, lane="maintenance")
            self.assertEqual(tid, "lane_status_board")

    def test_resolve_concept_map(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_cards(root)
            (root / ".technical/weave/concept-trinity-map.yaml").write_text(
                "version: 1\nconcepts:\n  lane_run_status:\n    trinity_id: lane_status_board\n",
                encoding="utf-8",
            )
            tid = resolve_trinity_id(root, concept="lane_run_status")
            self.assertEqual(tid, "lane_status_board")

    def test_build_trinity_pack_has_must_read(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_cards(root)
            pack = build_trinity_pack(root, "lane_status_board", concept="lane_run_status")
            self.assertEqual(pack["trinity_id"], "lane_status_board")
            self.assertTrue(pack["touch"]["must_read"])
            self.assertIn("forbidden", pack["rules"])
            self.assertIn("summary", pack["conceptual"])

    def test_envelope_includes_trinity_pack_for_maintenance_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_cards(root)
            (root / ".technical/parallel/maintenance").mkdir(parents=True)
            (root / ".technical/parallel/maintenance/MEMORY.md").write_text("", encoding="utf-8")
            (root / ".technical/parallel/maintenance/continuity.md").write_text("", encoding="utf-8")
            h = build_handoff(root, "maintenance")
            self.assertIn("trinity_pack:", h)
            self.assertIn("must_read:", h)
            self.assertIn("misread_risks:", h)

    def test_queue_entry_params_trinity_id(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_cards(root)
            block, req = trinity_pack_from_queue_entry(
                root,
                {
                    "mode": "REFRESH_LANE_BOARD",
                    "params": {"trinity_id": "lane_status_board", "meta_only": True},
                },
                lane="maintenance",
            )
            self.assertIn("trinity_pack:", block)
            self.assertTrue(req)

    def test_trinity_required_on_operator_surface_mode(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_config(root)
            self.assertTrue(
                trinity_pack_required(
                    root,
                    queue_mode="OPERATOR_SURFACE_REPAIR",
                )
            )

    def test_build_context_envelope_yaml_maintenance(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_cards(root)
            (root / ".technical/parallel/curator").mkdir(parents=True)
            (root / ".technical/parallel/curator/MEMORY.md").write_text("x", encoding="utf-8")
            (root / ".technical/parallel/curator/continuity.md").write_text("y", encoding="utf-8")
            block = build_context_envelope_yaml(root, "maintenance")
            self.assertIn("trinity_pack:", block)
            self.assertIn("trinity_pack_mandatory: true", block)


if __name__ == "__main__":
    unittest.main()
