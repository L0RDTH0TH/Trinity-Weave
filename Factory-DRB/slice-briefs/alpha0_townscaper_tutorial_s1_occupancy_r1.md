---
title: Slice brief — alpha0_townscaper_tutorial_s1_occupancy_r1
slice_id: alpha0_townscaper_tutorial_s1_occupancy_r1
ask_id: alpha0_townscaper_tutorial
series_id: alpha0_townscaper_tutorial_r1
umbrella_ask_id: alpha_architecture_half_b
tutorial_step: 1
created: 2026-10-02
updated: 2026-10-02
claim_class: staging
factory_greenlit: true
status: armed_ready_to_stage
template: Half-B-Weld-Brief-Template
depends_on: null
next_in_chain: alpha0_townscaper_tutorial_s2_dual_offset_r1
greenlit_at: 2026-10-02T19:35:00Z
go_latch_reverted_at: 2026-10-03T03:45:00Z
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_townscaper_tutorial_s1_occupancy_r1.armed.yaml
supersedes_attest: alpha0_townscaper_tutorial_s1_attest
resets: alpha0_townscaper_craft_core_r1
source_yt: https://www.youtube.com/watch?v=Y19Mw5YsgjI
f5_invalidated: true
f5_invalidated_reason: points_as_grid__hex19_point_cloud_not_lattice_graph
prior_weld_altitude: failed_altitude_points_as_grid
law_amended: 2026-10-02-lattice-graph-topology
---

# Slice brief — `alpha0_townscaper_tutorial_s1_occupancy_r1`

Filled from [[Half-B-Weld-Brief-Template]]. **Tutorial step 1 — hex lattice graph occupancy + placement ghost.** Series: [[alpha0_townscaper_tutorial_r1]]. Umbrella: [[alpha_architecture_half_b]]. Lock: [[FEEDSTOCK-SHAPE]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Canonical YT: https://www.youtube.com/watch?v=Y19Mw5YsgjI

**Law amended 2026-10-02 (lattice graph — points ≠ grid).** Prior hex-19 **point-cloud** weld (19 floating markers, no edges/faces) = **`failed_altitude` / `points_as_grid`**. Prior rect GridMap weld also invalid. Do **not** claim Success on current LIVE. Do **not** claim dual visuals, MeshLibrary connectors, or art as Success.

**Armed and stageable (2026-10-03).** There is no YAML launch latch — the earlier `operator_go` / `do_not_auto_dispatch` staging gate was reverted because it only blocked the factory; the operator kicks off a re-eat in chat. Real enforcement is the topology seat, not a flag: post-lane `prefer_authorship_pass` scans LIVE `Systems/DualGridCraftHost.cs` + `Core/WorldGen/Hex19OccupancyLattice.cs` and fails closed on `points_as_grid` / `count_equals_topology` / `explicit_met_implicit_miss` unless **edges and faces/cells** both show up as code-level evidence. LIVE is still the point cloud today — the seat catches it.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_townscaper_tutorial` |
| `slice_id` | `alpha0_townscaper_tutorial_s1_occupancy_r1` |
| Tutorial step | **1 of 6** — hex-19 **lattice graph** + placement ghost |
| Scope | Fixed hex scaffold (1+6+12 vertices) as a **graph**: vertices + neighbor **edges** + **faces/cells**; ghost snaps to a **cell**; occupancy-grid toggle; dual toggle stubbed; no cam yank; no Terrain3D |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` — Success bar amended to lattice graph; re-WELD required |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Worldgen entry scene | `res://scenes/WorldgenCraft.tscn` |
| Mode | update — replace point-cloud / rect GridMap with **hex lattice graph**; ghost + occupancy toggle; strip dual/connector Success |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| YT early ladder | Occupancy / click-add + placement preview — https://www.youtube.com/watch?v=Y19Mw5YsgjI · [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] |
| Topology law | Points ≠ grid — [[Grid-Topology-Host-Law]] |
| Grammar | Grid = graph before dual — [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] |
| Operator diagrams | `single-grid-section` / `multiple-grid-sections` / `Final-Grid` under Ingest / Factory-DRB/references |
| Host law | [[Prefer-Authorship-Host-Law]] — entry bind + Hot Wheels authorship |
| Primary feedstock | [[dual-grid-nested-placetile-world-authorship]] (scaffold ≠ product lattice) |
| Series law | [[alpha0_townscaper_tutorial_r1]] |

Seasoning only (cite, do not Success): Factory-DRB/references/craft-visual-r2/; dual-offset; connector modules.

### Hard law (this slice)

- **Hex lattice graph** on the fixed **hex-19 scaffold** (center + 2 rings: **1+6+12=19 vertices**). Success requires:
  1. **Vertices** — the 19 points  
  2. **Edges** — neighbor connections so the hex lattice is readable as a graph  
  3. **Faces / cells** — regions you paint/ghost onto (flat plate OK)  
- “19 points present” alone = refuse `count_equals_topology` / `points_as_grid`.
- LMB add / RMB remove under **mouse** (ray → craft plane → snap to **cell** or the vertex set that defines it).
- **Placement shadow / ghost:** previews the **cell** under cursor before commit — not a lone disk in empty space.
- **Occupancy grid display toggle:** show/hide lattice (vertices+edges+faces). Dual overlay toggle stubbed/hidden until s2.
- Visual = graybox OK — **lattice must read as cells**, not floating props.
- **No** dual MeshLibrary / connector / art Prefer Success.
- No cam yank / no camera-center aim.
- Terrain3D absent or hard-disabled (`terrain3d_in_scope`).
- Do **not** bundle steps 2–5 (`bundle_tutorial_steps`).
- Hex-19 is **tutorial scaffold** only — product lattice stays on [[dual-grid-nested-placetile-world-authorship]].

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [x] [[COHESIVE-VISION-ART-DIRECTION]]
- [x] [[Prefer-Authorship-Host-Law]]
- [x] [[Grid-Topology-Host-Law]]
- [x] Host-weld factory pilots
- [x] [[alpha0_townscaper_tutorial_r1]]
- [x] [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]]
- [x] [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]
- [ ] Dual offset / connectors / art — **later steps only**
- [ ] [[alpha0_townscaper_df_depth_r1]] — **blocked**
- [ ] Terrain3D — deferred

