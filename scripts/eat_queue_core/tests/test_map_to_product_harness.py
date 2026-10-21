"""Regression — map Prefer → factory eat without demo rewrite (Grok six + holes)."""

from __future__ import annotations

import textwrap
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from eat_queue_core.weave.factory.factory_dispatch_preflight import (
    check_map_prefer_eat_guards,
    run_factory_dispatch_preflight,
)
from eat_queue_core.weave.factory.implicit_intent_bind import (
    compose_implicit_intent_bind,
)
from eat_queue_core.weave.factory.prefer_map_fidelity import (
    PRODUCT_MAP_DO_NOT_WAIVE,
    classify_behavior_key_role,
    launch_scene_from_armed_fields,
    lane_id_from_armed_fields,
    validate_armed_map_fidelity,
)
from eat_queue_core.weave.factory.product_kinesthetic_honesty import (
    run_product_kinesthetic_honesty,
)
from eat_queue_core.weave.implementation_handoff import build_factory_lane_handoff


CONTRACT_DNW = list(PRODUCT_MAP_DO_NOT_WAIVE)

POLYGON_MAP = textwrap.dedent(
    """
    ## World board

    | Ticket | Status | Product job | Notes / welds |
    |--------|--------|-------------|----------------|
    | `WB-polygon-substrate` | open | Point at a low-fidelity polygon solid; identity holds after select. | Capability: polygon substrate. |
    | `WB-sim-clock` | open | World clock advances while unobserved. | Neighbor — out of scope. |
    """
)


def _vault_with_map(root: Path, *, row_extra: str = "") -> Path:
    drb = root / "1-Projects/genesis-mythos-master/Factory-DRB"
    drb.mkdir(parents=True)
    map_rel = (
        "1-Projects/genesis-mythos-master/Factory-DRB/"
        "World-Builder-Session-Prep-Ticket-Map.md"
    )
    body = POLYGON_MAP
    if row_extra:
        body = body.replace(
            "Capability: polygon substrate.",
            f"Capability: polygon substrate. {row_extra}",
        )
    (root / map_rel).write_text(
        "---\nticket_map: true\nmap_id: fixture-polygon\n"
        "map_status: active\nproject-id: genesis-mythos-master\n---\n" + body,
        encoding="utf-8",
    )
    (drb / "factory-project.yaml").write_text(
        "project_id: genesis-mythos-master\n"
        "game_repo_path: 5-Attachments/Code-Repos/fixture-game\n"
        "ticket_map_runtime:\n"
        "  map_id: fixture-polygon\n"
        f"  map_note: {map_rel}\n",
        encoding="utf-8",
    )
    return root


def _contract_armed(**overrides) -> dict:
    base = {
        "slice_id": "alpha0_wb_polygon_substrate_r2",
        "ticket_map_id": "WB-polygon-substrate",
        "prefer_authorship": True,
        "proof_shape": "contract",
        "claim_class": "component",
        "prefer_class": "foundation",
        "success_object": "polygon_solid_identity_holds",
        "structural_success": (
            "Point at a low-fidelity polygon solid; identity holds after select."
        ),
        "out_of_scope_ticket_ids": ["WB-sim-clock"],
        "do_not_waive": CONTRACT_DNW,
        "checklist_ids": [],
        "behavior_keys": ["selected_solid_identity_holds"],
    }
    base.update(overrides)
    return base


