---
title: Staging receipt — alpha0_stalberg_dual_face_centroid_r1
slice_id: alpha0_stalberg_dual_face_centroid_r1
ask_id: alpha0_stalberg_dual_face_centroid
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2h
producer_run_id: sp-fcr1-4205d9
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_offset_cells
geometric_success: stage6_face_centroid_dual_verts_hex19_polarity
intent_invariant: "Player edits logic points (primal Vertices); dual cell around a logic point is the polygon of face centroids of faces incident to that point; dual vertices sit at main-face centres."
completed: 2026-10-04T03:31:16Z
status: staging_prefer_ok_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_primal_graph_r1
supersedes: alpha0_stalberg_dual_rebind_r1
logic_prior_slice_id: alpha0_stalberg_primal_graph_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
trinity_sha: ebc8200503cf7232e1c07fddc1aa76b715a80905
prefer_main_sha: b4547f2b4deb5195866497c590cd578a936f3bc5
density_lift: deferred_until_pipeline_ask_success
dual_visual_ask_success: paused_until_dual_face_centroid_concept_and_operator_f5
goal_image: Ingest/Final-grid-state.jpg
mcp_evidence_a: Factory-DRB/slice-briefs/_evidence/dual_face_centroid_r1_verify_a.png
mcp_evidence_b: Factory-DRB/slice-briefs/_evidence/dual_face_centroid_r1_verify_b.png
mcp_note: "MCPRuntime connected; Stable_Neighborhood_Ready face_centroid=true hex19_half_step=true; corner=25 keys identical on repeat; cyan inset duals at face centres"
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
dual_report_a: Factory-DRB/slice-briefs/alpha0_stalberg_dual_face_centroid_r1.dual-report-a.md
dual_report_b: Factory-DRB/slice-briefs/alpha0_stalberg_dual_face_centroid_r1.dual-report-b.md
---

# Staging receipt — `alpha0_stalberg_dual_face_centroid_r1`

**claim_class: staging** until operator F5. Prefer **concept** ok (`dual_offset_cells` + face-centroid invariant). Dual-visual ask_success remains **out**. **No Curator.**

## Conceptual leg

| Field | Value |
|-------|--------|
| Project end-state | Authorable irregular dual-grid craft plane on organic all-quad board |
| Path | primal_graph_r1 MeshGraph → dual_rebind aborted (wrong locus) → **this** Stage-6 face-centroid dual → dual_visual_r3 |
| Intent invariant | dual cell around logic point = polygon of incident face centroids; dual verts at main-face centres |
| `success_object` | `dual_offset_cells` |
| Goal image | [[Ingest/Final-grid-state.jpg]] graph-family (not art parity) |

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_face_centroid_r1.prefer-result.json` → ok · `concept_prefer_ok: true` · `prefer_path: concept` |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_face_centroid_r1/implicit-intent-bind.json` |
| Compose | Slice Producer judgment `sp-fcr1-4205d9` — `compose_path: slice_producer_judgment` |
| LIVE compile | `dotnet build` GenesisMythos.csproj — **0 errors** |

## LIVE weld (face-centroid)

| Check | Evidence |
|-------|----------|
| Dual model | `OrganicDualOffsetLattice` — one dual per primal Face; `LocalCentre` = face centroid |
| Ownership | `DualCellsTouching(P)` = duals sampling P as corner (FacesTouchingVertex) |
| Polarity | `IsHalfStepOffset` Hex19 — centre OFF logic verts; at face centroid |
| Proof | `ProveFaceCentroidAround` · `ProveDualIncidenceOwnership` refuse vertex-neighbour star / dual_rebind wrong locus |
| Runtime prove | `Stable_Neighborhood_Ready` — `stable_face_centroid_dual max_incident=4 interior_exact4=35 … half_step=52 face_centroid=true hex19_half_step=true vertex_neighbor_star=false dual_rebind_wrong_locus=false` |
| Host | `WeldSliceId=alpha0_stalberg_dual_face_centroid_r1`; HUD **FACE-CENTROID r1 · dual_offset_cells** |
| Preserved | MeshGraph · organic underlay · craft authority · rings=2 · spacing=3.0 · Terrain3D OFF |

## MCP evidence

| Shot | Path | Notes |
|------|------|-------|
| A | [[_evidence/dual_face_centroid_r1_verify_a.png]] | Cyan ≤4 inset dual tiles at face centres around logic point — not filled primal-face 2×2 |
| B | [[_evidence/dual_face_centroid_r1_verify_b.png]] | Post-flip board; HUD face-centroid copy |

Runtime (excerpt):

- `Stable_Neighborhood_Ready|stable_face_centroid_dual … face_centroid=true hex19_half_step=true … dual_rebind_wrong_locus=false`
- `Corner_Flip|organic corner=25 … owned=[d_10_23_24_25,d_10_25_43_44,d_14_23_25_26,d_14_25_32_43]` — same CSV on repeat query

## Dual reports

- A (outcome): [[alpha0_stalberg_dual_face_centroid_r1.dual-report-a]]
- B (intent-seat): [[alpha0_stalberg_dual_face_centroid_r1.dual-report-b]]

## Trinity / Prefer SHAs

| Remote | SHA |
|--------|-----|
| `project/genesis-mythos-master` | `ebc8200503cf7232e1c07fddc1aa76b715a80905` (pushed force-with-lease) |
| Prefer `main` | `b4547f2b4deb5195866497c590cd578a936f3bc5` (unchanged this pass) |

## Operator F5 checklist (face-centroid duals)

1. Open `res://scenes/WorldgenCraft.tscn` — HUD **FACE-CENTROID r1 · dual_offset_cells**; dual overlay on (**D**).
2. Click an interior logic point — cyan on ≤4 **face-centroid** dual tiles (inset diamonds in surrounding faces), **not** a filled primary-face 2×2 plate, **not** a vertex-neighbour star around the point.
3. Repeat same click — identical ≤4 dual keys.
4. Confirm dual verts sit at main-face centres; MeshGraph organic underlay + rings≈2 / spacing=3.0; Terrain3D OFF.
5. Graph-family check vs [[Ingest/Final-grid-state.jpg]] (organic hex + irregular quads) — not art parity.
6. Attest only when face-centroid duals are product-legible; then [[alpha0_stalberg_dual_visual_r3]].

## Related

- Investigation [[alpha0_stalberg_dual_geometry_rethink_investigation]] · Aborted [[alpha0_stalberg_dual_rebind_r1]] · Prior [[alpha0_stalberg_primal_graph_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Prefer/weave [[prefer_intent_validates_gates_r1]] · Law [[Grid-Topology-Host-Law]]
