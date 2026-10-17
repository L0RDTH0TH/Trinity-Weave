---
slice_id: alpha0_stalberg_primal_graph_r1
ask_id: alpha0_stalberg_primal_graph
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2f
created: 2026-10-03
updated: 2026-10-03
claim_class: staging
factory_greenlit: true
status: f5_confirmed_neighbor_still_wrong__next_dual_rebind_r1
prior_slice_id: alpha0_stalberg_dual_lattice_r2
logic_prior_slice_id: alpha0_stalberg_dual_lattice_r2
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_dual_lattice_r2
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_primal_graph_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
trinity_sha: ee27f1e4fe0fa8d0100aef3e48b9c97650d387ab
prefer_main_sha: b4547f2b4deb5195866497c590cd578a936f3bc5
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
success_object: organic_mesh_graph
intent_invariant: "Primal ownership is Vertex/Edge/Face singletons with incidence; dual cells are half-offset quads whose corners are those shared Vertex refs."
prefer_concept_required: true
---

# Slice brief — `alpha0_stalberg_primal_graph_r1`

**GREENLIT** `2026-10-04T01:58:48Z` — primal MeshGraph + incidence ownership (concept Prefer). Investigation thesis: improper primal (`List<Vector2>`+`int[]`+ephemeral edge keys) compounds into dual neighbor failures. claim_class staging until operator F5.

## Project end-state (craft-plane north star)

Authorable irregular dual-grid craft plane on an organic all-quad board. Primal ownership is **Vertex / Edge / Face singletons with incidence**; dual cells are half-offset quads whose corners are those **shared Vertex refs** (not int-index theater, not SupportFaceIndex Success, not soft Take(4)).

## Path position

| Leg | Slice | Role |
|-----|-------|------|
| Prior | [[alpha0_stalberg_dual_lattice_r2]] | Half-step dual lattice symbols/concept; possible face-proxy dual corners |
| **This** | `alpha0_stalberg_primal_graph_r1` | Primal `OrganicMeshGraph` + incidence; dual corners = Vertex refs |
| Next | dual rebind proof → [[alpha0_stalberg_dual_visual_r3]] | Prove dual ownership on graph incidence; then dual_visual |

## Intent invariant (exact)

`Primal ownership is Vertex/Edge/Face singletons with incidence; dual cells are half-offset quads whose corners are those shared Vertex refs.`

## Success object

`success_object: organic_mesh_graph`

## Agree rationale

dual_lattice_r2 Prefer-concept'd `dual_offset_cells` while LIVE primal remained indexed lists + ephemeral edge keys + SupportFaceIndex / `_vertexToFaces` dual adjacency. That improper primal compounds into dual neighbor failures. This ticket installs MeshGraph singletons + incidence as the primal Success object and rebinds dual ownership corners to shared Vertex refs.

## Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Prefer **concept** ok: `organic_mesh_graph` + invariant; LIVE has `OrganicMeshGraph` (Vertex/Edge/Face, GetOrAddVertex/Edge, AddQuad, FacesTouchingVertex); kernel emit/hold graph; OrganicQuadMesh wraps graph; UniqueTopology2D migrated into graph builder; dual lattice/host corners = Vertex refs; no Success via SupportFaceIndex / dead `_vertexToFaces` / soft Take(4); rings=2 spacing=3.0 intact. |
| Out of scope | MeshLibrary dual_visual art polish, density lift, Terrain3D, Hex19 Success, chain-advance without concept Prefer |

## Refuse

- `proxy_substitution` · `intent_collapsed_to_mechanics`
- `indexed_lists_as_graph` · `ephemeral_edge_key_as_topology`
- `primary_face_as_dual` · `non_unique_vertices`
- `points_as_grid` · `count_equals_topology` · `explicit_met_implicit_miss`
- `hex19_pick_as_craft_authority` · `gray_ramp_only` · `inspiration_shape_miss` · `terrain3d_in_scope` · `craft_cam_recenter_on_place`

## Kickoff

1. Write + prime brief/armed; hub `armed_slice_id` → r1; greenlit true.
2. Slice Producer compose with full conceptual leg (judgment — structural-only must fail).
3. IMPLEMENT_SLICE weld LIVE OrganicMeshGraph + dual rebind.
4. Prefer **concept** ok; MCP if runnable.
5. Trinity push project tip (+ Prefer if scanners changed). Receipt staging until operator F5. No Curator.

## Related

- Prefer/weave [[prefer_intent_validates_gates_r1]] · [[Prefer-Authorship-Host-Law]] § C.2
- Prior [[alpha0_stalberg_dual_lattice_r2]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Next [[alpha0_stalberg_dual_visual_r3]]
