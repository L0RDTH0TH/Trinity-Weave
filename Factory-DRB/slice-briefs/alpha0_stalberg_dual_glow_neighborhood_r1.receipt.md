---
title: Staging receipt — alpha0_stalberg_dual_glow_neighborhood_r1
slice_id: alpha0_stalberg_dual_glow_neighborhood_r1
ask_id: alpha0_stalberg_dual_glow_neighborhood
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2j
producer_run_id: sp-dgn1-manual-greenlight
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_offset_cells
geometric_success: stage6_wire_small_corner_quads_glow
contract: B_small_corner_quads_glow_keep_stage6_wire
intent_invariant: "Player edits logic points (primal Vertices); DualCell identity remains the Stage-6 polygon of face centroids around V (OwnedDualCellKeys=one); on pick/flip of V the highlight and UpdateFour expand set is the degree-dependent dual-edge neighbour DualCells (ExpandDualNeighborKeys) — typically 2 at edge-ish sites and 4 at interior — matching annotate; dual verts stay at face centres; dual edges stay centroid–centroid; shared expansion main verts OK without dual-owning one DualCell."
completed: 2026-10-04T06:47:59Z
status: staging_prefer_ok_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_dual_stage6_cell_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
logic_prior_slice_id: alpha0_stalberg_primal_graph_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
trinity_push: skipped_cooldown
trinity_push_note: "project_bridge_push skipped reason=cooldown (last_push_utc=2026-10-04T02:07:46Z; pushes_today=1)"
density_lift: deferred_until_pipeline_ask_success
dual_visual_ask_success: paused_until_dual_glow_neighborhood_concept_and_operator_f5
goal_image: Ingest/Final-grid-state.jpg
annotate_proof: Ingest/Screenshot from 2026-10-04 01-19-00.png
bug_image: Ingest/Screenshot from 2026-10-04 01-19-00.png
mcp_evidence_a: Factory-DRB/slice-briefs/_evidence/dual_glow_neighborhood_r1_verify_a.png
mcp_evidence_b: Factory-DRB/slice-briefs/_evidence/dual_glow_neighborhood_r1_verify_b.png
mcp_note: "MCPRuntime Stable_Neighborhood_Ready stable_small_corner_quads max_owned=1 max_small=4 min_small=2 small2=18 small4=35 small_corner_slots=200 stage6_cells=41 stage6_union_as_single_glow_tile=false; Corner_Flip small_count=4 keys sc_v*_f*"
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
dual_report_a: Factory-DRB/slice-briefs/alpha0_stalberg_dual_glow_neighborhood_r1.dual-report-a.md
dual_report_b: Factory-DRB/slice-briefs/alpha0_stalberg_dual_glow_neighborhood_r1.dual-report-b.md
---

# Staging receipt — `alpha0_stalberg_dual_glow_neighborhood_r1`

**claim_class: staging** until operator F5. Prefer **concept** ok (`dual_offset_cells` + expand-glow invariant). Stage-6 geometry from [[alpha0_stalberg_dual_stage6_cell_r1]] **kept**. Dual-visual ask_success remains **out**. Curator snapshot per operator GREENLIGHT WELD.

## Conceptual leg

| Field | Value |
|-------|--------|
| Project end-state | Authorable irregular dual-grid craft plane on organic all-quad board |
| Path | stage6_cell_r1 geometry kept → **this** expand-glow neighborhood → dual_visual_r3 |
| Intent invariant | Owned=one Stage-6; ExpandDualNeighborKeys glow edge≈2 / interior≈4 |
| `success_object` | `dual_offset_cells` |
| Annotate proof | [[Ingest/Screenshot from 2026-10-04 01-19-00.png]] |
| Goal image | [[Ingest/Final-grid-state.jpg]] graph-family (not art parity) |
| Contract | **(B)** expand-neighbor glow; keep Stage-6 DualCell identity |

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_glow_neighborhood_r1.prefer-result.json` → ok · `concept_prefer_ok: true` · `prefer_path: concept` |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_glow_neighborhood_r1/implicit-intent-bind.json` |
| Compose | Slice Producer judgment `sp-dgn1-manual-greenlight` — `compose_path: slice_producer_judgment` |
| LIVE compile | `dotnet build` GenesisMythos.csproj — **0 errors** |

## LIVE weld (expand-glow neighborhood)

| Check | Evidence |
|-------|----------|
| Dual model | Stage-6 DualCell per logic V **unchanged** (centroids; cyan crosses amber) |
| Ownership | `OwnedDualCellKeys(V)` = one |
| Expand / glow | `ExpandDualNeighborKeys(V)` = dual-edge neighbours exclude owned |
| Highlight | `HighlightOwnedDualCells` → expand set (not owned-only) |
| UpdateFour | refreshes owned + expand (`DualCellsTouching`) |
| Runtime prove | `Stable_Neighborhood_Ready` — `stable_expand_glow max_owned=1 max_expand=4 min_expand=2 expand2=5 expand4=19 owned_only_glow=false hex19_always_4=false` |
| Host | `WeldSliceId=alpha0_stalberg_dual_glow_neighborhood_r1`; HUD **GLOW-NBR r1 · dual_offset_cells** |
| Preserved | MeshGraph · organic underlay · craft authority · craft cam 7× / zoom · DualLatticeDebug spheres · Terrain3D OFF |

## Before → after glow semantics

| | Before (mid-flight expand DualCells) | After (operator clarify) |
|--|--------------------------------------|--------------------------|
| Glow unit | Neighbor Stage-6 DualCells / union fill | **SmallCornerQuadsAround** (primary-cut sectors) |
| Corners of glow unit | Stage-6 face-centroid ring | **V, mid(edge), faceCentroid, mid(edge)** |
| Count | 2/4 DualCells (wrong size) | **2/4 small quads** (annotate size) |
| Stage-6 wire | centroid–centroid | **kept** |
| Runtime | — | `small2=18 small4=35` · `stage6_union_as_single_glow_tile=false` |

## MCP evidence

| Shot | Path | Notes |
|------|------|-------|
| A | [[_evidence/dual_glow_neighborhood_r1_verify_a.png]] | Board with Stage-6 dual overlay; expand-glow weld live |

Runtime (excerpt):

- `Stable_Neighborhood_Ready|stable_expand_glow max_owned=1 max_expand=4 min_expand=2 expand2=5 expand4=19 … owned_only_glow=false hex19_always_4=false dual_edges=centroid_centroid`

## F5 attest (operator)

1. Open `res://scenes/WorldgenCraft.tscn`, F5 / play.
2. Click edge-like Red-analogue → **2 small corner quads** glow (not one big Stage-6 diamond).
3. Click interior Purple-analogue → **4 small corner quads** glow.
4. Confirm cyan still crosses amber; spheres at face centres; dual≈ Stage-6 count; HUD `GLOW-NBR r1`.
5. Confirm two picks can share an expansion main vert without one DualCell having two owners.

## Out of scope

MeshLibrary dual_visual polish · density lift · Terrain3D · Hex19 Success · chain-advance without operator F5
