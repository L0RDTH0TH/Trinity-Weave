---
slice_id: alpha0_stalberg_dual_rebind_r1
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
producer_run_id: sp-drr1-3b82e5
ask_id: alpha0_stalberg_dual_rebind
series_id: alpha0_stalberg_grid_kernel_r1
factory_greenlit: true
prefer_authorship: true
prefer_concept_required: true
success_object: dual_offset_cells
intent_invariant: "Player edits logic points; dual cells are the half-offset quads whose corners are those shared Vertex refs — cardinal (N/E/S/W) around the point, never a primary-face 2×2 block."
composed_at: 2026-10-04T02:36:28Z
compose_path: slice_producer_judgment
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_rebind_r1.armed.yaml
lane_roster: [module]
---

# Slice Implementation Brief — Dual incidence rebind r1

## 1. Product goal (UX)

**North star (L5 / project end-state):**
Authorable irregular dual-grid craft plane on organic all-quad board. Player edits **logic points**; dual cells are the half-offset quads whose corners are those **shared Vertex refs**.

**Dispatch depth L1 bar:**
- **UX-1:** Dual Success = `dual_offset_cells` via MeshGraph incidence only (not face-scan / SupportFaceIndex / soft Take(4)).
- **UX-2:** `DualCellsTouching` / `OwnedDualCellKeys` / `UpdateFour*` resolve via `Vertex.Faces` / `DualCell.CornerVertices`; corners = MeshGraph Vertex singletons.
- **UX-3:** Valence>4 residue must not break editable or neighbor sets; cyan = owned dual cells only; repeat-click → identical ≤4 dual keys.
- **UX-4:** Prefer concept ok required: success_object + intent invariant; staging Prefer alone does not advance.
- **UX-5:** Preserve organic underlay + MeshGraph + craft-plane authority + rings=2 spacing=3.0.
- **UX-6:** Out of scope: density, Terrain3D, dual_visual art polish, Curator.

### Conceptual leg (Prefer concept — judgment; not structural-only Success)

| Field | Value |
|-------|--------|
| `project_end_state` | Authorable irregular dual-grid craft plane on organic all-quad board. |
| `end_state` | Authorable irregular dual-grid craft plane — dual ownership on MeshGraph incidence; click logic point → stable ≤4 dual_offset_cells; dual_visual later. |
| `path_position` | primal_graph_r1 (MeshGraph landed, F5 neighbor still wrong) → this dual rebind incidence-only → next dual_visual_r3 |
| `success_object` | `dual_offset_cells` |
| `intent_invariant` | Player edits logic points; dual cells are the half-offset quads whose corners are those shared Vertex refs — cardinal (N/E/S/W) around the point, never a primary-face 2×2 block. |
| `structural_success` | DualCellsTouching/OwnedDualCellKeys/UpdateFour via Vertex.Faces / DualCell.CornerVertices; corners = MeshGraph Vertex singletons; Prefer concept ok |
| `prefer_concept_required` | true |
| `factory_greenlit` | true |

**Refuse proxies:** `primary_face_as_dual` · `face_block_neighborhood` · `face_proxy_dual` · `support_face_index_as_dual_success` · `face_scan_proxy_neighborhood` · `soft_take_4` · `valence_drop_editable` · `proxy_substitution` · `intent_collapsed_to_mechanics`

## 2. Shape lock (Conceptual)

- success_object = dual_offset_cells
- Intent invariant exact (quoted above)
- Path: primal_graph_r1 (MeshGraph landed, F5 neighbor still wrong) → **this** dual rebind incidence-only → dual_visual_r3
- Prior Prefer concept'd MeshGraph + Vertex-corner rebind; neighbor ownership still face-scan cache — this ticket fixes incidence-only dual ownership

## 3. Realization (Execution)

| UX | Realization |
|----|-------------|
| UX-1 | Rebind dual ownership Success to incidence-only dual_offset_cells |
| UX-2 | DualCellsTouching / OwnedDualCellKeys / UpdateFour* via Vertex.Faces / CornerVertices |
| UX-3 | Clear valence>4 residue; cyan = owned ≤4 duals; stable repeat-click |
| UX-4 | Prefer concept ok; no staging-only chain-advance |
| UX-5 | Keep rings=2 spacing=3.0 MeshGraph organic craft authority |
| UX-6 | No dual_visual ask_success / density / Terrain3D / Curator |

**Zone (module):** OrganicDualOffsetLattice.cs, OrganicMeshGraph.cs, StalbergQuadKernel.cs, OrganicQuadMesh.cs, DualGridCraftHost.cs, WorldgenCraft.cs, WorldgenCraft.tscn

**LIVE:** `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/`

## 4. Cell roster

- `module` — sole lane this wave
