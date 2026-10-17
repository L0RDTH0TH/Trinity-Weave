---
slice_id: alpha0_gen_terrain_product_r1
ask_id: alpha0_gen_terrain_product
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: gen_terrain_product
created: 2026-10-15
updated: 2026-10-16
live_weld_landed_at: '2026-10-16T00:50:00Z'
composed_at: '2026-10-15T23:10:00Z'
prefer_amended_at: '2026-10-16T00:50:00Z'
cell_count_dial_amended: true
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_world_slice: alpha0_gen_terrain_r1
prior_world_step: 2a
prior_world_note: GEN-terrain_T-hotkey_INCOMPLETE_superseded_keep_callable_accel_only
prior_blank_open_note: F5_FAIL_incomplete_blank_Create_World_Open_amended_lane_split
prior_generate_button_note: Generate_button_product_ux_struck_operator_order
keeps_world_new: alpha0_world_new_r1
keeps_world_new_fidelity: KEEP-real
keeps_world_bounds: alpha0_world_bounds_dials_r1
keeps_world_bounds_fidelity: staging_paid_with_proof_GEN_W2
keeps_world_propose: alpha0_world_propose_feed_r1
keeps_world_propose_fidelity: staging_propose_feed_awaiting_f5
keeps_world_s0_intents: alpha0_world_s0_optional_lore_r1
keeps_world_s0_fidelity: staging_optional_lore_salts_gen_when_present
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
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_gen_terrain_product_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map_id: GEN-terrain-product
success_object: generated_land_water_height_rivers_from_ui
contract: C_gen_terrain_product_w1_w5
operator_f5_confirmed: false
disposition: staging
selection_rationale: operator_kill_generate_button_Create_World_Open_remains_auto_gen
empty_enter_law: enter_craft_manual_lane_only_1g_KEEP-real
create_world_open_law: auto_run_gen_pass_from_bias_dials
regen_law: dials_change_plus_reopen_or_session_rebind
do_not_arm_next: GEN-biomes
next_world_armed: false
---

# Slice brief — `alpha0_gen_terrain_product_r1`

**GREENLIGHT WELD LIVE landed (staging)** — Prefer amend for **`GEN-terrain-product`** (W1–W5): **Cell count** dial sister to **Cell size** (W2). Generate button stays struck. Create World → Open still auto-gens. Enter Craft stays empty until place. `claim_class: staging`. **Do not mark KEEP.** **Do not arm GEN-biomes / GEN-tone / PACK-save-load.** `next_world_armed: false`.

**Choice:** Map recovery row = **`GEN-terrain-product`**. First generate that is a product: knobs change the world, Create World Open auto-gens from bias+dials (no Generate button product control), land/water/height/rivers readable on the dual grid. Owns self-populate. Still not `MINI-hours`.

**Altitude:** Azgaar = options → Open → readable map (**exemplar**, not JS/WebView port). Dual grid = Townscaper **hands** only.

**Lane split (operator binding):**

| Lane | Law |
|------|-----|
| **Create World → Open** | World already generated — auto-run same gen pass from bias+dials. Refuse blank amber Open. |
| **Enter Craft** | Empty amber board until operator places. 1g empty-enter KEEP applies to this lane **ONLY**. |
| **Generate button** | **Struck.** No Generate / Generate (regen) product control. Refuse `generate_button_as_product_ux`. |
| **Regen** | Dials change + re-Open / session rebind. Key.T accel only — never Success. |

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `GEN-terrain-product` in [[World-Builder-Mini-Game-Ticket-Map]]. Law: [[Prefer-Authorship-Host-Law]] § C.3.

## Why (binding)

| Gate | Detail |
|------|--------|
| GEN-terrain-product | W1–W5 all required for any future KEEP |
| Create World Open | Auto gen from dials/bias — refuse `empty_create_world_open` |
| Enter Craft | Empty amber until place — 1g KEEP-real (manual lane only) |
| Generate button | **Refused** as product UX — no chrome, no Success surface |
| Regen | Dials + re-Open / session rebind · Key.T accel only |
| Dials | Cell size / **cell count** / rivers / climate / wildness change the pass (W2) |
| Out | KEEP · ask_success without F5 · GEN-biomes/GEN-tone/PACK arm · Azgaar port · Townscaper Done · generate_button_as_product_ux · hotkey_as_product_ux · config_meta_without_effect |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_gen_terrain_product` |
| `slice_id` | `alpha0_gen_terrain_product_r1` |
| `ticket_map_id` | **`GEN-terrain-product`** |
| `success_object` | **`generated_land_water_height_rivers_from_ui`** |
| Scope | Prefer + LIVE W1–W5 weld · staging until F5 |
| `claim_class` | `staging` until operator F5 on **all** W1–W5 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |

## 2. Welds (all required)

| Weld | Proof |
|------|-------|
| **W1** | No Generate / Generate (regen) product button. Create World → Open is the gen surface. Regen = dials + re-Open. `Key.T` accel only — never Success. |
| **W2** | Cell size, **cell count**, rivers, climate, wildness change the pass (crude OK; meta-only = `config_meta_without_effect`). Cell size → landform frequency; Cell count → seed rings / board cell budget (higher → more cells on Open). |
| **W3** | Land vs water = dual-grid occupancy from that pass. Create World Open auto-applies; Enter Craft stays empty until operator places. |
| **W4** | Height reads in craft view (high vs low visible). |
| **W5** | Rivers dial > 0 → readable watercourse; dial 0 → not. |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** Create World → dials → Open → board already populated (land/water/height/rivers). Enter Craft → empty amber until place. No Generate button. Regen via dials + re-Open. Dials change the pass. MCP alone ≠ Success. Partial W* = staging incomplete. |
| Out | Generate-button-as-product · Hotkey-as-product · meta-only dials · blank Create World Open · stub-as-hours · GEN-biomes · Azgaar port · Townscaper Done · KEEP without F5 |

## 4. Refuse (`do_not_waive`)

`generate_button_as_product_ux` · `hotkey_as_product_ux` · `config_meta_without_effect` · `stub_as_hours` · `map_job_name_only` · `explicit_met_implicit_miss` · `intent_collapsed_to_mechanics` · `proxy_substitution` · `gen_fill_as_craft_enter` · `empty_create_world_open` · `verify_mcp_only` · `terrain3d_in_scope` · `undo_empty_enter_1g` · `azgaar_js_port_as_success` · `gen_biomes_as_terrain_success`

## 5. LIVE weld (landed + Prefer amend)

W1 Generate product chrome **removed** (`MountGenerateChrome` / `GenerateTerrainButton` struck). Create World Open → deferred `AutoGenCreateWorldOpen` → `ApplyGenTerrainPass` **kept**. Enter Craft skips auto-gen. Key.T remains accel only (never Success). W2 dials change pass. W3 dual-grid occupancy; lane-split empty. W4 gen height lift. W5 river ribbon when rivers>0. Reuse GenTerrainService from 2a as callable — do not KEEP 2a. Not KEEP / not ask_success until F5.

## 6. Operator F5 bar

Layer 0 owns the long tutorial. Compact checklist returned to Layer 0 for this ticket only.

## Related

- Prior incomplete [[alpha0_gen_terrain_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]] · [[Prefer-Authorship-Host-Law]]
