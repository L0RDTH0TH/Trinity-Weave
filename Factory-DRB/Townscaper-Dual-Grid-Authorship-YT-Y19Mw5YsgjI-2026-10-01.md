---
title: Townscaper dual-grid authorship — canonical YT (worldgen step one)
created: 2026-10-01
updated: 2026-10-01
project-id: genesis-mythos-master
para-type: Resource
status: active
claim_class: staging
source_kind: youtube
source_url: https://www.youtube.com/watch?v=Y19Mw5YsgjI
source_title: How One Guy FIXED Procedural Generation
source_channel: Game Dev Buddies
operator_locked: 2026-10-01
tags:
  - townscaper
  - dual-grid
  - worldgen
  - step-1-authorship
  - hot-wheels-vs-terrain3d
---

# Townscaper dual-grid authorship — canonical YT (worldgen step one)

## Citation (first-class)

| Field | Value |
|-------|--------|
| **URL** | https://www.youtube.com/watch?v=Y19Mw5YsgjI |
| **Title** | How One Guy FIXED Procedural Generation |
| **Channel** | Game Dev Buddies |
| **Locked** | 2026-10-01 (operator) |
| **Role** | Canonical reference for **worldgen step one** — Townscaper authorship / dual-grid **Hot Wheels** layer |

## Operator framing (normative)

Maps how Townscaper achieves its goals; this is the **model for our world generation step one**; where Dwarf Fortress inspirations spring forth.

Pattern extract only — not a Townscaper clone; not Terrain3D.

## Hot Wheels vs real car (separation law)

| Layer | Metaphor | Job |
|-------|----------|-----|
| **Townscaper dual-grid craft** | Hot Wheels track | Tile authorship under craft cam — click-place cell grammar |
| **Terrain3D** | Real car / road | Consumer mesh/height world **fed by** craft intent |

- Craft cam = **tile authorship only**
- **No** camera recenter on place
- **No** deforming the craft grid into terrain
- Townscaper model **FEEDS** Terrain3D — they remain **distinct layers**
- **Do not** blend craft tiles with Terrain3D deformation **in craft view**

Refuse Prefer / Half-B that collapses these layers in craft authorship → `inspiration_shape_miss` / layer blend.

## TL;DR — technique points (dual-grid tile authorship)

**Normative craft grammar (GridMap terms):** [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] — Half-B must load that note; do not treat this TL;DR alone as enough.

Fetched via full video transcript + public summaries. Relevant to our step-one craft layer:

1. **Dual grid** — offset copy of the main grid by half a cell; each main-grid point sits at the center of a dual-grid cell.
2. **Corner typing** — dual-grid tiles encode land/water (or type) **per corner**, not whole-cell only; convex and concave corners both round cleanly inside the tile.
3. **Fewer meshes** — corner combinations collapse (with rotation/mirror) to a small set of distinct tile models (~6 vs ~15 whole-tile variants in the video’s framing).
4. **Place → update four** — on click, change the dual-grid **point** type, then refresh the **four** dual quads connected to that point.
5. **Authorship cam** — pieces placed by aiming at the grid (ray to grid under mouse); craft remains grid/tile authorship, not freeform terrain sculpt.
6. **Organic extras (later seasoning)** — irregular/relaxed grids, multi-tile neighbor-matched pieces, handcrafted variants, WFC — DF-shaped depth can spring from this authorship foundation; not required for craft-core lock.

## Cross-links

- **Grammar (normative):** [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]
- **Primary pattern card:** [[dual-grid-nested-placetile-world-authorship]] (supersedes [[townscaper-click-add-world-element]], 2026-10-02)
- Cohesive vision: [[COHESIVE-VISION-ART-DIRECTION]]
- Active series: [[alpha0_townscaper_tutorial_r1]] — step 1 WELD [[alpha0_townscaper_tutorial_s1_occupancy_r1]] (await F5); steps 2–6 draft — hex-19 scaffold ≠ product lattice
- Scrapped this round: [[alpha0_worldgen_dualgrid_sparky_r1]] · [[alpha0_worldgen_terrain3d_feed_r3]] (Terrain3D deferred later); visual + craft_core Prefer altitudes failed_altitude/metrics_only
