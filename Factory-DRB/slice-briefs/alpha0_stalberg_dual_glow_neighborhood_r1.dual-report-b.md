---
title: Dual report B — before/after + files — alpha0_stalberg_dual_glow_neighborhood_r1
slice_id: alpha0_stalberg_dual_glow_neighborhood_r1
ask_id: alpha0_stalberg_dual_glow_neighborhood
completed: 2026-10-04T06:47:59Z
---

# Dual report B — before/after + files

## Glow semantics (revised)

| | Before | After |
|--|--------|-------|
| Glow unit | Stage-6 DualCell / neighbor DualCells | **SmallCornerQuad** per incident Face |
| Corners | centroid ring / wrong size | **V, mid(edge), faceCentroid, mid(edge)** |
| Count | 1 or wrong DualCells | edge≈2 / interior≈4 **small** regions |
| Stage-6 wire | centroid–centroid | **kept** |
| Refuse | — | `stage6_union_as_single_glow_tile` |

## LIVE corner model

`OrganicDualOffsetLattice.SmallCornerQuadCorners(V,F)`:
1. Find V in Face.Corners at index i
2. prev = Corners[i-1], next = Corners[i+1]
3. Corners CCW: `V`, `mid(V,next)`, `FaceCentroid3(F)`, `mid(prev,V)`


## Files changed (LIVE)

- `Core/WorldGen/OrganicDualOffsetLattice.cs` — `ExpandDualNeighborKeys` / `DualCellsExpandingFrom`; expand map in Rebuild
- `Systems/DualGridCraftHost.cs` — highlight→expand; prove expand2/expand4; WeldSliceId glow_neighborhood_r1
- `Systems/WorldgenCraft.cs` — HUD GLOW-NBR r1

## Vault ticket

- Brief / armed / receipt / prefer-result / dual-reports A+B
- Hub: series step **2j**; `user-story-state` armed_slice_id
- Evidence: `_evidence/dual_glow_neighborhood_r1_verify_a.png`

## Trinity

`project_bridge_push` → **skipped: cooldown** (last push `2026-10-04T02:07:46Z`, daily budget already used). Branch tip local: `project/genesis-mythos-master`.
