---
title: Staging receipt — alpha0_stalberg_dual_owned_only_paint_r1
slice_id: alpha0_stalberg_dual_owned_only_paint_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2t
producer_run_id: sp-dual-owned-only-paint-r1-live-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_owned_only_paint
contract: C_dual_owned_only_paint
completed: 2026-10-05T00:05:51Z
status: live_weld_landed_staging_awaiting_f5
prior_slice_id: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame: alpha0_stalberg_dual_whole_cell_orient_r1
supersedes_paint_scope: alpha0_stalberg_dual_whole_cell_orient_r1
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
live_host: Systems/DualGridCraftHost.cs
trinity_branch: project/genesis-mythos-master
trinity_project_sha: 39107f54f318caa901e43168842df0ed3ffee7a7
trinity_live_weld_sha: d3439e8f104567399a5da23f6f337afa2b2a0ae9
trinity_main_sha: f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c
trinity_push: direct_export_project_push_force_with_lease
curator_snapshot: skipped_unsafe_mass_cursor_rules_deletes
---

# Staging receipt — alpha0_stalberg_dual_owned_only_paint_r1

**LIVE WELD LANDED** `2026-10-05T00:05:51Z`. Prefer concept ok (prior). Coverage+frame KEEP from [[alpha0_stalberg_dual_whole_cell_orient_r1]]; paint-scope SUPERSEDED. `UpdateFourDualSlots` / `ResolveOrganicDualVisualFamily` now owned-only: Full only when OwnerVertexId on; neighbors ClearDualSlot/Empty; Full Y/depth bias. **claim_class: staging** until operator F5. **No ask_success** from MCP. Valence-5 stays non-placeable.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_owned_only_paint_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law § C.1c |

## LIVE code changed

| File | Change |
|------|--------|
| `Systems/DualGridCraftHost.cs` | WeldSliceId/SliceId/VisualBarCite → `alpha0_stalberg_dual_owned_only_paint_r1`; PlacePolarity / PaintContract metas |
| ResolveOrganicDualVisualFamily | owner-on → Full; owner-off → Empty (bits reserved; coastline deferred) |
| UpdateFourDualSlots | still DualCellsTouching recompute; neighbors Clear via Empty path |
| PlaceStage6DualCellLibraryItem | FullYBias=0.12 + SortingOffset=0.02 + ApplyFullDepthBiasMaterials |
| MakeWalllessFullPlateau | keep top horizontal deck band only (strip lower coplanar decks) |

Lattice (`OrganicDualOffsetLattice.cs`) unchanged — OwnerVertexId / OccupancyCorners / DualCellsTouching KEEP.

## Host before → after

| Surface | Before (whole_cell_orient) | After (this weld) |
|---------|----------------------------|-------------------|
| Place Success | Full owned + neighbor Corner/Edge coastline as Success | **one Full on OwnedDualCell(V) only** |
| UpdateFour DualCellsTouching | refresh owned + stamp Corner on neighbors | recompute OK → **ClearDualSlot/Empty** neighbors unless N owner-on |
| Coverage | Full whole DualCell (all four pies) | **KEEP** |
| Frame / yaw | MeshFitToDualEdgeFrame edge0=c0→c1 | **KEEP** |
| Z-fight | Full + 4 Corner arms coplanar → seizure flash | owned-only removes arms + Full Y/sorting/depth bias + top-deck strip |
| Seat / snap / Empty / dual `+` | KEEP | **KEEP** |
| Valence-5 | non-editable | **KEEP** |

## KEEP

- Coverage+frame ([[alpha0_stalberg_dual_whole_cell_orient_r1]]) — Full whole DualCell; OccupancyCorners↔Stage6; dual-edge frame
- Seat polarity ([[alpha0_stalberg_dual_owned_cell_place_r1]]) — ghost=paint; UpdateFour=DualCellsTouching recompute
- Primary-V snap ([[alpha0_stalberg_dual_primary_vertex_place_r1]])
- Terrain sixpack GLBs/materials
- Stage-6 DualCell geometry · squarify Stage 5 · rings=5 spacing=210
- Empty skip ocean · dual debug plus (no DualCellEdges)

## Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Cursor near orange star → snap primary V; ghost = OwnedDualCell(V).
3. LMB → **one Full** covers whole OwnedDualCell(V) only — **no** 5-stack cross.
4. Neighbor DualCells stay Empty (amber) unless their own owner is on.
5. Pan/orbit — **no** seizure coplanar flicker.
6. Dual-edge frame KEEP; Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP.
7. Valence-5 verts remain non-editable.
8. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_owned_only_paint_r1]] · Prior [[alpha0_stalberg_dual_whole_cell_orient_r1]] · Seat [[alpha0_stalberg_dual_owned_cell_place_r1]] · Snap [[alpha0_stalberg_dual_primary_vertex_place_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]

## Trinity / Grok

| Branch | SHA |
|--------|-----|
| project/genesis-mythos-master | 39107f54f318caa901e43168842df0ed3ffee7a7 |
| main | f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c |

Prior tip `cdde237` was Prefer/ticket-only (LIVE UpdateFour not welded). LIVE weld commit `d3439e8f104567399a5da23f6f337afa2b2a0ae9`; receipt tip on `project/genesis-mythos-master` below. Vault `git.push_enabled` remains false; curator snapshot **skipped** — vault dirty with unrelated mass `.cursor/rules` deletes (rsync --delete unsafe).

## Blockers

- Operator F5 attest required for `ask_success` (staging only until then).
- Curator skipped (mass `.cursor/rules` deletes).
- Vault `git.push_enabled: false`.
- Coastline Corner/Edge on neighbor DualCells **deferred** (not this weld's Success).
