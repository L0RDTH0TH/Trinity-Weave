---
title: MINT-BACKLOG — genesis-mythos-master
project-id: genesis-mythos-master
para-type: Project
backlog_status: frozen_for_mint
waived_axes: []
schema_version: 1
frozen_at: 2026-07-30T04:16:06Z
rubric: Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md
machine_mirror: MINT-BACKLOG.yaml
---

# MINT-BACKLOG — `genesis-mythos-master`

Obsidian **operator prune / critique** surface. Edit item fields below (especially `status`), then harvest/freeze/sync will refresh `MINT-BACKLOG.yaml` (machine walk queue + Grok pack).

## Operator gate

1. Prune: set `status` to `dropped`, or rewrite `label` / `summary` toward experience nouns.
2. Cover or waive required taxonomy slots (see rubric) — missing faces/facets block freeze.
3. When ready: set frontmatter `backlog_status: frozen_for_mint` **or** run `UX_MINT_BACKLOG` `action: freeze`.
4. Mint walk: Grok takes next `pending` only when frozen (or you name an id).

**Current status:** `frozen_for_mint`  
**Waived axes/slots:** `(none)`  
**Rubric:** [[Docs/catalog-mint/_shared/UX-MINT-RUBRIC|UX mint rubric]]

## Quick status

- [x] `ux_world_generation` — DM can create (table can shape) a persistent living world (`done`) [living_world] [series]
- [x] `ux_dm_campaign_creation` — DM can bootstrap a campaign frame inside a world (`done`) [table] [series]
- [x] `ux_player_character_creation` — Players can author characters and submit them for DM acceptance into a world (`done`) [table] [series]
- [x] `ux_dm_session_prep` — DM can prep a session without leaving the collaborative table frame (`done`) [table] [series]
- [-] `ux_game_start` — Table can start play under a chosen campaign-start structure (`dropped`) [table] [coverage]
- [x] `ux_early_game` — Early play is a power band that gates world and pillar response (`done`) [flows] [series]
- [x] `ux_mid_game` — Mid play is a power band for lasting pressure and deeper world response (`done`) [living_world] [series]
- [ ] `ux_end_game` — Table can author campaign close and ending ownership (`pending`) [table] [series]
- [ ] `ux_mental_stat_interpretation` — Mental stats can surface as readable interpretation not only numbers (`pending`) [surfaces] [series]
- [ ] `ux_collaborative_table_agency` — Every seat is a player including the DM orchestrator (`pending`) [table] [series]
- [ ] `ux_quiet_between_pillars` — Downtime keeps continuous fiction between combat social and explore (`pending`) [table] [series]
- [ ] `ux_combat_play_surface` — Combat can resolve by authored paths including non-win ends (`pending`) [inhabit] [series]
- [ ] `ux_camera_control_envelopes` — Perspective and control envelopes can change and cleanly return (`pending`) [inhabit] [series]
- [ ] `ux_living_world_continuity` — World can move off-screen and show lasting readable costs (`pending`) [living_world] [series]
- [ ] `ux_backstory_legacy_integration` — Backstory and legacies can hook into play and chronicle (`pending`) [table] [series]
- [ ] `ux_world_authorship_modability` — Table and community can author world change via curated and mod contracts (`pending`) [living_world] [series]
- [ ] `ux_absent_proxy` — Absent-player proxy (`pending`) [inhabit] [coverage]
- [ ] `ux_agency_handoff_enter_exit` — Agency enter / exit handoff feel (`pending`) [inhabit] [coverage]
- [ ] `ux_baseline_fp` — Baseline first-person embodiment (`pending`) [inhabit] [coverage]
- [ ] `ux_baseline_fp_controls` — Baseline FP controls (`pending`) [inhabit] [coverage]
- [ ] `ux_class_chrome_discovery` — Class / identity chrome discovery (`pending`) [inhabit] [coverage]
- [ ] `ux_divination_override` — Divination / remote-sense override (`pending`) [inhabit] [coverage]
- [ ] `ux_dm_mapcam` — DM MapCam (`pending`) [inhabit] [coverage]
- [ ] `ux_dm_pilot` — DM pilot (agency, not Sensorium) (`pending`) [inhabit] [coverage]
- [ ] `ux_dm_sensorium` — DM Sensorium Attach (`pending`) [inhabit] [coverage]
- [ ] `ux_dm_worldcam` — DM WorldCam (`pending`) [inhabit] [coverage]
- [ ] `ux_dominate_pilot` — Dominate / pilot (controller) (`pending`) [inhabit] [coverage]
- [ ] `ux_dominate_victim` — Dominate victim / passenger overlay (`pending`) [inhabit] [coverage]
- [ ] `ux_liminal_unconscious` — Liminal / unconscious presentation (`pending`) [inhabit] [coverage]
- [ ] `ux_planar_travel_override` — Planar / gate travel override (`pending`) [inhabit] [coverage]
- [ ] `ux_combat_cast_feedback` — Combat / cast sensory feedback (`pending`) [inhabit] [coverage]
- [ ] `ux_chronicle_buckets` — Chronicle data buckets (`pending`) [table] [coverage]
- [ ] `ux_dm_workbench_lore_gui` — DM workbench lore GUI (`pending`) [table] [coverage]
- [ ] `ux_player_lite_lore_gui` — Player-lite lore GUI (`pending`) [table] [coverage]
- [ ] `ux_session0_bootstrap` — Session 0 bootstrap feel (`pending`) [table] [coverage]
- [ ] `ux_tone_profile_surface` — Campaign tone profile surface (`pending`) [table] [coverage]
- [ ] `ux_canon_pipeline_feel` — Canon pipeline feel (`pending`) [living_world] [coverage]
- [ ] `ux_economy_resources` — Resource distribution visibility (`pending`) [living_world] [coverage]
- [ ] `ux_economy_trade` — Trade routes / market pressure (`pending`) [living_world] [coverage]
- [ ] `ux_quest_pressure_surface` — Quest pressure from canon (`pending`) [living_world] [coverage]
- [ ] `ux_wa_faction_goals` — Faction goals / agenda surface (`pending`) [living_world] [coverage]
- [ ] `ux_wa_faction_hierarchy` — Faction hierarchy surface (`pending`) [living_world] [coverage]
- [ ] `ux_wa_faction_offscreen` — Off-screen faction activity (`pending`) [living_world] [coverage]
- [ ] `ux_wa_faction_reputation` — Reputation standing surface (`pending`) [living_world] [coverage]
- [ ] `ux_wa_lore_articles` — Lore codex / articles (`pending`) [living_world] [coverage]
- [ ] `ux_wa_npc_agenda` — NPC agenda / schedule visibility (`pending`) [living_world] [coverage]
- [ ] `ux_wa_npc_relations` — NPC relationship web (`pending`) [living_world] [coverage]
- [ ] `ux_wa_npc_secrets` — NPC secrets / knowledge gates (`pending`) [living_world] [coverage]
- [ ] `ux_wa_npc_sheet` — NPC identity sheet feel (`pending`) [living_world] [coverage]
- [ ] `ux_wa_timelines` — Timeline / era threads (`pending`) [living_world] [coverage]
- [ ] `ux_worldgen_gui` — Worldgen GUI (`pending`) [living_world] [coverage]
- [ ] `ux_sim_weather_pulse` — Weather / ambient sim pulse (`pending`) [living_world] [coverage]
- [ ] `ux_wa_faction_territory` — Faction territory / influence (`pending`) [living_world] [coverage]
- [ ] `ux_wa_locations` — Location surfaces (`pending`) [living_world] [coverage]
- [ ] `ux_wa_maps_vs_embodied` — Maps vs embodied discovery (`pending`) [living_world] [coverage]
- [ ] `ux_wa_npc_dialogue_hooks` — NPC dialogue / roleplay hooks (`pending`) [living_world] [coverage]
- [ ] `ux_application_shell` — Application shell / layout chrome (`pending`) [surfaces] [coverage]
- [ ] `ux_primary_navigation` — Primary navigation / wayfinding (`pending`) [flows] [coverage]
- [ ] `ux_session_onboarding` — Session / onboarding bootstrap (`pending`) [flows] [coverage]
- [ ] `ux_content_authoring_surface` — Content authoring surface (`pending`) [content] [coverage]
- [ ] `ux_dm_soft_framing_tools` — DM soft framing tools (`pending`) [inhabit] [thickener]
- [ ] `ux_escape_as_first_authorship` — Escape as first authorship (`pending`) [inhabit] [thickener]
- [ ] `ux_flee_as_authorship_combat_end` — Flee-as-authorship combat end (`pending`) [inhabit] [thickener]
- [ ] `ux_incomplete_information_before_blood` — Incomplete information before blood (`pending`) [inhabit] [thickener]
- [ ] `ux_wake_in_violation_open` — Wake-in-violation open (`pending`) [inhabit] [thickener]
- [ ] `ux_who_to_sit_with_tonight` — Who to sit with tonight (`pending`) [inhabit] [thickener]
- [ ] `ux_beautiful_rooms_in_a_cruel_place` — Beautiful rooms in a cruel place (`pending`) [table] [thickener]
- [ ] `ux_city_scale_panic_texture` — City-scale panic texture (`pending`) [table] [thickener]
- [ ] `ux_costly_identity_pact_after_a_death` — Costly identity pact after a death (`pending`) [table] [thickener]
- [ ] `ux_cure_that_harms` — Cure that harms (`pending`) [table] [thickener]
- [ ] `ux_empty_chair_fracture` — Empty-chair fracture (`pending`) [table] [thickener]
- [ ] `ux_estranged_home_social_ordeal` — Estranged-home social ordeal (`pending`) [table] [thickener]
- [ ] `ux_faith_shatter_at_the_machine` — Faith shatter at the machine (`pending`) [table] [thickener]
- [ ] `ux_fourth_option_social_agency` — Fourth-option social agency (`pending`) [table] [thickener]
- [ ] `ux_guide_who_was_the_problem` — Guide who was the problem (`pending`) [table] [thickener]
- [ ] `ux_joy_ritual_beside_betrayal_beat` — Joy ritual beside betrayal beat (`pending`) [table] [thickener]
- [ ] `ux_linger_after_the_fight` — Linger after the fight (`pending`) [table] [thickener]
- [ ] `ux_moral_fork_that_schedules_the_next_fight` — Moral fork that schedules the next fight (`pending`) [table] [thickener]
- [ ] `ux_party_trust_under_ascension_pressure` — Party trust under ascension pressure (`pending`) [table] [thickener]
- [ ] `ux_personal_stakes_set_piece_combat` — Personal-stakes set-piece combat (`pending`) [table] [thickener]
- [ ] `ux_post_coma_blame_texture` — Post-coma blame texture (`pending`) [table] [thickener]
- [ ] `ux_post_kill_political_handoff` — Post-kill political handoff (`pending`) [table] [thickener]
- [ ] `ux_power_object_that_demanded_a_person_not_a_check` — Power object that demanded a person, not a check (`pending`) [table] [thickener]
- [ ] `ux_rehabilitation_bargain_after_betrayal` — Rehabilitation bargain after betrayal (`pending`) [table] [thickener]
- [ ] `ux_rescue_as_social_contract` — Rescue as social contract (`pending`) [table] [thickener]
- [ ] `ux_rest_as_presence_not_only_refill` — Rest as presence, not only refill (`pending`) [table] [thickener]
- [ ] `ux_sibling_panic_in_the_quiet_after_the_roll` — Sibling panic in the quiet after the roll (`pending`) [table] [thickener]
- [ ] `ux_side_deal_mischief_beside_sincere_pain` — Side-deal mischief beside sincere pain (`pending`) [table] [thickener]
- [ ] `ux_soft_power_party_seizure` — Soft-power party seizure (`pending`) [table] [thickener]
- [ ] `ux_spare_or_swear_companion_crisis` — Spare-or-swear companion crisis (`pending`) [table] [thickener]
- [ ] `ux_triage_under_asymmetric_power` — Triage under asymmetric power (`pending`) [table] [thickener]
- [ ] `ux_trial_dungeon_that_ends_in_loyalty` — Trial dungeon that ends in loyalty (`pending`) [table] [thickener]
- [ ] `ux_who_owns_the_ending` — Who owns the ending (`pending`) [table] [thickener]
- [ ] `ux_earned_conspiracy_payoff` — Earned conspiracy payoff (`pending`) [living_world] [thickener]
- [ ] `ux_earned_spy_reveal` — Earned spy reveal (`pending`) [living_world] [thickener]
- [ ] `ux_friend_who_was_the_conspiracy` — Friend who was the conspiracy (`pending`) [living_world] [thickener]
- [ ] `ux_living_world_remembers_without_a_script` — Living-world remembers without a script (`pending`) [living_world] [thickener]
- [ ] `ux_quiet_level_acknowledgment` — Quiet level acknowledgment (`pending`) [living_world] [thickener]
- [ ] `ux_campfire_identity_chrome` — Campfire identity chrome (`pending`) [surfaces] [thickener]
- [ ] `ux_chrome_that_grew_with_you` — Chrome that grew with you (`pending`) [surfaces] [thickener]
- [ ] `ux_diegetic_chrome_persistence` — Diegetic chrome persistence (`pending`) [surfaces] [thickener]
- [ ] `ux_feedback_anchored_to_the_body` — Feedback anchored to the body (`pending`) [surfaces] [thickener]
- [ ] `ux_logistics_of_a_missing_seat` — Logistics of a missing seat (`pending`) [surfaces] [thickener]
- [ ] `ux_new_toy_in_the_next_fight` — New toy in the next fight (`pending`) [surfaces] [thickener]
- [ ] `ux_power_trophy_that_the_table_can_feel` — Power trophy that the table can feel (`pending`) [surfaces] [thickener]
- [ ] `ux_region_map_for_a_social_beat` — Region map for a social beat (`pending`) [surfaces] [thickener]
- [ ] `ux_title_reclaim_as_identity_chrome` — Title reclaim as identity chrome (`pending`) [surfaces] [thickener]
- [ ] `ux_verb_first_soft_exit` — Verb-first soft exit (`pending`) [surfaces] [thickener]
- [ ] `ux_class_chrome` — Class / subclass chrome (`pending`) [supplement] [thickener]
- [ ] `ux_dm_player_rails` — DM / player rails (`pending`) [supplement] [thickener]
- [ ] `ux_dmpausegate_interaction` — DMPauseGate interaction (`pending`) [supplement] [thickener]
- [ ] `ux_feedback_payload_composition_demo_truncated` — Feedback payload composition (demo-truncated) (`pending`) [supplement] [thickener]
- [ ] `ux_launch_playregion_hud_flow` — Launch → PlayRegion → HUD flow (`pending`) [supplement] [thickener]
- [ ] `ux_operator_dm_rail_hotkey_vs_scripted_cue` — Operator DM rail hotkey vs scripted cue (`pending`) [supplement] [thickener]
- [ ] `ux_perspectiveenvelope_player_fp_activation` — PerspectiveEnvelope `player_fp` activation (`pending`) [supplement] [thickener]
- [ ] `ux_player_agency_loop` — Player agency loop (`pending`) [supplement] [thickener]
- [ ] `ux_playerfprig_attachment` — PlayerFPRig attachment (`pending`) [supplement] [thickener]
- [ ] `ux_presentation_shell` — Presentation shell (`pending`) [supplement] [thickener]
- [ ] `ux_rule_representation` — Rule representation (`pending`) [supplement] [thickener]
- [ ] `ux_scry_presentation` — Scry / Clairvoyance presentation (`pending`) [supplement] [thickener]
- [ ] `ux_session0_identity_art` — Session 0 / identity art (`pending`) [supplement] [thickener]

