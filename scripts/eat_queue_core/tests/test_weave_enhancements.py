"""Tests for Layer 1 maintenance branch, PQ cap, museum QR audit."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.full_cycle import run_full_eat_queue_cycle
from eat_queue_core.layer1_maintenance import (
    handle_maintenance_at_layer1,
    is_maintenance_mode,
    run_layer1_maintenance_pass,
)
from eat_queue_core.maintenance_io import append_maintenance_entry, maintenance_pq_path
from eat_queue_core.models import QueueEntry
from eat_queue_core.museum_qr_check import audit_museum_note, note_has_quick_reference
from eat_queue_core.plan import load_queue_file
from eat_queue_core.pq_headless_cap import apply_pq_cap, restore_pq_overflow


class EnhancementsTests(unittest.TestCase):
    def test_is_maintenance_mode(self) -> None:
        self.assertTrue(is_maintenance_mode("OPERATOR_ALERT"))
        self.assertFalse(is_maintenance_mode("INGEST_MODE"))

    def test_layer1_maintenance_pass_consumes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            append_maintenance_entry(
                root,
                mode="MAINTENANCE_NOTE",
                params={"meta_only": True, "detail": "test"},
            )
            out = run_layer1_maintenance_pass(root, max_entries=5, emit_watcher=False)
            self.assertEqual(out.get("processed"), 1)
            self.assertEqual(len(load_queue_file(maintenance_pq_path(root))), 0)

    def test_full_cycle_maintenance_short_circuit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pq = root / ".technical" / "parallel" / "maintenance" / "prompt-queue.jsonl"
            pq.parent.mkdir(parents=True)
            append_maintenance_entry(
                root,
                mode="OPERATOR_ALERT",
                params={"meta_only": True, "code": "test", "origin_lane": "curator"},
            )
            result = run_full_eat_queue_cycle(
                initial_action="deepen",
                initial_profile="balance",
                vault_root=root,
                queue_path=pq,
                lane_filter="maintenance",
                max_passes=1,
                emit_watcher_result=False,
            )
            self.assertEqual(result.passes_run, 1)
            self.assertEqual(len(result.plans), 0)
            self.assertTrue(result.execute_summaries)
            self.assertTrue(result.queue_empty_after_cleanup)

    def test_pq_cap_apply_and_restore(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = root / ".technical" / "parallel" / "curator"
            bundle.mkdir(parents=True)
            pq = bundle / "prompt-queue.jsonl"
            lines = [
                json.dumps({"id": f"e{i}", "mode": "INGEST_MODE", "params": {}})
                for i in range(8)
            ]
            pq.write_text("\n".join(lines) + "\n", encoding="utf-8")
            applied = apply_pq_cap(root, "curator", 3)
            self.assertTrue(applied.get("applied"))
            self.assertEqual(len(load_queue_file(pq)), 3)
            restored = restore_pq_overflow(root, "curator")
            self.assertEqual(restored.get("restored_lines"), 5)
            self.assertEqual(len(load_queue_file(pq)), 8)

    def test_museum_qr_detect_and_audit(self) -> None:
        good = "## Quick Reference\n\n| Item | Value |\n|------|-------|\n| path | 5-Attachments/Code-Repos/x/a.py |\n"
        bad = "## Summary\n\nNo QR here.\n"
        self.assertTrue(note_has_quick_reference(good))
        self.assertFalse(note_has_quick_reference(bad))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / "3-Resources" / "claw-code" / "Code-Exhibit" / "x.md"
            note.parent.mkdir(parents=True)
            note.write_text(bad, encoding="utf-8")
            rel = str(note.relative_to(root))
            out = audit_museum_note(root, rel, auto_record=True)
            self.assertFalse(out.get("has_quick_reference"))
            self.assertTrue(out.get("hook", {}).get("gap_appended"))


if __name__ == "__main__":
    unittest.main()
