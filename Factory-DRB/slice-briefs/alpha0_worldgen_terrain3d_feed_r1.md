---
title: Slice brief — alpha0_worldgen_terrain3d_feed_r1
slice_id: alpha0_worldgen_terrain3d_feed_r1
ask_id: alpha0_worldgen_terrain3d_feed
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-01
updated: 2026-10-01
claim_class: staging
factory_greenlit: true
status: superseded_by_prefer
template: Half-B-Weld-Brief-Template
supersedes: alpha0_worldgen_dualgrid_sparky_r1
superseded_by: alpha0_worldgen_terrain3d_feed_r2
armed_packet: alpha0_worldgen_terrain3d_feed_r1.armed.yaml
launch_word: WELD
---

# Slice brief — `alpha0_worldgen_terrain3d_feed_r1`

Filled from [[Half-B-Weld-Brief-Template]]. **Fill before Half-B code.** Umbrella: [[alpha_architecture_half_b]]. Lock: [[FEEDSTOCK-SHAPE]]. Cohesive cite: [[COHESIVE-VISION-ART-DIRECTION]].

**POC Prefer landed.** Active Prefer rework is now [[alpha0_worldgen_terrain3d_feed_r2]] (operator F5: mouse aim · sparky without G · place→Terrain3D). Thin Prefer after [[alpha0_worldgen_dualgrid_sparky_r1]] POC. Goal: craft/stamp feeds **Terrain3D** so Sparky inspects real Terrain3D terrain — not placed graybox models alone.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_worldgen_terrain3d_feed` |
| `slice_id` | `alpha0_worldgen_terrain3d_feed_r1` |
| Scope | Terrain3D host under WorldgenCraft / DualGridCraftHost; one stamp path `stamp_oasis_desert` → Terrain3D height/data; Sparky consumer-only over that mesh |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Worldgen entry scene | `res://scenes/WorldgenCraft.tscn` — update (already exists from r1) |
| Mode | update (thin Prefer; do not reopen whole cell scope) |
| Catalog feed | `row_ux_world_generation_r1_d2` (budget raise → dispatch depth 2) — Half-B overlay law is **this** brief |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| Matrix Dual-grid Prefer | Terrain3D as world/height authority — [[Godot-Implementation-Decision-Matrix]] |
| r1 POC | Dual-grid craft + stamp + sparky handoff already landed; this Prefer closes graybox-only fail |
| Cohesive vision | Open-world craft reads as real terrain under sparky — [[COHESIVE-VISION-ART-DIRECTION]] |
| 3D bar | Astroneer stylized low poly when Terrain3D mesh shows — [[Visual-Factory-Direction-Stylized-Low-Poly]] |

Seasoning: Townscaper craft grammar already landed in r1 — do not re-litigate craft cam. GUI chrome out of focus.

### Terrain3D feed (normative)

1. **Host:** Live Terrain3D node under WorldgenCraft / DualGridCraftHost (Matrix Prefer). ClassDB Prefer path required for Success; Multimesh/graybox-only height preview = **fail visible**.
2. **Stamp path:** Named stamp **`stamp_oasis_desert`** must push height/region data into Terrain3D (not GridMap boxes as sole visible world).
3. **Sparky:** Consumer-only — inspect/fly the Terrain3D mesh after stamp; sparky does not author terrain.
4. **Fail visible:** Placed GridMap / Multimesh models alone without Terrain3D mesh update = fail.

### Dual-grid Godot representation (unchanged Prefer)

