---
title: Slice brief — alpha0_worldgen_dualgrid_sparky_r1
slice_id: alpha0_worldgen_dualgrid_sparky_r1
ask_id: alpha0_worldgen_dualgrid_sparky
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-01
updated: 2026-10-01
claim_class: staging
factory_greenlit: true
status: superseded_scrapped_chain
template: Half-B-Weld-Brief-Template
supersedes: alpha0_chargen_seats_tricam_r1
superseded_by: alpha0_townscaper_craft_core_r1
armed_packet: alpha0_worldgen_dualgrid_sparky_r1.armed.yaml
launch_word: WELD
---

> **Trinity publish copy.** Canonical Factory-DRB path: `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_worldgen_dualgrid_sparky_r1.md`. **SCRAPPED for next craft round** — active chain is [[alpha0_townscaper_craft_core_r1]] → visual → DF-depth. Terrain3D deferred later.

# Slice brief — `alpha0_worldgen_dualgrid_sparky_r1`

Filled from [[Half-B-Weld-Brief-Template]]. **Fill before Half-B code.** Umbrella: [[alpha_architecture_half_b]]. Lock: [[FEEDSTOCK-SHAPE]]. Cohesive cite: [[COHESIVE-VISION-ART-DIRECTION]].

**Active first Half-B weld.** Supersedes [[alpha0_chargen_seats_tricam_r1]] (chargen / seats / tricam polish deferred).

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_worldgen_dualgrid_sparky` |
| `slice_id` | `alpha0_worldgen_dualgrid_sparky_r1` |
| Scope | Open-world 3D dual-grid procedural craft (Townscaper-shaped pattern) under craft cam; **then** inspect/fly with functional `god_mode_sparky` once the 3D open world exists |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Worldgen entry scene | `res://scenes/WorldgenCraft.tscn` — **create-or-update** target for this weld (no Worldgen scene on LIVE slug yet) |
| Mode | generate / update as needed on LIVE slug |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| Townscaper (pattern extract) | **Step-1 authorship model** — click-add / dual-grid place-painting — [[townscaper-click-add-world-element]] · canonical YT [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] (https://www.youtube.com/watch?v=Y19Mw5YsgjI) |
| Cohesive vision | Dual-grid open-world craft + sparky posture + stylized low poly — [[COHESIVE-VISION-ART-DIRECTION]] |
| 3D bar (when meshes show) | Astroneer stylized low poly — [[Visual-Factory-Direction-Stylized-Low-Poly]] |
| Camera | **Two phases (do not collapse):** (1) Townscaper craft / dual-grid authorship — prefer `vtt_planar_ortho` or craft envelope per [[Camera-Mode-Taxonomy-Live]] (planar locked, slight angle, 180° about center) — **not** sparky; (2) **after** the 3D open world exists from that model — `god_mode_sparky` for inspect/fly mastery |
| DF (seasoning) | Living-detail / deep worldgen **possible ≠ required** — [[FEEDSTOCK-SHAPE]] / stub-df peers |

Seasoning: rest of Inspiration INDEX when not in focus. GUI chrome **out of focus** unless this ticket actually touches menus.

### Step-1 law — Hot Wheels vs Terrain3D (operator locked 2026-10-01)

- Craft cam = **tile authorship only** — **no** camera recenter on place; **no** deforming craft grid into terrain
- Dual-grid Townscaper (**Hot Wheels**) **FEEDS** Terrain3D (**real car**) — distinct layers
- **Do not** blend craft tiles with Terrain3D deformation in craft view
- Cite: [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]]

### Craft-cam control mapping (normative)

Craft phase under `vtt_planar_ortho` / craft envelope: **planar lock**; orbit about focus **≤180°**; **WASD** (or equivalent) **pan on the plane**; **paint/raise on primary action**. **Sparky bindings off until handoff.** Refuse: craft phase using sparky free soar → `inspiration_shape_miss` / camera conflation. Binding detail: [[Camera-Mode-Taxonomy-Live]].

