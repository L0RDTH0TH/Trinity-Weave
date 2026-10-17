---
lane_id: presentation
slice_id: row_ux_world_generation_r1_d3
producer_run_id: sp-overnigh-475e8a
package_id: pkg_world_shell
wave: alpha
fidelity: stub
ux_bullet_ids: []
half_b_overlay: alpha0_worldgen_terrain3d_feed_r2
thin_prefer: true
deferred: true
defer_reason: module-primary Prefer rework; activate only if HUD / project.godot wiring required for the three hard gaps
---

# Lane Mission — presentation (deferred Prefer standby)

## Mission

**Standby / deferred** for Prefer `alpha0_worldgen_terrain3d_feed_r2`. Module owns mouse aim, sparky-without-G, and per-place Terrain3D feed. Presentation only activates if LIVE requires `project.godot` input/plugin/main_scene or HUD hint wiring to close UX-1…UX-3 — otherwise do not invent GUI chrome.

## UX bullets you own

- (none while deferred)

## Shape context

See SIB §2 — do not relitigate conceptual lock. Do not smuggle fantasy UI polish, chargen, seats, or tricam.

## Realization notes

If un-deferred by PM rework: touch only `project.godot` / `UI/**` / `GameHud.tscn` (presentation zone); cite which Prefer gap required the touch. No chargen/seats/tricam.

## Done when (deferred)

- Lane receipt may record `deferred: true` with cite to armed packet `lanes_expected: [module]` / `lanes_if_needed: [presentation]`
- If activated: minimal wiring only + receipt cites why module could not complete the gap alone
