---
title: Townscaper click-add for world / grid elements
schema_version: 1
source_title: Townscaper
signal: strong
research_status: operator_locked_step1
assumption: false
updated: 2026-10-01
liked: "Click-and-add UX for placing world elements — joyful, low-friction authorship; 2D map intent → 3D world realization (or equivalent)"
why_it_worked: "Adding a building/block feels like painting place, not managing a construction sim"
fits_our_game: "Model for when a user adds a world element or grid item: Townscaper feel for intent. Realization still follows calendar-NPC-labor doctrine — click designs; world fills in over time. Worldgen step one = dual-grid Hot Wheels authorship that FEEDS Terrain3D (real car) — layers stay distinct."
refuse_to_copy:
  - "Townscaper toy scale / no-consequence building as the whole living world"
  - "Instant 3D completion on every click with no calendar or NPC labor"
  - "Only abstract pastel blocks — fantasy place must still read as our world"
  - "Blending craft tiles with Terrain3D deformation in craft view"
  - "Camera recenter on place; deforming craft grid into terrain under craft cam"
maps_to_series:
  - ux_world_authorship_modability
  - ux_camera_control_envelopes
  - ux_dm_campaign_creation
pillars:
  - tooling
  - exploration
ip_posture: pattern_only_no_clone
canonical_yt: https://www.youtube.com/watch?v=Y19Mw5YsgjI
canonical_yt_title: How One Guy FIXED Procedural Generation
---

# Townscaper click-add for world / grid elements

Job: authorship UX = delightful click-add. Complements Halo Forge glow (validity) and calendar-NPC-labor (timeful realization).

## Canonical YT — worldgen step one (operator locked 2026-10-01)

| Field | Value |
|-------|--------|
| **URL** | https://www.youtube.com/watch?v=Y19Mw5YsgjI |
| **Title** | How One Guy FIXED Procedural Generation |
| **Channel** | Game Dev Buddies |
| **Framing** | Maps how Townscaper achieves its goals; **model for our world generation step one**; where DF inspirations spring forth |
| **Full citation note** | [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] |

### Hot Wheels vs Terrain3D (separation law)

- **Craft cam** = tile authorship only — **no** camera recenter on place; **no** deforming craft grid into terrain
- Townscaper dual-grid (**Hot Wheels**) **FEEDS** Terrain3D (**real car**) — distinct layers
- **Do not** blend craft tiles with Terrain3D deformation in craft view

### TL;DR technique (normative grammar note)

**Must load:** [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] — dual grid offset half a cell; type per corner; place updates four dual quads; mouse-aim ray; not “click places a box.” Detail: citation + grammar notes.
