---
slice_id: row_ux_world_generation_r1_d4
catalog_row_id: ux_world_generation
catalog_row_ids:
  - ux_world_generation
package_id: pkg_world_shell
wave: alpha
fidelity: stub
dispatch_depth: 4
target_depth: 4
producer_run_id: sp-prefer-r3-d4
pillar_packet_hash: prefer-r3-layer-split
half_b_overlay: alpha0_worldgen_terrain3d_feed_r3
thin_prefer: true
ask_id: alpha0_worldgen_terrain3d_feed
parent_prefer: alpha0_worldgen_terrain3d_feed_r2
parent_factory_feed: row_ux_world_generation_r1_d3
composed_at: 2026-10-01T22:46:00Z
---

# Slice Implementation Brief — DM can create (table can shape) a persistent living world

## 1. Product goal (UX)

**North star (L5):** Durable world container — DM creates initial form; table can shape; players do not author the first world.

**Dispatch depth L4 bar (catalog):** Packet carries L4 scope — **this Prefer compose does not expand full L4 vision.** Acceptance is narrowed by Half-B Prefer overlay `alpha0_worldgen_terrain3d_feed_r3` (armed, `thin_prefer: true`) to the **layer-split** hard gaps only.

**Upstream claims justifying this compose:**
- Parent Prefer `alpha0_worldgen_terrain3d_feed_r2` / `row_ux_world_generation_r1_d3` — mouse aim + Tab-without-G landed; F5 failed on cam recenter + craft/Terrain3D blend + feed timing
- Operator Prefer rework — `alpha0_worldgen_terrain3d_feed_r3` + `.armed.yaml` (catalog feed = this `slice_id`)
- Step-1 YT Townscaper dual-grid (Hot Wheels) — https://www.youtube.com/watch?v=Y19Mw5YsgjI · [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] · [[COHESIVE-VISION-ART-DIRECTION]] · [[townscaper-click-add-world-element]]
- Matrix Dual-grid Prefer/Never — Terrain3D height authority + GridMap craft overlay (quote on receipt); **do not re-blend layers**

### UX bullets (stable ids) — Prefer layer-split gaps ONLY

- **UX-1 (no_cam_recenter + mouse_aim):** Craft click places/removes **tiles only** — **no** camera recenter on the new tile. Keep mouse-cursor ray (not camera center). Refuse: `craft_cam_recenter_on_place`, `camera_center_aim`.
- **UX-2 (no_craft_terrain_blend):** Craft view must **NOT** deform the checker/craft grid into Terrain3D heights — place = dual-grid tile addition only (Townscaper / Hot Wheels). Refuse: `craft_terrain_blend` / `inspiration_shape_miss` layer blend.
- **UX-3 (terrain3d_fed_layer + sparky_without_g):** Terrain3D updates only as the **fed** layer — on **Sparky enter** and/or **explicit feed** from the tile map. Sparky sees Terrain3D world derived from tiles; craft view stays toys. Tab → sparky **without** G seed (do not regress). Refuse: `unfed_terrain_under_sparky`, `graybox_only_world`, `sparky_requires_g_seed`.
- **UX-4 (dual_grid_lock):** Matrix **Dual-grid world craft** Prefer/Never remains law — Prefer **Terrain3D** as world/height authority + stock **GridMap** as craft cell overlay; Never a second parallel terrain/physics authority. Layers stay separate at runtime (craft toys ≠ Sparky car).

### Deferred above this Prefer (named — not wave-1 owned)

- Full L4…L5 polish / wizard+preview dialogue suite
- ADC/TAC art, GUI chrome beyond minimal wiring
- Chargen / seats / tricam (do **not** reopen)
- Re-opening r2 live per-place Terrain3D under craft view as Success

**Exit criteria (package `pkg_world_shell` / staging):** Operator F5 = the three hard gaps above (+ prior wins not regress); Matrix Dual-grid Prefer/Never quoted; step-1 YT + Hot-Wheels-vs-car cited; entry `res://scenes/WorldgenCraft.tscn`; `claim_class: staging`; `factory_greenlit: true`. Ban `verify_mcp_only`. Never waive Terrain3D/sparky feed proof for `host_touch_budget` (raise to 1200 or trim into `Systems/`).

## 2. Shape lock (Conceptual)

Do not relitigate:

| Lock | Source |
|------|--------|
| Dual-grid Prefer/Never (Terrain3D height + GridMap craft overlay) | Godot-Implementation-Decision-Matrix + Prefer overlay r3 |
| Step-1 Hot Wheels craft ≠ Terrain3D car | YT Y19Mw5YsgjI + COHESIVE + townscaper-click-add |
| Mouse-cursor aim + Tab sparky without G | Parent Prefer r2 wins — do not regress |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Entry scene | `res://scenes/WorldgenCraft.tscn` (update) |
| No chargen/seats/tricam reopen | Prefer refuse + AGENTS.md |

**Matrix quote (Dual-grid world craft):** Prefer — Terrain3D as **world/height authority** + stock **GridMap** as **craft cell overlay** — **one** craft cell data authority. Never — Second parallel terrain or physics authority; custom voxel engine; GridMap as a second height/terrain authority beside Terrain3D; **blending Terrain3D deformation into craft-tile authorship view**.

## 3. Realization (Execution)

Crosswalk UX bullets → Prefer acceptance (wave 1 module-primary):

| UX | Realization hint |
|----|------------------|
| UX-1 | Pick cell at cursor without moving craft cam/orbit focus onto placed tile; place/remove tiles only |
| UX-2 | Craft phase: GridMap toys visible; Terrain3D height mesh **not** deforming craft checker under craft cam |
| UX-3 | On Tab/Sparky enter (and/or explicit feed): push tile map → Terrain3D; Sparky consumes fed mesh; G optional |
| UX-4 | ClassDB Terrain3D Prefer host + GridMap overlay; Multimesh = fail visible under Sparky |

`host_touch_budget: 1200` — prefer trim into `Systems/`; escalate if Prefer blocked; **never waive** Terrain3D feed proof.

## 4. Lane plan

Wave 1 serial: **module** only. Presentation deferred unless `project.godot` / HUD wiring required. Skip asset/techart.
