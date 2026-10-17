---
slice_id: alpha0_stalberg_dual_face_centroid_r1
ask_id: alpha0_stalberg_dual_face_centroid
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2h
created: 2026-10-04
updated: 2026-10-04
greenlit_at: 2026-10-04T03:23:09Z
claim_class: superseded
factory_greenlit: false
status: superseded_partial_wrong_object_by_dual_stage6_cell_r1
operator_kill_at: 2026-10-04T04:57:09Z
superseded_reason: live_face_corners_local_as_dual_edges_cyan_overlays_amber
prior_slice_id: alpha0_stalberg_primal_graph_r1
supersedes: alpha0_stalberg_dual_rebind_r1
logic_prior_slice_id: alpha0_stalberg_primal_graph_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_primal_graph_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_face_centroid_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
goal_image_note: graph-family compare vs Final-grid-state (organic hex boundary + irregular quads) — not art parity
trinity_branch: project/genesis-mythos-master
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
success_object: dual_offset_cells
intent_invariant: "Player edits logic points (primal Vertices); dual cell around a logic point is the polygon of face centroids of faces incident to that point; dual vertices sit at main-face centres."
prefer_concept_required: true
investigation: alpha0_stalberg_dual_geometry_rethink_investigation
---

# ⛔ SUPERSEDED — partial wrong object

**2026-10-04T04:57:09Z** — Operator F5 [[Ingest/Screenshot_20261004_003640_YouTube.jpg]]: cyan overlays amber. Prefer concept held the Stage-6 invariant, but LIVE DualCell stayed 1:1 with Face + `FaceCornersLocal` inset rings. Superseded by [[alpha0_stalberg_dual_stage6_cell_r1]].

# Slice brief — `alpha0_stalberg_dual_face_centroid_r1`

**GREENLIT** `2026-10-04T03:23:09Z` — Stage-6 / Hex19 face-centroid dual geometry. Supersedes aborted [[alpha0_stalberg_dual_rebind_r1]] (wrong locus: duals centred on primal verts with edge-neighbor corners). Prefer **concept** required. claim_class staging until operator F5.

## Project end-state (craft-plane north star)

Authorable irregular dual-grid craft plane on an organic all-quad board. Dual **vertices** sit at **centroids of primal faces** (half-offset lattice). Player edits **logic points** (primal Vertices); the dual cell around a logic point is the CCW polygon of those face centroids. Cyan / update-four = face-centroid dual tiles that sample the clicked point (≤4 interior) — never a filled primal-face 2×2 block, never vertex-neighbour star quads.

## Path position

| Leg | Slice | Role |
|-----|-------|------|
| Prior | [[alpha0_stalberg_primal_graph_r1]] | MeshGraph + incidence landed |
| Aborted | [[alpha0_stalberg_dual_rebind_r1]] | Cardinal vertex-centred duals — **wrong locus** (geometry rethink) |
| Investigation | [[alpha0_stalberg_dual_geometry_rethink_investigation]] | Face-centroid dual verts = Stage 6 / Hex19 polarity |
| **This** | `alpha0_stalberg_dual_face_centroid_r1` | Stage-6 face-centroid dual lattice on MeshGraph |
| Next | [[alpha0_stalberg_dual_visual_r3]] | Dual visual on correct dual graph (after this F5) |

## Intent invariant (exact)

`Player edits logic points (primal Vertices); dual cell around a logic point is the polygon of face centroids of faces incident to that point; dual vertices sit at main-face centres.`

## Success object

`success_object: dual_offset_cells` (Prefer-aligned lattice SO; face-centroid geometry is the Prefer text / structural Success — not a new SO name that Prefer rejects as `centroid` proxy).

| Element | Locus |
|---------|--------|
| Dual vertex | Centroid of a primal Face |
| Dual cell around logic V | CCW polygon of face-centroids of `FacesTouchingVertex(V)` |
| Logic / paint | Primal Vertex ids (corner-state) |
| Update-four | Dual tiles that sample V as a corner → ≤4 interior face-centroid duals |

## Goal image / graph family

Cite [[Ingest/Final-grid-state.jpg]]: organic hex outer boundary + irregular quad-dominant mesh (Stålberg family). Success = **graph-family** match (dual verts in face centres; dual cells as offset polygons), **not** art parity / texture / color match.

## Agree rationale

dual_rebind Prefer-concept'd `dual_offset_cells` but LIVE set `LocalCentre = owner.Position` with corners = edge-neighbor Vertices — dual verts never sit in main-face centres. Hex19 / oskar Stage 6 want the opposite polarity for half-step proof (centre off occupancy / at face centre). This ticket rebuilds `OrganicDualOffsetLattice` to face-centroid duals and fixes `IsHalfStepOffset` to Hex19 polarity.

## Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Prefer **concept** ok: `dual_offset_cells` + face-centroid invariant; LIVE dual verts at face centres; `DualCellsTouching` / `OwnedDualCellKeys` / `UpdateFour*` = ≤4 face-centroid duals sampling the logic Vertex; cyan on those dual tiles (not filled primal face block); `IsHalfStepOffset` Hex19 polarity; MeshGraph Vertex corner-state preserved; rings=2 spacing=3.0 + organic underlay intact. |
| Out of scope | MeshLibrary dual_visual art polish, density lift, Terrain3D, Hex19 Success, chain-advance without concept Prefer |

## Refuse

- `proxy_substitution` · `intent_collapsed_to_mechanics`
- `vertex_neighbor_as_dual_corner` · `dual_rebind_cardinal_wrong_locus` · `dual_centre_on_logic_as_half_step_proof`
- `primary_face_as_dual` · `face_block_neighborhood` · `face_proxy_dual` · `support_face_index_as_dual_success`
- `face_scan_proxy_neighborhood` · `soft_take_4` · `valence_drop_editable`
- `unstable_dual_neighborhood` · `over_neighbor_paint` · `stamp_as_dual` · `skip_dual_offset`
- `indexed_lists_as_graph` · `ephemeral_edge_key_as_topology` · `non_unique_vertices`
- `points_as_grid` · `count_equals_topology` · `explicit_met_implicit_miss`
- `hex19_pick_as_craft_authority` · `gray_ramp_only` · `inspiration_shape_miss` · `terrain3d_in_scope` · `craft_cam_recenter_on_place`

## Kickoff

1. Write + prime brief/armed; hub `armed_slice_id` → dual_face_centroid_r1; greenlit true; supersede dual_rebind pointers.
2. Slice Producer compose with full conceptual leg (judgment — structural-only / harness_fallback must fail).
3. IMPLEMENT_SLICE rewrite `OrganicDualOffsetLattice` (+ host highlight/update) to Stage-6 face-centroid duals; fix `IsHalfStepOffset` polarity.
4. Prefer **concept** ok; MCP evidence (dual verts at face centres; update-four; not 2×2 primal block).
5. Trinity push project tip. Dual report B (intent-seat). Receipt staging until operator F5. No Curator.

## Related

- Investigation [[alpha0_stalberg_dual_geometry_rethink_investigation]] · Aborted [[alpha0_stalberg_dual_rebind_r1]]
- Prefer/weave [[prefer_intent_validates_gates_r1]] · [[Prefer-Authorship-Host-Law]] § C.2
- Prior [[alpha0_stalberg_primal_graph_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Next [[alpha0_stalberg_dual_visual_r3]]
- Goal image [[Ingest/Final-grid-state.jpg]] · Oskar Stage 6 · Hex19 dual polarity
