---
slice_id: alpha0_stalberg_dual_coast_strip_water_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2z
created: 2026-10-15
updated: 2026-10-15
greenlit_at: '2026-10-15T19:28:20Z'
composed_at: '2026-10-15T19:28:20Z'
claim_class: ask_success
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: ask_success_keep
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_place_coast_r1
supersedes_meshfit_water_from: alpha0_stalberg_dual_place_coast_r1
keeps_bit_map_from: alpha0_stalberg_dual_place_coast_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat_from: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame_from: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_tri_cell_place_from: alpha0_stalberg_dual_tri_cell_place_r1
keeps_single_deck_emit_from: alpha0_stalberg_dual_single_deck_emit_r1
keeps_update_four_from: alpha0_stalberg_dual_update_four_recompute_r1
depends_on: alpha0_stalberg_dual_place_coast_r1
keeps_place_coast_bits:
  - alpha0_stalberg_dual_place_coast_r1
keeps_update_four:
  - alpha0_stalberg_dual_update_four_recompute_r1
keeps_single_deck_emit:
  - alpha0_stalberg_dual_single_deck_emit_r1
keeps_tri_cell_place:
  - alpha0_stalberg_dual_tri_cell_place_r1
keeps_coverage_orient:
  - alpha0_stalberg_dual_whole_cell_orient_r1
keeps_seat_polarity:
  - alpha0_stalberg_dual_owned_cell_place_r1
keeps_snap_polarity:
  - alpha0_stalberg_dual_primary_vertex_place_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_coast_strip_water_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_place_coast_strip_water
contract: C_dual_coast_strip_water
materials_keep: dual_offset_terrain_tile_sixpack
ticket_map: PLACE-coast-strip-water
operator_f5_confirmed: true
operator_f5_at: '2026-10-15T19:49:00Z'
disposition: KEEP
operator_diagnosis: 2y_f5_fail__meshfit_includes_terrain_water_blue_blob__bit_map_keep__2z_accepted_fine
---

# Slice brief — `alpha0_stalberg_dual_coast_strip_water_r1`

**KEEP / ask_success** — operator accepted (“Fine”). Prefer concept + **PLACE-coast-strip-water** landed. Prior **2y** MeshFit water **SUPERSEDED** (bit map KEEP). Prior **2x** / **2w** / **2u** KEEP. Empty ClearDualSlot KEEP. Full single-deck KEEP. MeshFit strip Terrain_Water KEEP as prior; next Prefer **2aa** Stage-6 land-only coast emit supersedes MeshFit coast dependency. No Y-bias · no Townscaper Done · no WORLD-*.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Map ticket: `PLACE-coast-strip-water` in [[World-Builder-Mini-Game-Ticket-Map]]. Prior KEEP bits: [[alpha0_stalberg_dual_place_coast_r1]]. Prior KEEP emit: [[alpha0_stalberg_dual_single_deck_emit_r1]].

## Selection rationale

Operator + Grok + Layer 0 diagnosis accepted: **2y** bit→family works; Empty clear-to-amber innocent. Failure = MeshFit of Edge/Corner/Diagonal/InverseCorner GLBs includes full/near-full **Terrain_Water** → continuous blue blob; Moss/Earth/Stone ride same path → green stacks on blue. Do not paper over inside 2y — new slice **2z**.

## Why (binding — after 2y F5 FAIL)

| Gate | Prior | Gap |
|------|-------|-----|
| Bit map / UpdateFour | 2y MapOccupancyBitsToCoastFamily | **KEEP** |
| Empty ocean | ClearDualSlot amber | **KEEP** |
| Full owned | EmitFullSingleDeckFromStage6 | **KEEP** |
| Coast MeshFit water | Terrain_Water surfaces included | **SUPERSEDE** — strip at MeshFit |
| PLACE-coast-strip-water | — | **this ticket** |

## Coast strip-water contract (binding)

