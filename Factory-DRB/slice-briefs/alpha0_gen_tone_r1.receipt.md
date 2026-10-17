---
title: Staging receipt — alpha0_gen_tone_r1
slice_id: alpha0_gen_tone_r1
ask_id: alpha0_gen_tone
series_id: alpha0_world_builder_r1
series_step: gen_tone
ticket_map_id: GEN-tone
producer_run_id: sp-gen-tone-r1-bias-landform
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
prior_product_slice: alpha0_gen_terrain_product_r2
prior_product_disposition: operator_f5_pass_knobs_change_gen_r2
success_object: bias_reshapes_land_water_rivers_relief
contract: C_gen_tone_same_seed_two_biases
create_world_open: auto_gen_from_bias_dials
enter_craft_empty: kept_1g_manual_lane_only_until_place
generate_button_as_product_ux: barred_struck
bias_landform: true
same_dials_seed: bias_not_hashed
status: live_weld_landed_staging_awaiting_f5
selection_rationale: operator_f5_pass_terrain_product_r2_arm_gen_tone
not_selected: PACK-save-load
do_not_arm: PACK-save-load GEN-biomes
keep: false
ask_success: false
next_world_armed: false
welds:
  T1: landed_bias_landform_sea_continent_relief_rivers
  T2: landed_same_dials_seed_bias_not_hashed
  T3: landed_high_vs_grimdark_characteristic_difference
  T4: landed_create_world_open_auto_enter_craft_empty_no_generate
  T5: landed_nursery_salts_parked_pack_biomes_unarmed
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
trinity_branch: project/genesis-mythos-master
trinity_push: local_tip_only_push_enabled_false
trinity_tip: ad65543860d32639e262b87320577f352c98f8a6
trinity_tip_pin: ad65543860d32639e262b87320577f352c98f8a6
trinity_prior_tip: 5ad5e627da9586dfc0d849260cb91d19fa1bd2b2
curator_snapshot: skipped_push_enabled_false
gate_a: ok
completed: 2026-10-16T04:10:00Z
---

# Staging receipt — alpha0_gen_tone_r1

**Prefer + LIVE** — Create World bias drives landform (sea / continent shape / relief / rivers). Same dials → same dials-derived seed; two biases → different board. Create World Open auto-gen · Enter Craft empty until place · Generate button stays struck. Nursery salts parked. `claim_class: staging`. **Do not KEEP.** **No ask_success** without operator F5. **`next_world_armed: false`.** **PACK / GEN-biomes unarmed.**

## Welds landed

| Weld | Evidence |
|------|----------|
| T1 | `BiasLandform` per High/Medium/Low/Grimdark modulates sea, freq/aniso, detail/fragment, relief, river width/runoff |
| T2 | `DeriveSeed` = dials (+ parked scaffold/lore) only — bias not hashed |
| T3 | High = fuller land / clearer rivers; Grimdark = scarred breakup / harsher relief / thinner scour |
| T4 | Create World Open auto-gen; Enter Craft empty; no Generate button |
| T5 | Nursery propose/lore stay parked; PACK / GEN-biomes unarmed |

## LIVE code changed

| File | Change |
|------|--------|
| `Core/WorldGen/GenToneContract.cs` | New GEN-tone law constants |
| `Core/WorldGen/GenTerrainService.cs` | BiasLandform + dials-only DeriveSeed + bias reshape pass |
| `Core/WorldGen/GenTerrainContract.cs` | Feedstock note; successor = GEN-tone |
| `Core/WorldGen/WorldPackage.cs` | Active slice → GenToneContract; schema 9 |
| `Systems/WorldgenCraft.cs` | Create World Open log → GEN-tone |

## Gate A

`prefer_map_fidelity_check.py` → ok (hostile Prefer pending before KEEP — expected staging).

## F5 expected behavior

Create World → pick **High Fantasy** → leave dials at a fixed mid setting → Reject scaffold / skip lore so salts stay clear → Open → note land share, coast silhouette, river corridors, and craft relief. New world → **same dials** → pick **Grimdark** → same salt path → Open → board is **obviously different** (more water / scarred breakup / harsher relief / thinner scour rivers vs High’s fuller land and clearer watercourses). Identical boards = **FAIL**. Blank amber Open = **FAIL**. Enter Craft still opens empty amber until place. No Generate button.