## Items

### `ux_world_generation` — DM can create (table can shape) a persistent living world

- status: done
- walk_tier: series
- series_id: lifecycle
- series_order: 0
- altitude: product_contract
- seat: ["shared_table", "dm_as_player", "privileged_access"]
- time_scale: world_era
- does_not_mandate: ["one world equals exactly one campaign forever", "worldgen is only a Session 0 checkbox with no persistent container", "players author the first world", "world create forces unconstrained multi-knob fresh-noise every time", "world creation's default next step is player character creation"]
- alternatives_not_banned: ["Nth campaign in a long-lived world vs first campaign in a newly wizard-created world", "Thin shape+preview accept vs deeper multi-step wizard on first create", "Import vs in-tool wizard-create only", "World empty of campaigns vs world carrying prior scars/legacies", "Directional world-tone × campaign-tone combinations", "Adaptation heavy vs light (still always DM-gated and retconnable)"]
- catalog_face: living_world
- experience_mode: world_generation
- mode_tier: series
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: world_gen
- summary: Durable world container — DM creates initial form via wizard+preview; table can shape; players do not author the first world. Physical/settlement layers + monster-region tags; import/attach; DM retcon on any world-hitting change.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:world_generation
- ux_family: lifecycle
- supplement: False
- coverage_slot: False
- notes: applied:2026-07-30T05:32:23Z receipt=Mint-Receipts/ux_world_generation.receipt.yaml l5=scopes/ux_world_generation/L5.md

### `ux_dm_campaign_creation` — DM can bootstrap a campaign frame inside a world