class TopologyRegressionFixtureTests(unittest.TestCase):
    """Mandatory §2 fixture: full DNW + dual refuse + no lattice → topology_rewrite false."""

    def test_contract_full_dnw_no_lattice_disarms_topology(self) -> None:
        armed = _contract_armed(
            do_not_waive=CONTRACT_DNW,
            refuse=[
                "dual_grid_as_substrate_done",
                "explicit_met_implicit_miss",
            ],
        )
        # Success must not contain a lattice sentence.
        self.assertNotRegex(
            armed["structural_success"].lower(),
            r"\b(lattice|hex|dual.?grid)\b",
        )
        payload = compose_implicit_intent_bind(
            slice_id=armed["slice_id"],
            project_id="genesis-mythos-master",
            explicit_ask=armed["structural_success"],
            structural_success=armed["structural_success"],
            refuse=list(armed.get("refuse") or []),
            armed=armed,
        )
        self.assertFalse(payload["topology_rewrite"], payload)
        self.assertEqual(payload["inspiration_cites"], [])
        for code in ("craft_cam_recenter_on_place", "craft_terrain_blend"):
            self.assertNotIn(code, payload["refuse"])


class CraftCamExactClassTests(unittest.TestCase):
    def test_craft_cam_only_exact_place_or_craft_with_topology_law(self) -> None:
        armed = {
            "topology_law": True,
            "prefer_class": "foundation",
            "proof_shape": "contract",
        }
        payload = compose_implicit_intent_bind(
            slice_id="x",
            project_id="p",
            explicit_ask="a",
            structural_success="identity holds",
            armed=armed,
        )
        self.assertTrue(payload["topology_rewrite"])
        for code in ("craft_cam_recenter_on_place", "craft_terrain_blend"):
            self.assertNotIn(code, payload["refuse"])

        armed["prefer_class"] = "place_craft_hybrid"  # substring must not count
        payload2 = compose_implicit_intent_bind(
            slice_id="x",
            project_id="p",
            explicit_ask="a",
            structural_success="Hex lattice vertices edges faces",
            armed=armed,
        )
        for code in ("craft_cam_recenter_on_place", "craft_terrain_blend"):
            self.assertNotIn(code, payload2["refuse"])

        armed["prefer_class"] = "place"
        payload3 = compose_implicit_intent_bind(
            slice_id="x",
            project_id="p",
            explicit_ask="a",
            structural_success="Hex lattice vertices edges faces",
            armed=armed,
        )
        for code in ("craft_cam_recenter_on_place", "craft_terrain_blend"):
            self.assertIn(code, payload3["refuse"])


class ContractBehaviorKeyRoleTests(unittest.TestCase):
    def test_roles_are_pattern_based_not_two_string_denylist(self) -> None:
        self.assertEqual(classify_behavior_key_role("sees_polygon_solids"), "visibility")
        self.assertEqual(classify_behavior_key_role("points_at_solid"), "visibility")
        self.assertEqual(
            classify_behavior_key_role("selected_solid_identity_holds"), "invariant"
        )
        self.assertEqual(
            classify_behavior_key_role("board_shows_low_fidelity"), "visibility"
        )
        self.assertEqual(
            classify_behavior_key_role("occupancy_round_trip_equals"), "invariant"
        )

    def test_mixed_visibility_plus_invariant_fails_contract(self) -> None:
        with TemporaryDirectory() as tmp:
            root = _vault_with_map(Path(tmp))
            armed = _contract_armed(
                behavior_keys=[
                    "selected_solid_identity_holds",
                    "sees_polygon_solids",
                    "points_at_solid",
                ]
            )
            result = validate_armed_map_fidelity(
                root, armed, prefer_result={"map_fidelity_hostile_ok": True}
            )
            self.assertFalse(result.ok, result.violations)
            self.assertTrue(
                any("contract_visibility_key_forbidden" in v for v in result.violations),
                result.violations,
            )

    def test_single_invariant_key_passes_contract(self) -> None:
        with TemporaryDirectory() as tmp:
            root = _vault_with_map(Path(tmp))
            armed = _contract_armed()
            result = validate_armed_map_fidelity(
                root, armed, prefer_result={"map_fidelity_hostile_ok": True}
            )
            self.assertTrue(result.ok, result.violations)

    def test_missing_proof_shape_fails_gate_a(self) -> None:
        with TemporaryDirectory() as tmp:
            root = _vault_with_map(Path(tmp))
            armed = _contract_armed()
            del armed["proof_shape"]
            result = validate_armed_map_fidelity(
                root, armed, prefer_result={"map_fidelity_hostile_ok": True}
            )
            self.assertFalse(result.ok)
            self.assertTrue(
                any("missing_proof_shape" in v for v in result.violations),
                result.violations,
            )

    def test_invented_welds_fail_without_row_welds(self) -> None:
        with TemporaryDirectory() as tmp:
            root = _vault_with_map(Path(tmp))
            armed = _contract_armed(
                structural_success=(
                    "Point at polygon. W1 invent. W2 invent. W3 invent."
                ),
                welds={"W1": "a", "W2": "b", "W3": "c"},
            )
            result = validate_armed_map_fidelity(
                root, armed, prefer_result={"map_fidelity_hostile_ok": True}
            )
            self.assertFalse(result.ok)
            self.assertTrue(
                any("weld_invented" in v for v in result.violations),
                result.violations,
            )


