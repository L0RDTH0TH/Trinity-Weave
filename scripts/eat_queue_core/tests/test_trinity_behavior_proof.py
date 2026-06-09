"""Trinity external proof — behavior_signals execution."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_align import check, check_pilot_disconnects
from eat_queue_core.weave.trinity_card import DISCONNECT_TOUCH_CONCEPTUAL_GAP
from eat_queue_core.weave.trinity_touch_refresh import load_trinity_card, refresh_trinity_card
from eat_queue_core.weave.config import load_trinity_config


def _write_min_config(root: Path) -> None:
    cfg = root / "3-Resources/Second-Brain-Config.md"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(
        """
```yaml
weave:
  trinity_enabled: true
  trinity_checks_enabled: true
  trinity_run_behavior_proofs: true
  trinity_run_behavior_proofs: true
  trinity_max_closure_paths: 21
  trinity_max_closure_hops: 3
```
""",
        encoding="utf-8",
    )


class TestTrinityBehaviorProof(unittest.TestCase):
    def test_touch_conceptual_gap_on_failing_behavior_signal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_min_config(root)
            comp = root / ".technical/weave/components"
            comp.mkdir(parents=True, exist_ok=True)
            (comp / "lane_activity.yaml").write_text(
                """
id: lane_activity
conceptual:
  summary: Run axis resolver
  primary_case: Forward momentum only
  outcome: resolve_lane_activity authoritative
touch:
  primary_paths:
    - scripts/eat_queue_core/lane_activity.py
  behavior_signals:
    - test_block_only_pq_lock_not_running
rules:
  forbidden:
  - block-only pq.lock implies running
  precedence:
  - pre_read reconcile before classify
contract:
  proof:
    - scripts/eat_queue_core/tests/test_lane_activity.py
meta:
  schema_version: 2
""",
                encoding="utf-8",
            )
            tests = root / "scripts/eat_queue_core/tests"
            tests.mkdir(parents=True, exist_ok=True)
            (root / "scripts/eat_queue_core/lane_activity.py").parent.mkdir(parents=True, exist_ok=True)
            (root / "scripts/eat_queue_core/lane_activity.py").write_text("# stub\n", encoding="utf-8")
            (tests / "test_lane_activity.py").write_text(
                "import unittest\nclass T(unittest.TestCase):\n"
                "    def test_block_only_pq_lock_not_running(self):\n"
                "        self.fail('intentional disconnect')\n",
                encoding="utf-8",
            )
            tcfg = load_trinity_config(root)
            refresh_trinity_card(root, "lane_activity", tcfg, dry_run=False)
            disc = check_pilot_disconnects(
                root,
                load_trinity_card(root, "lane_activity"),
                run_behavior_proofs=True,
            )
            kinds = {d.kind for d in disc}
            self.assertIn(DISCONNECT_TOUCH_CONCEPTUAL_GAP, kinds)
            result = check(root, "lane_activity")
            self.assertFalse(result.ok)
            self.assertFalse(result.legs.get("external_proof", True))


if __name__ == "__main__":
    unittest.main()
