---
title: Slice brief — alpha0_worldgen_terrain3d_feed_r3
slice_id: alpha0_worldgen_terrain3d_feed_r3
ask_id: alpha0_worldgen_terrain3d_feed
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-01
updated: 2026-10-01
claim_class: staging
factory_greenlit: true
status: superseded_scrapped
template: Half-B-Weld-Brief-Template
supersedes: alpha0_worldgen_terrain3d_feed_r2
superseded_by: alpha0_townscaper_craft_core_r1
parent_prefer: alpha0_worldgen_terrain3d_feed_r2
parent_factory_feed: row_ux_world_generation_r1_d3
armed_packet: alpha0_worldgen_terrain3d_feed_r3.armed.yaml
launch_word: WELD
---

# Slice brief — `alpha0_worldgen_terrain3d_feed_r3`

Filled from [[Half-B-Weld-Brief-Template]]. **Fill before Half-B code.** Umbrella: [[alpha_architecture_half_b]]. Lock: [[FEEDSTOCK-SHAPE]]. Cohesive cite: [[COHESIVE-VISION-ART-DIRECTION]].

**SCRAPPED 2026-10-01** — combined Townscaper+Terrain3D Prefer retired. Next eat chain: [[alpha0_townscaper_craft_core_r1]] → [[alpha0_townscaper_craft_visual_r1]] → [[alpha0_townscaper_df_depth_r1]] (Terrain3D feed deferred to a later ticket).

**Thin Prefer rework** after operator F5 on [[alpha0_worldgen_terrain3d_feed_r2]] / `row_ux_world_generation_r1_d3`. Closes **layer-split** playtest fails — do **not** reopen chargen/seats/tricam; do **not** re-blend Hot Wheels craft with Terrain3D car.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_worldgen_terrain3d_feed` |
| `slice_id` | `alpha0_worldgen_terrain3d_feed_r3` |
| Scope | Prefer rework: craft = tile authorship only (no cam recenter; no craft-view Terrain3D deform); Terrain3D = fed layer on Sparky enter / explicit feed; keep mouse-cursor aim + Tab sparky without G |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Worldgen entry scene | `res://scenes/WorldgenCraft.tscn` — update |
| Mode | update (thin Prefer rework; module-primary) |
| Catalog feed | `row_ux_world_generation_r1_d4` once budget raised — Half-B overlay law is **this** brief |
| Parent | `alpha0_worldgen_terrain3d_feed_r2` / `row_ux_world_generation_r1_d3` |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| Operator F5 Prefer gaps (r2 fails) | Three hard layer-split fails below — house bar for this rework |
| Canonical YT step-1 | Townscaper dual-grid authorship — https://www.youtube.com/watch?v=Y19Mw5YsgjI · [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] |
| Hot Wheels vs car | Craft cam = **Hot Wheels / Townscaper tile authorship ONLY**; Terrain3D = **real car**, fed by tile map, inspected under Sparky — [[COHESIVE-VISION-ART-DIRECTION]] · [[townscaper-click-add-world-element]] |
| Matrix Dual-grid Prefer | Terrain3D height authority + GridMap craft overlay — [[Godot-Implementation-Decision-Matrix]] — **do not re-blend layers** |
| r2 Prefer | Mouse aim + Tab-without-G landed — **keep**; per-place live Terrain3D push under craft view **regressed** into layer blend — fix |

Seasoning: GUI chrome out of focus unless wiring required for the three gaps. Do not re-litigate craft cam orbit grammar beyond **no recenter on place**.

### Step-1 law — Hot Wheels vs Terrain3D (operator locked 2026-10-01 — MUST encode; do not re-blend)

- **Craft cam** = tile authorship only (Townscaper / Hot Wheels) — place/remove **tiles**; **no** camera recenter on the new tile; **no** deforming craft checker/grid into Terrain3D heights under craft view
- **Terrain3D** = real car — **FED** by the craft tile map; inspected under **Sparky** — not the craft mesh
- Distinct layers: dual-grid Townscaper **feeds** Terrain3D; Prefer must **not** blend Terrain3D deformation into craft-tile authorship view
- Cite: [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] · [[COHESIVE-VISION-ART-DIRECTION]] · [[townscaper-click-add-world-element]] · YT `Y19Mw5YsgjI`

### Hard Prefer gaps (normative — operator F5 after r2)

1. **No cam recenter** — craft click places/removes **tiles only**; camera must **not** recenter/orbit-focus onto the new tile (`craft_cam_recenter_on_place` banned). Keep mouse-cursor aim (not camera-center).
2. **No craft-view Terrain3D blend** — craft view must **not** deform the checker/craft grid into Terrain3D heights; place = dual-grid tile addition only (Townscaper model). Refuse `craft_terrain_blend` / `inspiration_shape_miss` layer blend.
3. **Terrain3D as fed layer** — Terrain3D updates only as the **fed** layer: on **Sparky enter** and/or **explicit feed** from the tile map (e.g. stamp / feed command). Sparky sees Terrain3D world **derived from tiles**; craft view stays toys. Do **not** waive Terrain3D/sparky feed proof.

### Prior Prefer wins (still true — do not regress)

- **Mouse-cursor aim** — place/stamp ray from mouse cursor (not camera center). Refuse `camera_center_aim`.
- **Tab sparky without G** — Tab → `god_mode_sparky` without requiring G seed. Refuse `sparky_requires_g_seed`.

### Dual-grid Godot representation (unchanged Prefer)

