---
slice_id: alpha0_stalberg_dual_art_style_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2n
created: 2026-10-04
updated: 2026-10-04
greenlit_at: 2026-10-04T19:57:41Z
composed_at: 2026-10-04T19:57:41Z
claim_class: staging
factory_greenlit: false
superseded_by: alpha0_stalberg_dual_terrain_tile_r1
ask_success: false
status: wrong_success_superseded_by_terrain_tile_r1
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_mesh_fit_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
depends_on: alpha0_stalberg_dual_mesh_fit_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_art_style_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Screenshot_20261004_003640_YouTube.jpg
density_lift_live: rings_5_spacing_210
prefer_concept_required: true
success_object: dual_offset_cells
contract: C_cream_quarter_platform_art_style_on_mesh_fit
camera_altitude: separate_live_craft_cam_tilt_not_prefer_success
---

# Slice brief — `alpha0_stalberg_dual_art_style_r1`

**WRONG SUCCESS / SUPERSEDED** by [[alpha0_stalberg_dual_terrain_tile_r1]] — Prefer scored cream quarter-platforms (plinths) because this ticket named that Success. Do **not** claim ask_success. Historical Prefer-ok remains audit-only.

~~GREENLIT — Restyle dual MeshLibrary / mesh-fit sector pieces toward the **cream quarter-platform** look~~ in [[Ingest/Screenshot_20261004_003640_YouTube.jpg]] (YT Game Dev Buddies dual-grid / Townscaper). Keep bilinear mesh_fit from [[alpha0_stalberg_dual_mesh_fit_r1]]. Prefer **concept**. `claim_class: staging` until operator F5.

**Altitude split (binding):** Craft-cam pitch/orbit tilt is a **separate LIVE action** (`CraftPlanarCamRig`) — **not** Prefer Success for this ticket. Terrain3D world-builder Success is **out**; light craft-plane water/env tint is in-scope documentation + light weld only.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]] § C.1. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Prior: [[alpha0_stalberg_dual_mesh_fit_r1]].

## Why (after 2m)

- [[alpha0_stalberg_dual_mesh_fit_r1]] warps family silhouettes onto `SmallCornerQuad.Corners` — geometry correct, charcoal-teal graybox still reads as “proxy art.”
- Operator model: four cream quarter-platforms meeting at center, rounded outer corners, elevated above water, soft under-glow; orange craft grid over teal water (YT still).
- Camera: separate tilt so WorldgenCraft reads as 3D (pitch ~35–55°) — do **not** pile cam into Prefer Success.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_art_style_r1` |
| Scope | Cream quarter-platform restyle of dual MeshLibrary + mesh-fit pieces; light water/env tint; cam tilt separate |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `cream_quarter_platform_art_style_on_mesh_fit` |

## 2. Focus inspirations

| Source | Why in focus |
|--------|----------------|
| https://www.youtube.com/watch?v=Y19Mw5YsgjI | Canonical Game Dev Buddies / Townscaper dual-grid authorship |
| [[Ingest/Screenshot_20261004_003640_YouTube.jpg]] | Cream 2×2 quarter platforms over water + orange grid |
| https://youtu.be/Jm3pLya3d9c | Lerg dual-grid seasoning if needed |
| [[Ingest/townscaper-screenshot.jpg]] | Product orbit pitch + waterline / cream foundations |
| Evidence `_evidence/yt_*` + `townscaper_product_orbit_ref.jpg` | Saved stills for Prefer / F5 |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Secondary small-corner slots show **cream** quarter/sector pieces (families empty/edge/corner/full still silhouette-distinct) elevated above teal craft-plane water, soft under-glow OK; bilinear mesh_fit to `SmallCornerQuad.Corners` kept; Stage-6 + secondary glow + squarify + rings=5 spacing=210 kept; Prefer refuses stretch_as_variant / gray_ramp_only / FaceCornersLocal / primary_face_as_dual / Hex19 / Terrain3D Success; cam pitch is separate LIVE (not this Prefer seat) |
| Out | Terrain3D world-builder Success · density-beyond-5 · resurrect stretch/FaceCornersLocal/gray_ramp · cam tilt as Prefer Success · Hex19 Success |

## 3b. Terrain / water target (document — light weld only)

| Target (from YT / Townscaper stills) | This altitude |
|--------------------------------------|---------------|
| Flat teal-blue water under orange craft grid | Craft-plane face tint + env background tint |
| Soft foam/ripple stylization | **Later** ticket (not claimed) |
| Terrain3D height blend under Sparky | **Later** Prefer — refuse `terrain3d_in_scope` |

## 4. Refuse

`stretch_as_variant` · `gray_ramp_only` · `primary_face_as_dual` · `face_corners_local_as_dual_edges` · `primary_star_glow_as_success` · `stage6_union_as_single_glow_tile` · `hex19_success` · `over_neighbor_paint` · `inspiration_shape_miss` · `verify_mcp_only` · `craft_cam_recenter_on_place` · `terrain3d_in_scope` · `cam_tilt_as_art_prefer_success` · non_uniform Scale-as-variant

## 5. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_mesh_fit_r1]] | Bilinear warp to SmallCornerQuad.Corners KEEP |
| [[alpha0_stalberg_dual_visual_r3]] | Discrete family MeshLibrary ids KEEP |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 dual wire KEEP |
| [[alpha0_stalberg_dual_secondary_glow_center_r1]] | Secondary glow/pick KEEP |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 rotate-90 squarify KEEP |
| Density lift LIVE | rings=5 · spacing=210 |
| Separate LIVE | `CraftPlanarCamRig` pitch 35–55° — not Prefer Success |

## 6. Operator F5

1. Open `res://scenes/WorldgenCraft.tscn`, F5; dual overlay on (D).
2. Expect **tilted** craft cam (default ~45° look-down) — board reads 3D, not parallel-plane top-down.
3. Secondary slots show **cream** quarter/sector pieces elevated above teal water; soft under-glow OK.
4. Families empty/edge/corner/full still distinct by silhouette (not albedo ramp).
5. Stage-6 cyan crosses amber; secondary glow intact; rings=5 spacing=210.
6. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Prior [[alpha0_stalberg_dual_mesh_fit_r1]] · Evidence `Factory-DRB/slice-briefs/_evidence/` · Series [[alpha0_stalberg_grid_kernel_r1]] · Goal [[Ingest/Screenshot_20261004_003640_YouTube.jpg]]
