---
lane_id: module
slice_id: row_ux_world_generation_r1_d2
weld_slice_id: alpha0_worldgen_terrain3d_feed_r1
ask_id: alpha0_worldgen_terrain3d_feed
claim_class: staging
factory_greenlit: true
producer_run_id: sp-overnigh-1f9b7c
receipt_id: sp-overnigh-1f9b7c-module
completed_at: 2026-10-01T21:20:00Z
---

# Lane receipt — module (Terrain3D Prefer feed)

## UX goal (one sentence)

Privileged seats stamp `stamp_oasis_desert` into a live Terrain3D mesh under WorldgenCraft so Sparky flies real terrain — not graybox alone.

## Matrix Dual-grid Prefer / Never (quoted)

- **Prefer:** Terrain3D (or existing Prefer terrain) as world/height authority + stock GridMap as craft cell overlay — one craft cell data authority.
- **Never:** Second parallel terrain or physics authority; custom voxel engine; GridMap as a second height/terrain authority beside Terrain3D.

## UX bullets

| Id | Proof |
|----|-------|
| UX-1 | `WorldShellController.Enter` + `VerifyWrongSeatRefuse` — privileged seats arm WorldgenCraft; wrong seat → Unauthorized |
| UX-2 | `StampOasisDesert` → `ApplyStampOasisDesertHeights` → `set_height` + `update_maps` on Terrain3DData |
| UX-3 | Player seat paint/stamp/persist/enter refused Unauthorized |
| UX-4 | `Terrain3DAuthorityHost` under `DualGridCraftHost`; ClassDB Prefer; Multimesh = `graybox_only_world` |
| UX-5 | Tab sparky only after `HasVendorHeightFeed`; consumer-only (no terrain authoring) |

## Prefer proof path

1. Host: `WorldgenCraft/DualGridCraftHost/Terrain3DAuthorityHost/Terrain3D_Prefer`
2. Stamp: F6 `stamp_oasis_desert` pushes height/region into Terrain3D + flush
3. Sparky: consumer-only over that mesh after feed
4. Fail visible: GridMap/Multimesh alone without Terrain3D mesh update → `graybox_only_world`

## Ban

- `verify_mcp_only` as Done — operator F5 attest required for ask_success
- Multimesh-only Success

## Operator F5 checklist

1. F5 play from LaunchShell → WorldgenCraft
2. F6 stamp → confirm Terrain3D mesh updates (checkered Prefer terrain rises)
3. Tab → sparky flies that mesh
4. Without Terrain3D ClassDB / without stamp feed → sparky refuse + FailVisible log

## Files touched

See manifest drops under `Systems/_factory/manifest.yaml`.
