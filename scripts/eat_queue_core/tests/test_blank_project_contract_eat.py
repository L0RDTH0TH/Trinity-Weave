"""Blank-project contract eat — refuse-demo bar, not a functional feedstock line.

Walks bind + handoff + preflight. Empty build_command must not invent Godot/dotnet.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from eat_queue_core.weave.engine_preflight import run_engine_preflight
from eat_queue_core.weave.factory.host_law import matching_cites, matching_refuse_codes
from eat_queue_core.weave.factory.implicit_intent_bind import compose_implicit_intent_bind
from eat_queue_core.weave.implementation_handoff import build_implementation_handoff

FIXTURE_PROJECT_ID = "fixture-project"


def _write_blank_vault(root: Path) -> None:
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
        "legacy-refuse": {
            "refuse_strings": [
                "explicit_met_implicit_miss",
                "dual_shape_refuse",
            ]
        },
    }
    for fam, body in families.items():
        (bindings / f"{fam}.yaml").write_text(
            yaml.dump(body, sort_keys=False), encoding="utf-8"
        )


class BlankProjectContractEatTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="contract-eat-"))
        _write_blank_vault(self.root)

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.root, ignore_errors=True)

    def test_contract_bind_empty_cites_no_topology_no_inspiration(self) -> None:
        armed = {
            "proof_shape": "contract",
            "host_law_ids": [],
            "do_not_waive": [
                "explicit_met_implicit_miss",
                "dual_shape_refuse",
            ],
        }
        payload = compose_implicit_intent_bind(
            slice_id="fixture_contract_slice",
            project_id=FIXTURE_PROJECT_ID,
            explicit_ask="assert invariant only",
            refuse=list(armed["do_not_waive"]),
            inspiration_cites=[],
            armed=armed,
        )
        self.assertEqual(payload.get("inspiration_cites"), [])
        self.assertFalse(payload.get("topology_rewrite"))
        self.assertNotIn("inspiration_shape_miss", payload.get("refuse") or [])
        cites = matching_cites(
            self.root, FIXTURE_PROJECT_ID, host_law_ids=[]
        )
        self.assertEqual(cites, [])
        refuses = matching_refuse_codes(
            self.root,
            FIXTURE_PROJECT_ID,
            context={"host_law_ids": []},
        )
        self.assertEqual(refuses, [])

    def test_handoff_and_preflight_empty_build_no_invent(self) -> None:
        entry = {
            "params": {
                "repo_path": f"1-Projects/{FIXTURE_PROJECT_ID}/game",
                "milestone_id": "IMPLEMENT_SLICE",
                "armed_packet_path": "",
                "proof_shape": "contract",
            }
        }
        charter = {"milestone_id": "IMPLEMENT_SLICE", "done_when": "invariant holds", "target_files": []}
        handoff = build_implementation_handoff(
            self.root,
            lane="factory",
            entry=entry,
            charter=charter,
            goal_packet=None,
        )
        low = handoff.lower()
        self.assertNotIn("dotnet", low)
        self.assertNotIn("dotnet build", low)
        self.assertNotIn("flow_launch", low)
        # Must not invent a Godot binary path or search instruction.
        self.assertNotIn("godot binary", low)
        self.assertNotIn("resolve_godot", low)

        preflight = run_engine_preflight(
            self.root,
            f"1-Projects/{FIXTURE_PROJECT_ID}/game",
            project_id=FIXTURE_PROJECT_ID,
            build_command="",
        )
        self.assertTrue(preflight.get("ok"))
        self.assertEqual(preflight.get("build_command"), "")
        checks = preflight.get("checks") or []
        statuses = {c.get("check"): c.get("status") for c in checks if isinstance(c, dict)}
        self.assertEqual(statuses.get("build_command"), "skip")
        joined = " ".join(str(c) for c in checks).lower()
        self.assertNotIn("flow_launch", joined)
        self.assertNotIn("godot", joined)
        self.assertNotIn("dotnet", joined)


if __name__ == "__main__":
    unittest.main()
