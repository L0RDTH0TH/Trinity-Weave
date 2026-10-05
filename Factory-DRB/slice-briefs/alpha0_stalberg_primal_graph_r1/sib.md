---
slice_id: alpha0_stalberg_primal_graph_r1
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
producer_run_id: sp-pgr1-25ad34
ask_id: alpha0_stalberg_primal_graph
series_id: alpha0_stalberg_grid_kernel_r1
factory_greenlit: true
prefer_authorship: true
prefer_concept_required: true
success_object: organic_mesh_graph
intent_invariant: "Primal ownership is Vertex/Edge/Face singletons with incidence; dual cells are half-offset quads whose corners are those shared Vertex refs."
composed_at: 2026-10-04T01:59:27Z
compose_path: slice_producer_judgment
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_primal_graph_r1.armed.yaml
lane_roster: [module]
---

# Slice Implementation Brief — Primal MeshGraph r1

## 1. Product goal (UX)

**North star (L5 / project end-state):**
Authorable irregular dual-grid craft plane on organic all-quad board. Primal ownership is **Vertex/Edge/Face singletons with incidence**; dual cells are half-offset quads whose corners are those **shared Vertex refs**.

**Dispatch depth L1 bar:**
- **UX-1:** Primal Success = `organic_mesh_graph` (not `List<Vector2>`+`int[]` theater).
- **UX-2:** Dual corners = shared MeshGraph Vertex refs; refuse SupportFaceIndex / `_vertexToFaces` / soft Take(4) as Success.
- **UX-3:** Incidence APIs: GetOrAddVertex, GetOrAddEdge, AddQuad, FacesTouchingVertex.
- **UX-4:** Prefer concept ok required: success_object + intent invariant; staging Prefer alone does not advance.
- **UX-5:** Preserve organic underlay + craft-plane authority + rings=2 spacing=3.0; regenerable.
- **UX-6:** Out of scope: density, Terrain3D, dual_visual art, Curator.

### Conceptual leg (Prefer concept — judgment; not structural-only Success)

| Field | Value |
|-------|--------|
| `project_end_state` | Authorable irregular dual-grid craft plane on organic all-quad board. |
| `end_state` | Primal MeshGraph incidence is ownership surface; dual cells half-offset on shared Vertex refs; dual_visual later. |
| `path_position` | dual_lattice_r2 → this primal MeshGraph + incidence → next dual rebind proof → dual_visual_r3 |
| `success_object` | `organic_mesh_graph` |
| `intent_invariant` | Primal ownership is Vertex/Edge/Face singletons with incidence; dual cells are half-offset quads whose corners are those shared Vertex refs. |
| `structural_success` | OrganicMeshGraph singletons + incidence; dual corners = Vertex refs; Prefer concept ok. |

**Refuse proxies:** `proxy_substitution` · `indexed_lists_as_graph` · `ephemeral_edge_key_as_topology` · `primary_face_as_dual` · `non_unique_vertices` · `intent_collapsed_to_mechanics`

## 2. Shape lock (Conceptual)

- success_object = organic_mesh_graph
- Intent invariant exact (quoted above)
- Path: dual_lattice_r2 → **this** → dual rebind proof → dual_visual_r3

## 3. Realization (Execution)

| UX | Realization |
|----|-------------|
| UX-1 | CREATE `OrganicMeshGraph.cs`; kernel emit/hold; OQM wrap |
| UX-2 | Rebind OrganicDualOffsetLattice + DualGridCraftHost to Vertex refs |
| UX-3 | Migrate UniqueTopology2D into graph builder |
| UX-4 | Prefer concept ok; no staging-only chain-advance |
| UX-5 | Keep rings=2 spacing=3.0 craft authority |
| UX-6 | No dual_visual / density / Terrain3D / Curator |

**Zone (module):** OrganicMeshGraph.cs, StalbergQuadKernel.cs, OrganicQuadMesh.cs, OrganicDualOffsetLattice.cs, DualGridCraftHost.cs, WorldgenCraft.cs, WorldgenCraft.tscn

**LIVE:** `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/`

## 4. Cell roster

- `module` — sole lane this wave
