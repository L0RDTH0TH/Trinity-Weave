"""Prefer-align + post-weld compare — blank fixture via live lane path. No GREENLIGHT."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import yaml

from eat_queue_core.weave.factory.factory_lane_runner import run_factory_lane_job
from eat_queue_core.weave.factory.prefer_align import run_prefer_align
from eat_queue_core.weave.factory.proof_runner import run_named_probes

FIXTURE_PROJECT_ID = "fixture-project"
PACKET_KEY = "identity_holds_after_select"
PROBE_COMPARE = "fixture_select_identity_compare"
PROBE_EXIT_ONLY = "fixture_exit_only"
PROBE_LITERAL = "fixture_literal_equals"
SOLID_ID = "solid-dyn-fixture-9f3a"


_HONEST_ENTRYPOINT = """\
import sys
import yaml
from pathlib import Path

idx = None
argv = sys.argv[1:]
if "--index" in argv:
    idx = int(argv[argv.index("--index") + 1])
else:
    raise SystemExit(2)
state = yaml.safe_load(Path("state/solids.yaml").read_text(encoding="utf-8"))
print(state["solids"][idx]["id"])
"""

_CONSTANT_ENTRYPOINT = f'print("{SOLID_ID}")\n'
_ECHO_ARG_ENTRYPOINT = """\
import sys
argv = sys.argv[1:]
# Echo selector index — must fail
if "--index" in argv:
    print(argv[argv.index("--index") + 1])
else:
    print("nope")
