"""Unit tests — ticket-map Prefer fidelity (Gate A) + hostile (Gate B)."""

from __future__ import annotations

import textwrap
from pathlib import Path

from eat_queue_core.weave.factory.prefer_map_fidelity import (
    WORLD_GEN_MAP_DO_NOT_WAIVE,
    armed_requires_hostile_prefer,
    armed_requires_ticket_map_fidelity,
    keep_latch_allowed,
    parse_ticket_map_rows,
    validate_armed_map_fidelity,
)


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
    rel = Path(
        "1-Projects/genesis-mythos-master/Factory-DRB/"
        "World-Builder-Mini-Game-Ticket-Map.md"
    )
    full = tmp_path / rel
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(SAMPLE_MAP, encoding="utf-8")
    return tmp_path


def _good_armed() -> dict:
    return {
        "slice_id": "alpha0_gen_terrain_product_r1",
        "ticket_map_id": "GEN-terrain-product",
        "prefer_authorship": True,
        "prefer_concept_required": True,
        "claim_class": "staging",
        "success_object": "generated_land_water_height_rivers_from_ui",
        "structural_success": (
            "Player sets bounds dials, presses a Generate control (not a taught hotkey), "
            "and the dual grid shows land, water, readable height, and rivers that "
            "change when rivers/climate/wildness/cell size change. "
            "W1 Generate control. W2 dials change pass. W3 land water. W4 height. W5 rivers."
        ),
        "welds": {"W1": "a", "W2": "b", "W3": "c", "W4": "d", "W5": "e"},
        "do_not_waive": list(WORLD_GEN_MAP_DO_NOT_WAIVE),
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
