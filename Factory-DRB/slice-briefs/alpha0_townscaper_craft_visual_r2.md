---
title: Slice brief — alpha0_townscaper_craft_visual_r2
slice_id: alpha0_townscaper_craft_visual_r2
ask_id: alpha0_townscaper_craft_visual
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-02
updated: 2026-10-02
claim_class: staging
factory_greenlit: false
status: failed_altitude_metrics_only
template: Half-B-Weld-Brief-Template
depends_on: alpha0_townscaper_craft_core_r1
reworks: alpha0_townscaper_craft_visual_r1
next_in_chain: null
launch_word: WELD
greenlit_at: 2026-10-02T05:10:00Z
operator_resume_at: 2026-10-02T05:27:00Z
refs_path: 1-Projects/genesis-mythos-master/Factory-DRB/references/craft-visual-r2/
adc_exported_at: 2026-10-02T05:48:26Z
armed_packet: null
failed_altitude_receipt: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_townscaper_craft_visual_altitude_failed_2026-10-02.md
superseded_by_series: alpha0_townscaper_tutorial_r1
---

# Slice brief — `alpha0_townscaper_craft_visual_r2`

**FAILED ALTITUDE (metrics-only) — 2026-10-02.** Operator: visually identical / same class despite technical dual differences. Do **not** Prefer again for art re-skin. Receipt: [[alpha0_townscaper_craft_visual_altitude_failed_2026-10-02]]. Active path: [[alpha0_townscaper_tutorial_r1]] → [[alpha0_townscaper_tutorial_s1_occupancy_r1]].

Filled from [[Half-B-Weld-Brief-Template]]. Historical rework of r1. Umbrella: [[alpha_architecture_half_b]].

**Was eat order 2b/3 — Real craft meshes.** Archived. Depth stays frozen until tutorial ladder clears.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_townscaper_craft_visual` |
| `slice_id` | `alpha0_townscaper_craft_visual_r2` |
| Scope | Author **real** stylized low-poly meshes + `MeshLibrary` for Empty, Full, Corner, Edge, Diagonal, InverseCorner; `DualGridCraftHost` loads asset library — procedural `Make*Mesh` **fail-visible fallback only**, not Success |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` (operator GREENLIGHT asset factory 2026-10-02) |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Worldgen entry scene | `res://scenes/WorldgenCraft.tscn` |
| Mode | **asset** (+ **techart** if needed) + **module** lanes — Blender MCP author/export; Godot MCP bind `MeshLibrary`; chrome cleanup |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| 3D bar | Astroneer stylized low poly — [[Visual-Factory-Direction-Stylized-Low-Poly]] |
| Cohesive vision | Restrained palette, soft bevels, intentional silhouette — [[COHESIVE-VISION-ART-DIRECTION]] |
| Step-1 law | Hot Wheels tile authorship — [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] |
| Grammar | [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] + [[alpha0_townscaper_craft_core_r1]] |

### Hard law (this slice)

- **NOT Success:** saturated debug candy / procedural-only colored `ArrayMesh` as the shipped craft read (`procedural_only_as_success` refuse)
- **Success:** Blender-authored (or equivalent ADC) meshes under `res://assets/craft/dual_grid/` bound into `MeshLibrary`; distinct variant ids 0–5 preserved
- Craft stays logic-point dual grid; LMB/RMB under mouse; no cam yank; Terrain3D hard-disabled under craft
- **Chrome cleanup:** HUD/PDC must not advertise sparky / Terrain3D / raise-as-height as active craft affordances
- Mandatory regression **F5** in `done_when`
- Schedule **asset** + **module** (+ **techart** if materials need TAC pass) — not bootstrap stubs

### Operator refs (resume 2026-10-02)

Filed under [[references/craft-visual-r2/README|Factory-DRB/references/craft-visual-r2/]]:

| Ref | Cite as |
|-----|---------|
| `nature-pack-eye-test-isometric.png` | eye-test — soft bevel diorama / mossy stone + sage hills |
| `nature-pack-aerial-silhouette.png` | silhouette — iconic readable forms; soft land/water bevel (pattern only) |
| `model-pack-craft-toys-palette.png` | palette — earth brown / sage / cool gray toy mass |
| `townscaper-screenshot.jpg` | craft density / toy-town / Hot Wheels authorship eye-test — clustered readable tiles, shared foundation language |

**Extract only** — not Townscaper sea-grid clone; not full biome atlas; not lego-spill debug.

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [x] [[COHESIVE-VISION-ART-DIRECTION]]
- [x] [[Visual-Factory-Direction-Stylized-Low-Poly]]
- [x] [[alpha0_townscaper_craft_core_r1]] (Prefer landed)
- [x] [[alpha0_townscaper_craft_visual_r1]] (receipt rework — operator F5 fail)
- [x] Host-weld factory pilots
- [ ] [[alpha0_townscaper_df_depth_r1]] — **blocked until this ticket F5 green**

## 4. End flavor

> Placed tiles read as cohesive stylized low-poly craft toys (soft bevel, earth-tone restraint) — not rainbow debug primitives. Place/remove still aim under the cursor; neighbor variants still read differently at a glance.

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | **F5** `WorldgenCraft`: placed dual-grid tiles show **asset-bound** stylized low-poly meshes (operator: not debug candy); LMB place / RMB remove under mouse; no cam yank; Full/Corner/Edge/Diagonal/InverseCorner/Empty still distinct; Terrain3D absent/hard-disabled; HUD chrome has no sparky/Terrain3D/raise-as-height as active craft hints. |
| Operator attest | F5 only — ban `verify_mcp_only` |
| Receipt must | Cite Visual-Factory-Direction + list `res://assets/craft/dual_grid/*` paths + prove MeshLibrary variant ids still differ + module loads asset library (not procedural-only proof pass) |

## 6. Refuse

| Code | Note |
|------|------|
| `graybox_only_craft` | Developer cubes / flat debug only |
| `procedural_only_as_success` | Runtime `Make*Mesh` ArrayMesh without asset MeshLibrary bind |
| `inspiration_shape_miss` | Saturated debug candy OR collapsed masks |
| `grammar_regress` | Place/remove / cam yank / mouse aim broken |
| `terrain3d_in_scope` | Terrain3D active under craft |
| `biome_atlas_scope_creep` | Full biome atlas under this ticket |
| `verify_mcp_only` | MCP-as-Success |

## 7. Out of scope

- [[alpha0_townscaper_df_depth_r1]] until visual F5 green
- Terrain3D / sparky handoff
- Full biome atlas
- Chargen / seats / tricam