"""


def _write_blank(
    root: Path,
    *,
    armed_extra: dict[str, Any] | None = None,
    probes: dict[str, Any] | None = None,
    with_checks: bool = True,
    entrypoint_body: str | None = None,
    solid_id: str = SOLID_ID,
) -> str:
    pid = FIXTURE_PROJECT_ID
    bindings = root / "1-Projects" / pid / "Factory-DRB" / "bindings"
    bindings.mkdir(parents=True, exist_ok=True)
    game = root / "1-Projects" / pid / "game"
    game.mkdir(parents=True, exist_ok=True)
    (game / "state").mkdir(parents=True, exist_ok=True)
    (game / "state" / "solids.yaml").write_text(
        yaml.dump({"solids": [{"id": solid_id}]}, sort_keys=False),
        encoding="utf-8",
    )
    default_probes = {
        PROBE_COMPARE: {
            "op": "entrypoint_result_equals",
            "argv": ["python3", "tools/select_probe.py"],
            "selector": {"index": 0},
            "equals_from": {"path": "state/solids.yaml", "key": "solids.0.id"},
        },
        PROBE_EXIT_ONLY: {
            "op": "command_exits_zero",
            "argv": ["python3", "-c", "raise SystemExit(0)"],
        },
        PROBE_LITERAL: {
            "op": "entrypoint_result_equals",
            "argv": ["python3", "tools/select_probe.py"],
            "selector": {"index": 0},
            "equals": solid_id,
        },
    }
    families = {
        "identity": {
            "project_id": pid,
            "game_repo_path": f"1-Projects/{pid}/game",
            "archive_path": "",
            "queue_lane": "factory",
            "release_checks": [],
        },
        "engine": {"adapter_id": "", "build_command": "", "ports": {}},
        "proof-catalog": {
            "probes": probes if probes is not None else default_probes,
            "required_playtest_ids": [],
        },
        "lanes": {"lane_ids": [], "order": []},
        "host-law": {"entries": []},
        "legacy-refuse": {"refuse_strings": []},
    }
    for fam, body in families.items():
        (bindings / f"{fam}.yaml").write_text(
            yaml.dump(body, sort_keys=False), encoding="utf-8"
        )
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
    tools = game / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    (tools / "select_probe.py").write_text(
        entrypoint_body if entrypoint_body is not None else _HONEST_ENTRYPOINT,
        encoding="utf-8",
    )

    armed: dict[str, Any] = {
        "proof_shape": "contract",
        "prefer_class": "foundation",
        "slice_id": "fixture_contract_slice",
        "host_law_ids": [],
        "behavior_keys": [PACKET_KEY],
        "structural_success": "identity holds after select",
        "allowed_entries": [
            "tools/select_probe.py",
            "state/solids.yaml",
        ],
        "do_not_waive": ["explicit_met_implicit_miss"],
    }
    if with_checks:
        armed["behavior_key_checks"] = {PACKET_KEY: PROBE_COMPARE}
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


def _wire_mocks(patches):
    from eat_queue_core.weave.factory.factory_dispatch_preflight import (
        DispatchPreflightResult,
    )

    mock_pf, mock_rec, mock_merge, mock_interp = (
        patches[0],
        patches[1],
        patches[2],
        patches[3],
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

    def test_align_blocks_missing_behavior_key_checks(self) -> None:
        rel = _write_blank(self.root, with_checks=False)
        armed = yaml.safe_load((self.root / rel).read_text(encoding="utf-8"))
        r = run_prefer_align(
            self.root, armed=armed, project_id=FIXTURE_PROJECT_ID, observed_entries=[]
        )
        self.assertFalse(r.ok)
        self.assertTrue(
            any("behavior_key_checks_missing" in v for v in r.violations)
        )

    def test_align_blocks_contract_play_path_success(self) -> None:
        rel = _write_blank(
            self.root,
            armed_extra={
                "structural_success": (
                    "A GM can point at a polygon solid and that solid stays "
                    "the same one that was pointed at."
                ),
                "intent_invariant": "point and stay on screen",
            },
        )
        armed = yaml.safe_load((self.root / rel).read_text(encoding="utf-8"))
        r = run_prefer_align(
            self.root, armed=armed, project_id=FIXTURE_PROJECT_ID, observed_entries=[]
        )
        self.assertFalse(r.ok)
        self.assertTrue(
            any(
                "contract_success_has_play_path_words" in v for v in r.violations
            ),
            r.violations,
        )
        self.assertTrue(
            any(
                "contract_play_path_words_with_yaml_lookup" in v
                for v in r.violations
            ),
            r.violations,
        )

    def test_align_blocks_moment_act_words_with_index_shell(self) -> None:
        """Moment + play-path success + all index/shell probes → align fail."""
        keys = [
            "points_at_that_polygon",
            "sees_same_polygon_after_point",
            "watches_pointed_solid_stay",
        ]
        probes = {
            "shell_a": {
                "op": "entrypoint_result_equals",
                "argv": ["python3", "tools/select_probe.py"],
                "selector": {"index": 0},
                "equals_from": {"path": "state/solids.yaml", "key": "solids.0.id"},
            },
            "shell_b": {
                "op": "entrypoint_result_equals",
                "argv": ["python3", "tools/select_probe.py"],
                "selector": {"index": 0},
                "equals_from": {"path": "state/solids.yaml", "key": "solids.0.id"},
            },
            "shell_c": {
                "op": "field_equals",
                "path": "state/solids.yaml",
                "key": "solids",
                "equals": [],
            },
        }
        rel = _write_blank(
            self.root,
            probes=probes,
            armed_extra={
                "proof_shape": "moment",
                "claim_class": "ask_success",
                "prefer_class": "foundation",
                "structural_success": (
                    "A GM can point at a polygon solid on the board and see "
                    "that solid stay the same one that was pointed at."
                ),
                "success_object": "point_and_stay_polygon_solid",
                "behavior_keys": keys,
                "behavior_key_checks": {
                    keys[0]: "shell_a",
                    keys[1]: "shell_b",
                    keys[2]: "shell_c",
                },
            },
        )
        armed = yaml.safe_load((self.root / rel).read_text(encoding="utf-8"))
        r = run_prefer_align(
            self.root, armed=armed, project_id=FIXTURE_PROJECT_ID, observed_entries=[]
        )
        self.assertFalse(r.ok)
        self.assertTrue(
            any(
                "moment_act_words_with_index_shell_lookup" in v for v in r.violations
            ),
            r.violations,
        )
        self.assertFalse(
            any(
                "contract_play_path_words_with_yaml_lookup" in v
                for v in r.violations
            ),
            r.violations,
        )

    def test_align_allows_moment_point_act_probes(self) -> None:
        """r4-shaped moment: equals_from + selector.point must not get shell refuse."""
        keys = [
            "points_at_that_polygon",
            "sees_same_polygon_after_point",
            "watches_pointed_solid_stay",
        ]
        probes = {
            "point_a": {
                "op": "entrypoint_result_equals",
                "argv": ["python3", "tools/point_select_entrypoint.py"],
                "selector": {"point": [0.5, 0.5]},
                "equals_from": {"path": "state/solids.yaml", "key": "solids.0.id"},
            },
            "point_b": {
                "op": "entrypoint_result_equals",
                "argv": ["python3", "tools/point_select_entrypoint.py"],
                "selector": {"point": [0.2, 0.2]},
                "equals_from": {"path": "state/solids.yaml", "key": "solids.0.id"},
            },
            "point_c": {
                "op": "entrypoint_result_equals",
                "argv": ["python3", "tools/point_select_entrypoint.py"],
                "selector": {"point": {"x": 0.55, "y": 0.55}},
                "equals_from": {
                    "path": "state/solids.yaml",
                    "key": "solids.0.commit_id",
                },
            },
        }
        rel = _write_blank(
            self.root,
            probes=probes,
            armed_extra={
                "proof_shape": "moment",
                "claim_class": "ask_success",
                "prefer_class": "foundation",
                "structural_success": (
                    "A GM can point at a polygon solid on the board and see "
                    "that solid stay the same one that was pointed at."
                ),
                "success_object": "point_and_stay_polygon_solid",
                "behavior_keys": keys,
                "behavior_key_checks": {
                    keys[0]: "point_a",
                    keys[1]: "point_b",
                    keys[2]: "point_c",
                },
            },
        )
        armed = yaml.safe_load((self.root / rel).read_text(encoding="utf-8"))
        r = run_prefer_align(
            self.root, armed=armed, project_id=FIXTURE_PROJECT_ID, observed_entries=[]
        )
        self.assertFalse(
            any(
                "moment_act_words_with_index_shell_lookup" in v for v in r.violations
            ),
            r.violations,
        )

    def test_probe_literal_equals_forbidden(self) -> None:
        _write_blank(self.root)
        out = run_named_probes(self.root, FIXTURE_PROJECT_ID, [PROBE_LITERAL])
        self.assertEqual(len(out), 1)
        self.assertFalse(out[0].ok)
        self.assertIn("literal_equals_forbidden", out[0].detail)

    def test_probe_constant_print_fails_when_state_differs(self) -> None:
        _write_blank(
            self.root,
            entrypoint_body=_CONSTANT_ENTRYPOINT,
            solid_id="other-solid-id-not-constant",
        )
        # Constant script still prints SOLID_ID; state has other id → fail
        out = run_named_probes(self.root, FIXTURE_PROJECT_ID, [PROBE_COMPARE])
        self.assertFalse(out[0].ok)

    def test_probe_echo_selector_arg_fails(self) -> None:
        _write_blank(self.root, entrypoint_body=_ECHO_ARG_ENTRYPOINT)
        out = run_named_probes(self.root, FIXTURE_PROJECT_ID, [PROBE_COMPARE])
        self.assertFalse(out[0].ok)
        self.assertIn("echoed_selector_arg", out[0].detail)

    def test_live_eat_blocks_before_agent_on_missing_checks(self) -> None:
        rel = _write_blank(self.root, with_checks=False)
        called = {"agent": False}

        def _fake_agent(*_a: Any, **_k: Any) -> dict[str, Any]:
            called["agent"] = True
            return {"ok": True}

        entry = {"id": "eat-1", "project_id": FIXTURE_PROJECT_ID, "params": {}}
        params = {
            "slice_id": "fixture_contract_slice",
            "lane_id": "implementation",
            "project_id": FIXTURE_PROJECT_ID,
            "armed_packet_path": rel,
            "repo_path": f"1-Projects/{FIXTURE_PROJECT_ID}/game",
        }
        patches = _lane_patches()
        with patches[0] as a, patches[1] as b, patches[2] as c, patches[3] as d, patches[
            4
        ], patches[5], patches[6], patches[7], patches[8], patches[9], patches[10]:
            _wire_mocks((a, b, c, d))
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

        def _agent(*_a: Any, **_k: Any) -> dict[str, Any]:
            return {"ok": True, "evidence_pack": {PACKET_KEY: True}}

        entry = {"id": "eat-2", "project_id": FIXTURE_PROJECT_ID, "params": {}}
        params = {
            "slice_id": "fixture_contract_slice",
            "lane_id": "implementation",
            "project_id": FIXTURE_PROJECT_ID,
            "armed_packet_path": rel,
            "repo_path": f"1-Projects/{FIXTURE_PROJECT_ID}/game",
        }
        patches = _lane_patches()
        with patches[0] as a, patches[1] as b, patches[2] as c, patches[3] as d, patches[
            4
        ], patches[5], patches[6], patches[7], patches[8], patches[9], patches[10]:
            _wire_mocks((a, b, c, d))
            out = run_factory_lane_job(
                self.root,
                "factory",
                entry,
                params=params,
                run_agent_fn=_agent,
                skip_preflight=True,
                complete_pipeline=False,
                auto_retry_seats=False,
            )
        self.assertFalse(out.get("ok"))
        self.assertEqual(out.get("error"), "weld_intent_evidence_failed")
        self.assertIn(
            "weld_intent:agent_sourced_evidence_pack",
            out.get("evidence_violations") or [],
        )

    def test_live_eat_exit_code_alone_probe_fails(self) -> None:
        rel = _write_blank(
            self.root,
            armed_extra={"behavior_key_checks": {PACKET_KEY: PROBE_EXIT_ONLY}},
        )

        def _agent(*_a: Any, **_k: Any) -> dict[str, Any]:
            return {"ok": True}

        entry = {"id": "eat-exit", "project_id": FIXTURE_PROJECT_ID, "params": {}}
        params = {
            "slice_id": "fixture_contract_slice",
            "lane_id": "implementation",
            "project_id": FIXTURE_PROJECT_ID,
            "armed_packet_path": rel,
            "repo_path": f"1-Projects/{FIXTURE_PROJECT_ID}/game",
        }
        patches = _lane_patches()
        with patches[0] as a, patches[1] as b, patches[2] as c, patches[3] as d, patches[
            4
        ], patches[5], patches[6], patches[7], patches[8], patches[9], patches[10]:
            _wire_mocks((a, b, c, d))
            out = run_factory_lane_job(
                self.root,
                "factory",
                entry,
                params=params,
                run_agent_fn=_agent,
                skip_preflight=True,
                complete_pipeline=False,
                auto_retry_seats=False,
            )
        self.assertFalse(out.get("ok"))
        self.assertEqual(out.get("error"), "weld_intent_evidence_failed")
        viol = " ".join(out.get("evidence_violations") or [])
        self.assertIn("probe_op_not_compare", viol)

    def test_live_eat_runner_compare_passes(self) -> None:
        rel = _write_blank(self.root)

        def _agent(*_a: Any, **_k: Any) -> dict[str, Any]:
            return {"ok": True}

        entry = {"id": "eat-ok", "project_id": FIXTURE_PROJECT_ID, "params": {}}
        params = {
            "slice_id": "fixture_contract_slice",
            "lane_id": "implementation",
            "project_id": FIXTURE_PROJECT_ID,
            "armed_packet_path": rel,
            "repo_path": f"1-Projects/{FIXTURE_PROJECT_ID}/game",
        }
        patches = _lane_patches()
        with patches[0] as a, patches[1] as b, patches[2] as c, patches[3] as d, patches[
            4
        ], patches[5], patches[6], patches[7], patches[8], patches[9], patches[10]:
            _wire_mocks((a, b, c, d))
            out = run_factory_lane_job(
                self.root,
                "factory",
                entry,
                params=params,
                run_agent_fn=_agent,
                skip_preflight=True,
                complete_pipeline=False,
                auto_retry_seats=False,
            )
        self.assertNotEqual(out.get("error"), "prefer_align_failed")
        self.assertNotEqual(out.get("error"), "weld_intent_evidence_failed")
        self.assertTrue(
            out.get("prefer_product_seats_met") is True or out.get("ok") is True,
            msg=str(out),
        )


if __name__ == "__main__":
    unittest.main()
