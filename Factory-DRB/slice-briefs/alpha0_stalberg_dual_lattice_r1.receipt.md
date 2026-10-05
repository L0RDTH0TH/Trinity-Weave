---
title: Staging receipt — alpha0_stalberg_dual_lattice_r1
slice_id: alpha0_stalberg_dual_lattice_r1
ask_id: alpha0_stalberg_dual_lattice
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2d
producer_run_id: sp-tdl-20261003
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
completed: 2026-10-03T21:30:00Z
status: superseded_partial_wrong_object
superseded_by: alpha0_stalberg_dual_lattice_r2
prior_slice_id: alpha0_stalberg_dual_neighborhood_r1
prior_altitude: partial_wrong_object_primary_face_2x2
logic_prior_slice_id: alpha0_stalberg_dual_corner_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
trinity_sha: 4521af3ac886e5bdc3237749a68dee9e65147a5b
prefer_main_sha: 09f1474f5f2f6d058f6e195b59a749e63a96002a
density_lift: deferred_until_pipeline_ask_success
dual_visual_ask_success: paused_until_dual_lattice_green
---

# Staging receipt — `alpha0_stalberg_dual_lattice_r1`

**SUPERSEDED** by [[alpha0_stalberg_dual_lattice_r2]]. r1 staging Prefer without concept Prefer — `partial_wrong_object` product altitude.

**claim_class: staging** (historical). Prefer authorship **ok**. Dual-visual ask_success remains **out**. **No Curator.**

## Agree rationale

`dual_neighborhood_r1` Prefer-ok'd **stable** ≤4 ownership of the **wrong object** (cyan 2×2 primary organic faces). This Prefer adds `primary_face_as_dual` refuse + `OrganicDualOffsetLattice` half-step dual keys / Varignon tiles.

## Prefer (primary)

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_lattice_r1.prefer-result.json` → ok |
| do_not_waive | `primary_face_as_dual` · `unstable_dual_neighborhood` · `stamp_as_dual` · `over_neighbor_paint` · `skip_dual_offset` |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_lattice_r1/implicit-intent-bind.json` |
| Host law | [[Prefer-Authorship-Host-Law]] § C.0b · [[Grid-Topology-Host-Law]] |
| LIVE compile | `dotnet build` GenesisMythos.csproj — **0 errors** |

## LIVE weld

| Check | Evidence |
|-------|----------|
| Dual lattice type | `Core/WorldGen/OrganicDualOffsetLattice.cs` — DualCellsTouching, IsHalfStepOffset, VarignonMidpoints |
| Host | `Systems/DualGridCraftHost.cs` — OwnedDualCellKeys, EnsureHalfStepDualCellMesh, highlight on dual keys `d_*` |
| Prove | `ProveStableDualNeighborhood` requires half-step centres + stable ≤4 dual keys |
| Preserved | organic underlay · craft-plane authority · rings=2 · spacing=3.0 · Terrain3D OFF · Hex19 not Success |

## MCP evidence

Godot MCP `run_scene` timed out after C# rebuild (editor busy). Prefer + `dotnet build` green. Operator F5 + optional MCP a/b still required for ask_success.

## Operator F5 checklist (vs Final-Grid / Townscaper dual grammar)

1. Open `res://scenes/WorldgenCraft.tscn` — dual overlay on (**D**).
2. Click an **interior logic point** (vertex / corner) — cyan highlight must sit on **half-step dual tiles** (Varignon / inset, labels `d_*`), **not** a filled 2×2 of primary yellow-wire faces.
3. Repeat the same click — owned dual-cell set identical every time (≤4).
4. Confirm organic yellow underlay silhouette + rings≈2 / spacing=3.0; Terrain3D OFF.
5. Attest `ask_success` only when dual lattice ownership is product-legible; then re-arm dual_visual r3.

## Related

- Prior partial [[alpha0_stalberg_dual_neighborhood_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Next [[alpha0_stalberg_dual_visual_r3]] after F5