Quote Matrix **Dual-grid world craft**: Prefer **Terrain3D** height authority **+** **GridMap** craft cell overlay — one craft cell data authority; **Never** a second parallel terrain/physics authority or custom voxel engine.

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [x] [[COHESIVE-VISION-ART-DIRECTION]]
- [x] Host-weld: `implementation_factory_loop` + `product_factory_pipeline` (trialing; `factory_greenlit: true`; word-gated WELD)
- [x] [[Godot-Implementation-Decision-Matrix]] — Dual-grid Prefer/Never + Terrain3D Prefer
- [ ] [[ENGINE-COMPILE-PACK-stock_godot_fps]] — not primary (no player FPS claim)
- [x] [[INSPIRATION-HALF-B-SHAPE]]
- [x] [[Camera-Mode-Taxonomy-Live]] — craft cam already landed; sparky post-stamp inspect only
- [x] [[Visual-Factory-Direction-Stylized-Low-Poly]] — cite when Terrain3D mesh lands
- [ ] [[GUI-Chrome-Direction-Fantasy-UI]] — out of scope

## 4. End flavor

After r1 dual-grid craft POC: operator paints/stamps under craft cam and **sees Terrain3D terrain update**. Tab→sparky flies **that** Terrain3D mesh. Graybox GridMap cells may remain as craft overlay — they must not be the only flyable “world.”

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | Terrain3D host armed under WorldgenCraft / DualGridCraftHost (ClassDB Prefer, not degraded Multimesh-only Success); `stamp_oasis_desert` writes height/region into Terrain3D data so the Terrain3D mesh visibly updates; Sparky inspect/fly consumes that Terrain3D mesh (consumer-only); Matrix Dual-grid Prefer/Never quoted; entry remains `res://scenes/WorldgenCraft.tscn` |
| Operator attest | F5: place/stamp → Terrain3D updates → sparky flies that mesh; **ban** `verify_mcp_only`; **ban** placed models alone as Success |
| `claim_class` | `staging` — not `ask_success`; factory greenlit true |

## 6. Refuse

Matrix **Never** + factory rejects:

`inspiration_shape_miss` · `fidelity_miss` · `engine_pattern_miss` · `verify_mcp_only` · `parallel_terrain_engine` · `graybox_only_world`

| Code | Note |
|------|------|
| `graybox_only_world` | Stamp/paint leaves only GridMap/Multimesh boxes; Terrain3D mesh not updated or ClassDB Prefer not armed |
| `parallel_terrain_engine` | Second terrain/physics authority or custom voxel beside Matrix Prefer |
| Instant Success | MCP-only / screenshot-only is not Done |
| Scope smuggle | Full biome matrix, ADC art pass, UI polish, chargen/seats/tricam, second stamp class |

## 7. Out of scope

- Full biome matrix / multi-stamp catalog
- ADC art pass / TAC material polish (Terrain3D already vendored — module-only Prefer)
- UI polish / GUI chrome
- PF1 chargen / seats / tricam (remain deferred; superseded chargen brief stays superseded)
- Reopening whole UX-1 cell scope beyond Terrain3D feed
- Nested dungeon grids, settlement path-connect
- Investor demo / archived `horizon_demo_investor`
- `dev/FpsSanity*.tscn` as Success proof

## 8. Receipt (required on Half-B completion)

1. `ask_id` / `slice_id`
2. Matrix Prefer quotes — Dual-grid + Terrain3D height authority
3. Terrain3D host path under WorldgenCraft / DualGridCraftHost (ClassDB Prefer armed)
4. `stamp_oasis_desert` → Terrain3D data push proof (receipt + operator F5)
5. Sparky consumer-only over Terrain3D mesh (not graybox-only)
6. No chargen/UI polish smuggle; module-only lane unless presentation `project.godot` required
7. `claim_class: staging` · `factory_greenlit: true`
8. Operator attest or explicit debt

## Related

- [[alpha0_worldgen_dualgrid_sparky_r1]] · [[alpha_architecture_half_b]] · [[Half-B-Weld-Brief-Template]] · [[Ask-Fidelity-Exemplars]] · [[COHESIVE-VISION-ART-DIRECTION]] · [[FEEDSTOCK-SHAPE]] · [[Godot-Implementation-Decision-Matrix]]
