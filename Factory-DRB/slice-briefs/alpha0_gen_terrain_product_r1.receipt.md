---
title: Staging receipt — alpha0_gen_terrain_product_r1
slice_id: alpha0_gen_terrain_product_r1
ask_id: alpha0_gen_terrain_product
series_id: alpha0_world_builder_r1
series_step: gen_terrain_product
ticket_map_id: GEN-terrain-product
producer_run_id: sp-gen-terrain-product-r1-cell-count-dial
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
prefer_amended: true
cell_count_dial_amended: true
success_object: generated_land_water_height_rivers_from_ui
contract: C_gen_terrain_product_w1_w5
create_world_open: auto_gen_from_bias_dials
enter_craft_empty: kept_1g_manual_lane_only_until_place
gen_fill_as_craft_enter: barred
empty_create_world_open: barred
generate_button_as_product_ux: barred_struck
explicit_generate: create_world_open_auto_gen_key_t_accel_only
regen_path: dials_change_plus_reopen_or_session_rebind
height_reads: craft_view_gen_y_lift
rivers_watercourse: dial_gt0_ribbon_eq0_none
cell_count_dial: seed_rings_2_to_8_default_5
status: live_weld_landed_staging_awaiting_f5
prior_incomplete: alpha0_gen_terrain_r1
prior_disposition: INCOMPLETE_superseded_callable_accel_only_do_not_KEEP
prior_blank_open: F5_FAIL_incomplete_amended_lane_split
prior_generate_button: struck_operator_order
selection_rationale: operator_cell_count_sister_dial_W2
not_selected: GEN-biomes
do_not_arm: GEN-biomes GEN-tone PACK-save-load
keep: false
ask_success: false
next_world_armed: false
welds:
  W1: landed
  W2: landed_incl_cell_count
  W3: landed
  W4: landed
  W5: landed
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
trinity_branch: project/genesis-mythos-master
trinity_push: local_tip_only_push_enabled_false_remote_behind
trinity_project_sha: 16952c714e4656c25addb0903f566bca4b5c1445
trinity_tip: 16952c714e4656c25addb0903f566bca4b5c1445
trinity_weld_tip: f299edb5ed3f086eb1464b66de0aea6fef6dbd76
trinity_prior_tip: 70d6942
curator_snapshot: skipped_push_enabled_false
gate_a: ok
completed: 2026-10-16T00:50:00Z
---

# Staging receipt — alpha0_gen_terrain_product_r1

**Prefer amend + LIVE** — **Cell count** dial sister to Cell size (W2). Create World Open auto-gen · Enter Craft empty until place · Generate button stays struck. `claim_class: staging`. **Do not KEEP.** **No ask_success** without operator F5. **`next_world_armed: false`.**

## Welds landed

| Weld | Evidence |
|------|----------|
| W1 | No Generate product button; Create World Open = gen surface; regen = dials + re-Open; `Key.T` accel only |
| W2 | Cell size (landform freq) + **Cell count** (seed rings 2–8 → remesh before paint) + rivers / climate / wildness; seed hash includes count |
| W3 | Create World → `AutoGenCreateWorldOpen` → `ApplyGenTerrainPass`; Enter Craft skips auto-gen |
| W4 | DualCell Y lift from gen height facts |
| W5 | Rivers dial > 0 → ribbon; dial 0 → none |

## LIVE code changed

| File | Change |
|------|--------|
| `Core/WorldGen/WorldBoundsDials.cs` | `CellCount` 2–8 (default 5) + `ToSeedRingCount()` |
| `UI/WorldgenGui.cs` | Cell count slider next to Cell size |
| `Systems/DualGridCraftHost.cs` | `ApplyGenTerrainPass` remeshes rings from dial before paint |
| `Core/WorldGen/GenTerrainService.cs` | Seed mix includes cell count; log seed_rings |
| `Core/WorldGen/WorldPackageSession.cs` | Meta dial cell count / seed rings |
| `Core/WorldGen/WorldScaffoldProposal.cs` | Region + hash include rings |

## Out

KEEP · ask_success · GEN-tone / GEN-biomes / PACK arm · Generate button re-add · meta-only cell count
