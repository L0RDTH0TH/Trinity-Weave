---
title: Pin-derive mint_target stubs — genesis-mythos-master
project-id: genesis-mythos-master
status: dual_approved_shape_only
updated: 2026-08-14
operator_split: grok_optimal_must_mint_6
---

# MINT-TARGET-STUBS (shape only — no amendment files yet)

**Operator accepted (2026-08-14):** Grok optimal volume split — confirm 4 · must-mint 6 · defer yellow 5.

**Dual-approve:** Grok volume gate + operator accept. **Write gate:** still closed until operator says **write**.

**After write (per row):** Highlightr on parent → PIN-INDEX → re-pin → PIN-EXCERPT → Trinity → Grok **single-row subset only**.

## Confirm now (no mint)

| row_id | Action |
|--------|--------|
| `ux_dm_campaign_creation` | Leave `minted: true` amendment |
| `ux_living_world_continuity` | Keep Phase-3-2 Off-Screen primary |
| `ux_backstory_legacy_integration` | Confirm Canon Registry primary |
| `ux_world_authorship_modability` | Confirm Modularity Seams primary |

## Defer (accepted yellow risk — revisit after apply_pins / L5 if painful)

`ux_dm_session_prep` · `ux_early_game` · `ux_mid_game` · `ux_collaborative_table_agency` · `ux_camera_control_envelopes`

## Must-mint stubs (6)

### 1. `ux_world_generation`

```yaml
mint_target:
  parent: Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914
  proposed_title: amend-durable-world-container
  path_class: amendment
  minted: false
  path: ""  # Conceptual-Amendments/Phase-2-Procedural-Generation-and-World-Building/
  weld_heading: "## Behavior (amendment weld)"
```

**Weld must carry:** durable world container; DM creates initial form; players do not author first world; import/attach first-class; multi-campaign attach to same world; every world-hitting change DM-retconnable.

**After mint:** amendment = primary; Phase-2 Behavior → supporting (actor/order machinery).

---

### 2. `ux_player_character_creation`

```yaml
mint_target:
  parent: Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600
  proposed_title: amend-player-author-dm-acceptance-flow
  path_class: amendment
  minted: false
  path: ""  # Conceptual-Amendments/.../Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/
  weld_heading: "## Behavior (amendment weld)"
```

**Weld must carry:** player owns character before and after greenlight; invite → attach → greenlight; unfinished ≠ draft type; background→world proposals DM-gated. Soft-closed class expression is **seasoning**, not the weld body.

**After mint:** amendment = primary; SpawnBootstrap → supporting (entry machinery). Do **not** keep thin SpawnBootstrap as primary.

---

### 3. `ux_late_game`

```yaml
mint_target:
  parent: Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615
  proposed_title: amend-high-band-close-pc-world-persistence
  path_class: amendment
  minted: false
  path: ""  # Conceptual-Amendments/.../Phase-3-2-Off-Screen-Faction-Tribe-Activity/
  weld_heading: "## Behavior (amendment weld)"
```

**Weld must carry:** high power-band crescendo + close; PC→world persistence as survivors; lasting costs at late amplitude. **Does not** steal living_world’s Off-Screen primary — Off-Screen stays supporting here (since-you-left machinery).

**Board fix:** breaks identical primary title with `ux_living_world_continuity`.

---

### 4. `ux_quiet_between_pillars`

```yaml
mint_target:
  parent: Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600
  proposed_title: amend-in-adventure-quiet-surface
  path_class: amendment
  minted: false
  path: ""  # Conceptual-Amendments/.../Phase-3-1-Tick-Based-Simulation-Core/
  weld_heading: "## Behavior (amendment weld)"
```

**Weld must carry:** in-adventure quiet as continuous low-intensity fiction (road/camp/linger); system waiting; between combat/social/explore bursts. Explicitly **not** between-adventures weeks/months (living_world).

**After mint:** amendment = primary; Tick Core → supporting (pipeline).

---

### 5. `ux_combat_play_surface`

```yaml
mint_target:
  parent: Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045
  proposed_title: amend-combat-play-surface-enter-exit-ends
  path_class: amendment
  minted: false
  path: ""  # Conceptual-Amendments/.../Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/
  weld_heading: "## Behavior (amendment weld)"
```

**Weld must carry:** combat as distinct enter/exit surface; authorship menu of legitimate ends (fight/flee/parley/stakes/surrender/escape-with-cost/…); power-band gated lasting costs; consumes rule math (does not own it).

**After mint:** amendment = primary; Rule-Engine → supporting.

---

### 6. `ux_mental_stat_interpretation`

```yaml
mint_target:
  parent: Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115
  proposed_title: amend-mental-stat-cue-read-paths
  path_class: amendment
  minted: false
  path: ""  # Conceptual-Amendments/.../Phase-5-2-Spell-Agency-Perspective-Metadata/
  weld_heading: "## Behavior (amendment weld)"
```

**Weld must carry:** INT/WIS/CHA (and kin) as available read-paths; cue-without-spill; soft-teaching. Dominate/absent-proxy metadata stays supporting altitude, not the Meaning weld.

**After mint:** amendment = primary; Spell-Agency Metadata → supporting.

---

## Write checklist (when operator says write)

For each of the six:

1. Create amendment under `Roadmap/Conceptual-Amendments/<relative-parent-path>/`
2. Highlightr wrap on parent Behavior (or cite amendment heading)
3. Add title to PIN-INDEX
4. Update PIN-DERIVE: recommended → amendment; refs roles; `minted: true` + path
5. Regenerate PIN-EXCERPT
6. Pack emit + Trinity sync
7. Grok single-row subset only

Still no L5. Still no `apply_pins` until all six written + board confirm (including deferred yellows as accepted-with-risk).
