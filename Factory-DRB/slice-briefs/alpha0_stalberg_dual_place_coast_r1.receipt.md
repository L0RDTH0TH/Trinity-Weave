---
title: Staging receipt — alpha0_stalberg_dual_place_coast_r1
slice_id: alpha0_stalberg_dual_place_coast_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2y
producer_run_id: sp-dual-place-coast-r1-live-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_place_coast
contract: C_dual_place_coast
ticket_map: PLACE-coast
completed: 2026-10-15T19:05:00Z
status: f5_fail_superseded_by_coast_strip_water_r1
superseded_by: alpha0_stalberg_dual_coast_strip_water_r1
f5_disposition: FAIL_meshfit_terrain_water_blue_blob
bit_map_disposition: KEEP
prior_slice_id: alpha0_stalberg_dual_update_four_recompute_r1
prior_disposition: KEEP_ask_success_operator_move_on
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_tri_cell_place: alpha0_stalberg_dual_tri_cell_place_r1
keeps_single_deck_emit: alpha0_stalberg_dual_single_deck_emit_r1
keeps_update_four: alpha0_stalberg_dual_update_four_recompute_r1
supersedes_owned_only_coastline_deferral: alpha0_stalberg_dual_owned_only_paint_r1
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
live_host: Systems/DualGridCraftHost.cs
live_lattice: Core/WorldGen/OrganicDualOffsetLattice.cs
trinity_branch: project/genesis-mythos-master
trinity_project_sha: e43bb0979eb027bba6af3ad69ee8acbad9c44d16
trinity_live_weld_sha: 630a2f353c285bcedf17a422cf2b0378d00629a4
trinity_prior_tip: 127a01aa136936a533bc3f7cc3af36fa785b6d3d
trinity_push: direct_export_project_push_force_with_lease
trinity_tip_note: tip_e43bb09; weld_630a2f3; prior_127a01a; 2x_keep_operator_move_on
curator_snapshot: skipped_push_enabled_false_and_mass_cursor_rules_dirt
---

# Staging receipt — alpha0_stalberg_dual_place_coast_r1

**F5 FAIL / SUPERSEDED** by [[alpha0_stalberg_dual_coast_strip_water_r1]] (`2z`). Bit map / UpdateFour / Empty / Full single-deck **KEEP**. MeshFit Terrain_Water continuous blue blob **SUPERSEDED** (do not paper over inside 2y). Original LIVE WELD `2026-10-15T19:05:00Z`. Active Prefer = **2z** strip-water — do not F5 this receipt again.

## Selection rationale

Map §0 after PLACE-update-four (2x operator move-on): next Prefer brush step is `PLACE-coast` (coasts read as coasts). Deliberate Prefer supersede of owned-only coastline Empty deferral. Not WORLD-* Session 0.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_place_coast_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law · Townscaper corner→MeshLibrary coast grammar |

## LIVE code changed

| File | Change |
|------|--------|
| `Systems/DualGridCraftHost.cs` | WeldSliceId/PlacePolarity → `alpha0_stalberg_dual_place_coast_r1` / `owned_dual_cell_place_coast` / `C_dual_place_coast` |
| Resolve | owner-on → Full KEEP; owner-off → `MapOccupancyBitsToCoastFamily` (quad 16 + tri 8) |
| Metas / Flip log | `place_coast=true`, `owned_only_coastline_deferred=false` |
| Full emit | single-deck KEEP (no Y-bias/MeshFit Full) |
| UpdateFour | DualCellsSampling KEEP |
| Lattice | unchanged (sampling index KEEP from 2x) |

## Host before → after

| Surface | Before (2x) | After (this weld) |
|---------|-------------|-------------------|
| Neighbor mesh | Empty unless N owner-on | **bits → coast family** |
| Place Full | owned Full | **KEEP** |
| UpdateFour set | owned + DualCellsSampling | **KEEP** |
| Full emit | single-deck | **KEEP** |
| PLACE-coast | deferred | **armed / LIVE** |
| Owned-only coastline deferral | law | **SUPERSEDED** |

## KEEP

- Update-four ask_success ([[alpha0_stalberg_dual_update_four_recompute_r1]] — operator move-on)
- Single-deck emit ask_success ([[alpha0_stalberg_dual_single_deck_emit_r1]])
- Tri place ask_success ([[alpha0_stalberg_dual_tri_cell_place_r1]])
- Coverage+frame / seat / snap / Empty-when-bits-0 / dual `+` / Stage-6 / terrain / squarify / rings=5 spacing=210

## Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid.
2. Place Full on OwnedDualCell(V) — place KEEP.
3. Flip a neighbor point — coast DualCells show Edge/Corner (not Empty skip) where bits warrant.
4. Ghost cyan only; single-deck no-strobe KEEP.
5. Do not attest Townscaper Done.
6. ask_success only when coasts read as coasts — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_place_coast_r1]] · Prior KEEP [[alpha0_stalberg_dual_update_four_recompute_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]

## Trinity / Curator

| Item | Value |
|------|-------|
| Branch | `project/genesis-mythos-master` |
| Push | **ok** tip `e43bb09` (weld `630a2f3`) force-with-lease (prior `127a01a`) |
| Curator | **skipped** — `git.push_enabled: false` + mass `.cursor/rules` dirt risk |
| Blockers | Operator F5 on PLACE-coast bar only (not 2x) |
