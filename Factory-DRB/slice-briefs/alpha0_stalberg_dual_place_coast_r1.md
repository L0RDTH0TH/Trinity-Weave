---
slice_id: alpha0_stalberg_dual_place_coast_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2y
created: 2026-10-15
updated: 2026-10-15
greenlit_at: '2026-10-15T19:05:00Z'
composed_at: '2026-10-15T19:05:00Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: f5_fail_superseded_by_coast_strip_water_r1
superseded_by: alpha0_stalberg_dual_coast_strip_water_r1
supersede_note: bit_map_KEEP__meshfit_terrain_water_SUPERSEDED
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_update_four_recompute_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat_from: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame_from: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_tri_cell_place_from: alpha0_stalberg_dual_tri_cell_place_r1
keeps_single_deck_emit_from: alpha0_stalberg_dual_single_deck_emit_r1
keeps_update_four_from: alpha0_stalberg_dual_update_four_recompute_r1
supersedes_owned_only_coastline_deferral: alpha0_stalberg_dual_owned_only_paint_r1
depends_on: alpha0_stalberg_dual_update_four_recompute_r1
keeps_update_four:
  - alpha0_stalberg_dual_update_four_recompute_r1
keeps_single_deck_emit:
  - alpha0_stalberg_dual_single_deck_emit_r1
keeps_tri_cell_place:
  - alpha0_stalberg_dual_tri_cell_place_r1
keeps_coverage_orient:
  - alpha0_stalberg_dual_whole_cell_orient_r1
keeps_seat_polarity:
  - alpha0_stalberg_dual_owned_cell_place_r1
keeps_snap_polarity:
  - alpha0_stalberg_dual_primary_vertex_place_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_place_coast_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_place_coast
contract: C_dual_place_coast
materials_keep: dual_offset_terrain_tile_sixpack
ticket_map: PLACE-coast
operator_diagnosis: owned_only_emptied_neighbor_coast__operator_move_on_2x__coasts_must_read_as_coasts
---

# Slice brief — `alpha0_stalberg_dual_place_coast_r1`

**F5 FAIL / SUPERSEDED** by [[alpha0_stalberg_dual_coast_strip_water_r1]] (`2z`) — bit map / UpdateFour / Empty ClearDualSlot / Full single-deck **KEEP**; MeshFit Terrain_Water blue blob **SUPERSEDED**. Original GREENLIGHT WELD LIVE was `2026-10-15T19:05:00Z` PLACE-coast bits→Edge/Corner. Do not F5 this ticket again — active Prefer is **2z** strip-water.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Map ticket: `PLACE-coast` in [[World-Builder-Mini-Game-Ticket-Map]]. Prior KEEP: [[alpha0_stalberg_dual_update_four_recompute_r1]] · [[alpha0_stalberg_dual_single_deck_emit_r1]] · [[alpha0_stalberg_dual_tri_cell_place_r1]]. Coastline deferral SUPERSEDED: [[alpha0_stalberg_dual_owned_only_paint_r1]].

## Selection rationale

Map §0 after PLACE-update-four (2x operator move-on KEEP): next brush Prefer is **`PLACE-coast`** — coasts read as coasts. Deliberate Prefer supersede of owned-only coastline deferral. Not WORLD-* (brush lane still open). Not VIS-read (materials KEEP). Not VIS-library (sixpack already bound).

## Why (binding — after 2x KEEP)

| Gate | Prior | Gap |
|------|-------|-----|
| Place honesty | 2u tri/quad Full owned | **KEEP** |
| VIS-zfight | 2w single-deck emit | **KEEP / ask_success** |
| UpdateFour set | DualCellsSampling OccupancyCorners | **KEEP / ask_success** (2x move-on) |
| Neighbor mesh | Clear/Empty unless N owner-on | **SUPERSEDE** — bits → coast family |
| PLACE-coast | deferred | **this ticket** |

Townscaper grammar: edit a point → rebuild DualCells that sample that point; each DualCell picks MeshLibrary from corner types. Place Success remains one Full on OwnedDualCell(V). Coast Success = land/water boundary DualCells read Edge/Corner/cove — not Empty ocean skip when bits warrant.

## Coast contract (binding)

