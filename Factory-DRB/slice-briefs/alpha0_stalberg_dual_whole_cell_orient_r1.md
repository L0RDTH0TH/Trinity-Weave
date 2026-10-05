---
slice_id: alpha0_stalberg_dual_whole_cell_orient_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2s
created: 2026-10-04
updated: 2026-10-04
greenlit_at: '2026-10-04T23:36:26Z'
composed_at: '2026-10-04T23:36:26Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: greenlit_weld_live_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_owned_cell_place_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat_from: alpha0_stalberg_dual_owned_cell_place_r1
depends_on: alpha0_stalberg_dual_owned_cell_place_r1
supersedes_coverage_orient:
  - alpha0_stalberg_dual_owned_cell_place_r1
supersedes_incomplete_yaw:
  - alpha0_stalberg_dual_cell_lookup_yaw_r1
keeps_seat_polarity:
  - alpha0_stalberg_dual_owned_cell_place_r1
keeps_snap_polarity:
  - alpha0_stalberg_dual_primary_vertex_place_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_whole_cell_orient_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_whole_cell_edge_frame
contract: C_dual_whole_cell_edge_frame
materials_keep: dual_offset_terrain_tile_sixpack
operator_diagnosis: seat_ok_one_pie_only__occupancy_primary_ring_neq_stage6__meta_yaw_lie__aabb_world_stretch
---

# Slice brief — `alpha0_stalberg_dual_whole_cell_orient_r1`

**GREENLIGHT WELD LIVE** `2026-10-04T23:36:26Z` — Prefer concept + whole DualCell coverage + dual-edge-frame orient. Seat KEEP from [[alpha0_stalberg_dual_owned_cell_place_r1]]; coverage+orient SUPERSEDE. Also supersedes incomplete yaw claim of [[alpha0_stalberg_dual_cell_lookup_yaw_r1]]. `claim_class: staging` until operator F5. Valence-5 stays non-placeable.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Materials KEEP: [[alpha0_stalberg_dual_terrain_tile_r1]]. Geometry KEEP: [[alpha0_stalberg_dual_stage6_cell_r1]]. Seat KEEP: [[alpha0_stalberg_dual_owned_cell_place_r1]]. Snap KEEP: [[alpha0_stalberg_dual_primary_vertex_place_r1]].

## Why (operator F5 2026-10-04)

Prior `alpha0_stalberg_dual_owned_cell_place_r1` fixed seat polarity partly. Location correct for **one** of four secondary quads; orientation still wrong (props world-XZ; DualCell plate skewed).

Code review match:

1. **Coverage:** only-V-on → Corner `0b0001` rot0 → MeshLibrary mass at geometry c0 only = one of four pies of DualCell(V). Prefer: flip V ⇒ DualCell(V) **Full** (whole-cell land = union of SmallCornerQuads around V).
2. **Frame mismatch:** Occupancy ring `[Owner V, n0,n1,n2]` (primary verts) ≠ warp ring `Stage6CornersLocal` (face centroids). Meta claimed `dual_edge_frame_yaw` but `mi.Rotation=0` and fit was AABB(X,Z)→quad bilinear without Stage6-aligned OccupancyCorners — world-authored stretch narrative, not dual-edge frame Success.
3. **Refuse:** `sector_pie_as_dual_cell_tile` as MeshLibrary host; `world_yaw_as_dual_edge_frame` / AABB-world props as Success.

## OccupancyCorners bit→corner map (binding)

`OccupancyCorners` for DualCell(V), CCW dual-edge frame = `Stage6CornersLocal` / `DualCorners`:

| Bit | Stage6 corner | Sample | Edge |
|----:|---------------|--------|------|
| 0 | DualCorners[0] (face centroid CornerFaces[0]) | CardinalNeighbors[0] | edge0 = c0→c1 |
| 1 | DualCorners[1] | CardinalNeighbors[1] | c1→c2 |
| 2 | DualCorners[2] | CardinalNeighbors[2] | c2→c3 |
| 3 | DualCorners[3] | CardinalNeighbors[3] | c3→c0 |

