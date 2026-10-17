---
title: Weld receipt — alpha0_townscaper_tutorial_s1_occupancy_r1
slice_id: alpha0_townscaper_tutorial_s1_occupancy_r1
ask_id: alpha0_townscaper_tutorial
series_id: alpha0_townscaper_tutorial_r1
created: 2026-10-02T19:40:00Z
rewelded: 2026-10-03T05:05:00Z
claim_class: staging
ask_success: false
factory_greenlit: true
status: staging_awaiting_operator_f5
lane: module
curator: forbidden
law: hex19_lattice_graph_topology
producer_run_id: sp-s1occ-a4506efc
superseded_producer_run_id: sp-craft-vis-032901
queue_entry_id: factory-s1occ-e2-module-125dc1
prior_weld_altitude: failed_altitude_points_as_grid
f5_invalidated: true
f5_invalidated_reason: points_as_grid__hex19_point_cloud_not_lattice_graph
f5_pending_on: hex19_lattice_graph_vertices_edges_faces
---

# Weld receipt — tutorial s1 occupancy (**lattice-graph re-weld, STAGING**)

Prior weld (19 coordinate markers, no edges/faces) was **`failed_altitude` / `points_as_grid`**. This run re-welded LIVE onto the **lattice graph** law and the Prefer topology seat now passes on all three axes. **This is not Success** — Success is operator **F5** only.

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_townscaper_tutorial` |
| `slice_id` | `alpha0_townscaper_tutorial_s1_occupancy_r1` |
| `producer_run_id` | `sp-s1occ-a4506efc` (supersedes `sp-craft-vis-032901` / d6) |
| Lane | `module` **only** — s2–s6 not opened |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Build | `dotnet build` — **0 errors**, 4 pre-existing warnings in unrelated files |
| `claim_class` | **`staging`** — awaiting operator F5 |
| Curator | **not run** (hard forbid) |

## 1. Compose + stage (authority moved off d6)

- `load_producer_receipt(s1)` was **None**; `implementation_cell.producer_run_id` was the superseded `sp-craft-vis-032901`. Both now point at s1.
- `translate_vault_work_orders` re-derives `row_ux_world_generation_r1_d6` from the catalog budget row, so the pillar packet was assembled **directly from the s1 brief + armed packet** instead.
- Compose artifacts (module lane only):
  - CDP — `Factory-DRB/slice-briefs/alpha0_townscaper_tutorial_s1_occupancy_r1/cell_dispatch_plan.json` (wave 1, lanes `[module]`)
  - Lane mission — `…/missions/module.md`
  - Producer receipt + pillar packet — `.technical/factory/slice-briefs/alpha0_townscaper_tutorial_s1_occupancy_r1/`
  - Implicit-intent bind — `.technical/weave/factory/genesis-mythos-master/alpha0_townscaper_tutorial_s1_occupancy_r1/implicit-intent-bind.json`, `composed_at` **2026-10-03T04:55:27Z** (newer than armed `law_amended_at` 2026-10-02T21:00:00Z), `topology_rewrite: true`.
- `IMPLEMENT_SLICE` staged on the **module** PQ with `armed_packet_path` injected and the 8 `do_not_waive` product Prefer seats; dispatch preflight passed.

## 2. Prefer topology evidence — before vs after

Seat: `prefer_authorship_pass` → `scan_topology_evidence` on LIVE.

| Axis | Before (point cloud) | After (lattice graph) |
|------|----------------------|------------------------|
| `has_edges` | **false** | **true** |
| `has_faces_or_cells` | **false** | **true** |
| `missing_axes` | `["edges","faces_cells"]` | **`[]`** |
| `points_only` | **true** | false |
| `point_signals` | 7 (`point_count`, `point_array`, `marker_per_point`, `logic_points`) | **0** |
| Topology violations | `explicit_met_implicit_miss`, `points_as_grid`, `count_equals_topology` | **none** |

Full seat after weld: `prefer_authorship_pass_ok` — violations `[]`, warnings `[]`, `implicit_bind.ok true`, `topology_axis_armed true`.

**The point signals went to zero rather than growing** — this is not a `points_as_grid` pass-by-accretion.

## 3. LIVE files changed (all inside module `zone_ownership`)

| File | Change |
|------|--------|
| `Core/WorldGen/Hex19OccupancyLattice.cs` | Point array → lattice **graph**: `Vertices`, `NeighborOffsets` / `NeighborsOf` / `AreAdjacent`, `Edges` + `EdgesOf` + `BuildEdges`, `HexCell` + `Cells` + `BuildCells`, `HexCorners` / `CellCornersOf`, and `TrySnapWorldToCell` (cube rounding over the whole face, replacing nearest-marker-within-radius) |
| `Core/WorldGen/ICraftCellAuthority.cs` | `LogicPointFill`/`SetLogicPoint`/`SnapshotLogicPoints` → `CellFill`/`SetCellFill`/`SnapshotCellFills` — occupancy lives on faces, not coordinates |
| `Systems/DualGridCraftHost.cs` | Draws all three axes under one toggleable root: `LatticeFaces` (hex triangle fans), `LatticeEdges` (`PrimitiveType.Lines` — cell outlines **and** adjacency edges), `LatticeVertices`. Ghost is a **hex cell footprint**, occupied cells are hex prisms (no disk markers). `ProveLatticeGraphTopology()` fails closed if the edge or face surface is absent |
| `Systems/WorldgenCraft.cs` | Picks cells (`TryPickHexCell`), `SliceId` repointed to s1, hint/telemetry describe the graph (`v / e / cells`) |

## 4. Structural verification (beyond the regex seat)

- Lattice math replicated independently: **19 vertices, 42 unique edges**, degree histogram `{6:7, 4:6, 3:6}` — consistent with a radius-2 hex graph.
- Adjacent cells share exactly **2 corners** each → the faces genuinely tile, they are not 19 independent hexagons.
- Every cell centre round-trips through the snap, and **20000/20000** sampled points inside a cell snap to that cell → the ghost tracks the **whole cell area**, not a radius around a marker.
- Headless `res://scenes/WorldgenCraft.tscn`: `lattice_graph_ok: true`, `lattice_vertices 19 / lattice_edges 42 / lattice_cells 19`, **0 runtime errors**.

