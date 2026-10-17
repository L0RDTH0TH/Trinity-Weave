---
title: Staging receipt — alpha0_gen_terrain_product_r2
slice_id: alpha0_gen_terrain_product_r2
ask_id: alpha0_gen_terrain_product
series_id: alpha0_world_builder_r1
series_step: gen_terrain_product
ticket_map_id: GEN-terrain-product
producer_run_id: sp-gen-terrain-product-r2-altitude-bands
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
prefer_deepened: true
altitude_bands_deepened: true
prior_product_slice: alpha0_gen_terrain_product_r1
success_object: generated_land_water_height_rivers_from_ui
contract: C_gen_terrain_product_w1_w5
create_world_open: auto_gen_from_bias_dials
enter_craft_empty: kept_1g_manual_lane_only_until_place
gen_fill_as_craft_enter: barred
empty_create_world_open: barred
generate_button_as_product_ux: barred_struck
explicit_generate: create_world_open_auto_gen_key_t_accel_only
regen_path: dials_change_plus_reopen_or_session_rebind
height_reads: craft_view_gen_y_lift_altitude_bands
rivers_watercourse: dial_gt0_ridge_plus_downhill_eq0_none
status: live_weld_landed_staging_awaiting_f5
selection_rationale: operator_flesh_terrain_gen_azgaar_altitude_anchor
not_selected: GEN-tone
do_not_arm: GEN-tone GEN-biomes PACK-save-load
keep: false
ask_success: false
next_world_armed: false
welds:
  W1: landed
  W2: landed_dials_reshape_altitude_climate_wildness_rivers_cell_count
  W3: landed_land_water_from_altitude_vs_sea
  W4: landed_altitude_bands_craft_lift
  W5: landed_ridge_plus_downhill_ribbon
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
trinity_branch: project/genesis-mythos-master
trinity_push: local_tip_only_push_enabled_false
trinity_tip: 5ad5e627da9586dfc0d849260cb91d19fa1bd2b2
trinity_tip_pin: 5ad5e627da9586dfc0d849260cb91d19fa1bd2b2
trinity_prior_tip: 2f94a4a
curator_snapshot: skipped_push_enabled_false
gate_a: ok
completed: 2026-10-16T03:45:00Z
---

# Staging receipt — alpha0_gen_terrain_product_r2

**Prefer deepen + LIVE** — Azgaar-style altitude bands (DeepOcean / Shelf / Lowland / Highland / Peak). Create World Open auto-gen · Enter Craft empty until place · Generate button stays struck. `claim_class: staging`. **Do not KEEP.** **No ask_success** without operator F5. **`next_world_armed: false`.** **GEN-tone unarmed.**

## Welds landed

| Weld | Evidence |
|------|----------|
| W1 | No Generate product button; Create World Open = gen surface; regen = dials + re-Open; `Key.T` accel only |
| W2 | Cell size / cell count / rivers / climate / wildness reshape pass (sea level, land share, relief, rings) |
| W3 | Land vs water from altitude vs sea; Create World auto; Enter Craft empty |
| W4 | Band-scaled craft Y lift (peaks high vs shelf/ocean low); GenHeightVisualScale 68 |
| W5 | Rivers 0 → no ribbon; rivers high → ridge corridors + downhill carve + wider blue ribbon |

## LIVE code changed

| File | Change |
|------|--------|
| `Core/WorldGen/GenTerrainService.cs` | Multi-octave elevation, sea level, altitude bands, river ridge + `CarveDownhillRivers` |
| `Core/WorldGen/GenTerrainContract.cs` | SliceId → `alpha0_gen_terrain_product_r2`; altitude / GEN-tone barred laws |
| `Systems/DualGridCraftHost.cs` | Adjacency downhill polish; taller height scale; wider river ribbon |
| `Core/WorldGen/WorldPackage.cs` | Comment / slice pointer r2 |

## Gate A

`prefer_map_fidelity_check.py` → ok (hostile Prefer pending before KEEP — expected staging).

## Build

`dotnet build` → 0 errors.

## F5 expected behavior (Play-path)

Create World → set Cell count 2 → Open → count cells/footprint X (small). New world → Cell count 8 → Open → obviously larger/more cells. Rivers 0 → no blue corridors; rivers high → visible blue watercourses from highlands toward shelf. Climate low vs high → land share / water shelf clearly different. Wildness low vs high → smoother vs broken relief. Height/climate change readable as land share and craft Y relief. Blank amber Open = FAIL. Enter Craft empty until place. No Generate button. GEN-tone unarmed.

## Out

KEEP · ask_success · GEN-tone / GEN-biomes / PACK arm · Generate button re-add · salt-ticket F5 theater · friends/roster/legality
