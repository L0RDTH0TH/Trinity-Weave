---
slice_id: alpha0_stalberg_dual_zfight_harden_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2v
created: 2026-10-13
updated: 2026-10-13
greenlit_at: '2026-10-13T00:27:00Z'
composed_at: '2026-10-13T00:27:00Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: f5_fail_superseded_by_single_deck_emit
operator_f5_confirmed: false
operator_f5_failed: true
operator_f5_failed_at: '2026-10-13T00:42:00Z'
disposition: SUPERSEDED
superseded_by: alpha0_stalberg_dual_single_deck_emit_r1
fail_note: Y-bias/flatten/sorting smaller than near-plane depth step at cam~3850/spacing210; parent agrees do not retry bigger Y
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_tri_cell_place_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
keeps_snap_from: alpha0_stalberg_dual_primary_vertex_place_r1
keeps_seat_from: alpha0_stalberg_dual_owned_cell_place_r1
keeps_coverage_frame_from: alpha0_stalberg_dual_whole_cell_orient_r1
keeps_owned_only_paint_from: alpha0_stalberg_dual_owned_only_paint_r1
keeps_tri_cell_place_from: alpha0_stalberg_dual_tri_cell_place_r1
depends_on: alpha0_stalberg_dual_tri_cell_place_r1
supersedes_visuals_deferred:
  - alpha0_stalberg_dual_tri_cell_place_r1
  - alpha0_stalberg_dual_owned_only_paint_r1
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
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_zfight_harden_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: owned_dual_cell_zfight_harden
contract: C_dual_zfight_harden
materials_keep: dual_offset_terrain_tile_sixpack
ticket_map: VIS-zfight
operator_diagnosis: full_ybias_0p12_too_weak_at_spacing210__seizure_decks_coplanar_flash_on_pan
---

# Slice brief — `alpha0_stalberg_dual_zfight_harden_r1`

**F5 FAIL / SUPERSEDED** `2026-10-13T00:42:00Z` → [[alpha0_stalberg_dual_single_deck_emit_r1]] (series **2w**). Operator F5 failed: craft-scale FullYBias / flatten / sorting cannot beat near-plane depth quantization at CameraHeight~3850 / spacing=210. Parent agrees — **do not** retry bigger Y. Prior **2u** tri place remains **KEEP / ask_success**.

~~**GREENLIGHT WELD LIVE** `2026-10-13T00:27:00Z`~~ — Prefer concept + **VIS-zfight** harden on Full MeshLibrary place. Prior **2u** [[alpha0_stalberg_dual_tri_cell_place_r1]] **KEEP / ask_success** (operator F5 confirmed). Owned-only KEEP; tri/quad place KEEP. **SUPERSEDE** deferred Z-fight / weak FullYBias / seizure-deck Success gap from 2t/2u. `claim_class: staging` until operator F5 on **this** ticket only. Coast / UpdateFour Corner spray / Townscaper product Done stay **out**.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Map ticket: `VIS-zfight` in [[World-Builder-Mini-Game-Ticket-Map]]. Tri place KEEP: [[alpha0_stalberg_dual_tri_cell_place_r1]]. Owned-only KEEP: [[alpha0_stalberg_dual_owned_only_paint_r1]].

## Why (binding diagnosis)

| Gate | Today (post-2u) | Result |
|------|-----------------|--------|
| Tri/quad Full place | n=3/n=4 owned-only | **KEEP** ask_success |
| FullYBias | `0.12` absolute | **too weak** at rings=5 / spacing≈210 (yLift≈12) |
| Seizure decks | multi-deck Full GLB + coplanar adjacent tops | pan **flicker** |
| Sorting/depth | SortingOffset `0.02` + RenderPriority 1 | insufficient vs amber underlay / neighbor Full edges |

Not PLACE-coast. Not PLACE-update-four spray. Prefer/host-weld does **not** require coast before VIS-zfight — map deferred this from 2t/2u explicitly.

## Z-fight contract (binding)

