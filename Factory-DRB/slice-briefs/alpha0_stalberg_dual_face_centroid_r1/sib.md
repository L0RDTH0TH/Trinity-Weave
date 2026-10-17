---
slice_id: alpha0_stalberg_dual_face_centroid_r1
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
producer_run_id: sp-fcr1-4205d9
ask_id: alpha0_stalberg_dual_face_centroid
series_id: alpha0_stalberg_grid_kernel_r1
factory_greenlit: true
prefer_authorship: true
prefer_concept_required: true
success_object: dual_offset_cells
intent_invariant: "Player edits logic points (primal Vertices); dual cell around a logic point is the polygon of face centroids of faces incident to that point; dual vertices sit at main-face centres."
composed_at: 2026-10-04T03:24:45Z
compose_path: slice_producer_judgment
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_face_centroid_r1.armed.yaml
lane_roster: [module]
goal_image: Ingest/Final-grid-state.jpg
---

# Slice Implementation Brief — Face-centroid dual r1

## 1. Product goal (UX)

**North star (L5 / project end-state):**
Authorable irregular dual-grid craft plane on organic all-quad board. Dual **vertices** sit at **centroids of primal faces**. Player edits **logic points** (primal Vertices); dual cell around a logic point is the polygon of those face centroids.

**Dispatch depth L1 bar:**
- **UX-1:** Dual Success = `dual_offset_cells` with Stage-6 face-centroid geometry (not vertex-neighbour star / dual_rebind wrong locus).
- **UX-2:** Dual verts at main-face centres; `DualCellsTouching` / `OwnedDualCellKeys` / `UpdateFour*` = ≤4 face-centroid duals sampling V.
- **UX-3:** `IsHalfStepOffset` Hex19 polarity (centre off logic verts); cyan = owned dual tiles only (inset at face centres — not filled primal face block); repeat-click → identical ≤4 keys.
- **UX-4:** Prefer concept ok required: success_object + face-centroid intent invariant; staging Prefer alone does not advance.
- **UX-5:** Preserve organic underlay + MeshGraph + craft-plane authority + rings=2 spacing=3.0.
- **UX-6:** Out of scope: density, Terrain3D, dual_visual art polish, Curator.
- **UX-7:** Goal image [[Ingest/Final-grid-state.jpg]] = graph-family compare, not art parity.

### Conceptual leg (Prefer concept — judgment; not structural-only Success)

| Field | Value |
|-------|--------|
| `project_end_state` | Authorable irregular dual-grid craft plane on organic all-quad board. |
| `end_state` | Authorable irregular dual-grid craft plane — face-centroid dual_offset_cells around logic points; dual_visual later. |
| `path_position` | primal_graph_r1 MeshGraph → dual_rebind aborted (wrong locus) → **this** Stage-6 face-centroid dual → next dual_visual_r3 |
| `success_object` | `dual_offset_cells` |
| `intent_invariant` | Player edits logic points (primal Vertices); dual cell around a logic point is the polygon of face centroids of faces incident to that point; dual vertices sit at main-face centres. |
| `structural_success` | Dual verts at face centroids; DualCellsTouching ≤4 face-centroid duals sampling V; IsHalfStepOffset Hex19; Prefer concept ok |
| `prefer_concept_required` | true |
| `factory_greenlit` | true |
| `goal_image` | Ingest/Final-grid-state.jpg (graph-family) |

**Refuse proxies:** `vertex_neighbor_as_dual_corner` · `dual_rebind_cardinal_wrong_locus` · `dual_centre_on_logic_as_half_step_proof` · `primary_face_as_dual` · `face_block_neighborhood` · `soft_take_4` · `proxy_substitution` · `intent_collapsed_to_mechanics`

## 2. Shape lock (Conceptual)

- success_object = dual_offset_cells (Prefer-aligned; face-centroid in Prefer text)
- Intent invariant exact (quoted above)
- Path: primal_graph → aborted dual_rebind → **this** → dual_visual_r3
- Investigation: [[alpha0_stalberg_dual_geometry_rethink_investigation]]

## 3. Realization (Execution)

| UX | Realization |
|----|-------------|
| UX-1 | Rewrite OrganicDualOffsetLattice — one dual per primal Face; LocalCentre = face centroid |
| UX-2 | DualCellsTouching via corner→dual map (faces sampling V); FaceCornersLocal = inset ring about face centroid |
| UX-3 | IsHalfStepOffset refuses centre-on-logic; ProveFaceCentroidAround; cyan highlight owned keys |
| UX-4 | Prefer concept ok; no staging-only chain-advance |
| UX-5 | Keep rings=2 spacing=3.0 MeshGraph organic craft authority |
| UX-6 | No dual_visual ask_success / density / Terrain3D / Curator |
| UX-7 | HUD + receipt cite goal_image graph-family |

**Zone (module):** OrganicDualOffsetLattice.cs, OrganicMeshGraph.cs, StalbergQuadKernel.cs, OrganicQuadMesh.cs, DualGridCraftHost.cs, WorldgenCraft.cs, WorldgenCraft.tscn

**LIVE:** `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/`

## 4. Cell roster

- `module` — sole lane this wave
