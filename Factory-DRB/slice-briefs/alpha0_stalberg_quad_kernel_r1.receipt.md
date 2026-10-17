---
title: Staging receipt — alpha0_stalberg_quad_kernel_r1
slice_id: alpha0_stalberg_quad_kernel_r1
ask_id: alpha0_stalberg_quad_kernel
producer_run_id: sp-sqk-3210b7
claim_class: staging
factory_greenlit: false
prefer_authorship_pass: ok
completed: 2026-10-03T07:16:18Z
status: failed_altitude_visual_execution_fail
prior_weld_altitude: failed_altitude_visual_execution_fail
altitude_class: visual_execution_fail
approach_status: intact
next_ticket: alpha0_stalberg_quad_kernel_visual_r1
operator_f5_at: 2026-10-03
operator_screenshot: /home/darth/.cursor/projects/home-darth-Documents-Second-Brain/assets/image-6abba0cc-ef21-4089-9adc-eb30636da82b.png
---

# Staging receipt — `alpha0_stalberg_quad_kernel_r1`

**ALTITUDE FAIL — visual execution (not approach).** Operator F5 read as overlapping semi-transparent prism/quad fills + tangled white wire edges ("mess of noodles"); no clear planar board. Pipeline approach (seed→tri→dissolve→subdivide→relax) remains correct. Follow-on Prefer: [[alpha0_stalberg_quad_kernel_visual_r1]] (draft). No tutorial s1–s6 claim. No dual paint / tiles / art / Terrain3D Success. No Curator.

## Identity

| Field | Value |
|-------|--------|
| producer_run_id | `sp-sqk-3210b7` |
| staged job | `factory-weld-sqk-202-module-c2f365` |
| armed packet | `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_quad_kernel_r1.armed.yaml` |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |

## Pipeline stages hit (code)

1. `SeedHexLatticeRings` (Variant B hex rings, tunable)
2. `TriangulateHexLattice`
3. `DissolveTrianglePairs`
4. `SubdivideFacesToQuads` → 100% quads (face valence 4)
5. `RelaxTowardSquares`
6. Render `OrganicQuadFaces` + `OrganicQuadEdges`; `RegenerateOrganicQuadMesh` (R)

## LIVE files

- `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/Core/WorldGen/StalbergQuadKernel.cs`
- `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/Core/WorldGen/OrganicQuadMesh.cs`
- `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/Systems/DualGridCraftHost.cs`
- `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/Systems/WorldgenCraft.cs`

## Prefer evidence

- **ok:** `True`
- **detail:** prefer_authorship_pass_ok
- **violations:** `[]`
- Refuse seats armed: `hex_scaffold_as_final_mesh` / `dual_overlay_as_grid_kernel` / `skip_dissolve_relax` / `points_as_grid`
- Hex19* is NOT Success type; dual overlay refused on this Prefer

## F5 bar (operator)

Irregular quads primary; hex not primary board; regenerable (R); pipeline in code. Staging until operator attests.

### Operator F5 outcome (2026-10-03)

| Field | Value |
|-------|--------|
| Result | **`failed_altitude_visual_execution_fail`** |
| Approach | **intact** — do not re-litigate pipeline |
| Visual | Dense overlapping dark translucent polys + white edge spaghetti; not a planar quad field |
| Next Prefer | [[alpha0_stalberg_quad_kernel_visual_r1]] — planar readable board / coherent surface |

## Out of Success

- dual paint / tiles / connectors / art / Terrain3D
- tutorial s1–s6 occupancy dual language
- Curator push
- Claiming this receipt as ask_success after noodle/prism F5