Quote Matrix **Dual-grid world craft**: Prefer **Terrain3D** height authority **+** **GridMap** craft cell overlay — one craft cell data authority; **Never** a second parallel terrain/physics authority or custom voxel engine. Layers stay separate at runtime under craft vs Sparky.

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [x] [[COHESIVE-VISION-ART-DIRECTION]]
- [x] Host-weld: `implementation_factory_loop` + `product_factory_pipeline` (trialing; `factory_greenlit: true`; word-gated WELD)
- [x] [[Godot-Implementation-Decision-Matrix]] — Dual-grid Prefer/Never + Terrain3D Prefer
- [ ] [[ENGINE-COMPILE-PACK-stock_godot_fps]] — not primary
- [x] [[INSPIRATION-HALF-B-SHAPE]]
- [x] [[Camera-Mode-Taxonomy-Live]] — craft cam tile authorship + sparky consumer-only (no G gate)
- [x] [[Visual-Factory-Direction-Stylized-Low-Poly]] — cite when Terrain3D mesh shows under Sparky
- [x] [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] + [[townscaper-click-add-world-element]]
- [ ] [[GUI-Chrome-Direction-Fantasy-UI]] — only if HUD hint wiring required for gaps

## 4. End flavor

Operator clicks tiles under craft cam like Townscaper toys (cursor-true, no cam yank, flat craft grid). Tab flies Sparky over the **fed** Terrain3D world derived from that tile map — Hot Wheels authorship, real-car inspection. G remains optional; F6/explicit feed remains available but craft place alone must not blend layers.

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | (1) Craft place/remove = tiles only with **no** camera recenter; mouse-cursor aim retained; (2) Craft view does **not** deform checker/craft grid into Terrain3D heights — tile addition only; (3) Terrain3D updates as **fed** layer on Sparky enter and/or explicit feed from tile map — Sparky sees Terrain3D derived from tiles; craft stays toys; Tab sparky without G retained; Matrix Dual-grid Prefer/Never quoted; entry `res://scenes/WorldgenCraft.tscn` |
| Operator attest | F5 checklist = the three hard gaps above (+ prior wins not regress); **ban** `verify_mcp_only`; **ban** graybox-only under sparky; **ban** craft-view Terrain3D blend |
| `claim_class` | `staging` — not `ask_success`; factory greenlit true |

## 6. Refuse

Matrix **Never** + factory rejects:

`inspiration_shape_miss` · `fidelity_miss` · `engine_pattern_miss` · `verify_mcp_only` · `parallel_terrain_engine` · `graybox_only_world` · `camera_center_aim` · `sparky_requires_g_seed` · `craft_cam_recenter_on_place` · `craft_terrain_blend` · `unfed_terrain_under_sparky`

| Code | Note |
|------|------|
| `craft_cam_recenter_on_place` | Place/remove recenters craft cam / orbit focus onto the new tile |
| `craft_terrain_blend` | Craft view shows Terrain3D height deformation / blended checker into terrain (Hot Wheels≠car violated) |
| `unfed_terrain_under_sparky` | Sparky enters without Terrain3D fed from tile map (and no explicit feed path) — graybox-only / unfed |
| `camera_center_aim` | Place/stamp uses camera center instead of mouse-cursor ray (prior win — do not regress) |
| `sparky_requires_g_seed` | Tab→sparky blocked unless G (prior win — do not regress) |
| `graybox_only_world` | Sparky sees GridMap/Multimesh only — Terrain3D mesh not fed from tiles |
| `inspiration_shape_miss` | Prefer re-blends craft tiles with Terrain3D deformation in craft view — violates step-1 YT / Hot-Wheels-vs-car |
| Instant Success | MCP-only / screenshot-only is not Done |
| Scope smuggle | Chargen/seats/tricam; full biome matrix; ADC art; reopening whole L3+ inventory beyond these gaps |

## 7. Out of scope

- PF1 chargen / seats / tricam (do **not** reopen)
- Full biome matrix / second stamp class
- ADC art / TAC polish
- GUI chrome beyond minimal hint/wiring for the three gaps
- Nested dungeon grids, settlement path-connect
- Investor demo / archived `horizon_demo_investor`
- `dev/FpsSanity*.tscn` as Success proof
- Waiving Terrain3D/sparky feed proof for host_touch_budget — escalate budget or trim into `Systems/`; do **not** waive Prefer proof
- Re-opening r2 “live per-place Terrain3D under craft view” as Success (that path caused layer blend)

## 8. Receipt (required on Half-B completion)

1. `ask_id` / `slice_id` (r3)
2. Matrix Prefer quotes — Dual-grid + Terrain3D height authority
3. Step-1 YT + Hot-Wheels-vs-car cited; layers not re-blended
4. No craft-cam recenter on place/remove proof
5. Craft view stays tile toys (no Terrain3D height deform under craft)
6. Terrain3D feed on Sparky enter and/or explicit feed; Sparky sees fed mesh
7. Mouse-cursor aim + Tab sparky without G retained (no regress)
8. No chargen/seats/tricam smuggle; module-only unless presentation `project.godot` required
9. `claim_class: staging` · `factory_greenlit: true`
10. Operator attest or explicit debt

## Related

- [[alpha0_worldgen_terrain3d_feed_r2]] · [[alpha0_worldgen_terrain3d_feed_r1]] · [[alpha0_worldgen_dualgrid_sparky_r1]] · [[alpha_architecture_half_b]] · [[Half-B-Weld-Brief-Template]] · [[Ask-Fidelity-Exemplars]] · [[COHESIVE-VISION-ART-DIRECTION]] · [[FEEDSTOCK-SHAPE]] · [[Godot-Implementation-Decision-Matrix]] · [[townscaper-click-add-world-element]] · [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]]
