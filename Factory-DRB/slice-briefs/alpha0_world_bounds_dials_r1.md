---
slice_id: alpha0_world_bounds_dials_r1
ask_id: alpha0_world_bounds_dials
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1b_bounds_dials
created: 2026-10-16
updated: 2026-10-16
prefer_composed_at: '2026-10-16T00:36:00Z'
prefer_amended_at: '2026-10-16T00:50:00Z'
cell_count_dial_amended: true
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_concept_required: true
status: staging_paid_with_proof_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_world_slice: alpha0_world_bounds_r1
prior_world_step: 1b
prior_world_note: KEEP-debt_feedstock_only_grid_unchanged_by_design_superseded_proof_on_GEN_W2
proof_owner: alpha0_gen_terrain_product_r1
proof_weld: W2
keeps_world_new: alpha0_world_new_r1
keeps_world_new_fidelity: KEEP-real
keeps_world_bounds: alpha0_world_bounds_r1
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
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_world_bounds_dials_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map_id: WORLD-bounds
success_object: dials_change_create_world_open_gen
contract: C_world_bounds_dials_w2_paid
operator_f5_confirmed: false
disposition: staging
selection_rationale: highest_priority_unpaid_KEEP-debt_weldable_now_label_receipt_close_no_forward_MAP
do_not_arm_next: GEN-tone
next_world_armed: false
---

# Slice brief — `alpha0_world_bounds_dials_r1`

**Prefer + MAP debt close (staging / paid-with-proof)** — Closes **`WORLD-bounds` (1b)** KEEP-debt label. Prior [[alpha0_world_bounds_r1]] feedstock-only KEEP (“grid unchanged by design”) is **superseded as product Success**. Dial effect already lives on [[alpha0_gen_terrain_product_r1]] **W2** (LIVE). This Prefer binds the MAP row to that proof. `claim_class: staging`. **Do not mark KEEP.** **Do not ask_success.** **Do not arm GEN-tone / GEN-biomes / PACK-save-load / MINI-hours.** Generate button stays absent. `next_world_armed: false`.

**Choice:** Highest-priority unpaid KEEP-debt weldable now. LIVE gaps for dial→gen already closed under GEN W2 — Prefer/MAP receipt only. Do not expand 1d. Do not unpark 1e.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `WORLD-bounds` in [[World-Builder-Mini-Game-Ticket-Map]]. Law: [[Prefer-Authorship-Host-Law]] § C.3.

## Why (binding)

| Gate | Detail |
|------|--------|
| WORLD-bounds | Dials: cell size, **cell count**, settlement distance, rivers, climate, wildness |
| Proof | Dials change Create World Open generate — GEN-terrain-product **W2** (not meta-only) |
| Prior | feedstock-only KEEP / “grid unchanged by design” = KEEP-debt superseded |
| Out | KEEP · ask_success without F5 · config_meta_without_effect · GEN-tone arm · Generate button re-add |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_world_bounds_dials` |
| `slice_id` | `alpha0_world_bounds_dials_r1` |
| `ticket_map_id` | **`WORLD-bounds`** |
| `success_object` | **`dials_change_create_world_open_gen`** |
| Scope | Prefer + MAP fidelity · LIVE proof owned by GEN W2 · staging until F5 |
| `claim_class` | `staging` |
| LIVE | no new weld required — `GenTerrainService` already consumes dials |

## 2. Welds (proof pointer)

| Weld | Proof |
|------|-------|
| **W2** (GEN owner) | Cell size, **cell count**, rivers, climate, wildness change the Create World Open pass. Cell count → seed rings / board cell budget. Settlement distance stored on package (sites later). Crude OK; meta-only = `config_meta_without_effect`. |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** Create World → change cell size / cell count / rivers / climate / wildness → Open → board differs (cell count low vs high = more/fewer cells). Same path as GEN-terrain-product W2. MCP alone ≠ Success. Not KEEP without F5. |
| Out | Meta-only dials · feedstock KEEP restored · KEEP without F5 · forward MAP arm · Generate button re-add |

## 4. Refuse (`do_not_waive`)

`hotkey_as_product_ux` · `config_meta_without_effect` · `stub_as_hours` · `map_job_name_only` · `explicit_met_implicit_miss` · `intent_collapsed_to_mechanics` · `feedstock_only_as_bounds_success` · `grid_unchanged_by_design_as_success` · `proxy_substitution` · `verify_mcp_only` · `gen_tone_biomes_pack_not_this_debt`

## 5. LIVE (already landed — Prefer-only this pass)

`WorldBoundsDials` on Create World path → `WorldPackage.Bounds` → remesh seed rings from **cell count** → `GenTerrainService.Compute` (cell size/freq, rivers carve, climate threshold, wildness + seed mix incl. cell count). Create World Open auto-gen. No Generate button. LIVE landed under GEN-terrain-product owner.

## Related

- Prior superseded [[alpha0_world_bounds_r1]] · Proof owner [[alpha0_gen_terrain_product_r1]] · Sibling [[alpha0_world_propose_feed_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]
