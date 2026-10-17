---
lane_id: module
slice_id: row_ux_world_generation_r1_d2
producer_run_id: sp-overnigh-1f9b7c
package_id: pkg_world_shell
wave: alpha
fidelity: stub
ux_bullet_ids: ["UX-1", "UX-2", "UX-3", "UX-4", "UX-5"]
half_b_overlay: alpha0_worldgen_terrain3d_feed_r1
zone_write:
  - scenes/**
  - addons/terrain_3d/**
  - Systems/**
  - Core/**
---

# Lane Mission — module (Terrain3D feed Prefer)

## Mission

Thin Prefer after `alpha0_worldgen_dualgrid_sparky_r1` POC: craft/stamp feeds **Terrain3D** so Sparky inspects real Terrain3D terrain — not placed graybox models alone.

**Why (UX-first):** L5 promises a durable living world the table can see and the DM can retcon. At L2 Prefer altitude, “durable residue” means the stamp path updates a Terrain3D mesh operators can fly — graybox-only fails the house.

Cite weld brief + armed packet (law):

- `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_worldgen_terrain3d_feed_r1.md`
- `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_worldgen_terrain3d_feed_r1.armed.yaml`

LIVE: `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/`  
Entry: `res://scenes/WorldgenCraft.tscn` (update)

## UX bullets you own

- **UX-1:** Privileged seats enter WorldgenCraft; wrong seat refuses visibly.
- **UX-2:** `stamp_oasis_desert` → Terrain3D height/region; mesh updates.
- **UX-3:** Players cannot author the first world (gate world-hitting commits).
- **UX-4:** Terrain3D host under WorldgenCraft / DualGridCraftHost; Matrix Dual-grid Prefer/Never; fail `graybox_only_world` / `parallel_terrain_engine`.
- **UX-5:** Sparky consumer-only over that Terrain3D mesh after stamp.

## Shape context

See SIB §2 — do not relitigate conceptual lock or reopen full L2 vision beyond this Prefer.

## Realization notes

See SIB §3 crosswalk. Quote Matrix Dual-grid Prefer (Terrain3D height + GridMap craft overlay). ClassDB Prefer path required — Multimesh-only Success = fail.

## Hard gap rework (operator 2026-10-01 — Terrain3D feed)

**MUST** land Prefer proof on LIVE tree:

1. Terrain3D host under `WorldgenCraft` / `DualGridCraftHost`
2. One stamp path: `stamp_oasis_desert` pushes into Terrain3D data
3. Sparky consumer-only after stamp
4. Fail visible: GridMap/Multimesh alone without Terrain3D mesh update

## Non-goals (do not smuggle)

- Full biome matrix / second stamp class
- ADC art / TAC polish
- UI polish / chargen / seats / tricam
- Import/attach Path B
- Reopening whole L5 inventory beyond Prefer

## Done when

- Build passes on Godot 4.6.3 .NET/C# module path
- Lane receipt cites UX-1…UX-5 + Prefer `ask_id: alpha0_worldgen_terrain3d_feed`
- `claim_class: staging`; Matrix Prefer/Never quoted
- Operator F5 checklist ready: place/stamp → Terrain3D updates → sparky flies that mesh
- Ban `verify_mcp_only` as Done
