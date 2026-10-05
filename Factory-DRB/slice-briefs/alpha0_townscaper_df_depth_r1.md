---
title: Slice brief — alpha0_townscaper_df_depth_r1
slice_id: alpha0_townscaper_df_depth_r1
ask_id: alpha0_townscaper_df_depth
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-01
updated: 2026-10-01
claim_class: staging
factory_greenlit: false
status: depth_frozen_until_tutorial_ladder
status: draft_ready
template: Half-B-Weld-Brief-Template
depends_on: alpha0_townscaper_craft_visual_r1
next_in_chain: null
launch_word: WELD
---

# Slice brief — `alpha0_townscaper_df_depth_r1`

Filled from [[Half-B-Weld-Brief-Template]]. **Fill before Half-B code.** Umbrella: [[alpha_architecture_half_b]]. Lock: [[FEEDSTOCK-SHAPE]]. Cohesive cite: [[COHESIVE-VISION-ART-DIRECTION]].

**Eat order 3/3 — DF-depth authorship (bounded).** Richer cell types, stacking, adjacency, stamps as **tile** operations. Seasoning aspiration: Townscaper-inspired builder toward DF levels of detail — **not** this slice’s Success bar. Still **Hot Wheels only; no Terrain3D**. Prerequisites: [[alpha0_townscaper_craft_core_r1]], [[alpha0_townscaper_craft_visual_r1]]. Terrain3D feed = **separate future ticket** after this F5-greens.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_townscaper_df_depth` |
| `slice_id` | `alpha0_townscaper_df_depth_r1` |
| Scope | Bounded craft-depth step only: fixed cell palette + one-level stack + one adjacency rule + one named tile stamp. DF-detail is aspiration/seasoning, not Success for this slice. Hot Wheels only; no Terrain3D. |
| `claim_class` | `staging` |
| `factory_greenlit` | `false` until operator greenlights |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Worldgen entry scene | `res://scenes/WorldgenCraft.tscn` — authorship deepen |
| Mode | update craft data model + rules + stamps (tile space only) |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| Townscaper YT / card / grammar | Authorship foundation — [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] · [[townscaper-click-add-world-element]] · [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] |
| DF seasoning | Living-detail / deep world **aspiration** — [[FEEDSTOCK-SHAPE]] (possible ≠ boil-the-ocean months); this slice ships a **fixed** depth step only |
| Cohesive vision | Craft remains Hot Wheels feedstock for a later real car — [[COHESIVE-VISION-ART-DIRECTION]] |
| Prior tickets | Keep core grammar + visual language — do not regress |

### Hard law (this slice)

- All depth lands as craft tile / cell authorship only
- No Terrain3D, no sparky open-world generation, no height-authority blend into craft view
- Stamps = tile operations only (paint cell sets / stacks), never Terrain3D `set_height`
- No cam yank / mouse-aim regression
- Host law: [[Prefer-Authorship-Host-Law]]
- **Ship only the four capabilities below.** Extra systems (pathing, labor, multi-year worldgen, full fortress sim, empire AI) = refuse `boil_the_ocean_df`

### Bounded depth step (staging house — exhaustive)

This slice Success = **exactly** these four, nothing more:

1. **Cell types (fixed palette)**  
   Empty · Ground · Wall · Water · Oasis  
   (Do not invent further types in this ticket.)

2. **Stacking**  
   One vertical stack level above ground (wall-on-ground or equivalent). No multi-story fortress sim.

3. **Adjacency rule (one)**  
   On place: if a Ground cell is fully enclosed by Wall cells on the four cardinal neighbors, auto-mark / auto-fill as interior (or equivalent single readable neighbor rule). One rule only.

4. **Named stamp (tile-space only)**  
   `stamp_oasis_cells` — paints a small desert/ground ring + one Oasis cell at center. Tile ops only; no height writes.

Mission list above is the **entire** done_when surface for depth. “Toward DF levels of detail” remains seasoning/aspiration for later tickets, not a Success bar here.

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [x] [[COHESIVE-VISION-ART-DIRECTION]]
- [x] [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]]
- [x] [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]
- [x] [[alpha0_townscaper_craft_core_r1]] + [[alpha0_townscaper_craft_visual_r1]]
- [x] Host-weld factory pilots
- [x] [[Godot-Implementation-Decision-Matrix]] — dual-grid craft / GridMap (Terrain3D Prefer out)
- [ ] Terrain3D feed Prefer — **future ticket after this**

## 4. End flavor

> Crafting is one clear step deeper: five readable cell types, one stack level, one neighbor rule, one tile stamp — still Hot Wheels feedstock, not a fortress sim and not the open world.

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | F5: the fixed five-type palette is placeable; one-level stack works; the single adjacency rule is visible in play; `stamp_oasis_cells` lands as tiles only; core grammar + visual language intact; zero Terrain3D in craft path. No other depth systems required or claimed. |
| Operator attest | F5 only — ban `verify_mcp_only` |
| `claim_class` | `staging` (full DF fidelity = later `ask_success` bar, not this slice alone) |

## 6. Refuse

| Code | Note |
|------|------|
| `boil_the_ocean_df` | Any system beyond the four capabilities (pathing empires, labor, multi-year worldgen, full fortress sim, extra cell types, multi-story stacks) claimed as Success for this slice |
| `stamp_as_terrain_height` | Stamp writes Terrain3D / height instead of tiles |
| `craft_terrain_blend` / `terrain3d_in_scope` | Terrain3D or height authority in craft |
| `grammar_regress` / `visual_regress` | Core or visual tickets broken |
| `inspiration_shape_miss` | Flat clicker with no typed/stack/adjacency/stamp depth |
| `verify_mcp_only` | MCP-as-Success |

## 7. Out of scope

- Terrain3D / sparky open-world Prefer (after this F5 only)
- Full fortress sim, pathing, labor calendars, multi-year worldgen
- Additional cell types beyond the fixed palette
- Multi-level stacks beyond one above ground
- Second stamp class
- Chargen / seats / tricam
- Replacing cohesive art direction
