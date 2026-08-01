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
waived_axes: []
schema_version: 1
series_published_trinity_ref: d480f3dade1ff5f19301c2aadaebcfc86eeabb8e
children_published_trinity_ref: c5511d545ca344047c0b1e98ee1838130f1ec7dc
quality_validation_status: children_relensed_dual_rail_awaiting_grok_validate
rubric: Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md
machine_mirror: MINT-BACKLOG.yaml
---

# MINT-BACKLOG — `genesis-mythos-master`

Obsidian **operator prune / critique** surface. Edit item fields below (especially `status`), then harvest/freeze/sync will refresh `MINT-BACKLOG.yaml` (machine walk queue + Grok pack).

## Operator gate (two-pass mint)

1. **Series draft** (Cursor) → accept → series-only harvest.
2. Prune series; freeze (series anti-mandate gate). Taxonomy coverage waits for children pass.
3. Grok+user **series walk** until all series `done`.
4. Diff/fit vs `archive_ref` if remine. Then **Trinity/GitHub publish** (`series_published_trinity_ref`) — Grok-facing gate, not Curator.
5. Only then children harvest (series lens) → greenlight → Cursor batches → Trinity-publish children.
6. Actions: `UX_MINT_BACKLOG` `series_draft` | `generate` | `freeze` | `publish_series` | `greenlight_children` | `publish_children`.

**Current status:** `frozen_for_mint`  
**Mint phase:** `children_batch`  
**Harvest pass:** `children`  
**Series Trinity ref:** `d480f3dade1ff5f19301c2aadaebcfc86eeabb8e`  
**Children Trinity ref:** `c5511d545ca344047c0b1e98ee1838130f1ec7dc`  
**Quality validation:** `children_relensed_dual_rail_awaiting_grok_validate`  
**Waived axes/slots:** `(none)`  
**Rubric:** [[Docs/catalog-mint/_shared/UX-MINT-RUBRIC|UX mint rubric]]

## Quick status

- [x] `ux_world_generation` — DM can create (table can shape) a persistent living world (`done`) [living_world] [series]
- [x] `ux_dm_campaign_creation` — DM can bootstrap a campaign frame inside a world (`done`) [table] [series]
- [x] `ux_player_character_creation` — Players can author characters and submit them for DM acceptance into a world (`done`) [table] [series]
- [x] `ux_dm_session_prep` — DM can prep a session without leaving the collaborative table frame (`done`) [table] [series]
- [x] `ux_early_game` — Early play is a power band that gates world and pillar response (`done`) [flows] [series]
- [x] `ux_mid_game` — Mid play is a power band for lasting pressure and deeper world response (`done`) [living_world] [series]
- [x] `ux_late_game` — Late play is a power band for campaign crescendo, close, and character-to-world persistence (`done`) [living_world] [series]
- [x] `ux_mental_stat_interpretation` — Mental stats surface available read paths not only sheet numbers (`done`) [surfaces] [series]
- [x] `ux_collaborative_table_agency` — Shared virtual-tabletop loop with character agency and DM orchestration (`done`) [table] [series]
- [x] `ux_quiet_between_pillars` — In-adventure quiet keeps continuous fiction between combat social and explore (`done`) [table] [series]
- [x] `ux_combat_play_surface` — Combat can resolve by authored paths including non-win ends (`done`) [inhabit] [series]
- [x] `ux_camera_control_envelopes` — Perspective and control envelopes can change and cleanly return (`done`) [inhabit] [series]
- [x] `ux_living_world_continuity` — World can move off-screen and show lasting readable costs (`done`) [living_world] [series]
- [x] `ux_backstory_legacy_integration` — Backstory and legacies can hook into play and chronicle (`done`) [table] [series]
- [x] `ux_world_authorship_modability` — Table and community can author world change via curated and mod contracts (`done`) [living_world] [series]
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

## Items

### `ux_world_generation` — DM can create (table can shape) a persistent living world

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_world_generation
- series_id: lifecycle
- series_order: 0
- series_walk_rank: 0
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
- summary: Durable world container — DM creates initial form via wizard+preview (tone-aware shape families, cached/pre-existing assets); table can shape; players do not author the first world. Physical/settlement layers + monster-region tags; import/attach first-class; every world-hitting change is DM-retconnable. Multiple campaigns/casts attach to the same world.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:world_generation
- ux_family: lifecycle
- supplement: False
- coverage_slot: False

### `ux_dm_campaign_creation` — DM can bootstrap a campaign frame inside a world

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_dm_campaign_creation
- series_id: lifecycle
- series_order: 1
- series_walk_rank: 0
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

### `ux_player_character_creation` — Players can author characters and submit them for DM acceptance into a world

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_player_character_creation
- series_id: lifecycle
- series_order: 2
- series_walk_rank: 0
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

### `ux_dm_session_prep` — DM can prep a session without leaving the collaborative table frame

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_dm_session_prep
- series_id: lifecycle
- series_order: 3
- series_walk_rank: 0
- altitude: product_contract
- seat: ["dm_as_player", "privileged_access"]
- time_scale: session
- does_not_mandate: ["prep must be a separate offline app", "players never see any prep residue", "all prep material is public by default", "prep is a back door around DM gate/retcon on world changes", "session prep creates or replaces the world or campaign frame", "visibility is only a single whole-table tag with no per-player option", "session open is a separate series product noun from prep", "one captivity/tavern/jailbreak open is the product default start"]
- alternatives_not_banned: ["Thin author notes vs rich structured beats (system still stages)", "Mostly secret with selective reveals vs broader general tags", "Prep mode distinct vs prep panels on the DM rail during downtime", "Batch applied on complete vs batch held for DM confirm in world-gen"]
- catalog_face: table
- experience_mode: dm_session_prep
- mode_tier: series
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: DM authors the next shared session experience in-tool; the system auto-stages against the attached world and campaign. Visibility is opt-in: general (whole-table) and/or per-player tags; unmarked stays secret. World-hitting edits batch and hand off into world-gen on prep complete under the same DM gate and retcon rules. Privileged orchestrator seat — not offline admin or invisible infrastructure. Opening situation (session 1 or session N), temporary constraints, and multi-path goals into an authored beat are prep authorship — not a separate series parent. Enter-live-play is a thin shell verb w
- conceptual_pin: needs pin
- derived_from: series:lifecycle:dm_session_prep
- ux_family: lifecycle
- supplement: False
- coverage_slot: False

