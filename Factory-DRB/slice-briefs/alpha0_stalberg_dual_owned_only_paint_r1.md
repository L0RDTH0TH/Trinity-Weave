---
slice_id: alpha0_stalberg_dual_owned_only_paint_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2t
created: 2026-10-04
updated: 2026-10-04
greenlit_at: '2026-10-04T23:58:00Z'
composed_at: '2026-10-04T23:58:00Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat_from: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame_from: alpha0_stalberg_dual_whole_cell_orient_r1
depends_on: alpha0_stalberg_dual_whole_cell_orient_r1
supersedes_paint_scope:
  - alpha0_stalberg_dual_whole_cell_orient_r1
keeps_coverage_orient:
  - alpha0_stalberg_dual_whole_cell_orient_r1
keeps_seat_polarity:
  - alpha0_stalberg_dual_owned_cell_place_r1
keeps_snap_polarity:
  - alpha0_stalberg_dual_primary_vertex_place_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_owned_only_paint_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_owned_only_paint
contract: C_dual_owned_only_paint
materials_keep: dual_offset_terrain_tile_sixpack
operator_diagnosis: flip_v_owned_full_ok__update_four_neighbor_corner_cross__coplanar_full_corner_zfight_flash
---

# Slice brief — `alpha0_stalberg_dual_owned_only_paint_r1`

**GREENLIGHT WELD LIVE** `2026-10-04T23:58:00Z` — Prefer concept + owned-only MeshLibrary paint scope + Z-fight harden. Coverage+frame KEEP from [[alpha0_stalberg_dual_whole_cell_orient_r1]]; paint-scope SUPERSEDE (neighbor Corner/Edge as place Success refused). Seat KEEP [[alpha0_stalberg_dual_owned_cell_place_r1]]; snap KEEP [[alpha0_stalberg_dual_primary_vertex_place_r1]]. `claim_class: staging` until operator F5. Valence-5 stays non-placeable.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Materials KEEP: [[alpha0_stalberg_dual_terrain_tile_r1]]. Geometry KEEP: [[alpha0_stalberg_dual_stage6_cell_r1]]. Coverage+frame KEEP: [[alpha0_stalberg_dual_whole_cell_orient_r1]]. Seat KEEP: [[alpha0_stalberg_dual_owned_cell_place_r1]]. Snap KEEP: [[alpha0_stalberg_dual_primary_vertex_place_r1]].

## Why (operator F5 2026-10-04)

After `alpha0_stalberg_dual_whole_cell_orient_r1`: secondary/owned DualCell looks filled, but click produces a **cross of 5 stacks** (center + 4 arms). Camera pan → **seizure-flashes** (Z-fighting).

Code diagnosis (confirmed):

1. **OwnedDualCell(V)** → `ownerOn` → forced **Full** (center, big green) — coverage KEEP correct.
2. **UpdateFour = DualCellsTouching(V)** refreshes owned + expand neighbors.
3. Each **neighbor DualCell(N)** has V in `OccupancyCorners` → one bit on → **Corner** (four arms).
4. Whole_cell_orient even named coastline Corner on neighbors as Success — that spray is **not** operator Success for “one module on DualCell(V).”
5. Z-fight: Full + neighbor Corner plates share edges at same `yLift` (~12); wallless Full tops coplanar with Corner decks; Full GLB multi-deck green/grey flicker on center cap.

## Paint-scope contract (binding)

