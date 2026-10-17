---
slice_id: alpha0_world_s0_intents_packaging_r1
ask_id: alpha0_world_s0_intents_packaging
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1d_packaging
created: 2026-10-16
updated: 2026-10-16
prefer_composed_at: '2026-10-16T00:58:11Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_concept_required: true
status: staging_packaging_receipt_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_world_slice: alpha0_world_s0_intents_r1
prior_world_step: 1d
prior_world_note: KEEP-debt_soft_KEEP_accept_gate_on_critical_path_superseded_by_packaging
keeps_world_new: alpha0_world_new_r1
keeps_world_new_fidelity: KEEP-real
keeps_world_bounds: alpha0_world_bounds_dials_r1
keeps_world_bounds_fidelity: staging_paid_with_proof_GEN_W2
keeps_world_propose: alpha0_world_propose_feed_r1
keeps_world_propose_fidelity: staging_propose_feed_awaiting_f5
keeps_world_s0_intents: alpha0_world_s0_intents_r1
keeps_world_s0_fidelity: staging_packaging_off_critical_path
keeps_world_import: alpha0_world_import_r1
keeps_world_import_fidelity: KEEP-debt_parked
keeps_world_empty_campaigns: alpha0_world_empty_campaigns_r1
keeps_world_empty_campaigns_fidelity: KEEP-real
keeps_world_parity: alpha0_world_parity_r1
keeps_world_parity_fidelity: KEEP-real
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_world_s0_intents_packaging_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map_id: WORLD-s0-intents
success_object: world_seeds_optional_off_create_world_path
contract: C_world_s0_intents_packaging
operator_f5_confirmed: false
disposition: staging
selection_rationale: highest_priority_unpaid_KEEP-debt_weldable_now_packaging_no_forward_MAP
do_not_arm_next: GEN-tone
next_world_armed: false
---

# Slice brief — `alpha0_world_s0_intents_packaging_r1`

**Prefer + minimal LIVE packaging close (staging)** — Closes **`WORLD-s0-intents` (1d)** KEEP-debt label as packaging. Prior [[alpha0_world_s0_intents_r1]] soft KEEP (Accept≥1 on Create World critical path / campaign-prep framing) is **superseded as product Success**. Seeds stay optional schema, unread until a GEN row consumes them. `claim_class: staging`. **Do not mark KEEP.** **Do not ask_success.** **Do not expand** campaign-seed / intent-graph sprawl. **Do not arm GEN-tone / GEN-biomes / PACK-save-load / MINI-hours.** Generate button stays absent. `next_world_armed: false`. Do not unpark 1e.

**Choice:** Highest-priority unpaid KEEP-debt weldable now. 1e stays parked until save/load. MAP requires seeds off Create World critical path — minimal LIVE seam (skip Intents phase after Accept scaffold). Prefer binds MAP row to that proof.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `WORLD-s0-intents` in [[World-Builder-Mini-Game-Ticket-Map]]. Law: [[Prefer-Authorship-Host-Law]] § C.3.

## Why (binding)

| Gate | Detail |
|------|--------|
| WORLD-s0-intents | World seeds that bias what the world *is* (not campaign attach) |
| Packaging | Seeds optional, off Create World critical path, unread until GEN |
| Prior | soft KEEP / Accept≥1 gate / table-prep framing = KEEP-debt superseded |
| Out | KEEP · expand s0 · campaign attach · GEN-tone arm · Generate button re-add · unpark 1e |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_world_s0_intents_packaging` |
| `slice_id` | `alpha0_world_s0_intents_packaging_r1` |
| `ticket_map_id` | **`WORLD-s0-intents`** |
| `success_object` | **`world_seeds_optional_off_create_world_path`** |
| Scope | Prefer + minimal LIVE skip Intents phase · staging until F5 |
| `claim_class` | `staging` |
| LIVE | Create World Accept scaffold → Open with empty intents; no Accept≥1 gate |

## 2. Welds (packaging proofs)

| Weld | Proof |
|------|-------|
| **P1** | Create World path does not require Session 0 intents phase after Accept scaffold |
| **P2** | Open world lawful with zero accepted seeds; package may carry empty intents |
| **P3** | Seeds remain unread schema until a GEN row consumes them — no campaign-seed sprawl |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** Create World → bias → dials → Propose/Accept scaffold → Open lands without intents phase / without Accept≥1. Enter Craft still empty. Auto-gen still runs. MCP alone ≠ Success. Not KEEP without F5 + Gate B. |
| Out | Expand s0 · restore Accept≥1 gate · KEEP without F5 · forward MAP arm · Generate button re-add · unpark WORLD-import |

## 4. Refuse (`do_not_waive`)

`hotkey_as_product_ux` · `config_meta_without_effect` · `stub_as_hours` · `map_job_name_only` · `explicit_met_implicit_miss` · `intent_collapsed_to_mechanics` · `accept_gate_as_packaging_success` · `campaign_table_prep_as_world_seeds` · `expand_s0_as_debt_close` · `proxy_substitution` · `verify_mcp_only` · `gen_tone_biomes_pack_not_this_debt`

## 5. LIVE (this pass — packaging seam)

- `WorldSession0IntentBoard.CanOpenWorld` always true; packaging slice constants
- `WorldgenGui` Accept scaffold → Open with `Empty` intents (skip Intents phase)
- Package schema retains Intents field unread until GEN — do not invent seed graph

## Deferred feedstock (operator 2026-10-15 — discuss → park)

Same park note as optional-lore Prefer / MAP § Deferred: `CAMP-roster-attach` · `RULE-pc-legality` — friends/sheets/legality after `PACK-save-load`; outside mini-game done-gate. **Do not implement now.** UI honesty note only (fake Player freeform wrong; DM lore OK) — not welded here.

## Related

- Optional lore [[alpha0_world_s0_optional_lore_r1]] · Prior superseded [[alpha0_world_s0_intents_r1]] · Sibling [[alpha0_world_propose_feed_r1]] · [[alpha0_world_bounds_dials_r1]] · [[alpha0_gen_terrain_product_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]