### `ux_early_game` — Early play is a power band that gates world and pillar response

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_early_game
- series_id: lifecycle
- series_order: 4
- series_walk_rank: 0
- altitude: product_contract
- seat: ["shared_table"]
- time_scale: session
- does_not_mandate: ["first session must teach stolen agency", "early game is combat-only onboarding", "progression requires a separate series parent from stage bands"]
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

### `ux_mid_game` — Mid play is a power band for lasting pressure and deeper world response

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_mid_game
- series_id: lifecycle
- series_order: 5
- series_walk_rank: 0
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

### `ux_late_game` — Late play is a power band for campaign crescendo, close, and character-to-world persistence

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_late_game
- series_id: lifecycle
- series_order: 6
- series_walk_rank: 0
- altitude: product_contract
- seat: ["shared_table", "dm_as_player"]
- time_scale: campaign
- does_not_mandate: ["the only correct ending is institutional seizure", "end game must erase player legacies", "progression requires a separate series parent from stage bands", "session prep replaces the late power-band / close contract", "post-close must start in a different world by default", "late play is only the final session, not a high power band"]
- alternatives_not_banned: ["Abrupt DM end vs long staged crescendo", "Heavy retirement planning vs light future-notes", "Same-world next campaign immediately vs gap time in world sim only", "Multi-world / multi-campaign setups via existing parents"]
- catalog_face: living_world
- experience_mode: late_game
- mode_tier: series
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Late-game is the high power band: survivors are world-shapers. It covers build-up to close and the close itself. DM triggers campaign end through a story crescendo visible in play; players map retirement/future plans; those characters persist as powerful DM-controlled NPCs in the living world. Default continuation is a new campaign in the same world; other topologies remain via world/campaign parents. Not one mandatory finale skin; not session prep.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:late_game
- ux_family: lifecycle
- supplement: False
- coverage_slot: False

### `ux_mental_stat_interpretation` — Mental stats surface available read paths not only sheet numbers

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_mental_stat_interpretation
- series_id: lifecycle
- series_order: 7
- series_walk_rank: 0
- altitude: product_contract
- seat: ["shared_table"]
- time_scale: moment
- does_not_mandate: ["mental stats unlock a single romance dialogue tree", "low mental stats hide all social information", "cues auto-reveal facts without a check or roleplay", "mental-stat cues are DM-only with no player-facing affordance", "one insight beat is the only product presentation"]
- alternatives_not_banned: ["Subtle diegetic cue vs strong highlight", "Always-on stat aura vs cue only when DM or system arms it", "Shared party cues vs strictly per-player vision", "Sparse cues vs frequent mental-stat texture"]
- catalog_face: surfaces
- experience_mode: mental_stat_interpretation
- mode_tier: series
- dnd_pillar: roleplay
- ux_axis: agency
- dimension: ui_surface
- summary: INT, WIS, and CHA can drive visual cues on people, places, and objects that hold relevant information. The cue signals that a mental-stat path is available — it does not spill the content. Cues are stat-gated per player where appropriate; the DM can place or fire cues. Structure menu for presentation, not auto-solving the interaction and not one social-scene skin.
- conceptual_pin: needs pin
- derived_from: series:lifecycle:mental_stat_interpretation
- ux_family: lifecycle
- supplement: False
- coverage_slot: False

