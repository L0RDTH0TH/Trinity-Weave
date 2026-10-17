---
slice_id: alpha0_stalberg_dual_single_deck_emit_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2w
created: 2026-10-13
updated: 2026-10-13
greenlit_at: '2026-10-13T00:45:00Z'
composed_at: '2026-10-13T00:45:00Z'
claim_class: ask_success
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: ask_success_keep
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_zfight_harden_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat_from: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame_from: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_owned_only_paint_from: alpha0_stalberg_dual_owned_only_paint_r1
keeps_tri_cell_place_from: alpha0_stalberg_dual_tri_cell_place_r1
depends_on: alpha0_stalberg_dual_tri_cell_place_r1
supersedes_zfight_harden:
  - alpha0_stalberg_dual_zfight_harden_r1
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
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_single_deck_emit_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_single_deck_emit
contract: C_dual_single_deck_emit
materials_keep: dual_offset_terrain_tile_sixpack
ticket_map: VIS-zfight
operator_f5_confirmed: true
operator_f5_at: '2026-10-13T01:00:00Z'
disposition: KEEP
operator_diagnosis: depth_step_tens_of_wu_at_cam3850_spacing210__ybias_cannot_fix__emit_one_inset_deck
---

# Slice brief — `alpha0_stalberg_dual_single_deck_emit_r1`

**KEEP / ask_success** — operator F5 confirmed (`alpha0_stalberg_dual_single_deck_emit_r1` single-deck Full emit). Prefer concept + **VIS-zfight** single-deck emit landed. Prior **2u** [[alpha0_stalberg_dual_tri_cell_place_r1]] **KEEP / ask_success**. Prior **2v** [[alpha0_stalberg_dual_zfight_harden_r1]] **F5 FAIL / SUPERSEDED**. Owned-only KEEP; tri/quad place KEEP. Coast / UpdateFour Corner spray / Townscaper product Done stay **out**. Next brush: [[alpha0_stalberg_dual_update_four_recompute_r1]] (`PLACE-update-four`).

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Map ticket: `VIS-zfight` in [[World-Builder-Mini-Game-Ticket-Map]]. Tri place KEEP: [[alpha0_stalberg_dual_tri_cell_place_r1]]. Owned-only KEEP: [[alpha0_stalberg_dual_owned_only_paint_r1]]. Supersedes: [[alpha0_stalberg_dual_zfight_harden_r1]].

## Why (binding diagnosis — parent + Grok)

| Gate | 2v attempt | Result |
|------|------------|--------|
| Tri/quad Full place | n=3/n=4 owned-only | **KEEP** ask_success (2u) |
| FullYBias / lift / ε | 2.0 + 1.5 + 0.04 | **smaller than one depth step** at cam~3850 / spacing=210 / near~0.05 |
| FlattenFullToSingleDeck | slam GLB verts to one Y | **worse** — bevel/underside → coplanar tris; MeshFit + bias lifts whole stack |
| SortingOffset / RenderPriority | 0.75 / pri 2 | **do not fix** opaque coplanar depth fights |
| Architecture | emit one Stage-6 deck | **this slice** |

Do **not** retry bigger Y bias. If flash remains after this weld, find second writer (amber `BuildFaceMesh`, debug overlay, duplicate `_dualSlots`) — do not add more Y.

## Single-deck emit contract (binding)

