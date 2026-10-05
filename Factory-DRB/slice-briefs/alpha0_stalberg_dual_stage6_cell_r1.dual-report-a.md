---
title: Dual report A — outcome — alpha0_stalberg_dual_stage6_cell_r1
slice_id: alpha0_stalberg_dual_stage6_cell_r1
report: A
role: outcome
completed: 2026-10-04T05:05:00Z
claim_class: staging
---

# Dual report A — outcome

| Field | Value |
|-------|--------|
| LIVE | `OrganicDualOffsetLattice` DualCell = Stage-6 cell-around-V (`d_v_{id}`) |
| Dual verts | `DualCorners` = face centroids; DualLatticeDebug spheres at those loci |
| Dual edges | Stage-6 polygon sides only — centroid–centroid; **no** FaceCornersLocal rings |
| Ownership | `OwnedDualCellKeys(V)` = one cell; `DualCellsTouching` = owned + dual-edge neighbours |
| Paint | `EnsureHalfStepDualCellMesh` uses `Stage6CornersLocal`; multi-hue segments when owner ON |
| Host / HUD | `WeldSliceId=alpha0_stalberg_dual_stage6_cell_r1` · **STAGE6-CELL r1** |
| Compile | `dotnet build` GenesisMythos.csproj — 0 errors |
| Prefer | concept ok — `alpha0_stalberg_dual_stage6_cell_r1.prefer-result.json` |
| Before | DualCell 1:1 Face + FaceCornersLocal inset → cyan overlays amber |
| After | DualCell = Stage6DualCellPolygon(V) → cyan crosses amber main cells |

## Outcome verdict

LIVE dual identity rebound to Stage-6 cell-around-V. Staging until operator F5 attests cyan edges connect face-centroid spheres across main cells (not along amber sides).
