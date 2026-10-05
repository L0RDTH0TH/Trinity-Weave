---
title: Series — alpha0_stalberg_grid_kernel_r1
slice_id: alpha0_stalberg_grid_kernel_r1
ask_id: alpha0_stalberg_quad_kernel
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-03
updated: 2026-10-04
claim_class: staging
factory_greenlit: true
status: whole_cell_orient_r1_greenlit_weld_live_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
active_step: 2s
active_step_slice_id: alpha0_stalberg_dual_whole_cell_orient_r1
parallel_dual_step: 2s
parallel_dual_slice_id: alpha0_stalberg_dual_whole_cell_orient_r1
density_lift: live_rings_5_spacing_210
dual_visual_ask_success: armed_staging_prefer_until_operator_f5
manual_limit: hex19_seed_rings_2
source_yt: https://www.youtube.com/watch?v=Y19Mw5YsgjI
lerg_yt: https://youtu.be/Jm3pLya3d9c
algorithm_upstream: https://github.com/kai-denrei/oskar-procedure
goal_image: Ingest/Final-grid-state.jpg
squarify_goal_image: Ingest/single-grid-section.jpg
---

# Series — `alpha0_stalberg_grid_kernel_r1`

**Thin product Prefer series** for Stålberg organic all-quad **grid kernel**, then craft-plane authority, then dual/corner. Separate from the Townscaper tutorial ladder ([[alpha0_townscaper_tutorial_r1]]).

Umbrella: [[alpha_architecture_half_b]]. Topology: [[Grid-Topology-Host-Law]]. Prefer: [[Prefer-Authorship-Host-Law]]. Goal visual: [[Ingest/Final-grid-state.jpg]].

## Ladder

