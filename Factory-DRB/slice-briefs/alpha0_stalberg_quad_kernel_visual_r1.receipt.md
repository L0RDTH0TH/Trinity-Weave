---
title: Staging receipt — alpha0_stalberg_quad_kernel_visual_r1
slice_id: alpha0_stalberg_quad_kernel_visual_r1
ask_id: alpha0_stalberg_quad_kernel
producer_run_id: sp-sqkv-29460a
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
completed: 2026-10-03T07:41:44Z
status: staging_awaiting_operator_f5
prior_weld_altitude: failed_altitude_visual_execution_fail
prior_slice_id: alpha0_stalberg_quad_kernel_r1
prior_producer_run_id: sp-sqk-3210b7
mcp_screenshot: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/_evidence/stalberg_visual_r1_planar_v2.png
---

# Staging receipt — `alpha0_stalberg_quad_kernel_visual_r1`

**claim_class: staging** until operator F5 readable planar irregular all-quad board. Approach from [[alpha0_stalberg_quad_kernel_r1]] stays (seed→tri→dissolve→subdivide→relax). Prior altitude: `failed_altitude_visual_execution_fail` (noodle/prism). This weld fixes visual/geometric execution. No tutorial s1–s6 claim. No dual paint / tiles / art / Terrain3D Success. No Curator.

## Identity

| Field | Value |
|-------|--------|
| producer_run_id | `sp-sqkv-29460a` |
| staged job | `factory-weld-sqkv-9cb62f9c-module-7d4aa5` |
| armed packet | `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_quad_kernel_visual_r1.armed.yaml` |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |

## Pipeline stages hit (code)

1. `SeedHexLatticeRings` (Variant B hex rings, tunable)
2. `TriangulateHexLattice`
3. `DissolveTrianglePairs`
4. `SubdivideFacesToQuads` → 100% quads (face valence 4)
5. `RelaxTowardSquares` — **boundary pinned** + adaptive side length (anti-clump)
6. `FlattenToCraftPlane` — finite sanitize / craft-plane law
7. Render opaque `OrganicQuadFaces` + depth-tested `OrganicQuadEdges`; `RegenerateOrganicQuadMesh` (R)

## Visual execution fixes (vs prior noodle/prism)

| Prior fail | Fix |
|------------|-----|
| Translucent Alpha faces + CullMode soup | Opaque `Transparency=Disabled`, depth write |
| Aggressive relax clump | Pin convex-hull boundary; softer pull; adaptive side |
| Unbounded Z / nonplanar read | Explicit `FlattenToCraftPlane` + Vector2→XZ Y=0 |
| Edge spaghetti without occlusion | Opaque edges, `NoDepthTest=false`, unique edge keys |

## Matrix Prefer quote used

> Same pipeline (seed→tri→dissolve→subdivide→relax); F5 primary = readable planar irregular all-quad mesh on craft plane; coherent surface + depth-tested edges; regenerable; graybox OK; flatten 3D intermediates for display.

## LIVE files

- `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/Core/WorldGen/StalbergQuadKernel.cs`
- `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/Core/WorldGen/OrganicQuadMesh.cs`
- `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/Systems/DualGridCraftHost.cs`
- `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/Systems/WorldgenCraft.cs`

## Prefer evidence

- **ok:** `True`
- **detail:** prefer_authorship_pass_ok
- **violations:** `[]`
- Refuse seats armed: visual (`noodle_edge_clutter` / `wireframe_spaghetti` / `extruded_prism_as_quad_board` / `unbounded_z_jitter` / `nonplanar_face_soup`) + prior kernel refuses
- Prefer scanners also fail Alpha transparency on `BuildFaceMesh` / `BuildEdgeMesh` and missing `FlattenToCraftPlane`

## Focus cites landed

- oskar docs/02 pipeline · [[Grid-Topology-Host-Law]] · [[Prefer-Authorship-Host-Law]]
- Prior [[alpha0_stalberg_quad_kernel_r1.receipt]] altitude fail

## F5 bar (operator)

Readable **planar** irregular all-quad mesh on craft plane; clean quad edges; no translucent prism soup; regenerate (R); graybox OK. Staging until operator attests. MCP screenshot is evidence aid only — **ban** `verify_mcp_only`.

MCP play evidence: `Factory-DRB/slice-briefs/_evidence/stalberg_visual_r1_planar_v2.png`

## Out of Success

- dual paint / tiles / connectors / art / Terrain3D
- tutorial s1–s6 occupancy dual language
- Curator push
- Claiming ask_success before operator F5
