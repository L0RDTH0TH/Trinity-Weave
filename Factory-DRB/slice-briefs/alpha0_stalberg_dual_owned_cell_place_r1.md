---
slice_id: alpha0_stalberg_dual_owned_cell_place_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2r
created: 2026-10-04
updated: 2026-10-04
greenlit_at: '2026-10-04T23:17:21Z'
composed_at: '2026-10-04T23:17:21Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: greenlit_weld_live_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
depends_on: alpha0_stalberg_dual_primary_vertex_place_r1
supersedes_paint_polarity:
  - alpha0_stalberg_dual_primary_vertex_place_r1
keeps_snap_polarity:
  - alpha0_stalberg_dual_primary_vertex_place_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_owned_cell_place_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_place
contract: C_owned_dual_cell_place_polarity
materials_keep: dual_offset_terrain_tile_sixpack
operator_diagnosis: ghost_snap_owned_ok__paint_wrong_dualcells__occupancy_excludes_owner__UpdateFour_expand_only
---

# Slice brief — `alpha0_stalberg_dual_owned_cell_place_r1`

**GREENLIGHT WELD LIVE** `2026-10-04T23:17:21Z` — Prefer concept + owned DualCell place polarity. Snap KEEP from [[alpha0_stalberg_dual_primary_vertex_place_r1]]; paint polarity SUPERSEDE. `claim_class: staging` until operator F5. Valence-5 stays non-placeable.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Materials KEEP: [[alpha0_stalberg_dual_terrain_tile_r1]]. Geometry KEEP: [[alpha0_stalberg_dual_stage6_cell_r1]]. Prior snap KEEP: [[alpha0_stalberg_dual_primary_vertex_place_r1]].

## Why (operator-confirmed 2026-10-04)

Ghost/snap to primary V is correct. Placement populates **wrong DualCells** (neighbor micro-quads / face wedges). NOT SmallCornerQuad MeshLibrary — `EnsureSmallCornerQuadMesh` is no-op.

Two linked LIVE bugs:

1. **Occupancy polarity:** Flip sets `_cornerLogic[V]`. DualCell(W) resolved family from `CornerLogicIndices` = `CardinalNeighbors(W)` only — **never included owner W**. Flipping V never changed DualCell(V)’s bitmask; it only lit DualCells owned by **neighbors of V**.
2. **UpdateFour refresh set:** On `PrimaryPickY`, `UpdateFourDualSlots` walked **`DualCellsExpandingFrom(V)`** (expand only; owned excluded). Comments/API said owned+expand via `DualCellsTouching`. Ghost uses `TryGetOwned` / OwnedDualCell(V) — ghost≠paint.

## Occupancy ordering (documented)

`CornerLogicIndices` for DualCell(V), CCW dual-edge frame aligned with Stage6CornersLocal:

| Index | Sample |
|------:|--------|
| 0 | **OwnerVertexId (V)** — only-V-on → Corner `0b0001`, rot0 |
| 1 | CardinalNeighbors[0] |
| 2 | CardinalNeighbors[1] |
| 3 | CardinalNeighbors[2] |

Valence-4: neighbor[3] omitted from this cell’s mask; shared via DualCellsTouching refresh of DualCell(neighbor[3]). Length ≠ 4 when neighbors &lt; 3 — no soft pad. Valence-5 non-editable (SmallCornerQuads 2..4 only).

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_owned_cell_place_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** (place polarity: `owned_dual_cell_place`) |
| Scope | Occupancy includes owner + UpdateFour=DualCellsTouching; snap/Empty/debug KEEP |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `owned_dual_cell_place` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| LMB flip V → MeshLibrary on **OwnedDualCell(V)** / `Stage6CornersLocal(V)` | `expand_only_paint_as_success` · `neighbor_dual_as_owned_place` |
| Occupancy for DualCell(V) **includes V** (Corner when only V on) | occupancy = neighbors-only |
| `UpdateFourDualSlots(PrimaryPickY)` → **`DualCellsTouching(V)`** (owned first + expand); cap ≤ MaxDualCellsPerLogicFlip; hard refuse over | soft `Take(4)` · expand-only refresh |
| Ghost + paint same OwnedDualCell(V) | ghost≠paint |
| `HighlightOwnedDualCells` → DualCell keys (not SmallCornerQuad) | `sector_pie_as_dual_cell_tile` |
| Keep: Empty skip, dual `+` only, primary-V snap, Stage-6, terrain GLBs, squarify, rings=5, valence-5 non-editable | `ocean_fill_all_empty_slots` · secondary face place |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** LMB snaps primary V; places one MeshLibrary module on **OwnedDualCell(V)** (ghost seat = paint seat); only-V-on → Corner on that owned cell; neighbor DualCells may refresh for shared corners; Empty skip; dual `+` at face centres; no dual-edge ribbons; Stage-6 + terrain + squarify + rings=5/spacing=210 KEEP; valence-5 non-placeable; Prefer refuses `expand_only_paint_as_success` / `neighbor_dual_as_owned_place` / `sector_pie_as_dual_cell_tile` / `ocean_fill_all_empty_slots` |
| Out | expand-only paint as Success · neighbor DualCell stamp as owned place · secondary face place · ocean fill · valence-5 editable · MCP-only attest |

## 4. Refuse (`do_not_waive`)

`expand_only_paint_as_success` · `neighbor_dual_as_owned_place` · `sector_pie_as_dual_cell_tile` · `secondary_face_snap_as_place` · `secondary_glow_center_as_place_target` · `face_stamp_as_dual_populate` · `ocean_fill_all_empty_slots` · `sector_pie_as_product` · `plinth_as_terrain` · `prop_scatter_as_composition` · `stretch_as_variant` · `gray_ramp_only` · `primary_face_as_dual` · `stamp_as_dual` · `metrics_only_glb_drop` · `proxy_substitution` · `intent_collapsed_to_mechanics` · `verify_mcp_only` · prior dual refuses

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_primary_vertex_place_r1]] | **Snap KEEP**; Empty skip / dual `+` KEEP; **paint polarity SUPERSEDED** |
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack GLBs/materials KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 DualCell geometry KEEP |
| [[alpha0_stalberg_dual_cell_lookup_yaw_r1]] | Lookup/yaw/edge-frame KEEP |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 squarify KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Cursor near orange star → snap primary V (KEEP); ghost outlines **OwnedDualCell(V)**.
3. LMB → MeshLibrary module lands on **same OwnedDualCell(V)** as ghost (not neighbor DualCells / wedges).
4. Only-V-on → Corner (or expected single-bit family) on that owned cell.
5. Free DualCells show amber grid — no ocean Empty carpet; dual `+` at face centres; no dual-edge ribbons.
6. Valence-5 verts remain non-editable. Seed showcase silhouettes are demo-only — place proof is owned DualCell.
7. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Prior [[alpha0_stalberg_dual_primary_vertex_place_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]
