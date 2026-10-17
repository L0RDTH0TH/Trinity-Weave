---
title: Slice brief — alpha0_townscaper_craft_core_r1
slice_id: alpha0_townscaper_craft_core_r1
ask_id: alpha0_townscaper_craft_core
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-01
updated: 2026-10-01
claim_class: staging
factory_greenlit: false
status: failed_altitude_metrics_only
template: Half-B-Weld-Brief-Template
supersedes: alpha0_worldgen_terrain3d_feed_r3
next_in_chain: null
launch_word: WELD
greenlit_at: 2026-10-02T02:30:00Z
prefer_landed_at: 2026-10-02T03:05:00Z
prefer_land_receipt: factory-overnigh-module-fe92b0
sp_review: pass
armed_packet: null
failed_altitude_receipt: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_townscaper_craft_visual_altitude_failed_2026-10-02.md
superseded_by_series: alpha0_townscaper_tutorial_r1
reset_note: operator_2026-10-02__do_not_audit_as_tutorial_s1_success
---

# Slice brief — `alpha0_townscaper_craft_core_r1`

**FAILED ALTITUDE / metrics_only (reset 2026-10-02).** Dual MeshLibrary / connector Success claims stripped from active ladder. Files kept for history. Active step 1: [[alpha0_townscaper_tutorial_s1_occupancy_r1]]. Receipt: [[alpha0_townscaper_craft_visual_altitude_failed_2026-10-02]].

Filled from [[Half-B-Weld-Brief-Template]]. Historical Prefer. Umbrella: [[alpha_architecture_half_b]].

**Was eat order 1/3 — Townscaper craft core.** Archived as ladder Success. Terrain3D still deferred.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_townscaper_craft_core` |
| `slice_id` | `alpha0_townscaper_craft_core_r1` |
| Scope | Townscaper-inspired dual-grid craft: LMB/RMB cell commit under mouse (interaction grid); module/visual form neighbor-derived (not raw-cell-only mesh authority); no cam yank / no camera-center aim; authorship layer only; **hard-disable / strip Terrain3D from craft path** ([[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]) |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` (operator GREENLIGHT 2026-10-02) |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Worldgen entry scene | `res://scenes/WorldgenCraft.tscn` — update (craft host only) |
| Mode | update / rewrite craft authorship; **strip or hard-disable Terrain3D from craft path** (Success criterion) |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| **Craft grammar (normative)** | Concrete GridMap/dual-grid rules — [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] |
| Canonical YT step-1 | Townscaper dual-grid authorship — https://www.youtube.com/watch?v=Y19Mw5YsgjI · [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] |
| Pattern card | Click-add / place-painting — [[townscaper-click-add-world-element]] |
| Cohesive vision | Craft = Hot Wheels authorship — [[COHESIVE-VISION-ART-DIRECTION]] |
| Camera | Craft envelope / `vtt_planar_ortho` — [[Camera-Mode-Taxonomy-Live]] — **not** sparky |

Seasoning: DF depth and visual polish are **later tickets**. GUI chrome out of focus.

### Hard law (this slice) — dual-grid rule (minimal, from YT step-1)

- Craft cam = **tile authorship only** (Hot Wheels). Cite: [[Prefer-Authorship-Host-Law]] · grammar card [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]].
- **Interaction grid (player):** LMB on empty cell under **mouse cursor** → place current brush (default Ground); RMB on occupied cell → clear. Cell-committed. No camera-center aim. No cam recenter on place/remove.
- **Dual / module grid (system):** Visual tile form is derived from the interaction cell + its neighbors (even if this slice only ships flat graybox boxes). Do not treat a single GridMap cell as both “the only grid” and “the finished building mesh authority” with no neighbor consideration path.
- **Alpha altitude:** Graybox Mesh/GridMap tiles OK. Full irregular dual (pent/hex → quad dual) and auto arches/stairs are **not** required this slice — only the interaction grammar + a readable path for neighbor-derived form later.
- Pattern extract only — not a Townscaper clone of the organic sea grid.
- **Forbidden on craft path (Success = hard strip/disable, not hope):**
  - Terrain3D host visible, present, or mutating under craft
  - Any height-paint / height-stamp path **callable or armed** from craft phase
  - `Terrain3DAuthority` / Prefer height feed **armed** from craft entry
  - feed-on-sparky / Tab → Terrain3D / sparky worldgen handoff from craft
  - “Code exists but unused” while still callable/armed under craft (nodes enabled, Tab bound, stamps writing heights, etc.)
