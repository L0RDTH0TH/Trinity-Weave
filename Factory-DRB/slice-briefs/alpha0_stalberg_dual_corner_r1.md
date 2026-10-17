---
slice_id: alpha0_stalberg_dual_corner_r1
ask_id: alpha0_stalberg_dual_corner
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2
created: 2026-10-03
updated: 2026-10-03
composed_at: 2026-10-03T17:59:34Z
claim_class: staging
factory_greenlit: true
status: staging_awaiting_operator_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_craft_plane_authority_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_craft_plane_authority_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_corner_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
---

# Slice brief — `alpha0_stalberg_dual_corner_r1` (draft)

Dual-corner logic points on organic quads; click flips; four dual cells rebuild. **Do not greenlight/launch until** [[alpha0_stalberg_craft_plane_authority_r1]] Prefer+staging weld succeeds.

Corrected from Grok draft: prior = craft_plane_authority_r1 (not relax_r1); cite [[alpha0_stalberg_topology_base_r1]] as kernel foundation.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_corner` |
| `slice_id` | `alpha0_stalberg_dual_corner_r1` |
| Scope | Logic points at organic quad corners (or dual offset); flip updates four dual cells; Prefer edges+faces; graybox OK |
| `factory_greenlit` | `false` until ticket 1 succeeds |
| Mode | bind_dual_corner_on_organic_quads |

## 2. Acceptance (when greenlit)

| Field | Value |
|-------|--------|
| `done_when` | F5/MCP: dual cells change on corner flip; Prefer edges+faces; organic board preserved; regenerable; graybox OK |
| Out | tiles/art/Terrain3D/cam yank / Hex19 tutorial Success |

## 3. Refuse

`points_as_grid`, `count_equals_topology`, `prop_scatter_as_composition`, `skip_dual_offset`, `inspiration_shape_miss` + kernel refuses + no Terrain3D/art/cam yank.

## Related

- Depends [[alpha0_stalberg_craft_plane_authority_r1]] · Foundation [[alpha0_stalberg_topology_base_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]
