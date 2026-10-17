---
slice_id: alpha0_stalberg_manual_scale_r1
ask_id: alpha0_stalberg_manual_scale
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1g
created: 2026-10-03
updated: 2026-10-03
composed_at: 2026-10-03T18:32:16Z
claim_class: staging
factory_greenlit: true
status: staging_prefer_ok_awaiting_operator_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_corner_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_manual_scale_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
density_lift: deferred_until_pipeline_ask_success
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
---

# Slice brief — `alpha0_stalberg_manual_scale_r1`

Dial Stålberg organic craft plane to the **manual / hex-19 cell-count budget** (`DefaultRingCount = 2` → 19 seed verts) while **enlarging world spacing** (`DefaultSpacing = 3.0`, was 1.15) so the few cells are large and clickable. Keep the correct pipeline: injective topo, craft-plane authority on OrganicQuadMesh, dual-corner four-cell update. **Do not** add rings/cells to fill the view; **do not** revert Hex19 point-cloud Success.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Topology: [[Grid-Topology-Host-Law]]. Prefer: [[Prefer-Authorship-Host-Law]].

## Why

Operator: organic craft plane is accurate but too detail-dense (~300+ quads / rings=5). Restore the dropped **19-point constraint** (Hex19OccupancyLattice = centre + 2 rings). Lift density later after pipeline greenlight / `ask_success`.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_manual_scale` |
| `slice_id` | `alpha0_stalberg_manual_scale_r1` |
| Scope | rings=2 cell budget + enlarged spacing (not more cells); Prefer edges+faces; dual-corner + craft authority wired |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | update — manual-scale seed rings |

## 2. Manual limit (resolved)

| Source | Resolution |
|--------|------------|
| [[Grid-Topology-Host-Law]] | Hex-19 (1+6+12) = tutorial scaffold size |
| `Hex19OccupancyLattice` | `BuildRingVertices(rings: 2)` → 19 verts |
| `StalbergQuadKernel.DefaultRingCount` | **2** (was 5) — cell count |
| `StalbergQuadKernel.DefaultSpacing` | **3.0** (was 1.15) — world size / click target |
| Seed hull diameter | ≈12.0 (was ≈11.5 at rings=5×1.15) |
| Product density | `ProductDensityRingCount = 5` — **deferred** until pipeline `ask_success` |

## 3. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | F5/MCP: small readable organic board (seed rings=2); Prefer edges+faces; craft pick on OrganicQuadMesh; dual-corner four-cell still wired; regenerable; graybox OK |
| Out | Hex19 tutorial Success · XOR antipode keys · abandoning organic kernel · density lift this Prefer |
| Receipt | Cite before/after face+vert counts; density_lift deferred |

## 4. Refuse

`points_as_grid`, `count_equals_topology`, `hex_scaffold_as_final_mesh`, `hex19_pick_as_craft_authority`, `skip_dual_offset`, kernel refuses, Terrain3D/art/cam yank, `verify_mcp_only`.

## 5. Kickoff

1. Armed + greenlit (this file).
2. LIVE: `DefaultRingCount = 2`; Prefer + MCP before/after density shots.
3. Trinity sync+push for Grok.
4. Operator F5 — density lift only after pipeline ask_success.

## Related

- Prior [[alpha0_stalberg_dual_corner_r1]] · Foundation [[alpha0_stalberg_topology_base_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Craft [[alpha0_stalberg_craft_plane_authority_r1]]
