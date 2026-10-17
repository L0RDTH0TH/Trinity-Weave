---
slice_id: alpha0_stalberg_quad_kernel_squarify_r1
ask_id: alpha0_stalberg_quad_kernel_squarify
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1h
created: 2026-10-04
updated: 2026-10-04
greenlit_at: 2026-10-04T16:29:00Z
composed_at: 2026-10-04T16:29:00Z
claim_class: staging
factory_greenlit: true
status: greenlit_weld
prior_slice_id: alpha0_stalberg_quad_kernel_relax_r2
kernel_foundation: alpha0_stalberg_topology_base_r1
producer_run_id: sp-sqks-c5720a
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
goal_image: Ingest/single-grid-section.jpg
goal_image_note: Oskar organic all-quad hex patch — flowing square-ish cells, not diamond field
live_write_target: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
worldgen_entry_scene: res://scenes/WorldgenCraft.tscn
prefer_concept_required: true
success_object: organic_all_quad_planar_board
relax_variant: rotate90_average_squarify
replaces_relax_variant: Variant_A_closest_square_atan
trinity_branch: project/genesis-mythos-master
---

# Slice brief — `alpha0_stalberg_quad_kernel_squarify_r1`

**GREENLIGHT WELD** `2026-10-04T16:29:00Z` — replace LIVE Stage 5 **Variant A closest-square** (atan + fixed half-diagonal) with classic **Oskar-style rotate-90 average squarify** so F5 WorldgenCraft reads as an organic all-quad field, not a diamond lattice.

Pipeline order **kept**: seed → tri → dissolve → subdivide → **squarify** → re-weld → flatten. Rings=5, pull≈0.12, iters≈80, spacing=210 unless small retune for stability. Boundary pins + force clamp **kept**.

## Bug / ask (operator)

| LIVE now (wrong look) | Success |
|-----------------------|---------|
| `RelaxTowardSquares` = Variant A closest-square (atan α + square targets) | rotate-90 average squarify |
| Hex seed + closest-square → field of diamonds / rhomb locks | Organic flowing quads (see [[Ingest/single-grid-section.jpg]]) |
| Selling diamond_lock_hex_seed as organic Success | Refuse |

## Prefer concept (required)

**Success algorithm (Stage 5), per quad, each iter:**

1. Vectors **corner ← centre** (rel[i] = vert[i] − centroid).
2. Align each into slot-0 by rotating back `i·90°` (flip coords, invert one axis per ±90°; 180 = negate).
3. **Average** the four aligned vectors → orientation+size signal.
4. Scale average length to area-derived half-diagonal (size discipline; not Laplacian-only).
5. **Rotate forward** 0°/90°/180°/270° → four square targets.
6. Accumulate pull = target − rel per corner; **sum/avg across incident quads**; clamp; step; iterate.

**Refuse:**

| Code | Meaning |
|------|---------|
| `closest_square_as_organic_success` | Keeping atan Variant A sold as organic Success |
| `diamond_lock_hex_seed` | Hex seed + diamond/rhomb field as done |
| `naive_laplacian_only` | Centroid/Laplacian-only relax without square targets |
| `free_boundary_fold` | Missing boundary-edge + hull pins |
| `relax_step_too_hard` | pull outside [0.05,0.15] / no force clamp |
| `relax_before_quad_only` | Relax before 100% quads |
| `missing_square_area_force` | No area→side scale on targets |

Keep prior kernel refuses (non_unique_vertices, extrusion_before_2d_stable, hex_scaffold_as_final_mesh, dual_overlay_as_grid_kernel, skip_dissolve_relax, …).

## Knobs (defaults — retune only if unstable)

| Knob | Value |
|------|-------|
| rings | 5 |
| spacing | 210 |
| relax iters | 80 |
| pull | 0.12 |
| force clamp | `side × 0.25` (side-relative) |
| pins | mesh boundary edges ∪ convex hull |

## Path position

| Leg | Slice | Role |
|-----|-------|------|
| Prior relax | [[alpha0_stalberg_quad_kernel_relax_r1]] / [[alpha0_stalberg_quad_kernel_relax_r2]] | Variant A welded; altitude / diamond look fail |
| Foundation | [[alpha0_stalberg_topology_base_r1]] | Injective topo + soft relax recovered |
| **This** | `alpha0_stalberg_quad_kernel_squarify_r1` | Stage 5 → rotate-90 average |
| Dual track | continues at series 2k+ | unchanged Success object for dual |

## Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Prefer concept ok + LIVE Stage 5 is rotate-90 average squarify; F5 WorldgenCraft organic all-quad hex board vs [[Ingest/single-grid-section.jpg]] (not diamond field); pins/clamp/iters/pull discipline kept; claim_class staging until operator F5 |
| Out of Success | dual paint / MeshLibrary / Terrain3D / Hex19 Success / ask_success from MCP alone |

## Related

- [[alpha0_stalberg_grid_kernel_r1]] · [[oskar-procedure/02-grid-algorithm]] · [[Prefer-Authorship-Host-Law]] · [[Grid-Topology-Host-Law]] · Lerg https://youtu.be/Jm3pLya3d9c
