---
slice_id: alpha0_stalberg_dual_primary_vertex_place_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2q
created: 2026-10-04
updated: 2026-10-04
greenlit_at: '2026-10-04T22:52:06Z'
composed_at: '2026-10-04T22:52:06Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: greenlit_weld_live_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_cell_lookup_yaw_r1
keeps_materials_from: alpha0_stalberg_dual_terrain_tile_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
depends_on: alpha0_stalberg_dual_cell_lookup_yaw_r1
supersedes_snap_polarity:
  - alpha0_stalberg_dual_cell_lookup_yaw_r1
  - alpha0_stalberg_dual_secondary_glow_center_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_primary_vertex_place_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
density_lift_live: rings_5_spacing_210
success_object: dual_cell_meshlibrary_placement
place_polarity: primary_vertex_dual_cell_place
contract: C_primary_vertex_dual_cell_place
materials_keep: dual_offset_terrain_tile_sixpack
grok_diagnosis: secondary_face_snap_wrong_place_target__ocean_fill_all_empty
---

# Slice brief — `alpha0_stalberg_dual_primary_vertex_place_r1`

**GREENLIGHT WELD LIVE** `2026-10-04T22:52:06Z` — Prefer concept + primary-V snap polarity + Empty skip. Do **not** F5-attest `dual_cell_lookup_yaw_r1` while face/secondary pick KEEP. `claim_class: staging` until operator F5.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Materials KEEP: [[alpha0_stalberg_dual_terrain_tile_r1]]. Geometry KEEP: [[alpha0_stalberg_dual_stage6_cell_r1]]. Supersedes snap: [[alpha0_stalberg_dual_cell_lookup_yaw_r1]].

## Why (F5 + Grok corrected 2026-10-04)

- Blue env background ≠ water tiles. Cyan under cursor on a primary face = **face selected**; **no land modules** — wrong place target.
- Snap must be **primary vertex V** (orange star / main intersection), NOT face centroid / secondary.
- Populate **ONE** terrain module on **Stage-6 DualCell(V)** wrapping V (corners = incident face centroids).
- Do NOT fill the primary face; do NOT stamp neighbor faces around a face pick.
- Do **NOT** place Empty/ocean MeshLibrary on every DualCell / free slot — Empty = no mesh; amber primary grid reads. Water = underlay tint only if needed.
- Dual debug: dual verts as **`+` at face centres**; **remove dual edge wireframe**.
- Keep Stage-6 DualCell geometry, terrain GLBs for non-Empty, squarify, rings=5/spacing=210, mesh_fit onto DualCell(V) whole quad.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_primary_vertex_place_r1` |
| `success_object` | **`dual_cell_meshlibrary_placement`** (place polarity: `primary_vertex_dual_cell_place`) |
| Scope | Host snap/place Empty-skip/debug on Stage-6 DualCell(V); terrain GLBs KEEP |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `primary_vertex_dual_cell_place` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| `TryPickHexCell` → **`TryPickOrganicCorner` first** (primary V) | `secondary_face_snap_as_place` · `secondary_glow_center_as_place_target` |
| LMB → `FlipOrganicCorner(V)` only; one MeshLibrary item on `OwnedDualCell` / `Stage6CornersLocal(V)` | `face_stamp_as_dual_populate` · fill primary face |
| Empty: skip ocean GLB / opaque Empty on every DualCell | `ocean_fill_all_empty_slots` |
| Dual debug: `+` at face centres; no DualCellEdges ribbons | dual edge wireframe clutter |
| Organic primary amber grid visible | blue env misread as water tiles |
| Terrain GLBs for Edge/Corner/Full/… when bits warrant | `sector_pie_as_product` |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** LMB snaps primary V (amber star); places one MeshLibrary module on DualCell(V); Empty slots show amber grid (no ocean carpet); dual verts = plus at face centres; no dual-edge ribbons; Stage-6 + terrain materials + squarify + rings=5 spacing=210 KEEP; Prefer refuses `secondary_glow_center_as_place_target` / `ocean_fill_all_empty_slots` / `face_stamp_as_dual_populate` / `sector_pie_as_product` |
| Out | F5-attest lookup_yaw while face pick KEEP · pie host · Terrain3D · density-beyond-5 · MCP-only attest |

## 4. Refuse (`do_not_waive`)

`secondary_face_snap_as_place` · `secondary_glow_center_as_place_target` · `face_stamp_as_dual_populate` · `ocean_fill_all_empty_slots` · `sector_pie_as_product` · `sector_pie_as_dual_cell_tile` · `plinth_as_terrain` · `prop_scatter_as_composition` · `stretch_as_variant` · `gray_ramp_only` · `primary_face_as_dual` · `stamp_as_dual` · `metrics_only_glb_drop` · `proxy_substitution` · `intent_collapsed_to_mechanics` · `verify_mcp_only` · prior dual refuses

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_terrain_tile_r1]] | Terrain sixpack GLBs/materials KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 DualCell geometry KEEP |
| [[alpha0_stalberg_dual_cell_lookup_yaw_r1]] | Lookup/yaw/edge-frame KEEP; **snap polarity SUPERSEDED** |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 squarify KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 6. Operator F5 bar

1. Open `res://scenes/WorldgenCraft.tscn`, F5; amber primary grid visible (blue env ≠ water tiles).
2. Cursor near orange star / main intersection → snap primary V (not face centroid cyan).
3. LMB → one terrain module on DualCell(V); not face fill; not neighbor-face stamp.
4. Free DualCells show amber grid — **no ocean Empty carpet**.
5. Dual debug: `+` at face centres; no dual-edge ribbons.
6. Attest ask_success only when house bar met — MCP alone ≠ Success. Do **not** attest lookup_yaw under face-pick KEEP.

## Related

- Prior [[alpha0_stalberg_dual_cell_lookup_yaw_r1]] · Materials [[alpha0_stalberg_dual_terrain_tile_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]
