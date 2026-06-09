"""Phase 1 verifier and governance fixtures for weave."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.lane_status_board import BOARD_REL, write_lane_status_board
from eat_queue_core.maintenance_handlers import handle_maintenance_entry
from eat_queue_core.maintenance_io import maintenance_pq_path
from eat_queue_core.weave.governance import lane_board_snapshot_path
from eat_queue_core.weave.verifier import verify_operator_surface_integrity


def _write_min_config(root: Path) -> None:
    cfg = root / "3-Resources/Second-Brain-Config.md"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(
        """
```yaml
parallel_execution:
  enabled: true
  default_to_legacy: false
  tracks:
    - id: institute
      lane: institute
      technical_subdir: parallel/institute
    - id: maintenance
      lane: maintenance
      lane_class: operational
      technical_subdir: parallel/maintenance
```
```yaml
weave:
  enabled: true
  governance_interval_days: 14
```
""",
        encoding="utf-8",
    )
    pol = root / ".technical/parallel/institute/orchestrator-policy.yaml"
    pol.parent.mkdir(parents=True, exist_ok=True)
    pol.write_text("paused_lanes: []\nstall_watch_lanes: []\n", encoding="utf-8")


class WeavePhase1VerifierTests(unittest.TestCase):
    def test_verifier_passes_on_generated_board(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_min_config(root)
            write_lane_status_board(root)
            vr = verify_operator_surface_integrity(root / BOARD_REL)
            self.assertTrue(vr.ok)

    def test_verifier_fails_when_section_missing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p = root / BOARD_REL
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("# Lane Status Board\n\n## At a glance\n", encoding="utf-8")
            vr = verify_operator_surface_integrity(p)
            self.assertFalse(vr.ok)
            self.assertIn(vr.code, ("token_missing", "section_missing"))

    def test_lane_snapshot_contains_content_hash(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_min_config(root)
            out = write_lane_status_board(root)
            snap = lane_board_snapshot_path(root)
            self.assertTrue(snap.is_file())
            row = json.loads(snap.read_text(encoding="utf-8"))
            self.assertTrue(bool(row.get("content_hash")))
            self.assertEqual(row.get("content_hash"), out.get("board_content_hash"))

    def test_governance_overdue_auto_queue_appends_line(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_min_config(root)
            out = write_lane_status_board(root)
            self.assertTrue(out.get("governance_overdue"))
            pq = maintenance_pq_path(root)
            self.assertTrue(pq.is_file())
            text = pq.read_text(encoding="utf-8")
            self.assertIn("GOVERNANCE_REVIEW", text)

    def test_operator_surface_repair_handler_wrapped_refresh(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write_min_config(root)
            out = handle_maintenance_entry(
                root,
                {
                    "id": "repair-1",
                    "mode": "OPERATOR_SURFACE_REPAIR",
                    "params": {"meta_only": True, "retry_eligible": True, "recovery_handler": "operator_surface_repair"},
                },
            )
            self.assertTrue(out.get("ok"))
            self.assertIn("operator_surface_repair", str(out.get("message")))


if __name__ == "__main__":
    unittest.main()
