---
slice_id: alpha0_stalberg_dual_stage6_cell_r1
ask_id: alpha0_stalberg_dual_stage6_cell
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2i
created: 2026-10-04
updated: 2026-10-04
greenlit_at: 2026-10-04T04:57:09Z
claim_class: staging
factory_greenlit: true
status: armed_ready_to_stage
prior_slice_id: alpha0_stalberg_dual_face_centroid_r1
supersedes: alpha0_stalberg_dual_face_centroid_r1
logic_prior_slice_id: alpha0_stalberg_primal_graph_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_dual_face_centroid_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_stage6_cell_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
bug_image: Ingest/Screenshot_20261004_003640_YouTube.jpg
goal_image_note: graph-family compare vs Final-grid-state (organic hex boundary + irregular quads) — not art parity
terminology: Untitled.md Final-Grid dual vocabulary table
trinity_branch: project/genesis-mythos-master
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
success_object: dual_offset_cells
intent_invariant: "Player edits logic points (primal Vertices); dual cell around a logic point is the Stage-6 polygon of face centroids of faces incident to that point; dual vertices sit at main-face centres; dual edges connect those centroids across shared primal edges (cross main cells — never along main sides)."
prefer_concept_required: true
investigation: alpha0_stalberg_dual_geometry_rethink_investigation
---

# Slice brief — `alpha0_stalberg_dual_stage6_cell_r1`

**GREENLIT** `2026-10-04T04:57:09Z` — Stage-6 dual **cell / edge identity rebind**. Supersedes [[alpha0_stalberg_dual_face_centroid_r1]] LIVE weld that Prefer-concept'd the right invariant but kept DualCell 1:1 with primal Face + `FaceCornersLocal` inset rings (cyan overlays amber). Prefer **concept** required. claim_class staging until operator F5.

## Bug proof (operator F5)

Cite [[Ingest/Screenshot_20261004_003640_YouTube.jpg]]: cyan “dual” overlays amber main (same corners/edges). Root cause: DualCell still 1:1 with primal Face; `CornerVertices` = main face verts; `FaceCornersLocal` inset toward those corners → dual edges = shrunk primary = `primary_face_as_dual` / wrong dual-edge definition.

## Project end-state (craft-plane north star)

Authorable irregular dual-grid craft plane on an organic all-quad board. Correct Stage-6 / Final-Grid polarity (terminology [[Untitled]]):

| Element | Locus |
|---------|--------|
| Dual **vertex** | Main face centre (`+`) |
| Dual **edge** | Between two face centres of faces that share a main edge — **crosses** the main cell; does **not** run along main sides |
| Dual **cell** | Polygon around a main **intersection** (logic Vertex V); corners = face centroids of faces incident to V (`Stage6DualCellPolygon` = DualCell geometry/identity) |
| Placement / snap | Main intersection; populate segments color the sides of **that** dual cell |
| Neighbours | Dual cells that share a dual edge (share two dual verts / a side) |

One dual tile per logic point — **not** four inset face duals painted as 2×2. Keep craft camera 7× / zoom / 360 / palette / DualLatticeDebug spheres — redefine what edges/cells mean so cyan **crosses** amber; spheres stay at face centres.

## Path position

| Leg | Slice | Role |
|-----|-------|------|
| Prior | [[alpha0_stalberg_primal_graph_r1]] | MeshGraph + incidence landed |
| Aborted | [[alpha0_stalberg_dual_rebind_r1]] | Cardinal vertex-centred duals — wrong locus |
| Partial | [[alpha0_stalberg_dual_face_centroid_r1]] | Prefer concept ok; LIVE still FaceCornersLocal / face-as-dual wire+paint |
| **This** | `alpha0_stalberg_dual_stage6_cell_r1` | DualCell = Stage-6 cell-around-V; dual edges = centroid–centroid only |
| Next | [[alpha0_stalberg_dual_visual_r3]] | Dual visual on correct dual graph (after this F5) |

## Intent invariant (exact)

`Player edits logic points (primal Vertices); dual cell around a logic point is the Stage-6 polygon of face centroids of faces incident to that point; dual vertices sit at main-face centres; dual edges connect those centroids across shared primal edges (cross main cells — never along main sides).`