| Rule | Detail |
|------|--------|
| Place KEEP | LMB → one Full on OwnedDualCell(V) for DualCorners n=3 or n=4 (owned-only) |
| Visual Success | Camera pan/orbit — **no** coplanar seizure flicker on Full decks |
| Harden | Craft-scale Full Y bias + sorting offset + single-deck flatten + per-key micro-Y + depth priority |
| Neighbor | Empty unless own owner on (owned-only KEEP); coastline Corner spray still deferred |
| Refuse | `seizure_coplanar_deck_as_success` · `weak_full_ybias_as_harden` · `verify_mcp_only` |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_zfight_harden_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | VIS-zfight harden on Full place path; place polarity KEEP |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_zfight_harden` |
| Map ticket | `VIS-zfight` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Pan/orbit after Full place — no seizure coplanar flicker | `seizure_coplanar_deck_as_success` |
| Craft-scale FullYBias / sorting / single-deck flatten land in LIVE | `weak_full_ybias_as_harden` · docs-only harden |
| Tri + quad Full owned-only place KEEP | `silent_ghost_without_place_n3` · regress place |
| Owned-only KEEP (no neighbor Corner spray) | `neighbor_corner_spray_as_place` |
| Empty skip; dual `+`; Stage-6; terrain; squarify; rings=5 | ocean carpet · valence-5 editable |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** place Full on OwnedDualCell (n=3 or n=4) as before; **pan/orbit shows no tile flicker / seizure coplanar decks**; Prefer refuses `seizure_coplanar_deck_as_success` / `weak_full_ybias_as_harden`; owned-only + tri place + snap/seat/Empty/dual+/Stage-6/terrain/squarify/rings=5 KEEP. MCP alone ≠ Success. |
| Out | PLACE-coast · neighbor Corner spray as Success · Townscaper product Done · Terrain3D · MCP-only attest |

## 4. Refuse (`do_not_waive`)

`seizure_coplanar_deck_as_success` · `weak_full_ybias_as_harden` · `neighbor_corner_spray_as_place` · `update_four_cross_as_success` · `silent_ghost_without_place_n3` · `soft_take_4` · `valence_5_editable` · `sector_pie_as_dual_cell_tile` · `verify_mcp_only` · prior dual refuses

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_tri_cell_place_r1]] | **Tri place KEEP / ask_success**; visuals-deferred **SUPERSEDED** by this harden |
| [[alpha0_stalberg_dual_owned_only_paint_r1]] | Owned-only KEEP; weak Z-fight attempt SUPERSEDED |
| [[alpha0_stalberg_dual_whole_cell_orient_r1]] | Coverage+frame KEEP |
| [[alpha0_stalberg_dual_owned_cell_place_r1]] | Seat KEEP |
| [[alpha0_stalberg_dual_primary_vertex_place_r1]] | Snap KEEP |
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. LIVE weld (implementer)

- `DualGridCraftHost`: craft-scale `FullYBias` / `FullSortingOffset`; `FlattenFullToSingleDeck` after wallless plateau; per-DualCell micro-Y epsilon; stronger depth RenderPriority; clear `zfight_success_deferred`.
- Prefer concept; arm `factory-project.yaml`; GREENLIGHT WELD LIVE; Trinity `project/genesis-mythos-master`.
- Receipt: `claim_class: staging` until operator F5 on **2v only**.
- Curator skip if mass `.cursor/rules` dirt / `git.push_enabled: false`.

## 7. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible.
2. Place Full on a DualCell (quad and/or tri) — place KEEP from 2u/2t.
3. **Pan and orbit** the craft cam across filled tiles — **no** flicker / seizure flash.
4. Neighbors Empty unless own owner on; Empty skip; dual `+`; Stage-6 + terrain + squarify + rings=5 KEEP.
5. Do **not** attest coast / Corner spray / Townscaper Done.
6. Attest ask_success only when no-flicker bar met — MCP alone ≠ Success.

## Related

- Prior tri place [[alpha0_stalberg_dual_tri_cell_place_r1]] · Owned-only [[alpha0_stalberg_dual_owned_only_paint_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_stalberg_grid_kernel_r1]]
