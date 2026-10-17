---
title: Staging receipt — alpha0_stalberg_craft_plane_authority_r1
slice_id: alpha0_stalberg_craft_plane_authority_r1
ask_id: alpha0_stalberg_quad_kernel
producer_run_id: sp-tcpa-20261003
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
completed: 2026-10-03T18:06:37Z
status: staging_awaiting_operator_f5
altitude_class: craft_plane_authority_rebound
prior_slice_id: alpha0_stalberg_topology_base_r1
next_in_chain: alpha0_stalberg_dual_corner_r1
trinity_branch: project/genesis-mythos-master
mcp_evidence: Factory-DRB/slice-briefs/_evidence/stalberg_craft_plane_authority_r1.png
---

# Staging receipt — `alpha0_stalberg_craft_plane_authority_r1`

**claim_class: staging** until operator F5. Prefer authorship **ok**. MCP evidence: organic board readable; HUD `OrganicQuadMesh`; painted face plates on organic quads; Terrain3D OFF. Hex19 is **not** Success pick/paint path (`TryPickOrganicFace` / `FaceCell`). Kernel pipeline intact. **No Curator.**

## Identity

| Field | Value |
|-------|--------|
| producer_run_id | `sp-tcpa-20261003` |
| prior | [[alpha0_stalberg_topology_base_r1]] |
| armed packet | `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_craft_plane_authority_r1.armed.yaml` |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |

## LIVE changes

- `Core/WorldGen/OrganicQuadMesh.cs` — `TryPickFace` / `FaceCell` / face geometry helpers
- `Core/WorldGen/ICraftCellAuthority.cs` — face-cell occupancy docs
- `Systems/DualGridCraftHost.cs` — `TryPickOrganicFace`, organic `SetCellFill`, `ProveCraftPlaneAuthority`, ghost on craft plane
- `Systems/WorldgenCraft.cs` — craft-plane tip / prove path

## Prefer

- `prefer_authorship_pass: ok`
- Craft-plane seat: no `hex19_pick_as_craft_authority` (no `TrySnapWorldToCell` in pick)
- Organic kernel seats green (edges+faces)
- Result: `alpha0_stalberg_craft_plane_authority_r1.prefer-result.json`

## MCP evidence

- `_evidence/stalberg_craft_plane_authority_r1.png` — denim organic quads + yellow edges; painted face cluster; HUD OrganicQuadMesh / Terrain3D OFF

## Out of Success

- dual_corner paint (next ticket)
- tiles / art / Terrain3D / Hex19 tutorial Success
- Curator push

## Operator F5

1. WorldgenCraft — LMB/RMB paint organic faces (not hex-19 cells).
2. Confirm kernel board still readable vs Final-grid-state.
3. Then allow greenlight of [[alpha0_stalberg_dual_corner_r1]] (chained).
