---
slice_id: alpha0_stalberg_craft_plane_authority_r1
ask_id: alpha0_stalberg_quad_kernel
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1f
created: 2026-10-03
updated: 2026-10-03
composed_at: 2026-10-03T17:59:34Z
claim_class: staging
factory_greenlit: true
status: staging_awaiting_operator_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_topology_base_r1
next_in_chain: alpha0_stalberg_dual_corner_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_craft_plane_authority_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
---

# Slice brief — `alpha0_stalberg_craft_plane_authority_r1`

Rebind craft pick/paint / `ICraftCellAuthority` onto the live **OrganicQuadMesh** faces (occupancy authority = organic quads). Kernel pipeline from [[alpha0_stalberg_topology_base_r1]] stays intact. Prefer edges+faces stay green. **No Curator.**

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Topology: [[Grid-Topology-Host-Law]]. Prefer: [[Prefer-Authorship-Host-Law]].

## Why (operator agree with disagree)

Grok wanted dual-corner next. Cursor disagreed: LIVE ray→snap→paint still goes through **Hex19**, while the readable board is OrganicQuadMesh. Craft-plane authority must rebind first; dual-corner is ticket 2.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_quad_kernel` |
| `slice_id` | `alpha0_stalberg_craft_plane_authority_r1` |
| Scope | Ray→snap→paint / `ICraftCellAuthority` occupancy on **OrganicQuadMesh faces** (or corner logic points as occupancy keys). Hex19 not Success. Kernel intact. |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | update — craft-plane authority rebind |

## 2. Focus inspirations

| Source | Why |
|--------|-----|
| topology_base_r1 receipt | Healthy organic all-quad board (injective topo + soft relax) |
| Grid-Topology-Host-Law | Faces/cells are paint targets; points ≠ grid |
| Prefer-Authorship-Host-Law | Fail-closed product seats |
| Townscaper dual-grid grammar | Seasoning only — dual-corner paint is **next** ticket |

## 3. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | F5/MCP: picking/painting uses OrganicQuadMesh craft authority (not Hex19 Success); kernel board still readable; Prefer edges+faces; regenerable; graybox OK |
| Operator attest | F5 primary; MCP screenshot evidence allowed as aid — ban MCP-as-Success alone (`verify_mcp_only`) |
| Receipt | Cite rebind; strip dual_corner/tiles/art/Terrain3D/Hex19 Success |

## 4. Refuse

| Code | Note |
|------|------|
| `hex19_pick_as_craft_authority` | Ray/snap/paint still owned by Hex19 as Success |
| `hex_scaffold_as_final_mesh` | Hex19 lattice primary board |
| `dual_overlay_as_grid_kernel` | Dual sold as this Success |
| `points_as_grid` / `count_equals_topology` / `explicit_met_implicit_miss` | Topology seat |
| `skip_dissolve_relax` + kernel refuses | Pipeline regress |
| `bundle_tutorial_steps` | dual_corner paint / tiles / art this Prefer |
| `terrain3d_in_scope` / `craft_terrain_blend` / `terrain3d_leak_f5` | Terrain3D |
| `craft_cam_recenter_on_place` | Cam yank |
| `verify_mcp_only` / `inspiration_shape_miss` / `fidelity_miss` | Honesty |

## 5. Out of scope

- Dual-corner paint Success → [[alpha0_stalberg_dual_corner_r1]]
- Tile families / art bind / Terrain3D / Hex19 tutorial Success
- Curator push

## 6. Kickoff

1. Armed + greenlit (this file).
2. Force-compose / IMPLEMENT_SLICE module lane with armed_packet_path **or** in-session Half-B weld under this packet.
3. Prefer authorship pass + MCP screenshot evidence.
4. Trinity sync+push for Grok.
5. Only then greenlight ticket 2.

## Related

- Prior [[alpha0_stalberg_topology_base_r1]] · Next [[alpha0_stalberg_dual_corner_r1]] · [[alpha0_stalberg_grid_kernel_r1]]