- status: done
- walk_tier: series
- series_id: lifecycle
- series_order: 1
- altitude: product_contract
- seat: ["dm_as_player", "privileged_access"]
- time_scale: campaign
- does_not_mandate: ["every campaign begins in captivity", "offline Microscope play is required before Session 0", "starting a campaign must regenerate the whole world", "campaign creation's default next step is player character creation", "DM is the primary author of player characters after frame bootstrap"]
- alternatives_not_banned: ["Second campaign in a long-lived world vs first campaign in a new world", "Thin collaborative seed (table proposes; DM accepts) vs DM-solo then reveal public slice", "Minimal quick-start frame vs deep Session 0 on top of an existing world"]
- catalog_face: table
- experience_mode: dm_campaign_creation
- mode_tier: series
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: Orchestrator creates or revises a campaign frame (tone, bounds, public facts, cast expectations, logging seam) as a player-facing authorship act inside an existing or newly attached world — not the world container itself. Exit to world or session prep; not player character creation.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:dm_campaign_creation
- ux_family: lifecycle
- supplement: False
- coverage_slot: False
- notes: applied:2026-07-30T05:32:23Z receipt=Mint-Receipts/ux_dm_campaign_creation.receipt.yaml l5=scopes/ux_dm_campaign_creation/L5.md apply_after_met=ux_world_generation

### `ux_player_character_creation` — Players can author characters and submit them for DM acceptance into a world

- status: done
- walk_tier: series
- series_id: lifecycle
- series_order: 2
- altitude: product_contract
- seat: ["player", "shared_table"]
- time_scale: campaign
- does_not_mandate: ["characters must start with a stolen-agency wound", "backstory is only flavor text with no play hooks", "ownership transfers to the DM on greenlight", "character creation requires a separate draft object type", "players may only build inside an open campaign invite"]
- alternatives_not_banned: ["Unbound build then later invite vs build only into an open invite", "Hard greenlight vs return-with-notes / overwrite negotiation", "One-campaign binding vs later invite into another campaign in the same world", "Minimal builder vs richer chrome after legality is solid", "Aligned vs divergent world/campaign option sets"]
- catalog_face: table
- experience_mode: player_character_creation
- mode_tier: series
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: Player authors and owns a character before and after DM greenlight. Builds may be unbound or against a campaign invite (entry into campaign and world); invited builds disable banned options from world and campaign configs with overwrite-request path. Accept flow: invite → attach → greenlight. Incomplete builds are unfinished characters, not a draft type. Background→world proposals stay DM-gated and retconnable.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:player_character_creation
- ux_family: lifecycle
- supplement: False
- coverage_slot: False
- notes: applied:2026-07-30T07:29:30Z receipt=Mint-Receipts/ux_player_character_creation.receipt.yaml l5=scopes/ux_player_character_creation/L5.md

### `ux_dm_session_prep` — DM can prep a session without leaving the collaborative table frame

- status: done
- walk_tier: series
- series_id: lifecycle
- series_order: 3
- altitude: product_contract
- seat: ["dm_as_player", "privileged_access"]
- time_scale: session
- does_not_mandate: ["prep must be a separate offline app", "players never see any prep residue", "all prep material is public by default", "prep is a back door around DM gate/retcon on world changes", "session prep creates or replaces the world or campaign frame", "visibility is only a single whole-table tag with no per-player option"]
- alternatives_not_banned: ["Thin author notes vs rich structured beats (system still stages)", "Mostly secret with selective reveals vs broader general tags", "Prep mode distinct vs prep panels on the DM rail during downtime", "Batch applied on complete vs batch held for DM confirm in world-gen"]
- catalog_face: table
- experience_mode: dm_session_prep
- mode_tier: series
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: DM authors the next shared session experience in-tool; the system auto-stages against the attached world and campaign. Visibility is opt-in: general (whole-table) and/or per-player tags; unmarked stays secret. World-hitting edits batch and hand off into world-gen on prep complete under the same DM gate and retcon rules. Privileged orchestrator seat — not offline admin or invisible infrastructure.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:dm_session_prep
- ux_family: lifecycle
- supplement: False
- coverage_slot: False
- notes: applied:2026-07-30T07:41:00Z amended:2026-07-30T18:37:43Z visibility=general+per-player; no char-create exit refrain

### `ux_game_start` — Table can start play under a chosen campaign-start structure

- status: dropped
- walk_tier: coverage
- altitude: experience_texture
- seat: ["shared_table"]
- time_scale: session
- does_not_mandate: ["every campaign begins in captivity", "tavern opens must secretly be prisons", "session open is a separate series product noun from prep"]
- alternatives_not_banned: []
- catalog_face: table
- experience_mode: game_start
- mode_tier: coverage
- dnd_pillar: shared
- ux_axis: agency
- dimension: session_bootstrap
- summary: DEMOTE: opening situation / start structure / situational constraints fold into ux_dm_session_prep. Enter-live-play is shell (Play readiness), not a series peer. Do not mint as product_contract series parent.
- conceptual_pin: needs pin
- derived_from: demoted_from:series:lifecycle:game_start
- ux_family: lifecycle
- supplement: True
- coverage_slot: True
- maps_to: ux_dm_session_prep
- notes: demoted:2026-07-30T19:10:59Z maps_to=ux_dm_session_prep; enter_play→shell/nav; reason=opening_is_prep_authorship

### `ux_early_game` — Early play is a power band that gates world and pillar response

- status: done
- walk_tier: series
- series_id: lifecycle
- series_order: 4
- altitude: product_contract
- seat: ["shared_table"]
- time_scale: session
- does_not_mandate: ["the only correct ending is institutional seizure", "end game must erase player legacies"]
- alternatives_not_banned: ["Implicit band (content only) vs visible band indicator", "Strict gates vs soft advice the DM can override", "Fast climb out of early vs long stay in band", "Prep-authored early situations vs mostly emergent within band limits"]
- catalog_face: flows
- experience_mode: early_game
- mode_tier: series
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Early-game is the low power band for the cast: world access, social audience, explore pressure, and combat offer scale to that band. Pillar rhythm follows the band rather than a second axis. Not a tutorial plot, not session prep, and not a mandatory onboarding fantasy. Mid/end stages own their bands the same way — no parallel progression parent.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:early_game
- ux_family: lifecycle
- supplement: False
- coverage_slot: False
- notes: applied:2026-07-30T19:16:52Z power_band_on_stages; receipt=Mint-Receipts/ux_early_game.receipt.yaml

### `ux_mid_game` — Mid play is a power band for lasting pressure and deeper world response

- status: done
- walk_tier: series
- series_id: lifecycle
- series_order: 5
- altitude: product_contract
- seat: ["shared_table"]
- time_scale: campaign
- does_not_mandate: ["mid game requires a companion romance track", "mid game must center a single conspiracy reveal", "progression requires a separate series parent from stage bands", "session prep replaces the mid power-band contract", "one CR/BG mid-arc skin is the product default"]
- alternatives_not_banned: ["Soft vs strict band gates (DM override)", "Long mid band vs fast transit", "Consequence-heavy mid vs access-heavy mid", "Visible band indicator vs implicit through content"]
- catalog_face: living_world
- experience_mode: mid_game
- mode_tier: series
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Mid-game is the middle power band: world access, social tier, explore stakes, and combat offer scale up with it — including who will engage and what costs can stick. Lasting pressure and party authorship are capabilities in this band, not one mandated conspiracy or romance skin. Pillar rhythm follows the band. Same ownership model as early: stages own the band; no parallel progression parent.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:mid_game
- ux_family: lifecycle
- supplement: False
- coverage_slot: False
- notes: applied:2026-07-30T19:21:51Z depends_on=ux_early_game; receipt=Mint-Receipts/ux_mid_game.receipt.yaml

### `ux_end_game` — Table can author campaign close and ending ownership

- status: pending
- walk_tier: series
- series_id: lifecycle
- series_order: 6
- altitude: product_contract
- seat: ["shared_table", "dm_as_player"]
- time_scale: campaign
- does_not_mandate: ["the only correct ending is institutional seizure", "end game must erase player legacies"]
- alternatives_not_banned: []
- catalog_face: table
- experience_mode: end_game
- mode_tier: series
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: End-game structures for who owns the ending and what persists — menu of closes, not one mandatory mythic finale.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:end_game
- ux_family: lifecycle
- supplement: False
- coverage_slot: False
- notes: power_band_on_stage_rows:true

### `ux_mental_stat_interpretation` — Mental stats can surface as readable interpretation not only numbers

- status: pending
- walk_tier: series
- series_id: lifecycle
- series_order: 7
- altitude: product_contract
- seat: ["shared_table"]
- time_scale: moment
- does_not_mandate: ["mental stats unlock a single romance dialogue tree", "low mental stats hide all social information"]
- alternatives_not_banned: []
- catalog_face: surfaces
- experience_mode: mental_stat_interpretation
- mode_tier: series
- dnd_pillar: roleplay
- ux_axis: agency
- dimension: ui_surface
- summary: Capability for mental-stat driven hints, social temperature, and perception texture as structure menus — not one episode's insight beat.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:mental_stat_interpretation
- ux_family: lifecycle
- supplement: False
- coverage_slot: False

### `ux_collaborative_table_agency` — Every seat is a player including the DM orchestrator

