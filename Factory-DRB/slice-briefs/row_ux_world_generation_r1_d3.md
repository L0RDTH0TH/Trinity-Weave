---
slice_id: row_ux_world_generation_r1_d3
catalog_row_id: ux_world_generation
catalog_row_ids:
  - ux_world_generation
package_id: pkg_world_shell
wave: alpha
fidelity: stub
dispatch_depth: 3
target_depth: 3
producer_run_id: sp-overnigh-475e8a
pillar_packet_hash: 035cd14ba5a3fe27
half_b_overlay: alpha0_worldgen_terrain3d_feed_r2
thin_prefer: true
ask_id: alpha0_worldgen_terrain3d_feed
parent_prefer: alpha0_worldgen_terrain3d_feed_r1
parent_factory_feed: row_ux_world_generation_r1_d2
composed_at: 2026-10-01T21:55:02Z
---

# Slice Implementation Brief — DM can create (table can shape) a persistent living world

## 1. Product goal (UX)

**North star (L5):** Durable world container — DM creates initial form via wizard+preview (tone-aware shape families, cached/pre-existing assets); table can shape; players do not author the first world. Physical/settlement layers + monster-region tags; import/attach first-class; every world-hitting change is DM-retconnable. Multiple campaigns/casts attach to the same world.

**Child surface:** `ux_worldgen_gui` — propose → refine → preview → accept/regenerate.

**Dispatch depth L3 bar (catalog):** Packet carries L3 scope — **this Prefer compose does not expand full L3 vision.** Acceptance is narrowed by Half-B Prefer overlay `alpha0_worldgen_terrain3d_feed_r2` (armed, `thin_prefer: true`) to the three operator-F5 hard gaps only.

**Upstream claims justifying this compose:**
- L5 moment inventory + contract clauses (`scopes/ux_world_generation/L5.md`) — context only; not wave-1 inventory
- Parent Prefer `alpha0_worldgen_terrain3d_feed_r1` / factory feed `row_ux_world_generation_r1_d2` — Terrain3D host + stamp path landed; F5 left three playtest fails
- Operator Prefer rework — `alpha0_worldgen_terrain3d_feed_r2` + `.armed.yaml` (catalog feed = this `slice_id`)
- Matrix Dual-grid Prefer/Never — Terrain3D height authority + GridMap craft overlay (quote on receipt)

### UX bullets (stable ids) — Prefer gaps ONLY

- **UX-1 (mouse_aim):** Place and stamp ray from the **mouse cursor**, not camera center / focus-only without cursor. Refuse: `camera_center_aim`.
- **UX-2 (sparky_without_g):** Tab → `god_mode_sparky` works **without** requiring **G** seed first (paint/place/stamp that feeds Terrain3D is enough; blank G ring must not gate sparky). Refuse: `sparky_requires_g_seed`.
- **UX-3 (craft_place_feeds_terrain3d):** Placing **one** craft module/cell updates the corresponding Terrain3D chunk/region so sparky sees that mesh — **not F6-only**. Graybox-only under sparky = fail visible (`graybox_only_world` / `f6_only_terrain_feed`).
- **UX-4 (dual_grid_lock):** Matrix **Dual-grid world craft** Prefer/Never remains law — Prefer **Terrain3D** as world/height authority + stock **GridMap** as craft cell overlay (one craft cell data authority); Never a second parallel terrain/physics authority or custom voxel engine. Quote on lane receipt.

### Deferred above this Prefer (named — not wave-1 owned)

- Full L3…L5 polish / wizard+preview dialogue suite
- L5 clause 4 import/attach first-class (Path B)
- Full settlement + monster-region tag matrices
- Multi-campaign/cast attach UX polish
- Full DM-retcon suite beyond per-place Terrain3D update
- ADC/TAC art, GUI chrome beyond minimal wiring for the three gaps
- Chargen / seats / tricam (do **not** reopen)
- Re-litigating craft cam (already landed)

