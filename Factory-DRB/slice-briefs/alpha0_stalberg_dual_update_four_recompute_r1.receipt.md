---
title: Staging receipt — alpha0_stalberg_dual_update_four_recompute_r1
slice_id: alpha0_stalberg_dual_update_four_recompute_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2x
producer_run_id: sp-dual-update-four-recompute-r1-live-weld
claim_class: ask_success
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_update_four_recompute
contract: C_dual_update_four_recompute
ticket_map: PLACE-update-four
completed: 2026-10-13T01:02:17Z
status: keep_ask_success_operator_move_on
operator_move_on_at: '2026-10-15T19:05:00Z'
next_slice_id: alpha0_stalberg_dual_place_coast_r1
prior_slice_id: alpha0_stalberg_dual_single_deck_emit_r1
prior_disposition: KEEP_ask_success
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_owned_only_paint: alpha0_stalberg_dual_owned_only_paint_r1
keeps_tri_cell_place: alpha0_stalberg_dual_tri_cell_place_r1
keeps_single_deck_emit: alpha0_stalberg_dual_single_deck_emit_r1
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
live_host: Systems/DualGridCraftHost.cs
live_lattice: Core/WorldGen/OrganicDualOffsetLattice.cs
trinity_branch: project/genesis-mythos-master
trinity_project_sha: f4a60462e06d2437cb1d2d4d85dda2a59fb3defb
trinity_live_weld_sha: c1e33d758bb54284700de230a2521e54e29456df
trinity_prior_tip: 812b122378533cf86cef659ca5bd76d9a3cb6c2e
trinity_push: direct_export_project_push_force_with_lease
trinity_tip_note: tip_f4a6046_continue_closed_58ebed74; weld_c1e33d7; PLACE-coast_deferred
curator_snapshot: skipped_push_enabled_false_and_mass_cursor_rules_dirt
continue_audit: '2026-10-15T18:09:05Z resume_after_58ebed74_usage_limit — PLACE-coast skipped; no half-armed junk'
---

# Staging receipt — alpha0_stalberg_dual_update_four_recompute_r1

**KEEP / ask_success** (operator move-on `2026-10-15T19:05:00Z`). LIVE weld landed `2026-10-13T01:02:17Z`. Do **not** re-F5 2x. Next: **2y** [[alpha0_stalberg_dual_place_coast_r1]]. PLACE-update-four DualCellsSampling KEEP.

## Selection rationale

Map §0 after place honesty (2u) + VIS-zfight KEEP (2w): next Prefer ladder craft step is `PLACE-update-four` (shared DualCells that sample the edited point recompute). Not PLACE-coast (would supersede owned-only coastline deferral). Not WORLD-* Session 0 (brush lane not closed).

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_update_four_recompute_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law · Townscaper update-four sample grammar |

## LIVE code changed

| File | Change |
|------|--------|
| `Core/WorldGen/OrganicDualOffsetLattice.cs` | `_samplingDualKeys` from OccupancyCorners; `DualCellsSampling` / `DualCellKeysSampling`; DualCellsTouching = owned + sampling (not CornerVertices star alone) |
| `Systems/DualGridCraftHost.cs` | WeldSliceId/PlacePolarity → `alpha0_stalberg_dual_update_four_recompute_r1` / `owned_dual_cell_update_four_recompute` / `C_dual_update_four_recompute` |
| Flip / UpdateFour | sample set logging; `LastOccupancyBitsSampled`; metas `update_four_sample_recompute` / `occupancy_bits_sampled` |
| Resolve | bits always sampled; owned-only mesh KEEP (no Corner spray) |
| Full emit | single-deck KEEP (no Y-bias/MeshFit Full return) |
| Ghost | cyan hover KEEP — no second Full under ghost |

## Host before → after

| Surface | Before (2w) | After (this weld) |
|---------|-------------|-------------------|
| UpdateFour set | owned + CornerVertices expand | **owned + DualCellsSampling** |
| Bit sampling | `_ = bits` discarded | **LastOccupancyBitsSampled + meta** |
| Neighbor mesh | Empty unless N owner-on | **KEEP** (not Corner spray) |
| Full / place | single-deck + tri/quad | **KEEP** |
| PLACE-coast | deferred | **still deferred** |

## KEEP

- Single-deck emit ask_success ([[alpha0_stalberg_dual_single_deck_emit_r1]])
- Tri place ask_success ([[alpha0_stalberg_dual_tri_cell_place_r1]])
- Owned-only paint ([[alpha0_stalberg_dual_owned_only_paint_r1]])
- Coverage+frame / seat / snap / Empty / dual `+` / Stage-6 / terrain / squarify / rings=5 spacing=210

## Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid.
2. Place Full on OwnedDualCell(V) — place KEEP.
3. Flip a neighbor point that samples that DualCell — refresh without Corner spray arms.
4. Ghost cyan only; single-deck no-strobe KEEP.
5. Do not attest PLACE-coast / Townscaper Done.
6. ask_success only when sample recompute bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_update_four_recompute_r1]] · Prior KEEP [[alpha0_stalberg_dual_single_deck_emit_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]

## Trinity / Curator

| Item | Value |
|------|-------|
| Branch | `project/genesis-mythos-master` |
| Push | **ok** tip `f4a6046` (weld `c1e33d7`) force-with-lease (harness push_disabled; direct export) |
| Curator | **skipped** — `git.push_enabled: false` + mass `.cursor/rules` dirt risk |
| Blockers | Operator F5 on PLACE-update-four sample recompute bar |
| Continue | 2026-10-15 — closed 58ebed74 mid-push; PLACE-coast deferred |