- status: pending
- walk_tier: series
- series_id: pmg_capabilities
- series_order: 0
- altitude: product_contract
- seat: ["shared_table", "dm_as_player", "privileged_access"]
- time_scale: session
- does_not_mandate: ["DM is only a cue issuer for other players", "players and DM share identical control envelopes"]
- alternatives_not_banned: []
- catalog_face: table
- experience_mode: collaborative_table_agency
- mode_tier: series
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Multiplayer collaborative storytelling with curated world-control tools; DM has privileged access and a different seat, and their fun is in-product — they are not system infrastructure.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:collaborative_table_agency
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_quiet_between_pillars` — Downtime keeps continuous fiction between combat social and explore

- status: pending
- walk_tier: series
- series_id: pmg_capabilities
- series_order: 1
- altitude: product_contract
- seat: ["shared_table"]
- time_scale: session
- does_not_mandate: ["downtime equals BG3 campsite companion UI", "quiet is only a long-rest resource refill"]
- alternatives_not_banned: []
- catalog_face: table
- experience_mode: quiet_between_pillars
- mode_tier: series
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Quiet-between is designed product surface — linger, camp, road — not a rest button or loading state alone.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:quiet_between_pillars
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_combat_play_surface` — Combat can resolve by authored paths including non-win ends

- status: pending
- walk_tier: series
- series_id: pmg_capabilities
- series_order: 2
- altitude: product_contract
- seat: ["shared_table"]
- time_scale: moment
- does_not_mandate: ["flee is the only correct authored end", "combat always resolves to XP loot chrome"]
- alternatives_not_banned: []
- catalog_face: inhabit
- experience_mode: combat_play_surface
- mode_tier: series
- dnd_pillar: combat
- ux_axis: combat_cast_feedback
- dimension: ui_surface
- summary: Combat authorship menu (fight, flee, parley, stakes) as product contract — not one flee-or-die caption.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:combat_play_surface
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_camera_control_envelopes` — Perspective and control envelopes can change and cleanly return

- status: pending
- walk_tier: series
- series_id: pmg_capabilities
- series_order: 3
- altitude: product_contract
- seat: ["player", "dm_as_player", "privileged_access"]
- time_scale: moment
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure"]
- alternatives_not_banned: []
- catalog_face: inhabit
- experience_mode: camera_control_envelopes
- mode_tier: series
- dnd_pillar: shared
- ux_axis: perspective_overrides
- dimension: player_rail
- summary: FP baseline, rules-bound overrides, pilots, and DM WorldCam/MapCam/Sensorium as experiential seats with enter/exit — privileged DM tools included, orchestrator fun considered.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:camera_control_envelopes
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_living_world_continuity` — World can move off-screen and show lasting readable costs

- status: pending
- walk_tier: series
- series_id: pmg_capabilities
- series_order: 4
- altitude: product_contract
- seat: ["shared_table", "dm_as_player"]
- time_scale: campaign
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts"]
- alternatives_not_banned: []
- catalog_face: living_world
- experience_mode: living_world_continuity
- mode_tier: series
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Living-world continuity contract — factions, threads, visible lasting costs — without mandating one conspiracy skin.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:living_world_continuity
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_backstory_legacy_integration` — Backstory and legacies can hook into play and chronicle

- status: pending
- walk_tier: series
- series_id: pmg_capabilities
- series_order: 5
- altitude: product_contract
- seat: ["shared_table", "player"]
- time_scale: campaign
- does_not_mandate: ["every backstory forces a mid-game reunion ordeal", "legacies are DM-only lore with no player surface"]
- alternatives_not_banned: []
- catalog_face: table
- experience_mode: backstory_legacy_integration
- mode_tier: series
- dnd_pillar: roleplay
- ux_axis: class_chrome
- dimension: ui_surface
- summary: Personal and table legacies surface in play and player-lite chronicle — structure menu for how hooks appear, not one CR identity pact.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:backstory_legacy_integration
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_world_authorship_modability` — Table and community can author world change via curated and mod contracts

