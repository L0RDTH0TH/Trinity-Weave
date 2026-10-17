---
slice_id: alpha0_stalberg_dual_update_four_recompute_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2x
created: 2026-10-13
updated: 2026-10-15
greenlit_at: '2026-10-13T01:02:00Z'
composed_at: '2026-10-13T01:02:00Z'
claim_class: ask_success
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: keep_ask_success_operator_move_on
operator_move_on_at: '2026-10-15T19:05:00Z'
operator_move_on_note: closed KEEP/ask_success without re-F5; next 2y PLACE-coast
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_single_deck_emit_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat_from: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame_from: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_owned_only_paint_from: alpha0_stalberg_dual_owned_only_paint_r1
keeps_tri_cell_place_from: alpha0_stalberg_dual_tri_cell_place_r1
keeps_single_deck_emit_from: alpha0_stalberg_dual_single_deck_emit_r1
depends_on: alpha0_stalberg_dual_single_deck_emit_r1
keeps_single_deck_emit:
  - alpha0_stalberg_dual_single_deck_emit_r1
keeps_tri_cell_place:
  - alpha0_stalberg_dual_tri_cell_place_r1
keeps_owned_only_paint:
  - alpha0_stalberg_dual_owned_only_paint_r1
keeps_coverage_orient:
  - alpha0_stalberg_dual_whole_cell_orient_r1
keeps_seat_polarity:
  - alpha0_stalberg_dual_owned_cell_place_r1
keeps_snap_polarity:
  - alpha0_stalberg_dual_primary_vertex_place_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_update_four_recompute_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_update_four_recompute
contract: C_dual_update_four_recompute
materials_keep: dual_offset_terrain_tile_sixpack
ticket_map: PLACE-update-four
operator_diagnosis: update_four_was_cornervertices_star__not_occupancy_sample_index__recompute_ok_but_not_prefer_success
---

# Slice brief — `alpha0_stalberg_dual_update_four_recompute_r1`

**KEEP / ask_success** (operator move-on `2026-10-15T19:05:00Z`) — Prefer concept + **PLACE-update-four** sample recompute landed. Do **not** re-F5 this ticket. Next active: **2y** [[alpha0_stalberg_dual_place_coast_r1]]. Prior **2w** / **2u** KEEP.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Map ticket: `PLACE-update-four` in [[World-Builder-Mini-Game-Ticket-Map]]. Single-deck KEEP: [[alpha0_stalberg_dual_single_deck_emit_r1]]. Tri place KEEP: [[alpha0_stalberg_dual_tri_cell_place_r1]]. Owned-only KEEP: [[alpha0_stalberg_dual_owned_only_paint_r1]].

## Why (binding — after 2w KEEP)

| Gate | Prior | Gap |
|------|-------|-----|
| Place honesty | 2u tri/quad Full owned-only | **KEEP** |
| VIS-zfight | 2w single-deck emit | **KEEP / ask_success** |
| UpdateFour set | DualCellsTouching ≈ owned + CornerVertices star | Prefer: shared DualCells that **sample** V via OccupancyCorners |
| Neighbor mesh | owned-only Clear/Empty unless N owner-on | **KEEP** — not Corner spray |
| PLACE-coast | deferred | still deferred |

Townscaper grammar: edit a point → rebuild DualCells that share that point as a corner sample. LIVE Prefer Success for this ticket is that **recompute set + bit sampling honesty**, not neighbor Corner MeshLibrary stamps (`neighbor_corner_spray_as_place` / `update_four_cross_as_success` refused until PLACE-coast).

## Update-four recompute contract (binding)

