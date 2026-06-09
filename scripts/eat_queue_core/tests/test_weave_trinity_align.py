"""Wave 2.5d — trinity_align leg checks and pilot disconnect rules."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.config import load_trinity_config
from eat_queue_core.weave.trinity_align import (
    apply_trinity_align_gate,
    check,
    check_pilot_disconnects,
    run_trinity_align,
)
from eat_queue_core.weave.trinity_touch_refresh import build_closure_manifest, refresh_trinity_card


def _write_config(root: Path, *, checks_enabled: bool = True) -> None:
    cfg = root / "3-Resources/Second-Brain-Config.md"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(
        f"""
```yaml
weave:
  enabled: true
  trinity_enabled: true
  trinity_checks_enabled: {str(checks_enabled).lower()}
  trinity_run_behavior_proofs: false
  trinity_block_on_stale_touch: true
  trinity_block_on_disconnect: true
  trinity_max_closure_paths: 21
  trinity_max_closure_hops: 3
```
""",
        encoding="utf-8",
    )


def _write_board_card(root: Path, *, behavior_signals: list[str] | None = None) -> None:
    comp = root / ".technical/weave/components"
    comp.mkdir(parents=True, exist_ok=True)
    signals = behavior_signals or [
        "test_receipt_success_only_idle_not_running",
        "test_fm_matches_table_run",
    ]
    sig_yaml = "\n".join(f"  - {s}" if not s.startswith("forbidden") else f'  - "{s}"' for s in signals)
    (comp / "lane_status_board.yaml").write_text(
        f"""
id: lane_status_board
conceptual:
  summary: Operator sees lane health without inferring live run from receipts.
  primary_case: Display health from LaneSnapshot after reconcile.
  outcome: Board is a view over LaneSnapshot kernel only.
touch:
  primary_paths:
    - scripts/eat_queue_core/lane_snapshot.py
  behavior_signals:
{sig_yaml}
rules:
  forbidden:
  - receipt tail alone implies Run
  - infer_run_from_receipt
  precedence:
  - Running state from resolve_lane_activity only
contract:
  proof:
    - scripts/eat_queue_core/tests/test_board_fixtures.py
meta:
  touch_content_hash: null
  touch_refreshed_at: null
  schema_version: 2
""",
        encoding="utf-8",
    )
    tests = root / "scripts/eat_queue_core/tests"
    tests.mkdir(parents=True, exist_ok=True)
    (tests / "test_board_fixtures.py").write_text(
        "def test_receipt_success_only_idle_not_running():\n    pass\n\n"
        "def test_fm_matches_table_run():\n    pass\n",
        encoding="utf-8",
    )
    snap = root / "scripts/eat_queue_core/lane_snapshot.py"
    snap.parent.mkdir(parents=True, exist_ok=True)
    snap.write_text("# stub\n", encoding="utf-8")


class TestTrinityAlign(unittest.TestCase):
    def test_stale_touch_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_config(root)
            _write_board_card(root)
            tcfg = load_trinity_config(root)
            refresh_trinity_card(root, "lane_status_board", tcfg, dry_run=False)
            result = check(root, "lane_status_board")
            self.assertFalse(result.stale_touch)
            from eat_queue_core.weave.trinity_touch_refresh import load_trinity_card

            card = load_trinity_card(root, "lane_status_board")
            card["meta"]["touch_content_hash"] = "deadbeef"
            path = root / ".technical/weave/components/lane_status_board.yaml"
            import yaml  # type: ignore[import-untyped]

            path.write_text(yaml.safe_dump(card, sort_keys=False), encoding="utf-8")
            result2 = check(root, "lane_status_board")
            self.assertTrue(result2.stale_touch)
            self.assertFalse(result2.ok)

    def test_precedence_collapse_forbidden_dominate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_config(root)
            _write_board_card(root)
            comp = root / ".technical/weave/components/lane_status_board.yaml"
            text = comp.read_text(encoding="utf-8")
            text = text.replace(
                "rules:\n  forbidden:\n  - receipt tail alone implies Run\n  - infer_run_from_receipt",
                "rules:\n  forbidden:\n  - f1\n  - f2\n  - f3\n  - f4",
            )
            text = text.replace(
                "  behavior_signals:\n    - test_receipt_success_only_idle_not_running\n    - test_fm_matches_table_run",
                "  behavior_signals:\n    - test_one",
            )
            comp.write_text(text, encoding="utf-8")
            disc = check_pilot_disconnects(root, load_trinity_card_from(root))
            kinds = {d.kind for d in disc}
            self.assertIn("precedence_collapse", kinds)

    def test_error_narrative_drift_code_hit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_config(root)
            _write_board_card(root)
            comp = root / ".technical/weave/components/lane_status_board.yaml"
            text = comp.read_text(encoding="utf-8")
            text = text.replace(
                "  - infer_run_from_receipt",
                "  - infer_run_from_receipt\n  fixtures: []\n  precedence:\n  - x",
            )
            comp.write_text(text, encoding="utf-8")
            py = root / "scripts/eat_queue_core/lane_snapshot.py"
            py.write_text("def infer_run_from_receipt():\n    return 'running'\n", encoding="utf-8")
            result = check(root, "lane_status_board")
            kinds = {d.kind for d in result.disconnects}
            self.assertIn("error_narrative_drift", kinds)

    def test_apply_gate_skipped_when_checks_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_config(root, checks_enabled=False)
            _write_board_card(root)
            gate = apply_trinity_align_gate(root, "lane_status_board")
            self.assertTrue(gate.get("skipped"))

    def test_apply_gate_blocks_on_disconnect(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_config(root, checks_enabled=True)
            _write_board_card(root)
            comp = root / ".technical/weave/components/lane_status_board.yaml"
            text = comp.read_text(encoding="utf-8")
            text = text.replace(
                "rules:\n  forbidden:\n  - receipt tail alone implies Run\n  - infer_run_from_receipt",
                "rules:\n  forbidden:\n  - a\n  - b\n  - c\n  - d",
            )
            text = text.replace(
                "  behavior_signals:\n    - test_receipt_success_only_idle_not_running\n    - test_fm_matches_table_run",
                "  behavior_signals:\n    - test_one",
            )
            comp.write_text(text, encoding="utf-8")
            gate = apply_trinity_align_gate(root, "lane_status_board", update_meta=False)
            self.assertFalse(gate.get("skipped"))
            self.assertFalse(gate.get("ok"))
            self.assertTrue(gate.get("blocked"))

    def test_run_trinity_align_writes_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_config(root)
            _write_board_card(root)
            tcfg = load_trinity_config(root)
            refresh_trinity_card(root, "lane_status_board", tcfg, dry_run=False)
            out = run_trinity_align(
                root,
                trinity_ids=["lane_status_board"],
                pilot_only=False,
                update_meta=False,
            )
            self.assertTrue(out.get("ok"))
            metrics = root / ".technical/weave/metrics.jsonl"
            self.assertTrue(metrics.is_file())
            rows = [json.loads(ln) for ln in metrics.read_text().splitlines() if ln.strip()]
            types = {r.get("metric_type") for r in rows}
            self.assertIn("trinity_align", types)


def load_trinity_card_from(root: Path):
    from eat_queue_core.weave.trinity_touch_refresh import load_trinity_card

    return load_trinity_card(root, "lane_status_board")


if __name__ == "__main__":
    unittest.main()
