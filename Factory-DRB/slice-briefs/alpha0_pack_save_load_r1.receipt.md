---
title: Staging receipt — alpha0_pack_save_load_r1
slice_id: alpha0_pack_save_load_r1
ask_id: alpha0_pack_save_load
series_id: alpha0_world_builder_r1
series_step: pack_save_load
ticket_map_id: PACK-save-load
producer_run_id: sp-pack-save-load-r1-organic-seed-fix
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
prior_product_slice: alpha0_gen_tone_r1
prior_product_disposition: operator_f5_pass_bias_landform_working
success_object: quit_reload_same_generated_world_board
contract: C_pack_save_load_quit_reload_same_board
create_world_open: auto_gen_from_bias_dials
enter_craft_empty: kept_1g_manual_lane_only_until_place
generate_button_as_product_ux: barred_struck
persist_path: user://worldgen/world_package_v1.json
pack_restore: true
organic_seed_persisted: true
operator_f5_fail: map_persisted_terrain_died_regened_on_load
operator_f5_fail_root_cause: load_remeshed_organic_board_with_new_random_seed_so_corner_indices_mapped_wrong
f5_fail_fix: persist_organic_seed_and_remesh_with_it_on_load_plus_pack_loaded_sticky_bars_autogen
status: live_weld_landed_staging_awaiting_f5_after_organic_seed_fix
selection_rationale: operator_f5_pass_gen_tone_arm_pack_save_load
not_selected: GEN-biomes
do_not_arm: GEN-biomes
keep: false
ask_success: false
next_world_armed: false
welds:
  P1: landed_real_user_data_pack_persist_with_organic_seed
  P2: landed_load_world_restores_same_board_via_seeded_remesh
  P3: landed_hand_edit_survives_reload
  P4: landed_create_world_open_auto_enter_craft_empty_no_generate
  P5: landed_nursery_salts_import_parked_gen_biomes_unarmed
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
trinity_branch: project/genesis-mythos-master
trinity_push: local_tip_only_push_enabled_false
trinity_tip: 24574024c29e7086cf5e4e6408a76b4cbd3772bb
trinity_tip_pin: 24574024c29e7086cf5e4e6408a76b4cbd3772bb
trinity_code_tip: 5e0b416c4550a71f0ce56d167800886c45152679
trinity_prior_tip: 79fe6fbc92954bb03d255e41244752658458d32d
curator_snapshot: skipped_push_enabled_false
gate_a: ok
completed: 2026-10-16T05:02:00Z
---

# Staging receipt — alpha0_pack_save_load_r1 (F5-fail fix)

**Prefer + LIVE** — Quit and reload the same generated world from real `user://worldgen/world_package_v1.json`, including **organic mesh seed** so vertex-bound land/water/height/rivers survive. Create World Open auto-gen · Enter Craft empty until place · Generate button stays struck. GEN-tone BiasLandform retained. Nursery salts parked. 1e Import parked. `claim_class: staging`. **Do not KEEP.** **No ask_success** without operator F5. **`next_world_armed: false`.** **GEN-biomes unarmed.**

## Operator F5 FAIL → fix proof

| Item | Detail |
|------|--------|
| Fail | Map persisted terrain died / looked regened on Load World |
| Root cause | Pack restored corner indices onto a **new random** Stålberg remesh (rings matched; topology did not — stage6 cell counts 101 vs 108) |
| Fix | Persist `organic_seed` + `seed_spacing`; Load always `RegenerateOrganicQuadMesh(rings, seed)` before applying board facts; `MetaPackLoadedFromPersist` sticky so AutoGen cannot wipe after consume |
| Re-F5 | Create World → Open → F5 (new pack with `organic_seed`) → quit → Load World → **same silhouette** |

## Welds landed

| Weld | Evidence |
|------|----------|
| P1 | `DualGridCraftHost.Persist` writes pack with world + gen + **organic_seed** under `user://` |
| P2 | LaunchShell **Load World** + seeded remesh + `RestorePackBoard` restores same board |
| P3 | Corner logic + occupancy cells round-trip — hand edit survives |
| P4 | Create World Open auto-gen; Enter Craft empty; no Generate button |
| P5 | Nursery propose/lore stay parked; 1e Import parked; GEN-biomes unarmed |

## LIVE code changed (fix pass)

| File | Change |
|------|--------|
| `Systems/DualGridCraftHost.cs` | Persist/Load `organic_seed` + `seed_spacing`; always remesh with seed on pack restore |
| `Core/WorldGen/WorldPackageSession.cs` | `MetaPackLoadedFromPersist` sticky; `IsCreateWorldOpenPath` false on Load |
| `Systems/WorldgenCraft.cs` | AutoGen refuses LoadedFromPack; hint lane for Load World |
| `LaunchShell.cs` | Enter Craft clears pack sticky |

## Gate A

`prefer_map_fidelity_check.py` → ok (hostile Prefer pending before KEEP — expected staging).

## F5 expected behavior

Create World → pick a bias → set dials → Open → note land/water silhouette. Optional hand edit. **F5** save (confirm pack has `organic_seed`). Quit/reload. **Load World** → **same silhouette / counts** (not a new gen, not scrambled mesh). Blank amber or different landmass = FAIL. Enter Craft still empty. No Generate button.
