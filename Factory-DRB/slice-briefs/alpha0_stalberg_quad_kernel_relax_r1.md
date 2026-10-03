---
slice_id: alpha0_stalberg_quad_kernel_relax_r1
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
producer_run_id: sp-sqkr-a1f7c2
pillar_packet_hash:
composed_at: 2026-10-03T07:59:01Z
prior_slice_id: alpha0_stalberg_quad_kernel_visual_r1
series_step: 1c
factory_greenlit: false
claim_class: staging
status: failed_altitude_relax_squarify_fail
next_in_chain: alpha0_stalberg_quad_kernel_relax_r2
---

# Slice Implementation Brief — Stålberg quad-kernel relax / squarify algorithm fidelity

## 1. Product goal (UX)

**North star (L5):**
Same Stålberg/Lerg pipeline; F5 = readable irregular **all-quad** planar board after **area-based square relax** on unique shared topology — not noodle spikes from duplicate verts / naïve Laplacian / free-boundary fold / premature extrusion.

**Dispatch depth L1 bar:**
- **UX-1:** Keep seed→tri→dissolve→subdivide→relax→flatten order intact (approach locked).
- **UX-2:** Unique Vertex/Edge/Face topology (position-hashed singletons); re-weld near-duplicates after relax.
- **UX-3:** Area-based square force (ideal side from avg face area → half-diagonal); not naïve Laplacian-only.
- **UX-4:** Small step (0.05–0.15), many iters (50–200), force clamp, boundary pinned.
- **UX-5:** No 3D extrusion / prism display before 2D grid stable; planar board remains primary.
- **UX-6:** Do not claim dual paint / tiles / art / Terrain3D / tutorial Success / ask_success before operator F5.

### UX bullets
- **UX-1:** Pipeline order intact (Lerg/oskar).
- **UX-2:** Unique hashed topology + post-relax weld.
- **UX-3:** Area-based closest-square relax.
- **UX-4:** Soft step / clamp / boundary pin.
- **UX-5:** 2D stable before any extrusion language.
- **UX-6:** Scope = kernel fidelity only.

## 2. Shape lock (Conceptual)

Approach from [[alpha0_stalberg_quad_kernel_r1]] intact. Prior [[alpha0_stalberg_quad_kernel_visual_r1]] fixed planar/opaque render but was **incomplete** on algorithm fidelity. This ticket (**1c**) welded unique topo + area-square relax; Prefer staging OK; **operator F5 failed** → `failed_altitude_relax_squarify_fail`. Authority parked at draft [[alpha0_stalberg_quad_kernel_relax_r2]].

## 3. Realization (Execution)

Position-hashed unique topology DS → merge triangles→quads (unpaired OK) → subdivide to 100% quads → area-based square relax (Variant A closest-square / Lerg squarify) with small step + boundary pin + force clamp → re-weld duplicates → flatten craft plane → opaque planar faces + depth-tested unique edges. No extrusion before 2D stable.

## 4. Prefer input (operator / Grok)

**Video (Sergey Lerg Godot Townscaper recreation):** https://youtu.be/Jm3pLya3d9c  
**Vault cite:** [[Factory-DRB/references/lerg-townscaper-godot/README]]

**Grok core claim:** noodle mess ≈ failed/missing relaxation/squarifying on still-triangular or poorly-merged mesh; OR broken shared topology (non-unique verts → duplicate edges → relax pulls apart → spikes).

**Diagnostic checklist (accept / refuse):**
| Check | Accept | Refuse code |
|-------|--------|-------------|
| Triangles remain after merge+subdivide as final faces? | Final faces 100% quads | `relax_before_quad_only` / leftover tris as Success |
| Vertices unique IDs / hashed by position? | Position-hash singleton | `non_unique_vertices` |
| Force magnitude clamped + small step? | clamp + step ∈ [0.05,0.15] | `relax_step_too_hard` |
| Square force from avg face area (half-diagonal)? | area→side→D | `missing_square_area_force` |
| Naïve Laplacian/centroid only? | closest-square / area square | `naive_laplacian_only` |
| Boundary pinned? | hull/boundary constrained | `free_boundary_fold` |
| Extrusion before 2D relax done? | planar 2D first | `extrusion_before_2d_stable` |

## 5. Cell roster

- `module` — crew for system
