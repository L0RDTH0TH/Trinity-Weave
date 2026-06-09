"""Phase 9/10 — symbolic scoping, corps sweep, combined cycle order."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from eat_queue_core.weave.invariant_registry import bootstrap_n2_invariants
from eat_queue_core.weave.symbolic_conflict import evaluate_symbolic_conflict
from eat_queue_core.weave.trinity_provisional_corps_sweep import (
    apply_corps_precedence_hygiene,
    build_corps_pass_gate,
    classify_nerve_status,
    _limit_provisional_ids,
    run_nerve_test_one,
)
from eat_queue_core.weave.trinity_weave_self_wrap import (
    _entry_point_invariant_ids,
    run_trinity_weave_self_wrap,
)


class TestSymbolicScoping(unittest.TestCase):
    def test_empty_invariant_set_skips_registry_global(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".technical" / "weave" / "invariants").mkdir(parents=True)
            bootstrap_n2_invariants(root)
            sym = evaluate_symbolic_conflict(
                root,
                context={"pre_read_steps": []},
                risk_tier="medium",
                invariant_ids=frozenset(),
            )
            self.assertEqual(sym.decision, "proceed")
            self.assertEqual(sym.temporal_inconsistencies, [])

    def test_registry_only_when_listed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".technical" / "weave" / "invariants").mkdir(parents=True)
            bootstrap_n2_invariants(root)
            sym = evaluate_symbolic_conflict(
                root,
                context={"pre_read_steps": ["reconcile_launch_registry"]},
                risk_tier="low",
                invariant_ids=frozenset({"registry_reconcile_pre_read"}),
            )
            self.assertEqual(sym.decision, "proceed")

    def test_entry_point_empty_invariants(self) -> None:
        ep = {"invariants": []}
        self.assertEqual(_entry_point_invariant_ids(ep), frozenset())


class TestCorpsHygiene(unittest.TestCase):
    def test_precedence_hygiene_migrates_forbidden(self) -> None:
        card = {
            "id": "demo",
            "touch": {"behavior_signals": []},
            "rules": {"forbidden": ["a", "b", "c"], "precedence": []},
        }
        out = apply_corps_precedence_hygiene(card)
        self.assertEqual(out["rules"]["forbidden"], [])
        self.assertTrue(any("policy: a" in p for p in out["rules"]["precedence"]))
        self.assertEqual(card["rules"]["forbidden"], ["a", "b", "c"])

    def test_precedence_hygiene_does_not_mutate_input(self) -> None:
        card = {
            "id": "demo",
            "touch": {"behavior_signals": []},
            "rules": {"forbidden": ["x", "y"], "precedence": []},
        }
        apply_corps_precedence_hygiene(card)
        self.assertEqual(card["rules"]["forbidden"], ["x", "y"])

    def test_yellow_advisory_only_when_conduct_pending_ok(self) -> None:
        st = classify_nerve_status(
            shape_ok=True,
            spine_ok=True,
            semantic_ok=True,
            conduct_ok=None,
            conduct_skipped=False,
            conduct_pending_ok=True,
        )
        self.assertEqual(st, "yellow")

    def test_red_when_conduct_unverified_strict_default(self) -> None:
        st = classify_nerve_status(
            shape_ok=True,
            spine_ok=True,
            semantic_ok=True,
            conduct_ok=None,
            conduct_skipped=False,
            conduct_pending_ok=False,
        )
        self.assertEqual(st, "red")

    def test_red_when_shape_fail(self) -> None:
        st = classify_nerve_status(
            shape_ok=False,
            spine_ok=True,
            semantic_ok=True,
            conduct_ok=True,
            conduct_skipped=False,
            conduct_pending_ok=True,
        )
        self.assertEqual(st, "red")

    def test_red_when_semantic_fail_conduct_skipped(self) -> None:
        st = classify_nerve_status(
            shape_ok=True,
            spine_ok=True,
            semantic_ok=False,
            conduct_ok=None,
            conduct_skipped=True,
            conduct_pending_ok=True,
        )
        self.assertEqual(st, "red")


class TestCorpsFullCorpusGate(unittest.TestCase):
    def test_limit_full_corpus_no_cap(self) -> None:
        ids = [f"id_{i}" for i in range(20)]
        limited, meta = _limit_provisional_ids(
            ids, full_corpus=True, max_cards=None, batch_size=7
        )
        self.assertEqual(limited, ids)
        self.assertTrue(meta["full_corpus"])
        self.assertEqual(meta["tested_count"], 20)

    def test_limit_sample_caps_at_batch(self) -> None:
        ids = [f"id_{i}" for i in range(20)]
        limited, meta = _limit_provisional_ids(
            ids, full_corpus=False, max_cards=None, batch_size=7
        )
        self.assertEqual(len(limited), 7)
        self.assertFalse(meta["full_corpus"])

    def test_pass_gate_fails_when_red_in_full_corpus(self) -> None:
        nerve = {
            "ok": False,
            "conduct_pending_ok": False,
            "counts": {"green": 3, "red": 1, "yellow": 0},
            "tier_failures": {"shape": 0, "spine": 0, "semantic": 1, "conduct": 0},
            "nerves": [{"trinity_id": "bad", "status": "red"}],
            "tested": 4,
        }
        gate = build_corps_pass_gate(nerve, full_corpus=True)
        self.assertFalse(gate["ok"])
        self.assertFalse(gate["semantic_ok"])
        self.assertEqual(gate["red_ids"], ["bad"])

    def test_pass_gate_tier_booleans_all_green(self) -> None:
        nerve = {
            "ok": True,
            "conduct_pending_ok": False,
            "counts": {"green": 2, "red": 0, "yellow": 0},
            "tier_failures": {"shape": 0, "spine": 0, "semantic": 0, "conduct": 0},
            "nerves": [],
            "tested": 2,
        }
        gate = build_corps_pass_gate(nerve, full_corpus=True)
        self.assertTrue(gate["ok"])
        self.assertTrue(gate["shape_ok"])
        self.assertTrue(gate["spine_ok"])
        self.assertTrue(gate["semantic_ok"])
        self.assertTrue(gate["conduct_ok"])

    def test_pass_gate_sample_mode_uses_nerve_ok(self) -> None:
        nerve = {
            "ok": True,
            "conduct_pending_ok": False,
            "counts": {"green": 7, "red": 0, "yellow": 0},
            "nerves": [],
            "tested": 7,
        }
        gate = build_corps_pass_gate(nerve, full_corpus=False)
        self.assertTrue(gate["ok"])
        self.assertFalse(gate["non_core_must_be_green"])


class TestCorpsRepairLoop(unittest.TestCase):
    def test_repair_loop_stops_when_no_changes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(
                "weave:\n  trinity_enabled: true\n"
                "  trinity_corps_sweep_enabled: true\n"
                "  trinity_corps_max_laps: 2\n"
                "  trinity_corps_max_llm_laps: 1\n",
                encoding="utf-8",
            )
            prop = root / ".technical/weave/component-proposals"
            prop.mkdir(parents=True)
            (prop / "demo_red.yaml").write_text(
                "id: demo_red\n"
                "conceptual:\n  summary: ''\n  primary_case: ''\n"
                "touch:\n  primary_paths: []\n  behavior_signals: []\n"
                "rules:\n  forbidden: []\n  precedence: []\n",
                encoding="utf-8",
            )
            from eat_queue_core.weave.corps_auto_repair import run_corps_sweep_with_repair_loop

            out = run_corps_sweep_with_repair_loop(
                root,
                full_corpus=True,
                max_laps=2,
                auto_repair=True,
                write_map=False,
            )
            loop = out.get("repair_loop") or {}
            self.assertGreaterEqual(loop.get("lap_count", 0), 1)
            self.assertEqual(loop.get("max_llm_laps"), 1)
            self.assertIn(
                loop.get("stop_reason"),
                ("pass_gate_green", "repair_stuck_no_changes", "max_laps", "repair_disabled_or_dry_run"),
            )


class TestNerveTierPoke(unittest.TestCase):
    def test_conduct_skipped_on_semantic_hard_fail(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(
                "weave:\n  trinity_enabled: true\n"
                "  trinity_corps_skip_conduct_on_semantic_fail: true\n"
                "  trinity_corps_max_llm_laps: 0\n",
                encoding="utf-8",
            )
            prop = root / ".technical/weave/component-proposals"
            prop.mkdir(parents=True)
            (prop / "empty_sem.yaml").write_text(
                "id: empty_sem\n"
                "conceptual:\n  summary: ''\n  primary_case: ''\n"
                "touch:\n  primary_paths: []\n  behavior_signals: []\n"
                "rules:\n  forbidden: []\n  precedence: []\n",
                encoding="utf-8",
            )
            row = run_nerve_test_one(
                root,
                "empty_sem",
                conduct_pending_ok=False,
                lap=1,
                max_llm_attempts=0,
            )
            tier = row.get("tier") or {}
            self.assertFalse(tier.get("semantic_ok"))
            self.assertTrue(tier.get("conduct_skipped"))
            self.assertIsNone(tier.get("conduct_ok"))
            self.assertFalse((row.get("conduct") or {}).get("behavior_proofs_ran"))


class TestCombinedCycle(unittest.TestCase):
    def test_cycle_order_in_report(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(
                "weave:\n  trinity_enabled: true\n"
                "  trinity_corps_sweep_enabled: false\n",
                encoding="utf-8",
            )
            out = run_trinity_weave_self_wrap(root, dry_run=True, skip_enforce=True)
            self.assertEqual(
                out.get("cycle_order"),
                [
                    "align_spine",
                    "unclog",
                    "regenerate_complete",
                    "corps_sweep",
                    "enforce_in_weave",
                    "observe",
                ],
            )


class TestOperatorOutcome(unittest.TestCase):
    def test_acceptance_audit_not_green_is_cycle_ok(self) -> None:
        from eat_queue_core.weave.trinity_weave_self_wrap import build_operator_outcome

        report = {
            "dry_run": False,
            "corps_full_corpus": True,
            "regenerate_complete_requested": False,
            "align_spine": {"ok": True},
            "unclog": {"ok": True},
            "pass_gate": {
                "ok": False,
                "conduct_ok": False,
                "counts": {"green": 117, "red": 4},
                "red_ids": ["harness_a", "harness_b"],
            },
            "corps_sweep": {"ok": False},
        }
        op = build_operator_outcome(report)
        self.assertTrue(op["cycle_ok"])
        self.assertFalse(op["pass_gate_ok"])
        self.assertEqual(op["operator_mode"], "acceptance_audit_only")
        self.assertIn("acceptance audit only", op["summary"])

    def test_regen_compensation_fail_is_not_cycle_ok(self) -> None:
        from eat_queue_core.weave.trinity_weave_self_wrap import build_operator_outcome

        report = {
            "dry_run": False,
            "corps_full_corpus": True,
            "regenerate_complete_requested": True,
            "regenerate_complete": {
                "ok": False,
                "test_compensation": {"compensation_ok": False, "verification_failures": [{}]},
            },
            "pass_gate": {"ok": False, "counts": {"red": 1}, "red_ids": ["x"]},
        }
        op = build_operator_outcome(report)
        self.assertFalse(op["cycle_ok"])
        joined = " ".join(op["infra_failures"])
        self.assertIn("test_compensation", joined)


class TestPytestBehaviorProof(unittest.TestCase):
    def test_pool_sync_proof_runs_via_pytest(self) -> None:
        vault = Path(__file__).resolve().parents[3]
        card = {
            "id": "pool_sync",
            "touch": {
                "primary_paths": ["scripts/eat_queue_core/pool_sync.py"],
                "behavior_signals": ["test_hydrate_filters_lane_and_shared"],
            },
            "contract": {
                "proof": ["scripts/eat_queue_core/tests/test_pool_sync.py"],
            },
        }
        from eat_queue_core.weave.trinity_behavior_proof import run_behavior_proof

        res = run_behavior_proof(vault, card, "test_hydrate_filters_lane_and_shared")
        self.assertTrue(res.ok, msg=res.detail)
        self.assertTrue((res.target or "").startswith("pytest:"))


class TestConductRepairRouting(unittest.TestCase):
    def test_split_conduct_only_reds(self) -> None:
        from eat_queue_core.weave.corps_auto_repair import _split_red_ids_for_repair

        nerves = {
            "conduct_red": {
                "tier": {
                    "shape_ok": True,
                    "spine_ok": True,
                    "semantic_ok": True,
                    "conduct_ok": False,
                    "conduct_skipped": False,
                }
            },
            "shape_red": {
                "tier": {
                    "shape_ok": False,
                    "spine_ok": True,
                    "semantic_ok": True,
                    "conduct_ok": None,
                    "conduct_skipped": False,
                }
            },
        }
        conduct, other = _split_red_ids_for_repair(
            ["conduct_red", "shape_red"],
            nerves,
        )
        self.assertEqual(conduct, ["conduct_red"])
        self.assertEqual(other, ["shape_red"])


class TestEnforcementUntrusted(unittest.TestCase):
    def test_enforce_skipped_when_conduct_not_ok(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(
                "weave:\n  trinity_enabled: true\n"
                "  trinity_corps_sweep_enabled: true\n"
                "  trinity_corps_sweep_before_enforce: true\n"
                "  trinity_corps_auto_repair_enabled: false\n"
                "  trinity_corps_self_wrap_full_corpus: true\n",
                encoding="utf-8",
            )
            from unittest.mock import patch

            fake_sweep = {
                "ok": False,
                "pass_gate": {
                    "ok": False,
                    "conduct_ok": False,
                    "shape_ok": True,
                    "spine_ok": True,
                    "semantic_ok": True,
                },
            }
            with patch(
                "eat_queue_core.weave.trinity_provisional_corps_sweep.run_trinity_provisional_corps_sweep",
                return_value=fake_sweep,
            ):
                out = run_trinity_weave_self_wrap(
                    root,
                    dry_run=False,
                    skip_align=True,
                    skip_unclog=True,
                    skip_observe=True,
                )
            self.assertTrue(out.get("provisional_enforcement_untrusted"))
            enforce = out.get("enforce_in_weave") or {}
            self.assertTrue(enforce.get("skipped"))
            self.assertIn("conduct_ok_false", enforce.get("reason", ""))


class TestConductSignalPrune(unittest.TestCase):
    def test_prune_drops_orphan_signals(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            tests = root / "scripts" / "eat_queue_core" / "tests"
            tests.mkdir(parents=True)
            proof = tests / "test_demo.py"
            proof.write_text(
                "def test_real_proof():\n    assert True\n",
                encoding="utf-8",
            )
            card = {
                "id": "demo",
                "touch": {
                    "primary_paths": ["scripts/eat_queue_core/demo.py"],
                    "behavior_signals": [
                        "test_orphan_name",
                        "test_real_proof",
                    ],
                },
                "contract": {"proof": ["scripts/eat_queue_core/tests/test_demo.py"]},
            }
            from eat_queue_core.weave.corps_conduct_repair import (
                prune_unresolved_behavior_signals,
            )

            out, changed, dropped = prune_unresolved_behavior_signals(root, card)
            self.assertTrue(changed)
            self.assertIn("test_orphan_name", dropped)
            sigs = (out.get("touch") or {}).get("behavior_signals") or []
            self.assertEqual(sigs, ["test_real_proof"])

    def test_prune_respects_locked_signals(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            card = {
                "id": "demo",
                "touch": {
                    "primary_paths": [],
                    "locked_behavior_signals": ["test_locked_orphan"],
                    "behavior_signals": ["test_locked_orphan"],
                },
                "contract": {"proof": []},
            }
            from eat_queue_core.weave.corps_conduct_repair import (
                prune_unresolved_behavior_signals,
            )

            out, changed, dropped = prune_unresolved_behavior_signals(root, card)
            self.assertFalse(changed)
            self.assertEqual(dropped, [])
            sigs = (out.get("touch") or {}).get("behavior_signals") or []
            self.assertEqual(sigs, ["test_locked_orphan"])


class TestCorpusRegenerate(unittest.TestCase):
    def test_classify_sole_owned_vs_shared(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prop = root / ".technical" / "weave" / "component-proposals"
            comp = root / ".technical" / "weave" / "components"
            prop.mkdir(parents=True)
            comp.mkdir(parents=True)
            tests = root / "scripts" / "eat_queue_core" / "tests"
            tests.mkdir(parents=True)
            sole = tests / "test_sole.py"
            shared = tests / "test_shared.py"
            sole.write_text("def test_sole():\n    pass\n", encoding="utf-8")
            shared.write_text("def test_shared():\n    pass\n", encoding="utf-8")

            import yaml

            (prop / "a.yaml").write_text(
                yaml.safe_dump(
                    {
                        "id": "a",
                        "touch": {"primary_paths": ["scripts/eat_queue_core/a.py"]},
                        "contract": {"proof": ["scripts/eat_queue_core/tests/test_sole.py"]},
                    }
                ),
                encoding="utf-8",
            )
            (prop / "b.yaml").write_text(
                yaml.safe_dump(
                    {
                        "id": "b",
                        "touch": {"primary_paths": ["scripts/eat_queue_core/b.py"]},
                        "contract": {"proof": ["scripts/eat_queue_core/tests/test_shared.py"]},
                    }
                ),
                encoding="utf-8",
            )
            (comp / "locked.yaml").write_text(
                yaml.safe_dump(
                    {
                        "id": "locked",
                        "meta": {
                            "conceptual_confirmed_at": "2026-01-01",
                            "rules_confirmed_at": "2026-01-01",
                        },
                        "touch": {"primary_paths": []},
                        "contract": {"proof": ["scripts/eat_queue_core/tests/test_shared.py"]},
                    }
                ),
                encoding="utf-8",
            )

            from eat_queue_core.weave.corps_corpus_regenerate import classify_test_ownership

            out = classify_test_ownership(root, ["a", "b"])
            self.assertIn(
                "scripts/eat_queue_core/tests/test_sole.py",
                out["sole_owned_tests"],
            )
            shared_rows = out["shared_anchors"]
            self.assertTrue(
                any(
                    r["proof_path"] == "scripts/eat_queue_core/tests/test_shared.py"
                    for r in shared_rows
                )
            )

    def test_production_module_not_sole_owned_on_regen(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prop = root / ".technical" / "weave" / "component-proposals"
            prop.mkdir(parents=True)
            mod = root / "scripts" / "eat_queue_core" / "orphan_module.py"
            mod.parent.mkdir(parents=True)
            mod.write_text("x = 1\n", encoding="utf-8")

            import yaml

            (prop / "only.yaml").write_text(
                yaml.safe_dump(
                    {
                        "id": "only",
                        "touch": {"primary_paths": ["scripts/eat_queue_core/orphan_module.py"]},
                        "contract": {"proof": ["scripts/eat_queue_core/orphan_module.py"]},
                    }
                ),
                encoding="utf-8",
            )

            from eat_queue_core.weave.corps_corpus_regenerate import classify_test_ownership

            out = classify_test_ownership(root, ["only"])
            self.assertNotIn(
                "scripts/eat_queue_core/orphan_module.py",
                out["sole_owned_tests"],
            )
            self.assertIn(
                "scripts/eat_queue_core/orphan_module.py",
                out["skipped_relocate_paths"],
            )

    def test_regenerate_complete_disabled_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = root / "3-Resources/Second-Brain-Config.md"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(
                "weave:\n  trinity_enabled: true\n"
                "  trinity_corps_regenerate_complete_enabled: false\n",
                encoding="utf-8",
            )
            from eat_queue_core.weave.corps_corpus_regenerate import run_regenerate_complete

            out = run_regenerate_complete(root)
            self.assertTrue(out.get("skipped"))
            self.assertEqual(out.get("reason"), "corps_regenerate_complete_disabled")

    def test_harness_dedupe_skip(self) -> None:
        from eat_queue_core.weave.corps_corpus_regenerate import _should_skip_harness_regen

        archive = {"pool_sync", "harness_pool_sync"}
        self.assertTrue(_should_skip_harness_regen("harness_pool_sync", archive))
        self.assertFalse(_should_skip_harness_regen("pool_sync", archive))