| Rule | Detail |
|------|--------|
| Place KEEP | LMB → one Full on OwnedDualCell(V) for DualCorners n=3 or n=4 (owned-only) |
| Full mesh | **No** MakeWalllessFullPlateau / FlattenFullToSingleDeck / MeshFit on Full GLB |
| Emit | n=4 → two tris; n=3 → one tri; every vertex Y = craft yLift (12); inset ~1% toward centroid |
| Material | albedo from Full library item; opaque; cull back; depth write on |
| Deleted harden | FullSortingOffset · RenderPriority=2 · PerKeyYEpsilon · FullYBias / FullCraftLiftExtra / flatten path |
| Ghost | cyan hover alpha one cell — do **not** paint a second Full under ghost |
| Refuse | `seizure_coplanar_deck_as_success` · `y_bias_as_zfight_fix` · `verify_mcp_only` |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_single_deck_emit_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | VIS-zfight — Full single-deck emit; place polarity KEEP |
| `claim_class` | `ask_success` (operator F5 KEEP) |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_single_deck_emit` |
| Map ticket | `VIS-zfight` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Two Fulls sharing an edge — pan/orbit face stays one color; shared edge does not strobe | `seizure_coplanar_deck_as_success` |
| Full place = Stage-6 corner deck emit (not GLB MeshFit/flatten/Y-bias) | `y_bias_as_zfight_fix` · docs-only |
| Tri + quad Full owned-only place KEEP | `silent_ghost_without_place_n3` · regress place |
| Owned-only KEEP (no neighbor Corner spray) | `neighbor_corner_spray_as_place` |
| Empty skip; dual `+`; Stage-6; terrain; squarify; rings=5 | ocean carpet · valence-5 editable |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** place two Fulls sharing an edge; pan/orbit — face one color, shared edge does not strobe; Prefer refuses `seizure_coplanar_deck_as_success` / `y_bias_as_zfight_fix`; owned-only + tri place + snap/seat/Empty/dual+/Stage-6/terrain/squarify/rings=5 KEEP. MCP alone ≠ Success. |
| Out | PLACE-coast · neighbor Corner spray · Townscaper product Done · Terrain3D · MCP-only · bigger Y bias |

## 4. Refuse (`do_not_waive`)

`seizure_coplanar_deck_as_success` · `y_bias_as_zfight_fix` · `weak_full_ybias_as_harden` · `neighbor_corner_spray_as_place` · `update_four_cross_as_success` · `silent_ghost_without_place_n3` · `soft_take_4` · `valence_5_editable` · `sector_pie_as_dual_cell_tile` · `verify_mcp_only` · prior dual refuses

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_tri_cell_place_r1]] | **Tri place KEEP / ask_success** |
| [[alpha0_stalberg_dual_owned_only_paint_r1]] | Owned-only KEEP |
| [[alpha0_stalberg_dual_zfight_harden_r1]] | **F5 FAIL / SUPERSEDED** — wrong architecture |
| [[alpha0_stalberg_dual_whole_cell_orient_r1]] | Coverage+frame KEEP |
| [[alpha0_stalberg_dual_owned_cell_place_r1]] | Seat KEEP |
| [[alpha0_stalberg_dual_primary_vertex_place_r1]] | Snap KEEP |
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack KEEP (albedo source for Full deck) |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. LIVE weld (implementer)

- `DualGridCraftHost.PlaceStage6DualCellLibraryItem`: Full → `EmitFullSingleDeckFromStage6` (inset deck @ yLift=12; library albedo); delete Full Y-bias/sorting/flatten/RenderPriority harden.
- Prefer concept; arm `factory-project.yaml`; GREENLIGHT WELD LIVE; Trinity `project/genesis-mythos-master`.
- Receipt: `claim_class: staging` until operator F5 on **2w only**.
- Curator skip if mass `.cursor/rules` dirt / `git.push_enabled: false`.

## 7. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Place **two** Fulls that share an edge (tri and/or quad) — place KEEP from 2u.
3. **Pan and orbit** — each face stays one color; shared edge does **not** strobe.
4. Ghost remains cyan hover only (no second Full under ghost).
5. Neighbors Empty unless own owner on; Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP.
6. If still flashes — hunt second writer; **do not** add more Y.
7. Attest ask_success only when no-strobe bar met — MCP alone ≠ Success.

## Related

- Supersedes [[alpha0_stalberg_dual_zfight_harden_r1]] · Prior tri place [[alpha0_stalberg_dual_tri_cell_place_r1]] · Owned-only [[alpha0_stalberg_dual_owned_only_paint_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_stalberg_grid_kernel_r1]]
