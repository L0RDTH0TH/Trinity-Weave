---
slice_id: alpha0_stalberg_dual_cell_lookup_yaw_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2p
created: 2026-10-04
updated: 2026-10-04
greenlit_at: '2026-10-04T22:08:30Z'
composed_at: '2026-10-04T22:08:30Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: greenlit_weld_live_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_terrain_tile_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
depends_on: alpha0_stalberg_dual_terrain_tile_r1
supersedes_placement:
  - alpha0_stalberg_dual_mesh_fit_r1
  - alpha0_stalberg_dual_visual_r3
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_cell_lookup_yaw_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
contract: C_dual_cell_lookup_yaw_edge_frame
materials_keep: dual_offset_terrain_tile_sixpack
grok_diagnosis: sector_pie_host_wrong_object_for_coalesce
---

# Slice brief — `alpha0_stalberg_dual_cell_lookup_yaw_r1`

**GREENLIGHT WELD LIVE** `2026-10-04T22:08:30Z` — Prefer concept + host coalesce/placement fix. Keep terrain sixpack **materials**; stop pie-sector host. `claim_class: staging` until operator F5.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Materials KEEP: [[alpha0_stalberg_dual_terrain_tile_r1]]. Geometry KEEP: [[alpha0_stalberg_dual_stage6_cell_r1]].

## Why (Grok + Cursor 2026-10-04)

- Terrain-tile sixpack fixed cream-blob materials; coalesce still failed.
- LIVE stacked **dual_visual_r3** sector pies + **mesh_fit** warp + whole dual-cell GLBs → Full face stamped as four Full pies; world/pie rot90 ≠ dual-edge frame.
- Townscaper: occupancy at logic points → each **Stage-6 DualCell** reads **four occupancy corners** → one MeshLibrary item → yaw in dual-cell edge frame → warp whole `Stage6CornersLocal`.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_cell_lookup_yaw_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** |
| Scope | Host placement/lookup/yaw on Stage-6 DualCell; terrain GLBs KEEP |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `dual_cell_lookup_yaw_edge_frame` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Lookup on **4 occupancy corners of Stage-6 DualCell** (`CornerLogicIndices`) | Sector-local Empty/Full only |
| Yaw/mirror in **dual cell edge frame**, then place/warp **whole** dual cell (`Stage6CornersLocal`) | World k·90° then pie warp |
| Full = wall-less plateau, same top height as neighbor Fulls | Skirt on land–land |
| Fill verts → coalesced moss pad; Edge/Corner only on waterline | Internal walls between Fulls |
| One click logic vert → ≤4 DualCells as Corners pointing at that vert (`DualCellsExpandingFrom`) | Face-stamp Full rectangles |
| F5: name Empty/Edge/Corner/InverseCorner from coastline, overlay off | Metrics-only Prefer |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** one MeshLibrary item per Stage-6 DualCell; lookup from 4 occupancy corners; yaw in dual-edge frame; Full wall-less plateau; Edge/Corner only on shoreline; one click → ≤4 Corners; name variants from coastline without overlay; terrain materials + Stage-6 wire + secondary glow pick + squarify + rings=5 spacing=210 KEEP; Prefer refuses `sector_pie_as_dual_cell_tile` / stretch / gray_ramp / plinth_as_terrain / prop_scatter / proxy_substitution |
| Out | another sixpack restyle · pie host KEEP as Success · dual_visual_r3 ask_success · Terrain3D · density-beyond-5 · MCP-only attest |

## 4. Refuse (`do_not_waive`)

`sector_pie_as_dual_cell_tile` · `face_stamp_as_dual_populate` · `world_yaw_as_dual_edge_frame` · `plinth_as_terrain` · `prop_scatter_as_composition` · `stretch_as_variant` · `gray_ramp_only` · `primary_face_as_dual` · `stamp_as_dual` · `metrics_only_glb_drop` · `proxy_substitution` · `intent_collapsed_to_mechanics` · `verify_mcp_only` · prior dual refuses

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack GLBs/materials KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 dual wire KEEP |
| [[alpha0_stalberg_dual_secondary_glow_center_r1]] | Secondary glow/pick KEEP (populate ≠ glow) |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 squarify KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; overlay off for coastline read.
2. One click logic vert → ≤4 Corner tiles pointing at that vert (small diamond), not face-stamp Full rectangles.
3. Filled cluster → one moss plateau; no brown internal walls between Fulls.
4. Name Empty / Edge / Corner / InverseCorner from coastline without debug overlay.
5. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Prior materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Supersedes placement [[alpha0_stalberg_dual_mesh_fit_r1]] / [[alpha0_stalberg_dual_visual_r3]] · Series [[alpha0_stalberg_grid_kernel_r1]]
