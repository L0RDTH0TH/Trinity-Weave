---
title: Staging receipt — alpha0_stalberg_dual_whole_cell_orient_r1
slice_id: alpha0_stalberg_dual_whole_cell_orient_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2s
producer_run_id: sp-dual-whole-cell-orient-r1-greenlight-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_whole_cell_edge_frame
contract: C_dual_whole_cell_edge_frame
completed: 2026-10-04T23:36:26Z
status: greenlit_weld_live_staging_awaiting_f5
prior_slice_id: alpha0_stalberg_dual_owned_cell_place_r1
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat: alpha0_stalberg_dual_owned_cell_place_r1
supersedes_coverage_orient: alpha0_stalberg_dual_owned_cell_place_r1
supersedes_incomplete_yaw: alpha0_stalberg_dual_cell_lookup_yaw_r1
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
trinity_branch: project/genesis-mythos-master
trinity_project_sha: c3e06736548150eaa497cf4265ad063a75884573
trinity_main_sha: f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c
trinity_push: direct_export_project_push_force_with_lease
curator_snapshot: skipped_unsafe_mass_cursor_rules_deletes
---

# Staging receipt — alpha0_stalberg_dual_whole_cell_orient_r1

**GREENLIGHT WELD LIVE** landed. Prefer concept ok (`dual_cell_meshlibrary_placement`, whole DualCell + dual-edge frame). Seat KEEP from [[alpha0_stalberg_dual_owned_cell_place_r1]]; coverage+orient SUPERSEDED. Incomplete yaw of [[alpha0_stalberg_dual_cell_lookup_yaw_r1]] SUPERSEDED. OccupancyCorners ↔ Stage6 DualCorners; owner-on → Full whole DualCell; MeshFitToDualEdgeFrame edge0=c0→c1. **claim_class: staging** until operator F5. **No ask_success** from MCP. Valence-5 stays non-placeable.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_whole_cell_orient_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law § C.1c |

## Host before → after

| Surface | Before (owned_cell_place) | After (this weld) |
|---------|---------------------------|-------------------|
| Occupancy ring | `[Owner V, n0, n1, n2]` primary verts | **`OccupancyCorners` = `[n0,n1,n2,n3]` ↔ Stage6 DualCorners** (bit i ↔ c_i) |
| only-V-on family | Corner `0b0001` rot0 → mass at geometry c0 (one pie) | **Full** whole OwnedDualCell(V) — all four pie sectors |
| Frame / yaw | meta `dual_edge_frame_yaw=true` but `mi.Rotation=0`; AABB(X,Z)→bilinear | **MeshFitToDualEdgeFrame** — authored UV → edge0=c0→c1; honest `dual_edge_frame_yaw_rad` |
| Seat / UpdateFour | ghost=paint OwnedDualCell; DualCellsTouching | **KEEP** |
| Snap / Empty / dual `+` | primary-V; Empty skip; plus markers | **KEEP** |
| Valence-5 | non-editable | **KEEP** |

## KEEP

- Seat polarity ([[alpha0_stalberg_dual_owned_cell_place_r1]]) — ghost=paint; UpdateFour=DualCellsTouching
- Primary-V snap ([[alpha0_stalberg_dual_primary_vertex_place_r1]])
- Terrain sixpack GLBs/materials
- Stage-6 DualCell geometry · squarify Stage 5 · rings=5 spacing=210
- Empty skip ocean · dual debug plus (no DualCellEdges)

## Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Cursor near orange star → snap primary V; ghost = OwnedDualCell(V).
3. LMB → **Full** covers **whole** OwnedDualCell(V) (all four secondary pie sectors — not one Corner wedge).
4. Neighbor DualCells may show Corner/Edge coastline; modules follow DualCell edges (edge0=c0→c1).
5. Free DualCells show amber grid — no ocean Empty carpet; dual `+` at face centres.
6. Valence-5 verts remain non-editable.
7. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_whole_cell_orient_r1]] · Seat [[alpha0_stalberg_dual_owned_cell_place_r1]] · Snap [[alpha0_stalberg_dual_primary_vertex_place_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]

## Trinity / Grok

| Branch | SHA |
|--------|-----|
| project/genesis-mythos-master | c3e06736548150eaa497cf4265ad063a75884573 |
| main | f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c |

Project bridge sync (`adb3607`) + receipt self-tip push (`c3e0673`) on `project/genesis-mythos-master`. Vault `git.push_enabled` remains false; curator snapshot **skipped** — vault dirty with unrelated mass `.cursor/rules` deletes (rsync --delete unsafe).

## Blockers

- Operator F5 attest required for `ask_success` (staging only until then).
- Curator skipped (mass `.cursor/rules` deletes).
- Vault `git.push_enabled: false`.