- status: pending
- walk_tier: series
- series_id: pmg_capabilities
- series_order: 6
- altitude: product_contract
- seat: ["shared_table", "dm_as_player", "privileged_access"]
- time_scale: world_era
- does_not_mandate: ["mods are post-1.0 only", "timeline editing is player-lite default"]
- alternatives_not_banned: []
- catalog_face: living_world
- experience_mode: world_authorship_modability
- mode_tier: series
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: Session 0, timelines/eras, factions, intentional re-gen, and modability as first-class authorship — Microscope-informed non-linear history welcome.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:world_authorship_modability
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_absent_proxy` — Absent-player proxy

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: absent_proxy
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Delegate pilots an absent PC with explicit handoff when the owner returns. Feedstock: …andidates - label: Soft-power party seizure summary: A living companion removed by law/magic, not HP. - label: Rescue as social contract summary: The table re-forms around getting them back. ## maps_to_taxonomy - absent_proxy / agency_handoff_enter_exit - dm_workbench_lore_gui / wa_faction_hierarchy Pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- ux_family: absent_proxy
- supplement: True
- coverage_slot: True

### `ux_agency_handoff_enter_exit` — Agency enter / exit handoff feel

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: agency_handoff_enter_exit
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Shared choreography when control or perspective transfers and cleanly returns. Feedstock: …ft-power party seizure summary: A living companion removed by law/magic, not HP. - label: Rescue as social contract summary: The table re-forms around getting them back. ## maps_to_taxonomy - absent_proxy / agency_handoff_enter_exit - dm_workbench_lore_gui / wa_faction_hierarchy
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- ux_family: agency_handoff_enter_exit
- supplement: True
- coverage_slot: True

### `ux_baseline_fp` — Baseline first-person embodiment

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: baseline_fp
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Default embodied play — what the human sees and touches in this pillar. Feedstock: # Genesis Mythos Master Goal ## One-line Build an open-source, monetizable, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM and player intents — mandatory in-tool session 0, visible world continuity, player-lite legacies and chronicle — players in fir… Pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: baseline_embodiment
- supplement: True
- coverage_slot: True

### `ux_baseline_fp_controls` — Baseline FP controls

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: baseline_fp_controls
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: How move, look, and intent issuance feel and where control surfaces sit relative to first-person view. Feedstock: # Genesis Mythos Master Goal ## One-line Build an open-source, monetizable, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM and player intents — mandatory in-tool session 0, visible world continuity, player-lite legacies and chronicle — players in fir…
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: baseline_fp_controls
- supplement: True
- coverage_slot: True

### `ux_class_chrome_discovery` — Class / identity chrome discovery

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: class_chrome_discovery
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: class_chrome
- dimension: ui_surface
- summary: How class or identity polish is noticed and used without leaving the embodied moment. Feedstock: …Companions/world notice growth without a banner-only UI. - label: New toy in the next fight summary: Progression that changes the next combat verb, felt immediately. - label: Chrome that grew with you summary: Class identity polish that tracks ordinary advancement. ## maps_to_taxonomy - class_chrome_discovery / combat_cast_feedback - session0_bootstrap / tone_profile_surface - baseline_fp
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- ux_family: class_chrome_discovery
- supplement: True
- coverage_slot: True

### `ux_divination_override` — Divination / remote-sense override

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: divination_override
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: perspective_overrides
- dimension: ui_surface
- summary: Temporary rules-bound departure from baseline FP for remote sensing (scry, clairvoyance, find path, and kin). Feedstock: …n for players and commanding mastery for the DM. - **Players default to first-person** — immediate, personal, experiential. No casual third-person orbit or free tactical camera for players. - **Perspective overrides** (Scry/Clairvoyance, divination, astral travel, DM-granted visions, unconscious/liminal states, etc.) are **explicit, temporary, rules-bound** departures from baseline FP — not a permanent camera mode. Overrides use contract-d… Pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: divination_overrides
- supplement: True
- coverage_slot: True

### `ux_dm_mapcam` — DM MapCam

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: dm_mapcam
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Map-fixed orthographic DM rail — tokens, measurements, fog, LOS adjudication feel. Feedstock: …tool session 0, visible world continuity, player-lite legacies and chronicle — players in first-person by default with rules-driven perspective and agency envelopes, DMs on a dedicated rail (WorldCam, map-fixed Tabletop MapCam, read-only Sensorium Attach), player lore woven into systemic depth, major structural changes via intentional re-generation, every layer built for community remixing. ## Vision **Perspective split** delivers immersion… Pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: dm_observe_rails
- supplement: True
- coverage_slot: True

### `ux_dm_pilot` — DM pilot (agency, not Sensorium)

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: dm_pilot
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: dm_rail
- summary: When session/rules put the DM in control of an entity via pilot envelope. Feedstock: …ey see?” — **no intent/control transfer** on the DM rail. Compare multiple viewpoints for ruling. Operator debug attach uses the same read-only contract. Always **exit back** to prior DM mode (WorldCam or MapCam). - **DM pilot** — when rules or session policy puts the DM in control of an entity (e.g. NPC dominate, absent PC), that uses the **agency delegation** system (pilot envelope), not Sensorium Attach. DM may pilot with FP from that body…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: dm_pilot
- supplement: True
- coverage_slot: True

### `ux_dm_sensorium` — DM Sensorium Attach

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: dm_sensorium
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Read-only sight bind to an entity — no intent transfer; adjudicate what they see. Feedstock: …re that lands because the player assembled it. - label: Guide who was the problem summary: Narrator/ally trust collapse without removing player agency. ## maps_to_taxonomy - wa_npc_secrets / canon_pipeline_feel - dm_sensorium / divination_override Pillars: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode).
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- ux_family: dm_observe_rails
- supplement: True
- coverage_slot: True

### `ux_dm_worldcam` — DM WorldCam

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: dm_worldcam
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Free-flight DM observation rail — how mastery feels in this pillar. Feedstock: …texture summary: How inhabit/table feel when the map itself is the enemy. - label: Triage under asymmetric power summary: Choosing who to carry when you cannot save the day. ## maps_to_taxonomy - baseline_fp / dm_worldcam - absent_proxy / agency_handoff_enter_exit - quest_pressure_surface / sim_weather_pulse Pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- ux_family: dm_observe_rails
- supplement: True
- coverage_slot: True

### `ux_dominate_pilot` — Dominate / pilot (controller)

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: dominate_pilot
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Dominator pilots the target — FP and control from the dominated body. Feedstock: # Felt moment (pattern language) Final hours ask **who owns the ending**: sacrifice, transform, free, dominate. Companions react; combat may resolve the social choice or follow it. Party trust under cosmic stakes. Digital D&D’s version of “the table decides what kind of story this was.” ## Spatial / temporal / control Climax a… Pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- ux_family: dominate_pilot
- supplement: True
- coverage_slot: True

### `ux_dominate_victim` — Dominate victim / passenger overlay

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: dominate_victim
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Victim presentation during dominate — passenger FP, locked input, liminal chrome. Feedstock: …where companions and combat hang on the choice. - label: Party trust under ascension pressure summary: Social contract tested when power offers an exit from humanity. ## maps_to_taxonomy - dominate_pilot / dominate_victim - planar_travel_override - canon_pipeline_feel Pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- ux_family: victim_overlay
- supplement: True
- coverage_slot: True

### `ux_liminal_unconscious` — Liminal / unconscious presentation

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: liminal_unconscious
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: perspective_overrides
- dimension: ui_surface
- summary: Status-bound liminal or unconscious presentation and return to baseline. Feedstock: …un candidates - label: Cure that harms summary: Trusted procedure as betrayal of body and belief. - label: Faith shatter at the machine summary: Identity progression via institutional doubt. ## maps_to_taxonomy - liminal_unconscious / combat_cast_feedback - class_chrome_discovery - session0_bootstrap
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P04-institutional-faith-betrayal.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P04-institutional-faith-betrayal.md
- ux_family: liminal_states
- supplement: True
- coverage_slot: True

### `ux_planar_travel_override` — Planar / gate travel override

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: planar_travel_override
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: perspective_overrides
- dimension: ui_surface
- summary: How planar travel or gate-like transitions feel as temporary perspective/agency departures. Feedstock: …(victim)** — dominated PC: presentation policy is spell-bound (e.g. passenger FP with locked input, liminal UI); exact default locked at Phase 5 spell metadata. - **Absent-player proxy** — session policy allows a delegate (another player or DM) to **pilot** an absent PC with explicit handoff when the owner returns. - **Enter/exit** — every delegation declares controller, victim presentation, duration, and clean return to `agency: self`… Pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: planar_travel_overrides
- supplement: True
- coverage_slot: True

### `ux_combat_cast_feedback` — Combat / cast sensory feedback

- status: pending
- walk_tier: coverage
- catalog_face: inhabit
- experience_mode: combat_cast_feedback
- mode_tier: multi_pillar
- dnd_pillar: combat
- ux_axis: combat_cast_feedback
- dimension: ui_surface
- summary: Cast and hit sensory response the player notices — not damage formulas. Feedstock: # Felt moment (pattern language) Phenomenology is not enough until it names **where the body meets the product**. For every major feel (camp talk, flee authorship, moral fork, cast feedback), the catalog must force later pseudo-code to answer: - **Screen region** — corner chrome, center stage, diegetic world, modal, or off-screen audio - **Persistence** — always-on identity chrome vs ephemeral prompt vs c…
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- ux_family: combat_cast_feedback
- supplement: True
- coverage_slot: True

### `ux_chronicle_buckets` — Chronicle data buckets

- status: pending
- walk_tier: coverage
- catalog_face: table
- experience_mode: chronicle_buckets
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Keep world ripples, session chronicle, and personal archive distinct in UX. Feedstock: …abel: Side-deal mischief beside sincere pain summary: Continuous fiction holding comedy theft and family grief in one session. ## maps_to_taxonomy - session0_bootstrap / tone_profile_surface - player_lite_lore_gui / chronicle_buckets - agency_handoff_enter_exit
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- ux_family: chronicle_buckets
- supplement: True
- coverage_slot: True

### `ux_dm_workbench_lore_gui` — DM workbench lore GUI

- status: pending
- walk_tier: coverage
- catalog_face: table
- experience_mode: dm_workbench_lore_gui
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Canon graph, accept/revise intents, faction off-screen, quest-hook integration UI. Feedstock: …since you left…”) · **Last session** recap · **My chronicle** (personal notes by session, search) · optional export/mirror for note-taking players. **Not** timeline editing, contradiction resolution, or sim admin. | | **DM workbench** | Full canon graph, faction/tribe off-screen activity, accept/revise intents, quest integration from active hooks. | Keep three **data buckets** distinct in UX: **world ripples** (system/DM canon) · **session chronic…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: dm_workbench_lore_gui
- supplement: True
- coverage_slot: True

### `ux_player_lite_lore_gui` — Player-lite lore GUI

- status: pending
- walk_tier: coverage
- catalog_face: table
- experience_mode: player_lite_lore_gui
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Intent inbox, Legacies, last-session recap, personal chronicle — not sim admin. Feedstock: …rce, monetizable, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM and player intents — mandatory in-tool session 0, visible world continuity, player-lite legacies and chronicle — players in first-person by default with rules-driven perspective and agency envelopes, DMs on a dedicated rail (WorldCam, map-fixed Tabletop MapCam, read-only Sensorium Attach), player lore wove…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: player_lite_lore_gui
- supplement: True
- coverage_slot: True

### `ux_session0_bootstrap` — Session 0 bootstrap feel

- status: pending
- walk_tier: coverage
- catalog_face: table
- experience_mode: session0_bootstrap
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: In-tool session 0 — bounds, tone pick, intent propose, table accept/revise. Feedstock: …Goal ## One-line Build an open-source, monetizable, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM and player intents — mandatory in-tool session 0, visible world continuity, player-lite legacies and chronicle — players in first-person by default with rules-driven perspective and agency envelopes, DMs on a dedicated rail (WorldCam, map-fixed Tabletop MapCam, read-o…
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: session0_bootstrap
- supplement: True
- coverage_slot: True

### `ux_tone_profile_surface` — Campaign tone profile surface

- status: pending
- walk_tier: coverage
- catalog_face: table
- experience_mode: tone_profile_surface
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: How the chosen tone biases chrome, previews, and felt world without siloed presets. Feedstock: …ts — so quests integrate with the world graph, not generic fetch loops. **Collaborative canon & session bootstrap.** - **Session 0 (required, in-tool):** world bootstrap before campaign play — table bounds, **campaign tone profile** (see below), player intents, DM/table accept or revise canon. Collaborative-history patterns (shared eras, legacies, non-linear threads) are **Microscope-informed** — see [[Ingest/Microscope PDF]] — **not** dependent…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: tone_profile_surface
- supplement: True
- coverage_slot: True

### `ux_canon_pipeline_feel` — Canon pipeline feel

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: canon_pipeline_feel
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: proposed → accepted → hooked → sim-active as human-facing states. Feedstock: …, legacies, non-linear threads) are **Microscope-informed** — see [[Ingest/Microscope PDF]] — **not** dependent on playing a separate RPG. Optional offline history may **import** as a canon bundle (power-user path). - **Canon pipeline:** `proposed → accepted → hooked → sim-active` — intents become facts, then systemic hooks, then visible ripples and quest pressure. **Campaign tone profiles** — one session-level vibe that biases every subsystem (Pale…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: canon_pipeline_feel
- supplement: True
- coverage_slot: True

### `ux_economy_resources` — Resource distribution visibility

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: economy_resources
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: What player/DM can see vs must discover about resources — not spreadsheet admin by default. Feedstock: …ial/explore. - label: Linger after the fight summary: Authored post-combat social/exploration residue before the next hook. - label: Rest as presence, not only refill summary: Long rest as camp identity layer, not a resource button alone. ## maps_to_taxonomy - session_onboarding / application_shell - player_lite_lore_gui / chronicle_buckets - sim_weather_pulse
- pillar_notes: exploration: mentioned in feedstock | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-quiet-between-pillars.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-quiet-between-pillars.md
- ux_family: economy_resources
- supplement: True
- coverage_slot: True

### `ux_economy_trade` — Trade routes / market pressure

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: economy_trade
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Trade and market pressure as world-continuity surfaces. Feedstock: # Felt moment (pattern language) The party suspects a friend is double-dealing. They **choose to look** (familiar spy, eavesdrop) and catch a disguised meeting. Truth lands: the ally traded sacred secrets for research ambition, then grew to care for the party against the original plan. The table must decide whether to destroy, use, or rehabilitate someone who lied. Players feel clever for connecting threa…
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- ux_family: economy_trade
- supplement: True
- coverage_slot: True

### `ux_quest_pressure_surface` — Quest pressure from canon

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: quest_pressure_surface
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How hooks appear in play and on the workbench — not fetch-only tables. Feedstock: …e RPG. Optional offline history may **import** as a canon bundle (power-user path). - **Canon pipeline:** `proposed → accepted → hooked → sim-active` — intents become facts, then systemic hooks, then visible ripples and quest pressure. **Campaign tone profiles** — one session-level vibe that biases every subsystem (Palette for *how* the world feels, not plot). Core set (**four only for now**; optional tags/modifiers deferred): | Profile | Vibe (re…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: quest_pressure_surface
- supplement: True
- coverage_slot: True

### `ux_wa_faction_goals` — Faction goals / agenda surface

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_faction_goals
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Faction goals and pressure as felt by player and DM. Feedstock: # Felt moment (pattern language) The party suspects a friend is double-dealing. They **choose to look** (familiar spy, eavesdrop) and catch a disguised meeting. Truth lands: the ally traded sacred secrets for research ambition, then grew to care for the party against the original plan. The table must decide whether to destroy, use, or rehabilitate someone who lied. Players feel clever for connecting threads — then responsible for the moral af…
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- ux_family: wa_faction_goals
- supplement: True
- coverage_slot: True

### `ux_wa_faction_hierarchy` — Faction hierarchy surface

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_faction_hierarchy
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Faction structure and ranks as browsable/playable continuity. Feedstock: # Felt moment (pattern language) Early in a digital D&D-like game, two factions ask for your blade. Choosing a side changes **who you fight**, who trusts you at camp, and which story threads stay open. The fork is not a dialogue checkbox only — the next combat encounter *is* the moral residue. Con…
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- ux_family: wa_faction_hierarchy
- supplement: True
- coverage_slot: True

### `ux_wa_faction_offscreen` — Off-screen faction activity

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_faction_offscreen
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Since-you-left deltas and off-screen faction pulse as human-facing continuity. Feedstock: …product**. For every major feel (camp talk, flee authorship, moral fork, cast feedback), the catalog must force later pseudo-code to answer: - **Screen region** — corner chrome, center stage, diegetic world, modal, or off-screen audio - **Persistence** — always-on identity chrome vs ephemeral prompt vs camp-only surface - **Input verbs** — look, approach, interrupt, soft-exit, commit, flee — not abstract “interact” - **Spatial feedback anchor**…
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- ux_family: wa_faction_offscreen
- supplement: True
- coverage_slot: True

### `ux_wa_faction_reputation` — Reputation standing surface

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_faction_reputation
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Reputation and consequence as surfaced to player vs DM. Feedstock: …giance rewrites the combat cast and camp trust. - label: Incomplete information before blood summary: Deciding with partial truth so regret and authorship coexist. ## maps_to_taxonomy - wa_faction_goals / wa_faction_reputation - baseline_fp / quest_pressure_surface
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- ux_family: wa_faction_reputation
- supplement: True
- coverage_slot: True

### `ux_wa_lore_articles` — Lore codex / articles

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_lore_articles
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: World lore articles as readable continuity distinct from personal chronicle. Feedstock: # Felt moment (pattern language) Mid/late game, the player connects breadcrumbs and learns who the **Chosen / conspiracy** really are — or that a trusted voice was shaping them. Lore dump feels earned because the player walked the map. Trust in narrator, dream-guide, or ally rewires. Digital cousin to table information scent. ## Spatial / temporal / control Colony / sanctum / dream space. Soft fra…
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- ux_family: wa_lore_articles
- supplement: True
- coverage_slot: True

### `ux_wa_npc_agenda` — NPC agenda / schedule visibility

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_npc_agenda
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Agenda and schedule as human-facing continuity — not raw sim tables. Feedstock: …DM canon) · **session chronicle** (table recap) · **personal archive** (player-owned notes — may disagree with canon). **The world pulses with life, customization, and balanced agency.** - Layered simulation: weather, NPC agendas, ambient surprises, persistent scars from play — **weighted by campaign tone profile**. - **DM overwrites:** in-session tweaks (tokens, weather, events, whispers) vs. deliberate re-generation for terrain reshaping or b…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: wa_npc_agenda
- supplement: True
- coverage_slot: True

### `ux_wa_npc_relations` — NPC relationship web

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_npc_relations
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How relationships among NPCs/factions are browsed and felt. Feedstock: …summary: Class and backstory felt as conversation, not menu. - label: Quiet between pillars summary: Designed downtime that keeps continuous fiction alive. - label: Who to sit with tonight summary: Soft agency over relationship temperature between quests. ## maps_to_taxonomy - session0_bootstrap / tone_profile_surface - class_chrome_discovery - application_shell / primary_navigation
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- ux_family: wa_npc_relations
- supplement: True
- coverage_slot: True

### `ux_wa_npc_secrets` — NPC secrets / knowledge gates

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_npc_secrets
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How hidden knowledge is gated and revealed without spoiling authoring vs play. Feedstock: # Felt moment (pattern language) A dungeon is structured as **tests** for a companion’s faith or order. Completing it can force a loyalty crisis: spare or sacrifice a person/secret the companion swore to. Exploration authorship (puzzles, paths) ends in a moral fork the party feels at camp afterward. Consequence lands mid-game, not at credits. ## Spatial / temporal / control Authored trial spaces…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- ux_family: wa_npc_secrets
- supplement: True
- coverage_slot: True

### `ux_wa_npc_sheet` — NPC identity sheet feel

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_npc_sheet
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: World Anvil–depth NPC identity surface — who they are at a glance in play/authoring. Feedstock: …hat ends in loyalty summary: Authored exploration whose boss is a relationship decision. - label: Spare-or-swear companion crisis summary: Party trust rewritten by one mid-campaign choice. ## maps_to_taxonomy - wa_npc_secrets / wa_npc_relations - canon_pipeline_feel - planar_travel_override (threshold metaphors)
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- ux_family: wa_npc_sheet
- supplement: True
- coverage_slot: True

### `ux_wa_timelines` — Timeline / era threads

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_timelines
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Eras and non-linear history threads as Microscope-informed continuity UX. Feedstock: …eed) · **My Legacies** (canon ripples — tribe status, threads, “since you left…”) · **Last session** recap · **My chronicle** (personal notes by session, search) · optional export/mirror for note-taking players. **Not** timeline editing, contradiction resolution, or sim admin. | | **DM workbench** | Full canon graph, faction/tribe off-screen activity, accept/revise intents, quest integration from active hooks. | Keep three **data buckets** dis…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: wa_timelines
- supplement: True
- coverage_slot: True

### `ux_worldgen_gui` — Worldgen GUI

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: worldgen_gui
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: presentation_shells
- dimension: world_gen
- summary: Collaborative generation dialogue — propose scaffolds, choose/refine, preview, accept/regenerate. Feedstock: …onflict | | **Grimdark** | Moral gray, harsh consequences (Witcher-like) | Bleak weather bias, costly hope, persistent scars | - `ToneProfile` — one bundled profile per campaign (chosen at session 0), consumed by **world gen**, **weather**, **sim defaults**, **lore/event tone**, and **quest framing** — not siloed presets per subsystem. - Profiles are **defaults**, not stereotypes; table Palette can veto elements. **Player & DM surfaces.**…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: worldgen_gui
- supplement: True
- coverage_slot: True

### `ux_sim_weather_pulse` — Weather / ambient sim pulse

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: sim_weather_pulse
- mode_tier: multi_pillar
- dnd_pillar: exploration
- ux_axis: agency
- dimension: sim_system
- summary: Tone-weighted weather and ambient world pulse as felt, not raw tick tables. Feedstock: …l: Triage under asymmetric power summary: Choosing who to carry when you cannot save the day. ## maps_to_taxonomy - baseline_fp / dm_worldcam - absent_proxy / agency_handoff_enter_exit - quest_pressure_surface / sim_weather_pulse
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- ux_family: sim_weather_pulse
- supplement: True
- coverage_slot: True

### `ux_wa_faction_territory` — Faction territory / influence

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_faction_territory
- mode_tier: multi_pillar
- dnd_pillar: exploration
- ux_axis: agency
- dimension: ui_surface
- summary: Territory and influence as map and embodied discovery. Feedstock: …log and attestation fail path; **PresentationSessionHandle** fields emitted at handoff; `presentation.launch_complete` bus contract; rollback on bootstrap failure. **Out of scope:** PlayRegion viewport mount (**6.1.2** territory); HUD layer stack (**6.1.3** territory); horizon demo spawn (**6.2**); factory vs demo glue (**6.3**); execution-track build pipeline CI wiring (execution-deferred / advisory). ## Behavior **Actors:** Player/operator…
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roll-up-2026-07-15.md
- derived_from: pin:1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roll-up-2026-07-15.md
- ux_family: wa_faction_territory
- supplement: True
- coverage_slot: True

### `ux_wa_locations` — Location surfaces

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_locations
- mode_tier: multi_pillar
- dnd_pillar: exploration
- ux_axis: agency
- dimension: world_gen
- summary: Locations as authoring and discovery surfaces. Feedstock: …ent surprises, persistent scars from play — **weighted by campaign tone profile**. - **DM overwrites:** in-session tweaks (tokens, weather, events, whispers) vs. deliberate re-generation for terrain reshaping or biome relocation. - Extensibility: swap simulation flavors, visual styles, rule behaviors, and **tone profiles** without breaking cohesion. **Open source and aggressive modularity** — every system (generation stages, simulation ticks,…
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: wa_locations
- supplement: True
- coverage_slot: True

### `ux_wa_maps_vs_embodied` — Maps vs embodied discovery

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_maps_vs_embodied
- mode_tier: multi_pillar
- dnd_pillar: exploration
- ux_axis: dm_player_rails
- dimension: ui_surface
- summary: When knowledge comes from map chrome vs first-person discovery. Feedstock: …ou at camp, and which story threads stay open. The fork is not a dialogue checkbox only — the next combat encounter *is* the moral residue. Consequence scent: the world remembers. ## Spatial / temporal / control Split map regions (sanctuary vs hostile camp). Attention on spokespeople then on the battlefield you unlocked. Soft framing via urgency and incomplete information. ## Experience noun candidates - label: Moral fork that schedule…
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- ux_family: wa_maps_vs_embodied
- supplement: True
- coverage_slot: True

### `ux_wa_npc_dialogue_hooks` — NPC dialogue / roleplay hooks

- status: pending
- walk_tier: coverage
- catalog_face: living_world
- experience_mode: wa_npc_dialogue_hooks
- mode_tier: multi_pillar
- dnd_pillar: roleplay
- ux_axis: agency
- dimension: ui_surface
- summary: How dialogue and roleplay hooks surface in the moment of play. Feedstock: …Felt moment (pattern language) Early in a digital D&D-like game, two factions ask for your blade. Choosing a side changes **who you fight**, who trusts you at camp, and which story threads stay open. The fork is not a dialogue checkbox only — the next combat encounter *is* the moral residue. Consequence scent: the world remembers. ## Spatial / temporal / control Split map regions (sanctuary vs hostile camp). Attention on spokespeople then o…
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- ux_family: wa_npc_dialogue_hooks
- supplement: True
- coverage_slot: True

### `ux_application_shell` — Application shell / layout chrome

- status: pending
- walk_tier: coverage
- catalog_face: surfaces
- experience_mode: application_shell
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: presentation_shells
- dimension: ui_surface
- summary: Baseline shell — screen regions, chrome placement, layout mapping for any product. Feedstock: …ction alive. - label: Who to sit with tonight summary: Soft agency over relationship temperature between quests. ## maps_to_taxonomy - session0_bootstrap / tone_profile_surface - class_chrome_discovery - application_shell / primary_navigation
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- ux_family: application_shell
- supplement: True
- coverage_slot: True

### `ux_primary_navigation` — Primary navigation / wayfinding

- status: pending
- walk_tier: coverage
- catalog_face: flows
- experience_mode: primary_navigation
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How users move between major areas — menus, routes, breadcrumbs, spatial wayfinding. Feedstock: …abel: Who to sit with tonight summary: Soft agency over relationship temperature between quests. ## maps_to_taxonomy - session0_bootstrap / tone_profile_surface - class_chrome_discovery - application_shell / primary_navigation
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- ux_family: primary_navigation
- supplement: True
- coverage_slot: True

### `ux_session_onboarding` — Session / onboarding bootstrap

- status: pending
- walk_tier: coverage
- catalog_face: flows
- experience_mode: session_onboarding
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: First-run or session-start rituals — setup, preferences, identity tone before core use. Feedstock: …en recovery reveals emotional injury. - label: Logistics of a missing seat summary: How the table reconfigures roles without a recruit screen. ## maps_to_taxonomy - absent_proxy / agency_handoff_enter_exit - session_onboarding / primary_navigation - chronicle_buckets
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- ux_family: session_onboarding
- supplement: True
- coverage_slot: True

### `ux_content_authoring_surface` — Content authoring surface

- status: pending
- walk_tier: coverage
- catalog_face: content
- experience_mode: content_authoring_surface
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How operators or users create, edit, and publish content — distinct from read-only consumption. Feedstock: …synthesis — L5 remint after contaminated artifact wipe (CTO brief) **Audience:** CTO — timeline and governance risk after intentional User-Story wipe and goal-authority supersession; what must be proven before fresh L5 authoring and `l5_manual_gate`. **Phase:** `conceptual_deepen`; vault-known: `Roadmap/User-Story/` tree **wiped** per remint (`gmm-remint-l5-20260627T231800Z`); prior factory run `7e3881b91953` **superseded**; conceptual roadma…
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: Ingest/Agent-Research/2026-06-28-influence-conceptual-deepen-gmm-003106Z.md
- derived_from: research:Ingest/Agent-Research/2026-06-28-influence-conceptual-deepen-gmm-003106Z.md
- ux_family: content_authoring_surface
- supplement: True
- coverage_slot: True

### `ux_dm_soft_framing_tools` — DM soft framing tools

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: inhabit
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Surfaces that help a human steer without stealing player authorship.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-human-operated-story.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-human-operated-story.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_escape_as_first_authorship` — Escape as first authorship

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: inhabit
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Exploration fantasy born as jailbreak, not travel map.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P11-stolen-agency-open.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P11-stolen-agency-open.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_flee_as_authorship_combat_end` — Flee-as-authorship combat end

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: inhabit
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Ending a fight by surviving and saving others when winning is impossible.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_incomplete_information_before_blood` — Incomplete information before blood

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: inhabit
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Deciding with partial truth so regret and authorship coexist.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_wake_in_violation_open` — Wake-in-violation open

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: inhabit
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: First session teaches stolen agency before empowerment.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P11-stolen-agency-open.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P11-stolen-agency-open.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_who_to_sit_with_tonight` — Who to sit with tonight

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: inhabit
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Soft agency over relationship temperature between quests.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_beautiful_rooms_in_a_cruel_place` — Beautiful rooms in a cruel place

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Environmental storytelling that makes the villain intimate.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P11-stolen-agency-open.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P11-stolen-agency-open.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_city_scale_panic_texture` — City-scale panic texture

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How inhabit/table feel when the map itself is the enemy.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_costly_identity_pact_after_a_death` — Costly identity pact after a death

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How resurrection/progression feels when the price is a lasting role the whole table can see.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x44-progression-as-identity.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x44-progression-as-identity.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_cure_that_harms` — Cure that harms

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Trusted procedure as betrayal of body and belief.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P04-institutional-faith-betrayal.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P04-institutional-faith-betrayal.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_empty_chair_fracture` — Empty-chair fracture

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: The feel when a living party member chooses out.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_estranged_home_social_ordeal` — Estranged-home social ordeal

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Returning to a hostile intimate space where rolls are insight and composure.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_faith_shatter_at_the_machine` — Faith shatter at the machine

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Identity progression via institutional doubt.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P04-institutional-faith-betrayal.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P04-institutional-faith-betrayal.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_fourth_option_social_agency` — Fourth-option social agency

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Room to invent a response the wheel did not list.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-human-operated-story.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-human-operated-story.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_guide_who_was_the_problem` — Guide who was the problem

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Narrator/ally trust collapse without removing player agency.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_joy_ritual_beside_betrayal_beat` — Joy ritual beside betrayal beat

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Continuous fiction holding celebration and moral crisis in one arc.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_linger_after_the_fight` — Linger after the fight

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Authored post-combat social/exploration residue before the next hook.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-quiet-between-pillars.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-quiet-between-pillars.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_moral_fork_that_schedules_the_next_fight` — Moral fork that schedules the next fight

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Choosing allegiance rewrites the combat cast and camp trust.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_party_trust_under_ascension_pressure` — Party trust under ascension pressure

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Social contract tested when power offers an exit from humanity.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_personal_stakes_set_piece_combat` — Personal-stakes set-piece combat

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Fight where lineage, shame, and crowd politics ride every swing.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x52-personal-stakes-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x52-personal-stakes-combat.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_post_coma_blame_texture` — Post-coma blame texture

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Social fallout when recovery reveals emotional injury.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_post_kill_political_handoff` — Post-kill political handoff

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: The social beat that starts the second the boss drops.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x52-personal-stakes-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x52-personal-stakes-combat.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_power_object_that_demanded_a_person_not_a_check` — Power object that demanded a person, not a check

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Artifact moments that rewrite identity instead of filling an inventory slot.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x44-progression-as-identity.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x44-progression-as-identity.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_rehabilitation_bargain_after_betrayal` — Rehabilitation bargain after betrayal

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Social agency choosing path over punishment when war politics loom.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_rescue_as_social_contract` — Rescue as social contract

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: The table re-forms around getting them back.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_rest_as_presence_not_only_refill` — Rest as presence, not only refill

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Long rest as camp identity layer, not a resource button alone.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-quiet-between-pillars.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-quiet-between-pillars.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_sibling_panic_in_the_quiet_after_the_roll` — Sibling panic in the quiet after the roll

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Social texture of the table when one life depends on another’s vow.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x44-progression-as-identity.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x44-progression-as-identity.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_side_deal_mischief_beside_sincere_pain` — Side-deal mischief beside sincere pain

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Continuous fiction holding comedy theft and family grief in one session.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_soft_power_party_seizure` — Soft-power party seizure

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: A living companion removed by law/magic, not HP.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_spare_or_swear_companion_crisis` — Spare-or-swear companion crisis

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Party trust rewritten by one mid-campaign choice.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_triage_under_asymmetric_power` — Triage under asymmetric power

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Choosing who to carry when you cannot save the day.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_trial_dungeon_that_ends_in_loyalty` — Trial dungeon that ends in loyalty

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Authored exploration whose boss is a relationship decision.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_who_owns_the_ending` — Who owns the ending

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: table
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Cosmic fork where companions and combat hang on the choice.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_earned_conspiracy_payoff` — Earned conspiracy payoff

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: living_world
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Lore that lands because the player assembled it.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_earned_spy_reveal` — Earned spy reveal

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: living_world
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Looking on purpose and being right — cleverness without spoon-feeding.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_friend_who_was_the_conspiracy` — Friend who was the conspiracy

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: living_world
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Trust rewrite when the ally is the information leak.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_living_world_remembers_without_a_script` — Living-world remembers without a script

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: living_world
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Trust/combat/faction shift from play, not only flagged dialogue nodes.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-human-operated-story.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-human-operated-story.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_quiet_level_acknowledgment` — Quiet level acknowledgment

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: living_world
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Companions/world notice growth without a banner-only UI.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_campfire_identity_chrome` — Campfire identity chrome

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: class_chrome
- dimension: ui_surface
- summary: Class and backstory felt as conversation, not menu.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- supplement: True
- coverage_slot: False
- maps_to: class_chrome_discovery

### `ux_chrome_that_grew_with_you` — Chrome that grew with you

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: class_chrome
- dimension: ui_surface
- summary: Class identity polish that tracks ordinary advancement.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- supplement: True
- coverage_slot: False
- maps_to: class_chrome_discovery

### `ux_diegetic_chrome_persistence` — Diegetic chrome persistence

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: class_chrome
- dimension: ui_surface
- summary: Identity/class cues that stay in the world view without opening a sheet.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- supplement: True
- coverage_slot: False
- maps_to: class_chrome_discovery

### `ux_feedback_anchored_to_the_body` — Feedback anchored to the body

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Cast/hit/trust signals felt at the avatar or companion, not a floating toast only.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_logistics_of_a_missing_seat` — Logistics of a missing seat

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How the table reconfigures roles without a recruit screen.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_new_toy_in_the_next_fight` — New toy in the next fight

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Progression that changes the next combat verb, felt immediately.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_power_trophy_that_the_table_can_feel` — Power trophy that the table can feel

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: class_chrome
- dimension: ui_surface
- summary: Progression chrome earned in the kill, visible to allies and rivals.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x52-personal-stakes-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x52-personal-stakes-combat.md
- supplement: True
- coverage_slot: False
- maps_to: class_chrome_discovery

