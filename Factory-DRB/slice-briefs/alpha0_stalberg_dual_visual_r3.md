---
slice_id: alpha0_stalberg_dual_visual_r3
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2l
created: 2026-10-04
updated: 2026-10-04
greenlit_at: 2026-10-04T19:02:28Z
composed_at: 2026-10-04T19:02:28Z
claim_class: staging
factory_greenlit: true
status: armed_ready_to_stage
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_secondary_glow_center_r1
logic_prior_slice_id: alpha0_stalberg_dual_visual_r2
kernel_foundation: alpha0_stalberg_topology_base_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
depends_on: alpha0_stalberg_dual_secondary_glow_center_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_visual_r3.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
density_lift_live: rings_5_spacing_210
prefer_concept_required: true
success_object: dual_offset_cells
contract: C_meshlibrary_models_on_secondary_small_corner_slots
terrain_success: false
ask_success: false
---

# Slice brief — `alpha0_stalberg_dual_visual_r3`

**GREENLIT** `2026-10-04T19:02:28Z` — MeshLibrary / discrete silhouettes on **secondary-centered small-corner** dual slots. **Altitude note:** discrete bind only — **not** terrain ask_success (see [[alpha0_stalberg_dual_terrain_tile_r1]]). Prefer **concept** + arm/prime. `claim_class: staging` until operator F5. LIVE weld may proceed with file edits + Blender MCP; Godot MCP screenshots optional if editor bridge down.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]] § C.1. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]].

## Why (after 2k / squarify)

- [[alpha0_stalberg_dual_secondary_glow_center_r1]] centered pick/glow on secondary face centroids via `SmallCornerQuadsAroundFace` — Stage-6 wire + small-corner units KEEP.
- [[alpha0_stalberg_quad_kernel_squarify_r1]] Stage-5 rotate-90 squarify KEEP; LIVE density **rings=5 · spacing=210**.
- Prior dual_visual r1/r2: Prefer harden + graybox stand-ins; this Prefer binds **Blender→MeshLibrary** models (`assets/craft/dual_grid/craft_dual_*.glb`) onto those secondary-centered slots — not stretch / gray ramp / primary-face-as-dual.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_visual_r3` |
| Scope | MeshLibrary models on secondary-centered small-corner dual slots; corner-config → empty/edge/corner/full + rot/mirror |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | `bind_dual_visual_meshlibrary_models_secondary_slots` |
| Pipeline | **Blender→MeshLibrary preferred** (`assets/craft/dual_grid/`) |

## 2. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Corner-config on secondary-centered small-corner slots selects **distinct** MeshLibrary items (empty/edge/corner/full + rot/mirror); place = **translate + yaw (+ uniform scale only)**; Stage-6 wire kept; secondary glow center kept; squarify Stage 5 kept; LIVE rings=5 spacing=210; Prefer refuses stretch_as_variant / gray_ramp_only / primary_face_as_dual / over_neighbor_paint / inspiration_shape_miss |
| Out | density-beyond-5 · Terrain3D · art-bind polish · cam yank · Hex19 Success · r1/r2 ask_success |

## 3. Refuse

`stretch_as_variant` · `gray_ramp_only` · `primary_face_as_dual` · `over_neighbor_paint` · `inspiration_shape_miss` · `skip_dual_offset` · `stage6_union_as_single_glow_tile` · `primary_star_glow_as_success` · `verify_mcp_only` · `craft_cam_recenter_on_place` · `terrain3d_in_scope` · prior kernel/dual refuses

## 4. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 dual wire KEEP |
| [[alpha0_stalberg_dual_secondary_glow_center_r1]] | Secondary glow/pick center KEEP |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 rotate-90 squarify KEEP |
| [[alpha0_stalberg_topology_base_r1]] | Organic all-quad underlay |
| Density lift LIVE | rings=5 · spacing=210 |
| [[alpha0_stalberg_dual_visual_r2]] | Prefer refuse harden (stretch/over-neighbor) — cite |

## 5. Operator F5

1. Open `res://scenes/WorldgenCraft.tscn`, F5 / play; dual overlay on (D).
2. Click near coral/cyan secondary → glow still secondary-centered; Stage-6 cyan crosses amber.
3. Populate / flip so empty / edge / corner / full silhouettes read as **discrete models** (not axis stretch, not gray height-ramp only).
4. Confirm place = translate+yaw(+uniform scale); rings=5 spacing=210 board intact.
5. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Prior [[alpha0_stalberg_dual_secondary_glow_center_r1]] · Prefer harden [[alpha0_stalberg_dual_visual_r2]] · Audit [[Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Goal [[Ingest/Final-grid-state.jpg]]
