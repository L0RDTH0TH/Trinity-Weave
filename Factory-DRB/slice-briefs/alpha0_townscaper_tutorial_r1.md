---
title: Series — alpha0_townscaper_tutorial_r1
slice_id: alpha0_townscaper_tutorial_r1
ask_id: alpha0_townscaper_tutorial
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-02
updated: 2026-10-03
claim_class: staging
factory_greenlit: false
status: parked_separate_ladder_non_authority
template: Half-B-Weld-Brief-Template
supersedes_altitude: alpha0_townscaper_craft_visual
resets_prefer: alpha0_townscaper_craft_core_r1
active_step: 2
active_step_slice_id: alpha0_townscaper_tutorial_s2_dual_offset_r1
go_latch_reverted_at: 2026-10-03T03:45:00Z
source_yt: https://www.youtube.com/watch?v=Y19Mw5YsgjI
law_amended: 2026-10-02-lattice-graph-topology
prefer_authority_moved_to: alpha0_stalberg_grid_kernel_r1
---

# Series — `alpha0_townscaper_tutorial_r1`

**Parked / separate ladder — not active Prefer authority** (2026-10-03). Active Prefer is [[alpha0_stalberg_grid_kernel_r1]] / [[alpha0_stalberg_quad_kernel_r1]]. Keep this series intact for later tutorial work; do **not** merge with the Stålberg kernel series.

**Thin tutorial ladder** for Townscaper dual-grid authorship. Treat the locked YT as a step-by-step tutorial with **operator F5 between each step**. Do not Prefer-weld art or depth until composition steps clear.

Umbrella: [[alpha_architecture_half_b]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Topology: [[Grid-Topology-Host-Law]]. Cite: [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]].

**Operator reset 2026-10-02:** START FROM THE BEGINNING — do **not** audit craft_core as green. Step 1 = occupancy weld [[alpha0_townscaper_tutorial_s1_occupancy_r1]].

**Operator hard requirements 2026-10-02 (series law):**

1. **Display grid + dual — both visible in future steps; toggleable.** Operator can show/hide **occupancy lattice** and **dual overlay** independently or as a pair.
2. **Placement shadow / ghost** — previews the **cell** under the cursor **before** click-commit.
3. **Fixed hexagonal scaffold — hex-19 as a lattice graph** = center + ring1 + ring2 (**1+6+12=19 vertices**) with **edges + faces/cells**. Points alone ≠ grid (`points_as_grid` / `count_equals_topology`). Fixed hex size for this ladder — **not** irregular sea-grid clone; **not** the product procedural lattice.

Later steps inherit these. Art / Terrain3D remain out of ladder scope until their tickets.

## Why this series exists

Prior Prefer path shipped dual-grid *data* (bitmask → N mesh ids) and fused dual+art Prefer without dual-grid *intent*. Visual r1/r2 and craft_core dual/connector Success claims = **`failed_altitude` / `metrics_only`**. Receipt: [[alpha0_townscaper_craft_visual_altitude_failed_2026-10-02]].

## Ladder (video order — adapted for Genesis Mythos)

| Step | Ticket | Scope | Greenlit | F5 gate |
|------|--------|-------|----------|---------|
| 1 | [[alpha0_townscaper_tutorial_s1_occupancy_r1]] | Hex-19 **lattice graph** (V+E+F) + cell ghost + occupancy toggle; dual toggle stubbed | **true — needs re-WELD** (`points_as_grid` altitude failed) | Lattice of cells readable; ghost on cell; no cam yank; no Terrain3D |
| 2 | [[alpha0_townscaper_tutorial_s2_dual_offset_r1]] | Dual overlay display + dual toggle (+ grid toggle); half-step offset; 4-corner reads | **true — LAUNCH** | One occupancy edit updates four dual slots; both overlays toggleable |
| 3 | [[alpha0_townscaper_tutorial_s3_connector_modules_r1]] | Six base modules as connectors; continuous mass; inherit hex-19 + toggles + ghost | false | Mass not prop scatter |
| 4 | [[alpha0_townscaper_tutorial_s4_module_selection_r1]] | Module selection rules; inherit display law | false | Edges/corners look built |
| 5 | [[alpha0_townscaper_tutorial_s5_genesis_adapt_r1]] | Palette/cam/seat; Terrain3D still out | false | Townscaper-shaped, clearly our craft |
| 6 | [[alpha0_townscaper_tutorial_s6_art_bind_r1]] | Art bind (blocked until s3–s4 mass green) | false / blocked | Not graybox craft-toy |

**Hard order:** One step per ticket; human F5 before next. Do **not** bundle steps 2–5. Do **not** jump to art. Do **not** open [[alpha0_townscaper_df_depth_r1]] until ladder clears (minimum steps 1–4 F5-green).

### Ownership split (display / grid)

