---
title: Recovery receipt — place thrash surgical rollback (no weld / no GREENLIGHT)
slice_id: alpha0_place_thrash_rollback_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
claim_class: staging
factory_greenlit: false
live_weld_greenlit: false
live_weld_landed: false
status: recovery_rollback_complete_awaiting_place_prefer
completed: 2026-10-16T21:12:37Z
disposition: recovery_only
keep: false
ask_success: false
operator_f5_confirmed: false
f5_pass_claimed: false
place_keep_claimed: false
no_weld: true
no_greenlight: true
restore_method: trinity_git_show_surgical_file_restore
restore_from_sha: 2675d229a5c50438c58e05dd5a31591de13a2d29
restore_from_label: GEN-biomes r1 weld tip (FlipOrganicCorner place; pre SeatPolygon/piggyback)
thrash_tip_sha: 5baf34971a5e8165ccfc226427909844ae72ed4c
seat_polygon_weld_sha: 587e8151cd155e49aae41699936b6866f972aab7
pre_seat_sync_sha: d5795a8fa0d7d9ce5024cab39e6eddb07d0cdf62
brush_keep_2z_trinity: 895df93cc3036194fc63413417a52102eb7681c0
brush_keep_2z_live_weld: 34275545
brush_2aa_parked_tip: ce80eb7
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
---

# Place thrash rollback recovery

**Recovery mutation only.** No Prefer greenlight. No new place “fix.” No piggyback v2. No F5 pass claim. No KEEP on place.

## Rolled back (from → to)

| File | From (thrash LIVE / tip) | To |
|------|--------------------------|-----|
| `Systems/DualGridCraftHost.cs` | piggyback tip `5baf349` / LIVE 4467 lines (SeatPolygon + stamp + Cull + piggyback) | Trinity **`2675d22`** (4033 lines) — GEN-biomes tip, FlipOrganicCorner place |
| `Core/WorldGen/OrganicDualOffsetLattice.cs` | `5baf349` 822 lines (`TrySeatPolygon`) | **`2675d22`** 800 lines (no SeatPolygon) |
| `Systems/WorldgenCraft.cs` | piggyback LMB log / `place_stamp_on` metas | FlipOrganicCorner LMB log (RefreshBiomeProbe after place kept) |

Thrash stack supersede start: SeatPolygon weld `587e815` → stamp-persist `3faea2b` → piggyback sync `5baf349`. Early post-GEN toggle / Stage6-ghost amends on `d5795a8` also abandoned by restoring `2675d22`.

## Preserved (not rolled back)

- GEN-tone BiasLandform (+ F5 pass disposition on Prefer)
- PACK organic_seed save/load (+ F5 pass disposition)
- GEN-biomes weld (services + DualGrid biome assign/tint/probe at `2675d22`)
- Salt parks / nursery stubs
- Factory Gate B hostile Prefer requirement (docs)
- Brush KEEP-real **2z** / **2y** / **2x** / **2w** / **2u**; **2aa** parked KEEP LIVE (coast emit law retained in restored host SliceId)
- WorldgenGui / GenBiomeService / PackSaveLoadContract / GenToneContract files untouched

## Honesty

- Do **not** claim place F5 pass or place KEEP after this restore.
- Piggyback receipt [[alpha0_stalberg_dual_piggyback_ghost_place_r1.receipt]] → **SUPERSEDED / parked / never KEEP**.
- Next product work = Prefer [[alpha0_stalberg_dual_place_product_r1]] (`ticket_map_id: PLACE-product`) — write only this session.

## Trinity

Recovery publish (sync only, **not** GREENLIGHT Prefer weld):

| Field | Value |
|-------|--------|
| Branch | `project/genesis-mythos-master` |
| Local tip after sync | `3c49007b5e869fcaa46cd9297dabac55023890a9` |
| Prior thrash tip | `5baf34971a5e8165ccfc226427909844ae72ed4c` |
| Push | **disabled** (`recommendation: push_disabled` / `git.push_enabled` gate) — operator push when ready |