## Success object

`success_object: dual_offset_cells` with **correct edge/cell identity** (Prefer text / structural Success — intent validates gates, not reverse).

## Agree rationale

dual_face_centroid_r1 Prefer-concept'd the Stage-6 invariant and put dual verts at face centres, but DualCell identity stayed **one dual per Face** with `FaceCornersLocal` inset rings drawn/painted as dual edges — F5 cyan coincides with amber (`primary_face_as_dual`). This ticket makes `Stage6DualCellPolygon(V)` the DualCell geometry/identity (owned by logic V), stops drawing FaceCornersLocal as dual edges, and rebinds DualCellsTouching / ownership / update / highlight to Stage-6 cell-around-V.

## Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Prefer **concept** ok: `dual_offset_cells` + Stage-6 cell/edge identity invariant; LIVE DualCell = Stage-6 polygon around logic V (not per Face); wireframe = Stage-6 polygons + dual edges between face-centroid spheres only (cyan **crosses** amber main cells); no FaceCornersLocal sold as dual edges; OwnedDualCellKeys(V) = one dual cell owned by V; DualCellsTouching neighbours = dual cells sharing a dual edge; populated dual tile centered on intersection with multi-hue segments; spheres at face centres; MeshGraph + rings=2 spacing=3.0 + organic underlay + craft cam intact. |
| Out of scope | MeshLibrary dual_visual art polish, density lift, Terrain3D, Hex19 Success, chain-advance without concept Prefer |

## Refuse

- `proxy_substitution` · `intent_collapsed_to_mechanics`
- `primary_face_as_dual` · `inset_face_corners_as_dual` · `face_corners_local_as_dual_edges` · `face_block_neighborhood` · `face_proxy_dual` · `support_face_index_as_dual_success`
- `vertex_neighbor_as_dual_corner` · `dual_rebind_cardinal_wrong_locus` · `dual_centre_on_logic_as_half_step_proof` (dual **verts** must stay at face centres — LocalCentre may sit at logic V as placement)
- `face_scan_proxy_neighborhood` · `soft_take_4` · `valence_drop_editable`
- `unstable_dual_neighborhood` · `over_neighbor_paint` · `stamp_as_dual` · `skip_dual_offset`
- `indexed_lists_as_graph` · `ephemeral_edge_key_as_topology` · `non_unique_vertices`
- `points_as_grid` · `count_equals_topology` · `explicit_met_implicit_miss`
- `hex19_pick_as_craft_authority` · `gray_ramp_only` · `inspiration_shape_miss` · `terrain3d_in_scope` · `craft_cam_recenter_on_place`
- Selling inset FaceCornersLocal rings as dual Success · dual wireframe that only redraws primary · face-fill paint as dual tile

## Kickoff

1. Write + prime brief/armed; hub `armed_slice_id` → dual_stage6_cell_r1; greenlit true; supersede dual_face_centroid pointers.
2. Slice Producer compose with full conceptual leg (judgment — structural-only / harness_fallback must fail).
3. IMPLEMENT_SLICE rebuild `OrganicDualOffsetLattice` DualCell = Stage-6 cell-around-V; host wireframe/paint/pick/prove; stop FaceCornersLocal as dual edges.
4. Prefer **concept** ok; MCP / F5 evidence (cyan crosses amber; one dual tile per logic point).
5. Trinity push project tip when Prefer path established. Dual report A + B. Receipt staging until operator F5. Curator snapshot per operator GREENLIGHT WELD.

## Related

- Bug shot [[Ingest/Screenshot_20261004_003640_YouTube.jpg]] · Terminology [[Untitled]] · Goal [[Ingest/Final-grid-state.jpg]]
- Supersedes [[alpha0_stalberg_dual_face_centroid_r1]] · Investigation [[alpha0_stalberg_dual_geometry_rethink_investigation]]
- Prefer/weave [[prefer_intent_validates_gates_r1]] · [[Prefer-Authorship-Host-Law]] § C.2
- Prior [[alpha0_stalberg_primal_graph_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Next [[alpha0_stalberg_dual_visual_r3]]
