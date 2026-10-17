---
slice_id: alpha0_stalberg_topology_base_r1
catalog_row_id: ux_world_generation
dispatch_depth: 1
target_depth: 1
composed_at: 2026-10-03T08:45:00Z
updated: 2026-10-03T08:50:00Z
prior_slice_id: alpha0_stalberg_quad_kernel_relax_r2
series_step: 1e
factory_greenlit: true
claim_class: staging
status: staged_topology_base_recovered
ask_id: alpha0_stalberg_quad_kernel
series_id: alpha0_stalberg_grid_kernel_r1
goal_image: Ingest/Final-grid-state.jpg
operator_authority: bedtime_autonomy_iterate_to_parity
trinity_branch: project/genesis-mythos-master
live_relax_iters: 40
live_ring_count: 5
---

# Slice Implementation Brief — Stålberg topology base r1 (bedtime loop)

## 0. Why

[[alpha0_stalberg_quad_kernel_relax_r2]] near-zero MCP proved **upstream** star/spike (not relax). Operator bedtime autonomy: iterate ≤5 with MCP screenshots until healthy pre-relax / path to [[Ingest/Final-grid-state.jpg]]. Implicit weld authority for this diagnostic loop. **No Curator.**

## 1. Root cause (fixed)

`UniqueTopology2D` XOR-packed `(qx*A)^(qy*B)` as dictionary key → **antipodal hex verts collided** → welded opposite sides → long diameter edges (= radial star). Failure mode: Grok #4 (index/connectivity) manifesting as #1 (star).

## 2. Fixes landed (LIVE)

| Change | File |
|--------|------|
| Injective `(qx,qy)` cell key (never XOR map key) | `Core/WorldGen/StalbergQuadKernel.cs` `UniqueTopology2D` |
| Axial-keyed seed + `TriangulateHexLatticeFromAxial` (no PlaneToAxial round-trip) | same |
| Mesh-boundary edge pins ∪ hull (`MarkBoundaryPinned(verts, quads)`) | same |
| Soft relax re-enabled after healthy zero-relax hex: iters=40, pull=0.05, force-average + corner rot | same |
| rings=5 (~10 cells across post-subdivide) | same |
| Denim unshaded faces + yellow edges | `OrganicQuadMesh.cs` / `DualGridCraftHost.cs` |
| Taller craft cam for denser board | `Camera/CraftPlanarCamRig.cs` |

## 3. MCP iteration log

| Iter | Change | Evidence | Verdict |
|------|--------|----------|---------|
| 1 | Injective topo key | `_evidence/stalberg_topology_base_r1_i1.png` | Star gone; local quads; silhouette still soft/amoeba (relax was on) |
| 2 | iters=0, rings=5 | `_evidence/stalberg_topology_base_r1_i2.png` | **Healthy pre-relax**: filled hex, longRays=0, quads=316 |
| 3 | soft relax 40 | `_evidence/stalberg_topology_base_r1_i3.png` | Flow OK; hull-only pin → jagged risk |
| 4 | boundary-edge pins + relax 40 | `_evidence/stalberg_topology_base_r1_i4.png` | Clean hex + organic interior; pinned=60 |
| 5 | unshaded denim faces | `_evidence/stalberg_topology_base_r1_i5.png` | Blueprint read closer to goal |

Console (i4/i5 class): `longRays=0` all stages; `topoKey=qxqy`; `relaxIters=40`.

## 4. Disposition

- **claim_class: staging** — Prefer product seats / MCP aid green; **operator F5** still owns ask_success.
- **Honest altitude:** **partial → near parity**. Star/spike upstream fixed. Hex silhouette + local all-quad board recovered. Soft relax adds Townscaper flow without star regression. Full pixel parity vs Final-grid-state still operator F5 (density/flow/palette).
- Morning F5: WorldgenCraft, compare to Final-grid-state; if hex+flow OK, GREENLIGHT WELD / ask_success path; else tune merge rate / relax iters only (do **not** revert injective topo key).

## Related

- [[alpha0_stalberg_quad_kernel_relax_r2]] · [[Grid-Topology-Host-Law]] · [[Prefer-Authorship-Host-Law]] · [[alpha0_stalberg_topology_base_r1.receipt]]
