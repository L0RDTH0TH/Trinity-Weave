---
slice_id: alpha0_townscaper_tutorial_s2_dual_offset_r1
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
producer_run_id: sp-s2dual-a-eb9041
pillar_packet_hash: a2f5f947bbbe24b0
composed_at: 2026-10-03T05:39:40Z
---

# Slice Implementation Brief — Tutorial s2 — dual half-offset quads + update-four + dual toggle

## 1. Product goal (UX)

**North star (L5):**
Tutorial s2 dual offset: dual half-offset quads with four-corner occupancy reads; update-four on one occupancy edit; dual overlay display + dual toggle; keep s1 hex-19 lattice graph, ghost, occupancy toggle, LMB/RMB, no cam yank; graybox; no connectors/art/Terrain3D.

**Dispatch depth L1 bar:**
- **UX-1:** Dual cells are HALF-STEP OFFSET quads from the hex-19 occupancy lattice (refuse skip_dual_offset).
- **UX-2:** Each dual cell reads FOUR occupancy corners (corner-typed dual).
- **UX-3:** UPDATE-FOUR — one occupancy paint/clear refreshes the four dual slots that touch that cell/point.
- **UX-4:** Dual overlay DISPLAY visible as graybox structure proof + dual TOGGLE independent of occupancy grid (paired toggle OK too).
- **UX-5:** Inherit s1 — hex-19 lattice graph + cell ghost + occupancy toggle + LMB/RMB under mouse + no cam yank.
- **UX-6:** No connectors, no art Prefer, no Terrain3D, no s3–s6 bundle; graybox only.


### UX bullets
- **UX-1:** **UX-1:** Dual cells are HALF-STEP OFFSET quads from the hex-19 occupancy lattice (refuse skip_dual_offset).
- **UX-2:** **UX-2:** Each dual cell reads FOUR occupancy corners (corner-typed dual).
- **UX-3:** **UX-3:** UPDATE-FOUR — one occupancy paint/clear refreshes the four dual slots that touch that cell/point.
- **UX-4:** **UX-4:** Dual overlay DISPLAY visible as graybox structure proof + dual TOGGLE independent of occupancy grid (paired toggle OK too).
- **UX-5:** **UX-5:** Inherit s1 — hex-19 lattice graph + cell ghost + occupancy toggle + LMB/RMB under mouse + no cam yank.
- **UX-6:** **UX-6:** No connectors, no art Prefer, no Terrain3D, no s3–s6 bundle; graybox only.

## 2. Shape lock (Conceptual)

Dual grid = copy offset by half a cell; place → update four dual quads; corner typing.

## 3. Realization (Execution)

Dual cells half-step offset from occupancy lattice; each dual cell reads 4 occupancy corners; one occupancy edit refreshes exactly the four dual slots that touch it; dual overlay visible and toggleable independently of occupancy grid; s1 lattice graph intact.

## 4. Cell roster

- `module` — crew for system
