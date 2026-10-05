---
slice_id: alpha0_stalberg_dual_mesh_fit_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2m
created: 2026-10-04
updated: 2026-10-04
greenlit_at: 2026-10-04T19:33:00Z
composed_at: 2026-10-04T19:33:00Z
claim_class: staging
factory_greenlit: true
status: armed_ready_to_stage
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_visual_r3
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
depends_on: alpha0_stalberg_dual_visual_r3
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_mesh_fit_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
density_lift_live: rings_5_spacing_210
prefer_concept_required: true
success_object: dual_offset_cells
contract: C_mesh_fit_four_corner_pieces_to_secondary_quad
---

# Slice brief — `alpha0_stalberg_dual_mesh_fit_r1`

**GREENLIT** `2026-10-04T19:33:00Z` — Split / fit dual MeshLibrary silhouettes into **four corner (sector) pieces** and **warp/skin vertices** onto true secondary dual corners (`SmallCornerQuad` = V · edge-mid · face-centroid · edge-mid). Prefer **concept**. `claim_class: staging` until operator F5.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]] § C.1. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Prior: [[alpha0_stalberg_dual_visual_r3]].

## Why (after 2l)

- [[alpha0_stalberg_dual_visual_r3]] placed discrete empty/edge/corner/full GLBs on secondary-centered small-corner slots via translate+yaw(+uniform scale) — rigid cubes / plates that read as filled blocks but **do not hug** true secondary sector edges.
- Next altitude: **mesh fit** — corner-config still selects the discrete family piece-set; each piece's footprint **skins** to `SmallCornerQuad.Corners` (and Stage-6 face-centroid + edge-mid loci). Refuse resurrecting stretch Scale / gray ramp / FaceCornersLocal / primary-star glow / Hex19 Success.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_mesh_fit_r1` |
| Scope | 4 corner/sector pieces + vertex warp to secondary dual corners; family ids kept |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `mesh_fit_four_corner_pieces_to_secondary_quad` |

## 2. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Each dual/secondary small-corner slot shows a **sector piece** (family empty/edge/corner/full) whose silhouette **hugs** secondary quad edges/corners via **vertex warp/skin** to `SmallCornerQuad.Corners` (V · edge-mids · face-centroid); corner-config still selects piece set + rot/mirror; Stage-6 wire + secondary glow + squarify Stage 5 + rings=5 spacing=210 kept; Prefer refuses stretch_as_variant / gray_ramp_only / primary_face_as_dual / FaceCornersLocal / primary_star_glow / Hex19 Success |
| Out | density-beyond-5 · Terrain3D · art-bind polish · cam yank · Hex19 Success · r1/r2/r3 ask_success substitution |

## 3. Refuse

`stretch_as_variant` · `gray_ramp_only` · `primary_face_as_dual` · `face_corners_local_as_dual_edges` · `primary_star_glow_as_success` · `stage6_union_as_single_glow_tile` · `hex19_success` · `over_neighbor_paint` · `inspiration_shape_miss` · `verify_mcp_only` · `craft_cam_recenter_on_place` · `terrain3d_in_scope` · non_uniform Scale-as-variant

## 4. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_visual_r3]] | Discrete family MeshLibrary ids KEEP (empty/edge/corner/full) |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 dual wire KEEP |
| [[alpha0_stalberg_dual_secondary_glow_center_r1]] | Secondary glow/pick KEEP |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 rotate-90 squarify KEEP |
| Density lift LIVE | rings=5 · spacing=210 |

## 5. Operator F5

1. Open `res://scenes/WorldgenCraft.tscn`, F5; dual overlay on (D).
2. Small-corner pieces should **hug** coral/cyan secondary edges — not rigid cubes floating at centres, not stretched plates.
3. Seeded / flipped faces still read empty / edge / corner / full families.
4. Stage-6 cyan crosses amber; secondary glow center intact; rings=5 spacing=210.
5. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Prior [[alpha0_stalberg_dual_visual_r3]] · Audit [[Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Goal [[Ingest/Final-grid-state.jpg]]