Owner V = placement centre (grammar) — **not** a corner bit. Host: owner-on → **Full** on OwnedDualCell(V). Coastline Corner/Edge on neighbor DualCellsTouching via shared OccupancyCorners. Valence-4 required (length 4); valence-5 non-editable.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_whole_cell_orient_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | Whole DualCell Full on flip V + OccupancyCorners↔Stage6 + dual-edge-frame fit |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_whole_cell_edge_frame` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| LMB flip V → one MeshLibrary **Full** covers whole OwnedDualCell(V) (all four pie sectors) | `sector_pie_as_dual_cell_tile` · Corner-wedge-only as Success |
| OccupancyCorners length-4 ↔ Stage6 DualCorners; bit i ↔ c_i; edge0 = c0→c1 | occupancy primary ring `[Owner,n0,n1,n2]` as Success |
| Mesh/props follow DualCell edge directions (dual-edge UV→Stage6 warp; honest `dual_edge_frame_yaw_rad`) | `world_yaw_as_dual_edge_frame` · AABB-world pillar Success |
| UpdateFour DualCellsTouching KEEP; ghost=owned DualCell KEEP | expand-only · ghost≠paint |
| Keep: primary-V snap, Empty skip, dual `+`, Stage-6, terrain GLBs, squarify, rings=5, valence-5 out | ocean carpet · valence-5 editable |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** LMB snaps primary V; ghost=OwnedDualCell(V); place → **Full** terrain covers whole DualCell plate (all four secondary sectors); neighbor DualCells may show Corner/Edge coastline; modules read dual-edge frame (edge0=c0→c1); Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP; valence-5 non-placeable; Prefer refuses `sector_pie_as_dual_cell_tile` / `world_yaw_as_dual_edge_frame` / Corner-wedge-only |
| Out | pie host · world-XZ props as Success · incomplete yaw meta-lie · MCP-only attest |

## 4. Refuse (`do_not_waive`)

`sector_pie_as_dual_cell_tile` · `world_yaw_as_dual_edge_frame` · `corner_wedge_as_whole_dual_cell` · `expand_only_paint_as_success` · `neighbor_dual_as_owned_place` · `ocean_fill_all_empty_slots` · `secondary_face_snap_as_place` · `plinth_as_terrain` · `prop_scatter_as_composition` · `stretch_as_variant` · `gray_ramp_only` · `primary_face_as_dual` · `stamp_as_dual` · `metrics_only_glb_drop` · `proxy_substitution` · `intent_collapsed_to_mechanics` · `verify_mcp_only` · prior dual refuses

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_owned_cell_place_r1]] | **Seat KEEP** (ghost=paint OwnedDualCell; UpdateFour=DualCellsTouching); **coverage+orient SUPERSEDED** |
| [[alpha0_stalberg_dual_primary_vertex_place_r1]] | **Snap KEEP**; Empty skip / dual `+` KEEP |
| [[alpha0_stalberg_dual_cell_lookup_yaw_r1]] | Incomplete yaw SUPERSEDED (honest dual-edge frame + OccupancyCorners) |
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack GLBs/materials KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 DualCell geometry KEEP |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 squarify KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Cursor near orange star → snap primary V (KEEP); ghost outlines **OwnedDualCell(V)**.
3. LMB → **Full** MeshLibrary land covers **whole** OwnedDualCell(V) (all four secondary pie sectors — not one Corner wedge at c0).
4. Neighbor DualCells may refresh Corner/Edge for shared coastline; modules/props follow DualCell edges (edge0=c0→c1), not world-XZ pillars.
5. Free DualCells show amber grid — no ocean Empty carpet; dual `+` at face centres; no dual-edge ribbons.
6. Valence-5 verts remain non-editable.
7. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Prior seat [[alpha0_stalberg_dual_owned_cell_place_r1]] · Snap [[alpha0_stalberg_dual_primary_vertex_place_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]
