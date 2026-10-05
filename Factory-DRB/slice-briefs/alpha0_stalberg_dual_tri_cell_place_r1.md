---
slice_id: alpha0_stalberg_dual_tri_cell_place_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2u
created: 2026-10-05
updated: 2026-10-05
greenlit_at: '2026-10-05T00:33:00Z'
composed_at: '2026-10-05T00:33:00Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_owned_only_paint_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat_from: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame_from: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_owned_only_paint_from: alpha0_stalberg_dual_owned_only_paint_r1
depends_on: alpha0_stalberg_dual_owned_only_paint_r1
supersedes_n3_place_skip:
  - alpha0_stalberg_dual_owned_only_paint_r1
keeps_owned_only_paint:
  - alpha0_stalberg_dual_owned_only_paint_r1
keeps_coverage_orient:
  - alpha0_stalberg_dual_whole_cell_orient_r1
keeps_seat_polarity:
  - alpha0_stalberg_dual_owned_cell_place_r1
keeps_snap_polarity:
  - alpha0_stalberg_dual_primary_vertex_place_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_tri_cell_place_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_tri_cell_place
contract: C_dual_tri_cell_place
materials_keep: dual_offset_terrain_tile_sixpack
operator_diagnosis: editable_valence3_ghost_ok__EnsureStage6_requires_corners_eq4__silent_noop_place
visuals_deferred: zfight_full_ybias_seizure_decks
---

# Slice brief — `alpha0_stalberg_dual_tri_cell_place_r1`

**GREENLIGHT WELD LIVE** `2026-10-05T00:33:00Z` — Prefer concept + **tri-edge DualCell** spawn/place (n=3 DualCorners). Owned-only KEEP from [[alpha0_stalberg_dual_owned_only_paint_r1]]; **SUPERSEDE** silent n=3 place skip (`EnsureStage6` / `OccupancyCorners` ==4-only). Ghost already ≥3 — keep. **OUT OF SCOPE:** Z-fight / FullYBias / seizure decks — explicit defer; do not block on visuals. `claim_class: staging` until operator F5. Valence-5 stays non-placeable.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Materials KEEP: [[alpha0_stalberg_dual_terrain_tile_r1]]. Geometry KEEP: [[alpha0_stalberg_dual_stage6_cell_r1]]. Owned-only KEEP: [[alpha0_stalberg_dual_owned_only_paint_r1]]. Coverage+frame KEEP: [[alpha0_stalberg_dual_whole_cell_orient_r1]]. Seat KEEP: [[alpha0_stalberg_dual_owned_cell_place_r1]]. Snap KEEP: [[alpha0_stalberg_dual_primary_vertex_place_r1]].

## Why (binding diagnosis)

Primary mesh is all-quad. Cursor triangle = Stage-6 **DualCell with DualCorners.Length==3** (owner V with 3 incident faces).

| Gate | Today | Result |
|------|-------|--------|
| Editable / snap | SmallCornerQuads **2..4** | valence-3 **allowed** |
| Ghost | Stage6CornersLocal length **≥ 3** | **shows** |
| Place | `EnsureStage6DualCellMesh` corners **== 4** + `OccupancyCorners` **== 4** | **silent no-op** |

Not valence-5 (stays non-editable). Not false 5-family highlight. Operator prefer: **adapt spawn/place to n=3** (over “don’t ghost”).

## Tri OccupancyCorners bit map (binding)

| Bit | Sample | Geometry |
|-----|--------|----------|
| bit0 | CardinalNeighbors[0] | DualCorners[0] (face centroid of CornerFaces[0]) |
| bit1 | CardinalNeighbors[1] | DualCorners[1] |
| bit2 | CardinalNeighbors[2] | DualCorners[2] |

