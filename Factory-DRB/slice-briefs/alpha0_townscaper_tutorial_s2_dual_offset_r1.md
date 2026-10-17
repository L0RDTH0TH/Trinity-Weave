---
slice_id: alpha0_townscaper_tutorial_s2_dual_offset_r1
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
attempt: 2
producer_run_id: sp-s2dual2-35fcaa
pillar_packet_hash: 88b8162c869ec038
composed_at: 2026-10-03T05:56:59Z
---

# Slice Implementation Brief — Tutorial s2 attempt2 — unique dual half-offset + DualCellsTouching update-four

## 1. Product goal (UX)

**North star (L5):**
Tutorial s2 attempt 2: unique dual half-offset quads with four explicit occupancy corner reads; DualCellsTouching update-four; dual overlay + toggle; keep s1; graybox; refuse markers-only dual.

**Dispatch depth L1 bar:**
- **UX-1:** Dual cells are UNIQUE HALF-STEP OFFSET quads (not hex tiles; not 19×4 marker spray).
- **UX-2:** Each dual cell reads FOUR explicit occupancy corners (CornerAxialOffsets).
- **UX-3:** UPDATE-FOUR via DualCellsTouching — one occupancy edit refreshes exactly four dual cells.
- **UX-4:** Dual overlay DISPLAY + independent dual TOGGLE (D); occupancy G kept; Shift+G paired OK.
- **UX-5:** Inherit s1 — hex-19 lattice graph + cell ghost + LMB/RMB + no cam yank.
- **UX-6:** Graybox TileFamilyIndex 0–5 only; no connectors/art/Terrain3D/s3–s6.


### UX bullets
- **UX-1:** **UX-1:** Dual cells are UNIQUE HALF-STEP OFFSET quads (not hex tiles; not 19×4 marker spray).
- **UX-2:** **UX-2:** Each dual cell reads FOUR explicit occupancy corners (CornerAxialOffsets).
- **UX-3:** **UX-3:** UPDATE-FOUR via DualCellsTouching — one occupancy edit refreshes exactly four dual cells.
- **UX-4:** **UX-4:** Dual overlay DISPLAY + independent dual TOGGLE (D); occupancy G kept; Shift+G paired OK.
- **UX-5:** **UX-5:** Inherit s1 — hex-19 lattice graph + cell ghost + LMB/RMB + no cam yank.
- **UX-6:** **UX-6:** Graybox TileFamilyIndex 0–5 only; no connectors/art/Terrain3D/s3–s6.

## 2. Shape lock (Conceptual)

oskar docs/03 dual+corner-state+update-four on hex-19; half-offset quads; not docs/02 sea-grid.

## 3. Realization (Execution)

Unique dual quads half-step offset; each dual spans four occupancy corners; DualCellsTouching returns exactly four duals per occupancy edit; dual overlay toggleable; s1 intact.

## 4. Cell roster

- `module` — crew for system