### `ux_collaborative_table_agency` — Shared virtual-tabletop loop with character agency and DM orchestration

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_collaborative_table_agency
- series_id: pmg_capabilities
- series_order: 0
- series_walk_rank: 1
- altitude: product_contract
- seat: ["shared_table", "dm_as_player", "privileged_access"]
- time_scale: session
- does_not_mandate: ["DM is only a cue issuer for other players", "players and DM share identical control envelopes", "system-owned NPC dialogue is the product default", "player social play defaults to dialogue-option trees", "play must be combat-primary / hack-and-slash"]
- alternatives_not_banned: ["Combat-heavy tables vs social/explore-primary tables", "Heavy transcription vs light note capture of player intent", "Rich NPC context assist vs minimal prompts", "DM who also runs a character vs DM seat only", "Optional later system-suggested NPC lines under DM accept (not default auto-speak)"]
- catalog_face: table
- experience_mode: collaborative_table_agency
- mode_tier: series
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Virtual tabletop for collaborative storytelling: players act through character tools in an open 3D world; the DM is the privileged orchestrator in the same product loop. Loop is player agency → system and DM resolution → world reacts → roleplay inside that structure. Motives/stakes are table-defined and recorded; player speech can be transcribed. NPC dialogue is the DM’s responsibility — assist tools surface context, they do not replace the DM as speaker by default.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:collaborative_table_agency
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_quiet_between_pillars` — In-adventure quiet keeps continuous fiction between combat social and explore

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_quiet_between_pillars
- series_id: pmg_capabilities
- series_order: 1
- series_walk_rank: 1
- altitude: product_contract
- seat: ["shared_table"]
- time_scale: session
- does_not_mandate: ["downtime equals BG3 campsite companion UI", "quiet is only a long-rest resource refill", "quiet is a loading state between pillars", "this row owns between-adventures weeks/months calendar downtime", "system must force the next combat social or explore beat during quiet"]
- alternatives_not_banned: ["Camp-centric vs road-centric vs both inside the adventure", "Quiet as distinct mode vs low-intensity state in the same world view", "Rest embedded in quiet vs separate rest verb usable during quiet", "Sparse linger vs frequent light authored beats on the road"]
- catalog_face: table
- experience_mode: quiet_between_pillars
- mode_tier: series
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: In-adventure quiet is the product surface for time between pillar bursts — road, camp, linger, and other low-intensity presence — so fiction stays continuous while the table is not in a forced combat, social set-piece, or explore objective. Quiet is largely the system waiting for players and DM to move the story forward. Between-adventures weeks/months sit with living-world continuity, not this parent.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:quiet_between_pillars
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_combat_play_surface` — Combat can resolve by authored paths including non-win ends

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_combat_play_surface
- series_id: pmg_capabilities
- series_order: 2
- series_walk_rank: 1
- altitude: product_contract
- seat: ["shared_table"]
- time_scale: moment
- does_not_mandate: ["flee is the only correct authored end", "combat always resolves to XP loot chrome", "combat is a single win/lose elimination pipeline", "DM only adjudicates and never inhabits creature roles", "player and DM share identical combat control envelopes"]
- alternatives_not_banned: ["Lethal-default tables vs non-lethal-friendly tables", "Flee with chase vs clean disengage", "Parley mid-fight vs only before blows land", "Sparse authored ends vs many stake levers", "XP/loot present vs progression mostly elsewhere", "Heavy vs light creature chrome in early builds", "System-default music only vs frequent DM-queued tracks"]
- catalog_face: inhabit
- experience_mode: combat_play_surface
- mode_tier: series
- dnd_pillar: combat
- ux_axis: combat_cast_feedback
- dimension: ui_surface
- summary: Combat is a distinct play surface the whole table enters and exits: combat chrome and audio for both seats; authorship menu of ends (fight, disengage/flee, parley, stakes, surrender, escape-with-cost, and other legitimate paths); DM gates all actions, owns the encounter cast with creature chrome and voice tools, and can adjust live values. Movement is a readable terrain-aware envelope. Surface consumes pre-compiled rule math from an import/library path. Power band gates offer and lasting costs. Not one flee caption and not the full rules-math pack.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:combat_play_surface
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_camera_control_envelopes` — Perspective and control envelopes can change and cleanly return

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_camera_control_envelopes
- series_id: pmg_capabilities
- series_order: 3
- series_walk_rank: 1
- altitude: product_contract
- seat: ["player", "dm_as_player", "privileged_access"]
- time_scale: moment
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- alternatives_not_banned: ["Heavy vs light transition interpolation (comfort) as long as final state is hard-restored", "Sparse vs frequent override use", "DM who rarely leaves WorldCam vs frequent MapCam / Sensorium / pilot use", "Strict rules-only overrides vs session-policy additions (absent proxy, custom visions)", "Minimal vs rich liminal/unconscious or dominate-victim presentation", "Thin vs fuller dominate pilot/victim in early builds"]
- catalog_face: inhabit
- experience_mode: camera_control_envelopes
- mode_tier: series
- dnd_pillar: shared
- ux_axis: perspective_overrides
- dimension: player_rail
- summary: Baseline player FP and a set of explicit temporary envelopes that change perspective and/or control then hard-restore. Overrides (scry/divination, dominate, liminal/unconscious, planar/gate, absent-proxy, etc.) always return to baseline FP or the declared prior state. DM rail is first-class in the same parent: WorldCam is the DM default; MapCam, Sensorium Attach, and DM pilot are explicit departures with hard restore. Players never use WorldCam/MapCam. Every enter declares controller, presentation, duration, and return target.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:camera_control_envelopes
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_living_world_continuity` — World can move off-screen and show lasting readable costs

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_living_world_continuity
- series_id: pmg_capabilities
- series_order: 4
- series_walk_rank: 1
- altitude: product_contract
- seat: ["shared_table", "dm_as_player"]
- time_scale: campaign
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- alternatives_not_banned: ["Sparse vs dense off-screen pulse", "Soft “the world noticed” texture vs hard mechanical scars that block options", "Mostly social/faction residue vs mostly geographic/physical/resource", "Fast-moving political worlds vs slow scar accumulation", "High-band existential threats that are planar/cosmic vs purely political-apocalyptic", "Thin vs richer downtime surfaces later"]
- catalog_face: living_world
- experience_mode: living_world_continuity
- mode_tier: series
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Living world continues while the party is elsewhere: factions, threads, calendar, minimal downtime, random pressure, and resource sites move off-screen. Costs are readable on return — DM sees machinery; players feel residue in first person (worried NPCs, rumors, tense streets, closed doors, resource interruptions). Lasting-cost amplitude is power-band gated (early local/regional; mid structural/campaign-scale; late existential). Distinct from in-adventure quiet-between. Not a single conspiracy skin.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:living_world_continuity
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_backstory_legacy_integration` — Backstory and legacies can hook into play and chronicle

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_backstory_legacy_integration
- series_id: pmg_capabilities
- series_order: 5
- series_walk_rank: 1
- altitude: product_contract
- seat: ["shared_table", "player"]
- time_scale: campaign
- does_not_mandate: ["every backstory forces a mid-game reunion ordeal", "legacies are DM-only lore with no player surface", "system auto-weaves hooks without DM accept", "one identity-pact skin is the product default for legacies", "players may auto-write world canon from backstory without DM gate"]
- alternatives_not_banned: ["Sparse vs dense seeding", "Mostly social recognition vs mechanical claims (land, title, blood debt)", "Early-only seeding vs ongoing personal stakes added later", "Quiet chronicle-only persistence vs loud in-play callbacks", "One-campaign binding of a legacy vs legacies that can travel into a later campaign in the same world", "Minimal vs richer player-lite chronicle chrome later"]
- catalog_face: table
- experience_mode: backstory_legacy_integration
- mode_tier: series
- dnd_pillar: roleplay
- ux_axis: class_chrome
- dimension: ui_surface
- summary: Backstory and legacies are a first-class player seeding system: players seed personal history, relationships, debts, places, and claims; the system floats those hooks to the DM; the DM weaves timing, intensity, and form under the world/campaign gate (accept, revise, retcon). Players do not auto-write canon. Seeds appear in play and player-lite chronicle as structure menu — not a mandated reunion ordeal and not DM-only lore with no player surface.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:backstory_legacy_integration
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_world_authorship_modability` — Table and community can author world change via curated and mod contracts

- status: done
- walk_tier: series
- mint_lane: human_grok
- fanout: low
- historical_id: ux_world_authorship_modability
- series_id: pmg_capabilities
- series_order: 6
- series_walk_rank: 1
- altitude: product_contract
- seat: ["shared_table", "dm_as_player", "privileged_access"]
- time_scale: world_era
- does_not_mandate: ["mods are post-1.0 only", "timeline editing is player-lite default", "world mutation may bypass intentional re-gen and DM gate", "expensive re-gen dumps the table to menus", "physical and esoteric authorship use different cheat paths outside the mod contract"]
- alternatives_not_banned: ["Thin collaborative seed vs deeper multi-step world authorship sessions", "Heavy Microscope-style era play vs light era tags only", "Curated-only packages vs open community mods later", "Re-gen of a region vs re-gen of a whole biome or faction graph", "Waiting activities other than pong (camp vignette, short challenge, etc.) under the same contract", "Physical-only vs esoteric-only emphasis at different tables"]
- catalog_face: living_world
- experience_mode: world_authorship_modability
- mode_tier: series
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: World change is first-class authorship across the physical container and the esoteric graph (terrain, settlements, eras, factions, populations, high-authority fiction such as Wish). Every structural change gets a computational cost estimate: cheap → in-place; expensive → intentional re-gen with a designed waiting activity (e.g. tournament-style pong or equivalent), then hard-restore — no menu dump. One mod contract covers table/DM and community packages; authority/trust differ, contract shape does not. Microscope-informed non-linear history welcome. Under DM gate; not silent mutation.
- conceptual_pin: needs pin
- derived_from: series:pmg_capabilities:world_authorship_modability
- ux_family: pmg_capabilities
- supplement: False
- coverage_slot: False

