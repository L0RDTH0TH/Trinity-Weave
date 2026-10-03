---
title: Townscaper dual-grid craft grammar (GridMap / Half-B)
created: 2026-10-01
updated: 2026-10-02
project-id: genesis-mythos-master
para-type: Resource
status: active
claim_class: staging
source_kind: youtube_extract
source_url: https://www.youtube.com/watch?v=Y19Mw5YsgjI
source_title: How One Guy FIXED Procedural Generation
source_channel: Game Dev Buddies
operator_locked: 2026-10-01
topology_law_locked: 2026-10-02
normative_for: alpha0_townscaper_tutorial_r1
tags:
  - townscaper
  - dual-grid
  - craft-grammar
  - gridmap
  - half-b
  - topology
---

# Townscaper dual-grid craft grammar (GridMap / Half-B)

**Normative for** tutorial series [[alpha0_townscaper_tutorial_r1]] (step 1 occupancy → dual later). Historical Prefer [[alpha0_townscaper_craft_core_r1]] = failed_altitude. Citation parent: [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]]. Pattern card (superseded draft): [[townscaper-click-add-world-element]] → primary [[dual-grid-nested-placetile-world-authorship]]. Topology host law: [[Grid-Topology-Host-Law]].

Extracted from the **entire** locked YT (Game Dev Buddies — *How One Guy FIXED Procedural Generation*, Oskar Stålberg / Townscaper lineage) plus public dual-grid writeups. Half-B must implement this grammar — **not** “click places a box,” and **not** “N floating points = grid.”

## Refuse substitute

| Code | Meaning |
|------|---------|
| `points_as_grid` | Markers at coordinates with **no edges/faces** claimed as grid Success |
| `count_equals_topology` | “N points present” ≠ lattice graph with cells |
| `inspiration_shape_miss` / grammar miss | Single GridMap cell gets a box mesh on click with **no** corner-typed dual update |
| Cam yank | Camera recenters / follows placed piece |
| Terrain blend | Terrain3D / height deform on craft path |

### Grid = graph (s1 before dual)

When the ticket says “hexagonal grid … 19 points,” Success is a **hex lattice graph**:

1. **Vertices** — the 19 points (or scaffold count)  
2. **Edges** — lines between neighbors so the hex lattice is readable  
3. **Faces / cells** — regions you paint/ghost onto (flat plate OK)  

Ghost snaps to a **cell** (or the vertex set that defines it), not a lone dot in empty space. Until edges (and preferably faces) are visible → **refuse `points_as_grid`**.

---

## Operational meaning: dual-grid

| Layer | Role in Godot/craft terms |
|-------|---------------------------|
| **Logic / authorship points** | Discrete points the player edits (land vs water / typed). Think: vertex / corner authority — **not** “whole cell = one mesh forever.” |
| **Visual dual cells (GridMap / MeshLibrary)** | Quads **offset by half a cell** from the logic lattice. Each visual cell sits so a logic point is at its **center**; each visual cell’s **four corners** sample logic types. |
| **Why dual** | Whole-tile land/water needs ~15 distinct neighbor meshes (after rotation/mirror). Corner-typed dual tiles collapse to **~6** distinct meshes and round **both** convex and concave corners inside the tile. |

**Operational one-liner:** Player edits a **point**; visuals refresh the **four dual quads** that share that point.

---

## Minimal cell rule set (core Success)

1. **Constraint:** Authorship is grid-bound. Ray from craft cam → hit craft plane → snap to lattice (not freeform sculpt).
2. **Aim:** Place/remove under **mouse cursor** (ray to grid), not camera-center aim.
3. **Edit target:** Closest **logic point** (dual-grid point / vertex), **not** “nearest whole main-grid quad alone.”
4. **LMB place (default land/fill):** Flip or set that point’s type (e.g. water→land / empty→occupied). Then **rebuild meshes for the four dual cells** connected to that point.
5. **RMB remove (or clear binding):** Inverse type flip on that point; again refresh the **same four** dual cells.
6. **Adjacency on place:** Neighbor configuration is read from the **four corner types** of each dual cell → pick MeshLibrary entry (and rotation/mirror). Adjacency is **automatic mesh selection**, not a separate sim.
7. **No cam yank:** Camera pose unchanged on place/remove.
8. **Graybox OK for core:** Distinct dual-cell mesh variants may be simple gray meshes — but there must be **corner-driven variant selection**, not one cube for every cell.

