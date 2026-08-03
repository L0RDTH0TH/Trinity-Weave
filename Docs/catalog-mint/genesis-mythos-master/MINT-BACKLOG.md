---
title: MINT-BACKLOG — genesis-mythos-master
project-id: genesis-mythos-master
para-type: Project
backlog_status: frozen_for_mint
mint_phase: children_batch
harvest_pass: children
series_draft_accepted: true
waive_series_draft: false
children_greenlit: true
children_rewritten: true
walk_defs_split: true
waived_axes: []
schema_version: 1
locked_child_batches: [ux_camera_control_envelopes, ux_living_world_continuity, ux_backstory_legacy_integration]
active_child_batch: ux_dm_campaign_creation
next_child_batch: ux_dm_campaign_creation
series_published_trinity_ref: d480f3dade1ff5f19301c2aadaebcfc86eeabb8e
children_published_trinity_ref: af5ec0d334b71c0a2cb65661d5abfb6bf7138de5
quality_validation_status: camera_lw_backstory_locked; active_dm_campaign_creation
walk_defs_layout: scopes/<parent>/children-of-<parent>/<child>/WALK.md
rubric: Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md
machine_mirror: MINT-BACKLOG.yaml
---

# MINT-BACKLOG — `genesis-mythos-master`

Obsidian **list / prune** surface. Full Meaning defs live under `scopes/<parent>/SERIES.md` and `scopes/<parent>/children-of-<parent>/<child>/WALK.md` (list **dirs** under `children-of-*` to see the batch). Edit walk cards or status here; harvest/freeze/sync refreshes `MINT-BACKLOG.yaml`.

## Operator gate (two-pass mint)

1. **Series draft** (Cursor) → accept → series-only harvest.
2. Prune series; freeze (series anti-mandate gate). Taxonomy coverage waits for children pass.
3. Grok+user **series walk** until all series `done`.
4. Diff/fit vs `archive_ref` if remine. Then **Trinity/GitHub publish** (`series_published_trinity_ref`) — Grok-facing gate, not Curator.
5. Only then children harvest (series lens) → greenlight → Cursor batches → Trinity-publish children.
6. Actions: `UX_MINT_BACKLOG` `series_draft` | `generate` | `freeze` | `publish_series` | `greenlight_children` | `lock_child_batch` | `publish_children`.

**Current status:** `frozen_for_mint`  
**Mint phase:** `children_batch`  
**Harvest pass:** `children`  
**Series Trinity ref:** `d480f3dade1ff5f19301c2aadaebcfc86eeabb8e`  
**Children Trinity ref:** `af5ec0d334b71c0a2cb65661d5abfb6bf7138de5`  
**Quality validation:** `camera_lw_backstory_locked; active_dm_campaign_creation`  
**Locked child batches:** `ux_camera_control_envelopes, ux_living_world_continuity, ux_backstory_legacy_integration`  
**Active / next child batch:** `ux_dm_campaign_creation`  
**Waived axes/slots:** `(none)`  
**Walk defs split:** `True`  
**Rubric:** [[Docs/catalog-mint/_shared/UX-MINT-RUBRIC|UX mint rubric]]

## Quick status (by series parent)

Grouped by paternity — series parent, then its children. Not a flat coverage list.

#### Series `ux_backstory_legacy_integration` — Backstory and legacies can hook into play and chronicle — **LOCKED batch**

- [x] `ux_backstory_legacy_integration` — Backstory and legacies can hook into play and chronicle (`done`) [table] [series]
  - *Walk dirs:* `scopes/ux_backstory_legacy_integration/SERIES.md` · `scopes/ux_backstory_legacy_integration/children-of-ux_backstory_legacy_integration/<child>/WALK.md`
  - *Children: 3 done / 0 pending / 3 total*
  - [x] `ux_chronicle_buckets` — Chronicle data buckets (`done`) [table] [coverage]
  - [x] `ux_class_chrome_discovery` — Class / identity chrome discovery (`done`) [inhabit] [coverage]
  - [x] `ux_player_lite_lore_gui` — Player-lite lore GUI (`done`) [table] [coverage]

