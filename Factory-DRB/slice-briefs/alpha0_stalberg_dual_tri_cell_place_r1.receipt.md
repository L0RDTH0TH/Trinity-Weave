---
title: Staging receipt — alpha0_stalberg_dual_tri_cell_place_r1
slice_id: alpha0_stalberg_dual_tri_cell_place_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2u
producer_run_id: sp-dual-tri-cell-place-r1-live-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_tri_cell_place
contract: C_dual_tri_cell_place
completed: 2026-10-05T00:35:00Z
status: live_weld_landed_staging_awaiting_f5
prior_slice_id: alpha0_stalberg_dual_owned_only_paint_r1
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_owned_only_paint: alpha0_stalberg_dual_owned_only_paint_r1
supersedes_n3_place_skip: alpha0_stalberg_dual_owned_only_paint_r1
visuals_deferred: zfight_full_ybias_seizure_decks
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
live_host: Systems/DualGridCraftHost.cs
trinity_branch: project/genesis-mythos-master
trinity_project_sha: 20792e0d5a352a94e7b9a954cc08bfed05b8c422
trinity_live_weld_sha: 20792e0d5a352a94e7b9a954cc08bfed05b8c422
trinity_main_sha: f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c
trinity_push: direct_export_project_push_force_with_lease
curator_snapshot: skipped_unsafe_mass_cursor_rules_deletes
---

# Staging receipt — alpha0_stalberg_dual_tri_cell_place_r1

**LIVE WELD LANDED** `2026-10-05T00:35:00Z`. Prefer concept ok. Owned-only KEEP from [[alpha0_stalberg_dual_owned_only_paint_r1]]; **SUPERSEDE** silent n=3 place skip. `EnsureStage6` / Place / MeshFit accept DualCorners **n=3**; `OccupancyCorners` length-3 bit map (no soft_take_4). **Visuals deferred:** Z-fight / FullYBias / seizure decks — not Success this slice. `claim_class: staging` until operator F5. **No ask_success** from MCP. Valence-5 stays non-placeable.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_tri_cell_place_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law · concept Prefer for dual/authorship chain-advance |

## LIVE code changed

| File | Change |
|------|--------|
| `Systems/DualGridCraftHost.cs` | WeldSliceId/SliceId/PlacePolarity → `alpha0_stalberg_dual_tri_cell_place_r1` / `owned_dual_cell_tri_cell_place` / `C_dual_tri_cell_place` |
| EnsureStage6DualCellMesh | accept corners length **3 or 4**; occ length must match |
| PlaceStage6DualCellLibraryItem | n=3/n=4; metas `tri_cell_place`, `vertex_barycentric_warp_to_stage6_triangle` |
| MeshFitToDualEdgeFrame | n=4 bilinear KEEP; n=3 **BarycentricCorner** (fold u+v>1) |
| OrientStage6Targets | n=3 rotate/mirror; n=4 KEEP |
| ResolveOrganicDualVisualFamily | bit sample n=3 or n=4; owner-on → Full KEEP |
| `Core/WorldGen/OrganicDualOffsetLattice.cs` | OccupancyCorners n=3/n=4 path; **no** soft pad to fake 4 |

## Host before → after

| Surface | Before (owned_only_paint) | After (this weld) |
|---------|---------------------------|-------------------|
| Ghost DualCorners==3 | shows (≥3) | **KEEP** |
| Place DualCorners==3 | silent no-op (`corners == 4`) | **one Full** owned-only |
| OccupancyCorners n=3 | Empty (required ==4) | length-3 bit map |
| MeshFit n=3 | blocked | barycentric triangle warp |
| MeshFit n=4 | dual-edge bilinear | **KEEP** |
| Owned-only / snap / seat / Empty / dual `+` | KEEP | **KEEP** |
| Z-fight / seizure | claimed harden | **DEFERRED** (not F5 Success) |
| Valence-5 | non-editable | **KEEP** |

## Tri OccupancyCorners bit map

| Bit | Sample | Geometry |
|-----|--------|----------|
| bit0 | CardinalNeighbors[0] | DualCorners[0] |
| bit1 | CardinalNeighbors[1] | DualCorners[1] |
| bit2 | CardinalNeighbors[2] | DualCorners[2] |

Owner V = centre (not a bit). Resolve: owner-on → Full. No soft_take_4.

## KEEP

- Owned-only paint ([[alpha0_stalberg_dual_owned_only_paint_r1]])
- Coverage+frame for quads ([[alpha0_stalberg_dual_whole_cell_orient_r1]])
- Seat / snap / Empty / dual `+` / Stage-6 / terrain / squarify / rings=5 spacing=210
- Ghost ≥3

## Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid.
2. Snap primary V; find editable V with **triangular** OwnedDualCell (3 DualCorners); ghost outlines it.
3. LMB → **one Full** on that DualCell — ghost and paint agree.
4. Neighbors Empty unless own owner on.
5. Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP.
6. Valence-5 non-editable.
7. **Do not** attest Z-fight / seizure Success (deferred).
8. ask_success only when tri place bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_tri_cell_place_r1]] · Prior [[alpha0_stalberg_dual_owned_only_paint_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]

## Trinity / Curator

| Item | Value |
|------|-------|
| Branch | `project/genesis-mythos-master` |
| Push | direct_export force-with-lease (git.push_enabled false; Curator skipped) |
| Curator | **skipped** — mass `.cursor/rules` deletes (unsafe) |
| Blockers | Operator F5 on tri place; Z-fight deferred to later slice |