| Rule | Detail |
|------|--------|
| Place KEEP | LMB → one Full on OwnedDualCell(V) via single-deck emit |
| Bits KEEP | Owner off → `MapOccupancyBitsToCoastFamily` → Empty/Edge/Corner/Diagonal/InverseCorner/Full |
| Empty KEEP | bits=0 → ClearDualSlot (amber primary; no Empty GLB MeshFit) |
| MeshFit strip | Edge/Corner/Diagonal/InverseCorner → skip surfaces whose material is Terrain_Water (name or water albedo); keep Moss/Earth/Stone/Sand |
| Full refuse | No MeshFit Full GLB / multi-layer on owned Full |
| Refuse | `blue_water_as_coast_success` · `y_bias_as_zfight_fix` · Townscaper Done · WORLD-* · Terrain3D · GLB reauth as blocker |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_coast_strip_water_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | MeshFit strip Terrain_Water on non-Empty coast families; bit map KEEP |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_coast_strip_water` |
| Map ticket | `PLACE-coast-strip-water` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Coast DualCells show land silhouette (Moss/Earth/Stone/Sand) without continuous blue water blob | `blue_water_as_coast_success` |
| Empty DualCells stay clear → amber primary | MeshFit Empty ocean carpet |
| Owned Full = single-deck Stage-6 emit | MeshFit Full GLB / multi-layer |
| Bits → family + UpdateFour KEEP | paper-over inside 2y; Y-bias; Townscaper Done |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** flip V → owned Full KEEP; sampling DualCells refresh; coast DualCells (Edge/Corner/…) show land materials without continuous Terrain_Water blue blob; Empty clear-to-amber KEEP; bits sampled KEEP; Prefer refuses `blue_water_as_coast_success` / `y_bias_as_zfight_fix` / MeshFit Full; snap/seat/dual+/Stage-6/terrain/squarify/rings=5 KEEP. MCP alone ≠ Success. |
| Out | Townscaper product Done · Terrain3D · WORLD-* · Y-bias · GLB reauth as blocker · MCP-only |

## 4. Refuse (`do_not_waive`)

`blue_water_as_coast_success` · `y_bias_as_zfight_fix` · `seizure_coplanar_deck_as_success` · `full_glb_meshfit` · `owned_only_empty_coast_as_success` · `update_four_cross_as_success` · `silent_ghost_without_place_n3` · `soft_take_4` · `valence_5_editable` · `verify_mcp_only` · `terrain3d_in_scope`

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_place_coast_r1]] | **Bit map KEEP**; MeshFit water **SUPERSEDED** (2y F5 FAIL) |
| [[alpha0_stalberg_dual_update_four_recompute_r1]] | Update-four KEEP / ask_success |
| [[alpha0_stalberg_dual_single_deck_emit_r1]] | Single-deck Full KEEP / ask_success |
| [[alpha0_stalberg_dual_tri_cell_place_r1]] | Tri place KEEP / ask_success |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. LIVE weld (implementer)

- `MeshFitToDualEdgeFrame`: skip surface when `IsTerrainWaterMaterial` (name contains Terrain_Water or blue water albedo).
- Empty still ClearDualSlot entirely (never MeshFit).
- Full still `EmitFullSingleDeckFromStage6` only.
- Metas: `coast_strip_terrain_water=true` on non-Full; WeldSliceId → `alpha0_stalberg_dual_coast_strip_water_r1`.
- Prefer concept; arm `factory-project.yaml`; GREENLIGHT WELD LIVE; Trinity `project/genesis-mythos-master`.
- Receipt: `claim_class: staging` until operator F5 on **2z only**.
- Curator skip if mass `.cursor/rules` dirt / `git.push_enabled: false`.

## 7. Operator F5 bar

Layer 0 owns the long F5 tutorial. Compact: WorldgenCraft → coasts = land without blue blob; Empty = amber; Full = single deck; no green-on-blue stacks.

## Related

- Prior SUPERSEDED MeshFit water [[alpha0_stalberg_dual_place_coast_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]
