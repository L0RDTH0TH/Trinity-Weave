---
lane_id: module
slice_id: row_ux_world_generation_r1_d4
producer_run_id: sp-prefer-r3-d4
package_id: pkg_world_shell
wave: alpha
fidelity: stub
ux_bullet_ids: ["UX-1", "UX-2", "UX-3", "UX-4"]
half_b_overlay: alpha0_worldgen_terrain3d_feed_r3
thin_prefer: true
ask_id: alpha0_worldgen_terrain3d_feed
zone_write:
  - scenes/**
  - addons/terrain_3d/**
  - Systems/**
  - Core/**
  - Camera/**
  - Player/**
---

# Lane Mission — module (Terrain3D Prefer layer-split r3)

## Mission

Thin Prefer rework after operator F5 on `alpha0_worldgen_terrain3d_feed_r2` / `row_ux_world_generation_r1_d3`. Close **layer-split** hard gaps only — do not reopen chargen/seats/tricam; do not re-blend Hot Wheels craft with Terrain3D car.

**Why (UX-first):** r2 landed mouse aim + Tab-without-G, but F5 failed house feel: place yanked cam to the new tile, craft view deformed checker/grid into Terrain3D heights, and live per-place Terrain3D push under craft violated step-1 Townscaper authorship (Hot Wheels ≠ real car).

Cite weld brief + armed packet (law):

- `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_worldgen_terrain3d_feed_r3.md`
- `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_worldgen_terrain3d_feed_r3.armed.yaml`
- Step-1 YT: https://www.youtube.com/watch?v=Y19Mw5YsgjI · `Ingest/Resources/Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md` · COHESIVE · townscaper-click-add

LIVE: `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/`  
Entry: `res://scenes/WorldgenCraft.tscn` (update)  
`host_touch_budget: 1200` — prefer trim into `Systems/`; **never waive** Terrain3D Prefer proof.

## UX bullets you own

- **UX-1:** Place/remove **tiles only** — **no** camera recenter on new tile; keep mouse-cursor aim. Refuse `craft_cam_recenter_on_place`, `camera_center_aim`.
- **UX-2:** Craft view stays Townscaper toys — **no** deforming checker/craft grid into Terrain3D heights. Refuse `craft_terrain_blend`.
- **UX-3:** Terrain3D updates as **fed** layer on Sparky enter and/or explicit feed from tile map; Sparky sees Terrain3D derived from tiles; Tab sparky without G. Refuse `unfed_terrain_under_sparky`, `graybox_only_world`, `sparky_requires_g_seed`.
- **UX-4:** Quote Matrix Dual-grid Prefer/Never — Terrain3D height authority + GridMap craft overlay; layers not re-blended under craft.

## Shape context

See SIB §2 — do not relitigate conceptual lock or reopen chargen/seats/tricam. Parent r2 mouse/sparky wins remain; replace live per-place craft-view Terrain3D push with deferred/explicit feed.

## Realization notes

Likely touch (trim into `Systems/` / `Core/WorldGen/` / `Player/`):

1. Stop craft-cam focus yank on place (`SetFocusWorld` / focus move in pick) — pick cell without recentering orbit.
2. Craft place/remove = GridMap tile ops only; do **not** push Terrain3D heights while craft view is active (or hide Terrain3D under craft so checker stays flat toys).
3. On Sparky enter (and/or explicit feed/stamp): feed tile map → Terrain3D `set_height`/`update_maps`; Sparky consumes fed mesh.
4. Retain `TryPickCellAtCursor` + Tab without G.

## Hard Prefer gaps (operator F5 — ONLY acceptance)

1. **No cam recenter** — place/remove tiles; camera stays put
2. **No craft Terrain3D blend** — craft checker/grid not deformed into terrain heights
3. **Terrain3D fed layer** — Sparky enter and/or explicit feed; Sparky sees Terrain3D from tiles; craft stays toys

Also: mouse-cursor aim + Tab sparky without G must not regress.

## Non-goals (do not smuggle)

- Full biome matrix / second stamp class
- ADC art / TAC polish
- UI polish / chargen / seats / tricam reopen
- Waiving Terrain3D proof for touch-budget theater
- Re-blending layers under craft cam as “Success”

## Done when

- Build passes on Godot 4.6.3 .NET/C# module path
- Lane receipt cites UX-1…UX-4 + Prefer `ask_id: alpha0_worldgen_terrain3d_feed` / overlay `alpha0_worldgen_terrain3d_feed_r3`
- Step-1 YT + Hot-Wheels-vs-car cited on receipt
- `claim_class: staging`; Matrix Dual-grid Prefer/Never quoted
- Operator F5 checklist = the three hard gaps (+ prior wins)
- Ban `verify_mcp_only` as Done