class LaunchSceneFieldsOnlyTests(unittest.TestCase):
    def test_body_not_launchshell_does_not_set_scene(self) -> None:
        armed = {
            "structural_success": "Do not use LaunchShell; blank shell only.",
            "intent_invariant": "not LaunchShell",
        }
        self.assertEqual(launch_scene_from_armed_fields(armed), "")
        armed["launch_scene"] = "res://Play.tscn"
        self.assertEqual(launch_scene_from_armed_fields(armed), "res://Play.tscn")
        self.assertEqual(
            lane_id_from_armed_fields({"lane_id": "foundation_lane"}),
            "foundation_lane",
        )


class EatPreflightCallerTests(unittest.TestCase):
    def test_dispatch_preflight_invokes_map_guards(self) -> None:
        with TemporaryDirectory() as tmp:
            root = _vault_with_map(Path(tmp))
            armed_rel = (
                "1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/"
                "alpha0_wb_polygon_substrate_r2.armed.yaml"
            )
            import yaml

            (root / armed_rel).parent.mkdir(parents=True)
            # Mixed keys → Gate A fail must surface via eat preflight caller.
            armed = _contract_armed(
                behavior_keys=[
                    "selected_solid_identity_holds",
                    "sees_polygon_solids",
                ]
            )
            (root / armed_rel).write_text(yaml.safe_dump(armed), encoding="utf-8")
            job = {
                "slice_id": "alpha0_wb_polygon_substrate_r2",
                "project_id": "genesis-mythos-master",
                "ticket_map_id": "WB-polygon-substrate",
                "armed_packet_path": armed_rel,
                "checklist_ids": [],
            }
            guards = check_map_prefer_eat_guards(
                root, job=job, project_id="genesis-mythos-master", checklist_ids=[]
            )
            self.assertTrue(
                any("contract_visibility_key_forbidden" in v for v in guards),
                guards,
            )
            result = run_factory_dispatch_preflight(
                root,
                job=job,
                project_id="genesis-mythos-master",
                checklist_ids=[],
                skip_armed_path_check=True,
            )
            self.assertFalse(result.ok, result.detail)
            self.assertTrue(
                any("contract_visibility_key_forbidden" in v for v in result.violations),
                result.violations,
            )

    def test_missing_proof_shape_fails_eat_preflight(self) -> None:
        with TemporaryDirectory() as tmp:
            root = _vault_with_map(Path(tmp))
            armed_rel = (
                "1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/"
                "alpha0_wb_polygon_substrate_r2.armed.yaml"
            )
            import yaml

            (root / armed_rel).parent.mkdir(parents=True)
            armed = _contract_armed()
            del armed["proof_shape"]
            (root / armed_rel).write_text(yaml.safe_dump(armed), encoding="utf-8")
            job = {
                "slice_id": "alpha0_wb_polygon_substrate_r2",
                "project_id": "genesis-mythos-master",
                "ticket_map_id": "WB-polygon-substrate",
                "armed_packet_path": armed_rel,
                "checklist_ids": [],
            }
            guards = check_map_prefer_eat_guards(
                root, job=job, project_id="genesis-mythos-master", checklist_ids=[]
            )
            self.assertTrue(
                any("missing_proof_shape" in v for v in guards), guards
            )


