---
title: Dual report B — before/after + files — alpha0_stalberg_dual_secondary_glow_center_r1
slice_id: alpha0_stalberg_dual_secondary_glow_center_r1
ask_id: alpha0_stalberg_dual_secondary_glow_center
completed: 2026-10-04T07:15:00Z
---

# Dual report B — before/after + files

## Pick / glow semantics

| | Before | After |
|--|--------|-------|
| Pick | nearest primary V | nearest secondary face centroid |
| Glow API | `SmallCornerQuadsAround(V)` | `SmallCornerQuadsAroundFace(F)` |
| Visual center | amber primary | coral/cyan secondary |
| Encoder | `Vector2I(V, 1)` | `Vector2I(F, 2)` |
| Stage-6 wire | kept | **kept** |
| Small-corner units | kept | **kept** |
| Refuse | — | `primary_star_glow_as_success` |

## LIVE model

`OrganicDualOffsetLattice.SmallCornerQuadsAroundFace(faceId)`:
1. Index small corner quads by FaceId during Rebuild
2. Editable secondary = faces with 3..4 incident small quads
3. Pick snaps to `FaceCentroid2(F)`; glow highlights those quads

## Files changed (LIVE)

- `Core/WorldGen/OrganicDualOffsetLattice.cs` — by-face index; `SmallCornerQuadsAroundFace`; editable secondary faces
- `Systems/DualGridCraftHost.cs` — `TryPickOrganicSecondary`; `FlipOrganicSecondary`; `HighlightSecondaryDualCells`; UpdateFour Y=2; WeldSliceId secondary_glow_center_r1
- `Systems/WorldgenCraft.cs` — HUD SEC-GLOW r1; PreferAskId/WeldSliceId

## Vault ticket

- Brief / armed / receipt / prefer-result / dual-reports A+B / producer-receipt
- Hub: series step **2k**; `user-story-state` + `factory-project` armed_slice_id
- Bind: `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_secondary_glow_center_r1/`

## Trinity / Curator

- `project_bridge_push` → **skipped: push_disabled** (`branch=project/genesis-mythos-master`)
- `curator_snapshot` → local commit `auto: … dual secondary glow center r1` (push skipped; `git.push_enabled false`)
