---
slice_id: alpha0_world_s0_intents_r1
ask_id: alpha0_world_s0_intents
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1d
created: 2026-10-15
updated: 2026-10-15
greenlit_at: '2026-10-15T21:06:00Z'
composed_at: '2026-10-15T21:06:00Z'
closed_at: '2026-10-15T21:42:18Z'
claim_class: keep
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: keep_ask_success
template: Half-B-Weld-Brief-Template
prior_keep_slice: alpha0_world_propose_r1
prior_keep_step: 1c
keeps_world_new: alpha0_world_new_r1
keeps_world_bounds: alpha0_world_bounds_r1
keeps_world_propose: alpha0_world_propose_r1
keeps_brush_tri: alpha0_stalberg_dual_tri_cell_place_r1
keeps_brush_single_deck: alpha0_stalberg_dual_single_deck_emit_r1
keeps_brush_update_four: alpha0_stalberg_dual_update_four_recompute_r1
keeps_brush_coast_bits: alpha0_stalberg_dual_place_coast_r1
keeps_brush_strip_water: alpha0_stalberg_dual_coast_strip_water_r1
keeps_brush_coast_stage6_landed: alpha0_stalberg_dual_coast_stage6_emit_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_world_s0_intents_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map: WORLD-s0-intents
success_object: session0_intent_proposed_accepted_board
contract: C_world_s0_intents_collaborative
operator_f5_confirmed: true
disposition: KEEP_ask_success
soft_success: true
soft_success_class: framing_examples_altitude_debt
selection_rationale: map_section_1_after_WORLD-propose_next_is_WORLD-s0-intents
ui_layout_deferred_to_sibling: true
next_slice: alpha0_world_import_r1
next_slice_armed: true
---

# Slice brief — `alpha0_world_s0_intents_r1`

**KEEP / ask_success (soft)** — operator F5 soft SUCCESS: flow works; **framing/examples/altitude debt remains**.

Prior **1c** [[alpha0_world_propose_r1]] KEEP. Next = `WORLD-import` (**pointer only; not armed** — sibling owns next Prefer weld).

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `WORLD-s0-intents` in [[World-Builder-Mini-Game-Ticket-Map]].

## Soft-success problem (binding honesty)

| Field | Value |
|-------|--------|
| Intent (correct) | **World seeds** that bias what the world *is* (e.g. "from X wandering tribe", "starting kingdom is France-but-magic") — **not** campaign attach / session prep |
| Packaging confuse | Vague adventure-hook seed examples + "Session 0"/player-DM seat framing + Accept≥1 gate on Create World **felt like campaign/table prep** |
| Campaigns | Still **empty**; `WORLD-empty-campaigns` remains later guest — **do not claim campaign integration** |
| Soft success means | Flow works; framing/examples/altitude debt remains (follow-up: better seed copy and/or make intents optional/off Create World critical path) |

## Closed

| Field | Value |
|-------|--------|
| `done_when` | Operator soft SUCCESS — Create World → bias → dials → scaffold → Session 0 intents → Accept ≥1 → Open world → craft; campaigns empty |
| Disposition | **KEEP / ask_success** (`soft_success: true`) |
| Next | `WORLD-import` (not armed) |

## Related

- Prior KEEP [[alpha0_world_propose_r1]] · [[alpha0_world_bounds_r1]] · [[alpha0_world_new_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]]
