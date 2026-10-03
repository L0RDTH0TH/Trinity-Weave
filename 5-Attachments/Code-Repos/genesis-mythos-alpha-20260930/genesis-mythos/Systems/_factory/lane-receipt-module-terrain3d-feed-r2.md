---
lane_id: module
slice_id: row_ux_world_generation_r1_d3
weld_slice_id: alpha0_worldgen_terrain3d_feed_r2
ask_id: alpha0_worldgen_terrain3d_feed
half_b_overlay: alpha0_worldgen_terrain3d_feed_r2
claim_class: staging
factory_greenlit: true
thin_prefer: true
producer_run_id: sp-overnigh-475e8a
receipt_id: sp-overnigh-475e8a-module
completed_at: 2026-10-01T22:10:00Z
---

# Lane receipt — module (Terrain3D Prefer rework r2)

## UX goal (one sentence)

Craft place/stamp rays from the mouse cursor, Tab enters sparky without a G seed, and each place updates Terrain3D so sparky sees living mesh — not camera-center aim, G-gated sparky, or graybox-until-F6.

## Matrix Dual-grid Prefer / Never (quoted)

- **Prefer:** Terrain3D (or existing Prefer terrain) as world/height authority + stock GridMap as craft cell overlay — one craft cell data authority.
- **Never:** Second parallel terrain or physics authority; custom voxel engine; GridMap as a second height/terrain authority beside Terrain3D.

## UX bullets

| Id | Proof |
|----|-------|
| UX-1 | `TryPickCellAtCursor` for LMB place + F6 stamp — refuse `camera_center_aim` focus fallback |
| UX-2 | Tab → `god_mode_sparky` after place/stamp Terrain3D feed; G is optional (`g_seed_required=false`); refuse `sparky_requires_g_seed` |
| UX-3 | `WorldShellController.Paint` → `ApplyPlaceCellHeight` → `set_height` + `update_maps` per module; refuse `f6_only_terrain_feed` / `graybox_only_world` |
| UX-4 | Terrain3D ClassDB Prefer host under DualGridCraftHost + GridMap craft overlay; Multimesh = fail visible |

## Hard Prefer gaps closed (operator F5 — only acceptance)

1. Mouse aim — place/stamp ray from mouse cursor
2. Sparky without G — Tab without G-seed gate
3. Craft → Terrain3D per place — not F6-only

## Ban

- `verify_mcp_only` as Done — operator F5 attest required for ask_success
- Multimesh/graybox-only Success
- Waiving Terrain3D Prefer proof for touch-budget theater

## Operator F5 checklist

1. LMB place under cursor → Terrain3D chunk updates (sparky can see mesh after Tab)
2. F6 stamp under cursor (not camera center)
3. Tab → sparky **without** pressing G first
4. Graybox GridMap alone without Terrain3D update = fail (not Done)

## Files touched

See manifest drops under `Systems/_factory/manifest.yaml`.
