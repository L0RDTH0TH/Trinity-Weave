---
slice_id: alpha0_pack_save_load_r1
ask_id: alpha0_pack_save_load
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: pack_save_load
created: 2026-10-16
updated: 2026-10-16
live_weld_landed_at: '2026-10-16T04:25:00Z'
composed_at: '2026-10-16T04:25:00Z'
prefer_authored_at: '2026-10-16T04:25:00Z'
operator_f5_fail_at: '2026-10-16T04:51:00Z'
f5_fail_fix_at: '2026-10-16T04:55:00Z'
prior_product_slice: alpha0_gen_tone_r1
prior_product_ticket: GEN-tone
prior_product_disposition: operator_f5_pass_bias_landform_working
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5_after_organic_seed_fix
template: Half-B-Weld-Brief-Template
operator_f5_fail_note: map_persisted_terrain_died_regened_on_load_organic_seed_not_persisted
keeps_world_new: alpha0_world_new_r1
keeps_world_new_fidelity: KEEP-real
keeps_world_bounds: alpha0_world_bounds_dials_r1
keeps_world_bounds_fidelity: staging_paid_with_proof_GEN_W2
keeps_world_propose: alpha0_world_propose_feed_r1
keeps_world_propose_fidelity: nursery_parked_effect_deferred_to_gen
keeps_world_s0_intents: alpha0_world_s0_dm_lore_honesty_r1
keeps_world_s0_fidelity: nursery_parked_effect_deferred_to_gen
keeps_world_import: alpha0_world_import_r1
keeps_world_import_fidelity: KEEP-debt_parked
keeps_world_empty_campaigns: alpha0_world_empty_campaigns_r1
keeps_world_empty_campaigns_fidelity: KEEP-real
keeps_world_parity: alpha0_world_parity_r1
keeps_world_parity_fidelity: KEEP-real
keeps_brush_tri: alpha0_stalberg_dual_tri_cell_place_r1
keeps_brush_single_deck: alpha0_stalberg_dual_single_deck_emit_r1
keeps_brush_update_four: alpha0_stalberg_dual_update_four_recompute_r1
keeps_brush_coast_bits: alpha0_stalberg_dual_place_coast_r1
keeps_brush_strip_water: alpha0_stalberg_dual_coast_strip_water_r1
keeps_brush_coast_stage6_landed: alpha0_stalberg_dual_coast_stage6_emit_r1
prior_gen_tone: alpha0_gen_tone_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_pack_save_load_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map_id: PACK-save-load
success_object: quit_reload_same_generated_world_board
contract: C_pack_save_load_quit_reload_same_board
operator_f5_confirmed: false
disposition: staging
selection_rationale: operator_f5_pass_gen_tone_arm_pack_save_load
empty_enter_law: enter_craft_manual_lane_only_1g_KEEP-real
create_world_open_law: auto_run_gen_pass_from_bias_dials
regen_law: dials_change_plus_reopen_or_session_rebind
do_not_arm_next: GEN-biomes
next_world_armed: false
---

# Slice brief — `alpha0_pack_save_load_r1`

**GREENLIGHT WELD LIVE landed (staging)** — Prefer for **`PACK-save-load`**: quit and reload the same generated world (bias, dials, land/water/height/rivers, optional hand edit) from a real `user://worldgen/world_package_v1.json` pack — not a fake toast. Create World → Open still auto-gens (GEN-tone BiasLandform). Enter Craft empty until place. No Generate button. Nursery salt stubs stay parked. 1e Import stays parked (use Load World). `claim_class: staging`. **Do not mark KEEP.** **Do not arm GEN-biomes.** Prior [[alpha0_gen_tone_r1]] operator F5 working.

**Operator F5 FAIL (2026-10-16):** Save wrote corners, Load restored indices, but board silhouette died / looked regened — organic Stålberg remesh used a **new random seed** on Load, so vertex indices mapped onto a different mesh (cell counts 101→108). **Fix:** persist `organic_seed` (+ spacing) in pack; Load always remeshes with that seed before reapplying corners/heights/rivers; Load World sticky bars AutoGen after restore. **Re-F5:** Create World → Open → F5 save (new pack must include `organic_seed`) → quit → Load World → **same silhouette**. Pre-fix packs without `organic_seed` must be re-saved.

**Choice:** Map row = **`PACK-save-load`**. Quit and reload the same world, including a hand edit.

**Lane split (operator binding):**

