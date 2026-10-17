---
slice_id: alpha0_stalberg_dual_coast_stage6_emit_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2aa
created: 2026-10-15
updated: 2026-10-15
greenlit_at: '2026-10-15T19:51:59Z'
composed_at: '2026-10-15T19:51:59Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_coast_strip_water_r1
supersedes_meshfit_coast_from: alpha0_stalberg_dual_coast_strip_water_r1
keeps_strip_water_law_from: alpha0_stalberg_dual_coast_strip_water_r1
keeps_bit_map_from: alpha0_stalberg_dual_place_coast_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat_from: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame_from: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_tri_cell_place_from: alpha0_stalberg_dual_tri_cell_place_r1
keeps_single_deck_emit_from: alpha0_stalberg_dual_single_deck_emit_r1
keeps_update_four_from: alpha0_stalberg_dual_update_four_recompute_r1
depends_on: alpha0_stalberg_dual_coast_strip_water_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_coast_stage6_emit_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_place_coast_stage6_emit
contract: C_dual_coast_stage6_emit
materials_keep: dual_offset_terrain_tile_sixpack
ticket_map: PLACE-coast-stage6-emit
selection_rationale: after_2z_KEEP_coast_still_meshfit_glb_dependent__stage6_land_emit_closes_brush_gap
---

# Slice brief — `alpha0_stalberg_dual_coast_stage6_emit_r1`

**GREENLIGHT WELD LIVE** `2026-10-15T19:51:59Z` — Prefer concept + **PLACE-coast-stage6-emit**. Prior **2z** [[alpha0_stalberg_dual_coast_strip_water_r1]] **KEEP / ask_success** (strip-water law KEEP; MeshFit coast path **SUPERSEDED**). Prior **2y** bits KEEP · **2x** / **2w** / **2u** KEEP. Empty ClearDualSlot amber KEEP. Full `EmitFullSingleDeckFromStage6` KEEP. `claim_class: staging` until operator F5 on **this** ticket only. No Y-bias · no Townscaper Done · no WORLD-* · no Terrain3D · no blue-water-as-success.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Map ticket: `PLACE-coast-stage6-emit` in [[World-Builder-Mini-Game-Ticket-Map]]. Prior KEEP strip: [[alpha0_stalberg_dual_coast_strip_water_r1]]. Prior KEEP bits: [[alpha0_stalberg_dual_place_coast_r1]].

## Selection rationale

After PLACE-coast readability (2y SUPERSEDED + **2z strip-water KEEP**), §0 brush still had a weldable craft gap: Edge/Corner/Diagonal/InverseCorner silhouettes still depended on MeshFit of GLB authorship (strip only filtered Terrain_Water). Grok secondary / operator selection: **land-only Stage-6 coast emit** so coasts read without GLB-strip dependency. VIS-read materials already KEEP — not the gap. Do **not** invent WORLD-* Session 0 product yet.

## Why (binding — after 2z KEEP)

| Gate | Prior | Gap |
|------|-------|-----|
| Bit map / UpdateFour | 2y MapOccupancyBitsToCoastFamily | **KEEP** |
| Strip water law | 2z IsTerrainWaterMaterial | **KEEP** (land-only albedo) |
| Empty ocean | ClearDualSlot amber | **KEEP** |
| Full owned | EmitFullSingleDeckFromStage6 | **KEEP** |
| Coast MeshFit GLB | 2z strip then MeshFit | **SUPERSEDE** — Stage-6 land emit |
| PLACE-coast-stage6-emit | — | **this ticket** |

## Coast Stage-6 land-emit contract (binding)

