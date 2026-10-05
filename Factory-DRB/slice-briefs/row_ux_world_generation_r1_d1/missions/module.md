---
lane_id: module
slice_id: row_ux_world_generation_r1_d1
producer_run_id: sp-weld-pro-1be97b
ux_bullet_ids: ["UX-1"]
---

# Lane Mission — module

## Mission
Deliver your lane contribution for `ux_world_generation` at depth 1.

## UX bullets you own
- **UX-1:** ---
level: 1
row_id: ux_world_generation
label: DM can create (table can shape) a persistent living world
derived_from: L5
scope_kind: depth_slice
---

# DM can create (table can shape) a persistent living world — depth 1 scope

## Level contract
Global depth level 1

## Vision at this depth
## Scaffold minimum

Smallest honest vertical slice for **DM can create (table can shape) a persistent livi

## Shape context
See SIB §2 — do not relitigate conceptual lock.

## Realization notes
See SIB §3 — crosswalk acceptance to your UX bullets.

## Done when
- Build passes
- Lane receipt cites UX bullet ids satisfied

## Hard gap rework (operator 2026-10-01)

**MUST create-or-update** `res://scenes/WorldgenCraft.tscn` under LIVE `genesis-mythos-alpha-20260930/genesis-mythos/scenes/` (module `zone_write` includes `scenes/**`).

- Cite weld brief `alpha0_worldgen_dualgrid_sparky_r1` § Worldgen entry scene / done_when / acceptance item 6.
- Do **not** treat LaunchShell→PlayRegion or `UI/WorldgenCraftControls` as substitute.
- Wire DualGridCraftHost + craft cam so the entry is operator-reachable.
- Lane Success requires the file to exist on disk before seats.