| Concern | Step that owns Success | Notes |
|---------|------------------------|-------|
| Fixed hex-19 lattice graph (V+E+F) | **s1** | Refuse point-cloud / rect GridMap as Success |
| Placement ghost / shadow preview | **s1** | Ghost snaps to **cell** before commit |
| Occupancy lattice display + toggle | **s1** | Show/hide vertices+edges+faces |
| Dual overlay display + dual toggle | **s2** | s1 may stub/hide dual toggle until s2 |
| Grid + dual as a pair (both visible, independent or paired toggle) | **s2+** (inherits s1 grid toggle) | Both must be visible in future steps; toggles remain |
| YT grammar / `skip_dual_offset` etc. | **s2+** when dual arrives | Cite [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]; refuse still apply |

### LIVE vs law (brief only — no Code-Repos freestyle)

Prior s1 LIVE delivered hex-19 **point cloud** → **`failed_altitude_points_as_grid`**. **s1 re-weld** must ship a **hex lattice graph**. Do **not** freestyle Code-Repos until operator **GO**.

LIVE is deliberately left as the point cloud so the seat has something to catch. `prefer_authorship_pass` scans `Systems/DualGridCraftHost.cs` + `Core/WorldGen/Hex19OccupancyLattice.cs` on every run and currently returns `points_as_grid` + `count_equals_topology` + `explicit_met_implicit_miss` with the matched signals listed per file. Those three codes are non-waivable. "Edges" and "faces/cells" must appear as code, not as comments or log strings.

## Active eat

| Field | Value |
|-------|--------|
| Prefer authority | **Moved** to [[alpha0_stalberg_grid_kernel_r1]] / [[alpha0_stalberg_quad_kernel_r1]] (2026-10-03) |
| This series | **Parked / separate** — not factory armed target |
| Last ladder step held | **2** — [[alpha0_townscaper_tutorial_s2_dual_offset_r1]] (cite-only until re-armed) |
| Step 1 | keep (staging); not discarded |
| Kickoff | do **not** EAT this series unless operator re-arms it deliberately |
| Steps 3–6 | draft / greenlit false |
| Prior invalid attest | [[alpha0_townscaper_tutorial_s1_attest]] — superseded |
| Prior s1 weld | **`failed_altitude_points_as_grid`** — do not F5 |
| Parked non-authority | `row_ux_world_generation_r1_d6` / craft_visual — authority points at the s1 armed packet |

## Failed / frozen altitudes

| Item | Status |
|------|--------|
| [[alpha0_townscaper_craft_visual_r1]] / [[alpha0_townscaper_craft_visual_r2]] | `failed_altitude_metrics_only` |
| [[alpha0_townscaper_craft_core_r1]] | `failed_altitude_metrics_only` for dual/connector Success — reset; files kept |
| s1 hex-19 point-cloud weld (2026-10-02) | `failed_altitude_points_as_grid` |
| [[alpha0_townscaper_df_depth_r1]] | `depth_frozen_until_tutorial_ladder` |
| Terrain3D Prefer | Deferred later |

## Pre-loaded refuse codes (entire series)

| Code | Meaning |
|------|---------|
| `points_as_grid` | Markers at coords with no edges/faces claimed as grid Success |
| `count_equals_topology` | N points present ≠ lattice with cells/edges |
| `prop_scatter_as_composition` | Distinct mesh/prop ids treated as composed modules |
| `bitmask_equals_townscaper` | Bitmask → variant table claimed as dual-grid intent |
| `skip_dual_offset` | GridMap cells only; no half-step dual lattice (steps 2+) |
| `procedural_only_as_success` | Procedural fallback sold as art Success |
| `terrain3d_in_scope` | Terrain3D on craft path |
| `boil_the_ocean_df` | DF-depth / sparky open-world in this ladder |
| `verify_mcp_only` | MCP-as-Success |
| `bundle_tutorial_steps` | Welding multiple tutorial steps in one Prefer |
| `infinite_rect_as_hex19` | Unbounded/rect GridMap sold as fixed hex-19 Success |

Also in play: `craft_terrain_blend` · `terrain3d_leak_f5` · `art_before_mass` · `craft_cam_recenter_on_place` · `explicit_met_implicit_miss`.

## Feedstock (primary authorship — not ladder Success)

**Primary move-pin (locked 2026-10-02):** [[dual-grid-nested-placetile-world-authorship]]. Nesting / biome / living-sim connectivity / Terrain3D hand-off on that card are **aspiration altitude** for later tickets. This series remains the **step-by-step execution ladder**. Hex-19 is a **tutorial scaffold** (must still be a graph), not the ossified product lattice.

## Cross-links

- Active: [[Half-B-Alpha-Mode]] · project `AGENTS.md` · [[Prefer-Authorship-Host-Law]]
- Primary authorship feedstock: [[dual-grid-nested-placetile-world-authorship]] · cohesive: [[COHESIVE-VISION-ART-DIRECTION]]
- Refs seasoning only: `Factory-DRB/references/craft-visual-r2/` · dual-grid diagram cites under `Ingest/` (`single-grid-section.jpg`, `multiple-grid-sections.jpg`, `Final-Grid.jpg`)
