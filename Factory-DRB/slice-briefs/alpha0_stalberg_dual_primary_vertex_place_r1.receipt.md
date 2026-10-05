---
title: Staging receipt — alpha0_stalberg_dual_primary_vertex_place_r1
slice_id: alpha0_stalberg_dual_primary_vertex_place_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2q
producer_run_id: sp-dual-primary-vertex-place-r1-greenlight-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
place_polarity: primary_vertex_dual_cell_place
contract: C_primary_vertex_dual_cell_place
completed: 2026-10-04T22:52:06Z
status: greenlit_weld_live_staging_awaiting_f5
prior_slice_id: alpha0_stalberg_dual_cell_lookup_yaw_r1
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
supersedes_snap_polarity: alpha0_stalberg_dual_cell_lookup_yaw_r1 / alpha0_stalberg_dual_secondary_glow_center_r1
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
trinity_branch: project/genesis-mythos-master
trinity_project_sha: 901a344494441d6611551d0d517e921be8eceb46
trinity_main_sha: f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c
trinity_push: direct_export_project_push_force_with_lease
curator_snapshot: skipped_unsafe_mass_cursor_rules_deletes
---

# Staging receipt — alpha0_stalberg_dual_primary_vertex_place_r1

**GREENLIGHT WELD LIVE** landed. Prefer concept ok (`dual_cell_meshlibrary_placement`, place polarity primary V). Host snap moved from secondary face-centroid to **primary Vertex V**; Empty MeshLibrary skip (no ocean carpet); dual debug = plus markers (no DualCellEdges). **claim_class: staging** until operator F5. **No ask_success** from MCP. Do **not** F5-attest lookup_yaw under face-pick KEEP.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_primary_vertex_place_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law § C.1c |

## Host before → after

| Before (lookup_yaw face/secondary place) | After (this weld) |
|------------------------------------------|-------------------|
| `TryPickHexCell` → `TryPickOrganicSecondary` (Y=2) then face | `TryPickHexCell` → **`TryPickOrganicCorner` first** (PrimaryPickY) |
| LMB → `FlipOrganicSecondary` / face-adjacent populate | LMB → **`FlipOrganicCorner(V)` only** |
| Empty ocean GLB on every DualCell | **Empty skip** — amber primary grid reads |
| Dual debug: spheres + DualCellEdges ribbons | Dual debug: **`+` at face centres**; **no DualCellEdges** |
| Organic faces hidden / water-tint underlay | Organic amber faces + edges visible |
| Secondary glow as place Success | Secondary glow debug-only; refuse as place target |

## KEEP

- Terrain sixpack GLBs/materials (`craft_dual_*.glb`) for non-Empty families
- Stage-6 DualCell geometry · edge-frame yaw / mesh_fit whole DualCell(V)
- Squarify Stage 5 · rings=5 spacing=210

## Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible (blue env ≠ water tiles).
2. Cursor near orange star / main intersection → snap primary V (not face-centroid cyan).
3. LMB → one terrain module on DualCell(V); not face fill; not neighbor-face stamp.
4. Free DualCells show amber grid — **no ocean Empty carpet**.
5. Dual debug: `+` at face centres; no dual-edge ribbons.
6. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_primary_vertex_place_r1]] · Prior [[alpha0_stalberg_dual_cell_lookup_yaw_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]

## Trinity / Grok

| Branch | SHA |
|--------|-----|
| project/genesis-mythos-master | 901a344494441d6611551d0d517e921be8eceb46 |
| main | f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c |

Direct export push with `--force-with-lease` (orphan project tip; vault git.push_enabled left false). Curator snapshot **skipped** — vault dirty with unrelated mass `.cursor/rules` deletes (rsync --delete unsafe).
