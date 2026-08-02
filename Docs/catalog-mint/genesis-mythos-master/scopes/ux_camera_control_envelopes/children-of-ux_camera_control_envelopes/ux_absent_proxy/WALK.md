---
title: Walk — ux_absent_proxy
row_id: ux_absent_proxy
parent_id: ux_camera_control_envelopes
walk_tier: coverage
label: Absent-player proxy
status: done
---

# `ux_absent_proxy` — Absent-player proxy

- status: done
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
- summary: When a player is absent, their PC stays in the shared fiction via a session-policy delegate (another player or the DM) who receives that character's controls so the DM is not forced to run monsters and the missing PC at once. Table may volunteer a delegate, or the DM may propose a vote and players choose who is stuck with it; policy is per-session and revocable when the owner returns. This is an agency / control envelope under camera-control — not Sensorium (read-only sight) and not permanent ownership transfer.
- pillar_notes: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode)
- conceptual_pin: 1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- derived_from: actual_play:1-Projects/genesis-mythos-master/Roadmap/User-Story/Actual-Play-Feedstock/moments/BG-P12-institutional-seizure.md
- ux_family: absent_proxy
- supplement: true
- coverage_slot: true
- notes: feedstock_excerpt: …andidates - label: Soft-power party seizure summary: A living companion removed by law/magic, not HP. - label: Rescue as social contract summary: The table re-forms around getting them back. ## maps_to_taxonomy - absent_proxy / agency_handoff_enter_exit - dm_workbench_lore_gui / wa_faction_hierarchy; pillars: exploration: (infer from mode) | combat: mentioned in feedstock | roleplay: (infer from mode); lensed_by:ux_camera_control_envelopes; operator:4pc_absent_delegate_vote_or_volunteer; grok:thin→session_policy_agency_envelope_not_sensorium; batch_locked:camera_control_envelopes:2026-08-01