### Click grammar (normative)

Under craft cam (`vtt_planar_ortho` / craft envelope): primary pointer on a **cell** + click/drag **paints or raises that cell** (type change and/or height). Authorship is **cell-committed** under the locked craft camera — **not** free-orbit authorship, **not** floating cursor without cell commit. Refuse → `inspiration_shape_miss` / camera conflation.

### Canonical stamp (must-land)

Named stamp **`stamp_oasis_desert`**: paints a desert cell region + one oasis marker under craft cam. Oasis/lumber phrasing elsewhere remains **illustrative only**; acceptance **requires this named stamp**. A second stamp class is a **later ticket**.

### Dual-grid Godot representation (normative)

Half-B must **quote** the [[Godot-Implementation-Decision-Matrix]] row **Dual-grid world craft**: Prefer **Terrain3D** (existing Prefer terrain) as world/height authority **+** **GridMap** (or equivalent stock grid) as craft cell overlay — **one** craft cell data authority; **Never** a second parallel terrain/physics authority or custom voxel engine for this ticket. Do not invent a third stack.

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [x] [[COHESIVE-VISION-ART-DIRECTION]]
- [x] Host-weld: `implementation_factory_loop` + `product_factory_pipeline` (trialing; `factory_greenlit: true`; overnight conductor word-gated / non-auto)
- [x] [[Godot-Implementation-Decision-Matrix]] — **must quote** Prefer/Never for **Dual-grid world craft** (+ terrain/cam rows touched); **no parallel terrain engine**
- [ ] [[ENGINE-COMPILE-PACK-stock_godot_fps]] only if player/anchored move-look is touched (not primary for this ticket)
- [x] [[INSPIRATION-HALF-B-SHAPE]] + [[townscaper-click-add-world-element]]
- [x] [[Camera-Mode-Taxonomy-Live]] — craft cam for authorship (`vtt_planar_ortho` / craft envelope) + craft-phase control mapping; `god_mode_sparky` for post-world inspect/fly (not primary for whole weld)
- [x] [[Visual-Factory-Direction-Stylized-Low-Poly]] — load when meshes/env land (bar cited; apply on mesh land)
- [ ] [[GUI-Chrome-Direction-Fantasy-UI]] **only if** menus/panels land in this ticket

## 4. End flavor

Townscaper-esque **3D dual-grid** open-world procedural craft: start blank or with initial gen options; fill/edit tiles via **cell-committed** click/drag paint-or-raise under a **Townscaper-appropriate craft camera** (`vtt_planar_ortho` / craft envelope — planar lock; orbit about focus ≤180°; WASD plane pan; paint/raise on primary; sparky bindings off). Land named stamp **`stamp_oasis_desert`** (desert cell region + one oasis marker). **After** that model yields a 3D open world, hand off to working **`god_mode_sparky`** for inspect/fly mastery — sparky is **not** the craft-authorship cam and **not** primary for the entire weld. When meshes appear, they read **stylized low poly** (Astroneer bar). Pattern extract — not a Townscaper clone. DF-deep worldgen remains possible, not mandatory for this slice.

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | Operator can author/edit open-world dual-grid place under craft cam (`vtt_planar_ortho` / craft envelope) with **cell-committed** primary click/drag paint-or-raise (type and/or height); craft-phase controls = planar lock, orbit about focus ≤180°, WASD (or equiv) plane pan, paint/raise on primary, **sparky bindings off until handoff**; land named stamp **`stamp_oasis_desert`** (desert cell region + one oasis marker); blank start and/or initial gen options; Matrix **Dual-grid world craft** Prefer/Never quoted (Terrain3D height authority + GridMap craft overlay; no second terrain/physics/voxel authority); **then**, once the 3D open world exists from that model, inspect/fly with functional `god_mode_sparky`; meshes (if any) land on stylized low-poly bar; entry via `res://scenes/WorldgenCraft.tscn` (create-or-update) |
| Operator attest | F5 / play for craft-cam authorship path **and** post-world sparky inspect/fly handoff; **ban** `verify_mcp_only` |
| `claim_class` | `staging` — not `ask_success`; factory greenlit true |

