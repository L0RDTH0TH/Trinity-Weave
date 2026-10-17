---
title: Staging receipt — alpha0_stalberg_dual_coast_strip_water_r1
slice_id: alpha0_stalberg_dual_coast_strip_water_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2z
producer_run_id: sp-dual-coast-strip-water-r1-live-weld
claim_class: ask_success
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_place_coast_strip_water
contract: C_dual_coast_strip_water
ticket_map: PLACE-coast-strip-water
completed: 2026-10-15T19:28:20Z
operator_f5_confirmed: true
operator_f5_at: '2026-10-15T19:49:00Z'
disposition: KEEP
status: ask_success_keep
prior_slice_id: alpha0_stalberg_dual_place_coast_r1
prior_disposition: F5_FAIL_SUPERSEDED_meshfit_water__bit_map_KEEP
keeps_place_coast_bits: alpha0_stalberg_dual_place_coast_r1
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_tri_cell_place: alpha0_stalberg_dual_tri_cell_place_r1
keeps_single_deck_emit: alpha0_stalberg_dual_single_deck_emit_r1
keeps_update_four: alpha0_stalberg_dual_update_four_recompute_r1
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
live_host: Systems/DualGridCraftHost.cs
trinity_branch: project/genesis-mythos-master
trinity_project_sha: 895df93cc3036194fc63413417a52102eb7681c0
trinity_live_weld_sha: 3427554508622cc3d73e69ba9a1bbec7a313a74f
trinity_prior_tip: e43bb0979eb027bba6af3ad69ee8acbad9c44d16
trinity_push: direct_export_project_push_force_with_lease
trinity_tip_note: tip_895df93; weld_3427554; prior_e43bb09; 2y_f5_fail_superseded_meshfit_water
curator_snapshot: skipped_push_enabled_false_and_mass_cursor_rules_dirt
---

# Staging receipt — alpha0_stalberg_dual_coast_strip_water_r1

**KEEP / ask_success** — operator accepted (“Fine”) `2026-10-15T19:49:00Z`. Prior **LIVE WELD LANDED** `2026-10-15T19:28:20Z`. Prefer concept ok. Prior **2y** [[alpha0_stalberg_dual_place_coast_r1]] **F5 FAIL / SUPERSEDED** for MeshFit Terrain_Water (bit map / UpdateFour / Empty ClearDualSlot / Full single-deck **KEEP**). MeshFit of Edge/Corner/Diagonal/InverseCorner skips Terrain_Water surfaces; land materials KEEP. `claim_class: staging` until operator F5 on **this** ticket only. **No ask_success** from MCP. Townscaper Done out of scope.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_coast_strip_water_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law · strip water at MeshFit (not GLB reauth) |

## LIVE code changed

| File | Change |
|------|--------|
| `Systems/DualGridCraftHost.cs` | WeldSliceId → `alpha0_stalberg_dual_coast_strip_water_r1`; PlacePolarity / PaintContract strip-water |
| `MeshFitToDualEdgeFrame` | skip `IsTerrainWaterMaterial` surfaces (name Terrain_Water or blue albedo) |
| `IsTerrainWaterMaterial` | new helper |
| Place metas | `coast_strip_terrain_water=true` on non-Full; `blue_water_as_coast_success=false` |
| Full / Empty | EmitFullSingleDeckFromStage6 KEEP; ClearDualSlot KEEP |
| Bits / UpdateFour | MapOccupancyBitsToCoastFamily + DualCellsSampling KEEP |

## Host before → after

| Surface | Before (2y) | After (this weld) |
|---------|-------------|-------------------|
| Coast MeshFit | Terrain_Water included → blue blob | **Terrain_Water stripped** |
| Bit → family | MapOccupancyBitsToCoastFamily | **KEEP** |
| Empty | ClearDualSlot amber | **KEEP** |
| Full owned | single-deck emit | **KEEP** |
| 2y MeshFit water | LIVE fail | **SUPERSEDED** |

## KEEP

- 2y bit map / place_coast family resolve
- Update-four ask_success ([[alpha0_stalberg_dual_update_four_recompute_r1]])
- Single-deck emit ask_success ([[alpha0_stalberg_dual_single_deck_emit_r1]])
- Tri place ask_success ([[alpha0_stalberg_dual_tri_cell_place_r1]])
- Coverage+frame / seat / snap / dual `+` / Stage-6 / terrain / squarify / rings=5 spacing=210

## Operator F5 bar (facts for Layer 0)

1. Scene: `res://scenes/WorldgenCraft.tscn`
2. Pass: coast DualCells = land silhouette without continuous blue water blob
3. Pass: Empty DualCells clear → amber primary grid
4. Fail: continuous blue coast carpet; green stacks on blue
5. Fail: MeshFit Full / Y-bias return / Townscaper Done claim

## Trinity / Curator

| Item | Value |
|------|-------|
| Branch | `project/genesis-mythos-master` |
| Push | **ok** tip `895df93` (weld `3427554`) force-with-lease (prior `e43bb09`) |
| Curator | **skipped** — `git.push_enabled: false` + mass `.cursor/rules` dirt risk |
| Blockers | Operator F5 on strip-water bar only (not re-F5 2y bits) |

## Related

- Brief [[alpha0_stalberg_dual_coast_strip_water_r1]] · Prior SUPERSEDED MeshFit [[alpha0_stalberg_dual_place_coast_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]
