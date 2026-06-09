"""Phase 14 — expand_self delta wrap tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[3]


class TestTrinityExpandSelf(unittest.TestCase):
    def test_parse_scope_ids(self) -> None:
        from eat_queue_core.weave.trinity_expand_self import parse_scope_ids

        self.assertEqual(parse_scope_ids("a,b, a"), ("a", "b"))
        self.assertEqual(parse_scope_ids(["x", "y"]), ("x", "y"))

    def test_blocks_maintenance_core_without_override(self) -> None:
        from eat_queue_core.weave.trinity_dual_lock import load_maintenance_core_policy
        from eat_queue_core.weave.trinity_expand_self import validate_expand_self_scope

        policy = load_maintenance_core_policy(VAULT_ROOT)
        if not policy.ids:
            self.skipTest("no maintenance core ids")
        tid = sorted(policy.ids)[0]
        out = validate_expand_self_scope(VAULT_ROOT, [tid], operator_override_scope=False)
        self.assertFalse(out.get("ok"))
        self.assertEqual(out["blocked"][0]["reason"], "maintenance_core")

    def test_forbids_regenerate_with_expand_self(self) -> None:
        from eat_queue_core.weave.trinity_weave_self_wrap import run_trinity_weave_self_wrap

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".technical/weave").mkdir(parents=True)
            out = run_trinity_weave_self_wrap(
                root,
                expand_self=True,
                expand_self_scope_ids=("fake_card",),
                regenerate_complete=True,
                dry_run=True,
            )
            self.assertFalse(out.get("ok"))
            self.assertEqual(out.get("error"), "expand_self_forbids_regenerate_complete")

    def test_resolve_empty_scope(self) -> None:
        from eat_queue_core.weave.trinity_expand_self import resolve_expand_self_scope

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".technical/weave/component-proposals").mkdir(parents=True)
            out = resolve_expand_self_scope(root, scope_ids=("missing_id",))
            self.assertEqual(out["resolved_ids"], [])
            self.assertEqual(out["missing_ids"], ["missing_id"])


if __name__ == "__main__":
    unittest.main()