**Exit criteria (package `pkg_world_shell` / staging):** Operator F5 = the three hard gaps above; Matrix Dual-grid Prefer/Never quoted; entry `res://scenes/WorldgenCraft.tscn`; `claim_class: staging`; `factory_greenlit: true`. Ban `verify_mcp_only`. Never waive Terrain3D Prefer proof for `host_touch_budget` (raise to 1200 or trim into `Systems/`).

## 2. Shape lock (Conceptual)

Do not relitigate:

| Lock | Source |
|------|--------|
| Long-lived `WorldShellController` under Main→World; regenerate by swapping World children | Phase-2 execution primary |
| Seat gate before accept/regenerate/import | L5 + JUNIOR WORK-ORDER paint |
| Preview residue ≠ durable world until accept | L5 wizard+preview moments |
| Terrain via `ITerrainAuthority` (Terrain3D); Gaea = map-data parallel only — not terrain authority | Phase-2 C# weave + Junior-Tech-Adapt |
| Dual-grid Prefer/Never (Terrain3D height + GridMap craft overlay) | Godot-Implementation-Decision-Matrix + Prefer overlay r2 |
| Terrain3D host + `stamp_oasis_desert` path already landed in r1/d2 | Parent Prefer — extend, do not rebuild |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Entry scene | `res://scenes/WorldgenCraft.tscn` (update) |
| No chargen/seats/tricam reopen | Prefer refuse + AGENTS.md |

Conceptual pin ref: `[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]` (packet `conceptual.body` empty — shape taken from execution paint + Prefer brief r2; not a pillar conflict for this Prefer).

**Matrix quote (Dual-grid world craft):** Prefer — Terrain3D (or existing Prefer terrain) as **world/height authority** + stock **GridMap** (or equivalent stock grid) as **craft cell overlay** — **one** craft cell data authority. Never — Second parallel terrain or physics authority; custom voxel engine for this ticket; GridMap (or other) as a second height/terrain authority beside Terrain3D.

## 3. Realization (Execution)

Crosswalk UX bullets → Prefer acceptance (wave 1 module-primary):

| UX id | Realization | Verify / done signal |
|-------|-------------|----------------------|
| UX-1 | Place + stamp pick rays use mouse-cursor screen position → world ray | Cursor-true aim on F5; refuse camera-center aim |
| UX-2 | Tab → sparky without G-seed gate; sparky remains consumer-only | Sparky after place/stamp alone; refuse `sparky_requires_g_seed` |
| UX-3 | Per-module craft place pushes corresponding Terrain3D chunk/region; F6 stamp remains optional not sole feed | Sparky sees Terrain3D mesh after one place; refuse F6-only / graybox-only |
| UX-4 | Keep Terrain3D host under WorldgenCraft / DualGridCraftHost; GridMap craft overlay | Receipt quotes Dual-grid Prefer/Never |

Execution pin excerpt (Prefer subset only):

- Terrain3D via `ITerrainAuthority` — per-place feed must update mesh (not Multimesh/graybox Success)
- Godot 4.6.3 .NET/C# module path compiles
- `host_touch_budget: 1200` — prefer trim into `Systems/`; escalate if budget blocks Prefer proof; **never waive** Terrain3D proof
- Full `WorldShellController` Unauthorized leaf-true remains open debt if Prefer does not touch shell API — cite debt; do not claim shell AC closed

## 4. Cell roster

| Lane | Role this Prefer | Owns |
|------|------------------|------|
| `module` | Wave 1 — mouse-cursor ray; sparky without G; per-place Terrain3D feed | UX-1…UX-4 |
| `presentation` | Deferred — only if HUD / `project.godot` wiring required for the three gaps | (none unless un-deferred) |
| `asset` / `techart` | Skip — no ADC/TAC pass | — |

Wave 1 is **serial module-only** (`parallel: false`). Harness stages PQ from CDP — Producer does not append PQ.
