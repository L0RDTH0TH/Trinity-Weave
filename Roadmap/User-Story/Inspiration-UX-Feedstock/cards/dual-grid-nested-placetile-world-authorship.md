---
title: dual-grid-nested-placetile-world-authorship
schema_version: 1
source_title: Townscaper dual-grid + Civ/Anno living-sim cheat-mode (operator synthesis)
signal: strong
research_status: operator_locked_feedstock
assumption: false
updated: 2026-10-02
liked: "Dual-grid nested placetile authorship that feels like painting place at multiple scales; procedural and full-manual parity; living-sim connectivity in cheat mode; clean hand-off into realistic Terrain3D while keeping stylized low-poly craft language"
why_it_worked: "Click/wheel intent on a dual grid produces coherent nested worlds without forcing the player into a full city-builder desk; nesting + biome pressure + automatic roads give the long-form curation mini-game that feeds the open world"
fits_our_game: "Primary world-generation / curation surface. Replaces the thin townscaper-click-add-world-element draft. Dual-grid (Hot Wheels craft layer) feeds Terrain3D (real car). Four starting nest levels with natural zoom. Config dials (cell size, settlement distance, rivers, climate, ToneProfile) bias everything. Biomes express living-sim + rules-system mechanical features. Full procedural and full manual craft are peers."
refuse_to_copy:
  - "Pure Townscaper toy-scale, zero-consequence click-and-raise as the entire living world"
  - "Instant 3D completion on every click with no calendar / NPC labor / living-sim residue"
  - "Manual road drawing as the primary or required path"
  - "Skyrim-style loading-screen transitions between nest levels"
  - "Blending craft-grid camera with Terrain3D deformation in the craft view"
  - "Treating the dual-grid as a full population / economy / city-builder desk"
  - "1:1 scale between model cell and open-world footprint"
  - "Photoreal or high-poly default (stylized low-poly remains factory bar)"
  - "Hard-coded fixed list of only four biomes with no living-sim pressure"
  - "Ossifying tutorial hex-19 scaffold as the forever product lattice"
maps_to_series:
  - ux_world_authorship_modability
  - ux_dm_campaign_creation
  - ux_camera_control_envelopes
pillars:
  - exploration
  - tooling
ip_posture: pattern_only_no_clone
canonical_yt: https://www.youtube.com/watch?v=Y19Mw5YsgjI
canonical_yt_title: How One Guy FIXED Procedural Generation
replaces: townscaper-click-add-world-element
feedstock_locked: true
feedstock_locked_at: 2026-10-02
---

# Derived move-pin — dual-grid nested placetile world authorship

**Job:** Give the DM / world-curator a Civ/Anno-style living-sim world builder in cheat mode. Dual-grid nested placetile surface with biome support, procedural + full-manual parity, automatic connectivity, four starting nest levels, and a clean hand-off into the playable open-world Terrain3D instance. Curation itself is a satisfying long-form mini-game.

## Lock clarifications (validate 2026-10-02)

| Clarification | Statement |
|---------------|-----------|
| **Feedstock only** | This card is feedstock. No L5, no pin-derive, no seasoning apply, no factory WELD from this lock turn. |
| **Tutorial scaffold ≠ product lattice** | Fixed **hex-19** occupancy on [[alpha0_townscaper_tutorial_r1]] / [[alpha0_townscaper_tutorial_s1_occupancy_r1]] is a **ladder teaching scaffold** for dual-grid intent — **not** the ossified forever product lattice. Product cell size / grid extent remain tunable (config dials below). |
| **Aspiration altitude** | Four-level nesting, biome mechanical pressure, living-sim connectivity / Civ–Anno cheat-mode curation, and full Terrain3D hand-off are **north-star feedstock altitude** for later tickets — **not** Success for the current tutorial ladder. Ladder remains step-by-step execution. |
| **Hot Wheels ≠ Terrain3D** | Dual-grid craft = Hot Wheels; Terrain3D = real car. No craft-view blend; no cam recenter on place. Law: [[Prefer-Authorship-Host-Law]] · [[COHESIVE-VISION-ART-DIRECTION]]. |

## Pillar(s)
- Exploration — world shape, density, habitat, travel pressure, nested place
- Tooling — DM / Session-0 world-authorship surface, config dials, craft-to-play hand-off

## Pattern (do)

### Dual-grid craft surface
- Townscaper / dual-grid grammar (canonical YT): interact on one grid; generation and mesh live on the offset dual. Neighbor blending is automatic and correct.
- Interaction model: radial wheel with icons on tile select. Top-level categories include “modify living-simulation aspects” and “modify terrain aspects.” Under terrain sit physical form, biome expression, height, etc. Height raise is one option inside the wheel, not the primary double-click gesture.
- Grid size is procedurally generatable inside a tunable range.

