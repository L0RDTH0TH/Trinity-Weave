---
lane_id: module
slice_id: alpha0_townscaper_tutorial_s2_dual_offset_r1
producer_run_id: sp-s2dual2--35fcaa
ux_bullet_ids: ["UX-1", "UX-2", "UX-3", "UX-4", "UX-5", "UX-6"]
prefer_authorship_injected: true
implicit_bind_path: .technical/weave/factory/genesis-mythos-master/alpha0_townscaper_tutorial_s2_dual_offset_r1/implicit-intent-bind.json
---

# Lane Mission — module

## Mission
Deliver your lane contribution for `ux_world_generation` at depth 1.


## Prefer authorship contract (host law — durable; not one-off brief text)

- **Slice:** `alpha0_townscaper_tutorial_s2_dual_offset_r1`
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
- `skip_dual_offset` — s2 dual missing half-step offset quads / four-corner reads / update-four (markers-only dual)


## Implicit-intent bind (entry seat — fail-closed)

**Explicit ask:** Tutorial s2 attempt 2: unique dual half-offset quads with four explicit occupancy corner reads; DualCellsTouching update-four; dual overlay + toggle; keep s1; graybox; refuse markers-only dual.

**Structural Success (binding):** Unique dual quads half-step offset; each dual spans four occupancy corners; DualCellsTouching returns exactly four duals per occupancy edit; dual overlay toggleable; s1 intact.

**Refuse:** `skip_dual_offset`, `markers_only_dual`, `bitmask_equals_townscaper`, `prop_scatter_as_composition`, `colored_props_as_modules`, `bundle_tutorial_steps`, `art_before_mass`, `grammar_regress`, `points_as_grid`, `count_equals_topology`, `explicit_met_implicit_miss`, `craft_cam_recenter_on_place`, `craft_terrain_blend`, `terrain3d_in_scope`, `terrain3d_leak_f5`, `verify_mcp_only`, `inspiration_shape_miss`, `fidelity_miss`, `infinite_rect_as_hex19`

**Inspiration cites:**
- https://www.youtube.com/watch?v=Y19Mw5YsgjI
- 1-Projects/genesis-mythos-master/Factory-DRB/Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI.md
- 1-Projects/genesis-mythos-master/Factory-DRB/Grid-Topology-Host-Law.md
- 1-Projects/genesis-mythos-master/Factory-DRB/Prefer-Authorship-Host-Law.md
- 1-Projects/genesis-mythos-master/Roadmap/User-Story/Inspiration-UX-Feedstock/cards/dual-grid-nested-placetile-world-authorship.md

Meeting the countable proxy without this structural Success → `explicit_met_implicit_miss` / `points_as_grid`.

## UX bullets you own
- **UX-1:** **UX-1:** Dual cells are UNIQUE HALF-STEP OFFSET quads (not hex tiles; not 19×4 marker spray).
- **UX-2:** **UX-2:** Each dual cell reads FOUR explicit occupancy corners (CornerAxialOffsets).
- **UX-3:** **UX-3:** UPDATE-FOUR via DualCellsTouching — one occupancy edit refreshes exactly four dual cells.
- **UX-4:** **UX-4:** Dual overlay DISPLAY + independent dual TOGGLE (D); occupancy G kept; Shift+G paired OK.
- **UX-5:** **UX-5:** Inherit s1 — hex-19 lattice graph + cell ghost + LMB/RMB + no cam yank.
- **UX-6:** **UX-6:** Graybox TileFamilyIndex 0–5 only; no connectors/art/Terrain3D/s3–s6.

## Shape context
See SIB §2 — do not relitigate conceptual lock.

## Realization notes
See SIB §3 — crosswalk acceptance to your UX bullets.

## Done when
- Build passes
- Lane receipt cites UX bullet ids satisfied
- Prefer product seats met (no proxy override)