| Rule | Detail |
|------|--------|
| Place KEEP | LMB → one Full on OwnedDualCell(V) for n=3/n=4 when owner on |
| Refresh KEEP | DualCellsTouching = owned + DualCellsSampling(V); bits sampled |
| Coast | Owner off → `MapOccupancyBitsToCoastFamily(bits, n)` → Empty/Edge/Corner/Diagonal/InverseCorner/Full |
| Full mesh | Single-deck Stage-6 emit KEEP (no GLB MeshFit/Y-bias) |
| Non-Full | MeshFit dual-edge / barycentric KEEP |
| Ghost | cyan hover one cell — no second Full under ghost |
| Refuse | `update_four_cross_as_success` as sole place · `y_bias_as_zfight_fix` · `owned_only_empty_coast_as_success` · Townscaper Done |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_place_coast_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | PLACE-coast — OccupancyCorners bits → coastline MeshLibrary; place Full KEEP |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_place_coast` |
| Map ticket | `PLACE-coast` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Flip V → owned Full KEEP; sampling DualCells refresh | expand-only paint; silent recompute |
| Owner-off DualCell with bits → Edge/Corner/Diagonal/InverseCorner/Full readable as coast | `owned_only_empty_coast_as_success` (Empty when bits warrant coast) |
| Spray ≠ place Success (owned Full remains place) | `update_four_cross_as_success` as sole place Success |
| Single-deck Full + tri place + sample recompute KEEP | reintroduce Y-bias / GLB MeshFit Full |
| Ghost cyan one cell; Empty skip when bits=0; dual `+`; Stage-6; terrain; squarify; rings=5 | ocean carpet · valence-5 · Townscaper Done |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** flip editable V → OwnedDualCell Full (KEEP); DualCells that sample V refresh; neighbor DualCells with partial OccupancyCorners bits show Edge/Corner (or Diagonal/InverseCorner) coastline readable as coast — not Empty ocean skip; bits sampled; single-deck + tri place + update-four KEEP; Prefer refuses `owned_only_empty_coast_as_success` / `y_bias_as_zfight_fix` / `update_four_cross_as_success` as sole place; snap/seat/Empty/dual+/Stage-6/terrain/squarify/rings=5 KEEP. MCP alone ≠ Success. |
| Out | Townscaper product Done · Terrain3D · MCP-only · Y-bias Full harden · GLB MeshFit Full return |

## 4. Refuse (`do_not_waive`)

`owned_only_empty_coast_as_success` · `update_four_cross_as_success` · `y_bias_as_zfight_fix` · `seizure_coplanar_deck_as_success` · `silent_ghost_without_place_n3` · `soft_take_4` · `valence_5_editable` · `sector_pie_as_dual_cell_tile` · `verify_mcp_only` · prior dual refuses (except coastline Empty-neighbor deferral superseded)

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_update_four_recompute_r1]] | **Update-four sample recompute KEEP / ask_success** (operator move-on) |
| [[alpha0_stalberg_dual_single_deck_emit_r1]] | **Single-deck Full emit KEEP / ask_success** |
| [[alpha0_stalberg_dual_tri_cell_place_r1]] | Tri place KEEP / ask_success |
| [[alpha0_stalberg_dual_owned_only_paint_r1]] | Place one-Full-on-owned KEEP; **coastline Empty deferral SUPERSEDED** |
| [[alpha0_stalberg_dual_whole_cell_orient_r1]] | Coverage+frame KEEP |
| [[alpha0_stalberg_dual_owned_cell_place_r1]] | Seat KEEP |
| [[alpha0_stalberg_dual_primary_vertex_place_r1]] | Snap KEEP |
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. LIVE weld (implementer)

- `DualGridCraftHost.ResolveOrganicDualVisualFamily`: owner-on → Full; owner-off → `MapOccupancyBitsToCoastFamily` (quad 16 + tri 8).
- Metas: `place_coast=true`, `owned_only_coastline_deferred=false`; WeldSliceId → `alpha0_stalberg_dual_place_coast_r1`.
- Full single-deck emit KEEP; non-Full MeshFit KEEP; DualCellsSampling UpdateFour KEEP.
- Prefer concept; arm `factory-project.yaml`; GREENLIGHT WELD LIVE; Trinity `project/genesis-mythos-master`.
- Receipt: `claim_class: staging` until operator F5 on **2y only**.
- Curator skip if mass `.cursor/rules` dirt / `git.push_enabled: false`.

## 7. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Place Full on OwnedDualCell(V) (tri and/or quad) — place KEEP.
3. Flip a **neighbor** editable point — DualCells that sample it refresh; **coast** DualCells show Edge/Corner (not Empty skip) where bits warrant.
4. Ghost remains cyan hover only (no second Full under ghost).
5. Single-deck no-strobe KEEP; Empty skip when bits=0; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP.
6. Attest ask_success only when coasts read as coasts — MCP alone ≠ Success. Do **not** attest Townscaper Done.

## Related

- Prior KEEP [[alpha0_stalberg_dual_update_four_recompute_r1]] · Single-deck [[alpha0_stalberg_dual_single_deck_emit_r1]] · Tri [[alpha0_stalberg_dual_tri_cell_place_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_stalberg_grid_kernel_r1]]
