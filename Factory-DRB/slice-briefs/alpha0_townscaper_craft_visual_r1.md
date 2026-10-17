---
title: Slice brief — alpha0_townscaper_craft_visual_r1
slice_id: alpha0_townscaper_craft_visual_r1
ask_id: alpha0_townscaper_craft_visual
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-01
updated: 2026-10-02
claim_class: staging
factory_greenlit: false
status: failed_altitude_metrics_only
template: Half-B-Weld-Brief-Template
depends_on: alpha0_townscaper_craft_core_r1
next_in_chain: null
launch_word: WELD
armed_packet: null
failed_altitude_receipt: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_townscaper_craft_visual_altitude_failed_2026-10-02.md
superseded_by_series: alpha0_townscaper_tutorial_r1
---

# Slice brief — `alpha0_townscaper_craft_visual_r1`

**FAILED ALTITUDE (metrics-only).** Do not Prefer again for art re-skin. Receipt: [[alpha0_townscaper_craft_visual_altitude_failed_2026-10-02]]. Active: [[alpha0_townscaper_tutorial_s1_occupancy_r1]].

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_townscaper_craft_visual` |
| `slice_id` | `alpha0_townscaper_craft_visual_r1` |
| Scope | Re-skin existing dual MeshLibrary variants with stylized low-poly meshes/materials; craft remains Hot Wheels authorship; **preserve picking / collision / mouse-aim** |
| `claim_class` | `staging` |
| `factory_greenlit` | `true` (operator GREENLIGHT 2026-10-02) |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Worldgen entry scene | `res://scenes/WorldgenCraft.tscn` — visual update only |
| Mode | update craft presentation / MeshLibrary / materials; schedule **asset/techart** lanes as drops under this ticket if real ADC/TAC needed — **do not expand into DF depth** |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| 3D bar | Astroneer stylized low poly — [[Visual-Factory-Direction-Stylized-Low-Poly]] |
| Cohesive vision | Craft look must match Genesis Mythos art direction — [[COHESIVE-VISION-ART-DIRECTION]] |
| Step-1 law | Visuals dress Hot Wheels; they do **not** become Terrain3D — [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] |
| Grammar | [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] + [[alpha0_townscaper_craft_core_r1]] — **do not regress** |

Seasoning: DF-depth cell variety waits for ticket 3. This ticket ships a **small craft tile set only — no full biome atlas.**

### Hard law (this slice)

- Craft stays **tile authorship** — no cam yank regression; mouse-aim place/remove preserved
- **No Terrain3D** host, height feed, or craft-view terrain deform
- Prefer MeshLibrary / material / mesh swaps on the **existing** craft host — **do not carelessly replace the whole craft host** (breaks picking, collision, mouse-aim)
- **Re-skin the existing dual MeshLibrary variants (Full / Corner / Edge / Diagonal / InverseCorner + Empty).**
  Do not collapse to a single cube mesh for all masks.
  Do not replace the logic-point → corner-bitmask path with a raw-cell-only visual authority.
- Palette cap: **small craft tile set only — no full biome atlas**
- Visual success = operator F5 “I’m not looking at graybox anymore” for placed craft tiles
- **Mandatory regression F5** after visual change: place + remove still work under mouse; dual-grid neighbor variants still distinct; no cam yank — **not optional**
- Prefer authorship host law still applies: [[Prefer-Authorship-Host-Law]]
- Receipt **must** cite [[Visual-Factory-Direction-Stylized-Low-Poly]] + proof dual variant MeshLibrary item ids still differ after re-skin
- If ADC/TAC needed: schedule as drops under this ticket only — **do not expand into DF depth**

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [x] [[COHESIVE-VISION-ART-DIRECTION]]
- [x] [[Visual-Factory-Direction-Stylized-Low-Poly]]
- [x] [[alpha0_townscaper_craft_core_r1]] (grammar prerequisite — Prefer landed)
- [x] [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]
- [x] Host-weld factory pilots
- [x] [[Godot-Implementation-Decision-Matrix]] — presentation / MeshLibrary rows
- [ ] DF-depth stacking / rich adjacency — [[alpha0_townscaper_df_depth_r1]]
- [ ] Terrain3D feed — deferred

## 4. End flavor

> Placing a tile looks like a stylized low-poly craft toy, not a developer cube — still clearly the Hot Wheels layer, not the open world; place/remove still aim under the cursor; Full/Corner/Edge/Diagonal/InverseCorner remain visually distinct.

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | F5: placed dual-grid tiles read stylized low-poly (not graybox developer cubes); LMB place / RMB remove under mouse still work; no cam yank; dual neighbor variants still distinct; Terrain3D still absent/hard-disabled under craft. |
| Operator attest | F5 only — ban `verify_mcp_only`; visual-only attest without place/remove retest = fail |
| `claim_class` | `staging` |
| Receipt must | Cite Visual-Factory-Direction + prove MeshLibrary variant ids (Full/Corner/Edge/Diagonal/InverseCorner/Empty) still differ after re-skin |

## 6. Refuse

| Code | Note |
|------|------|
| `inspiration_shape_miss` | Looks generic / wrong art bar; or all masks collapsed to one cube |
| `graybox_only_craft` | Still developer cubes as the only craft read |
| `craft_terrain_blend` / `terrain3d_in_scope` | Terrain3D sneaks in |
| `grammar_regress` | Place/remove / cam yank / mouse aim / dual-grid broken after visual swap |
| `raw_cell_only_visual` | Logic-point → corner-bitmask path replaced with raw-cell-only visual authority |
| `host_replace_careless` | Whole craft host rewritten and picking/collision broken |
| `biome_atlas_scope_creep` | Full biome atlas / DF-depth expansion under this ticket |
| `verify_mcp_only` | MCP-as-Success |

## 7. Out of scope

- Terrain3D / sparky worldgen
- Full DF-depth authoring grammar ([[alpha0_townscaper_df_depth_r1]])
- Full biome / atlas art pass beyond small craft tile palette
- Chargen / seats / tricam
- GUI fantasy chrome unless required for craft HUD
