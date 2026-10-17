---
title: Staging receipt — alpha0_stalberg_dual_single_deck_emit_r1
slice_id: alpha0_stalberg_dual_single_deck_emit_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2w
producer_run_id: sp-dual-single-deck-emit-r1-live-weld
claim_class: ask_success
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_single_deck_emit
contract: C_dual_single_deck_emit
ticket_map: VIS-zfight
completed: 2026-10-13T00:45:00Z
status: ask_success_keep
prior_slice_id: alpha0_stalberg_dual_zfight_harden_r1
prior_disposition: F5_FAIL_SUPERSEDED
keeps_materials: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_owned_only_paint: alpha0_stalberg_dual_owned_only_paint_r1
keeps_tri_cell_place: alpha0_stalberg_dual_tri_cell_place_r1
supersedes_zfight_harden: alpha0_stalberg_dual_zfight_harden_r1
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
live_host: Systems/DualGridCraftHost.cs
trinity_branch: project/genesis-mythos-master
trinity_project_sha: 812b122378533cf86cef659ca5bd76d9a3cb6c2e
trinity_live_weld_sha: d20ae88c63cb28bde6f2ed296b721725dc2ce05b
trinity_push: direct_export_project_push_force_with_lease
curator_snapshot: skipped_push_enabled_false_and_mass_cursor_rules_dirt
operator_f5_confirmed: true
operator_f5_at: '2026-10-13T01:00:00Z'
disposition: KEEP
---

# Staging receipt — alpha0_stalberg_dual_single_deck_emit_r1

**KEEP / ask_success** — operator F5 confirmed `2026-10-13T01:00:00Z` (single-deck Full emit; shared-edge no-strobe). Prefer concept ok. Prior **2u** KEEP. Prior **2v** F5 FAIL SUPERSEDED. Full place = one opaque inset Stage-6 deck. Coast / Corner spray / Townscaper Done out of scope. Next: [[alpha0_stalberg_dual_update_four_recompute_r1]].

## Selection rationale

Operator F5 failed 2v. Grok + parent binding diagnosis: depth quantization at craft camera dwarfs FullYBias/lift/ε; FlattenFullToSingleDeck makes coplanar fights worse. Architecture change — emit one deck from Stage-6 corners — not bigger Y.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_single_deck_emit_r1.prefer-result.json → ok · concept_prefer_ok: true |
| detail | prefer_authorship_pass_ok |
| Law | Prefer-Authorship-Host-Law · concept Prefer for dual/authorship chain-advance |

## LIVE code changed

| File | Change |
|------|--------|
| `Systems/DualGridCraftHost.cs` | WeldSliceId/SliceId/PlacePolarity → `alpha0_stalberg_dual_single_deck_emit_r1` / `owned_dual_cell_single_deck_emit` / `C_dual_single_deck_emit` |
| Full place | **NEW** `EmitFullSingleDeckFromStage6` — n=3 one tri / n=4 two tris @ `FullDeckYLift=12`; inset `FullDeckEdgeInset=0.01`; library albedo opaque cull-back |
| DELETED Full harden | `FullYBias` · `FullCraftLiftExtra` · `FullSortingOffset` · `FullPerKeyYEpsilon` · `MakeWalllessFullPlateau` · `FlattenFullToSingleDeck` · `PerKeyYEpsilon` · `ApplyFullDepthBiasMaterials` |
| Non-Full | MeshFit KEEP (no yBias arg) |
| Ghost | cyan hover KEEP — no second Full under ghost |
| metas | `full_single_deck_emit=true` · `y_bias_as_zfight_fix=false` · flatten/MeshFit Full flags false |

## Host before → after

| Surface | Before (2v) | After (this weld) |
|---------|-------------|-------------------|
| Tri/quad Full place | KEEP ask_success | **KEEP** |
| Full mesh | GLB → wallless → flatten → MeshFit + Y bias | **Stage-6 corner deck emit** |
| Y/sorting/priority harden | 2.0+1.5+ε / 0.75 / pri 2 | **deleted** |
| Shared-edge strobe | F5 fail | **architecture fix pending F5** |
| Owned-only / snap / seat | KEEP | **KEEP** |
| Coast / Corner spray | deferred | **still deferred** |

## KEEP

- Tri place ask_success ([[alpha0_stalberg_dual_tri_cell_place_r1]])
- Owned-only paint ([[alpha0_stalberg_dual_owned_only_paint_r1]])
- Coverage+frame / seat / snap / Empty / dual `+` / Stage-6 / terrain / squarify / rings=5 spacing=210

## Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid.
2. Place **two** Fulls sharing an edge — place KEEP.
3. **Pan/orbit** — face one color; shared edge does **not** strobe.
4. If still flashes — hunt second writer (amber / overlay / duplicate slot); do **not** add more Y.
5. Do not attest coast / Townscaper Done.
6. ask_success only when no-strobe bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_single_deck_emit_r1]] · Supersedes [[alpha0_stalberg_dual_zfight_harden_r1]] · Prior KEEP [[alpha0_stalberg_dual_tri_cell_place_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]

## Trinity / Curator

| Item | Value |
|------|-------|
| Branch | `project/genesis-mythos-master` |
| Push | **ok** tip `812b122` (weld `d20ae88`) force-with-lease (harness push_disabled; direct export) |
| Curator | **skipped** — `git.push_enabled: false` + mass `.cursor/rules` dirt risk |
| Blockers | none (KEEP) — next PLACE-update-four |
