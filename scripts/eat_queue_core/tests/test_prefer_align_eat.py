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
    evaluate_behavior_key_evidence,
    run_prefer_align,
)

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
                "locks": {"prefer_law": "Some-Host-Law", "law_cite": "Factory-DRB/Some-Law.md"},
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

    def test_align_blocks_unnamed_observed_entry(self) -> None:
        rel = _write_blank(self.root)
        armed = yaml.safe_load((self.root / rel).read_text(encoding="utf-8"))
        r = run_prefer_align(
            self.root,
            armed=armed,
            project_id=FIXTURE_PROJECT_ID,
            observed_entries=["DemoEntry.tscn"],
        )
        self.assertFalse(r.ok)
        self.assertTrue(any("unnamed_entries_present" in v for v in r.violations))

    def test_align_blocks_factory_project_game_repo_disagree(self) -> None:
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

    def test_evidence_pack_not_handoff_text(self) -> None:
        ok, viol = evaluate_behavior_key_evidence(
            [PACKET_KEY], {"keys_ok": True}
        )
        self.assertFalse(ok)
        ok2, _ = evaluate_behavior_key_evidence(
            [PACKET_KEY], {PACKET_KEY: True}
        )
        self.assertTrue(ok2)
        ok3, _ = evaluate_behavior_key_evidence(
            [PACKET_KEY], {PACKET_KEY: False}
        )
        self.assertFalse(ok3)

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
        with patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_factory_dispatch_preflight"
        ) as mock_pf, patch(
            "eat_queue_core.weave.factory.implementation_cursor.reconcile_implementation_cursor",
        ) as mock_rec, patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_interpretation_pass",
        ) as mock_interp, patch(
            "eat_queue_core.weave.factory.factory_lane_runner._persist_state",
        ), patch(
            "eat_queue_core.weave.factory.factory_lane_runner.append_gate_log",
        ), patch(
            "eat_queue_core.weave.factory.factory_lane_runner.check_job_allowed",
        ) as mock_merge:
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
            from eat_queue_core.weave.factory.factory_dispatch_preflight import (
                DispatchPreflightResult,
            )

            mock_pf.return_value = DispatchPreflightResult(
                True, (), "ok", fail_closed=True
            )
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

    def test_live_eat_green_requires_evidence_pack_not_handoff(self) -> None:
        rel = _write_blank(self.root)

        def _agent_handoff_only(*_a: Any, **_k: Any) -> dict[str, Any]:
            # Agent "ok" but no evidence pack — handoff text is not evidence.
            return {"ok": True, "handoff_echo": PACKET_KEY}

        def _agent_with_pack(*_a: Any, **_k: Any) -> dict[str, Any]:
            return {"ok": True, "evidence_pack": {PACKET_KEY: True}}

        entry = {"id": "eat-2", "project_id": FIXTURE_PROJECT_ID, "params": {}}
        params = {
            "slice_id": "fixture_contract_slice",
            "lane_id": "implementation",
            "project_id": FIXTURE_PROJECT_ID,
            "armed_packet_path": rel,
            "repo_path": f"1-Projects/{FIXTURE_PROJECT_ID}/game",
            "observed_entries": [],
        }
        with patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_factory_dispatch_preflight"
        ) as mock_pf, patch(
            "eat_queue_core.weave.factory.implementation_cursor.reconcile_implementation_cursor",
        ) as mock_rec, patch(
            "eat_queue_core.weave.factory.factory_lane_runner.check_job_allowed"
        ) as mock_merge, patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_interpretation_pass",
        ) as mock_interp, patch(
            "eat_queue_core.weave.factory.factory_lane_runner.append_gate_log",
        ), patch(
            "eat_queue_core.weave.factory.factory_lane_runner.build_lane_agent_handoff",
            return_value=f"handoff contains {PACKET_KEY} but that is not evidence",
        ), patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_engine_preflight",
            return_value={"ok": True, "checks": []},
        ), patch(
            "eat_queue_core.weave.factory.factory_lane_runner.run_mcp_postedit_validate",
            return_value={},
        ), patch(
            "eat_queue_core.weave.factory.factory_lane_runner.release_lane_job",
        ), patch(
            "eat_queue_core.weave.factory.factory_lane_runner.append_factory_event",
        ), patch(
            "eat_queue_core.weave.factory.factory_lane_runner._persist_state",
        ):
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

            miss = run_factory_lane_job(
                self.root,
                "factory",
                entry,
                params=params,
                run_agent_fn=_agent_handoff_only,
                skip_preflight=True,
                complete_pipeline=False,
                auto_retry_seats=False,
            )
            self.assertFalse(miss.get("ok"))
            self.assertEqual(miss.get("error"), "behavior_key_evidence_failed")

            hit = run_factory_lane_job(
                self.root,
                "factory",
                {**entry, "id": "eat-3"},
                params=params,
                run_agent_fn=_agent_with_pack,
                skip_preflight=True,
                complete_pipeline=False,
                auto_retry_seats=False,
            )
            self.assertNotEqual(hit.get("error"), "prefer_align_failed")
            self.assertNotEqual(hit.get("error"), "behavior_key_evidence_failed")


if __name__ == "__main__":
    unittest.main()
