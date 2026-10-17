---
title: Staging receipt — alpha0_stalberg_dual_corner_r1
slice_id: alpha0_stalberg_dual_corner_r1
ask_id: alpha0_stalberg_dual_corner
producer_run_id: sp-tdc-20261003
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
completed: 2026-10-03T18:12:16Z
status: staging_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_craft_plane_authority_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
mcp_evidence_a: Factory-DRB/slice-briefs/_evidence/stalberg_dual_corner_r1_a.png
mcp_evidence_b: Factory-DRB/slice-briefs/_evidence/stalberg_dual_corner_r1_b.png
---

# Staging receipt — `alpha0_stalberg_dual_corner_r1`

**claim_class: staging** until operator F5. Prefer authorship **ok**. Chained after craft_plane_authority Prefer+staging success. **No Curator.**

## Proof

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_corner_r1.prefer-result.json` → ok |
| Dual armed | factory-runtime: `organic dual-corner cells armed — unique_cells=320` |
| Corner flip | `Corner_Flip organic corner=249 … dual_cells_refreshed=4` and `corner=130 … refreshed=4` |
| Board | MCP screenshots a/b — organic edges+faces preserved; Terrain3D OFF |

## LIVE

- `DualGridCraftHost` — `TryPickOrganicCorner`, `FlipOrganicCorner`, `BuildOrganicDualCornerOverlay`, organic `UpdateFourDualSlots`
- Craft-plane authority retained (organic pick/paint path)
- Hex19 / tiles / art / Terrain3D not Success

## Operator F5

1. WorldgenCraft — LMB near a corner; confirm up to four dual cells recolor/rebuild.
2. Organic board still readable vs Final-grid-state.
3. Attest ask_success when house bar met.

## Authority hand-off (2026-10-03)

**Not** product `ask_success`. Operator F5 showed adjacency via gray ramp only. Next Prefer draft: [[alpha0_stalberg_dual_visual_r1]] (MeshLibrary / shape-distinct variants; refuse `gray_ramp_only`).