### `ux_region_map_for_a_social_beat` — Region map for a social beat

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Camp vs inhabit vs table workbench — which screen owns the moment.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_title_reclaim_as_identity_chrome` — Title reclaim as identity chrome

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: class_chrome
- dimension: ui_surface
- summary: A spoken correction that makes class/status feel worn on the body.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- supplement: True
- coverage_slot: False
- maps_to: class_chrome_discovery

### `ux_verb_first_soft_exit` — Verb-first soft exit

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: surfaces
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Leaving a beat via flee, silence, or walk-away as authored input, not cancel UI.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_class_chrome` — Class / subclass chrome

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: class_chrome
- dimension: ui_surface
- summary: Visible class identity polish — not class feature math.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- supplement: True
- coverage_slot: False
- maps_to: class_chrome_discovery

### `ux_dm_player_rails` — DM / player rails

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: How DM and player flows share chrome without fighting each other.
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- supplement: True
- coverage_slot: False
- maps_to: dm_pilot

### `ux_dmpausegate_interaction` — DMPauseGate interaction

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Project-specific experience noun from feedstock heading `DMPauseGate interaction`. Grounds taxonomy coverage in local pin language.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-4-SimTickStub-Sim-Stub-Roll-up-2026-07-16.md
- derived_from: pin:1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-4-SimTickStub-Sim-Stub-Roll-up-2026-07-16.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_feedback_payload_composition_demo_truncated` — Feedback payload composition (demo-truncated)

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Project-specific experience noun from feedstock heading `Feedback payload composition (demo-truncated)`. Grounds taxonomy coverage in local pin language.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-8-PlayerFeedbackChannel-Feedback-Roll-up-2026-07-17.md
- derived_from: pin:1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-8-PlayerFeedbackChannel-Feedback-Roll-up-2026-07-17.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_launch_playregion_hud_flow` — Launch → PlayRegion → HUD flow

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Project-specific experience noun from feedstock heading `Launch → PlayRegion → HUD flow`. Grounds taxonomy coverage in local pin language.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roll-up-2026-07-15.md
- derived_from: pin:1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roll-up-2026-07-15.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_operator_dm_rail_hotkey_vs_scripted_cue` — Operator DM rail hotkey vs scripted cue

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: ui_surface
- summary: Project-specific experience noun from feedstock heading `Operator DM rail hotkey vs scripted cue`. Grounds taxonomy coverage in local pin language.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roll-up-2026-07-16.md
- derived_from: pin:1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roll-up-2026-07-16.md
- supplement: True
- coverage_slot: False
- maps_to: dm_pilot

### `ux_perspectiveenvelope_player_fp_activation` — PerspectiveEnvelope `player_fp` activation

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Project-specific experience noun from feedstock heading `PerspectiveEnvelope` player_fp `activation`. Grounds taxonomy coverage in local pin language.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roll-up-2026-07-15.md
- derived_from: pin:1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roll-up-2026-07-15.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_player_agency_loop` — Player agency loop

