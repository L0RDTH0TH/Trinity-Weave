---
title: Staging receipt — alpha0_stalberg_dual_visual_r1
slice_id: alpha0_stalberg_dual_visual_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2b
producer_run_id: sp-tdv-20261003
claim_class: failed_altitude
factory_greenlit: false
prefer_authorship_pass: ok_then_product_fail
completed: 2026-10-03T19:12:00Z
status: failed_altitude_partial_visual_fidelity
altitude_audit: 1-Projects/genesis-mythos-master/Factory-DRB/Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03.md
superseded_by: alpha0_stalberg_dual_visual_r2
prior_slice_id: alpha0_stalberg_manual_scale_r1
logic_prior_slice_id: alpha0_stalberg_dual_corner_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
trinity_sha: 5c992107584340d3344dea7aa5e03e252bb7ad94
mcp_evidence_a: Factory-DRB/slice-briefs/_evidence/stalberg_dual_visual_r1_a.png
mcp_evidence_b: Factory-DRB/slice-briefs/_evidence/stalberg_dual_visual_r1_b.png
pipeline: approved_shape_distinct_graybox_standins_empty_edge_corner_full
density_lift: deferred_until_pipeline_ask_success
---

# Staging receipt — `alpha0_stalberg_dual_visual_r1`

**Altitude fail (partial):** Prefer authorship passed under underspecified gates; F5/Grok showed stretch-as-shape, not discrete silhouettes. **Not** product Success. Audit: [[Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03]]. Superseded by [[alpha0_stalberg_dual_visual_r2]]. **No Curator.**

## Proof

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_visual_r1.prefer-result.json` → ok |
| Dual visual seat | `has_shape_distinct` · `has_four_families` · `has_prove_dual_visual` · `gray_ramp_only: false` |
| LIVE families | Runtime dual nodes include `DualCell_org_*_{Empty,Corner,Edge,Full}` |
| Factory log | `DualVisual_FamilyShowcase` + `shape_distinct=empty\|edge\|corner\|full` |
| Board | MCP screenshots a/b — raised gray silhouettes (not albedo ramp); Terrain3D OFF |
| Manual scale | rings=2 / spacing=3.0 preserved (~50 quads) |

## LIVE

- `DualGridCraftHost` — `DualVisualFamily` empty/edge/corner/full; `MakeShapeDistinctDualVariant` / `CommitDualFamilyMesh`; `EnsureShapeDistinctDualMeshLibrary`; `ProveDualVisualVariants`
- `Library` → runtime MeshLibrary (4 items); `MeshLibrarySource` = `approved_shape_distinct_graybox_standins_empty_edge_corner_full`
- Organic underlay + craft-plane authority + dual-corner four-cell retained
- Hex19 / density lift / Terrain3D / art polish / cam yank **not** Success

## Soft spots (operator F5)

1. Prefer already signals four families differ in silhouette/geometry (seat + runtime node names).
2. Four families enough this altitude — full ~6 MeshLibrary depth later (diagonal/inverse as Edge/Corner fold).

## Operator F5

1. WorldgenCraft — confirm empty rim vs edge bar vs corner L vs full plate (same mid-gray).
2. LMB flip corner — up to four dual cells rebuild with shape change (not brightness ramp).
3. Organic board + rings=2 spacing=3.0 still readable vs Final-grid-state.
4. Attest ask_success when house bar met.

## Related

- Logic prior [[alpha0_stalberg_dual_corner_r1]] · Scale [[alpha0_stalberg_manual_scale_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]
