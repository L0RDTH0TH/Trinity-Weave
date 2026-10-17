---
slice_id: alpha0_gen_biomes_r1
ask_id: alpha0_gen_biomes
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: gen_biomes
created: 2026-10-16
updated: 2026-10-16
live_weld_landed_at: '2026-10-16T05:15:00Z'
composed_at: '2026-10-16T05:15:00Z'
prefer_authored_at: '2026-10-16T05:15:00Z'
prior_product_slice: alpha0_pack_save_load_r1
prior_product_ticket: PACK-save-load
prior_product_disposition: operator_f5_pass_demo_quality_ok
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
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
prior_pack: alpha0_pack_save_load_r1
prior_gen_tone: alpha0_gen_tone_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_gen_biomes_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map_id: GEN-biomes
success_object: biomes_mechanical_tags_visible_material
contract: C_gen_biomes_tags_and_look
operator_f5_confirmed: false
disposition: staging
selection_rationale: operator_f5_pass_pack_save_load_arm_gen_biomes
empty_enter_law: enter_craft_manual_lane_only_1g_KEEP-real
create_world_open_law: auto_run_gen_pass_from_bias_dials
regen_law: dials_change_plus_reopen_or_session_rebind
do_not_arm_next: GEN-sites
next_world_armed: false
---

# Slice brief — `alpha0_gen_biomes_r1`

**GREENLIGHT WELD LIVE landed (staging)** — Prefer for **`GEN-biomes`**: biomes with mechanical tags. No creatures. Each land biome has a tag that changes at least one readout (movement cost or difficult terrain) **and** a visible material / family tint difference at craft cam. String-on-a-cell alone = refuse. Create World → Open auto-gens (terrain + biomes). Enter Craft empty until place. No Generate button. GEN-tone BiasLandform + PACK organic_seed save/load retained. Nursery salt stubs stay parked. `claim_class: staging`. **Do not mark KEEP.** **Do not arm GEN-sites.** Prior [[alpha0_pack_save_load_r1]] operator F5 pass (demo quality OK).

**Choice:** Map row = **`GEN-biomes`**. Biomes with mechanical tags; visible look differs.

**Lane split (operator binding):**

| Lane | Law |
|------|-----|
| **Create World → Open** | Auto-run gen pass from bias landform + dials + biome assign. Refuse blank amber Open. |
| **Hover / probe** | Biome name + mechanical tag + move/difficult on land. Tag differs across biomes. |
| **Enter Craft** | Empty amber board until operator places. 1g empty-enter KEEP applies to this lane **ONLY**. |
| **Generate button** | **Struck.** Refuse `generate_button_as_product_ux`. |
| **Load World / F5** | PACK save/load still restores board (+ biomes). Do not break organic_seed. |
| **Nursery salts** | Propose-feed / lore stubs stay parked. |

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `GEN-biomes` in [[World-Builder-Mini-Game-Ticket-Map]]. Law: [[Prefer-Authorship-Host-Law]] § C.3.

## Why (binding)

| Gate | Detail |
|------|--------|
| GEN-biomes | Biomes with mechanical tags; no creatures |
| Visible look | ≥2 land biome materials/tints readable at craft cam |
| Mechanical tag | Tag changes move cost and/or difficult readout between biomes |
| Refuse string-only | Identical look + string label = FAIL |
| Create World Open | Auto gen — refuse blank amber |
| Enter Craft | Empty amber until place |
| Generate button | Refused as product UX |
| Out | KEEP · ask_success without F5 · GEN-sites · creatures · unpark nursery salts · friends/roster |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_gen_biomes` |
| `slice_id` | `alpha0_gen_biomes_r1` |
| `ticket_map_id` | **`GEN-biomes`** |
| `success_object` | **`biomes_mechanical_tags_visible_material`** |
| Scope | Prefer + LIVE biome assign + tint + probe · staging until F5 |
| `claim_class` | `staging` until operator F5 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |

## 2. Welds (all required)

| Weld | Proof |
|------|-------|
| **B1** | After terrain gen, land cells/regions get biome from altitude/climate/bias dials. |
| **B2** | ≥2 land biomes readable at craft cam (material/color/family tint difference). |
| **B3** | Each biome exposes mechanical tag; hover/HUD probe shows name + tag; tag changes move/difficult readout across biomes. |
| **B4** | Create World Open auto-applies; Enter Craft empty; no Generate button; PACK organic_seed save/load retained. |
| **B5** | Nursery salts parked; GEN-sites unarmed; no creatures. |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** Create World → Open → see ≥2 biome looks on land → hover shows biome name + tag → tags differ (move/difficult) → water vs land clear → Save/Load still restores board. Blank amber or string-only identical look = FAIL. Enter Craft empty. No Generate button. MCP alone ≠ Success. |
| Out | One flat land material · string-only · identical tags · blank Open · Generate button · KEEP without F5 · GEN-sites |

## 4. Refuse (`do_not_waive`)

`string_on_cell_alone_as_biome` · `identical_look_all_land_biomes` · `creatures_as_biome_success` · `config_meta_without_effect` · `generate_button_as_product_ux` · `hotkey_as_product_ux` · `empty_create_world_open` · `gen_fill_as_craft_enter` · `stub_as_hours` · `map_job_name_only` · `explicit_met_implicit_miss` · `intent_collapsed_to_mechanics` · `proxy_substitution` · `verify_mcp_only` · `gen_sites_not_armed` · `nursery_salt_stubs_stay_parked`

## 5. LIVE weld (landed)

`GenBiomeService` assigns Plains/Forest/Highland/Marsh/Desert from altitude band + climate + patch noise. DualCell land decks tint by biome albedo. Hover probe + HUD show name + mechanical tag + move/difficult. Pack persists/restores biomes with organic_seed. Create World Open auto-gen kept. Enter Craft empty. Generate chrome stays struck. Nursery salts parked. **Do not arm GEN-sites.** Not KEEP / not ask_success until F5.

## 6. Operator F5 expected behavior (Play-path paragraph)

Create World → pick any bias → leave dials mid (climate not extreme-zero so multiple biomes appear) → Open → land shows **at least two** biome looks (e.g. bright Plains vs dark Forest vs gray Highland — not one flat green). Hover a land cell: HUD/hint shows **biome name + tag** (e.g. `Plains · move:1` vs `Forest · difficult+move:2`); tags differ so move cost / difficult readout changes. Water stays clear vs land. F5 Save → Load World still restores the same board (organic_seed). Blank amber Open or string-only labels with identical look = **FAIL**. Enter Craft still empty until place. No Generate button.

## Related

- Prior [[alpha0_pack_save_load_r1]] · [[alpha0_gen_tone_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]] · [[Prefer-Authorship-Host-Law]]
