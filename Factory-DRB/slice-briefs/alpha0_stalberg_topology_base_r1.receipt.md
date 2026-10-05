---
title: Staging receipt — alpha0_stalberg_topology_base_r1
slice_id: alpha0_stalberg_topology_base_r1
ask_id: alpha0_stalberg_quad_kernel
producer_run_id: sp-tqbr-bedtime-20261003
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
completed: 2026-10-03T08:50:00Z
status: staged_topology_base_recovered
altitude_class: near_parity_awaiting_operator_f5
approach_status: intact_upstream_fixed
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
trinity_sha: d3ddf7c5c5eeff8bd82bca69f8720ae70e805f0f
mcp_iterations: 5
---

# Staging receipt — `alpha0_stalberg_topology_base_r1`

**BEDTIME LOOP COMPLETE (≤5).** Upstream radial-star fixed (injective unique-topo key + axial triangulation). Zero-relax MCP = filled hex all-quad, `longRays=0`. Soft relax 40 + mesh-boundary pins = clean hex + organic flow. **claim_class: staging** — not ask_success. Ban `verify_mcp_only`. **No Curator.**

## Evidence

| Iter | Path |
|------|------|
| i1 | `Factory-DRB/slice-briefs/_evidence/stalberg_topology_base_r1_i1.png` |
| i2 | `Factory-DRB/slice-briefs/_evidence/stalberg_topology_base_r1_i2.png` |
| i3 | `Factory-DRB/slice-briefs/_evidence/stalberg_topology_base_r1_i3.png` |
| i4 | `Factory-DRB/slice-briefs/_evidence/stalberg_topology_base_r1_i4.png` |
| i5 | `Factory-DRB/slice-briefs/_evidence/stalberg_topology_base_r1_i5.png` |

## Failure mode closed

| Grok mode | Status |
|-----------|--------|
| 1 Bad concentric-ring / center rays | Closed as symptom of antipode weld |
| 2 Merge does almost nothing | Not primary — merge ~65–67 quads / ~16–22 tris remaining OK |
| 3 Incomplete subdivision | Not primary — 100% quads post-subdivide |
| 4 Index/connectivity (XOR PositionHash) | **FIXED** — `(qx,qy)` injective key |

## LIVE knobs (end of loop)

- `DefaultRingCount = 5`
- `DefaultRelaxIters = 40`
- `DefaultPullRate = 0.05`
- `topoKey=qxqy` (DIAG breadcrumb)

## Prefer authorship

LIVE `DualGridCraftHost` / `OrganicQuadMesh` emit opaque faces + unique edge lines (graph topology). Refuse `points_as_grid` / `count_equals_topology` not applicable as Success substitute — organic quads are the board. Seat: `prefer_authorship_pass` treated **ok** for staging claim (edges+faces present in code, not comments).

## Morning F5

1. Open WorldgenCraft; confirm filled hex irregular all-quad vs [[Ingest/Final-grid-state.jpg]].
2. Hit R a few times (seed variance).
3. If OK → operator ask_success / GREENLIGHT close; else only tune relax/merge (keep injective key).
