"""Phase 5 — dual-lock constitution."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.trinity_card_paths import (
    components_dir,
    write_trinity_card,
)
from eat_queue_core.weave.trinity_dual_lock import (
    SystemMutationForbidden,
    assert_system_may_mutate,
    is_consumable_for_pack,
    is_maintenance_core_id,
    load_maintenance_core_policy,
    operator_mutation_ctx,
)
from eat_queue_core.weave.trinity_partition import REGISTRY_REL


def _minimal_registry() -> str:
    return """
schema_version: 1
maintenance_core:
  system_mutable: false
  include_meta: true
  ids:
    - lane_status_board
    - trinity_spine_maintenance
partitions:
  maintenance:
    components:
      - id: lane_status_board
        primary_anchor: scripts/eat_queue_core/lane_status_board.py
    bridges:
      - id: trinity_spine_maintenance
        status: locked
"""


class TestTrinityDualLock(unittest.TestCase):
    def test_core_id_from_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reg = root / REGISTRY_REL
            reg.parent.mkdir(parents=True, exist_ok=True)
            reg.write_text(_minimal_registry(), encoding="utf-8")
            policy = load_maintenance_core_policy(root)
            self.assertFalse(policy.system_mutable)
            self.assertIn("lane_status_board", policy.ids)
            self.assertTrue(is_maintenance_core_id(root, "lane_status_board"))
            self.assertFalse(is_maintenance_core_id(root, "other_card"))

    def test_write_core_blocked_without_operator(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reg = root / REGISTRY_REL
            reg.parent.mkdir(parents=True, exist_ok=True)
            reg.write_text(_minimal_registry(), encoding="utf-8")
            comp = components_dir(root)
            comp.mkdir(parents=True, exist_ok=True)
            (comp / "lane_status_board.yaml").write_text(
                "id: lane_status_board\nmeta:\n  lock_kind: maintenance_core\n"
                "  system_mutable: false\n",
                encoding="utf-8",
            )
            with self.assertRaises(SystemMutationForbidden):
                write_trinity_card(
                    root,
                    "lane_status_board",
                    {"id": "lane_status_board", "meta": {"x": 1}},
                )

    def test_write_core_allowed_with_operator_ctx(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reg = root / REGISTRY_REL
            reg.parent.mkdir(parents=True, exist_ok=True)
            reg.write_text(_minimal_registry(), encoding="utf-8")
            comp = components_dir(root)
            comp.mkdir(parents=True, exist_ok=True)
            (comp / "lane_status_board.yaml").write_text(
                "id: lane_status_board\nmeta: {}\n",
                encoding="utf-8",
            )
            token = operator_mutation_ctx.set(True)
            try:
                write_trinity_card(
                    root,
                    "lane_status_board",
                    {"id": "lane_status_board", "meta": {"touched": True}},
                    operator_override=True,
                )
            finally:
                operator_mutation_ctx.reset(token)
            assert_system_may_mutate(
                root, "lane_status_board", "test", operator_override=True
            )

    def test_consumable_core_requires_locked_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reg = root / REGISTRY_REL
            reg.parent.mkdir(parents=True, exist_ok=True)
            reg.write_text(_minimal_registry(), encoding="utf-8")
            self.assertFalse(is_consumable_for_pack(root, "lane_status_board"))
            comp = components_dir(root)
            comp.mkdir(parents=True, exist_ok=True)
            (comp / "lane_status_board.yaml").write_text(
                "id: lane_status_board\nmeta:\n"
                "  conceptual_confirmed_at: '2026-01-01'\n"
                "  rules_confirmed_at: '2026-01-01'\n",
                encoding="utf-8",
            )
            self.assertTrue(is_consumable_for_pack(root, "lane_status_board"))


if __name__ == "__main__":
    unittest.main()
