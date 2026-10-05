---
title: Staging receipt — alpha0_stalberg_dual_owned_cell_place_r1
slice_id: alpha0_stalberg_dual_owned_cell_place_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2r
producer_run_id: sp-dual-owned-cell-place-r1-greenlight-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_place
contract: C_owned_dual_cell_place_polarity
completed: 2026-10-04T23:17:21Z
status: greenlit_weld_live_staging_awaiting_f5
prior_slice_id: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap: alpha0_stalberg_dual_primary_vertex_place_r1
supersedes_paint_polarity: alpha0_stalberg_dual_primary_vertex_place_r1
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
trinity_branch: project/genesis-mythos-master
trinity_project_sha: dee60f58ea521217c8e71e166915839bad146dc8
trinity_main_sha: e012eddf65e7d61a2db995445757acb4af781ccf
trinity_push: direct_export_project_push_force_with_lease
curator_snapshot: skipped_unsafe_mass_cursor_rules_deletes
---

# Staging receipt — alpha0_stalberg_dual_owned_cell_place_r1

**GREENLIGHT WELD LIVE** landed. Prefer concept ok (`dual_cell_meshlibrary_placement`, place polarity owned DualCell). Snap KEEP from [[alpha0_stalberg_dual_primary_vertex_place_r1]]; paint polarity SUPERSEDED. Occupancy includes owner V; UpdateFour = DualCellsTouching. **claim_class: staging** until operator F5. **No ask_success** from MCP. Valence-5 stays non-placeable.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_owned_cell_place_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law § C.1c |

## Host before → after

| Surface | Before (primary_vertex_place paint) | After (this weld) |
|---------|-------------------------------------|-------------------|
| Occupancy for DualCell(V) | `CornerLogicIndices` = CardinalNeighbors(V) only — **owner excluded** | `[Owner V, n0, n1, n2]` CCW dual-edge / Stage6CornersLocal-aligned — **only-V-on → Corner** |
| UpdateFour (PrimaryPickY) | `DualCellsExpandingFrom(V)` expand-only (owned excluded) | **`DualCellsTouching(V)`** owned-first + expand; cap = MaxDualsPerLogicPoint; hard refuse over (no soft Take) |
| Ghost | `TryGetOwned` / OwnedDualCell(V) | same KEEP |
| Paint seat | Neighbor DualCells lit (wrong wedges) | **OwnedDualCell(V)** / Stage6CornersLocal(V) — ghost = paint |
| HighlightOwnedDualCells | SmallCornerQuad keys (missed MeshLibrary seats) | **DualCell keys** via TryGetOwned |
| Snap / Empty / dual `+` | primary-V snap; Empty skip; plus markers | **KEEP** |
| Valence-5 | non-editable (2..4 SmallCornerQuads) | **KEEP** non-placeable |

## KEEP

- Primary-V snap polarity ([[alpha0_stalberg_dual_primary_vertex_place_r1]])
- Terrain sixpack GLBs/materials for non-Empty families
- Stage-6 DualCell geometry · edge-frame yaw / mesh_fit whole DualCell(V)
- Squarify Stage 5 · rings=5 spacing=210
- Empty skip ocean · dual debug plus (no DualCellEdges)
- Seed showcase face-corner silhouettes = demo only (place proof = owned DualCell)

## Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Cursor near orange star → snap primary V; ghost = OwnedDualCell(V).
3. LMB → MeshLibrary lands on **same OwnedDualCell(V)** as ghost (not neighbor wedges).
4. Only-V-on → Corner (single-bit family) on that owned cell.
5. Free DualCells show amber grid — no ocean Empty carpet; dual `+` at face centres.
6. Valence-5 verts remain non-editable.
7. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_owned_cell_place_r1]] · Prior snap [[alpha0_stalberg_dual_primary_vertex_place_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]

## Trinity / Grok

| Branch | SHA |
|--------|-----|
| project/genesis-mythos-master | dee60f58ea521217c8e71e166915839bad146dc8 |
| main | f07d4b0f3af5fa3760d6ab08232ab0bc0559d55c |

Direct export push with `--force-with-lease` (orphan project tip; vault git.push_enabled left false). Curator snapshot **skipped** — vault dirty with unrelated mass `.cursor/rules` deletes (rsync --delete unsafe).

## Blockers

- Operator F5 attest required for `ask_success` (staging only until then).
- Curator skipped (mass `.cursor/rules` deletes).
- Vault `git.push_enabled: false`.