- status: pending
- walk_tier: thickener
- altitude: scene_exemplar
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Frictionless moments where the player feels authorship over outcomes.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_playerfprig_attachment` — PlayerFPRig attachment

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Project-specific experience noun from feedstock heading `PlayerFPRig attachment`. Grounds taxonomy coverage in local pin language.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roll-up-2026-07-15.md
- derived_from: pin:1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roll-up-2026-07-15.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_presentation_shell` — Presentation shell

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: presentation_shells
- dimension: ui_surface
- summary: Baseline shell that hosts experience surfaces (supporting axis only).
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- supplement: True
- coverage_slot: False
- maps_to: application_shell

### `ux_rule_representation` — Rule representation

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Project-specific experience noun from feedstock heading `Rule representation`. Grounds taxonomy coverage in local pin language.
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roll-up-2026-07-15.md
- derived_from: pin:1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roll-up-2026-07-15.md
- supplement: True
- coverage_slot: False
- maps_to: baseline_fp

### `ux_scry_presentation` — Scry / Clairvoyance presentation

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: perspective_overrides
- dimension: ui_surface
- summary: How perspective overrides feel and present to the player (not the sim alone).
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- supplement: True
- coverage_slot: False
- maps_to: divination_override

### `ux_session0_identity_art` — Session 0 / identity art

- status: pending
- walk_tier: thickener
- catalog_face: supplement
- mode_tier: thickener
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: Bootstrap rituals and art direction that set identity tone.
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- supplement: True
- coverage_slot: False
- maps_to: session0_bootstrap

## Coverage reminder

Primary walk: `UX-MINT-SERIES` packs (`walk_tier: series`). Taxonomy slots are coverage supplements; Actual-Play nouns are thickeners/skins. See rubric lenses + `SERIES-ALTITUDE-EXEMPLARS.md`. Prune before freeze.