- LIVE may **retain** Terrain3D addon/files for later tickets — craft entry / craft host **must not call, show, or arm** them this round

### Terrain3D archive posture (this test round)

| Keep | Do not use |
|------|------------|
| Addon / scripts on disk for later Prefer | Craft F5 path, Tab feed-on-sparky, height stamps from craft |
| Future ticket after DF-depth F5 | Any armed Terrain3DAuthority under WorldgenCraft craft phase |

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [x] [[COHESIVE-VISION-ART-DIRECTION]]
- [x] Host-weld: `implementation_factory_loop` + `product_factory_pipeline`
- [x] [[Godot-Implementation-Decision-Matrix]] — Dual-grid / GridMap craft rows (Terrain3D Prefer **out of scope this round**)
- [x] [[INSPIRATION-HALF-B-SHAPE]] + [[townscaper-click-add-world-element]]
- [x] [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] — **required before code**
- [x] [[Camera-Mode-Taxonomy-Live]]
- [ ] [[Visual-Factory-Direction-Stylized-Low-Poly]] — deferred to [[alpha0_townscaper_craft_visual_r1]]
- [ ] Terrain3D / sparky feed — deferred (future ticket after DF-depth)

## 4. End flavor

> Clicking the craft plane feels like Townscaper step-1: LMB places / RMB clears the cell under the mouse; the camera stays put; graybox tiles read as cell-committed authorship with a neighbor-derived module path (not raw-cell-only mesh authority); Terrain3D is nowhere in craft.

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | F5: LMB places under mouse cursor, RMB removes; no cam yank; no camera-center aim; dual-grid interaction grammar readable (cell commit on interaction grid; module/visual path not identical to raw cell only); Terrain3D host absent or hard-disabled under craft; no height-paint/feed path callable from craft phase. Armed Authority, Tab/feed-on-sparky handoff, or callable stamp = fail. “Code exists but unused” fails if still callable/armed under craft. Disk retention of Terrain3D files alone ≠ fail. |
| Operator attest | F5 only — ban `verify_mcp_only` |
| `claim_class` | `staging` |

## 6. Refuse

| Code | Note |
|------|------|
| `inspiration_shape_miss` | Not Townscaper click-add / dual-grid grammar (e.g. camera-center aim; raw GridMap cell treated as sole finished mesh authority with no neighbor-derived path) |
| `craft_cam_recenter_on_place` | Camera follows new tile |
| `craft_terrain_blend` | Any Terrain3D / height deform in craft |
| `terrain3d_in_scope` | Terrain3D touched / armed / Tab-fed from craft this ticket |
| `terrain3d_leak_f5` | “Unused” code still reachable under F5 (enabled nodes, bindings, stamps) |
| `camera_center_aim` | Place uses camera center not mouse |
| `verify_mcp_only` | MCP-as-Success |

## 7. Out of scope

- Terrain3D / sparky open-world feed (**later** ticket — archive Prefer **results usage** for this round)
- Stylized materials / non-graybox art ([[alpha0_townscaper_craft_visual_r1]])
- DF-depth cell types, stacking, rich adjacency ([[alpha0_townscaper_df_depth_r1]])
- Chargen / seats / tricam
- Horizon investor demo Success chase
- Irregular Stålberg grids / multi-tile WFC pieces (grammar note marks as later)
