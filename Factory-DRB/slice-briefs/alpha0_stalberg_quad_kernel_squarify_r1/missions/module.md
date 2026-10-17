---
lane: module
slice_id: alpha0_stalberg_quad_kernel_squarify_r1
producer_run_id: sp-sqks-c5720a
---

# Module mission — rotate-90 average squarify

## Weld

Replace `StalbergQuadKernel.RelaxTowardSquares` Variant A (atan closest-square) with Oskar-style rotate-90 average squarify. Called from `Generate` Stage 5. Keep boundary pins, force clamp, area half-diagonal scale, knobs rings=5 / pull=0.12 / iters=80 / spacing=210.

## Algorithm

```
per quad, each iter:
  rel[i] = vert[i] - centroid
  avg = 0.25 * (rel[0] + RotNeg90(rel[1]) + (-rel[2]) + Rot90(rel[3]))
  avg = avg.Normalized() * (side / √2)   # area side from EstimateIdealSideFromArea
  targets = [avg, Rot90(avg), -avg, RotNeg90(avg)]
  force[vi] += target[i] - rel[i]
then: force[vi] /= count[vi]; clamp; vert += force * pull
```

## Refuse seats

- `closest_square_as_organic_success` — atan Variant A remains Success
- `diamond_lock_hex_seed` — diamond/rhomb field sold as organic
- `naive_laplacian_only` — no square targets
- `free_boundary_fold` / `relax_step_too_hard` / `missing_square_area_force`

## Out

Dual paint, MeshLibrary, Terrain3D, Hex19 Success, Curator push enable.
