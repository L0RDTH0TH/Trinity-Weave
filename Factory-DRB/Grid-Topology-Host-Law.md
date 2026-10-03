---
title: Grid Topology Host Law — points ≠ grid
created: 2026-10-02
updated: 2026-10-03
project-id: genesis-mythos-master
status: active
constitution_article: V-topology
host_weld_pilot: implementation_factory_loop
tags: [factory, host-law, grid, topology, townscaper, prefer, dual-visual]
canonical_yt: https://www.youtube.com/watch?v=Y19Mw5YsgjI
---

# Grid Topology Host Law

**Binding** for Townscaper / dual-grid / world-authorship Prefer and tutorial steps. Closes the failure mode where “N points” is treated as a grid.

## Thesis

**A point set is not a grid.** In Townscaper / dual-grid language (canonical YT [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] · grammar [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]):

| Element | Role |
|---------|------|
| **Vertices** | Discrete lattice points (may be counted, e.g. hex-19 scaffold) |
| **Edges** | Neighbor connections — make the lattice readable as a **graph** |
| **Faces / cells** | Regions the player paints / ghosts onto |

Markers at coordinates with **no edges and no faces** = `points_as_grid` — **not** Success.

## Durable refuse codes

| Code | Meaning |
|------|---------|
| `points_as_grid` | Markers at coordinates with no edges/faces claimed as grid Success |
| `count_equals_topology` | “N points present” ≠ “lattice of N vertices with cells/edges” |
| `prop_scatter_as_composition` | Distinct mesh ids / colored props claimed as dual composition |
| `bitmask_equals_townscaper` | Corner bitmask alone claimed as Townscaper mass without connectors |
| `skip_dual_offset` | Dual visual layer omitted when Prefer requires dual |
| `infinite_rect_as_hex19` | Unbounded/rect GridMap sold as hex-19 scaffold Success |
| `gray_ramp_only` | Dual cells differ only by gray albedo/alpha on one plate |
| `stretch_as_variant` | Axis elongation / non-uniform Scale / face-warped mesh sold as dual family silhouette |
| `over_neighbor_paint` | Logic-point flip paints more than the ≤4 dual cells that share that corner |
| `unstable_dual_neighborhood` | Same logic point yields different dual-cell ownership sets across repeated clicks |
| `stamp_as_dual` | Independent occupancy / centroid MeshLibrary stamps sold as dual cells owned by shared logic corners |
| `primary_face_as_dual` | OrganicQuadMesh face indices / primary-face 2×2 neighborhood sold as dual Success (no half-step OrganicDualOffsetLattice) |

### Dual-cell neighborhood cardinality

Townscaper dual-corner authorship: flipping one **logic point** (organic vertex) rebuilds **only** the dual cells whose corners include that point — valence ≤4 on an all-quad mesh. Flooding face-adjacency or uncapped incident sets = `over_neighbor_paint`. Soft `Take(4)` after a warn without hard refuse, or centroid stamps instead of corner-owned dual geometry = `unstable_dual_neighborhood` / `stamp_as_dual` (see [[alpha0_stalberg_dual_neighborhood_r1]]). Stable primary-face 2×2 highlight without half-step dual lattice = `primary_face_as_dual` (see [[alpha0_stalberg_dual_lattice_r1]]).

### Dual silhouette ≠ stretch

Family identity (empty / single-edge / L-corner / full) is **discrete geometry** (MeshLibrary item + rot/mirror), not stretching a bar along the organic face’s long axis. Prefer must refuse `stretch_as_variant`. See [[Prefer-Authorship-Host-Law]] § C.1.

## Tutorial scaffold vs product lattice

- **Hex-19** (1+6+12) is a **tutorial scaffold** only — fixed size for ladder steps.
- Product world-authorship ([[dual-grid-nested-placetile-world-authorship]]) uses a **procedural planar graph** in a tunable range — do **not** ossify hex-19 as the product lattice.
- Scaffold still requires **graph topology** (vertices + edges + faces), not a point cloud.
- **Stålberg organic craft plane (2026-10-03):** LIVE keeps **manual / hex-19 cell-count** (`DefaultRingCount = 2`) and enlarges **world spacing** (`DefaultSpacing = 3.0`, was 1.15) so few cells are large/clickable — do **not** raise rings to fill the view. Product density rings (`ProductDensityRingCount = 5`) **deferred until pipeline Prefer `ask_success`** — see [[alpha0_stalberg_manual_scale_r1]]. Still edges+faces; Hex19* types remain not Success.

## Operator visual bar (s1)

Cite diagrams under `Factory-DRB/references/dual-grid-nested/` / Ingest:

- Section cell → [[single-grid-section]] class readability  
- Combined sections → multiple-grid-sections  
- Final assembly → Final-Grid  

F5: you see a **hex lattice of cells**, not floating disks.

## Entry-seat bind (required)

Before `IMPLEMENT_SLICE`, slice-producer / factory entry **must** emit an **implicit-intent bind** artifact that maps colloquial asks (“19 points”, “grid”) to structural Success + these refuse codes. See harness `implicit_intent_bind.py` and [[Prefer-Authorship-Host-Law]] § Entry bind.

## Related

- [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]
- [[dual-grid-nested-placetile-world-authorship]]
- [[Prefer-Authorship-Host-Law]]
- [[alpha0_townscaper_tutorial_r1]]
