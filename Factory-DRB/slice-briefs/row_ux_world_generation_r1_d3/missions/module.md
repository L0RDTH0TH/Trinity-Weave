---
lane_id: module
slice_id: row_ux_world_generation_r1_d3
producer_run_id: sp-overnigh-475e8a
package_id: pkg_world_shell
wave: alpha
fidelity: stub
ux_bullet_ids: ["UX-1", "UX-2", "UX-3", "UX-4"]
half_b_overlay: alpha0_worldgen_terrain3d_feed_r2
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

# Lane Mission — module (Terrain3D Prefer rework r2)

## Mission

Thin Prefer rework after operator F5 on `alpha0_worldgen_terrain3d_feed_r1` / `row_ux_world_generation_r1_d2`. Close **three hard playtest gaps** only — do not reopen chargen/seats/tricam or expand full L3 vision.

**Why (UX-first):** Parent Prefer landed Terrain3D host + stamp, but F5 failed house feel: aim was camera-center, sparky gated on G, and craft place left graybox-only until F6. L5 “durable living world the table can see” fails if operators cannot cursor-aim, fly without a seed ritual, or see Terrain3D update per place.

Cite weld brief + armed packet (law):

- `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_worldgen_terrain3d_feed_r2.md`
- `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_worldgen_terrain3d_feed_r2.armed.yaml`

LIVE: `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/`  
Entry: `res://scenes/WorldgenCraft.tscn` (update)  
`host_touch_budget: 1200` — prefer trim into `Systems/`; **never waive** Terrain3D Prefer proof.

## UX bullets you own

- **UX-1:** Place and stamp ray from **mouse cursor** (not camera center). Refuse `camera_center_aim`.
- **UX-2:** Tab → `god_mode_sparky` **without** requiring G seed first. Refuse `sparky_requires_g_seed`. Sparky stays consumer-only.
- **UX-3:** Each craft place/module updates corresponding Terrain3D chunk/region so sparky sees that mesh — not F6-only. Fail visible: `graybox_only_world` / `f6_only_terrain_feed`.
- **UX-4:** Quote Matrix Dual-grid Prefer/Never — Terrain3D height authority + GridMap craft overlay; no second terrain authority.

## Shape context

See SIB §2 — do not relitigate conceptual lock, craft cam, or reopen chargen/seats/tricam. Parent r1 host + `stamp_oasis_desert` remain; extend for per-place feed + aim/sparky gaps.

## Realization notes

See SIB §3 crosswalk. Quote Matrix Dual-grid Prefer (Terrain3D height + GridMap craft overlay). ClassDB Prefer path required — Multimesh/graybox-only under sparky = fail.

## Hard Prefer gaps (operator F5 — ONLY acceptance)

1. **Mouse aim** — place/stamp ray from mouse cursor
2. **Sparky without G** — Tab/sparky without G-seed gate
3. **Craft → Terrain3D per place** — one module place updates Terrain3D chunk/region; sparky sees mesh; not F6-only

## Non-goals (do not smuggle)

- Full biome matrix / second stamp class
- ADC art / TAC polish
- UI polish / chargen / seats / tricam reopen
- Import/attach Path B
- Full L3…L5 inventory beyond these three gaps
- Waiving Terrain3D proof for touch-budget theater

## Done when

- Build passes on Godot 4.6.3 .NET/C# module path
- Lane receipt cites UX-1…UX-4 + Prefer `ask_id: alpha0_worldgen_terrain3d_feed` / overlay `alpha0_worldgen_terrain3d_feed_r2`
- `claim_class: staging`; Matrix Dual-grid Prefer/Never quoted
- Operator F5 checklist = the three hard gaps only
- Ban `verify_mcp_only` as Done
