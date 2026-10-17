---
title: Dual report B — intent-seat — alpha0_stalberg_dual_stage6_cell_r1
slice_id: alpha0_stalberg_dual_stage6_cell_r1
report: B
role: intent-seat
completed: 2026-10-04T05:05:00Z
claim_class: staging
---

# Dual report B — intent-seat

| Field | Value |
|-------|--------|
| Intent invariant | Player edits logic points (primal Vertices); dual cell around a logic point is the Stage-6 polygon of face centroids of faces incident to that point; dual vertices sit at main-face centres; dual edges connect those centroids across shared primal edges (cross main cells — never along main sides). |
| `success_object` | `dual_offset_cells` (correct edge/cell identity — intent validates gates) |
| Prefer path | **concept** (object identity + Stage-6 cell/edge invariant) |
| Refuse (binding) | `primary_face_as_dual` · `inset_face_corners_as_dual` · `face_corners_local_as_dual_edges` · `face_block_neighborhood` · `vertex_neighbor_as_dual_corner` · `proxy_substitution` · `intent_collapsed_to_mechanics` |
| Law | [[Grid-Topology-Host-Law]] · [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] · [[Prefer-Authorship-Host-Law]] § C.2 |
| Terminology | [[Untitled]] Final-Grid dual vocabulary |
| Bug proof | [[Ingest/Screenshot_20261004_003640_YouTube.jpg]] |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_stage6_cell_r1/implicit-intent-bind.json` |
| Compose | Slice Producer judgment `sp-s6c1-manual-greenlight` — conceptual leg present |
| Supersedes | [[alpha0_stalberg_dual_face_centroid_r1]] (Prefer ok; LIVE FaceCornersLocal wrong object) |

## Intent-seat verdict

Concept Prefer holds for `dual_offset_cells` under Stage-6 **cell/edge identity**. Selling inset FaceCornersLocal rings as dual Success is refused. Product `ask_success` / chain-advance to [[alpha0_stalberg_dual_visual_r3]] gated on operator F5.
