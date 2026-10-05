---
lane_id: module
slice_id: alpha0_townscaper_tutorial_s1_occupancy_r1
producer_run_id: sp-s1occ-a4506efc
ux_bullet_ids: ["UX-1", "UX-2", "UX-3", "UX-4", "UX-5", "UX-6"]
prefer_authorship_injected: true
implicit_bind_path: .technical/weave/factory/genesis-mythos-master/alpha0_townscaper_tutorial_s1_occupancy_r1/implicit-intent-bind.json
---

# Lane Mission — module

## Mission
Deliver your lane contribution for `ux_world_generation` at depth 1.


## Prefer authorship contract (host law — durable; not one-off brief text)

- **Slice:** `alpha0_townscaper_tutorial_s1_occupancy_r1`
- **YT lock:** https://www.youtube.com/watch?v=Y19Mw5YsgjI
- **Vault cite:** `Ingest/Resources/Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md`
- **Craft** = Hot Wheels tile authorship only (Townscaper dual-grid)
- **Terrain3D** = real car / fed consumer under Sparky (or explicit feed)
- **No** craft-view Terrain3D blend / deform
- **No** camera recenter on place
- **No proxy override:** host_touch_budget / shell seats / bootstrap stubs cannot pass or waive these product Prefer seats

### Durable negative examples (fail closed)
- `craft_cam_recenter_on_place` — Craft place/remove recenters camera / orbit focus onto the new tile
- `craft_terrain_blend` — Craft view deforms checker/grid into Terrain3D heights (Hot Wheels≠car)
- `craft_phase_terrain3d_deform` — Craft phase authors via Terrain3D sculpt instead of tile map
- `unfed_terrain_under_sparky` — Sparky sees graybox-only; Terrain3D not fed as separate consumer layer
- `inspiration_shape_miss` — Prefer collapses Hot Wheels craft into Terrain3D under craft cam
- `points_as_grid` — Markers at coordinates with no edges/faces claimed as grid Success
- `count_equals_topology` — N points present ≠ lattice graph with cells/edges (proxy metric trap)
- `explicit_met_implicit_miss` — Countable ask met while the bound structural Success (edges + faces/cells) is absent


## Implicit-intent bind (entry seat — fail-closed)

**Explicit ask:** Hex-19 lattice graph occupancy for Townscaper tutorial step 1: 19 vertices with neighbor edges and faces/cells, placement ghost snapping to a cell, occupancy lattice toggle, LMB/RMB under mouse, no cam yank, no Terrain3D.

**Structural Success (binding):** Hex-19 lattice graph — 19 vertices plus neighbour edges plus faces/cells. The ghost snaps to a cell; the occupancy lattice toggle shows/hides vertices, edges and faces. Armed token: hex19_lattice_graph__vertices_plus_neighbor_edges_plus_faces_cells

**Refuse:** `points_as_grid`, `count_equals_topology`, `prop_scatter_as_composition`, `bitmask_equals_townscaper`, `skip_dual_offset`, `procedural_only_as_success`, `terrain3d_in_scope`, `boil_the_ocean_df`, `verify_mcp_only`, `bundle_tutorial_steps`, `craft_cam_recenter_on_place`, `craft_terrain_blend`, `terrain3d_leak_f5`, `infinite_rect_as_hex19`, `inspiration_shape_miss`

**Inspiration cites:**
- https://www.youtube.com/watch?v=Y19Mw5YsgjI
- 1-Projects/genesis-mythos-master/Factory-DRB/Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI.md
- 1-Projects/genesis-mythos-master/Factory-DRB/Grid-Topology-Host-Law.md
- 1-Projects/genesis-mythos-master/Factory-DRB/Prefer-Authorship-Host-Law.md
- 1-Projects/genesis-mythos-master/Roadmap/User-Story/Inspiration-UX-Feedstock/cards/dual-grid-nested-placetile-world-authorship.md

Meeting the countable proxy without this structural Success → `explicit_met_implicit_miss` / `points_as_grid`.

## UX bullets you own
- **UX-1:** **UX-1:** Hex-19 lattice GRAPH on the fixed scaffold — 19 vertices + neighbor EDGES + FACES/CELLS. Points alone refuse `points_as_grid` / `count_equals_topology`.
- **UX-2:** **UX-2:** Placement ghost previews the CELL under the cursor before commit (not a lone disk in empty space).
- **UX-3:** **UX-3:** Occupancy lattice toggle shows/hides the lattice (vertices + edges + faces). Dual overlay toggle stubbed/hidden until s2.
- **UX-4:** **UX-4:** LMB add / RMB remove under the MOUSE (ray -> craft plane -> snap to cell). No camera-center aim.
- **UX-5:** **UX-5:** No cam yank — place/remove never recenters the craft camera.
- **UX-6:** **UX-6:** Terrain3D absent or hard-disabled under craft; graybox OK; no dual/connector/art Success.

## Shape context
See SIB §2 — do not relitigate conceptual lock.

## Realization notes
See SIB §3 — crosswalk acceptance to your UX bullets.

## Done when
- Build passes
- Lane receipt cites UX bullet ids satisfied
- Prefer product seats met (no proxy override)
