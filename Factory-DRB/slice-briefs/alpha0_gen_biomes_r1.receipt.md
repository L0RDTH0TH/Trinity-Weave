---
title: Staging receipt — alpha0_gen_biomes_r1
slice_id: alpha0_gen_biomes_r1
ask_id: alpha0_gen_biomes
series_id: alpha0_world_builder_r1
series_step: gen_biomes
ticket_map_id: GEN-biomes
producer_run_id: sp-gen-biomes-r1
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
prior_product_slice: alpha0_pack_save_load_r1
prior_product_disposition: operator_f5_pass_demo_quality_ok
success_object: biomes_mechanical_tags_visible_material
contract: C_gen_biomes_tags_and_look
create_world_open: auto_gen_from_bias_dials_plus_biomes
enter_craft_empty: kept_1g_manual_lane_only_until_place
generate_button_as_product_ux: barred_struck
pack_organic_seed_retained: true
status: live_weld_landed_staging_awaiting_f5
selection_rationale: operator_f5_pass_pack_save_load_arm_gen_biomes
not_selected: GEN-sites
do_not_arm: GEN-sites
keep: false
ask_success: false
next_world_armed: false
welds:
  B1: landed_biomes_assigned_after_terrain_altitude_climate
  B2: landed_two_plus_land_biome_material_tints
  B3: landed_mechanical_tag_move_difficult_hover_probe
  B4: landed_create_world_open_auto_enter_craft_empty_pack_ok
  B5: landed_nursery_salts_parked_gen_sites_unarmed_no_creatures
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
trinity_branch: project/genesis-mythos-master
trinity_push: local_tip_only_push_enabled_false
trinity_tip: 7c89c2d44f01522895a1ea25f32b24d282f10148
trinity_tip_pin: 7c89c2d44f01522895a1ea25f32b24d282f10148
trinity_weld_tip: 2675d229a5c50438c58e05dd5a31591de13a2d29
trinity_prior_tip: 24574024c29e7086cf5e4e6408a76b4cbd3772bb
curator_snapshot: skipped_push_enabled_false
gate_a: ok
completed: 2026-10-16T05:20:00Z
---

# Staging receipt — alpha0_gen_biomes_r1

**Prefer + LIVE** — Biomes with mechanical tags (move/difficult) and visible material tints after Create World Open terrain gen. Hover probe shows name + tag. PACK organic_seed save/load retained. Create World Open auto-gen · Enter Craft empty until place · Generate button stays struck. Nursery salts parked. `claim_class: staging`. **Do not KEEP.** **No ask_success** without operator F5. **`next_world_armed: false`.** **GEN-sites unarmed.**

## Welds landed

| Weld | Evidence |
|------|----------|
| B1 | `GenBiomeService.Assign` after `ApplyGenTerrainPass` from altitude band + climate |
| B2 | DualCell land decks tinted Plains/Forest/Highland/Marsh/Desert albedos |
| B3 | Hover → HUD/hint `Biome {name} · {tag} · move=N` (+ difficult when set) |
| B4 | Create World Open auto; Enter Craft empty; no Generate; pack biomes + organic_seed |
| B5 | Nursery propose/lore parked; GEN-sites unarmed; no creatures |

## LIVE code changed

| File | Change |
|------|--------|
| `Core/WorldGen/GenBiomesContract.cs` | New contract |
| `Core/WorldGen/GenBiomeService.cs` | Assign + specs + tags |
| `Systems/DualGridCraftHost.cs` | Tint, probe, pack biomes serialize/restore |
| `Systems/WorldgenCraft.cs` | Hover biome probe |
| `LaunchShell.cs` / `WorldPackage.cs` / `PackSaveLoadContract.cs` | Pin + feedstock |

## Gate A

`prefer_map_fidelity_check.py` → ok (hostile Prefer pending before KEEP — expected staging).

## Trinity / Curator

| Item | Value |
|------|-------|
| Tip | `7c89c2d44f01522895a1ea25f32b24d282f10148` (weld `2675d229`) |
| Prior | `24574024c29e7086cf5e4e6408a76b4cbd3772bb` |
| Push | local tip only (`git.push_enabled: false`) |
| Curator | skipped (`push_enabled: false`) |

## F5 expected behavior

Create World → bias + dials mid → Open → see at least two biome looks on land (not one flat material). Hover land: HUD/hint shows biome name + tag; tags differ so move cost / difficult readout changes (e.g. Plains `move:1` vs Forest `difficult+move:2`). Water vs land still clear. F5 Save → Load World still restores board. Blank amber or string-only with identical look = FAIL. Enter Craft empty. No Generate button.