| Lane | Law |
|------|-----|
| **Create World → Open** | Auto-run gen pass from bias landform + dials. Refuse blank amber Open. |
| **F5 / pack save** | Writes real pack file (bias, dials, gen occupancy/height/rivers). |
| **Load World** | Restores same board facts after quit/reload. Blank amber / lost world = FAIL. |
| **Enter Craft** | Empty amber board until operator places. 1g empty-enter KEEP applies to this lane **ONLY**. |
| **Generate button** | **Struck.** Refuse `generate_button_as_product_ux`. |
| **Import (1e)** | Parked — Load World owns quit/reload; do not fake full canon ingest. |
| **Nursery salts** | Propose-feed / lore stubs stay parked. |

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `PACK-save-load` in [[World-Builder-Mini-Game-Ticket-Map]]. Law: [[Prefer-Authorship-Host-Law]] § C.3.

## Why (binding)

| Gate | Detail |
|------|--------|
| PACK-save-load | Quit and reload the same generated world, including a hand edit |
| Real file | `user://worldgen/world_package_v1.json` — not toast-only |
| Same board | Land/water silhouette / counts (and height/rivers) match after Load |
| Create World Open | Auto gen retained — refuse blank amber |
| Enter Craft | Empty amber until place |
| Generate button | Refused as product UX |
| Out | KEEP · ask_success without F5 · GEN-biomes · fake toast · blank after load · unpark nursery salts · friends/roster |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_pack_save_load` |
| `slice_id` | `alpha0_pack_save_load_r1` |
| `ticket_map_id` | **`PACK-save-load`** |
| `success_object` | **`quit_reload_same_generated_world_board`** |
| Scope | Prefer + LIVE pack persist/restore · staging until F5 |
| `claim_class` | `staging` until operator F5 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |

## 2. Welds (all required)

| Weld | Proof |
|------|-------|
| **P1** | Persist writes real pack (bias, dials, gen corner land/water, heights, rivers) under `user://`. |
| **P2** | Load World restores package + board after quit/reload — same silhouette / counts. |
| **P3** | Optional hand edit (dual place / corner flip) survives reload. |
| **P4** | Create World Open auto-gen; Enter Craft empty; no Generate button; GEN-tone BiasLandform retained. |
| **P5** | Nursery salts parked; 1e Import parked; GEN-biomes unarmed. |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** Create World → bias+dials → Open → note land/water. Optional: one dual edit. F5 Save. Quit/reload. Load World → **same board facts**. Lost world or blank amber = FAIL. Enter Craft still empty for new craft. No Generate button. MCP alone ≠ Success. |
| Out | Blank after load · lost world · toast-only · Generate button · KEEP without F5 · GEN-biomes |

## 4. Refuse (`do_not_waive`)

`blank_amber_after_load` · `lost_world_after_load` · `fake_toast_as_save` · `hotkey_as_product_ux` · `config_meta_without_effect` · `stub_as_hours` · `map_job_name_only` · `explicit_met_implicit_miss` · `intent_collapsed_to_mechanics` · `generate_button_as_product_ux` · `empty_create_world_open` · `gen_fill_as_craft_enter` · `proxy_substitution` · `verify_mcp_only` · `gen_biomes_not_armed` · `nursery_salt_stubs_stay_parked` · `world_import_full_ingest_parked_until_pack`

## 5. LIVE weld (landed + F5-fail fix)

`PackSaveLoadContract` + `DualGridCraftHost.Persist/Load` write/read full pack including **`organic_seed`** / `seed_spacing`; LaunchShell **Load World**; WorldgenCraft F5 save + restore remeshes with persisted seed then reapplies corners/heights/rivers (skips AutoGen wipe; sticky `MetaPackLoadedFromPersist`). Create World Open auto-gen kept. Enter Craft empty. Generate chrome stays struck. GEN-tone BiasLandform kept. Nursery salts parked. **Do not arm GEN-biomes.** Not KEEP / not ask_success until F5.

## 6. Operator F5 expected behavior (Play-path paragraph)

Create World → pick a bias → set dials → Open → note land/water silhouette (and rivers/relief if readable). Optional: place one dual cell / flip one corner. Press **F5** to save the pack (must write `organic_seed` into `user://worldgen/world_package_v1.json`). Quit craft or reload the session. From LaunchShell press **Load World** → the **same board silhouette** returns (land/water shape / counts match; hand edit still there if you made one) — **not** a fresh Create World auto-gen and **not** scrambled vertices on a new organic mesh. Lost world, blank amber, or a visibly different landmass after load = **FAIL**. Enter Craft for a fresh manual session still opens empty amber until place. No Generate button.

## Related

- Prior [[alpha0_gen_tone_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]] · [[Prefer-Authorship-Host-Law]]