#### Series `ux_camera_control_envelopes` — Perspective and control envelopes can change and cleanly return — **LOCKED batch**

- [x] `ux_camera_control_envelopes` — Perspective and control envelopes can change and cleanly return (`done`) [inhabit] [series]
  - *Walk dirs:* `scopes/ux_camera_control_envelopes/SERIES.md` · `scopes/ux_camera_control_envelopes/children-of-ux_camera_control_envelopes/<child>/WALK.md`
  - *Children: 13 done / 0 pending / 13 total*
  - [x] `ux_absent_proxy` — Absent-player proxy (`done`) [inhabit] [coverage]
  - [x] `ux_agency_handoff_enter_exit` — Agency enter / exit handoff feel (`done`) [inhabit] [coverage]
  - [x] `ux_baseline_fp` — Baseline first-person embodiment (`done`) [inhabit] [coverage]
  - [x] `ux_baseline_fp_controls` — Baseline FP controls (`done`) [inhabit] [coverage]
  - [x] `ux_divination_override` — Divination / remote-sense override (`done`) [inhabit] [coverage]
  - [x] `ux_dm_mapcam` — DM MapCam (`done`) [inhabit] [coverage]
  - [x] `ux_dm_pilot` — DM pilot (agency, not Sensorium) (`done`) [inhabit] [coverage]
  - [x] `ux_dm_sensorium` — DM Sensorium Attach (`done`) [inhabit] [coverage]
  - [x] `ux_dm_worldcam` — DM WorldCam (`done`) [inhabit] [coverage]
  - [x] `ux_dominate_pilot` — Dominate / pilot (controller) (`done`) [inhabit] [coverage]
  - [x] `ux_dominate_victim` — Dominate victim / passenger overlay (`done`) [inhabit] [coverage]
  - [x] `ux_liminal_unconscious` — Liminal / unconscious presentation (`done`) [inhabit] [coverage]
  - [x] `ux_planar_travel_override` — Planar / gate travel override (`done`) [inhabit] [coverage]

#### Series `ux_collaborative_table_agency` — Shared virtual-tabletop loop with character agency and DM orchestration

- [x] `ux_collaborative_table_agency` — Shared virtual-tabletop loop with character agency and DM orchestration (`done`) [table] [series]
  - *Walk dirs:* `scopes/ux_collaborative_table_agency/SERIES.md` · `scopes/ux_collaborative_table_agency/children-of-ux_collaborative_table_agency/<child>/WALK.md`
  - *Children: 0 done / 2 pending / 2 total*
  - [ ] `ux_application_shell` — Application shell / layout chrome (`pending`) [surfaces] [coverage]
  - [ ] `ux_primary_navigation` — Primary navigation / wayfinding (`pending`) [flows] [coverage]

#### Series `ux_combat_play_surface` — Combat can resolve by authored paths including non-win ends

- [x] `ux_combat_play_surface` — Combat can resolve by authored paths including non-win ends (`done`) [inhabit] [series]
  - *Walk dirs:* `scopes/ux_combat_play_surface/SERIES.md` · `scopes/ux_combat_play_surface/children-of-ux_combat_play_surface/<child>/WALK.md`
  - *Children: 0 done / 1 pending / 1 total*
  - [ ] `ux_combat_cast_feedback` — Combat / cast sensory feedback (`pending`) [inhabit] [coverage]

#### Series `ux_living_world_continuity` — World can move off-screen and show lasting readable costs — **LOCKED batch**

