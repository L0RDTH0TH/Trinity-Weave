---
title: Staging receipt — alpha0_stalberg_manual_scale_r1
slice_id: alpha0_stalberg_manual_scale_r1
ask_id: alpha0_stalberg_manual_scale
series_id: alpha0_stalberg_grid_kernel_r1
created: 2026-10-03
updated: 2026-10-03
claim_class: staging
prefer_authorship_pass: ok
prior_slice_id: alpha0_stalberg_dual_corner_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
mcp_evidence_before: Factory-DRB/slice-briefs/_evidence/stalberg_manual_scale_before_r5.png
mcp_evidence_after: Factory-DRB/slice-briefs/_evidence/stalberg_manual_scale_after_r2.png
density_lift: deferred_until_pipeline_ask_success
---

# Staging receipt — `alpha0_stalberg_manual_scale_r1`

**claim_class: staging** until operator F5. Prefer authorship **ok**. **No Curator.**

## Manual limit (resolved) — cell count low, world size large

Operator clarification: scale **physical size**, not cell count.

| Metric | Dense era (rings=5) | After (manual) |
|--|--------|-------|
| Seed rings | 5 | **2** (hex-19: 1+6+12 = 19 seed verts) |
| Post-pipeline quads | 328 | **~50–54** (count held; seed RNG) |
| Post-pipeline verts | 359 | **~63–67** (count held; seed RNG) |
| Edge estimate (diag) | 1312 | **216** |
| Cell spacing | 1.15 | **3.0** (~2.6×) |
| Seed hull diameter (≈2·rings·spacing) | ≈11.5 | **≈12.0** |
| Approx face side (post-sub) | ~0.51 | **~1.37** (scales with spacing) |

Sources: [[Grid-Topology-Host-Law]] · `DefaultRingCount=2` · `DefaultSpacing=3.0`. Product density rings **deferred** until pipeline `ask_success`.

## Prefer / weld

| Field | Value |
|-------|--------|
| Prefer | `alpha0_stalberg_manual_scale_r1.prefer-result.json` → ok |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_manual_scale_r1/implicit-intent-bind.json` |
| LIVE | `DefaultRingCount=2`; dual-corner + craft-plane authority still wired |

## Pipeline preserved (not reverted)

- Injective topo + soft relax organic kernel
- Craft pick/paint on OrganicQuadMesh (`TryPickOrganicFace`) — Hex19 not Success
- Dual-corner four-cell (`TryPickOrganicCorner` → `UpdateFourDualSlots`)
- Prefer edges + faces (has_edges / has_faces_or_cells)

## MCP evidence

- Before (dense): `_evidence/stalberg_manual_scale_before_r5.png`
- After rings=2 spacing=1.15 (tiny): `_evidence/stalberg_manual_scale_after_r2.png`
- After rings=2 spacing=3.0 (canonical): `_evidence/stalberg_manual_scale_r1_spacing3.png`

## Operator F5

1. WorldgenCraft — small readable organic board (rings=2).
2. LMB/RMB face paint still organic; corner flip still rebuilds up to four dual cells.
3. Density lift only after Prefer pipeline `ask_success` (raise `DefaultRingCount` toward `ProductDensityRingCount`).

## Related

- Series [[alpha0_stalberg_grid_kernel_r1]] · Dual [[alpha0_stalberg_dual_corner_r1]] · Craft [[alpha0_stalberg_craft_plane_authority_r1]]
