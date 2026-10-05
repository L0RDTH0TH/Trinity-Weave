---
lane_id: module
slice_id: row_ux_world_generation_r1_d4
weld_slice_id: alpha0_worldgen_terrain3d_feed_r3
ask_id: alpha0_worldgen_terrain3d_feed
half_b_overlay: alpha0_worldgen_terrain3d_feed_r3
claim_class: staging
factory_greenlit: true
thin_prefer: true
producer_run_id: sp-prefer-r3-d4
receipt_id: sp-prefer-r3-d4-module
completed_at: 2026-10-01T22:55:00Z
---

# Lane receipt — module (Terrain3D Prefer layer-split r3)

## UX goal (one sentence)

Craft places/removes tiles only with mouse-cursor aim and no cam recenter; craft stays flat Townscaper toys; Terrain3D is a separate fed layer on Sparky enter / explicit F6 — Hot Wheels ≠ car (YT Y19Mw5YsgjI).

## Matrix Dual-grid Prefer / Never (quoted)

- **Prefer:** Terrain3D (or existing Prefer terrain) as world/height authority + stock GridMap as craft cell overlay — one craft cell data authority.
- **Never:** Second parallel terrain or physics authority; custom voxel engine; GridMap as a second height/terrain authority beside Terrain3D; blending Terrain3D height deformation into craft-tile authorship view.

## Step-1 cite

- YT: https://www.youtube.com/watch?v=Y19Mw5YsgjI
- Vault: Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01 · COHESIVE-VISION-ART-DIRECTION · townscaper-click-add-world-element
- Law: craft = Hot Wheels tile authorship; Terrain3D = real car fed under Sparky — do not re-blend layers

## UX bullets

| Id | Proof |
|----|-------|
| UX-1 | `TryPickCell` no longer moves focus; paint does not `SetFocusWorld`; mouse-cursor ray retained — refuse `craft_cam_recenter_on_place`, `camera_center_aim` |
| UX-2 | `SetVisibleForCraftPhase(true)` hides Terrain3D under craft; Paint = GridMap only — refuse `craft_terrain_blend` |
| UX-3 | `FeedTerrainFromCraftMap` on Tab→Sparky; F6 stamp = explicit feed; Tab without G retained — refuse `unfed_terrain_under_sparky`, `sparky_requires_g_seed` |
| UX-4 | Terrain3D ClassDB Prefer host + GridMap overlay; Matrix Dual-grid Prefer/Never quoted; layers not re-blended |

## Hard Prefer gaps closed (operator F5 — only acceptance)

1. No cam recenter — place/remove tiles; camera stays put
2. No craft Terrain3D blend — craft checker/grid not deformed into terrain heights
3. Terrain3D fed layer — Sparky enter and/or explicit F6; Sparky sees Terrain3D from tiles; craft stays toys

Prior wins retained: mouse-cursor aim · Tab sparky without G.

## Ban

- `verify_mcp_only` as Done — operator F5 attest required for ask_success
- Multimesh/graybox-only Success
- Waiving Terrain3D Prefer proof for touch-budget theater
- Re-blending Hot Wheels craft with Terrain3D under craft cam

## Operator F5 checklist

1. LMB place under cursor → tiles only; camera does **not** yank to new tile
2. Craft view stays flat toys (Terrain3D host hidden) — no height deform under craft
3. Tab → sparky feeds Terrain3D from tile map (or after F6 explicit); sees living mesh; **no G required**
4. Graybox GridMap alone without Terrain3D feed under sparky = fail (not Done)

## Files touched

See manifest drops under `Systems/_factory/manifest.yaml`.