- [x] `ux_living_world_continuity` — World can move off-screen and show lasting readable costs (`done`) [living_world] [series]
  - *Walk dirs:* `scopes/ux_living_world_continuity/SERIES.md` · `scopes/ux_living_world_continuity/children-of-ux_living_world_continuity/<child>/WALK.md`
  - *Children: 19 done / 0 pending / 19 total*
  - [x] `ux_canon_pipeline_feel` — Canon pipeline feel (`done`) [living_world] [coverage]
  - [x] `ux_economy_resources` — Resource distribution visibility (`done`) [living_world] [coverage]
  - [x] `ux_economy_trade` — Trade routes / market pressure (`done`) [living_world] [coverage]
  - [x] `ux_quest_pressure_surface` — Quest pressure from canon (`done`) [living_world] [coverage]
  - [x] `ux_sim_weather_pulse` — Weather / ambient sim pulse (`done`) [living_world] [coverage]
  - [x] `ux_wa_faction_goals` — Faction goals / agenda surface (`done`) [living_world] [coverage]
  - [x] `ux_wa_faction_hierarchy` — Faction hierarchy surface (`done`) [living_world] [coverage]
  - [x] `ux_wa_faction_offscreen` — Off-screen faction activity (`done`) [living_world] [coverage]
  - [x] `ux_wa_faction_reputation` — Reputation standing surface (`done`) [living_world] [coverage]
  - [x] `ux_wa_faction_territory` — Faction territory / influence (`done`) [living_world] [coverage]
  - [x] `ux_wa_locations` — Location surfaces (`done`) [living_world] [coverage]
  - [x] `ux_wa_lore_articles` — Lore codex / articles (`done`) [living_world] [coverage]
  - [x] `ux_wa_maps_vs_embodied` — Maps vs embodied discovery (`done`) [living_world] [coverage]
  - [x] `ux_wa_npc_agenda` — NPC agenda / schedule visibility (`done`) [living_world] [coverage]
  - [x] `ux_wa_npc_dialogue_hooks` — NPC dialogue / roleplay hooks (`done`) [living_world] [coverage]
  - [x] `ux_wa_npc_relations` — NPC relationship web (`done`) [living_world] [coverage]
  - [x] `ux_wa_npc_secrets` — NPC secrets / knowledge gates (`done`) [living_world] [coverage]
  - [x] `ux_wa_npc_sheet` — NPC identity sheet feel (`done`) [living_world] [coverage]
  - [x] `ux_wa_timelines` — Timeline / era threads (`done`) [living_world] [coverage]

#### Series `ux_quiet_between_pillars` — In-adventure quiet keeps continuous fiction between combat social and explore

- [x] `ux_quiet_between_pillars` — In-adventure quiet keeps continuous fiction between combat social and explore (`done`) [table] [series]
  - *Walk dirs:* `scopes/ux_quiet_between_pillars/SERIES.md` · `scopes/ux_quiet_between_pillars/children-of-ux_quiet_between_pillars/<child>/WALK.md`
  - *No children lensed under this series*

#### Series `ux_world_authorship_modability` — Table and community can author world change via curated and mod contracts

- [x] `ux_world_authorship_modability` — Table and community can author world change via curated and mod contracts (`done`) [living_world] [series]
  - *Walk dirs:* `scopes/ux_world_authorship_modability/SERIES.md` · `scopes/ux_world_authorship_modability/children-of-ux_world_authorship_modability/<child>/WALK.md`
  - *Children: 0 done / 1 pending / 1 total*
  - [ ] `ux_content_authoring_surface` — Content authoring surface (`pending`) [content] [coverage]

#### Series `ux_dm_campaign_creation` — DM can bootstrap a campaign frame inside a world — **ACTIVE batch**

- [x] `ux_dm_campaign_creation` — DM can bootstrap a campaign frame inside a world (`done`) [table] [series]
  - *Walk dirs:* `scopes/ux_dm_campaign_creation/SERIES.md` · `scopes/ux_dm_campaign_creation/children-of-ux_dm_campaign_creation/<child>/WALK.md`
  - *Children: 0 done / 3 pending / 3 total*
  - [ ] `ux_session0_bootstrap` — Session 0 bootstrap feel (`pending`) [table] [coverage]
  - [ ] `ux_session_onboarding` — Session / onboarding bootstrap (`pending`) [flows] [coverage]
  - [ ] `ux_tone_profile_surface` — Campaign tone profile surface (`pending`) [table] [coverage]