## 5. Known divergences (not fixed — out of module zone ownership)

1. `Core/ClosedAlpha/AlphaFactoryLog.cs` still defaults the log **envelope** `weld_slice_id` / `half_b_overlay` / `ask_id` to the superseded `alpha0_townscaper_craft_visual_r1`. Per-emission `observation.overlay` is correct for s1.
2. `Systems/_factory/manifest.yaml` still describes `row_ux_world_generation_r1_d6` / `sp-craft-vis-032901`. It carries `claim_class: staging`, so it does not greenwash.

Both sit outside `zone_ownership.module` in the armed packet and were deliberately left for a later owning lane.

## 6. Operator F5 bar (unchanged — this is the Success gate)

1. **Hex lattice graph:** 19 vertices + neighbour **edges** + **faces/cells**, reading as a hex grid of cells.
2. **Placement ghost:** previews the **cell** under the cursor before commit.
3. **Occupancy lattice toggle:** `G` shows/hides vertices + edges + faces.
4. **Input feel:** LMB fill / RMB clear under the mouse; **no cam yank**; Terrain3D absent; graybox OK; dual toggle stubbed.

## 7. Explicit wait

**`claim_class: staging`. Do not read green metrics as Success.** Prefer seats green + build green are necessary, not sufficient — only operator **F5** of the lattice graph closes s1. Do not open [[alpha0_townscaper_tutorial_s2_dual_offset_r1]] until then. Curator **not run**.

## Cross-links

- Brief [[alpha0_townscaper_tutorial_s1_occupancy_r1]] · armed packet `alpha0_townscaper_tutorial_s1_occupancy_r1.armed.yaml`
- [[Grid-Topology-Host-Law]] · [[Prefer-Authorship-Host-Law]]
- Series [[alpha0_townscaper_tutorial_r1]] · next [[alpha0_townscaper_tutorial_s2_dual_offset_r1]] (**blocked**)
- Lane receipt — `.technical/factory/slice-briefs/alpha0_townscaper_tutorial_s1_occupancy_r1/receipts/module.json`
