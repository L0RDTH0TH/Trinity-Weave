"""Phase B — Trinity validation drill tests (temp vault; no live drill)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.config import load_trinity_config
from eat_queue_core.weave.trinity_touch_refresh import refresh_trinity_card
from eat_queue_core.weave.trinity_validation_drill import (
    DRILL_FUNCS,
    drill_trinity_enforcement_fault,
    drill_trinity_schema_v2,
    run_trinity_validation_drill,
)


def _write_trinity_config(root: Path) -> None:
    cfg = root / "3-Resources" / "Second-Brain-Config.md"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(
        """
```yaml
weave:
  enabled: true
  trinity_enabled: true
  trinity_checks_enabled: false
  trinity_block_on_stale_touch: true
  trinity_block_on_disconnect: true
  trinity_max_closure_paths: 21
  trinity_max_closure_hops: 3
```
""",
        encoding="utf-8",
    )


def _write_pilot_trio(root: Path) -> None:
    comp = root / ".technical/weave/components"
    comp.mkdir(parents=True, exist_ok=True)
    (root / ".technical/weave/concept-trinity-map.yaml").write_text(
        """
concepts:
  lane_board:
    trinity_id: lane_status_board
  lane_activity:
    trinity_id: lane_activity
  launch_registry:
    trinity_id: launch_registry_reconcile
""",
        encoding="utf-8",
    )
    snap = root / "scripts/eat_queue_core/lane_snapshot.py"
    snap.parent.mkdir(parents=True, exist_ok=True)
    snap.write_text("# stub\n", encoding="utf-8")
    tests = root / "scripts/eat_queue_core/tests"
    tests.mkdir(parents=True, exist_ok=True)
    (tests / "test_board_fixtures.py").write_text(
        "def test_receipt_success_only_idle_not_running():\n    pass\n",
        encoding="utf-8",
    )
    doc = root / "3-Resources/Second-Brain/Docs/Weave-Invariant-Registry.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("# registry\n", encoding="utf-8")

    cards = {
        "lane_status_board": """
id: lane_status_board
conceptual:
  summary: Board view over LaneSnapshot.
  primary_case: Display health after reconcile.
  refs:
    - "[[3-Resources/Second-Brain/Docs/Weave-Invariant-Registry]]"
touch:
  primary_paths:
    - scripts/eat_queue_core/lane_snapshot.py
  behavior_signals:
    - test_receipt_success_only_idle_not_running
rules:
  forbidden:
    - infer_run_from_receipt
  precedence:
    - Running state from resolve_lane_activity only
contract:
  proof:
    - scripts/eat_queue_core/tests/test_board_fixtures.py
meta:
  schema_version: 2
  conceptual_confirmed_at: "2026-01-01T00:00:00Z"
  rules_confirmed_at: "2026-01-01T00:00:00Z"
""",
        "lane_activity": """
id: lane_activity
conceptual:
  summary: Authoritative lane activity resolution.
  primary_case: resolve_lane_activity is source of truth.
touch:
  primary_paths:
    - scripts/eat_queue_core/lane_snapshot.py
rules:
  forbidden:
    - receipt_only_running
contract:
  proof:
    - scripts/eat_queue_core/tests/test_board_fixtures.py
meta:
  schema_version: 2
  conceptual_confirmed_at: "2026-01-01T00:00:00Z"
  rules_confirmed_at: "2026-01-01T00:00:00Z"
""",
        "launch_registry_reconcile": """
id: launch_registry_reconcile
conceptual:
  summary: Reconcile registry before board read.
  primary_case: Pre-read reconcile gate.
touch:
  primary_paths:
    - scripts/eat_queue_core/lane_snapshot.py
rules:
  forbidden:
    - skip_reconcile
contract:
  proof:
    - scripts/eat_queue_core/tests/test_board_fixtures.py
meta:
  schema_version: 2
  conceptual_confirmed_at: "2026-01-01T00:00:00Z"
  rules_confirmed_at: "2026-01-01T00:00:00Z"
""",
    }
    for tid, body in cards.items():
        (comp / f"{tid}.yaml").write_text(body.strip() + "\n", encoding="utf-8")


class TestTrinityValidationDrill(unittest.TestCase):
    def test_dry_run_all_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_trinity_config(root)
            _write_pilot_trio(root)
            out = run_trinity_validation_drill(root, dry_run=True, write_report=False)
            self.assertTrue(out["ok"], out)
            self.assertEqual(out["summary"]["failed"], 0)

    def test_schema_v2_drill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_trinity_config(root)
            _write_pilot_trio(root)
            out = drill_trinity_schema_v2(root)
            self.assertTrue(out["passed"], out)

    def test_enforcement_fault_drill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_trinity_config(root)
            _write_pilot_trio(root)
            tcfg = load_trinity_config(root)
            refresh_trinity_card(root, "lane_status_board", tcfg, dry_run=False)
            out = drill_trinity_enforcement_fault(root)
            self.assertTrue(out["passed"], out)

    def test_unknown_drill_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_trinity_config(root)
            out = run_trinity_validation_drill(root, drill="not_a_drill", write_report=False)
            self.assertFalse(out["ok"])
            self.assertEqual(out["error"], "unknown_drill")

    def test_drill_registry_complete(self) -> None:
        expected = {
            "schema_v2",
            "touch_refresh",
            "align_green",
            "pack_envelope",
            "conceptual_refs",
            "enforcement_fault",
            "component_scope",
        }
        self.assertEqual(set(DRILL_FUNCS.keys()), expected)


if __name__ == "__main__":
    unittest.main()