### Binary corner palette (core minimum)

For craft-core staging, two types at logic points are enough to prove Townscaper shape:

- `Empty` / water-equivalent
- `Filled` / land-equivalent

(Depth ticket widens typed palette later — Empty·Ground·Wall·Water·Oasis.)

### Mesh count check (honesty)

If the craft path only ever instances **one** box mesh id regardless of neighbors → **fail** Townscaper shape.

---

## Click-add sequence (Half-B pseudocode)

```text
on_lmb:
  hit = ray_from_mouse_to_craft_plane()
  P = nearest_logic_point(hit)          # dual-grid point, half-cell offset lattice
  set_type(P, FILLED)                   # or toggle
  for Q in four_dual_cells_around(P):
      corners = (NW, NE, SW, SE) types at Q's corners
      mesh_id, rot = lookup_dual_tile(corners)   # ≤16 raw / ~6 unique + rot/mirror
      gridmap_set(Q, mesh_id, rot)

on_rmb:
  same as above with EMPTY / clear
```

**Godot mapping (Prefer):**

- Logic point store: dictionary / sparse map keyed by integer lattice coords (or custom resource).
- Visual: stock **GridMap** + **MeshLibrary** for the dual-cell variants (or equivalent stock grid overlay).
- Picking: ray → plane → snap to logic point; collider on craft plane / GridMap must support mouse-aim after visual swaps.

---

## What adjacency does on place (normative)

| Event | Effect |
|-------|--------|
| Point type changes | Only local dual cells update (four quads) |
| Each dual cell | Reads its four corner types → selects edge / corner / full / empty variant |
| Convex + concave | Both round **inside** the dual tile (corners modeled in-tile, not on shared edges) |
| Cascades | No global rebuild required for one click; no Terrain3D height write |

---

## Full video technique map (useful later; not all required for craft-core)

| Stage in video | Use for us |
|----------------|------------|
| Plain grid + ray place | Baseline authorship |
| Neighbor-swapped whole tiles (~15) | **Do not ship** as final grammar — motivates dual |
| Insert-in vs enlarge-out corner tradeoff | Explains why dual exists |
| **Dual grid + corner typing + update-four** | **Craft-core Success bar** |
| Multiple handcrafted variants per config | Visual ticket seasoning (hide repetition) |
| Handle-based squash/stretch on irregular grid | Later organic polish — out of craft-core |
| Stålberg irregular quad grid (hex→dissolve→relax) | Later — not required for Hot Wheels graybox |
| Multi-tile special pieces / neighbor pattern match | Later Townscaper “magic” — depth/visual seasoning |
| Model synthesis / WFC (Bad North auto islands) | Out of craft authorship path |

---

## Hot Wheels vs Terrain3D (unchanged)

- Craft = dual-grid tile authorship only.
- Terrain3D = later consumer feed — **not** armed on craft path for `alpha0_townscaper_craft_core_r1`.
- Files may remain on LIVE disk; craft entry must not call / show / Tab-handoff into Terrain3D.

## Cross-links

- [[alpha0_townscaper_tutorial_r1]] · [[alpha0_townscaper_tutorial_s1_attest]] · [[alpha0_townscaper_tutorial_s2_dual_offset_r1]]
- [[alpha0_townscaper_craft_core_r1]] (step 1 Prefer base) · visual Prefer failed altitude · [[alpha0_townscaper_df_depth_r1]] (frozen)
- [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]]
- [[Prefer-Authorship-Host-Law]] · [[COHESIVE-VISION-ART-DIRECTION]]