| Rule | Detail |
|------|--------|
| Refresh set | `DualCellsTouching(V)` = OwnedDualCell(V) + `DualCellsSampling(V)` (OccupancyCorners contain V) |
| Bit honesty | On each recompute, OccupancyCorners bits are sampled (`occupancy_bits_sampled` meta) |
| Place KEEP | LMB → one Full on OwnedDualCell(V) for n=3/n=4; owned-only |
| Neighbor mesh | Sampling DualCells Clear/Empty unless **their own** owner is on |
| Full mesh | Single-deck Stage-6 emit KEEP (no GLB MeshFit/Y-bias harden) |
| Ghost | cyan hover one cell — no second Full under ghost |
| Refuse | `neighbor_corner_spray_as_place` · `update_four_cross_as_success` · `expand_only_paint_as_success` |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_update_four_recompute_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | PLACE-update-four — sample-indexed DualCellsTouching recompute; owned-only mesh KEEP |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_update_four_recompute` |
| Map ticket | `PLACE-update-four` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Flip V → DualCells that sample V recompute (owned + DualCellsSampling) | topology CornerVertices star as sole Success; expand-only paint |
| OccupancyCorners bits sampled on recompute (meta/log) | silent recompute without sample honesty |
| Owned DualCell Full when owner on; neighbors Empty unless N owner-on | `neighbor_corner_spray_as_place` · `update_four_cross_as_success` |
| Tri/quad place + single-deck Full KEEP | reintroduce GLB MeshFit/Y-bias Full harden |
| Ghost cyan one cell; Empty skip; dual `+`; Stage-6; terrain; squarify; rings=5 | ocean carpet · valence-5 editable · Townscaper Done |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** flip editable V → OwnedDualCell Full (KEEP); every DualCell that samples V refreshes (Clear/Empty or Full if that owner on); no Corner spray arms; OccupancyCorners bits sampled; Prefer refuses `neighbor_corner_spray_as_place` / `update_four_cross_as_success` / `expand_only_paint_as_success`; single-deck + tri place + owned-only + snap/seat/Empty/dual+/Stage-6/terrain/squarify/rings=5 KEEP. MCP alone ≠ Success. |
| Out | PLACE-coast Corner/Edge stamps · Townscaper product Done · Terrain3D · MCP-only · reintroduce Y-bias Full harden |

## 4. Refuse (`do_not_waive`)

`neighbor_corner_spray_as_place` · `update_four_cross_as_success` · `expand_only_paint_as_success` · `y_bias_as_zfight_fix` · `seizure_coplanar_deck_as_success` · `silent_ghost_without_place_n3` · `soft_take_4` · `valence_5_editable` · `sector_pie_as_dual_cell_tile` · `verify_mcp_only` · prior dual refuses

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_single_deck_emit_r1]] | **Single-deck Full emit KEEP / ask_success** |
| [[alpha0_stalberg_dual_tri_cell_place_r1]] | Tri place KEEP / ask_success |
| [[alpha0_stalberg_dual_owned_only_paint_r1]] | Owned-only KEEP (no Corner spray as place) |
| [[alpha0_stalberg_dual_whole_cell_orient_r1]] | Coverage+frame KEEP |
| [[alpha0_stalberg_dual_owned_cell_place_r1]] | Seat KEEP |
| [[alpha0_stalberg_dual_primary_vertex_place_r1]] | Snap KEEP |
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. LIVE weld (implementer)

- `OrganicDualOffsetLattice`: index `_samplingDualKeys` from OccupancyCorners; `DualCellsSampling` / `DualCellKeysSampling`; `DualCellsTouching` = owned + sampling (not CornerVertices star alone).
- `DualGridCraftHost`: Flip/UpdateFour walk sample set; `LastOccupancyBitsSampled` + metas `update_four_sample_recompute` / `occupancy_bits_sampled`; owned-only Resolve KEEP; single-deck Full KEEP.
- Prefer concept; arm `factory-project.yaml`; GREENLIGHT WELD LIVE; Trinity `project/genesis-mythos-master`.
- Receipt: `claim_class: staging` until operator F5 on **2x only**.
- Curator skip if mass `.cursor/rules` dirt / `git.push_enabled: false`.

## 7. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Place Full on OwnedDualCell(V) (tri and/or quad) — place KEEP.
3. Flip a **neighbor** editable point that samples that DualCell — owned Full stays; DualCells that sample the flipped point refresh (Clear if their owner off; Full if their owner on). **No** Corner spray arms.
4. Ghost remains cyan hover only (no second Full under ghost).
5. Single-deck no-strobe KEEP; Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP.
6. Attest ask_success only when sample recompute bar met — MCP alone ≠ Success. Do **not** attest PLACE-coast / Townscaper Done.

## Related

- Prior KEEP [[alpha0_stalberg_dual_single_deck_emit_r1]] · Tri [[alpha0_stalberg_dual_tri_cell_place_r1]] · Owned-only [[alpha0_stalberg_dual_owned_only_paint_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_stalberg_grid_kernel_r1]]
