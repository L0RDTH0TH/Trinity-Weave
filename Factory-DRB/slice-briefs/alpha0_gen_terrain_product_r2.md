---
slice_id: alpha0_gen_terrain_product_r2
ask_id: alpha0_gen_terrain_product
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: gen_terrain_product
created: 2026-10-16
updated: 2026-10-16
live_weld_landed_at: '2026-10-16T03:40:00Z'
composed_at: '2026-10-16T03:40:00Z'
prefer_deepened_at: '2026-10-16T03:40:00Z'
prior_product_slice: alpha0_gen_terrain_product_r1
altitude_bands_deepened: true
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_world_slice: alpha0_gen_terrain_r1
prior_world_step: 2a
prior_world_note: GEN-terrain_T-hotkey_INCOMPLETE_superseded_keep_callable_accel_only
keeps_world_new: alpha0_world_new_r1
keeps_world_new_fidelity: KEEP-real
keeps_world_bounds: alpha0_world_bounds_dials_r1
keeps_world_bounds_fidelity: staging_paid_with_proof_GEN_W2
keeps_world_propose: alpha0_world_propose_feed_r1
keeps_world_propose_fidelity: staging_propose_feed_awaiting_f5
keeps_world_s0_intents: alpha0_world_s0_dm_lore_honesty_r1
keeps_world_s0_fidelity: staging_dm_lore_honesty_awaiting_f5
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
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_gen_terrain_product_r2.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map_id: GEN-terrain-product
success_object: generated_land_water_height_rivers_from_ui
contract: C_gen_terrain_product_w1_w5
operator_f5_confirmed: false
disposition: staging
selection_rationale: operator_flesh_terrain_gen_azgaar_altitude_anchor
empty_enter_law: enter_craft_manual_lane_only_1g_KEEP-real
create_world_open_law: auto_run_gen_pass_from_bias_dials
regen_law: dials_change_plus_reopen_or_session_rebind
do_not_arm_next: GEN-tone
next_world_armed: false
---

# Slice brief — `alpha0_gen_terrain_product_r2`

**GREENLIGHT WELD LIVE landed (staging)** — Prefer deepen for **`GEN-terrain-product`** (W1–W5): **Azgaar-style altitude bands** → clearer land/water share, craft-visible height relief, downhill river watercourses. Generate button stays struck. Create World → Open auto-gens. Enter Craft stays empty until place. `claim_class: staging`. **Do not mark KEEP.** **Do not arm GEN-tone / GEN-biomes / PACK-save-load.** `next_world_armed: false`. Prior [[alpha0_gen_terrain_product_r1]] remains feedstock (cell-count sister dial).

**Choice:** Map row = **`GEN-terrain-product`**. First generate that is a product: knobs change the world, Create World Open auto-gens from bias+dials (no Generate button), land/water/height/rivers readable on the dual grid. Owns self-populate. Still not `MINI-hours`.

**Altitude:** Azgaar = options → Open → readable map (**exemplar**, not JS/WebView port). Dual grid = Townscaper **hands** only.

**Lane split (operator binding):**

| Lane | Law |
|------|-----|
| **Create World → Open** | World already generated — auto-run gen pass from bias+dials. Refuse blank amber Open. |
| **Enter Craft** | Empty amber board until operator places. 1g empty-enter KEEP applies to this lane **ONLY**. |
| **Generate button** | **Struck.** Refuse `generate_button_as_product_ux`. |
| **Regen** | Dials change + re-Open / session rebind. Key.T accel only — never Success. |

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `GEN-terrain-product` in [[World-Builder-Mini-Game-Ticket-Map]]. Law: [[Prefer-Authorship-Host-Law]] § C.3.

## Why (binding)

