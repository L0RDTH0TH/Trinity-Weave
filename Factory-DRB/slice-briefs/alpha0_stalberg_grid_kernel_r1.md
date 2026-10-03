---
title: Series — alpha0_stalberg_grid_kernel_r1
slice_id: alpha0_stalberg_grid_kernel_r1
ask_id: alpha0_stalberg_quad_kernel
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-03
updated: 2026-10-03
claim_class: staging
factory_greenlit: true
status: dual_lattice_r1_greenlit_welding
template: Half-B-Weld-Brief-Template
active_step: 2d
active_step_slice_id: alpha0_stalberg_dual_lattice_r1
density_lift: deferred_until_pipeline_ask_success
dual_visual_ask_success: paused_until_neighborhood_green
manual_limit: hex19_seed_rings_2
source_yt: https://www.youtube.com/watch?v=Y19Mw5YsgjI
lerg_yt: https://youtu.be/Jm3pLya3d9c
algorithm_upstream: https://github.com/kai-denrei/oskar-procedure
goal_image: Ingest/Final-grid-state.jpg
---

# Series — `alpha0_stalberg_grid_kernel_r1`

**Thin product Prefer series** for Stålberg organic all-quad **grid kernel**, then craft-plane authority, then dual/corner. Separate from the Townscaper tutorial ladder ([[alpha0_townscaper_tutorial_r1]]).

Umbrella: [[alpha_architecture_half_b]]. Topology: [[Grid-Topology-Host-Law]]. Prefer: [[Prefer-Authorship-Host-Law]]. Goal visual: [[Ingest/Final-grid-state.jpg]].

## Ladder

| Step | Ticket | Scope | Greenlit | Notes |
|------|--------|-------|----------|-------|
| 1 | [[alpha0_stalberg_quad_kernel_r1]] | Organic all-quad pipeline | was true — altitude fail | Approach OK |
| 1b | [[alpha0_stalberg_quad_kernel_visual_r1]] | Planar readable board | superseded | — |
| 1c | [[alpha0_stalberg_quad_kernel_relax_r1]] | Unique topo + area square relax | altitude fail | — |
| 1d | [[alpha0_stalberg_quad_kernel_relax_r2]] | Goal fidelity draft | false | near-zero diag |
| 1e | [[alpha0_stalberg_topology_base_r1]] | Upstream injective topo + soft relax | staging recovered | kernel foundation |
| **1f** | [[alpha0_stalberg_craft_plane_authority_r1]] | Rebind pick/paint onto OrganicQuadMesh | **staging Prefer ok** | Hex19 not Success; MCP evidence |
| 2 | [[alpha0_stalberg_dual_corner_r1]] | Dual-corner **logic** on organic quads | **staging Prefer ok** — not product ask_success | gray ramp visual gap |
| **1g** | [[alpha0_stalberg_manual_scale_r1]] | Hex-19 / tutorial seed scale (rings=2) | **staging Prefer ok** | density lift deferred |
| **2b** | [[alpha0_stalberg_dual_visual_r1]] | Dual visual / MeshLibrary fidelity | **failed_altitude / partial** | Prefer ok then stretch-as-shape; see [[Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03]] |
| 2c′ | [[alpha0_stalberg_dual_visual_r2]] | Discrete silhouettes Prefer harden | **paused** — dual_visual ask_success deferred | Prefer harden landed; neighborhood first |
| **2c** | [[alpha0_stalberg_dual_neighborhood_r1]] | Stable dual-graph ownership (≤4) | **partial_wrong_object** | stable primary-face 2×2; superseded by 2d |
| **2d** | [[alpha0_stalberg_dual_lattice_r1]] | True half-step dual lattice ownership | **GREENLIT welding** | refuse `primary_face_as_dual` + neighborhood refuses |
| 2e | [[alpha0_stalberg_dual_visual_r3]] | Dual visual on correct dual lattice | draft (after 2d green) | next_in_chain |

## Active authority

| Field | Value |
|-------|--------|
| Active step | **2d** — [[alpha0_stalberg_dual_lattice_r1]] (**GREENLIT**; Prefer `primary_face_as_dual`) |
| Kernel foundation | [[alpha0_stalberg_topology_base_r1]] |
| Manual limit | rings=2 (~54 quads) + spacing=3.0 (large cells) — Prefer edges+faces |
| Density lift | **deferred** until pipeline `ask_success` |
| Dual visual | **paused** until dual **lattice** green (`ask_success` not in play) |
| Prior Prefer ok (staging) | craft-plane · dual_corner (logic only) · manual_scale |
| Dual visual r1 | **failed_altitude / partial** — not product Success |
| Prefer audit | [[Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03]] |
| Tutorial ladder | cite-only — [[alpha0_townscaper_tutorial_r1]] |

## Related

- [[alpha0_stalberg_dual_lattice_r1]] · [[alpha0_stalberg_dual_neighborhood_r1]] · [[alpha0_stalberg_dual_visual_r2]] · [[alpha0_stalberg_dual_visual_r1]] · [[Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03]] · [[Prefer-Authorship-Host-Law]] · [[Half-B-Weld-Brief-Template]]