### Nesting (starting contract)
- Four levels: World → City → Building → Cellar.
- Entering a nested tile is a continuous, natural zoom into its own dual-grid (no loading-screen cut).
- Extending the stack later (add a fifth level) is allowed; depth is not artificially capped at four forever.
- Different grids may later be used for dimensional separation (stray thought only — not required for first card).
- **Altitude:** nesting zoom is feedstock aspiration; tutorial ladder does not ship nest levels as Success.

### Biome support
- Generic biome system (not a hard-coded four-item list).
- Biomes affect visuals, blending, what can nest, **and** mechanical pressure via the living-simulation layer.
- Must express rules-system features the world is required to adapt to (difficult terrain, movement costs, habitat suitability, etc.).
- Habitat actors respect biome (an owlbear in open desert is immersion-breaking unless its presence is the explicit plot anomaly).
- **Altitude:** biome mechanical pressure = later tickets; not tutorial Success.

### Connectivity / roads
- Automatic / procedural first. Serves the living-sim layer (trade, movement, settlement networks).
- Manual override possible but never required.
- Optimal routing + wrapping so the network stays coherent as tiles change.
- **Altitude:** living-sim connectivity = cheat-mode curation north star; not current ladder Success.

### Generation posture & config page
- Full procedural generation and full manual craft are first-class peers.
- Config / setup page dials (non-exhaustive, all feed Terrain3D):
  - Cell size
  - Town / settlement distance
  - River prevalence
  - Climate distribution
  - **World tone profile** (already defined in Conceptual / PMG excerpt):

| Profile        | Vibe                            | System bias                                              |
|----------------|---------------------------------|----------------------------------------------------------|
| High Fantasy   | Wonder, abundant magic          | Exotic biomes, high magic density, wondrous weather      |
| Medium Fantasy | Default adventure table         | Functional societies, balanced intrigue + adventure      |
| Low Fantasy    | Grounded, rare dangerous magic  | Muted world, political human-scale conflict              |
| Grimdark       | Moral gray, harsh consequences  | Bleak weather bias, costly hope, persistent scars        |

Tone biases every other world-gen and living-sim value. Terrain output remains realistic even while the craft and character language stays stylized low-poly.

### Live vs prep
- Both supported.
- Intentional regeneration remains available.
- During live play: structure placement and monster-nest spawning are allowed; full terrain re-generation is the exception.

### Downstream hand-off
- Dual-grid model uses an **attention-correct scaling factor** so important features are never lost at model scale.
- Open-world Terrain3D instance uses its own **realistic footprint**.
- Dual-grid emits actual low-poly mesh instances as the **first approach**. Production must keep the option open to separate craft meshes from open-world meshes later if needed.
- Hot Wheels craft layer stays distinct from the Terrain3D “real car” (no camera recenter or deformation of the craft grid into terrain while in craft view).
- **Altitude:** full Terrain3D feed remains deferred / later ticket (scrapped Prefer this round); hand-off grammar stays feedstock law.

## Refuse (required)
- Pure Townscaper toy-scale, zero-consequence building as the whole living world
- Instant 3D completion on every click with no calendar / NPC labor / living-sim residue
- Manual road drawing as the primary path
- Skyrim-style loading-screen nest transitions
- Blending craft-grid camera with Terrain3D deformation in craft view
- Treating the dual-grid as a full population / economy desk
- 1:1 scale between model cell and open-world footprint
- Photoreal or high-poly default
- Habitat actors that ignore biome pressure without explicit plot justification
- Treating tutorial hex-19 as the forever product lattice

## Maps to factory / existing pins
- Replaces / supersedes `townscaper-click-add-world-element`
- Strengthens: seed-region-density-and-travel, exploration-altitude-ecology, structures-gen-cultural-historical, calendar-npc-labor-world-shape, intent-shape-to-realization, manor-lords-high-altitude-region
- New or thickened candidates (for later pin-derive / seasoning — **not this turn**): dual-grid-nested-placetile-authorship, biome-mechanical-pressure, living-sim-connectivity-cheat-mode, four-level-nest-zoom, procedural-manual-parity-config, dual-grid-to-terrain3d-hand-off

## Visual language
- Stylized low-poly (Astroneer bar already locked)
- Reference set: Ingest dual-grid diagrams (`single-grid-section.jpg`, `multiple-grid-sections.jpg`, `Final-Grid.jpg`) + Factory-DRB craft-visual refs + nature packs / Model-pack — readability and saturation target
- Terrain itself stays realistic; craft and character language stays stylized
- Cite: [[Visual-Factory-Direction-Stylized-Low-Poly]] · [[COHESIVE-VISION-ART-DIRECTION]]

## Notes
- Canonical dual-grid technique source remains the linked YouTube — [[Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01]] · grammar [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]].
- Active execution ladder (step-by-step, not this card’s Success bar): [[alpha0_townscaper_tutorial_r1]].
- Cursor + operator own the vault write and INDEX / dialogue-receipt update.
