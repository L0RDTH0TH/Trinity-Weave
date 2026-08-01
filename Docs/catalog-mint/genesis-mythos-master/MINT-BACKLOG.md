---
title: MINT-BACKLOG — genesis-mythos-master
project-id: genesis-mythos-master
para-type: Project
backlog_status: frozen_for_mint
mint_phase: series_locked
harvest_pass: series
series_draft_accepted: true
waive_series_draft: false
children_greenlit: false
waived_axes: []
schema_version: 1
generated_at: 2026-08-01 21:11:08+00:00
frozen_at: 2026-08-01 21:11:08+00:00
archive_ref: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Versions/mint-run--20260801-twopass-archive
quality_validation_status: structure_validated_content_unproven_cold_mine
quality_validation: structure_only_pending_content_validation — 2026-08-01 remine expanded UX-MINT-SERIES packs (not a cold PMG-only series invent). Series set matched archive 15/15; content restored from archive + selective live template drift. Full independent series quality validation outside structure is FUTURE debt if issues appear.
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
**Mint phase:** `series_locked`  
**Harvest pass:** `series`  
**Series Trinity ref:** `(none)`  
**Children Trinity ref:** `(none)`  
**Quality validation:** `structure_validated_content_unproven_cold_mine`  
**Waived axes/slots:** `(none)`  
**Rubric:** [[Docs/catalog-mint/_shared/UX-MINT-RUBRIC|UX mint rubric]]

> [!warning] Quality caveat — structure first  
> structure_only_pending_content_validation — 2026-08-01 remine expanded UX-MINT-SERIES packs (not a cold PMG-only series invent). Series set matched archive 15/15; content restored from archive + selective live template drift. Full independent series quality validation outside structure is FUTURE debt if issues appear.

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

## Coverage reminder

Two-pass: series cards first (`walk_tier: series`), locked + Trinity-published, then children mined through those lenses. Taxonomy slots are children-pass coverage; Actual-Play nouns are thickeners/skins. See rubric + `SERIES-ALTITUDE-EXEMPLARS.md`.
