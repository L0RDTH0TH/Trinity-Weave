---
title: Series — ux_player_character_creation
row_id: ux_player_character_creation
walk_tier: series
label: Players can author characters and submit them for DM acceptance into a world
status: done
---

# `ux_player_character_creation` — Players can author characters and submit them for DM acceptance into a world

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
- supplement: false
- coverage_slot: false