| Rule | Detail |
|------|--------|
| Place KEEP | LMB → one Full on OwnedDualCell(V) via single-deck emit |
| Bits KEEP | Owner off → `MapOccupancyBitsToCoastFamily` → Empty/Edge/Corner/Diagonal/InverseCorner/Full |
| Empty KEEP | bits=0 → ClearDualSlot (amber primary) |
| Coast emit | Non-Full non-Empty → `EmitCoastLandOnlyFromStage6` from OccupancyCorners bits (ON corners + mixed-edge midpoints → fan) |
| Material | Land albedo from library (skip Terrain_Water) — strip-water law KEEP |
| Full refuse | No MeshFit Full GLB |
| Refuse | `glb_meshfit_coast_as_success` · `blue_water_as_coast_success` · `y_bias_as_zfight_fix` · Townscaper Done · WORLD-* · Terrain3D |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_coast_stage6_emit_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | Land-only Stage-6 coast emit for Edge/Corner/Diagonal/InverseCorner; bits KEEP |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_coast_stage6_emit` |
| Map ticket | `PLACE-coast-stage6-emit` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Coast DualCells show land silhouette from Stage-6 occupancy outline (no MeshFit GLB) | `glb_meshfit_coast_as_success` |
| No continuous Terrain_Water blue blob | `blue_water_as_coast_success` |
| Empty DualCells stay clear → amber primary | MeshFit Empty ocean carpet |
| Owned Full = single-deck Stage-6 emit | MeshFit Full GLB / multi-layer |
| Bits → family + UpdateFour KEEP | Y-bias; Townscaper Done; WORLD-* |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** flip V → owned Full KEEP; sampling DualCells refresh; coast DualCells show land Stage-6 silhouettes (Edge/Corner/…) without MeshFit GLB / without continuous Terrain_Water blue; Empty clear-to-amber KEEP; bits sampled KEEP; Prefer refuses `glb_meshfit_coast_as_success` / `blue_water_as_coast_success` / `y_bias_as_zfight_fix` / MeshFit Full; snap/seat/dual+/Stage-6/terrain/squarify/rings=5 KEEP. MCP alone ≠ Success. |
| Out | Townscaper product Done · Terrain3D · WORLD-* · Y-bias · MCP-only |

## 4. Refuse (`do_not_waive`)

`glb_meshfit_coast_as_success` · `blue_water_as_coast_success` · `y_bias_as_zfight_fix` · `seizure_coplanar_deck_as_success` · `full_glb_meshfit` · `owned_only_empty_coast_as_success` · `update_four_cross_as_success` · `silent_ghost_without_place_n3` · `soft_take_4` · `valence_5_editable` · `sector_pie_as_dual_cell_tile` · `verify_mcp_only` · `terrain3d_in_scope`

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_coast_strip_water_r1]] | **KEEP / ask_success**; MeshFit coast path **SUPERSEDED**; strip-water land-only law KEEP |
| [[alpha0_stalberg_dual_place_coast_r1]] | **Bit map KEEP** |
| [[alpha0_stalberg_dual_update_four_recompute_r1]] | Update-four KEEP / ask_success |
| [[alpha0_stalberg_dual_single_deck_emit_r1]] | Single-deck Full KEEP / ask_success |
| [[alpha0_stalberg_dual_tri_cell_place_r1]] | Tri place KEEP / ask_success |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. LIVE weld (implementer)

- `EmitCoastLandOnlyFromStage6`: occupancy bits → land outline (ON corners + mixed midpoints) → fan at FullDeckYLift; land albedo skips Terrain_Water.
- Non-Full coast path: **no** `MeshFitToDualEdgeFrame`.
- Full still `EmitFullSingleDeckFromStage6` only; Empty still ClearDualSlot.
- Metas: `coast_stage6_land_emit=true`; `glb_meshfit_coast_as_success=false`; WeldSliceId → `alpha0_stalberg_dual_coast_stage6_emit_r1`.
- Prefer concept; arm `factory-project.yaml`; GREENLIGHT WELD LIVE; Trinity `project/genesis-mythos-master`.
- Receipt: `claim_class: staging` until operator F5 on **2aa only**.
- Curator skip if mass `.cursor/rules` dirt / `git.push_enabled: false`.

## 7. Operator F5 bar

Layer 0 owns the long F5 tutorial. Compact: WorldgenCraft → coasts = Stage-6 land silhouettes (Edge/Corner readable) without blue blob / without MeshFit GLB dependency; Empty = amber; Full = single deck.

## Related

- Prior KEEP strip [[alpha0_stalberg_dual_coast_strip_water_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]