#### Series `ux_dm_session_prep` — DM can prep a session without leaving the collaborative table frame

- [x] `ux_dm_session_prep` — DM can prep a session without leaving the collaborative table frame (`done`) [table] [series]
  - *Walk dirs:* `scopes/ux_dm_session_prep/SERIES.md` · `scopes/ux_dm_session_prep/children-of-ux_dm_session_prep/<child>/WALK.md`
  - *Children: 0 done / 1 pending / 1 total*
  - [ ] `ux_dm_workbench_lore_gui` — DM workbench lore GUI (`pending`) [table] [coverage]

#### Series `ux_early_game` — Early play is a power band that gates world and pillar response

- [x] `ux_early_game` — Early play is a power band that gates world and pillar response (`done`) [flows] [series]
  - *Walk dirs:* `scopes/ux_early_game/SERIES.md` · `scopes/ux_early_game/children-of-ux_early_game/<child>/WALK.md`
  - *No children lensed under this series*

#### Series `ux_late_game` — Late play is a power band for campaign crescendo, close, and character-to-world persistence

- [x] `ux_late_game` — Late play is a power band for campaign crescendo, close, and character-to-world persistence (`done`) [living_world] [series]
  - *Walk dirs:* `scopes/ux_late_game/SERIES.md` · `scopes/ux_late_game/children-of-ux_late_game/<child>/WALK.md`
  - *No children lensed under this series*

#### Series `ux_mental_stat_interpretation` — Mental stats surface available read paths not only sheet numbers

- [x] `ux_mental_stat_interpretation` — Mental stats surface available read paths not only sheet numbers (`done`) [surfaces] [series]
  - *Walk dirs:* `scopes/ux_mental_stat_interpretation/SERIES.md` · `scopes/ux_mental_stat_interpretation/children-of-ux_mental_stat_interpretation/<child>/WALK.md`
  - *No children lensed under this series*

#### Series `ux_mid_game` — Mid play is a power band for lasting pressure and deeper world response

- [x] `ux_mid_game` — Mid play is a power band for lasting pressure and deeper world response (`done`) [living_world] [series]
  - *Walk dirs:* `scopes/ux_mid_game/SERIES.md` · `scopes/ux_mid_game/children-of-ux_mid_game/<child>/WALK.md`
  - *No children lensed under this series*

#### Series `ux_player_character_creation` — Players can author characters and submit them for DM acceptance into a world

- [x] `ux_player_character_creation` — Players can author characters and submit them for DM acceptance into a world (`done`) [table] [series]
  - *Walk dirs:* `scopes/ux_player_character_creation/SERIES.md` · `scopes/ux_player_character_creation/children-of-ux_player_character_creation/<child>/WALK.md`
  - *No children lensed under this series*

#### Series `ux_world_generation` — DM can create (table can shape) a persistent living world

- [x] `ux_world_generation` — DM can create (table can shape) a persistent living world (`done`) [living_world] [series]
  - *Walk dirs:* `scopes/ux_world_generation/SERIES.md` · `scopes/ux_world_generation/children-of-ux_world_generation/<child>/WALK.md`
  - *Children: 0 done / 1 pending / 1 total*
  - [ ] `ux_worldgen_gui` — Worldgen GUI (`pending`) [living_world] [coverage]

## Items

Full Meaning cards are **not** inlined here. Open:

- Series: `scopes/<series_id>/SERIES.md`
- Children: list dirs under `scopes/<parent>/children-of-<parent>/` then open `<child>/WALK.md`

Factory L5 remains `scopes/<row_id>/L5.md` (separate from walk cards).

## Coverage reminder

Two-pass: series cards first (`walk_tier: series`), locked + Trinity-published, then children mined through those lenses. Display groups children under their `parent_id` series. Taxonomy slots are children-pass coverage; Actual-Play nouns are thickeners/skins. See rubric + `SERIES-ALTITUDE-EXEMPLARS.md`.
