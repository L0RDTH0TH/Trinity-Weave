---
title: Series — ux_camera_control_envelopes
row_id: ux_camera_control_envelopes
walk_tier: series
label: Perspective and control envelopes can change and cleanly return
status: done
---

# `ux_camera_control_envelopes` — Perspective and control envelopes can change and cleanly return

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
- supplement: false
- coverage_slot: false