## 6. Refuse

Matrix **Never** + [[Ask-Fidelity-Exemplars]] + factory rejects:

`inspiration_shape_miss` · `fidelity_miss` · `engine_pattern_miss` · `gui_input_steal` · `verify_mcp_only` · `parallel_terrain_engine`

| Code | Note |
|------|------|
| `inspiration_shape_miss` | Generic flat terrain / no Townscaper-shaped craft feel; free-orbit authorship or floating cursor without **cell commit**; craft phase using sparky free soar when dual-grid craft is claimed; **blending craft tiles with Terrain3D deformation in craft view**; camera recenter on place / deforming craft grid into terrain |
| `parallel_terrain_engine` | Do not invent a second terrain/physics authority or custom voxel engine beside Decision Matrix **Dual-grid world craft** Prefer path |
| Camera conflation | Ortho ≠ sparky ≠ anchored — craft authorship uses craft cam (`vtt_planar_ortho` / craft envelope) with craft-phase mapping; `god_mode_sparky` is **post-world** inspect/fly only. Do **not** call sparky primary for the whole weld or use sparky as the Townscaper craft cam |
| Layer blend | Prefer that collapses Hot Wheels craft into Terrain3D sculpt under craft cam — refuse; Terrain3D is fed consumer, not craft-view authorship medium |
| Instant Success | MCP-only or screenshot-only is not Done |
| Scope smuggle | Nested dungeon grids, settlement path-connect, PF1 chargen, full tricam polish, extending superseded chargen/tricam chrome as Success for *this* slice |

## 7. Out of scope

- Nested dungeon / structure grids (later — same tooling vision, not this ticket)
- Settlement path-connect (later)
- PF1 chargen / player-seat authorship
- Full tricam polish (all three cams as Success bar for this slice)
- Extending superseded [[alpha0_chargen_seats_tricam_r1]] chargen / seats / tricam chrome
- Investor demo / archived `horizon_demo_investor` Success
- Paizo prose dump
- GUI chrome work unless menus are actually touched here
- Months of DF worldgen as mandatory (possible ≠ required)
- Second stamp class beyond **`stamp_oasis_desert`** (later ticket)
- `dev/FpsSanity*.tscn` as Success proof — **FpsSanity remains diagnostic only**

## 8. Receipt (required on Half-B completion)

1. `ask_id` / `slice_id`
2. Focus inspiration + cohesive vision cites landed (Townscaper card + [[COHESIVE-VISION-ART-DIRECTION]])
3. Matrix Prefer quotes for touched rows — **must include Dual-grid world craft** (Terrain3D + GridMap craft overlay; no parallel terrain/physics/voxel)
4. Craft cam verified for dual-grid authorship (cell-committed paint/raise + craft-phase mapping; sparky bindings off in craft); `god_mode_sparky` verified for post-world inspect/fly handoff
5. Named stamp **`stamp_oasis_desert`** landed under craft cam
6. Worldgen entry `res://scenes/WorldgenCraft.tscn` create-or-update; no chargen/tricam chrome extension; FpsSanity not used as Done proof
7. 3D bar cite if meshes landed
8. `claim_class: staging` · `factory_greenlit: true`
9. Operator attest or explicit debt

## Related

- [[alpha_architecture_half_b]] · [[Half-B-Alpha-Mode]] · [[Half-B-Weld-Brief-Template]] · [[Ask-Fidelity-Exemplars]] · [[COHESIVE-VISION-ART-DIRECTION]] · [[FEEDSTOCK-SHAPE]] · [[INSPIRATION-HALF-B-SHAPE]] · [[townscaper-click-add-world-element]] · [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] · [[Camera-Mode-Taxonomy-Live]] · [[Godot-Implementation-Decision-Matrix]]
