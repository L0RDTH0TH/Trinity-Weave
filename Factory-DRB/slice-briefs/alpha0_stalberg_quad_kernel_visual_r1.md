---
slice_id: alpha0_stalberg_quad_kernel_visual_r1
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
producer_run_id: sp-sqkv-29460a
pillar_packet_hash: 
composed_at: 2026-10-03T07:36:06Z
---

# Slice Implementation Brief — Stålberg organic all-quad planar board visual execution fix

## 1. Product goal (UX)

**North star (L5):**
Stålberg organic all-quad VISUAL fix: same pipeline; F5 readable planar irregular quad board; no extruded translucent prism soup / noodle_edge_clutter; regenerable; graybox OK.

**Dispatch depth L1 bar:**
- **UX-1:** Keep seed→tri→dissolve→subdivide→relax pipeline intact.
- **UX-2:** Flatten / constrain vertices to craft plane after relax.
- **UX-3:** Render opaque coherent planar faces (no translucent prism soup).
- **UX-4:** Depth-tested clean quad edge graph (no noodle spaghetti).
- **UX-5:** Regenerate yields a new planar field; graybox OK.
- **UX-6:** Do not claim dual paint / tiles / art / Terrain3D / tutorial Success.


### UX bullets
- **UX-1:** **UX-1:** Keep seed→tri→dissolve→subdivide→relax pipeline intact.
- **UX-2:** **UX-2:** Flatten / constrain vertices to craft plane after relax.
- **UX-3:** **UX-3:** Render opaque coherent planar faces (no translucent prism soup).
- **UX-4:** **UX-4:** Depth-tested clean quad edge graph (no noodle spaghetti).
- **UX-5:** **UX-5:** Regenerate yields a new planar field; graybox OK.
- **UX-6:** **UX-6:** Do not claim dual paint / tiles / art / Terrain3D / tutorial Success.

## 2. Shape lock (Conceptual)

oskar docs/02 pipeline intact; visual execution = planar board + coherent surface.

## 3. Realization (Execution)

Organic all-quad planar lattice graph: vertices + edges + faces (valence-4 quads); seed → triangulate → dissolve → subdivide → relax → flatten to craft plane; render coherent opaque quad surface with depth-tested edge graph; F5 primary = readable planar irregular all-quad field (not noodle/prism soup).

## 4. Cell roster

- `module` — crew for system