### `ux_absent_proxy` — Absent-player proxy

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: absent_proxy
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Delegate pilots an absent PC with explicit handoff when the owner returns (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- ux_family: absent_proxy
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …andidates - label: Soft-power party seizure summary: A living companion removed by law/magic, not HP. - label: Rescue as social contract summary: The table re-forms around getting them back. ## maps_to_taxonomy - absent_proxy / agency_handoff_enter_exit - dm_workbench_lore_gui / wa_faction_hierarchy; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes

### `ux_agency_handoff_enter_exit` — Agency enter / exit handoff feel

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: agency_handoff_enter_exit
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Shared choreography when control or perspective transfers and cleanly returns (under Perspective and control envelopes can change and cleanly return).
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- ux_family: agency_handoff_enter_exit
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …ft-power party seizure summary: A living companion removed by law/magic, not HP. - label: Rescue as social contract summary: The table re-forms around getting them back. ## maps_to_taxonomy - absent_proxy / agency_handoff_enter_exit - dm_workbench_lore_gui / wa_faction_hierarchy; lensed_by:ux_camera_control_envelopes

### `ux_baseline_fp` — Baseline first-person embodiment

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: baseline_fp
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Default embodied play — what the human sees and touches in this pillar (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: baseline_embodiment
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: # Genesis Mythos Master Goal ## One-line Build an open-source, monetizable, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM and player intents — mandatory in-tool session 0, visible world continuity, player-lite legacies and chronicle — players in fir…; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes

### `ux_baseline_fp_controls` — Baseline FP controls

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: baseline_fp_controls
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: How move, look, and intent issuance feel and where control surfaces sit relative to first-person view (under Perspective and control envelopes can change and cleanly return).
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: baseline_fp_controls
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: # Genesis Mythos Master Goal ## One-line Build an open-source, monetizable, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM and player intents — mandatory in-tool session 0, visible world continuity, player-lite legacies and chronicle — players in fir…; lensed_by:ux_camera_control_envelopes

### `ux_class_chrome_discovery` — Class / identity chrome discovery

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_backstory_legacy_integration
- depth_band: 1
- does_not_mandate: ["every backstory forces a mid-game reunion ordeal", "legacies are DM-only lore with no player surface", "system auto-weaves hooks without DM accept", "one identity-pact skin is the product default for legacies", "players may auto-write world canon from backstory without DM gate"]
- catalog_face: inhabit
- experience_mode: class_chrome_discovery
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: class_chrome
- dimension: ui_surface
- summary: How class or identity polish is noticed and used without leaving the embodied moment (under Backstory and legacies can hook into play and chronicle).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-ordinary-progression-rhythm.md
- ux_family: class_chrome_discovery
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …Companions/world notice growth without a banner-only UI. - label: New toy in the next fight summary: Progression that changes the next combat verb, felt immediately. - label: Chrome that grew with you summary: Class identity polish that tracks ordinary advancement. ## maps_to_taxonomy - class_chrome_discovery / combat_cast_feedback - session0_bootstrap / tone_profile_surface - baseline_fp; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_backstory_legacy_integration

### `ux_divination_override` — Divination / remote-sense override

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: divination_override
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: perspective_overrides
- dimension: ui_surface
- summary: Temporary rules-bound departure from baseline FP for remote sensing (scry, clairvoyance, find path, and kin) (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: divination_overrides
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …n for players and commanding mastery for the DM. - **Players default to first-person** — immediate, personal, experiential. No casual third-person orbit or free tactical camera for players. - **Perspective overrides** (Scry/Clairvoyance, divination, astral travel, DM-granted visions, unconscious/liminal states, etc.) are **explicit, temporary, rules-bound** departures from baseline FP — not a per; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes

### `ux_dm_mapcam` — DM MapCam

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: dm_mapcam
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Map-fixed orthographic DM rail — tokens, measurements, fog, LOS adjudication feel (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: dm_observe_rails
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …tool session 0, visible world continuity, player-lite legacies and chronicle — players in first-person by default with rules-driven perspective and agency envelopes, DMs on a dedicated rail (WorldCam, map-fixed Tabletop MapCam, read-only Sensorium Attach), player lore woven into systemic depth, major structural changes via intentional re-generation, every layer built for community remixing. ## Vi; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes; relens:affinity

### `ux_dm_pilot` — DM pilot (agency, not Sensorium)

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: dm_pilot
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: dm_rail
- summary: When session/rules put the DM in control of an entity via pilot envelope (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: dm_pilot
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …ey see?” — **no intent/control transfer** on the DM rail. Compare multiple viewpoints for ruling. Operator debug attach uses the same read-only contract. Always **exit back** to prior DM mode (WorldCam or MapCam). - **DM pilot** — when rules or session policy puts the DM in control of an entity (e.g. NPC dominate, absent PC), that uses the **agency delegation** system (pilot envelope), not Sensor; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes; relens:affinity

### `ux_dm_sensorium` — DM Sensorium Attach

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: dm_sensorium
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Read-only sight bind to an entity — no intent transfer; adjudicate what they see (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- ux_family: dm_observe_rails
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …re that lands because the player assembled it. - label: Guide who was the problem summary: Narrator/ally trust collapse without removing player agency. ## maps_to_taxonomy - wa_npc_secrets / canon_pipeline_feel - dm_sensorium / divination_override; pillars: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes; relens:affinity

### `ux_dm_worldcam` — DM WorldCam

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: dm_worldcam
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Free-flight DM observation rail — how mastery feels in this pillar (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- ux_family: dm_observe_rails
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …texture summary: How inhabit/table feel when the map itself is the enemy. - label: Triage under asymmetric power summary: Choosing who to carry when you cannot save the day. ## maps_to_taxonomy - baseline_fp / dm_worldcam - absent_proxy / agency_handoff_enter_exit - quest_pressure_surface / sim_weather_pulse; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes; relens:affinity

### `ux_dominate_pilot` — Dominate / pilot (controller)

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: dominate_pilot
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Dominator pilots the target — FP and control from the dominated body (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- ux_family: dominate_pilot
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: # Felt moment (pattern language) Final hours ask **who owns the ending**: sacrifice, transform, free, dominate. Companions react; combat may resolve the social choice or follow it. Party trust under cosmic stakes. Digital D&D’s version of “the table decides what kind of story this was.” ## Spatial / temporal / control Climax a…; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes

### `ux_dominate_victim` — Dominate victim / passenger overlay

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: dominate_victim
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: agency
- dimension: player_rail
- summary: Victim presentation during dominate — passenger FP, locked input, liminal chrome (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P10-endgame-authorship-fork.md
- ux_family: victim_overlay
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …where companions and combat hang on the choice. - label: Party trust under ascension pressure summary: Social contract tested when power offers an exit from humanity. ## maps_to_taxonomy - dominate_pilot / dominate_victim - planar_travel_override - canon_pipeline_feel; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes

### `ux_liminal_unconscious` — Liminal / unconscious presentation

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: liminal_unconscious
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: perspective_overrides
- dimension: ui_surface
- summary: Status-bound liminal or unconscious presentation and return to baseline (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P04-institutional-faith-betrayal.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P04-institutional-faith-betrayal.md
- ux_family: liminal_states
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …un candidates - label: Cure that harms summary: Trusted procedure as betrayal of body and belief. - label: Faith shatter at the machine summary: Identity progression via institutional doubt. ## maps_to_taxonomy - liminal_unconscious / combat_cast_feedback - class_chrome_discovery - session0_bootstrap; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes

### `ux_planar_travel_override` — Planar / gate travel override

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_camera_control_envelopes
- depth_band: 1
- does_not_mandate: ["players get free third-person orbit as default", "DM tools exist only as debug infrastructure", "envelope exits leave soft residual control or wrong perspective", "camera modes can become permanent without a restore path", "players may use WorldCam or MapCam as free exploration seats"]
- catalog_face: inhabit
- experience_mode: planar_travel_override
- mode_tier: critical_matrix
- dnd_pillar: shared
- ux_axis: perspective_overrides
- dimension: ui_surface
- summary: How planar travel or gate-like transitions feel as temporary perspective/agency departures (under Perspective and control envelopes can change and cleanly return).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: planar_travel_overrides
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …(victim)** — dominated PC: presentation policy is spell-bound (e.g. passenger FP with locked input, liminal UI); exact default locked at Phase 5 spell metadata. - **Absent-player proxy** — session policy allows a delegate (another player or DM) to **pilot** an absent PC with explicit handoff when the owner returns. - **Enter/exit** — every delegation declares controller, victim presentation, dura; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes

### `ux_combat_cast_feedback` — Combat / cast sensory feedback

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_combat_play_surface
- depth_band: 1
- does_not_mandate: ["flee is the only correct authored end", "combat always resolves to XP loot chrome", "combat is a single win/lose elimination pipeline", "DM only adjudicates and never inhabits creature roles", "player and DM share identical combat control envelopes"]
- catalog_face: inhabit
- experience_mode: combat_cast_feedback
- mode_tier: multi_pillar
- dnd_pillar: combat
- ux_axis: combat_cast_feedback
- dimension: ui_surface
- summary: Cast and hit sensory response the player notices — not damage formulas (under Combat can resolve by authored paths including non-win ends).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- ux_family: combat_cast_feedback
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: # Felt moment (pattern language) Phenomenology is not enough until it names **where the body meets the product**. For every major feel (camp talk, flee authorship, moral fork, cast feedback), the catalog must force later pseudo-code to answer: - **Screen region** — corner chrome, center stage, diegetic world, modal, or off-screen audio - **Persistence** — always-on identity chrome vs ephemeral pro; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_combat_play_surface

### `ux_chronicle_buckets` — Chronicle data buckets

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_backstory_legacy_integration
- depth_band: 1
- does_not_mandate: ["every backstory forces a mid-game reunion ordeal", "legacies are DM-only lore with no player surface", "system auto-weaves hooks without DM accept", "one identity-pact skin is the product default for legacies", "players may auto-write world canon from backstory without DM gate"]
- catalog_face: table
- experience_mode: chronicle_buckets
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Keep world ripples, session chronicle, and personal archive distinct in UX (under Backstory and legacies can hook into play and chronicle).
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x60-social-identity-texture.md
- ux_family: chronicle_buckets
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …abel: Side-deal mischief beside sincere pain summary: Continuous fiction holding comedy theft and family grief in one session. ## maps_to_taxonomy - session0_bootstrap / tone_profile_surface - player_lite_lore_gui / chronicle_buckets - agency_handoff_enter_exit; lensed_by:ux_backstory_legacy_integration; relens:affinity

### `ux_dm_workbench_lore_gui` — DM workbench lore GUI

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_dm_session_prep
- depth_band: 1
- does_not_mandate: ["prep must be a separate offline app", "players never see any prep residue", "all prep material is public by default", "prep is a back door around DM gate/retcon on world changes", "session prep creates or replaces the world or campaign frame", "visibility is only a single whole-table tag with no per-player option", "session open is a separate series product noun from prep", "one captivity/tavern/jailbreak open is the product default start"]
- catalog_face: table
- experience_mode: dm_workbench_lore_gui
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: dm_player_rails
- dimension: dm_rail
- summary: Canon graph, accept/revise intents, faction off-screen, quest-hook integration UI (under DM can prep a session without leaving the collaborative table frame).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: dm_workbench_lore_gui
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …since you left…”) · **Last session** recap · **My chronicle** (personal notes by session, search) · optional export/mirror for note-taking players. **Not** timeline editing, contradiction resolution, or sim admin. | | **DM workbench** | Full canon graph, faction/tribe off-screen activity, accept/revise intents, quest integration from active hooks. | Keep three **data buckets** distinct in UX: **w; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_dm_session_prep

### `ux_player_lite_lore_gui` — Player-lite lore GUI

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_backstory_legacy_integration
- depth_band: 1
- does_not_mandate: ["every backstory forces a mid-game reunion ordeal", "legacies are DM-only lore with no player surface", "system auto-weaves hooks without DM accept", "one identity-pact skin is the product default for legacies", "players may auto-write world canon from backstory without DM gate"]
- catalog_face: table
- experience_mode: player_lite_lore_gui
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Intent inbox, Legacies, last-session recap, personal chronicle — not sim admin (under Backstory and legacies can hook into play and chronicle).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: player_lite_lore_gui
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …rce, monetizable, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM and player intents — mandatory in-tool session 0, visible world continuity, player-lite legacies and chronicle — players in first-person by default with rules-driven perspective and agency envelopes, DMs on a dedicated rail (WorldCam, map-fixed Tabletop M; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_backstory_legacy_integration; relens:affinity

### `ux_session0_bootstrap` — Session 0 bootstrap feel

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_dm_campaign_creation
- depth_band: 1
- does_not_mandate: ["every campaign begins in captivity", "offline Microscope play is required before Session 0", "starting a campaign must regenerate the whole world", "campaign creation's default next step is player character creation", "DM is the primary author of player characters after frame bootstrap"]
- catalog_face: table
- experience_mode: session0_bootstrap
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: In-tool session 0 — bounds, tone pick, intent propose, table accept/revise (under DM can bootstrap a campaign frame inside a world).
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: session0_bootstrap
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …Goal ## One-line Build an open-source, monetizable, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM and player intents — mandatory in-tool session 0, visible world continuity, player-lite legacies and chronicle — players in first-person by default with rules-driven perspective and agency envelopes, DMs on a dedicated ra; lensed_by:ux_dm_campaign_creation

### `ux_tone_profile_surface` — Campaign tone profile surface

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_dm_campaign_creation
- depth_band: 1
- does_not_mandate: ["every campaign begins in captivity", "offline Microscope play is required before Session 0", "starting a campaign must regenerate the whole world", "campaign creation's default next step is player character creation", "DM is the primary author of player characters after frame bootstrap"]
- catalog_face: table
- experience_mode: tone_profile_surface
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: How the chosen tone biases chrome, previews, and felt world without siloed presets (under DM can bootstrap a campaign frame inside a world).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: tone_profile_surface
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …ts — so quests integrate with the world graph, not generic fetch loops. **Collaborative canon & session bootstrap.** - **Session 0 (required, in-tool):** world bootstrap before campaign play — table bounds, **campaign tone profile** (see below), player intents, DM/table accept or revise canon. Collaborative-history patterns (shared eras, legacies, non-linear threads) are **Microscope-informed** —; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_dm_campaign_creation

### `ux_canon_pipeline_feel` — Canon pipeline feel

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: canon_pipeline_feel
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: proposed → accepted → hooked → sim-active as human-facing states (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: canon_pipeline_feel
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …, legacies, non-linear threads) are **Microscope-informed** — see [[Ingest/Microscope PDF]] — **not** dependent on playing a separate RPG. Optional offline history may **import** as a canon bundle (power-user path). - **Canon pipeline:** `proposed → accepted → hooked → sim-active` — intents become facts, then systemic hooks, then visible ripples and quest pressure. **Campaign tone profiles** — on; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_economy_resources` — Resource distribution visibility

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: economy_resources
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: What player/DM can see vs must discover about resources — not spreadsheet admin by default (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: mentioned in feedstock | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-quiet-between-pillars.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-quiet-between-pillars.md
- ux_family: economy_resources
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …ial/explore. - label: Linger after the fight summary: Authored post-combat social/exploration residue before the next hook. - label: Rest as presence, not only refill summary: Long rest as camp identity layer, not a resource button alone. ## maps_to_taxonomy - session_onboarding / application_shell - player_lite_lore_gui / chronicle_buckets - sim_weather_pulse; pillars: exploration: mentioned in feedstock | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_economy_trade` — Trade routes / market pressure

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: economy_trade
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Trade and market pressure as world-continuity surfaces (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- ux_family: economy_trade
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: # Felt moment (pattern language) The party suspects a friend is double-dealing. They **choose to look** (familiar spy, eavesdrop) and catch a disguised meeting. Truth lands: the ally traded sacred secrets for research ambition, then grew to care for the party against the original plan. The table must decide whether to destroy, use, or rehabilitate someone who lied. Players feel clever for connecti; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_quest_pressure_surface` — Quest pressure from canon

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: quest_pressure_surface
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How hooks appear in play and on the workbench — not fetch-only tables (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: quest_pressure_surface
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …e RPG. Optional offline history may **import** as a canon bundle (power-user path). - **Canon pipeline:** `proposed → accepted → hooked → sim-active` — intents become facts, then systemic hooks, then visible ripples and quest pressure. **Campaign tone profiles** — one session-level vibe that biases every subsystem (Palette for *how* the world feels, not plot). Core set (**four only for now**; opt; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_faction_goals` — Faction goals / agenda surface

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_faction_goals
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Faction goals and pressure as felt by player and DM (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C2-2x97-information-scent-social-agency.md
- ux_family: wa_faction_goals
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: # Felt moment (pattern language) The party suspects a friend is double-dealing. They **choose to look** (familiar spy, eavesdrop) and catch a disguised meeting. Truth lands: the ally traded sacred secrets for research ambition, then grew to care for the party against the original plan. The table must decide whether to destroy, use, or rehabilitate someone who lied. Players feel clever for connecti; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_faction_hierarchy` — Faction hierarchy surface

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_faction_hierarchy
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Faction structure and ranks as browsable/playable continuity (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- ux_family: wa_faction_hierarchy
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: # Felt moment (pattern language) Early in a digital D&D-like game, two factions ask for your blade. Choosing a side changes **who you fight**, who trusts you at camp, and which story threads stay open. The fork is not a dialogue checkbox only — the next combat encounter *is* the moral residue. Con…; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_faction_offscreen` — Off-screen faction activity

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_faction_offscreen
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Since-you-left deltas and off-screen faction pulse as human-facing continuity (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/WB-control-surface-mapping.md
- ux_family: wa_faction_offscreen
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …product**. For every major feel (camp talk, flee authorship, moral fork, cast feedback), the catalog must force later pseudo-code to answer: - **Screen region** — corner chrome, center stage, diegetic world, modal, or off-screen audio - **Persistence** — always-on identity chrome vs ephemeral prompt vs camp-only surface - **Input verbs** — look, approach, interrupt, soft-exit, commit, flee — not ; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_faction_reputation` — Reputation standing surface

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_faction_reputation
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Reputation and consequence as surfaced to player vs DM (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- ux_family: wa_faction_reputation
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …giance rewrites the combat cast and camp trust. - label: Incomplete information before blood summary: Deciding with partial truth so regret and authorship coexist. ## maps_to_taxonomy - wa_faction_goals / wa_faction_reputation - baseline_fp / quest_pressure_surface; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_lore_articles` — Lore codex / articles

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_lore_articles
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: World lore articles as readable continuity distinct from personal chronicle (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P07-conspiracy-rewires-trust.md
- ux_family: wa_lore_articles
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: # Felt moment (pattern language) Mid/late game, the player connects breadcrumbs and learns who the **Chosen / conspiracy** really are — or that a trusted voice was shaping them. Lore dump feels earned because the player walked the map. Trust in narrator, dream-guide, or ally rewires. Digital cousin to table information scent. ## Spatial / temporal / control Colony / sanctum / dream space. Soft fra; pillars: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_npc_agenda` — NPC agenda / schedule visibility

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_npc_agenda
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Agenda and schedule as human-facing continuity — not raw sim tables (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: wa_npc_agenda
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …DM canon) · **session chronicle** (table recap) · **personal archive** (player-owned notes — may disagree with canon). **The world pulses with life, customization, and balanced agency.** - Layered simulation: weather, NPC agendas, ambient surprises, persistent scars from play — **weighted by campaign tone profile**. - **DM overwrites:** in-session tweaks (tokens, weather, events, whispers) vs. de; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_npc_relations` — NPC relationship web

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_npc_relations
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How relationships among NPCs/factions are browsed and felt (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- ux_family: wa_npc_relations
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …summary: Class and backstory felt as conversation, not menu. - label: Quiet between pillars summary: Designed downtime that keeps continuous fiction alive. - label: Who to sit with tonight summary: Soft agency over relationship temperature between quests. ## maps_to_taxonomy - session0_bootstrap / tone_profile_surface - class_chrome_discovery - application_shell / primary_navigation; pillars: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_npc_secrets` — NPC secrets / knowledge gates

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_npc_secrets
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How hidden knowledge is gated and revealed without spoiling authoring vs play (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- ux_family: wa_npc_secrets
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: # Felt moment (pattern language) A dungeon is structured as **tests** for a companion’s faith or order. Completing it can force a loyalty crisis: spare or sacrifice a person/secret the companion swore to. Exploration authorship (puzzles, paths) ends in a moral fork the party feels at camp afterward. Consequence lands mid-game, not at credits. ## Spatial / temporal / control Authored trial spaces…; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_npc_sheet` — NPC identity sheet feel

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_npc_sheet
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: World Anvil–depth NPC identity surface — who they are at a glance in play/authoring (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P06-loyalty-trial-authored-space.md
- ux_family: wa_npc_sheet
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …hat ends in loyalty summary: Authored exploration whose boss is a relationship decision. - label: Spare-or-swear companion crisis summary: Party trust rewritten by one mid-campaign choice. ## maps_to_taxonomy - wa_npc_secrets / wa_npc_relations - canon_pipeline_feel - planar_travel_override (threshold metaphors); pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_timelines` — Timeline / era threads

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_timelines
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: Eras and non-linear history threads as Microscope-informed continuity UX (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: wa_timelines
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …eed) · **My Legacies** (canon ripples — tribe status, threads, “since you left…”) · **Last session** recap · **My chronicle** (personal notes by session, search) · optional export/mirror for note-taking players. **Not** timeline editing, contradiction resolution, or sim admin. | | **DM workbench** | Full canon graph, faction/tribe off-screen activity, accept/revise intents, quest integration from; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_worldgen_gui` — Worldgen GUI

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_world_generation
- depth_band: 1
- does_not_mandate: ["one world equals exactly one campaign forever", "worldgen is only a Session 0 checkbox with no persistent container", "players author the first world", "world create forces unconstrained multi-knob fresh-noise every time", "world creation's default next step is player character creation"]
- catalog_face: living_world
- experience_mode: worldgen_gui
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: presentation_shells
- dimension: world_gen
- summary: Collaborative generation dialogue — propose scaffolds, choose/refine, preview, accept/regenerate a persistent living world) (under DM can create (table can shape) a persistent living world).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: worldgen_gui
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …onflict | | **Grimdark** | Moral gray, harsh consequences (Witcher-like) | Bleak weather bias, costly hope, persistent scars | - **`ToneProfile`** — one bundled profile per campaign (chosen at session 0), consumed by **world gen**, **weather**, **sim defaults**, **lore/event tone**, and **quest framing** — not siloed presets per subsystem. - Profiles are **defaults**, not stereotypes; table Palet; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_world_generation

### `ux_sim_weather_pulse` — Weather / ambient sim pulse

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: sim_weather_pulse
- mode_tier: multi_pillar
- dnd_pillar: exploration
- ux_axis: agency
- dimension: sim_system
- summary: Tone-weighted weather and ambient world pulse as felt, not raw tick tables (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x39-flee-as-correct-agency.md
- ux_family: sim_weather_pulse
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …l: Triage under asymmetric power summary: Choosing who to carry when you cannot save the day. ## maps_to_taxonomy - baseline_fp / dm_worldcam - absent_proxy / agency_handoff_enter_exit - quest_pressure_surface / sim_weather_pulse; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_faction_territory` — Faction territory / influence

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_faction_territory
- mode_tier: multi_pillar
- dnd_pillar: exploration
- ux_axis: agency
- dimension: ui_surface
- summary: Territory and influence as map and embodied discovery (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roll-up-2026-07-15.md
- derived_from: pin:1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roll-up-2026-07-15.md
- ux_family: wa_faction_territory
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …log and attestation fail path; **PresentationSessionHandle** fields emitted at handoff; `presentation.launch_complete` bus contract; rollback on bootstrap failure. **Out of scope:** PlayRegion viewport mount (**6.1.2** territory); HUD layer stack (**6.1.3** territory); horizon demo spawn (**6.2**); factory vs demo glue (**6.3**); execution-track build pipeline CI wiring (execution-deferred / advi; pillars: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_locations` — Location surfaces

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_locations
- mode_tier: multi_pillar
- dnd_pillar: exploration
- ux_axis: agency
- dimension: world_gen
- summary: Location surfaces — table-facing capability under Mid play is a power band for lasting pressure and deeper world response; structure menu, not a single AP scene default (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- derived_from: pmg:1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md
- ux_family: wa_locations
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …ent surprises, persistent scars from play — **weighted by campaign tone profile**. - **DM overwrites:** in-session tweaks (tokens, weather, events, whispers) vs. deliberate re-generation for terrain reshaping or biome relocation. - Extensibility: swap simulation flavors, visual styles, rule behaviors, and **tone profiles** without breaking cohesion. **Open source and aggressive modularity** — eve; pillars: exploration: mentioned in feedstock | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_maps_vs_embodied` — Maps vs embodied discovery

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_maps_vs_embodied
- mode_tier: multi_pillar
- dnd_pillar: exploration
- ux_axis: dm_player_rails
- dimension: ui_surface
- summary: When knowledge comes from map chrome vs first-person discovery (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- ux_family: wa_maps_vs_embodied
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …ou at camp, and which story threads stay open. The fork is not a dialogue checkbox only — the next combat encounter *is* the moral residue. Consequence scent: the world remembers. ## Spatial / temporal / control Split map regions (sanctuary vs hostile camp). Attention on spokespeople then on the battlefield you unlocked. Soft framing via urgency and incomplete information. ## Experience noun cand; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_wa_npc_dialogue_hooks` — NPC dialogue / roleplay hooks

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_living_world_continuity
- depth_band: 1
- does_not_mandate: ["world motion requires a scripted companion betrayal arc", "lasting costs are only cosmic death pacts", "one conspiracy skin is the only continuity form", "this row owns in-adventure quiet-between road/camp/linger", "players get full sim-admin tools as the continuity surface"]
- catalog_face: living_world
- experience_mode: wa_npc_dialogue_hooks
- mode_tier: multi_pillar
- dnd_pillar: roleplay
- ux_axis: agency
- dimension: ui_surface
- summary: How dialogue and roleplay hooks surface in the moment of play (under World can move off-screen and show lasting readable costs).
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P01-moral-fork-with-combat.md
- ux_family: wa_npc_dialogue_hooks
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …Felt moment (pattern language) Early in a digital D&D-like game, two factions ask for your blade. Choosing a side changes **who you fight**, who trusts you at camp, and which story threads stay open. The fork is not a dialogue checkbox only — the next combat encounter *is* the moral residue. Consequence scent: the world remembers. ## Spatial / temporal / control Split map regions (sanctuary vs ho; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_living_world_continuity; relens:affinity

### `ux_application_shell` — Application shell / layout chrome

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_collaborative_table_agency
- depth_band: 1
- does_not_mandate: ["DM is only a cue issuer for other players", "players and DM share identical control envelopes", "system-owned NPC dialogue is the product default", "player social play defaults to dialogue-option trees", "play must be combat-primary / hack-and-slash"]
- catalog_face: surfaces
- experience_mode: application_shell
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: presentation_shells
- dimension: ui_surface
- summary: Baseline shell — screen regions, chrome placement, layout mapping for any product (under Shared virtual-tabletop loop with character agency and DM orchestration).
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- ux_family: application_shell
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …ction alive. - label: Who to sit with tonight summary: Soft agency over relationship temperature between quests. ## maps_to_taxonomy - session0_bootstrap / tone_profile_surface - class_chrome_discovery - application_shell / primary_navigation; lensed_by:ux_collaborative_table_agency; relens:affinity

### `ux_primary_navigation` — Primary navigation / wayfinding

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_collaborative_table_agency
- depth_band: 1
- does_not_mandate: ["DM is only a cue issuer for other players", "players and DM share identical control envelopes", "system-owned NPC dialogue is the product default", "player social play defaults to dialogue-option trees", "play must be combat-primary / hack-and-slash"]
- catalog_face: flows
- experience_mode: primary_navigation
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How users move between major areas — menus, routes, breadcrumbs, spatial wayfinding (under Shared virtual-tabletop loop with character agency and DM orchestration).
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P02-camp-social-layer.md
- ux_family: primary_navigation
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …abel: Who to sit with tonight summary: Soft agency over relationship temperature between quests. ## maps_to_taxonomy - session0_bootstrap / tone_profile_surface - class_chrome_discovery - application_shell / primary_navigation; lensed_by:ux_collaborative_table_agency; relens:affinity

### `ux_session_onboarding` — Session / onboarding bootstrap

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_dm_campaign_creation
- depth_band: 1
- does_not_mandate: ["every campaign begins in captivity", "offline Microscope play is required before Session 0", "starting a campaign must regenerate the whole world", "campaign creation's default next step is player character creation", "DM is the primary author of player characters after frame bootstrap"]
- catalog_face: flows
- experience_mode: session_onboarding
- mode_tier: shared_chrome
- dnd_pillar: shared
- ux_axis: session0_identity_art
- dimension: session_bootstrap
- summary: First-run or session-start rituals — setup, preferences, identity tone before core use (under DM can bootstrap a campaign frame inside a world).
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/CR-C1-1x85-party-fracture.md
- ux_family: session_onboarding
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …en recovery reveals emotional injury. - label: Logistics of a missing seat summary: How the table reconfigures roles without a recruit screen. ## maps_to_taxonomy - absent_proxy / agency_handoff_enter_exit - session_onboarding / primary_navigation - chronicle_buckets; lensed_by:ux_dm_campaign_creation

### `ux_content_authoring_surface` — Content authoring surface

- status: pending
- walk_tier: coverage
- mint_lane: validate_batch
- parent_id: ux_world_authorship_modability
- depth_band: 1
- does_not_mandate: ["mods are post-1.0 only", "timeline editing is player-lite default", "world mutation may bypass intentional re-gen and DM gate", "expensive re-gen dumps the table to menus", "physical and esoteric authorship use different cheat paths outside the mod contract"]
- catalog_face: content
- experience_mode: content_authoring_surface
- mode_tier: multi_pillar
- dnd_pillar: shared
- ux_axis: agency
- dimension: ui_surface
- summary: How operators or users create, edit, and publish content — distinct from read-only consumption (under Table and community can author world change via curated and mod contracts).
- pillar_notes: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode)
- conceptual_pin: Ingest/Agent-Research/2026-06-28-influence-conceptual-deepen-gmm-003106Z.md
- derived_from: research:Ingest/Agent-Research/2026-06-28-influence-conceptual-deepen-gmm-003106Z.md
- ux_family: content_authoring_surface
- supplement: True
- coverage_slot: True
- notes: feedstock_excerpt: …synthesis — L5 remint after contaminated artifact wipe (CTO brief) **Audience:** CTO — timeline and governance risk after intentional User-Story wipe and goal-authority supersession; what must be proven before fresh L5 authoring and `l5_manual_gate`. **Phase:** `conceptual_deepen`; vault-known: `Roadmap/User-Story/` tree **wiped** per remint (`gmm-remint-l5-20260627T231800Z`); prior factory run `; pillars: exploration: (infer from mode) | combat: (infer from mode) | roleplay: (infer from mode); lensed_by:ux_world_authorship_modability; relens:affinity

## Coverage reminder

Two-pass: series cards first (`walk_tier: series`), locked + Trinity-published, then children mined through those lenses. Taxonomy slots are children-pass coverage; Actual-Play nouns are thickeners/skins. See rubric + `SERIES-ALTITUDE-EXEMPLARS.md`.
