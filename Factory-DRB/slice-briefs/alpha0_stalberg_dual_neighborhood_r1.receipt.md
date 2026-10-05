---
title: Staging receipt — alpha0_stalberg_dual_neighborhood_r1
slice_id: alpha0_stalberg_dual_neighborhood_r1
ask_id: alpha0_stalberg_dual_neighborhood
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2c
producer_run_id: sp-tdn-20261003
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
completed: 2026-10-03T20:49:47Z
status: staging_prefer_ok_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_dual_visual_r2
logic_prior_slice_id: alpha0_stalberg_dual_corner_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
trinity_sha: 0176db5729406c7974136248628de3b53e963e70
prefer_main_sha: 0176db5729406c7974136248628de3b53e963e70
mcp_evidence_a: Factory-DRB/slice-briefs/_evidence/stalberg_dual_neighborhood_r1_a.png
mcp_evidence_b: Factory-DRB/slice-briefs/_evidence/stalberg_dual_neighborhood_r1_b.png
density_lift: deferred_until_pipeline_ask_success
dual_visual_ask_success: paused_until_neighborhood_green
---

# Staging receipt — `alpha0_stalberg_dual_neighborhood_r1`

**claim_class: staging** until operator F5. Prefer authorship **ok**. Dual-visual empty/edge/corner/full ask_success remains **out**. **No Curator.**

## Prefer (primary)

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_neighborhood_r1.prefer-result.json` → ok |
| do_not_waive | `unstable_dual_neighborhood` · `stamp_as_dual` · `over_neighbor_paint` (non-waivable) |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_neighborhood_r1/implicit-intent-bind.json` |
| Host law | [[Prefer-Authorship-Host-Law]] · [[Grid-Topology-Host-Law]] |
| Trinity | `0176db5729406c7974136248628de3b53e963e70` on `main` / project tip (no Prefer scanner delta this weld) |

## LIVE proof

| Check | Evidence |
|-------|----------|
| Stable neighborhood | `Stable_Neighborhood_Ready` — `max_incident=4 interior_exact4=36 logic_points=63 stamp_as_dual=false` |
| Repeat north click | screen (576,220) → vertex **39** owned **`[15,16,38,39]`** on fill / clear / refill (identical) |
| Hard refuse >4 | `UpdateFourDualSlots` returns 0 when incident > cap |
| Corner-owned dual | `MakeCornerOwnedDualCellMesh` via `FaceCornersLocal` — no centroid MeshLibrary stamps |
| Debug highlight | Cyan material override + Label3D on owned dual cells until next click |
| Preserved | organic underlay · craft-plane authority · rings=2 · spacing=3.0 · Terrain3D OFF · Hex19 not Success |

## MCP evidence

- `_evidence/stalberg_dual_neighborhood_r1_a.png` / `_b.png` (cyan owned dual set)
- factory-runtime `Corner_Flip` lines: corner=39 owned=[15,16,38,39] ×3

## Operator F5 checklist

1. Open `res://scenes/WorldgenCraft.tscn` — dual overlay on (D toggles).
2. Click a **north** interior logic point — cyan highlight shows ≤4 owned dual cells.
3. **Repeat the same north click** (or LMB → RMB → LMB) — owned set must match (same `org_*` ids).
4. Confirm organic yellow edges + rings≈2 / spacing=3.0; Terrain3D OFF; no MeshLibrary stamp scatter.
5. Attest `ask_success` only when house bar met; dual_visual r3 stays draft until then.

## Related

- Series [[alpha0_stalberg_grid_kernel_r1]] · Prior [[alpha0_stalberg_dual_visual_r2]] (paused) · Next [[alpha0_stalberg_dual_visual_r3]] after neighborhood green