| Gate | Detail |
|------|--------|
| GEN-terrain-product | W1–W5 all required for any future KEEP |
| Create World Open | Auto gen from dials/bias — refuse `empty_create_world_open` |
| Enter Craft | Empty amber until place — 1g KEEP-real (manual lane only) |
| Generate button | **Refused** as product UX |
| Dials | Cell size / cell count / rivers / climate / wildness reshape the board (W2) |
| Altitude | DeepOcean / Shelf / Lowland / Highland / Peak → land share + height lift (W3/W4) |
| Rivers | Dial 0 = no blue corridors; dial high = ridge + downhill watercourses (W5) |
| Out | KEEP · ask_success without F5 · GEN-tone arm · GEN-biomes · Azgaar port · Townscaper Done · generate_button_as_product_ux · hotkey_as_product_ux · config_meta_without_effect |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_gen_terrain_product` |
| `slice_id` | `alpha0_gen_terrain_product_r2` |
| `ticket_map_id` | **`GEN-terrain-product`** |
| `success_object` | **`generated_land_water_height_rivers_from_ui`** |
| Scope | Prefer deepen + LIVE altitude/rivers weld · staging until F5 |
| `claim_class` | `staging` until operator F5 on **all** W1–W5 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |

## 2. Welds (all required)

| Weld | Proof |
|------|-------|
| **W1** | No Generate product button. Create World → Open is the gen surface. Regen = dials + re-Open. `Key.T` accel only — never Success. |
| **W2** | Cell size, cell count, rivers, climate, wildness change the pass (not meta-only). Cell size → landform frequency; Cell count → seed rings / board footprint. Climate → sea level / land share. Wildness → relief roughness. |
| **W3** | Land vs water = dual-grid occupancy from altitude vs sea. Create World Open auto-applies; Enter Craft stays empty until place. |
| **W4** | Height / altitude bands read in craft view (peaks high vs shelf/ocean low). |
| **W5** | Rivers dial > 0 → readable blue watercourse; dial 0 → not. |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** Create World → dials → Open → board already populated (land/water/height/rivers). Enter Craft → empty amber until place. No Generate button. Regen via dials + re-Open. Dials reshape the board. MCP alone ≠ Success. Partial W* = staging incomplete. |
| Out | Generate-button-as-product · Hotkey-as-product · meta-only dials · blank Create World Open · stub-as-hours · GEN-tone arm · GEN-biomes · Azgaar port · Townscaper Done · KEEP without F5 |

## 4. Refuse (`do_not_waive`)

`generate_button_as_product_ux` · `hotkey_as_product_ux` · `config_meta_without_effect` · `stub_as_hours` · `map_job_name_only` · `explicit_met_implicit_miss` · `intent_collapsed_to_mechanics` · `proxy_substitution` · `gen_fill_as_craft_enter` · `empty_create_world_open` · `verify_mcp_only` · `terrain3d_in_scope` · `undo_empty_enter_1g` · `azgaar_js_port_as_success` · `gen_biomes_as_terrain_success` · `gen_tone_not_armed_until_terrain_f5`

## 5. LIVE weld (landed)

`GenTerrainService` r2: multi-octave elevation → sea level from climate/bias → altitude bands → land/water; river ridge + downhill carve when rivers>0; height lift scaled. `DualGridCraftHost.ApplyGenTerrainPass` remesh (cell count) + adjacency river polish + wider blue ribbon. Generate chrome stays struck. Create World Open auto-gen kept. Enter Craft empty. Key.T accel only. **Do not arm GEN-tone.** Not KEEP / not ask_success until F5.

## 6. Operator F5 expected behavior (Play-path paragraph)

Create World → set Cell count **2** → Open → count cells/footprint: small board (few rings). New world → Cell count **8** → Open → obviously larger / more cells. Rivers **0** → no blue corridors on the dual grid; rivers **high** → visible blue watercourses from highlands toward shelf. Climate low vs high → land share / water shelf clearly different. Wildness low vs high → relief smoother vs more broken. Height/climate change readable as land share and craft Y relief (peaks up, ocean/shelf low). Blank amber Create World Open = **FAIL**. Enter Craft still opens empty amber until place. No Generate button. GEN-tone stays unarmed this pass.

## Related

- Prior [[alpha0_gen_terrain_product_r1]] · incomplete [[alpha0_gen_terrain_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]] · [[Prefer-Authorship-Host-Law]]
