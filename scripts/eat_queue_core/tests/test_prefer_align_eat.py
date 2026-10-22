"""Prefer-align live eat — blank fixture, not Genesis. No GREENLIGHT."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import yaml

from eat_queue_core.weave.factory.factory_lane_runner import run_factory_lane_job
from eat_queue_core.weave.factory.prefer_align import (
    discover_write_target_entries,
    run_prefer_align,
)
from eat_queue_core.weave.factory.prefer_weld_intent import evaluate_behavior_evidence

FIXTURE_PROJECT_ID = "fixture-project"
PACKET_KEY = "polygon_solid_identity_holds_after_select"


def _write_blank(root: Path, *, armed_extra: dict[str, Any] | None = None) -> str:
    pid = FIXTURE_PROJECT_ID
    bindings = root / "1-Projects" / pid / "Factory-DRB" / "bindings"
    bindings.mkdir(parents=True, exist_ok=True)
    (root / "1-Projects" / pid / "game").mkdir(parents=True, exist_ok=True)
    families = {
        "identity": {
            "project_id": pid,
            "game_repo_path": f"1-Projects/{pid}/game",
            "archive_path": "",
            "queue_lane": "factory",
            "release_checks": [],
        },
        "engine": {"adapter_id": "", "build_command": "", "ports": {}},
        "proof-catalog": {"probes": {}, "required_playtest_ids": []},
        "lanes": {"lane_ids": [], "order": []},
        "host-law": {"entries": []},
        "legacy-refuse": {"refuse_strings": []},
    }
    for fam, body in families.items():
        (bindings / f"{fam}.yaml").write_text(
            yaml.dump(body, sort_keys=False), encoding="utf-8"
        )
    # factory-project: eat latches only — no game_repo_path duplicate
    fp = root / f"1-Projects/{pid}/Factory-DRB/factory-project.yaml"
    fp.write_text(
        yaml.dump(
            {
                "schema_version": 1,
                "project_id": pid,
                "factory_greenlit": False,
                "factory_bootstrap": {"require_weave_track_coupled": False},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    armed: dict[str, Any] = {
        "proof_shape": "contract",
        "prefer_class": "foundation",
        "slice_id": "fixture_contract_slice",
        "host_law_ids": [],
        "behavior_keys": [PACKET_KEY],
        "structural_success": "identity key holds after select",
        "allowed_entries": [],
        "do_not_waive": ["explicit_met_implicit_miss"],
    }
    if armed_extra:
        armed.update(armed_extra)
    rel = f"1-Projects/{pid}/Factory-DRB/slice-briefs/fixture_contract.armed.yaml"
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(armed, sort_keys=False), encoding="utf-8")
    return rel


def _lane_patches():
    return [
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_factory_dispatch_preflight"
        ),
        patch(
            "eat_queue_core.weave.factory.implementation_cursor.reconcile_implementation_cursor",
        ),
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner.check_job_allowed",
        ),
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_interpretation_pass",
        ),
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner.append_gate_log",
        ),
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner.build_lane_agent_handoff",
            return_value=f"handoff contains {PACKET_KEY} but that is not evidence",
        ),
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_engine_preflight",
            return_value={"ok": True, "checks": []},
        ),
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_mcp_postedit_validate",
            return_value={},
        ),
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner.release_lane_job",
        ),
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner.append_factory_event",
        ),
        patch(
            "eat_queue_core.weave.factory.factory_lane_runner._persist_state",
        ),
    ]


class PreferAlignEatTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="prefer-align-"))

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.root, ignore_errors=True)

    def test_prefer_align_py_has_no_product_nouns(self) -> None:
        text = (
            Path(__file__).resolve().parents[1]
            / "weave/factory/prefer_align.py"
        ).read_text(encoding="utf-8")
        for tok in ("LaunchShell", "project.godot", "Townscaper", "Systems/"):
            self.assertNotIn(tok, text)

    def test_align_blocks_host_law_cite_without_ids(self) -> None:
        rel = _write_blank(
            self.root,
            armed_extra={
                "locks": {
                    "prefer_law": "Some-Host-Law",
                    "law_cite": "Factory-DRB/Some-Law.md",
                },
            },
        )
        armed = yaml.safe_load((self.root / rel).read_text(encoding="utf-8"))
        r = run_prefer_align(
            self.root, armed=armed, project_id=FIXTURE_PROJECT_ID, observed_entries=[]
        )
        self.assertFalse(r.ok)
        self.assertTrue(
            any("host_law_cite_without_host_law_ids" in v for v in r.violations)
        )

    def test_align_blocks_unnamed_discovered_entry(self) -> None:
        rel = _write_blank(self.root)
        # Product-shaped file Prefer did not name — discover must surface it.
        entry_name = "UnnamedEntry.tscn"
        (self.root / f"1-Projects/{FIXTURE_PROJECT_ID}/game" / entry_name).write_text(
            "[gd_scene]\n", encoding="utf-8"
        )
        found = discover_write_target_entries(
            self.root, f"1-Projects/{FIXTURE_PROJECT_ID}/game"
        )
        self.assertIn(entry_name, found)
        armed = yaml.safe_load((self.root / rel).read_text(encoding="utf-8"))
        r = run_prefer_align(
            self.root,
            armed=armed,
            project_id=FIXTURE_PROJECT_ID,
            observed_entries=found,
        )
        self.assertFalse(r.ok)
        self.assertTrue(
            any("unnamed_entries_present" in v for v in r.violations)
            or any("entry_not_named_by_prefer" in v for v in r.violations)
        )

    def test_factory_project_game_repo_disagree_blocks(self) -> None:
        rel = _write_blank(self.root)
        fp = self.root / f"1-Projects/{FIXTURE_PROJECT_ID}/Factory-DRB/factory-project.yaml"
        data = yaml.safe_load(fp.read_text(encoding="utf-8"))
        data["game_repo_path"] = "1-Projects/fixture-project/other-game"
        fp.write_text(yaml.dump(data, sort_keys=False), encoding="utf-8")
        armed = yaml.safe_load((self.root / rel).read_text(encoding="utf-8"))
        r = run_prefer_align(
            self.root, armed=armed, project_id=FIXTURE_PROJECT_ID, observed_entries=[]
        )
        self.assertFalse(r.ok)
        self.assertTrue(
            any("factory_project_game_repo_disagree" in v for v in r.violations)
        )

    def test_agent_flat_key_true_is_not_weld_intent_success(self) -> None:
        # Self-set {key: true} without pass_basis behavior is not Success.
        pack = {PACKET_KEY: True}
        beh = evaluate_behavior_evidence(
            pack,
            armed={
                "proof_shape": "contract",
                "prefer_class": "foundation",
                "behavior_keys": [PACKET_KEY],
            },
        )
        self.assertFalse(beh.ok)
        pack2 = {
            "pass_basis": "behavior",
            "behavior": {PACKET_KEY: True},
            "source": "agent",
        }
        beh2 = evaluate_behavior_evidence(
            pack2,
            armed={
                "proof_shape": "contract",
                "prefer_class": "foundation",
                "behavior_keys": [PACKET_KEY],
            },
        )
        self.assertFalse(beh2.ok)
        self.assertTrue(
            any("agent_sourced_evidence_pack" in v for v in beh2.violations)
        )

    def test_live_eat_blocks_before_agent_on_align_fail(self) -> None:
        rel = _write_blank(
            self.root,
            armed_extra={"locks": {"law_cite": "Factory-DRB/Some-Law.md"}},
        )
        called = {"agent": False}

        def _fake_agent(*_a: Any, **_k: Any) -> dict[str, Any]:
            called["agent"] = True
            return {"ok": True, "evidence_pack": {PACKET_KEY: True}}

        entry = {"id": "eat-1", "project_id": FIXTURE_PROJECT_ID, "params": {}}
        params = {
            "slice_id": "fixture_contract_slice",
            "lane_id": "implementation",
            "project_id": FIXTURE_PROJECT_ID,
            "armed_packet_path": rel,
            "repo_path": f"1-Projects/{FIXTURE_PROJECT_ID}/game",
            "observed_entries": [],
        }
        patches = _lane_patches()
        with patches[0] as mock_pf, patches[1] as mock_rec, patches[2] as mock_merge, patches[
            3
        ] as mock_interp, patches[4], patches[5], patches[6], patches[7], patches[
            8
        ], patches[9], patches[10]:
            from eat_queue_core.weave.factory.factory_dispatch_preflight import (
                DispatchPreflightResult,
            )

            mock_pf.return_value = DispatchPreflightResult(
                True, (), "ok", fail_closed=True
            )
            mock_rec.return_value = type(
                "R",
                (),
                {
                    "handoff_ready": True,
                    "handoff_reason": "",
                    "to_dict": lambda self: {},
                },
            )()
            mock_interp.return_value = type(
                "I",
                (),
                {
                    "ok": True,
                    "detail": "ok",
                    "to_dict": lambda self: {},
                    "little_val": type("LV", (), {"anti_pattern_violations": []})(),
                },
            )()
            mock_merge.return_value = type(
                "M", (), {"allowed": True, "to_dict": lambda self: {}}
            )()
            out = run_factory_lane_job(
                self.root,
                "factory",
                entry,
                params=params,
                run_agent_fn=_fake_agent,
                skip_preflight=True,
                complete_pipeline=False,
                auto_retry_seats=False,
            )
        self.assertFalse(out.get("ok"))
        self.assertEqual(out.get("error"), "prefer_align_failed")
        self.assertFalse(called["agent"])

    def test_live_eat_discovers_unnamed_entry_before_agent(self) -> None:
        rel = _write_blank(self.root)
        (self.root / f"1-Projects/{FIXTURE_PROJECT_ID}/game" / "OrphanEntry.tscn").write_text(
            "[gd_scene]\n", encoding="utf-8"
        )
        called = {"agent": False}

        def _fake_agent(*_a: Any, **_k: Any) -> dict[str, Any]:
            called["agent"] = True
            return {"ok": True}

        entry = {"id": "eat-discover", "project_id": FIXTURE_PROJECT_ID, "params": {}}
        params = {
            "slice_id": "fixture_contract_slice",
            "lane_id": "implementation",
            "project_id": FIXTURE_PROJECT_ID,
            "armed_packet_path": rel,
            "repo_path": f"1-Projects/{FIXTURE_PROJECT_ID}/game",
            "observed_entries": [],  # caller empty — discovery must still block
        }
        patches = _lane_patches()
        with patches[0] as mock_pf, patches[1] as mock_rec, patches[2] as mock_merge, patches[
            3
        ] as mock_interp, patches[4], patches[5], patches[6], patches[7], patches[
            8
        ], patches[9], patches[10]:
            from eat_queue_core.weave.factory.factory_dispatch_preflight import (
                DispatchPreflightResult,
            )

            mock_pf.return_value = DispatchPreflightResult(True, (), "ok")
            mock_rec.return_value = type(
                "R",
                (),
                {
                    "handoff_ready": True,
                    "handoff_reason": "",
                    "to_dict": lambda self: {},
                },
            )()
            mock_merge.return_value = type(
                "M", (), {"allowed": True, "to_dict": lambda self: {}}
            )()
            mock_interp.return_value = type(
                "I",
                (),
                {
                    "ok": True,
                    "detail": "ok",
                    "to_dict": lambda self: {},
                    "little_val": type("LV", (), {"anti_pattern_violations": []})(),
                },
            )()
            out = run_factory_lane_job(
                self.root,
                "factory",
                entry,
                params=params,
                run_agent_fn=_fake_agent,
                skip_preflight=True,
                complete_pipeline=False,
                auto_retry_seats=False,
            )
        self.assertFalse(out.get("ok"))
        self.assertEqual(out.get("error"), "prefer_align_failed")
        self.assertFalse(called["agent"])

    def test_live_eat_rejects_agent_evidence_pack(self) -> None:
        rel = _write_blank(self.root)

        def _agent_with_pack(*_a: Any, **_k: Any) -> dict[str, Any]:
            return {"ok": True, "evidence_pack": {PACKET_KEY: True}}

        def _agent_no_pack(*_a: Any, **_k: Any) -> dict[str, Any]:
            return {"ok": True, "handoff_echo": PACKET_KEY}

        entry = {"id": "eat-2", "project_id": FIXTURE_PROJECT_ID, "params": {}}
        params = {
            "slice_id": "fixture_contract_slice",
            "lane_id": "implementation",
            "project_id": FIXTURE_PROJECT_ID,
            "armed_packet_path": rel,
            "repo_path": f"1-Projects/{FIXTURE_PROJECT_ID}/game",
            "observed_entries": [],
        }
        patches = _lane_patches()
        with patches[0] as mock_pf, patches[1] as mock_rec, patches[2] as mock_merge, patches[
            3
        ] as mock_interp, patches[4], patches[5], patches[6], patches[7], patches[
            8
        ], patches[9], patches[10]:
            from eat_queue_core.weave.factory.factory_dispatch_preflight import (
                DispatchPreflightResult,
            )

            mock_pf.return_value = DispatchPreflightResult(True, (), "ok")
            mock_rec.return_value = type(
                "R",
                (),
                {
                    "handoff_ready": True,
                    "handoff_reason": "",
                    "to_dict": lambda self: {},
                },
            )()
            mock_merge.return_value = type(
                "M", (), {"allowed": True, "to_dict": lambda self: {}}
            )()
            mock_interp.return_value = type(
                "I",
                (),
                {
                    "ok": True,
                    "detail": "ok",
                    "to_dict": lambda self: {},
                    "little_val": type("LV", (), {"anti_pattern_violations": []})(),
                },
            )()

            stamped = run_factory_lane_job(
                self.root,
                "factory",
                entry,
                params=params,
                run_agent_fn=_agent_with_pack,
                skip_preflight=True,
                complete_pipeline=False,
                auto_retry_seats=False,
            )
            self.assertFalse(stamped.get("ok"))
            self.assertEqual(stamped.get("error"), "weld_intent_evidence_failed")
            self.assertIn(
                "weld_intent:agent_sourced_evidence_pack",
                stamped.get("evidence_violations") or [],
            )

            missing = run_factory_lane_job(
                self.root,
                "factory",
                {**entry, "id": "eat-3"},
                params=params,
                run_agent_fn=_agent_no_pack,
                skip_preflight=True,
                complete_pipeline=False,
                auto_retry_seats=False,
            )
            self.assertFalse(missing.get("ok"))
            self.assertEqual(missing.get("error"), "weld_intent_evidence_failed")


if __name__ == "__main__":
    unittest.main()