| Rule | Detail |
|------|--------|
| Place Success | LMB flip V → **one** MeshLibrary item on **OwnedDualCell(V) only** |
| Coverage KEEP | owner-on → **Full** whole DualCell (all four pies) — not Corner-wedge-only |
| Neighbor mesh | UpdateFour may *recompute* neighbors → **Empty / ClearDualSlot** when bits change; neighbor cells stay **Empty mesh** unless **their own** owner is on (coastline Corner/Edge deferred) |
| Orient/frame KEEP | OccupancyCorners ↔ Stage6 DualCorners; MeshFitToDualEdgeFrame edge0=c0→c1 |
| Z-fight | No coplanar Full/Corner deck flicker — owned-only removes 4-arm overlap; bias Full tops (epsilon Y / depth / strip duplicate decks) so pan does not flash |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_owned_only_paint_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | Owned-only non-Empty MeshLibrary on DualCell(V); Full coverage KEEP; Z-fight harden |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_owned_only_paint` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| LMB flip V → one MeshLibrary **Full** on OwnedDualCell(V) only | `neighbor_corner_spray_as_place` · `update_four_cross_as_success` |
| Owned DualCell still **Full** (whole cell / all four pies) when owner on | Corner-wedge-only / `sector_pie_as_dual_cell_tile` |
| Neighbor DualCells: ClearDualSlot / Empty skip unless N owner-on | coastline Corner/Edge stamp as place Success (deferred) |
| No coplanar Full/Corner deck seizure-flash on camera pan | `seizure_coplanar_deck_as_success` |
| Orient/frame KEEP from whole_cell_orient (dual-edge frame) | `world_yaw_as_dual_edge_frame` |
| Keep: primary-V snap, ghost=owned, Empty skip, dual `+`, Stage-6, terrain GLBs, squarify, rings=5, valence-5 out | ocean carpet · valence-5 editable |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** LMB snaps primary V; ghost=OwnedDualCell(V); place → **one Full** on OwnedDualCell(V) only (whole plate, not wedge); **no** 5-stack cross of neighbor Corner arms; neighbors Empty unless own owner on; camera pan shows **no** seizure coplanar flicker; dual-edge frame KEEP; Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP; valence-5 non-placeable; Prefer refuses `neighbor_corner_spray_as_place` / `update_four_cross_as_success` / `seizure_coplanar_deck_as_success` |
| Out | neighbor Corner spray as Success · UpdateFour cross as Success · coplanar flash as Success · MCP-only attest · coastline contract (deferred) |

## 4. Refuse (`do_not_waive`)

`neighbor_corner_spray_as_place` · `update_four_cross_as_success` · `seizure_coplanar_deck_as_success` · `sector_pie_as_dual_cell_tile` · `world_yaw_as_dual_edge_frame` · `corner_wedge_as_whole_dual_cell` · `expand_only_paint_as_success` · `neighbor_dual_as_owned_place` · `ocean_fill_all_empty_slots` · `secondary_face_snap_as_place` · `plinth_as_terrain` · `prop_scatter_as_composition` · `stretch_as_variant` · `gray_ramp_only` · `primary_face_as_dual` · `stamp_as_dual` · `metrics_only_glb_drop` · `proxy_substitution` · `intent_collapsed_to_mechanics` · `verify_mcp_only` · prior dual refuses

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_whole_cell_orient_r1]] | **Coverage+frame KEEP** (Full whole DualCell; OccupancyCorners↔Stage6; dual-edge frame); **paint-scope SUPERSEDED** (neighbor Corner coastline as place Success out) |
| [[alpha0_stalberg_dual_owned_cell_place_r1]] | **Seat KEEP** (ghost=paint OwnedDualCell; UpdateFour=DualCellsTouching recompute OK) |
| [[alpha0_stalberg_dual_primary_vertex_place_r1]] | **Snap KEEP**; Empty skip / dual `+` KEEP |
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack GLBs/materials KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 DualCell geometry KEEP |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 squarify KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. LIVE weld (implementer)

- `UpdateFourDualSlots` / resolve: only place non-Empty MeshLibrary on DualCell whose `OwnerVertexId` is the flipped (or filled) owner; neighbors `ClearDualSlot` / Empty skip unless owner-on.
- Or: OccupancyCorners bit from V must not instantiate Corner on DualCell(N) while N owner off — coastline deferred.
- Z-fight hardening on Full path if needed (epsilon Y / depth / strip duplicate decks).
- Prefer concept; arm `factory-project.yaml`; claim_class staging until F5.

## 7. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Cursor near orange star → snap primary V (KEEP); ghost outlines **OwnedDualCell(V)**.
3. LMB → **one Full** MeshLibrary land covers **whole** OwnedDualCell(V) only — **no** cross of 5 stacks (no neighbor Corner arms).
4. Neighbor DualCells stay Empty mesh (amber grid) unless their own owner is on.
5. Pan/orbit camera — **no** seizure coplanar Full/Corner flicker.
6. Modules still read dual-edge frame (edge0=c0→c1); Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP.
7. Valence-5 verts remain non-editable.
8. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Prior coverage+frame [[alpha0_stalberg_dual_whole_cell_orient_r1]] · Seat [[alpha0_stalberg_dual_owned_cell_place_r1]] · Snap [[alpha0_stalberg_dual_primary_vertex_place_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]
