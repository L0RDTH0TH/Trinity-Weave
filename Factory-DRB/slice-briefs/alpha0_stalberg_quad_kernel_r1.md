---
slice_id: alpha0_stalberg_quad_kernel_r1
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
producer_run_id: sp-sqk-3210b7
pillar_packet_hash: 
composed_at: 2026-10-03T07:12:37Z
status: failed_altitude_visual_execution_fail
prior_weld_altitude: failed_altitude_visual_execution_fail
approach_status: intact
next_in_chain: alpha0_stalberg_quad_kernel_visual_r1
factory_greenlit: false
---

# Slice Implementation Brief — Stålberg organic all-quad grid kernel (seed→tri→dissolve→subdivide→relax)

**ALTITUDE FAIL — visual execution (not approach).** Operator F5 = noodle/prism clump. Approach (pipeline) stays. Active Prefer parked at [[alpha0_stalberg_quad_kernel_visual_r1]] (draft). Receipt: [[alpha0_stalberg_quad_kernel_r1.receipt]].

## 1. Product goal (UX)

**North star (L5):**
Stålberg organic all-quad grid kernel: regenerable irregular quad mesh via seed→tri→dissolve→subdivide→relax; graybox OK; no dual paint/tiles/art/Terrain3D.

**Dispatch depth L1 bar:**
- **UX-1:** Seed points from hex-lattice rings (tunable), not fixed hex-19 product lattice.
- **UX-2:** Triangulate seed (hex connectivity or Delaunay).
- **UX-3:** Dissolve triangle pairs into quads (quality bounds OK; leftovers OK).
- **UX-4:** Subdivide every remaining face to 100% quads.
- **UX-5:** Relax vertices toward squareness; irregular organic look.
- **UX-6:** Render quad faces/edges; regenerate yields a new field; graybox OK.


### UX bullets
- **UX-1:** **UX-1:** Seed points from hex-lattice rings (tunable), not fixed hex-19 product lattice.
- **UX-2:** **UX-2:** Triangulate seed (hex connectivity or Delaunay).
- **UX-3:** **UX-3:** Dissolve triangle pairs into quads (quality bounds OK; leftovers OK).
- **UX-4:** **UX-4:** Subdivide every remaining face to 100% quads.
- **UX-5:** **UX-5:** Relax vertices toward squareness; irregular organic look.
- **UX-6:** **UX-6:** Render quad faces/edges; regenerate yields a new field; graybox OK.

## 2. Shape lock (Conceptual)

oskar docs/02 pipeline Variant B hex seed preferred; organic all-quad mesh; not dual-on-hex tutorial.

## 3. Realization (Execution)

Organic all-quad mesh faces (valence 4): seed → triangulate → dissolve triangle pairs into quads → subdivide remaining faces to 100% quads → relax vertices; F5 primary is irregular quads, not hex scaffold lattice or dual overlay on hex.

## 4. Cell roster

- `module` — crew for system
