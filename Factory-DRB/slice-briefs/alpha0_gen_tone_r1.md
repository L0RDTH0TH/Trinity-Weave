---
slice_id: alpha0_gen_tone_r1
ask_id: alpha0_gen_tone
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: gen_tone
created: 2026-10-16
updated: 2026-10-16
live_weld_landed_at: '2026-10-16T04:05:00Z'
composed_at: '2026-10-16T04:05:00Z'
prefer_authored_at: '2026-10-16T04:05:00Z'
prior_product_slice: alpha0_gen_terrain_product_r2
prior_product_ticket: GEN-terrain-product
prior_product_disposition: operator_f5_pass_knobs_change_gen_r2
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
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_gen_tone_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map_id: GEN-tone
success_object: bias_reshapes_land_water_rivers_relief
contract: C_gen_tone_same_seed_two_biases
operator_f5_confirmed: false
disposition: staging
selection_rationale: operator_f5_pass_terrain_product_r2_arm_gen_tone
empty_enter_law: enter_craft_manual_lane_only_1g_KEEP-real
create_world_open_law: auto_run_gen_pass_from_bias_dials
regen_law: dials_change_plus_reopen_or_session_rebind
do_not_arm_next: PACK-save-load
do_not_arm_also: GEN-biomes
next_world_armed: false
---

# Slice brief — `alpha0_gen_tone_r1`

**GREENLIGHT WELD LIVE landed (staging)** — Prefer for **`GEN-tone`**: same dials (same dials-derived seed when scaffold/lore salts absent), two Create World biases → **visibly different world** (land share / land shape / river feel / relief). Stored bias with identical board = refuse. Bias drives altitude / land-water / rivers / relief — not meta-only, not salt-hash with same silhouette. Create World → Open auto-gens. Enter Craft empty until place. No Generate button. Nursery salt stubs stay parked. `claim_class: staging`. **Do not mark KEEP.** **Do not arm PACK-save-load / GEN-biomes.** Prior [[alpha0_gen_terrain_product_r2]] operator F5 pass (knobs change gen).

**Choice:** Map row = **`GEN-tone`**. Same seed, two biases, different world you can see.

**Lane split (operator binding):**

| Lane | Law |
|------|-----|
| **Create World → Open** | Auto-run gen pass from bias landform + dials. Refuse blank amber Open. |
| **Enter Craft** | Empty amber board until operator places. 1g empty-enter KEEP applies to this lane **ONLY**. |
| **Generate button** | **Struck.** Refuse `generate_button_as_product_ux`. |
| **Regen** | Dials change + re-Open / session rebind. Key.T accel only — never Success. |
| **Nursery salts** | Propose-feed / lore stubs stay parked — do not unpark F5 theater. |

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `GEN-tone` in [[World-Builder-Mini-Game-Ticket-Map]]. Law: [[Prefer-Authorship-Host-Law]] § C.3.

## Why (binding)

| Gate | Detail |
|------|--------|
| GEN-tone | Same dials seed · two biases → different land/water/rivers/relief |
| Bias landform | High vs Grimdark (any two of four) change sea / continent shape / relief / river feel |
| Refuse identical | Stored bias with identical board = FAIL |
| Refuse salt-only | Bias must not be seed salt with same silhouette |
| Create World Open | Auto gen — refuse blank amber |
| Enter Craft | Empty amber until place |
| Generate button | Refused as product UX |
| Out | KEEP · ask_success without F5 · PACK · GEN-biomes · unpark nursery salts · friends/roster |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_gen_tone` |
| `slice_id` | `alpha0_gen_tone_r1` |
| `ticket_map_id` | **`GEN-tone`** |
| `success_object` | **`bias_reshapes_land_water_rivers_relief`** |
| Scope | Prefer + LIVE bias landform weld · staging until F5 |
| `claim_class` | `staging` until operator F5 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |

## 2. Welds (all required)

| Weld | Proof |
|------|-------|
| **T1** | Bias landform modulates sea / continent frequency / anisotropy / detail / relief / river width / runoff — not meta-only. |
| **T2** | Same dials → same dials-derived seed (bias not hashed into seed). Two biases → different board at that seed. |
| **T3** | High vs Grimdark (or any two of four) differ in land share and/or land shape and/or river feel and/or relief — stranger-visible. |
| **T4** | Create World Open auto-applies; Enter Craft empty until place; no Generate button; dials/cell-count/Open laws retained. |
| **T5** | Nursery propose/lore salts stay parked; PACK / GEN-biomes unarmed. |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** Create World → High Fantasy → same dials → Open → note land/water/rivers/relief. New world → same dials → Grimdark → Open → board obviously differs. Identical boards = FAIL. Blank amber = FAIL. Enter Craft empty. No Generate button. MCP alone ≠ Success. |
| Out | Identical boards · salt-only silhouette · meta-only bias · blank Open · Generate button · KEEP without F5 · PACK · GEN-biomes |

## 4. Refuse (`do_not_waive`)

`stored_bias_identical_board` · `bias_salt_hash_same_silhouette` · `config_meta_without_effect` · `generate_button_as_product_ux` · `hotkey_as_product_ux` · `empty_create_world_open` · `gen_fill_as_craft_enter` · `stub_as_hours` · `map_job_name_only` · `explicit_met_implicit_miss` · `intent_collapsed_to_mechanics` · `proxy_substitution` · `verify_mcp_only` · `pack_save_load_not_armed` · `gen_biomes_not_armed` · `nursery_salt_stubs_stay_parked`

## 5. LIVE weld (landed)

`BiasLandform` per `WorldGenBias` in `GenTerrainService`: sea base, freq/aniso, detail/fragment, relief, river width/runoff, rim, warp. `DeriveSeed` = dials (+ parked scaffold/lore salts) only — bias not mixed into seed. Create World Open auto-gen kept. Enter Craft empty. Generate chrome stays struck. Key.T accel only. Nursery salts parked. **Do not arm PACK / GEN-biomes.** Not KEEP / not ask_success until F5.

## 6. Operator F5 expected behavior (Play-path paragraph)

Create World → pick **High Fantasy** → leave dials at a fixed mid setting (Cell count / rivers / climate / wildness unchanged for the pair) → Reject scaffold or skip lore so salts stay clear → Open → note land share, coast silhouette, river corridors, and craft relief. New world → **same dials** → pick **Grimdark** → same salt path → Open → board is **obviously different** (more water / scarred breakup / harsher relief / thinner scour rivers vs High’s fuller land and clearer watercourses). Identical boards = **FAIL**. Blank amber Open = **FAIL**. Enter Craft still opens empty amber until place. No Generate button.

## Related

- Prior [[alpha0_gen_terrain_product_r2]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]] · [[Prefer-Authorship-Host-Law]]
