---
title: Staging receipt — alpha0_stalberg_quad_kernel_relax_r1
slice_id: alpha0_stalberg_quad_kernel_relax_r1
ask_id: alpha0_stalberg_quad_kernel
producer_run_id: sp-sqkr-a1f7c2
claim_class: staging
factory_greenlit: false
prefer_authorship_pass: ok
completed: 2026-10-03T08:05:00Z
status: failed_altitude_relax_squarify_fail
prior_weld_altitude: failed_altitude_relax_squarify_fail
altitude_class: relax_squarify_fail
approach_status: intact
operator_f5_at: 2026-10-03
next_ticket: alpha0_stalberg_quad_kernel_relax_r2
prior_slice_id: alpha0_stalberg_quad_kernel_visual_r1
prior_producer_run_id: sp-sqkv-29460a
lerg_yt: https://youtu.be/Jm3pLya3d9c
trinity_sha: 8f0cb066e955dfa8e9dce8342ddf7282f4979021
mcp_screenshot_at_weld: none
mcp_audit_screenshot: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/_evidence/stalberg_relax_r1_f5_audit.png
goal_image: Ingest/Final-grid-state.jpg
---

# Staging receipt — `alpha0_stalberg_quad_kernel_relax_r1`

**ALTITUDE FAIL — relax/squarify fidelity (not approach).** Prefer staging seats OK (`prefer_authorship_pass`); operator F5 failed vs [[Ingest/Final-grid-state.jpg]]. LIVE MCP audit shot = spike/star clump (`_evidence/stalberg_relax_r1_f5_audit.png`) — not filled hex irregular all-quad board. **No `take_screenshot` evidence was attached at weld/staging time** (ban `verify_mcp_only` only). Approach (pipeline order) stays. Follow-on Prefer: [[alpha0_stalberg_quad_kernel_relax_r2]] (draft, `factory_greenlit: false`). No tutorial s1–s6 claim. No dual paint / tiles / art / Terrain3D Success. No Curator. **No ask_success.**

## Identity

| Field | Value |
|-------|--------|
| producer_run_id | `sp-sqkr-a1f7c2` |
| armed packet | `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_quad_kernel_relax_r1.armed.yaml` |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| greenlit_at | `2026-10-03T07:59:01Z` |

## Pipeline stages hit (code)

1. `SeedHexLatticeRings` via `UniqueTopology2D.GetOrAddVertex` (position-hash)
2. `TriangulateHexLattice`
3. `DissolveTrianglePairs` (unpaired tris OK)
4. `SubdivideFacesToQuads` → 100% quads **before** relax
5. `UniqueTopology2D.FromIndexedMesh` — singleton verts by `PositionHash`
6. `EstimateIdealSideFromArea` → side = √(mean area); half-diagonal D for square targets
7. `RelaxTowardSquares` — closest-square (not Laplacian); pull 0.10; `ClampForce`; `MarkBoundaryPinned`
8. `WeldNearDuplicates` post-relax
9. `FlattenToCraftPlane` — 2D stable; no extrusion-before-stable
10. Render opaque `OrganicQuadFaces` + depth-tested unique `OrganicQuadEdges`; R = regenerate

## Grok refuse seats armed

| Code | Seat |
|------|------|
| `non_unique_vertices` | UniqueTopology2D / GetOrAddVertex / PositionHash |
| `missing_square_area_force` | EstimateIdealSideFromArea |
| `naive_laplacian_only` | closest-square + area side required with relax |
| `free_boundary_fold` | MarkBoundaryPinned |
| `relax_step_too_hard` | ClampForce + pull ∈ [0.05,0.15] |
| `extrusion_before_2d_stable` | FlattenToCraftPlane with relax; planar Vector2 path |
| `relax_before_quad_only` | dissolve+subdivide before relax; AllFacesAreQuads gate |

Plus prior visual/kernel refuses (noodle/prism/hex/dual/points…).

## LIVE files

- `Core/WorldGen/StalbergQuadKernel.cs` (+ `UniqueTopology2D`)
- `Core/WorldGen/OrganicQuadMesh.cs`
- `Systems/DualGridCraftHost.cs`
- `Systems/WorldgenCraft.cs`

## Focus cites

- oskar docs/02 · [[lerg-townscaper-godot/README]] (https://youtu.be/Jm3pLya3d9c) · [[Grid-Topology-Host-Law]] · [[Prefer-Authorship-Host-Law]]
- Prior [[alpha0_stalberg_quad_kernel_visual_r1.receipt]] (superseded authority)

## F5 bar (operator)

Readable **planar** irregular all-quad mesh after area-square relax; clean edges (no noodle spikes from duplicate verts); boundary stable; regenerate (R); graybox OK. Staging until operator attests. Ban `verify_mcp_only`.

## Result (operator + MCP audit)

| Field | Value |
|-------|--------|
| Result | **`failed_altitude_relax_squarify_fail`** |
| Operator F5 | fail — noodles “better” but wrong vs goal |
| MCP at weld | **not used** (no `_evidence/` for relax_r1 until audit) |
| MCP audit now | spike/star clump ≠ Final-grid-state |
| Next Prefer | [[alpha0_stalberg_quad_kernel_relax_r2]] — draft, await GREENLIGHT WELD |

## Out of Success

- dual paint / tiles / connectors / art / Terrain3D
- tutorial s1–s6
- Curator push
- Claiming ask_success before operator F5
- Claiming Success from Prefer staging seats alone
