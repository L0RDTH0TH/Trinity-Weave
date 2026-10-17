---
title: Staging receipt — alpha0_stalberg_dual_mesh_fit_r1
slice_id: alpha0_stalberg_dual_mesh_fit_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2m
producer_run_id: sp-mesh-fit-r1-manual-greenlight
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_offset_cells
contract: C_mesh_fit_four_corner_pieces_to_secondary_quad
completed: 2026-10-04T19:35:51Z
status: staging_prefer_ok_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_dual_visual_r3
r3_pass: true
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
trinity_push: skipped_push_disabled
trinity_push_note: "project_bridge_push skipped; curator_snapshot local commit only (git.push_enabled false)"
density_lift: live_rings_5_spacing_210
warp_method: bilinear_uv_skin_to_SmallCornerQuad_Corners
meshlibrary_path: assets/craft/dual_grid/
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
---

# Staging receipt — `alpha0_stalberg_dual_mesh_fit_r1`

**claim_class: staging** until operator F5. Prefer **concept** ok. Four corner/sector pieces mesh-fit (bilinear warp) onto secondary `SmallCornerQuad.Corners`. Curator **local** snapshot only (`git.push_enabled: false`).

## r3_pass gate (precondition)

| Check | Evidence |
|-------|----------|
| Hypothesis | Dual/secondary slots show discrete empty/edge/corner/full GLB cubes/blocks |
| LIVE | `PlaceDiscreteDualLibraryItem` + `assets/craft/dual_grid/craft_dual_*.glb` |
| Runtime | WorldgenCraft playing; CraftHint DUAL-VISUAL r3; OrganicDualOffsetOverlay **1272** MeshInstance3D (Empty 1220 / Corner 32 / Edge 16 / Full 4); dual overlay ON by default (D toggles) |
| Screenshot | `addons/godot_mcp/cache/screenshots/stalberg_dual_visual_r3_verify.png` |
| Verdict | **r3_pass: true** — proceed to mesh-fit |

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_mesh_fit_r1.prefer-result.json` → ok · `concept_prefer_ok: true` |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_mesh_fit_r1/implicit-intent-bind.json` |
| LIVE compile | `dotnet build` GenesisMythos.csproj — **succeeded** |

## LIVE weld

| Item | Path / note |
|------|-------------|
| Host | `Systems/DualGridCraftHost.cs` — `MeshFitToSmallCornerQuad` bilinear skin; Empty fast rim on true Corners |
| Entry | `Systems/WorldgenCraft.cs` — HUD DUAL MESH-FIT r1 |
| Place law | vertex warp to SmallCornerQuad.Corners (+ rot/mirror UV orient); **not** Scale stretch |
| Kept | Stage-6 wire · secondary glow · squarify Stage 5 · rings=5 spacing=210 · discrete family ids |

## Warp method summary

Canonical MeshLibrary footprint UV (XZ AABB → [0,1]²) bilinear-maps onto oriented `SmallCornerQuad.Corners` = V · edge-mid(next) · face-centroid · edge-mid(prev). Height kept via uniform heightScale from slot diagonal. Rot90/mirror permute target corners before warp. Empty uses thin rim generated on those edges (four corner pieces still hug).

## Operator F5

1. Open `res://scenes/WorldgenCraft.tscn`, F5; dual overlay on (D).
2. Sector pieces should **hug** secondary edges — not rigid cubes floating at centres, not stretched plates.
3. Families empty/edge/corner/full still distinct after flips.
4. Stage-6 + secondary glow + rings=5 spacing=210 intact.
5. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_mesh_fit_r1]] · Prior [[alpha0_stalberg_dual_visual_r3]] · Series [[alpha0_stalberg_grid_kernel_r1]]
