"""Pass 5 Tip A — Half B single-seat check. Not Genesis. No GREENLIGHT."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from eat_queue_core.weave.factory.lane_agent_registry import LANE_AGENTS, get_lane_agent
from eat_queue_core.weave.factory.lane_factories import (
    SINGLE_SEAT_ID,
    dispatch_slice_lanes,
)
from eat_queue_core.weave.factory.review_seats import run_integration_pass
from eat_queue_core.weave.implementation_handoff import build_implementation_handoff

FIXTURE_PROJECT_ID = "fixture-project"
# Keys live only on the armed Prefer — fixture must not pass them in twice.
PACKET_KEY = "polygon_solid_identity_holds_after_select"


def _write_blank_vault(root: Path) -> Path:
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
        # Six ids on project — Prefer silent must still be one seat.
        "lanes": {
            "lane_ids": [
                "asset",
                "techart",
                "content",
                "presentation",
                "audio",
                "module",
            ],
            "order": [],
        },
        "host-law": {"entries": []},
        "legacy-refuse": {"refuse_strings": []},
    }
    for fam, body in families.items():
        (bindings / f"{fam}.yaml").write_text(
            yaml.dump(body, sort_keys=False), encoding="utf-8"
        )

    armed_rel = f"1-Projects/{pid}/Factory-DRB/slice-briefs/fixture_contract.armed.yaml"
    armed_path = root / armed_rel
    armed_path.parent.mkdir(parents=True, exist_ok=True)
    armed_path.write_text(
        yaml.dump(
            {
                "proof_shape": "contract",
                "host_law_ids": [],
                "behavior_keys": [PACKET_KEY],
                "structural_success": "identity key holds after select",
                "do_not_waive": ["explicit_met_implicit_miss"],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return armed_path


class HalfBSingleSeatTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="half-b-seat-"))
        self.armed_path = _write_blank_vault(self.root)

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.root, ignore_errors=True)

    def test_empty_prefer_lanes_one_seat_not_catalog(self) -> None:
        self.assertEqual(LANE_AGENTS, {})
        self.assertIsNone(get_lane_agent(SINGLE_SEAT_ID))
        self.assertIsNone(get_lane_agent("module"))
        jobs = dispatch_slice_lanes(
            self.root,
            slice_id="fixture_contract_slice",
            lane_ids=(),  # Prefer silent — do not pass lanes.yaml
            game_repo_rel=f"1-Projects/{FIXTURE_PROJECT_ID}/game",
        )
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].lane_id, SINGLE_SEAT_ID)
        self.assertNotEqual(jobs[0].lane_id, "module")
        self.assertNotEqual(jobs[0].lane_id, "presentation")

    def test_handoff_reads_keys_from_packet_no_method(self) -> None:
        armed_rel = str(self.armed_path.relative_to(self.root))
        entry = {
            "params": {
                "armed_packet_path": armed_rel,
                "proof_shape": "contract",
            }
        }
        # Do not pass PACKET_KEY into the builder — only the packet holds it.
        handoff = build_implementation_handoff(
            self.root,
            lane=SINGLE_SEAT_ID,
            entry=entry,
            charter={},
            goal_packet=None,
        )
        self.assertIn(PACKET_KEY, handoff)
        low = handoff.lower()
        self.assertNotIn("dotnet", low)
        self.assertNotIn("systems/", low)
        self.assertNotIn("project.godot", low)
        self.assertNotIn("restate the ux goal", low)
        self.assertNotIn("keys_ok", low)

    def test_integration_pass_empty_build_no_game_project_invent(self) -> None:
        result = run_integration_pass(
            self.root,
            game_repo_rel=f"1-Projects/{FIXTURE_PROJECT_ID}/game",
            project_id=FIXTURE_PROJECT_ID,
            build_command="",
        )
        self.assertTrue(result.ok)
        detail = (result.detail or "").lower()
        self.assertIn("empty_build_command", detail)
        self.assertNotIn("project.godot", detail)
        self.assertNotIn("csproj", detail)
        self.assertNotIn("dotnet", detail)


if __name__ == "__main__":
    unittest.main()
