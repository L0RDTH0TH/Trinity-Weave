---
slice_id: alpha0_world_propose_feed_r1
ask_id: alpha0_world_propose_feed
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1c_propose_feed
created: 2026-10-16
updated: 2026-10-16
live_weld_landed_at: '2026-10-16T00:19:45Z'
composed_at: '2026-10-16T00:19:45Z'
prefer_amended_at: '2026-10-16T00:19:45Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: nursery_parked_effect_deferred_to_gen
operator_parked: true
effect_deferred_to_gen: true
refuse_ask_success_on: salt_only_f5
template: Half-B-Weld-Brief-Template
prior_world_slice: alpha0_world_propose_r1
prior_world_step: 1c
prior_world_note: KEEP-debt_menu_only_superseded_by_propose_feed_do_not_KEEP
keeps_world_new: alpha0_world_new_r1
keeps_world_new_fidelity: KEEP-real
keeps_world_bounds: alpha0_world_bounds_dials_r1
keeps_world_bounds_fidelity: staging_paid_with_proof_GEN_W2
keeps_world_propose: alpha0_world_propose_r1
keeps_world_propose_fidelity: nursery_parked_effect_deferred_to_gen
keeps_world_s0_intents: alpha0_world_s0_dm_lore_honesty_r1
keeps_world_s0_fidelity: nursery_parked_effect_deferred_to_gen
keeps_world_import: alpha0_world_import_r1
keeps_world_import_fidelity: KEEP-debt_parked
keeps_world_empty_campaigns: alpha0_world_empty_campaigns_r1
keeps_world_empty_campaigns_fidelity: KEEP-real
keeps_world_parity: alpha0_world_parity_r1
keeps_world_parity_fidelity: KEEP-real
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_world_propose_feed_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map_id: WORLD-propose
success_object: scaffold_accept_feeds_gen_pass
contract: C_world_propose_feed_w1_w3
operator_f5_confirmed: false
disposition: nursery_parked_effect_deferred_to_gen
selection_rationale: operator_park_stubs_effect_deferred_to_gen
do_not_arm_next: GEN-tone
next_world_armed: false
parked_at: '2026-10-16T03:34:58Z'
---

# Slice brief — `alpha0_world_propose_feed_r1`

**Operator park — nursery parked, effect deferred to GEN.** Prefer for **`WORLD-propose`** (1c). Capture/LIVE may exist; **not KEEP**. Visible board Success waits on terrain gen. **Refuse ask_success on salt-only F5.** Prior [[alpha0_world_propose_r1]] menu-only = KEEP-debt. Generate button stays absent. Do **not** arm GEN-tone. Next work = `GEN-terrain-product` deepen (sibling owns Prefer + LIVE weld).

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `WORLD-propose` in [[World-Builder-Mini-Game-Ticket-Map]]. Law: [[Prefer-Authorship-Host-Law]] § C.3.

## Why (binding)

| Gate | Detail |
|------|--------|
| WORLD-propose | Accept/reject/revise change scaffold the generator uses |
| W1 | Accept binds GenFeedSalt + coast/ridge axes into Create World Open gen pass |
| W2 | Propose again / Revise mints new salt → visibly different land/water |
| W3 | Reject clears feed; Accept after Reject requires a new Propose |
| Out | KEEP · ask_success without F5 · menu-only · meta-without-gen · GEN-tone/biomes/PACK · Generate button re-add |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_world_propose_feed` |
| `slice_id` | `alpha0_world_propose_feed_r1` |
| `ticket_map_id` | **`WORLD-propose`** |
| `success_object` | **`scaffold_accept_feeds_gen_pass`** |
| Scope | Prefer + LIVE propose→gen feed · staging until F5 |
| `claim_class` | `staging` until operator F5 on **all** W1–W3 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |

## 2. Welds (all required)

| Weld | Proof |
|------|-------|
| **W1** | Accept binds scaffold feed salt into Create World Open gen pass (menu-only ≠ Success). |
| **W2** | Propose again / Revise changes GenFeedSalt → different land/water on Open. |
| **W3** | Reject clears feed; Accept after Reject needs a new Propose. |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** Create World → Propose → Accept → Open → board reflects that scaffold feed. Propose again / Revise → Open → different land/water. Reject → no feed until new Propose. MCP alone ≠ Success. Partial = staging incomplete. |
| Out | Menu-only Accept · scaffold meta without gen effect · KEEP without F5 · forward MAP arm · Generate button re-add |

## 4. Refuse (`do_not_waive`)

`hotkey_as_product_ux` · `config_meta_without_effect` · `stub_as_hours` · `map_job_name_only` · `explicit_met_implicit_miss` · `intent_collapsed_to_mechanics` · `menu_only_propose_as_success` · `scaffold_meta_without_gen_effect` · `proxy_substitution` · `verify_mcp_only` · `gen_tone_biomes_pack_not_this_debt`

## 5. LIVE weld (landed)

`WorldScaffoldProposal` carries `GenFeedSalt` / coast / ridge. Reject clears salt. Accept keeps salt. `GenTerrainService.Compute` mixes salt into seed + applies axis biases. Create World Open / Key.T pass package scaffold. No Generate button re-add. Not KEEP / not ask_success until F5.

## 6. Operator F5 bar

Layer 0 owns the long tutorial. Compact checklist returned to Layer 0 for this ticket only.

## Related

- Prior menu-only [[alpha0_world_propose_r1]] · Product sibling [[alpha0_gen_terrain_product_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · [[Prefer-Authorship-Host-Law]]
