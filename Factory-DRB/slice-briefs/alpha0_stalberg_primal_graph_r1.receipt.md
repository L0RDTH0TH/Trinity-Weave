---
title: Staging receipt — alpha0_stalberg_primal_graph_r1
slice_id: alpha0_stalberg_primal_graph_r1
ask_id: alpha0_stalberg_primal_graph
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2f
producer_run_id: sp-pgr1-25ad34
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: organic_mesh_graph
intent_invariant: "Primal ownership is Vertex/Edge/Face singletons with incidence; dual cells are half-offset quads whose corners are those shared Vertex refs."
completed: 2026-10-04T02:04:11Z
status: f5_confirmed_neighbor_still_wrong__superseded_by_dual_rebind_r1
prior_slice_id: alpha0_stalberg_dual_lattice_r2
logic_prior_slice_id: alpha0_stalberg_dual_lattice_r2
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
trinity_sha: ee27f1e4fe0fa8d0100aef3e48b9c97650d387ab
prefer_main_sha: b4547f2b4deb5195866497c590cd578a936f3bc5
density_lift: deferred_until_pipeline_ask_success
dual_visual_ask_success: paused_until_dual_rebind_concept_and_operator_f5
mcp_evidence_a: Factory-DRB/slice-briefs/_evidence/primal_graph_r1_verify_a.png
mcp_evidence_b: Factory-DRB/slice-briefs/_evidence/primal_graph_r1_verify_b.png
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
operator_f5_at: '2026-10-04T02:34:56Z'
operator_f5_result: neighbor_cluster_still_wrong_same_wrong_cluster_feel
next_ticket: alpha0_stalberg_dual_rebind_r1
---

# Staging receipt — `alpha0_stalberg_primal_graph_r1`

**claim_class: staging.** Prefer **concept** ok (`organic_mesh_graph` + invariant). **Operator F5 confirmed (2026-10-04):** MeshGraph landed, but **neighbor cluster still wrong** (same wrong cluster feel) → next ticket [[alpha0_stalberg_dual_rebind_r1]]. Dual-visual ask_success remains **out**. **No Curator.**

## Conceptual leg

| Field | Value |
|-------|--------|
| Project end-state | Authorable irregular dual-grid craft plane on organic all-quad board |
| Path | dual_lattice_r2 → this primal MeshGraph + incidence → next dual rebind proof → dual_visual_r3 |
| Intent invariant | `Primal ownership is Vertex/Edge/Face singletons with incidence; dual cells are half-offset quads whose corners are those shared Vertex refs.` |
| `success_object` | `organic_mesh_graph` |

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_primal_graph_r1.prefer-result.json` → ok · `concept_prefer_ok: true` · `prefer_path: concept` |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_primal_graph_r1/implicit-intent-bind.json` |
| Compose | Slice Producer judgment `sp-pgr1-25ad34` — conceptual leg present; harness_fallback → `slice_producer_judgment_required` |
| Scanners | `indexed_lists_as_graph` / `ephemeral_edge_key_as_topology` added to Prefer contract |
| do_not_waive | proxy_substitution · intent_collapsed_to_mechanics · indexed_lists_as_graph · ephemeral_edge_key_as_topology · primary_face_as_dual · non_unique_vertices |
| LIVE compile | `dotnet build` GenesisMythos.csproj — **0 errors** |

## LIVE weld

| Check | Evidence |
|-------|----------|
| MeshGraph | `Core/WorldGen/OrganicMeshGraph.cs` — Vertex/Edge/Face, GetOrAddVertex, GetOrAddEdge, AddQuad, FacesTouchingVertex |
| Kernel | `StalbergQuadKernel` emits `OrganicMeshGraph.FromIndexedMesh` → `new OrganicQuadMesh(graph, …)` |
| OQM wrap | `OrganicQuadMesh.Graph` / graph ctor / AttachGraph |
| Dual rebind | `OrganicDualOffsetLattice.CornerVertices` = shared Vertex refs; SupportFaceIndex obsolete → DeriveFaceIndex |
| Host | `DualGridCraftHost` WeldSliceId=primal_graph_r1; ProveOrganicMeshGraph; `_vertexToFaces` marked dead for dual Success |
| HUD | WorldgenCraft · STÅLBERG PRIMAL-GRAPH r1 · organic_mesh_graph |
| Preserved | organic underlay · craft-plane authority · rings≈2 · spacing=3.0 · Terrain3D OFF |

## MCP evidence

| Shot | Path | Notes |
|------|------|-------|
| A | [[_evidence/primal_graph_r1_verify_a.png]] | WorldgenCraft running post-weld; kernel Generate log edges=200 quads=50 verts=63 |
| B | [[_evidence/primal_graph_r1_verify_b.png]] | board still image (runtime helper lag; structural MCP) |

Runtime console (excerpt): kernel `sub_unique` → MeshGraph path; `post_weld: refuse valence=5>4 — keep pre-weld unique topo` (valence residual noted for dual rebind proof / F5).

## Operator F5 checklist

1. Open `res://scenes/WorldgenCraft.tscn` — HUD shows **PRIMAL-GRAPH r1 · organic_mesh_graph**.
2. Confirm organic board regenerates; dual overlay corners owned via Vertex refs (cyan on `d_*` still geometric).
3. Confirm no Success via SupportFaceIndex / soft Take(4).
4. Note residual max valence=5 on some verts (kernel refuses over-weld) — dual rebind proof / next ticket.
5. Attest only when MeshGraph ownership is product-legible; then dual rebind proof → [[alpha0_stalberg_dual_visual_r3]].

## Operator F5 result (confirmed)

| Field | Value |
|-------|--------|
| Result | **MeshGraph landed** · **neighbor cluster still wrong** (same wrong cluster feel) |
| Disposition | Not product ask_success for dual neighborhood; MeshGraph Prefer concept remains staging-ok for primal |
| Next | [[alpha0_stalberg_dual_rebind_r1]] — incidence-only dual ownership (`success_object: dual_offset_cells`) |
| Dual visual | Still paused until dual_rebind concept + F5 |

## Related

- Next [[alpha0_stalberg_dual_rebind_r1]] · Prior [[alpha0_stalberg_dual_lattice_r2]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Prefer/weave [[prefer_intent_validates_gates_r1]]