- Length **3** — **no** soft-pad to fake 4 (`soft_take_4` refuse).
- Owner V is placement centre — **not** a corner bit.
- Resolve: owner-on → **Full** whole triangular DualCell; owner-off → Empty (owned-only KEEP).
- Quad n=4 path KEEP (bits 0..3; dual-edge frame edge0=c0→c1).

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_tri_cell_place_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | n=3 DualCorners Full owned-only place; MeshFit triangle warp; OccupancyCorners length-3 |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_tri_cell_place` |
| Visuals | **DEFERRED** — Z-fight / FullYBias / seizure decks out of scope |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| LMB editable V with OwnedDualCell DualCorners==3 → **one Full** on that DualCell | `silent_ghost_without_place_n3` |
| Ghost and paint agree (same OwnedDualCell) | ghost-without-place · paint-elsewhere |
| MeshFit / Full warp for triangle Stage6CornersLocal (barycentric or equiv) | `corners_eq4_only_meshfit` |
| OccupancyCorners n=3 path; owner-on → Full; **no** soft-pad to 4 | `soft_take_4` |
| Owned-only KEEP (no neighbor Corner spray) | `neighbor_corner_spray_as_place` |
| Primary-V snap, Empty skip, dual `+`, Stage-6, dual-edge frame for quads, valence-5 out, terrain/squarify/rings=5 | `valence_5_editable` · `sector_pie_as_dual_cell_tile` |
| Do **not** block / claim Z-fight Success | `seizure_coplanar_deck_as_success` as this slice’s Success |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** LMB on editable V whose OwnedDualCell has **3 DualCorners** → place **one Full** (owned-only) on that triangular DualCell; ghost and paint agree; MeshFit covers the triangle; Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP; valence-5 non-placeable; Prefer refuses `silent_ghost_without_place_n3` / `soft_take_4` / `valence_5_editable` / `neighbor_corner_spray_as_place` / `sector_pie_as_dual_cell_tile`. **No Z-fight / seizure claim** this slice. |
| Out | Z-fight / FullYBias / seizure decks · MCP-only attest · coastline Corner · soft_take_4 · valence-5 editable |

## 4. Refuse (`do_not_waive`)

`silent_ghost_without_place_n3` · `soft_take_4` · `valence_5_editable` · `neighbor_corner_spray_as_place` · `sector_pie_as_dual_cell_tile` · `corners_eq4_only_meshfit` · `update_four_cross_as_success` · `world_yaw_as_dual_edge_frame` · `ocean_fill_all_empty_slots` · `secondary_face_snap_as_place` · `verify_mcp_only` · prior dual refuses

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_owned_only_paint_r1]] | **Owned-only paint KEEP**; **n=3 place skip SUPERSEDED** |
| [[alpha0_stalberg_dual_whole_cell_orient_r1]] | Coverage+frame KEEP for quads; OccupancyCorners↔Stage6; dual-edge frame |
| [[alpha0_stalberg_dual_owned_cell_place_r1]] | Seat KEEP (ghost=paint OwnedDualCell) |
| [[alpha0_stalberg_dual_primary_vertex_place_r1]] | Snap KEEP; Empty skip / dual `+` KEEP |
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack GLBs/materials KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 DualCell geometry KEEP (n≥3 wire) |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 squarify KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. LIVE weld (implementer)

- `DualGridCraftHost.EnsureStage6DualCellMesh` / Place / MeshFit: support `DualCorners.Length==3` Full owned-only (barycentric or equiv; not require ==4 only).
- `OrganicDualOffsetLattice.OccupancyCorners` (or parallel): n=3 path — length 3 bit map; no soft_take_4 pad.
- Ghost already ≥3 — keep; Flip path must place (not silent no-op).
- Prefer concept; arm `factory-project.yaml`; GREENLIGHT WELD LIVE; Trinity `project/genesis-mythos-master`.
- Receipt: visuals (Z-fight / FullYBias / seizure) **deferred**.
- Curator skip if mass `.cursor/rules` deletes.

## 7. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Cursor near orange star → snap primary V (KEEP); find editable V whose OwnedDualCell is a **triangle** (3 DualCorners) — ghost outlines that DualCell.
3. LMB → **one Full** MeshLibrary lands on that triangular OwnedDualCell — ghost and paint agree.
4. Neighbor DualCells stay Empty mesh unless their own owner is on (owned-only KEEP).
5. Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP.
6. Valence-5 verts remain non-editable.
7. **Do not** attest Z-fight / seizure Success this slice (deferred).
8. Attest ask_success only when tri place bar met — MCP alone ≠ Success.

## Related

- Prior owned-only [[alpha0_stalberg_dual_owned_only_paint_r1]] · Coverage+frame [[alpha0_stalberg_dual_whole_cell_orient_r1]] · Seat [[alpha0_stalberg_dual_owned_cell_place_r1]] · Snap [[alpha0_stalberg_dual_primary_vertex_place_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]
