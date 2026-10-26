"""Unit tests — ticket-map Prefer fidelity (Gate A) + hostile (Gate B)."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any

import yaml

from eat_queue_core.weave.factory.prefer_map_fidelity import (
    WORLD_GEN_MAP_DO_NOT_WAIVE,
    armed_requires_hostile_prefer,
    armed_requires_ticket_map_fidelity,
    keep_latch_allowed,
    parse_ticket_map_rows,
    validate_armed_map_fidelity,
)

# Catalog shapes for moment Gate A (index/shell vs point-act).
_INDEX_SHELL_PROBE = {
    "op": "entrypoint_result_equals",
    "argv": ["python3", "tools/select_probe.py"],
    "selector": {"index": 0},
    "equals_from": {"path": "state/solids.yaml", "key": "solids.0.id"},
}
_POINT_ACT_PROBE = {
    "op": "entrypoint_result_equals",
    "argv": ["python3", "tools/point_select_entrypoint.py", "--mode", "point"],
    "selector": {"point": [0.5, 0.5]},
    "equals_from": {"path": "state/solids.yaml", "key": "solids.0.id"},
}
_FIELD_EQUALS_SHELL = {
    "op": "field_equals",
    "path": "state/solids.yaml",
    "key": "solids",
    "equals": [],
}


SAMPLE_MAP = textwrap.dedent(
    """
    | Ticket | Product job | Welds (all required for KEEP) |
    |--------|-------------|-------------------------------|
    | `GEN-terrain-product` | First generate that is a product: knobs change the world, Generate is a control, land/water/height/rivers are readable on the dual grid. | **W1** Generate control. **W2** Cell size, rivers, climate, wildness change the pass. **W3** Land vs water dual-grid. **W4** Height reads. **W5** River dial watercourse. |
    | `PLACE-coast` | Coasts read as coasts (bits → family). | Bits map to coast MeshLibrary family. |
    | `GEN-biomes` | Biomes with mechanical tags. | Tag + visible material. |
    """
)


def _map_vault(tmp_path: Path) -> Path:
    """Fixture vault: ticket map + factory-project socket (no harness hardwire)."""
    drb = tmp_path / "1-Projects/genesis-mythos-master/Factory-DRB"
    drb.mkdir(parents=True, exist_ok=True)
    map_rel = (
        "1-Projects/genesis-mythos-master/Factory-DRB/"
        "World-Builder-Session-Prep-Ticket-Map.md"
    )
    map_body = (
        "---\nticket_map: true\nmap_id: fixture-session-prep\n"
        "map_status: active\nproject-id: genesis-mythos-master\n---\n"
        + SAMPLE_MAP
    )
    (tmp_path / map_rel).write_text(map_body, encoding="utf-8")
    (drb / "factory-project.yaml").write_text(
        "project_id: genesis-mythos-master\n"
        "ticket_map_runtime:\n"
        f"  map_id: fixture-session-prep\n"
        f"  map_note: {map_rel}\n",
        encoding="utf-8",
    )
    return tmp_path


def _install_proof_catalog(
    vault: Path, probes: dict[str, Any], *, project_id: str = "genesis-mythos-master"
) -> None:
    bindings = vault / f"1-Projects/{project_id}/Factory-DRB/bindings"
    bindings.mkdir(parents=True, exist_ok=True)
    (bindings / "proof-catalog.yaml").write_text(
        yaml.dump(
            {"probes": probes, "required_playtest_ids": []},
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def _good_armed() -> dict:
    return {
        "slice_id": "alpha0_gen_terrain_product_r1",
        "ticket_map_id": "GEN-terrain-product",
        "prefer_authorship": True,
        "prefer_concept_required": True,
        "proof_shape": "moment",
        "claim_class": "ask_success",
        "success_object": "generated_land_water_height_rivers_from_ui",
        "structural_success": (
            "Player sets bounds dials, presses a Generate control (not a taught hotkey), "
            "and the dual grid shows land, water, readable height, and rivers that "
            "change when rivers/climate/wildness/cell size change. "
            "W1 Generate control. W2 dials change pass. W3 land water. W4 height. W5 rivers."
        ),
        "welds": {"W1": "a", "W2": "b", "W3": "c", "W4": "d", "W5": "e"},
        "do_not_waive": list(WORLD_GEN_MAP_DO_NOT_WAIVE),
        # Unsectioned fixture → whole map is one section.
        "out_of_scope_ticket_ids": ["GEN-biomes", "PLACE-coast"],
        "behavior_keys": [
            "generate_control_changes_land_water",
            "river_dial_moves_watercourse",
            "height_reads_on_dual_grid",
        ],
    }


def _hostile_ok() -> dict:
    return {"map_fidelity_hostile_ok": True}


def test_parse_ticket_map_rows():
    rows = parse_ticket_map_rows(SAMPLE_MAP)
    assert "GEN-terrain-product" in rows
    assert "PLACE-coast" in rows
    assert "W1" in rows["GEN-terrain-product"].welds
    assert "Generate" in rows["GEN-terrain-product"].product_job


def test_armed_requires_when_ticket_map_id():
    assert armed_requires_ticket_map_fidelity(_good_armed()) is True
    assert armed_requires_ticket_map_fidelity({"slice_id": "x"}) is False


def test_armed_requires_place_prefix_with_prefer():
    armed = {
        "ask_id": "PLACE-coast",
        "prefer_authorship": True,
        "slice_id": "alpha0_stalberg_dual_place_coast_r1",
        "claim_class": "staging",
    }
    assert armed_requires_ticket_map_fidelity(armed) is True
    assert armed_requires_hostile_prefer(armed) is True


def test_hostile_required_for_stalberg_without_ticket_map():
    """Prefer-product slice without ticket_map_id → Gate B only (no Gate A miss)."""
    armed = {
        "slice_id": "alpha0_stalberg_dual_place_coast_r1",
        "prefer_authorship": True,
        "prefer_concept_required": True,
        "claim_class": "staging",
        "success_object": "dual_cell_meshlibrary_placement",
        "structural_success": "x" * 50,
    }
    assert armed_requires_ticket_map_fidelity(armed) is False
    assert armed_requires_hostile_prefer(armed) is True


def test_validate_ok_with_hostile(tmp_path: Path):
    vault = _map_vault(tmp_path)
    result = validate_armed_map_fidelity(
        vault, _good_armed(), prefer_result=_hostile_ok()
    )
    assert result.applicable is True
    assert result.gate_a_applicable is True
    assert result.gate_b_applicable is True
    assert result.ok is True, result.violations


def test_staging_without_hostile_is_violation(tmp_path: Path):
    """Mechanical Gate A alone must never green staging Success."""
    vault = _map_vault(tmp_path)
    result = validate_armed_map_fidelity(vault, _good_armed(), prefer_result=None)
    assert result.ok is False
    assert any(
        "hostile_prefer_required_before_success" in v for v in result.violations
    )
    assert not any("hostile_prefer_pending" in v for v in result.warnings)


def test_stalberg_staging_without_hostile_is_violation(tmp_path: Path):
    vault = _map_vault(tmp_path)
    armed = {
        "slice_id": "alpha0_stalberg_dual_visual_r1",
        "prefer_authorship": True,
        "claim_class": "staging",
        "success_object": "dual_offset_terrain_tile",
    }
    result = validate_armed_map_fidelity(vault, armed, prefer_result=None)
    assert result.applicable is True
    assert result.gate_a_applicable is False
    assert result.gate_b_applicable is True
    assert result.ok is False
    assert any(
        "hostile_prefer_required_before_success" in v for v in result.violations
    )
    # Must not invent missing_ticket_map_id for Gate-B-only Prefer slices.
    assert not any("missing_ticket_map_id" in v for v in result.violations)


def test_validate_missing_do_not_waive(tmp_path: Path):
    vault = _map_vault(tmp_path)
    armed = _good_armed()
    armed["do_not_waive"] = ["hotkey_as_product_ux"]
    result = validate_armed_map_fidelity(
        vault, armed, prefer_result=_hostile_ok()
    )
    assert result.ok is False
    assert any("missing_do_not_waive" in v for v in result.violations)


def test_validate_denied_success_object(tmp_path: Path):
    vault = _map_vault(tmp_path)
    armed = _good_armed()
    armed["success_object"] = "contract_bound"
    result = validate_armed_map_fidelity(
        vault, armed, prefer_result=_hostile_ok()
    )
    assert result.ok is False
    assert any("success_object_denied" in v for v in result.violations)


def test_keep_latch_requires_hostile_and_f5(tmp_path: Path):
    vault = _map_vault(tmp_path)
    armed = _good_armed()
    r = keep_latch_allowed(vault, armed, prefer_result=None, operator_f5_ok=False)
    assert r.ok is False
    r2 = keep_latch_allowed(
        vault,
        armed,
        prefer_result=_hostile_ok(),
        operator_f5_ok=True,
    )
    assert r2.ok is True, r2.violations


def _live_vault() -> Path:
    vault = Path(__file__).resolve().parents[3]
    assert (vault / "3-Resources/Second-Brain-Config.md").is_file()
    return vault


def test_fat_polygon_job_consumes_siblings_fails():
    """Regression: Prefer that describes living/flight/dials fails on this map.

    Uses the live world-builder-session-prep map as fixture (not a hardcoded ticket).
    """
    from eat_queue_core.weave.factory.prefer_map_fidelity import (
        PRODUCT_MAP_DO_NOT_WAIVE,
        validate_armed_map_fidelity,
    )
    from eat_queue_core.weave.factory.ticket_map_schema import (
        load_ticket_map_rows,
        resolve_active_ticket_map_rel,
        section_open_neighbor_ids,
    )

    vault = _live_vault()
    rel = resolve_active_ticket_map_rel(
        vault, project_id="genesis-mythos-master", ticket_map_id="WB-polygon-substrate"
    )
    assert rel and "Session-Prep" in rel
    rows = load_ticket_map_rows(vault, map_rel=rel, ticket_map_id="WB-polygon-substrate")
    oos = section_open_neighbor_ids(rows, "WB-polygon-substrate")
    assert "WB-sim-clock" in oos or "WB-world-container" in oos

    fat = {
        "ticket_map_id": "WB-polygon-substrate",
        "prefer_authorship": True,
        "proof_shape": "moment",
        "claim_class": "ask_success",
        "success_object": "living_world_with_flight_and_dials",
        "structural_success": (
            "A GM can see and point at a living world made of low-fidelity polygon solids "
            "and can read occupancy, hierarchy, and control surfaces during both deep "
            "authoring and live flight. The world clock advances. Dials change density. "
            "WorldCam flies the board."
        ),
        "out_of_scope_ticket_ids": oos,
        "do_not_waive": list(PRODUCT_MAP_DO_NOT_WAIVE),
        "behavior_keys": [
            "living_world_ticks_unobserved",
            "live_flight_reads_control_surfaces",
            "occupancy_hierarchy_visible",
        ],
    }
    result = validate_armed_map_fidelity(
        vault, fat, prefer_result={"map_fidelity_hostile_ok": True}
    )
    assert result.ok is False, result.violations
    assert any("job_consumes_sibling" in v for v in result.violations), result.violations


def test_contract_prefer_with_play_path_success_fails_gate_a():
    """Scope-cut refuse: contract + point/see/GM success must not green Gate A."""
    from eat_queue_core.weave.factory.prefer_map_fidelity import (
        PRODUCT_MAP_DO_NOT_WAIVE,
        validate_armed_map_fidelity,
    )
    from eat_queue_core.weave.factory.ticket_map_schema import (
        load_ticket_map_rows,
        resolve_active_ticket_map_rel,
        section_open_neighbor_ids,
    )

    vault = _live_vault()
    rel = resolve_active_ticket_map_rel(
        vault, project_id="genesis-mythos-master", ticket_map_id="WB-polygon-substrate"
    )
    rows = load_ticket_map_rows(vault, map_rel=rel, ticket_map_id="WB-polygon-substrate")
    oos = section_open_neighbor_ids(rows, "WB-polygon-substrate")
    job = rows["WB-polygon-substrate"].product_job
    armed = {
        "ticket_map_id": "WB-polygon-substrate",
        "prefer_authorship": True,
        "project_id": "genesis-mythos-master",
        "proof_shape": "contract",
        "claim_class": "component",
        "prefer_class": "foundation",
        "success_object": "point_at_polygon_stays_same_solid",
        "structural_success": job,
        "out_of_scope_ticket_ids": oos,
        "do_not_waive": list(PRODUCT_MAP_DO_NOT_WAIVE),
        "checklist_ids": [],
        "behavior_keys": [
            "selected_solid_identity_holds",
        ],
        # Any equals_from probe trips contract yaml-lookup refuse (not moment predicate).
        "behavior_key_checks": {
            "selected_solid_identity_holds": "moment_points_at_that_polygon",
        },
    }
    result = validate_armed_map_fidelity(
        vault, armed, prefer_result={"map_fidelity_hostile_ok": True}
    )
    assert result.ok is False, result.violations
    assert any(
        "contract_success_has_play_path_words" in v for v in result.violations
    ), result.violations
    assert any(
        "contract_play_path_words_with_yaml_lookup" in v for v in result.violations
    ), result.violations


def test_r4_catalog_shape_fails_play_path_allowlist(tmp_path: Path):
    """Fixture: entrypoint_result_equals + selector.point + equals_from + play-path → red."""
    vault = _map_vault(tmp_path)
    _install_proof_catalog(
        vault,
        {
            "r4_a": _POINT_ACT_PROBE,
            "r4_b": {**_POINT_ACT_PROBE, "selector": {"point": [0.2, 0.2]}},
            "r4_c": {
                **_POINT_ACT_PROBE,
                "selector": {"point": {"x": 0.55, "y": 0.55}},
            },
        },
    )
    armed = _good_armed()
    armed["project_id"] = "genesis-mythos-master"
    armed["structural_success"] = (
        "Player can point at land on the board and see height stay readable "
        "when Generate runs. W1 Generate control. W2 dials. W3 land water. "
        "W4 height. W5 rivers."
    )
    armed["success_object"] = "point_and_see_land_on_board"
    armed["behavior_keys"] = [
        "points_at_land_on_board",
        "sees_height_stay_readable",
        "watches_generate_control",
    ]
    armed["behavior_key_checks"] = {
        "points_at_land_on_board": "r4_a",
        "sees_height_stay_readable": "r4_b",
        "watches_generate_control": "r4_c",
    }
    result = validate_armed_map_fidelity(
        vault, armed, prefer_result=_hostile_ok()
    )
    assert result.ok is False, result.violations
    assert any(
        "play_path_success_requires_point_hits_solid" in v for v in result.violations
    ), result.violations


def test_empty_checks_with_play_path_fails_allowlist(tmp_path: Path):
    """Unresolved / zero checks is not all-passed under play-path trigger."""
    vault = _map_vault(tmp_path)
    _install_proof_catalog(vault, {})
    armed = _good_armed()
    armed["project_id"] = "genesis-mythos-master"
    armed["structural_success"] = (
        "Player can point at land on the board. W1 Generate control. W2 dials. "
        "W3 land water. W4 height. W5 rivers."
    )
    armed["behavior_key_checks"] = {}
    result = validate_armed_map_fidelity(
        vault, armed, prefer_result=_hostile_ok()
    )
    assert any(
        "play_path_success_requires_point_hits_solid" in v for v in result.violations
    ), result.violations


def test_map_row_play_path_triggers_even_if_prefer_text_drops_point(tmp_path: Path):
    """Map-row product job with play-path words still fires allowlist."""
    vault = _map_vault(tmp_path)
    # Override map so GEN-terrain-product job names point/see.
    map_rel = (
        "1-Projects/genesis-mythos-master/Factory-DRB/"
        "World-Builder-Session-Prep-Ticket-Map.md"
    )
    (vault / map_rel).write_text(
        "---\nticket_map: true\nmap_id: fixture-session-prep\n"
        "map_status: active\nproject-id: genesis-mythos-master\n---\n"
        "| Ticket | Product job | Welds |\n"
        "|--------|-------------|-------|\n"
        "| `GEN-terrain-product` | A GM can point at land and see it stay. | "
        "**W1** Generate. **W2** dials. **W3** land. **W4** height. **W5** rivers. |\n"
        "| `PLACE-coast` | Coasts read as coasts. | Bits. |\n"
        "| `GEN-biomes` | Biomes with tags. | Tag. |\n",
        encoding="utf-8",
    )
    _install_proof_catalog(vault, {"shell": _INDEX_SHELL_PROBE})
    armed = _good_armed()
    armed["project_id"] = "genesis-mythos-master"
    # Prefer text deliberately drops play-path words.
    armed["structural_success"] = (
        "Index lookup returns durable land id after Generate. "
        "W1 Generate control. W2 dials. W3 land water. W4 height. W5 rivers."
    )
    armed["success_object"] = "index_lookup_land_id"
    armed["behavior_key_checks"] = {
        "generate_control_changes_land_water": "shell",
        "river_dial_moves_watercourse": "shell",
        "height_reads_on_dual_grid": "shell",
    }
    result = validate_armed_map_fidelity(
        vault, armed, prefer_result=_hostile_ok()
    )
    assert any(
        "play_path_success_requires_point_hits_solid" in v for v in result.violations
    ), result.violations


def test_live_r4_fails_play_path_allowlist():
    """Live r4 Prefer (entrypoint + selector.point + equals_from) must go Gate A red."""
    from eat_queue_core.weave.factory.prefer_map_fidelity import (
        PRODUCT_MAP_DO_NOT_WAIVE,
        load_armed_yaml,
        validate_armed_map_fidelity,
    )

    vault = _live_vault()
    armed_path = (
        vault
        / "1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs"
        / "alpha0_wb_polygon_substrate_r4.armed.yaml"
    )
    if not armed_path.is_file():
        return
    armed = load_armed_yaml(armed_path)
    armed.setdefault("do_not_waive", list(PRODUCT_MAP_DO_NOT_WAIVE))
    result = validate_armed_map_fidelity(
        vault, armed, prefer_result={"map_fidelity_hostile_ok": True}
    )
    assert result.ok is False, result.violations
    assert any(
        "play_path_success_requires_point_hits_solid" in v for v in result.violations
    ), result.violations


def test_contract_prefer_library_still_hits_map_row_allowlist():
    """Dropping play-path from Prefer text cannot bypass map-row play-path job."""
    from eat_queue_core.weave.factory.prefer_map_fidelity import (
        PRODUCT_MAP_DO_NOT_WAIVE,
        validate_armed_map_fidelity,
    )
    from eat_queue_core.weave.factory.ticket_map_schema import (
        load_ticket_map_rows,
        resolve_active_ticket_map_rel,
        section_open_neighbor_ids,
    )

    vault = _live_vault()
    rel = resolve_active_ticket_map_rel(
        vault, project_id="genesis-mythos-master", ticket_map_id="WB-polygon-substrate"
    )
    rows = load_ticket_map_rows(vault, map_rel=rel, ticket_map_id="WB-polygon-substrate")
    oos = section_open_neighbor_ids(rows, "WB-polygon-substrate")
    armed = {
        "ticket_map_id": "WB-polygon-substrate",
        "prefer_authorship": True,
        "project_id": "genesis-mythos-master",
        "proof_shape": "contract",
        "claim_class": "component",
        "prefer_class": "foundation",
        "success_object": "index_lookup_returns_solid_id_in_state",
        "structural_success": (
            "Index lookup returns the durable solid id recorded in state for the "
            "chosen row. Function/file fact only."
        ),
        "out_of_scope_ticket_ids": oos,
        "do_not_waive": list(PRODUCT_MAP_DO_NOT_WAIVE),
        "checklist_ids": [],
        "behavior_keys": ["selected_solid_identity_holds"],
        "behavior_key_checks": {
            "selected_solid_identity_holds": "moment_points_at_that_polygon",
        },
    }
    result = validate_armed_map_fidelity(
        vault, armed, prefer_result={"map_fidelity_hostile_ok": True}
    )
    assert any(
        "play_path_success_requires_point_hits_solid" in v for v in result.violations
    ), result.violations
