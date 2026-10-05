---
slice_id: alpha0_stalberg_dual_lattice_r2
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
producer_run_id: sp-tdlr2-a29d70
ask_id: alpha0_stalberg_dual_lattice
series_id: alpha0_stalberg_grid_kernel_r1
factory_greenlit: true
prefer_authorship: true
prefer_concept_required: true
success_object: dual_offset_cells
intent_invariant: "Player edits logic points; dual cells are the half-offset quads whose corners are those points."
composed_at: 2026-10-03T23:57:04Z
compose_path: slice_producer_judgment
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_lattice_r2.armed.yaml
lane_roster: [module]
---

# Slice Implementation Brief — Dual lattice r2 (half-step ownership + Prefer concept)

## 1. Product goal (UX)

**North star (L5 / project end-state):**
Player paints **logic points** on the organic craft plane; the living world ownership graph is the **half-step dual lattice** — `dual_offset_cells` (Varignon / half-offset quads) whose corners are those logic points. Cyan debug / occupancy updates sit on `d_*` dual tiles around a clicked point, never a primary-face 2×2. Dual-visual art and density ride this graph later; craft-plane authority and organic underlay stay.

**Dispatch depth L1 bar:**
- **UX-1:** Player edits logic points; living ownership is dual_offset_cells (half-step dual lattice), not primary faces.
- **UX-2:** Click an interior logic point → cyan/highlight on ≤4 d_* dual tiles whose corners include that point; identical every repeat.
- **UX-3:** Ownership graph = OrganicDualOffsetLattice Varignon/half-offset quads; refuse primary_face_as_dual / stamp_as_dual / proxy_substitution.
- **UX-4:** Prefer concept ok required: success_object dual_offset_cells + intent invariant (object identity); staging Prefer alone does not advance.
- **UX-5:** Preserve organic underlay + craft-plane authority + rings=2 spacing=3.0; regenerable.
- **UX-6:** Out of scope this Prefer: density lift, Terrain3D, dual_visual art, chain-advance without concept Prefer, Curator push.

### UX bullets
- **UX-1:** Player edits logic points; living ownership is dual_offset_cells (half-step dual lattice), not primary faces.
- **UX-2:** Click an interior logic point → cyan/highlight on ≤4 d_* dual tiles whose corners include that point; identical every repeat.
- **UX-3:** Ownership graph = OrganicDualOffsetLattice Varignon/half-offset quads; refuse primary_face_as_dual / stamp_as_dual / proxy_substitution.
- **UX-4:** Prefer concept ok required: success_object dual_offset_cells + intent invariant (object identity); staging Prefer alone does not advance.
- **UX-5:** Preserve organic underlay + craft-plane authority + rings=2 spacing=3.0; regenerable.
- **UX-6:** Out of scope this Prefer: density lift, Terrain3D, dual_visual art, chain-advance without concept Prefer, Curator push.

### Conceptual leg (Prefer concept — judgment; not structural-only Success)

| Field | Value |
|-------|--------|
| `project_end_state` | Player paints logic points on the organic craft plane; living ownership is the half-step dual lattice — dual_offset_cells whose corners are those points. |
| `end_state` | Craft-plane north star: player edits logic points; ownership graph is the half-step dual lattice (dual_offset_cells); dual_visual and density ride this graph later. |
| `path_position` | last green wrong-object = neighborhood r1 primary faces → this = half-step dual lattice ownership → next = dual_visual on correct graph |
| `success_object` | `dual_offset_cells` |
| `intent_invariant` | Player edits logic points; dual cells are the half-offset quads whose corners are those points. |
| `structural_success` | Dual cells are half-offset quads whose corners are logic points the player edits; OwnedDualCellKeys / DualCellsTouching on OrganicDualOffsetLattice; highlight on d_* Varignon tiles; Prefer concept ok (object identity + invariant). |

**Refuse proxies:** `proxy_substitution` · `primary_face_as_dual` · `stamp_as_dual` · `unstable_dual_neighborhood` · `intent_collapsed_to_mechanics` · `over_neighbor_paint` · `skip_dual_offset` · density / Terrain3D / dual_visual art / chain-advance without concept Prefer.

## 2. Shape lock (Conceptual)

- Dual object identity: `success_object = dual_offset_cells` on `OrganicDualOffsetLattice` (half-step offset; keys `d_*`).
- Intent invariant (exact): *Player edits logic points; dual cells are the half-offset quads whose corners are those points.*
- Path: neighborhood r1 primary-face wrong-object → **this** half-step dual ownership → next dual_visual on correct graph (after concept Prefer + F5).
- Supersedes `alpha0_stalberg_dual_lattice_r1` (staging Prefer / symbols-only).

## 3. Realization (Execution)

| UX | Realization crosswalk |
|----|------------------------|
| UX-1 | Weld LIVE `OrganicDualOffsetLattice` as ownership graph; logic-point edits own dual cells. |
| UX-2 | `DualCellsTouching` / `OwnedDualCellKeys` → ≤4 `d_*`; host cyan on dual tiles not primary-face 2×2; stable repeats. |
| UX-3 | Prefer/prove refuse `primary_face_as_dual`, `stamp_as_dual`, `proxy_substitution`; no Hex19 Success. |
| UX-4 | Prefer **concept** ok (object identity + invariant); do not treat staging Prefer / Prefer-symbols alone as chain-advance. |
| UX-5 | Keep organic underlay, `ICraftCellAuthority` on OrganicQuadMesh faces, rings=2 spacing=3.0. |
| UX-6 | No MeshLibrary dual_visual polish, no density lift, no Terrain3D, no Curator this Prefer. |

**Zone (module):** `Core/WorldGen/OrganicDualOffsetLattice.cs`, `StalbergQuadKernel.cs`, `OrganicQuadMesh.cs`, `ICraftCellAuthority.cs`, `Systems/DualGridCraftHost.cs`, `Systems/WorldgenCraft.cs`, `scenes/WorldgenCraft.tscn`.

**LIVE:** `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/`

## 4. Cell roster

- `module` — sole lane this wave (worldgen dual-lattice ownership + host highlight/prove)
