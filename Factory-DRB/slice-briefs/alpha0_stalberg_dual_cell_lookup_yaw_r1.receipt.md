---
title: Staging receipt — alpha0_stalberg_dual_cell_lookup_yaw_r1
slice_id: alpha0_stalberg_dual_cell_lookup_yaw_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2p
producer_run_id: sp-dual-cell-lookup-yaw-r1-greenlight-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
contract: C_dual_cell_lookup_yaw_edge_frame
completed: 2026-10-04T22:10:49Z
status: greenlit_weld_live_staging_awaiting_f5
prior_slice_id: alpha0_stalberg_dual_terrain_tile_r1
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
supersedes_placement: alpha0_stalberg_dual_mesh_fit_r1 / alpha0_stalberg_dual_visual_r3
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
trinity_branch: project/genesis-mythos-master
trinity_project_sha: 9d165add2dd4752b65a1ca4c795b771dae11b113
trinity_main_sha: f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c
trinity_push: direct_export_project_push
curator_snapshot: skipped_unsafe_mass_cursor_rules_deletes
---

# Staging receipt — alpha0_stalberg_dual_cell_lookup_yaw_r1

**GREENLIGHT WELD LIVE** landed. Prefer concept ok (`dual_cell_meshlibrary_placement`). Host populate moved from SmallCornerQuad pies to **Stage-6 DualCell** occupancy lookup + edge-frame warp. Terrain sixpack materials KEEP. **claim_class: staging** until operator F5. **No ask_success** from MCP.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_cell_lookup_yaw_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law § C.1c |

## Host before → after

| Before (broken coalesce) | After (this weld) |
|--------------------------|-------------------|
| Resolve family from primary face bitmask; stamp onto each SmallCornerQuad pie | Lookup on DualCell `CornerLogicIndices` (4 occupancy corners) |
| Whole Edge/Corner/Full GLB bilinear-warped onto 1/4 pie | One MeshLibrary item warped onto whole `Stage6CornersLocal` |
| World/pie-index rot90 as yaw | Rot/mirror in dual-cell edge frame (edge 0 = c0→c1) |
| Secondary flip face-stamped all corner verts | Secondary glow KEEP; populate flips one nearest logic vert |
| UpdateFour = SmallCornerQuadsAround / AroundFace | UpdateFour = `DualCellsExpandingFrom` ≤4 |
| Full with land–land skirts | Full = wall-less plateau (`MakeWalllessFullPlateau`) |

## KEEP

- Terrain sixpack GLBs/materials (`craft_dual_*.glb`)
- Stage-6 wire · secondary glow pick · squarify Stage 5 · rings=5 spacing=210

## Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; overlay off for coastline read.
2. One click logic vert → ≤4 Corner tiles pointing at that vert (small diamond), not face-stamp Full rectangles.
3. Filled cluster → one moss plateau; no brown internal walls between Fulls.
4. Name Empty / Edge / Corner / InverseCorner from coastline without debug overlay.
5. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_cell_lookup_yaw_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]

## Trinity / Grok

| Branch | SHA |
|--------|-----|
| project/genesis-mythos-master | 9d165add2dd4752b65a1ca4c795b771dae11b113 |
| main | f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c |

Direct export push (vault git.push_enabled left false). Curator snapshot **skipped** — vault dirty with unrelated mass `.cursor/rules` deletes (rsync --delete unsafe).
