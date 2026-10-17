---
title: Staging receipt — alpha0_stalberg_dual_lattice_r2
slice_id: alpha0_stalberg_dual_lattice_r2
ask_id: alpha0_stalberg_dual_lattice
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2e
producer_run_id: sp-tdlr2-a29d70
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_offset_cells
intent_invariant: "Player edits logic points; dual cells are the half-offset quads whose corners are those points."
completed: 2026-10-04T00:07:29Z
status: staging_prefer_ok_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_dual_lattice_r1
prior_altitude: superseded_partial_wrong_object_staging_prefer_without_concept
logic_prior_slice_id: alpha0_stalberg_dual_corner_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
trinity_sha: eebe46f4a4a682e94c26ab475bbf482d83e8d12e
prefer_main_sha: 3aced2f5156acceeaf633e41eff7368a35331e82
density_lift: deferred_until_pipeline_ask_success
dual_visual_ask_success: paused_until_operator_f5
mcp_evidence_a: Factory-DRB/slice-briefs/_evidence/dual_lattice_r2_verify_a.png
mcp_evidence_b: Factory-DRB/slice-briefs/_evidence/dual_lattice_r2_verify_b.png
---

# Staging receipt — `alpha0_stalberg_dual_lattice_r2`

**claim_class: staging** until operator F5. Prefer **concept** ok (object identity + invariant) — not staging Prefer alone. Dual-visual ask_success remains **out**. **No Curator.**

## Conceptual leg

| Field | Value |
|-------|--------|
| Project end-state | Logic-point edits own half-step dual lattice; dual_visual/density later |
| Path | neighborhood r1 wrong-object → this dual lattice ownership → next dual_visual r3 |
| Intent invariant | `Player edits logic points; dual cells are the half-offset quads whose corners are those points.` |
| `success_object` | `dual_offset_cells` |

## Harness gate (pre-LIVE)

| Check | Result |
|-------|--------|
| DualLatticePreferHardenTests | **ok** (3) |
| IntentValidatesGatesPreferTests | **ok** (4) — primary-face host Prefer-fails; lattice+invariant Prefer-passes |
| `dual_offset_cells` accept | Prefer contract accepts (main `3aced2f`) |

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_lattice_r2.prefer-result.json` → ok · `concept_prefer_ok: true` |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_lattice_r2/implicit-intent-bind.json` |
| Compose | Slice Producer judgment `sp-tdlr2-a29d70` — conceptual leg present |
| do_not_waive | `proxy_substitution` · `intent_collapsed_to_mechanics` · `primary_face_as_dual` · neighborhood/lattice seats |
| LIVE compile | `dotnet build` GenesisMythos.csproj — **0 errors** |

## LIVE weld

| Check | Evidence |
|-------|----------|
| Dual lattice | `OrganicDualOffsetLattice` — DualCellsTouching, IsHalfStepOffset, VarignonMidpoints; `success_object: dual_offset_cells` |
| Host | `DualGridCraftHost` WeldSliceId=r2; OwnedDualCellKeys; `cells.Count > MaxDualCellsPerLogicFlip → return 0` |
| HUD | WorldgenCraft · STÅLBERG DUAL-LATTICE r2 · dual_offset_cells |
| Preserved | organic underlay · craft-plane authority · rings≈2 · spacing=3.0 · Terrain3D OFF |

## MCP evidence

| Shot | Path | Notes |
|------|------|-------|
| A | [[_evidence/dual_lattice_r2_verify_a.png]] | cyan on 4 inset `d_*` dual tiles; HUD r2 |
| B | [[_evidence/dual_lattice_r2_verify_b.png]] | repeat click same set |

Runtime (repeat click same screen point):

- `LastFlippedVertex=63`
- `LastOwnedDualCellsCsv=d_5_58_62_63,d_5_59_63_64,d_9_20_62_63,d_9_38_63_64` (identical a→b)
- `LastOwnedDualFaceCount=4` · `LastNeighborhoodStable=true`
- Overlay children named `DualCell_d_*` (no `org_` Success ids)

## Operator F5 checklist

1. Open `res://scenes/WorldgenCraft.tscn` — dual overlay on (**D**); HUD shows **DUAL-LATTICE r2 · dual_offset_cells**.
2. Click an **interior logic point** — cyan on ≤4 **half-step** `d_*` dual tiles (Varignon inset), **not** a filled primary-face 2×2.
3. Repeat the same click — owned dual-cell set identical (≤4).
4. Confirm organic yellow underlay + rings≈2 / spacing=3.0; Terrain3D OFF.
5. Attest `ask_success` only when dual lattice ownership is product-legible; then re-arm [[alpha0_stalberg_dual_visual_r3]].

## Related

- Supersedes [[alpha0_stalberg_dual_lattice_r1]] · Prior partial [[alpha0_stalberg_dual_neighborhood_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Prefer/weave [[prefer_intent_validates_gates_r1]]
