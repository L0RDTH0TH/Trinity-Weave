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
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5
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
operator_f5_confirmed: false
disposition: staging
selection_rationale: map_section_1_after_WORLD-propose_next_is_WORLD-s0-intents
ui_layout_deferred_to_sibling: true
---

# Slice brief — `alpha0_world_s0_intents_r1`

**GREENLIGHT WELD LIVE** — Prefer concept + **WORLD-s0-intents**. Prior **1c** [[alpha0_world_propose_r1]] **KEEP/ask_success** (operator F5). Brush §0 closed. Owned Full = flat single-deck green KEEP. `claim_class: staging` until operator F5 on **this** ticket only. No Townscaper Done · no GEN-* · no Terrain3D.

**Choice:** After WORLD-propose, map §1 next = **`WORLD-s0-intents`** (collaborative Session 0 intents `proposed → accepted`; Microscope-informed; not DM-wizard-only). Series step **1d**.

**UI layout:** WorldgenGui anchors/ScrollContainer/widescreen clipping deferred to sibling agent — this weld is product Prefer on Play path only.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `WORLD-s0-intents` in [[World-Builder-Mini-Game-Ticket-Map]]. Feedstock: [[dual-grid-nested-placetile-world-authorship]].

## Why (binding)

| Gate | Detail |
|------|--------|
| WORLD-s0-intents | Player/DM/shared seeds enter proposed→accepted; Open world requires ≥1 accepted |
| Play path | LaunchShell Create World → bias → dials → scaffold → **Session 0 intents** → Open world → craft |
| Package | world_id + gen_bias + dials + scaffold + accepted intents + empty campaigns |
| Brush KEEP | Full single-deck; DualGridCraftHost unchanged |
| Out of scope | GEN-* fill · WORLD-import · PACK-save · Terrain3D · Townscaper Done · layout chrome |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_world_s0_intents` |
| `slice_id` | `alpha0_world_s0_intents_r1` |
| `success_object` | **`session0_intent_proposed_accepted_board`** |
| Scope | After scaffold accept → collaborative intent board → ≥1 accepted → open package |
| `claim_class` | `staging` until operator F5 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Map ticket | `WORLD-s0-intents` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Visible Session 0 intents phase on Create World path | Docs-only / orphan UI off LaunchShell |
| Propose seed + Accept/Reject intent + Open world (≥1) | Open world with zero accepted intents |
| Player/DM/shared seats on seed bank (not wizard-only) | DM-only wizard sold as collaborative Success |
| Accepted intents bind onto WorldPackage | GEN-fill / Townscaper Done as Success |
| LaunchShell remains main_scene | main_scene WorldgenCraft regress |
| Owned Full stays single-deck flat green | MeshFit Full GLB |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** LaunchShell → Create World → bias → dials → Propose scaffold → Accept scaffold → Session 0 intents visible → Accept ≥1 intent (Reject or Propose seed once) → Open world → craft; HUD shows scaffold + s0 count + dials + world_id; campaigns empty; Full single-deck KEEP. MCP alone ≠ Success. |
| Out | GEN-terrain Done · WORLD-import · PACK-save · Terrain3D · Townscaper product Done |

## 4. Refuse (`do_not_waive`)

`open_world_without_accepted_intent` · `dm_wizard_only_as_s0` · `gen_fill_as_s0_intents` · `orphan_intents_off_play_path` · `oneshot_propose_as_success` · `campaign_tone_hardlock` · `full_glb_meshfit` · `y_bias_as_zfight_fix` · `verify_mcp_only` · `terrain3d_in_scope` · `townscaper_product_done`

## 5. LIVE weld (implementer)

- `Core/WorldGen/WorldSession0Intent.cs` · `WorldSession0IntentBoard.cs` — proposed→accepted board + seed bank
- `Core/WorldGen/WorldPackage.cs` · `WorldPackageSession.cs` — schema v4 · intent metas
- `UI/WorldgenGui.cs` — Intents phase after Accept scaffold (**no** `.tscn` layout/anchor/ScrollContainer edits)
- `LaunchShell.cs` — Bind intents; HUD s0 count
- DualGridCraftHost **unchanged** (brush KEEP)

## 6. Operator F5 bar

Layer 0 owns the long tutorial. Compact: Create World → … → Accept scaffold → Accept ≥1 intent → Open world → craft with package+intents; Full still flat green.

## Related

- Prior KEEP [[alpha0_world_propose_r1]] · [[alpha0_world_bounds_r1]] · [[alpha0_world_new_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]]
