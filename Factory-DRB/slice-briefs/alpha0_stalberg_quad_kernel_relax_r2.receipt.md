---
trinity_sha: d3ddf7c5c5eeff8bd82bca69f8720ae70e805f0f
title: Bedtime iterate receipt — alpha0_stalberg_quad_kernel_relax_r2
slice_id: alpha0_stalberg_quad_kernel_relax_r2
ask_id: alpha0_stalberg_quad_kernel
claim_class: staging
factory_greenlit: false
completed: 2026-10-03T08:40:00Z
status: near_parity_zero_relax_base
best_mcp: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/_evidence/stalberg_best_zero_relax_iter4.png
goal_image: Ingest/Final-grid-state.jpg
---

# Receipt — bedtime base-mesh + soft-relax iterate

## Result

- **Parity:** near (zero-relax filled hex all-quad) — not full Townscaper flow.
- **LIVE:** `DefaultRelaxIters=0`, `DefaultRingCount=5`, axial triangulation, injective unique topo, camera LookAt fix, relax force-average ready but held off.
- **MCP used now:** yes, every iteration under `_evidence/stalberg_*`.
- **MCP used for relax_r1 weld:** no (prior audit).

## What was wrong

1. UniqueTopology XOR position hash → long rays after subdivide remesh.  
2. Craft camera pitch clobber after LookAt → false “star” silhouette.  
3. Soft square-relax without force averaging → real star when iters>0.  
4. PlaneToAxial triangulation path retired in favor of axial-keyed seed.

## Out of Success

- Full ask_success / dual / tiles / Terrain3D / tutorial / Curator