class HandoffNoUxSermonTests(unittest.TestCase):
    def test_catalog_row_without_row_naming_skips_ux_sermon(self) -> None:
        with TemporaryDirectory() as tmp:
            root = _vault_with_map(Path(tmp))
            armed_rel = (
                "1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/"
                "alpha0_wb_polygon_substrate_r2.armed.yaml"
            )
            import yaml

            (root / armed_rel).parent.mkdir(parents=True)
            armed = _contract_armed(catalog_row_id="ux_world_generation")
            (root / armed_rel).write_text(yaml.safe_dump(armed), encoding="utf-8")
            entry = {
                "params": {
                    "slice_id": "alpha0_wb_polygon_substrate_r2",
                    "project_id": "genesis-mythos-master",
                    "ticket_map_id": "WB-polygon-substrate",
                    "armed_packet_path": armed_rel,
                    "catalog_row_id": "ux_world_generation",
                    "ux_feed": {
                        "l5_scope_path": "1-Projects/x/L5.md",
                        "catalog_row_id": "ux_world_generation",
                    },
                    "proof_shape": "contract",
                    "checklist_ids": [],
                }
            }
            text = build_factory_lane_handoff(
                root, lane="factory", entry=entry, goal_packet=None
            )
            self.assertNotIn("UX pillar feed", text)
            self.assertNotIn("Restate the UX goal", text)
            self.assertNotIn("L5 north star", text)

    def test_row_named_catalog_allows_ux_on_moment_only(self) -> None:
        with TemporaryDirectory() as tmp:
            root = _vault_with_map(
                Path(tmp),
                row_extra="catalog_row_id: ux_world_generation",
            )
            armed_rel = (
                "1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/"
                "alpha0_wb_polygon_substrate_r2.armed.yaml"
            )
            import yaml

            (root / armed_rel).parent.mkdir(parents=True)
            armed = _contract_armed(
                proof_shape="moment",
                claim_class="ask_success",
                catalog_row_id="ux_world_generation",
                behavior_keys=[
                    "sees_a",
                    "sees_b",
                    "sees_c",
                ],
            )
            (root / armed_rel).write_text(yaml.safe_dump(armed), encoding="utf-8")
            entry = {
                "params": {
                    "slice_id": "alpha0_wb_polygon_substrate_r2",
                    "project_id": "genesis-mythos-master",
                    "ticket_map_id": "WB-polygon-substrate",
                    "armed_packet_path": armed_rel,
                    "catalog_row_id": "ux_world_generation",
                    "ux_feed": {"l5_scope_path": "L5.md"},
                    "proof_shape": "moment",
                    "checklist_ids": [],
                }
            }
            text = build_factory_lane_handoff(
                root, lane="factory", entry=entry, goal_packet=None
            )
            self.assertIn("UX pillar feed", text)


class HonestyContractWeaveTrackTests(unittest.TestCase):
    def test_contract_skips_missing_weave_track(self) -> None:
        with TemporaryDirectory() as tmp:
            root = _vault_with_map(Path(tmp))
            from eat_queue_core.weave.factory.product_kinesthetic_honesty import (
                TRINITY_CARD_REL,
            )

            card = root / TRINITY_CARD_REL
            card.parent.mkdir(parents=True)
            card.write_text("id: product_kinesthetic_honesty\n", encoding="utf-8")
            result = run_product_kinesthetic_honesty(
                root,
                project_id="genesis-mythos-master",
                proof_shape="contract",
            )
            self.assertFalse(
                any("weave_track" in v for v in result.violations),
                result.violations,
            )


if __name__ == "__main__":
    unittest.main()
