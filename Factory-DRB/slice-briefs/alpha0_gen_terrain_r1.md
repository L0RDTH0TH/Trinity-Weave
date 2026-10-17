---
slice_id: alpha0_gen_terrain_r1
ask_id: alpha0_gen_terrain
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2a
created: 2026-10-15
updated: 2026-10-15
greenlit_at: '2026-10-15T22:16:00Z'
composed_at: '2026-10-15T22:16:00Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_world_slice: alpha0_world_parity_r1
prior_world_step: 1g
prior_world_note: empty_craft_enter_folded_into_1g_KEEP
keeps_world_new: alpha0_world_new_r1
keeps_world_bounds: alpha0_world_bounds_r1
keeps_world_propose: alpha0_world_propose_r1
keeps_world_s0_intents: alpha0_world_s0_intents_r1
keeps_world_import: alpha0_world_import_r1
keeps_world_empty_campaigns: alpha0_world_empty_campaigns_r1
keeps_world_parity: alpha0_world_parity_r1
keeps_brush_tri: alpha0_stalberg_dual_tri_cell_place_r1
keeps_brush_single_deck: alpha0_stalberg_dual_single_deck_emit_r1
keeps_brush_update_four: alpha0_stalberg_dual_update_four_recompute_r1
keeps_brush_coast_bits: alpha0_stalberg_dual_place_coast_r1
keeps_brush_strip_water: alpha0_stalberg_dual_coast_strip_water_r1
keeps_brush_coast_stage6_landed: alpha0_stalberg_dual_coast_stage6_emit_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_gen_terrain_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map: GEN-terrain
success_object: gen_terrain_dualgrid_height_starter
contract: C_gen_terrain_explicit_populate
operator_f5_confirmed: false
disposition: staging
selection_rationale: map_section_2_first_GEN-terrain_after_1g_empty_enter_fold
empty_enter_law: sibling_1g_KEEP_do_not_undo
natural_gen_honesty: height_stub_plus_value_noise_land_water_rivers_full_erosion_stack_later
---

# Slice brief — `alpha0_gen_terrain_r1`

**GREENLIGHT WELD LIVE** — Prefer concept + first **GEN-terrain** populate path. Prior **1g** [[alpha0_world_parity_r1]] folded **empty craft enter** (KEEP that law — do not undo). Series step **2a**. `claim_class: staging` until operator F5 on **this** ticket only.

**Choice:** Map §2 first = **`GEN-terrain`**. Explicit Generate after world/craft open paints dual-grid land/water from dials/bias + height contract stub (+ river corridors). Not silent fill on Enter Craft / Create World open.

**Altitude:** Natural-gen starter (value noise → land/water + height facts). Full gradient/erosion stack / VIS-height / DF-hours loop = later. Not GEN-biomes / GEN-history. Campaigns stay empty. No Townscaper Done.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `GEN-terrain` in [[World-Builder-Mini-Game-Ticket-Map]].

## Why (binding)

| Gate | Detail |
|------|--------|
| GEN-terrain | Land, water, height, rivers — dual-grid facts + natural-gen height contract |
| Explicit invoke | Generate (T) after open — never craft-enter Success |
| Empty enter KEEP | 1g sibling law untouched |
| Honesty | Height stub + land Prefer LIVE; not DF-hours Done; not full natural stack Done |
| Out | GEN-biomes · GEN-history · Townscaper Done · campaign attach · Terrain3D · silent fill |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_gen_terrain` |
| `slice_id` | `alpha0_gen_terrain_r1` |
| `success_object` | **`gen_terrain_dualgrid_height_starter`** |
| Scope | Prefer + GenTerrain service + explicit Play-path Generate |
| `claim_class` | `staging` until operator F5 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Map ticket | `GEN-terrain` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Craft enter stays empty amber (1g KEEP) | Silent GEN / showcase / auto-import on enter |
| Explicit T Generate paints land/water from dials+bias | Docs-only / meta-only Success |
| Height facts recorded (contract stub) | Fake full erosion stack / VIS-height Done |
| River corridors from rivers dial | GEN-biomes/history sold as this Success |
| Campaigns empty KEEP; LaunchShell main | Campaign attach / Townscaper Done |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** Enter Craft / Create World→Open → empty amber board → press **T** → dual-grid land/water populates from dials/bias; height stub logged; campaigns=0; empty-enter still true before T. MCP alone ≠ Success. DF-hours / full natural stack / Townscaper Done = **out**. |
| Out | Silent craft-enter fill · GEN-biomes Done · GEN-history Done · Townscaper Done · Terrain3D · fake DF-hours |

## 4. Refuse (`do_not_waive`)

`gen_fill_as_craft_enter` · `full_natural_gen_stack_as_done` · `df_hours_as_this_slice_done` · `gen_biomes_as_terrain_success` · `gen_history_as_terrain_success` · `townscaper_done_as_gen_success` · `campaign_attach_as_world_create_success` · `verify_mcp_only` · `terrain3d_in_scope` · `undo_empty_enter_1g`

## 5. LIVE weld (implementer)

- `Core/WorldGen/GenTerrainContract.cs` — **new** law
- `Core/WorldGen/GenTerrainService.cs` — **new** compute (noise land/water/height/rivers)
- `Systems/DualGridCraftHost.cs` — `ApplyGenTerrainPass` only (empty-enter arm untouched except clear gen state)
- `Systems/WorldgenCraft.cs` — Key.T explicit Generate
- `Core/WorldGen/WorldPackage.cs` · `WorldPackageSession.cs` — schema v8 · gen metas
- `LaunchShell.cs` · `WorldgenCraftControls.cs` — chrome / hints
- Do **not** thrash empty-enter sibling law

## 6. Operator F5 bar

Layer 0 owns the long tutorial. Compact: empty enter → T Generate → board populates; height stub honest; not DF-hours Done.

## Related

- Prior [[alpha0_world_parity_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]]
