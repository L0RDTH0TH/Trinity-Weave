---
title: Slice brief — alpha0_worldgen_terrain3d_feed_r2
slice_id: alpha0_worldgen_terrain3d_feed_r2
ask_id: alpha0_worldgen_terrain3d_feed
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-01
updated: 2026-10-01
claim_class: staging
factory_greenlit: true
status: superseded
template: Half-B-Weld-Brief-Template
supersedes: alpha0_worldgen_terrain3d_feed_r1
superseded_by: alpha0_worldgen_terrain3d_feed_r3
parent_prefer: alpha0_worldgen_terrain3d_feed_r1
parent_factory_feed: row_ux_world_generation_r1_d2
armed_packet: alpha0_worldgen_terrain3d_feed_r2.armed.yaml
launch_word: WELD
---

# Slice brief — `alpha0_worldgen_terrain3d_feed_r2`

Filled from [[Half-B-Weld-Brief-Template]]. **Fill before Half-B code.** Umbrella: [[alpha_architecture_half_b]]. Lock: [[FEEDSTOCK-SHAPE]]. Cohesive cite: [[COHESIVE-VISION-ART-DIRECTION]].

**Superseded / scrapped Prefer chain.** Combined Townscaper+Terrain3D Prefer retired. Active next: [[alpha0_townscaper_craft_core_r1]] (Terrain3D deferred later). Prior: [[alpha0_worldgen_terrain3d_feed_r3]] was last Prefer rework after F5 on [[alpha0_worldgen_terrain3d_feed_r1]] / `row_ux_world_generation_r1_d2`.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_worldgen_terrain3d_feed` |
| `slice_id` | `alpha0_worldgen_terrain3d_feed_r2` |
| Scope | Prefer rework: mouse-cursor ray place/stamp; Tab/sparky without G seed; every craft place updates Terrain3D chunk/region (not F6-only) |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Worldgen entry scene | `res://scenes/WorldgenCraft.tscn` — update |
| Mode | update (thin Prefer rework; module-primary) |
| Catalog feed | Next factory beat after d2 (`row_ux_world_generation_r1_d3` once budget raised) — Half-B overlay law is **this** brief |
| Parent | `alpha0_worldgen_terrain3d_feed_r1` / `row_ux_world_generation_r1_d2` |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| Operator F5 Prefer gaps | Three hard fails below — house bar for this rework |
| Matrix Dual-grid Prefer | Terrain3D height authority + GridMap craft overlay — [[Godot-Implementation-Decision-Matrix]] |
| Step-1 authorship model | Townscaper dual-grid (**Hot Wheels**) — [[townscaper-click-add-world-element]] · [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] (https://www.youtube.com/watch?v=Y19Mw5YsgjI) — craft **feeds** Terrain3D; do **not** re-blend layers |
| r1 Prefer | Terrain3D host + stamp path landed; rework closes playtest gaps without graybox-only Success |
| Cohesive vision | Craft place must read as living Terrain3D under sparky — [[COHESIVE-VISION-ART-DIRECTION]] |

Seasoning: Townscaper craft grammar already landed — do not re-litigate craft cam. GUI chrome out of focus unless UI wiring required for the three gaps.

### Step-1 law — Hot Wheels vs Terrain3D (operator locked 2026-10-01 — Prefer must not re-blend)

- Craft cam = **tile authorship only** — **no** camera recenter on place; **no** deforming craft grid into terrain under craft view
- Dual-grid Townscaper (**Hot Wheels**) **FEEDS** Terrain3D (**real car**) — distinct layers
- Per-place Terrain3D update (gap 3) = **feed path** from craft intent → Terrain3D consumer mesh — **not** blending Terrain3D deformation into craft-tile authorship view
- Cite: [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] · [[COHESIVE-VISION-ART-DIRECTION]]

### Hard Prefer gaps (normative — operator F5)

1. **Mouse aim** — place/stamp must ray from **mouse cursor**, not camera center / focus-only without cursor.
2. **Sparky without G** — Tab → `god_mode_sparky` must work **without** requiring **G** seed first (paint/place/stamp that feeds Terrain3D is enough; blank G ring must not be a gate).
3. **Craft → Terrain3D per place** — townscaper craft is feedstock: placing **one** module/cell must generate/update the corresponding Terrain3D chunk/region. **Not F6-only.** Sparky must see that mesh. Graybox-only under sparky = **fail visible** (`graybox_only_world`).

### Dual-grid Godot representation (unchanged Prefer)

Quote Matrix **Dual-grid world craft**: Prefer **Terrain3D** height authority **+** **GridMap** craft cell overlay — one craft cell data authority; **Never** a second parallel terrain/physics authority or custom voxel engine.

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [x] [[COHESIVE-VISION-ART-DIRECTION]]
- [x] Host-weld: `implementation_factory_loop` + `product_factory_pipeline` (trialing; `factory_greenlit: true`; word-gated WELD)
- [x] [[Godot-Implementation-Decision-Matrix]] — Dual-grid Prefer/Never + Terrain3D Prefer
- [ ] [[ENGINE-COMPILE-PACK-stock_godot_fps]] — not primary
- [x] [[INSPIRATION-HALF-B-SHAPE]]
- [x] [[Camera-Mode-Taxonomy-Live]] — craft cam + sparky consumer-only (no G gate)
- [x] [[Visual-Factory-Direction-Stylized-Low-Poly]] — cite when Terrain3D mesh shows
- [ ] [[GUI-Chrome-Direction-Fantasy-UI]] — only if HUD hint wiring required for gaps

## 4. End flavor

Operator paints/places under craft cam with **cursor-true** aim; each place updates Terrain3D; Tab flies that mesh **without** a mandatory G seed. F6 stamp remains available but is **not** the only Terrain3D feed path.

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | (1) Place and stamp ray from **mouse cursor** (not camera center); (2) Tab/sparky works **without** requiring G seed first; (3) Each craft place/module updates corresponding Terrain3D chunk/region so sparky sees that mesh — not F6-only / not graybox-only; Matrix Dual-grid Prefer/Never quoted; entry `res://scenes/WorldgenCraft.tscn` |
| Operator attest | F5 checklist = the three hard gaps above; **ban** `verify_mcp_only`; **ban** graybox-only under sparky |
| `claim_class` | `staging` — not `ask_success`; factory greenlit true |

## 6. Refuse

Matrix **Never** + factory rejects:

`inspiration_shape_miss` · `fidelity_miss` · `engine_pattern_miss` · `verify_mcp_only` · `parallel_terrain_engine` · `graybox_only_world` · `camera_center_aim` · `sparky_requires_g_seed` · `f6_only_terrain_feed`

| Code | Note |
|------|------|
| `camera_center_aim` | Place/stamp uses camera center / unrealted focus instead of mouse-cursor ray |
| `sparky_requires_g_seed` | Tab→sparky blocked unless operator pressed G |
| `f6_only_terrain_feed` | Only F6 stamp updates Terrain3D; plain place leaves graybox-only world |
| `graybox_only_world` | Sparky sees GridMap/Multimesh only — Terrain3D mesh not updated |
| `inspiration_shape_miss` / layer blend | Prefer that blends craft tiles with Terrain3D deformation **in craft view**, recenters craft cam on place, or deforms craft grid into terrain under craft cam — violates step-1 Hot Wheels vs real-car law ([[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]]) |
| Instant Success | MCP-only / screenshot-only is not Done |
| Scope smuggle | Chargen/seats/tricam; full biome matrix; ADC art; reopening whole L3+ inventory beyond these three gaps |

## 7. Out of scope

- PF1 chargen / seats / tricam (do **not** reopen)
- Full biome matrix / second stamp class
- ADC art / TAC polish
- GUI chrome beyond minimal hint/wiring for the three gaps
- Nested dungeon grids, settlement path-connect
- Investor demo / archived `horizon_demo_investor`
- `dev/FpsSanity*.tscn` as Success proof
- Waiving Terrain3D proof for host_touch_budget — escalate budget or trim into `Systems/`; do **not** waive Prefer proof

## 8. Receipt (required on Half-B completion)

1. `ask_id` / `slice_id` (r2)
2. Matrix Prefer quotes — Dual-grid + Terrain3D height authority
3. Hard Prefer gaps closed under step-1 separation law (Hot Wheels craft feeds Terrain3D; no craft-view Terrain3D blend)
4. Mouse-cursor ray proof for place **and** stamp
5. Tab/sparky without G seed proof
6. Per-place Terrain3D chunk/region update proof (sparky sees mesh; not F6-only) — feed path, not craft-layer blend
7. No chargen/seats/tricam smuggle; module-only unless presentation `project.godot` required
8. `claim_class: staging` · `factory_greenlit: true`
9. Operator attest or explicit debt

## Related

- [[alpha0_worldgen_terrain3d_feed_r1]] · [[alpha0_worldgen_dualgrid_sparky_r1]] · [[alpha_architecture_half_b]] · [[Half-B-Weld-Brief-Template]] · [[Ask-Fidelity-Exemplars]] · [[COHESIVE-VISION-ART-DIRECTION]] · [[FEEDSTOCK-SHAPE]] · [[Godot-Implementation-Decision-Matrix]] · [[townscaper-click-add-world-element]] · [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]]
