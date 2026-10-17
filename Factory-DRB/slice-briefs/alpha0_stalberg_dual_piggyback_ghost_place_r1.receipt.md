---
title: SUPERSEDED — piggyback ghost place (place thrash; never KEEP)
slice_id: alpha0_stalberg_dual_piggyback_ghost_place_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
claim_class: staging
factory_greenlit: false
live_weld_landed: false
completed: 2026-10-16T08:05:00Z
superseded_at: 2026-10-16T21:12:37Z
status: superseded_parked_never_keep
disposition: SUPERSEDED
parked: true
never_keep: true
product_success: false
false_success_stripped: true
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
live_host: Systems/DualGridCraftHost.cs
trinity_branch: project/genesis-mythos-master
trinity_project_sha_thrash_tip: 5baf34971a5e8165ccfc226427909844ae72ed4c
proof_tag: piggyback_place_v1
rollback_recovery: alpha0_place_thrash_rollback_r1
rollback_restore_sha: 2675d229a5c50438c58e05dd5a31591de13a2d29
superseded_by: alpha0_stalberg_dual_place_product_r1
---

# SUPERSEDED / PARKED — piggyback ghost place

**Never KEEP. Never product Success.** This receipt documented a LIVE hotfix thrash stack (SeatPolygon / stamp-on / Cull / piggyback ghost→opaque) that collapsed place intent into wording-minimal mechanics.

## Law at thrash tip (historical only — rolled back)

- `UpdateGhost` → `TrySeatPolygon` → `MakeStage6FullFootprintGhost`
- LMB piggyback stamp into `_dualSlots` without `UpdateFour`
- Trinity thrash tip `5baf349` (`piggyback_place_v1`)

## Rollback recovery (2026-10-16)

Surgical restore of place/ghost/SetCellFill path from Trinity **`2675d22`** (GEN-biomes r1 weld tip — FlipOrganicCorner place, no SeatPolygon). GEN/PACK/biome services preserved. See [[alpha0_place_thrash_rollback_r1.receipt]].

**Next Prefer (write only, no weld):** [[alpha0_stalberg_dual_place_product_r1]] — meaning-minimal place product (grey ghost → LMB → permanent opaque Full). `claim_class: staging` until Gate B + operator F5.
