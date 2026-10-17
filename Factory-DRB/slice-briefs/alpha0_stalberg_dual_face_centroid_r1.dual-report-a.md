---
title: Dual report A — outcome — alpha0_stalberg_dual_face_centroid_r1
slice_id: alpha0_stalberg_dual_face_centroid_r1
report: A
role: outcome
completed: 2026-10-04T03:31:16Z
claim_class: staging
---

# Dual report A — outcome

| Field | Value |
|-------|--------|
| Slice | `alpha0_stalberg_dual_face_centroid_r1` |
| LIVE | `OrganicDualOffsetLattice` — one dual per primal Face; `LocalCentre` = face centroid; `DualCellsTouching(V)` = ≤4 face-centroid duals sampling V |
| Host | `WeldSliceId=alpha0_stalberg_dual_face_centroid_r1`; HUD **FACE-CENTROID r1 · dual_offset_cells** |
| Prove | `Stable_Neighborhood_Ready` — `stable_face_centroid_dual … half_step=52 face_centroid=true hex19_half_step=true vertex_neighbor_star=false dual_rebind_wrong_locus=false` |
| MCP | corner=25 owned=`d_10_23_24_25,d_10_25_43_44,d_14_23_25_26,d_14_25_32_43` identical on repeat |
| Evidence | [[_evidence/dual_face_centroid_r1_verify_a.png]] · [[_evidence/dual_face_centroid_r1_verify_b.png]] |
| Prefer | concept ok (`prefer_authorship_pass_ok`) |
| Compose | Slice Producer judgment `sp-fcr1-4205d9` |
| Supersedes | aborted [[alpha0_stalberg_dual_rebind_r1]] |
| Trinity | `ebc82005` on `project/genesis-mythos-master` (force-with-lease) |

## Outcome

Stage-6 face-centroid dual lattice welded. Cyan highlights inset dual tiles at face centres (not filled primal-face 2×2, not vertex-neighbour star). claim_class staging until operator F5.
