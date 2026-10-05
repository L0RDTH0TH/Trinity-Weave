---
title: Staging receipt — alpha0_stalberg_dual_stage6_cell_r1
slice_id: alpha0_stalberg_dual_stage6_cell_r1
ask_id: alpha0_stalberg_dual_stage6_cell
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2i
producer_run_id: sp-s6c1-manual-greenlight
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_offset_cells
geometric_success: stage6_dual_cell_around_logic_vertex_centroid_edges
intent_invariant: "Player edits logic points (primal Vertices); dual cell around a logic point is the Stage-6 polygon of face centroids of faces incident to that point; dual vertices sit at main-face centres; dual edges connect those centroids across shared primal edges (cross main cells — never along main sides)."
completed: 2026-10-04T05:10:00Z
status: staging_prefer_ok_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_dual_face_centroid_r1
supersedes: alpha0_stalberg_dual_face_centroid_r1
logic_prior_slice_id: alpha0_stalberg_primal_graph_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
density_lift: deferred_until_pipeline_ask_success
dual_visual_ask_success: paused_until_dual_stage6_cell_concept_and_operator_f5
goal_image: Ingest/Final-grid-state.jpg
bug_image: Ingest/Screenshot_20261004_003640_YouTube.jpg
mcp_evidence_a: Factory-DRB/slice-briefs/_evidence/dual_stage6_cell_r1_verify_a.png
mcp_note: "MCPRuntime Stable_Neighborhood_Ready stable_stage6_dual_cell max_owned=1 owned_exact1=42 dual_cells=43 face_corners_local=false dual_edges=centroid_centroid; HUD STAGE6-CELL r1 dual=43 (not face-count 52)"
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
dual_report_a: Factory-DRB/slice-briefs/alpha0_stalberg_dual_stage6_cell_r1.dual-report-a.md
dual_report_b: Factory-DRB/slice-briefs/alpha0_stalberg_dual_stage6_cell_r1.dual-report-b.md
---

# Staging receipt — `alpha0_stalberg_dual_stage6_cell_r1`

**claim_class: staging** until operator F5. Prefer **concept** ok (`dual_offset_cells` + Stage-6 cell/edge identity). Dual-visual ask_success remains **out**. Curator snapshot per operator GREENLIGHT WELD.

## Conceptual leg

| Field | Value |
|-------|--------|
| Project end-state | Authorable irregular dual-grid craft plane on organic all-quad board |
| Path | primal_graph → dual_rebind aborted → dual_face_centroid Prefer-ok/LIVE-wrong → **this** Stage-6 cell/edge rebind → dual_visual_r3 |
| Intent invariant | Dual cell = Stage-6 polygon of incident face centroids; dual edges cross main cells |
| `success_object` | `dual_offset_cells` |
| Bug proof | [[Ingest/Screenshot_20261004_003640_YouTube.jpg]] cyan overlay amber |
| Goal image | [[Ingest/Final-grid-state.jpg]] graph-family (not art parity) |
| Terminology | [[Untitled]] Final-Grid dual vocabulary |

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_stage6_cell_r1.prefer-result.json` → ok · `concept_prefer_ok: true` · `prefer_path: concept` |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_stage6_cell_r1/implicit-intent-bind.json` |
| Compose | Slice Producer judgment `sp-s6c1-manual-greenlight` — `compose_path: slice_producer_judgment` |
| LIVE compile | `dotnet build` GenesisMythos.csproj — **0 errors** |

## LIVE weld (Stage-6 cell identity)

| Check | Evidence |
|-------|----------|
| Dual model | `OrganicDualOffsetLattice` — one DualCell per logic Vertex; `DualCorners` = face centroids; `LocalCentre` = V |
| Ownership | `OwnedDualCellKeys(V)` = one; `DualCellsTouching` = owned + dual-edge neighbours |
| Wireframe | Stage-6 polygons only — **no** FaceCornersLocal dual edges |
| Paint | `Stage6CornersLocal` N-gon multi-hue segments when owner ON |
| Runtime prove | `Stable_Neighborhood_Ready` — `stable_stage6_dual_cell max_owned=1 owned_exact1=42 dual_cells=43 face_corners_local=false dual_edges=centroid_centroid` |
| Host | `WeldSliceId=alpha0_stalberg_dual_stage6_cell_r1`; HUD **STAGE6-CELL r1 · dual_offset_cells** · dual=43 |
| Preserved | MeshGraph · organic underlay · craft authority · craft cam · Terrain3D OFF |

## Before → after dual identity

| | Before (dual_face_centroid LIVE) | After (this weld) |
|--|----------------------------------|-------------------|
| DualCell | 1:1 primal Face | Stage-6 cell around logic V |
| LocalCentre | Face centroid | Logic Vertex (placement) |
| Dual verts | Face centroid (as cell centre) | Face centroids (`DualCorners`) |
| Dual edges | FaceCornersLocal inset rings ≈ shrunk primary | Centroid–centroid Stage-6 sides (cross amber) |
| Owned keys | ≤4 face duals sampling V | Exactly one Stage-6 cell |
| Cell count | ~face count (52) | editable logic verts (43) |

## MCP evidence

| Shot | Path | Notes |
|------|------|-------|
| A | [[_evidence/dual_stage6_cell_r1_verify_a.png]] | Board with Stage-6 dual overlay; HUD STAGE6-CELL; dual=43 |

Runtime (excerpt):

- `Stable_Neighborhood_Ready|stable_stage6_dual_cell max_owned=1 … face_corners_local=false dual_edges=centroid_centroid …`

## F5 attest (operator)

1. Open `res://scenes/WorldgenCraft.tscn`, F5 / play.
2. Confirm cyan dual edges connect face-centroid spheres and **cross** amber main cells (not overlay / inset-along sides).
3. LMB a logic intersection → one dual tile centered on that point with multi-hue segments.
4. Confirm HUD `STAGE6-CELL r1` and dual count ≈ logic verts (not face count).

## Out of scope

MeshLibrary dual_visual polish · density lift · Terrain3D · Hex19 Success · chain-advance without operator F5