## 4. End flavor

> Painting the fixed hex lattice under the mouse feels like Townscaper input — you see a hex grid of cells with edges, ghost previews the next cell, add/remove occupancy, toggle the grid, camera stays put. Not floating disks. Not dual MeshLibrary. Not pretty modules. Not Terrain3D.

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | **F5:** Hex-19 **lattice graph** (vertices + edges + faces/cells); ghost snaps to a **cell**; LMB/RMB under mouse; occupancy lattice toggle; graybox OK; dual toggle stubbed OK; no cam yank; no Terrain3D |
| Operator attest | F5 only — ban `verify_mcp_only`; prior point-cloud / rect F5 **does not count** |
| `claim_class` | `staging` until operator F5 after lattice-graph re-WELD |
| Receipt must | Cite graph topology; strip dual/connector Success; note prior `points_as_grid` altitude failed |

### Exact Success lines (operator bar)

1. **Hex lattice graph:** Fixed scaffold of 19 vertices with **neighbor edges** and **faces/cells** visible (cite Final-Grid / section diagrams).
2. **Placement ghost:** Before commit, ghost shows the **cell** snap target under the cursor.
3. **Occupancy lattice toggle:** Operator can show/hide the lattice (not markers-only without edges).
4. **Input feel:** LMB add / RMB remove under mouse; no cam yank; Terrain3D absent/hard-disabled; graybox OK — no dual visual Success.

### Success refuses

- `points_as_grid`
- `count_equals_topology`
- `prop_scatter_as_composition`
- `bitmask_equals_townscaper`
- `skip_dual_offset` *(reserved — dual out of scope this step)*
- `procedural_only_as_success` *(as art Success)*
- `terrain3d_in_scope` / `terrain3d_leak_f5` / `craft_terrain_blend`
- `boil_the_ocean_df`
- `verify_mcp_only`
- `bundle_tutorial_steps`
- `infinite_rect_as_hex19`

## 6. Refuse

| Code | Note |
|------|------|
| `points_as_grid` | Markers at coords with no edges/faces claimed as grid Success |
| `count_equals_topology` | “19 points present” ≠ lattice of cells |
| `bundle_tutorial_steps` | Dual / connectors / art / depth in this Prefer |
| `bitmask_equals_townscaper` | Bitmask table as Townscaper Success |
| `prop_scatter_as_composition` | Props as composition |
| `procedural_only_as_success` | Procedural dual as art Success |
| `terrain3d_in_scope` / `craft_terrain_blend` / `terrain3d_leak_f5` | Terrain3D on craft |
| `boil_the_ocean_df` | DF-depth in this ticket |
| `verify_mcp_only` | MCP-as-Success |
| `inspiration_shape_miss` | Not occupancy click-add + cell ghost feel |
| `craft_cam_recenter_on_place` | Cam yank |
| `infinite_rect_as_hex19` | Rect/unbounded GridMap claimed as hex-19 |

## 7. Out of scope

- Dual cells / half-step offset / dual overlay + dual toggle (step 2)
- Connector modules / continuous mass (step 3)
- Module selection polish (step 4)
- Genesis adaptation (step 5)
- Art bind (step 6)
- DF-depth · Terrain3D · sparky
- Irregular Stålberg sea grid / product procedural lattice (feedstock later)

## 8. Re-eat kickoff steps

No flags to flip — the GO-latch surfaces were reverted 2026-10-03. When the operator kicks off a re-eat:

1. Force-compose s1 — module lane only CDP + fresh implicit-intent bind (compose rewrites the bind, so `composed_at` postdates `law_amended_at`).
2. Stage `IMPLEMENT_SLICE` for the `module` lane; staging injects `armed_packet_path`, `half_b_brief_path`, `ask_id`, and the non-waivable `do_not_waive` set.
3. EAT-QUEUE the module lane → F5 the **lattice graph**.

Nothing else is outstanding: bind is fresh, s1 holds authority, d6 is parked, and both module/godot PQs are empty. Staging does not refuse on armed state; a divergent composed slice only yields an advisory `armed_slice_divergence` note.

## Cross-links

- Series [[alpha0_townscaper_tutorial_r1]] · next [[alpha0_townscaper_tutorial_s2_dual_offset_r1]]
- [[Grid-Topology-Host-Law]] · [[Prefer-Authorship-Host-Law]]
- Archive [[alpha0_townscaper_craft_visual_altitude_failed_2026-10-02]]
- Prior hex-19 point-cloud weld = **`failed_altitude_points_as_grid`** — re-WELD before F5