| Step | Ticket | Scope | Greenlit | Notes |
|------|--------|-------|----------|-------|
| 1 | [[alpha0_stalberg_quad_kernel_r1]] | Organic all-quad pipeline | was true — altitude fail | Approach OK |
| 1b | [[alpha0_stalberg_quad_kernel_visual_r1]] | Planar readable board | superseded | — |
| 1c | [[alpha0_stalberg_quad_kernel_relax_r1]] | Unique topo + area square relax | altitude fail | — |
| 1d | [[alpha0_stalberg_quad_kernel_relax_r2]] | Goal fidelity draft | false | near-zero diag |
| 1e | [[alpha0_stalberg_topology_base_r1]] | Upstream injective topo + soft relax | staging recovered | kernel foundation |
| **1h** | [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage 5 rotate-90 average squarify | **GREENLIT WELD** | replaces Variant A closest-square; goal [[Ingest/single-grid-section.jpg]] |
| **1f** | [[alpha0_stalberg_craft_plane_authority_r1]] | Rebind pick/paint onto OrganicQuadMesh | **staging Prefer ok** | Hex19 not Success; MCP evidence |
| 2 | [[alpha0_stalberg_dual_corner_r1]] | Dual-corner **logic** on organic quads | **staging Prefer ok** — not product ask_success | gray ramp visual gap |
| **1g** | [[alpha0_stalberg_manual_scale_r1]] | Hex-19 / tutorial seed scale (rings=2) | **staging Prefer ok** | density lift deferred |
| **2b** | [[alpha0_stalberg_dual_visual_r1]] | Dual visual / MeshLibrary fidelity | **failed_altitude / partial** | Prefer ok then stretch-as-shape; see [[Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03]] |
| 2c′ | [[alpha0_stalberg_dual_visual_r2]] | Discrete silhouettes Prefer harden | **paused** — dual_visual ask_success deferred | Prefer harden landed; neighborhood first |
| **2c** | [[alpha0_stalberg_dual_neighborhood_r1]] | Stable dual-graph ownership (≤4) | **partial_wrong_object** | stable primary-face 2×2; superseded by 2d |
| **2d** | [[alpha0_stalberg_dual_lattice_r1]] | Half-step lattice weld + staging Prefer | **superseded / partial_wrong_object** | no concept Prefer; superseded by 2e |
| **2e** | [[alpha0_stalberg_dual_lattice_r2]] | Dual lattice ownership + conceptual leg | staging Prefer concept ok · awaiting F5 | `success_object: dual_offset_cells` |
| **2f** | [[alpha0_stalberg_primal_graph_r1]] | Primal MeshGraph + incidence; dual corners = Vertex refs | F5: MeshGraph ok · **neighbor still wrong** | `success_object: organic_mesh_graph` |
| **2g** | [[alpha0_stalberg_dual_rebind_r1]] | Dual ownership via MeshGraph incidence only | **ABORTED** (geometry rethink) | `success_object: dual_offset_cells` |
| **2h** | [[alpha0_stalberg_dual_face_centroid_r1]] | Stage-6 face-centroid dual verts on MeshGraph | **superseded / partial_wrong_object** | Prefer concept ok; LIVE FaceCornersLocal / face-as-dual |
| **2i** | [[alpha0_stalberg_dual_stage6_cell_r1]] | DualCell = Stage-6 cell-around-V; centroid–centroid edges | **staging Prefer concept ok** | geometry KEEP for 2j |
| **2j** | [[alpha0_stalberg_dual_glow_neighborhood_r1]] | Expand-glow neighborhood (2 edge / 4 interior) | **staging Prefer concept ok** | small-corner units KEEP for 2k |
| **2k** | [[alpha0_stalberg_dual_secondary_glow_center_r1]] | Pick/glow center on secondary (face centroid) | **staging Prefer ok · 2k F5 assumed green (operator trajectory)** | `success_object: dual_offset_cells` |
| **2l** | [[alpha0_stalberg_dual_visual_r3]] | Dual visual / MeshLibrary models | **r3_pass verified** (staging Prefer) | rigid discrete GLB cubes/blocks on secondary slots |
| **2m** | [[alpha0_stalberg_dual_mesh_fit_r1]] | Mesh-fit 4 corner sectors to secondary quads | **GREENLIT WELD** | bilinear warp to SmallCornerQuad.Corners |
| **2n** | [[alpha0_stalberg_dual_art_style_r1]] | Cream quarter-platform restyle | **wrong Success / superseded** | Prefer-fails plinth_as_terrain under harden |
| **2o** | [[alpha0_stalberg_dual_terrain_tile_r1]] | Land/water dual_offset_terrain_tile sixpack | **GREENLIGHT WELD LIVE** · staging until F5 | gold sixpack + LIVE GLB bind |
| **2p** | [[alpha0_stalberg_dual_cell_lookup_yaw_r1]] | Host DualCell lookup/yaw | incomplete yaw **SUPERSEDED** by 2s | materials KEEP |
| **2q** | [[alpha0_stalberg_dual_primary_vertex_place_r1]] | Primary-V snap + Empty skip | snap **KEEP** | paint polarity superseded |
| **2r** | [[alpha0_stalberg_dual_owned_cell_place_r1]] | Owned DualCell seat polarity | seat **KEEP** · coverage+orient superseded by 2s | UpdateFour DualCellsTouching |
| **2s** | [[alpha0_stalberg_dual_whole_cell_orient_r1]] | Whole DualCell Full + Stage6 OccupancyCorners + dual-edge frame | coverage+frame **KEEP** · paint-scope SUPERSEDED by 2t | `success_object: dual_cell_meshlibrary_placement` |
| **2t** | [[alpha0_stalberg_dual_owned_only_paint_r1]] | Owned-only Full paint + Z-fight harden | owned-only **KEEP** · n=3 place skip SUPERSEDED by 2u | `success_object: dual_cell_meshlibrary_placement` |
| **2u** | [[alpha0_stalberg_dual_tri_cell_place_r1]] | Tri DualCell (DualCorners==3) Full owned-only place | **GREENLIGHT WELD LIVE** · staging until F5 · visuals deferred | `success_object: dual_cell_meshlibrary_placement` |

## Active authority

| Field | Value |
|-------|--------|
| Active step | **2u** — [[alpha0_stalberg_dual_tri_cell_place_r1]] (**GREENLIGHT WELD LIVE** · tri DualCell place · visuals deferred · staging until F5) |
| Squarify foundation | **1h** — [[alpha0_stalberg_quad_kernel_squarify_r1]] KEEP |
| Prior dual | **2k** — [[alpha0_stalberg_dual_secondary_glow_center_r1]] (F5 assumed green · KEEP secondary glow) |
| Kernel foundation | [[alpha0_stalberg_topology_base_r1]] |
| Manual limit | rings=2 (~54 quads) + spacing=3.0 (large cells) — Prefer edges+faces |
| Density lift | **LIVE** rings=5 / spacing=210 (squarify_r1 knobs) |
| Dual visual | **2o** terrain materials KEEP · **2r** seat KEEP · **2s** coverage+frame KEEP · **2t** owned-only KEEP · **2u** tri-cell place **GREENLIGHT WELD LIVE** (staging until F5 · visuals deferred) |
| Prior Prefer ok (staging) | craft-plane · dual_corner (logic only) · manual_scale · dual_lattice_r2 · primal_graph_r1 (MeshGraph) · dual_stage6_cell_r1 (geometry) · dual_glow_neighborhood_r1 (small-corner units) |
| Superseded | dual_face_centroid_r1 — Prefer ok; LIVE inset face duals (see bug shot Screenshot_20261004_003640) |
| Aborted | dual_rebind_r1 — vertex-centred wrong locus (see [[alpha0_stalberg_dual_geometry_rethink_investigation]]) |
| Dual visual r1 | **failed_altitude / partial** — not product Success |
| Prefer audit | [[Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03]] |
| Tutorial ladder | cite-only — [[alpha0_townscaper_tutorial_r1]] |

## Prefer/weave track (cross-cutting — not a ladder step)

Doctrine harden (draft): [[prefer_authorship_harden_track_r1]] · umbrella [[prefer_intent_validates_gates_r1]] · dual seat [[prefer_dual_object_identity_r1]] · audit [[Prefer-Audit-proxy-substitution-pattern-2026-10-03]]. Does **not** replace step 2e welding; widens Prefer law so dual harden is not the whole Prefer product.

## Related

- [[alpha0_stalberg_dual_tri_cell_place_r1]] · [[alpha0_stalberg_dual_owned_only_paint_r1]] · [[alpha0_stalberg_dual_whole_cell_orient_r1]] · [[alpha0_stalberg_dual_owned_cell_place_r1]] · [[alpha0_stalberg_dual_primary_vertex_place_r1]] · [[alpha0_stalberg_dual_cell_lookup_yaw_r1]] · [[alpha0_stalberg_dual_terrain_tile_r1]] · [[alpha0_stalberg_dual_art_style_r1]] · [[alpha0_stalberg_dual_mesh_fit_r1]] · [[alpha0_stalberg_dual_visual_r3]] · [[alpha0_stalberg_dual_secondary_glow_center_r1]] · [[alpha0_stalberg_dual_glow_neighborhood_r1]] · [[alpha0_stalberg_dual_stage6_cell_r1]] · [[alpha0_stalberg_dual_face_centroid_r1]] · [[alpha0_stalberg_dual_geometry_rethink_investigation]] · [[alpha0_stalberg_dual_rebind_r1]] · [[alpha0_stalberg_primal_graph_r1]] · [[alpha0_stalberg_dual_lattice_r2]] · [[alpha0_stalberg_dual_lattice_r1]] · [[alpha0_stalberg_dual_neighborhood_r1]] · [[alpha0_stalberg_dual_visual_r2]] · [[alpha0_stalberg_dual_visual_r1]] · [[Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03]] · [[Prefer-Authorship-Host-Law]] · [[Half-B-Weld-Brief-Template]]
