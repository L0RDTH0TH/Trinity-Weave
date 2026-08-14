---
title: Phase 6.2.6 — DMCamTransitionSlot DM Cam
roadmap-level: tertiary
phase-number: 6
subphase-index: 6.2.6
project-id: genesis-mythos-master
status: active
priority: high
progress: 100
created: 2026-06-27
tags:
- roadmap
- genesis-mythos-master
- phase-6
- horizon-demo
- dm-cam
- beat-6
- half-a
para-type: Project
roadmap_track: conceptual
factory_track: false
horizon_demo_track: true
links:
- '[[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]'
- '[[Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]'
- '[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roll-up-2026-07-16]]'
handoff_readiness: 85
product_factory_run_id: c1dc1d565ea2
parent_secondary: '6.2'
depth_first_backfill: true
demo_loop_beat: 6
persona_id: half_a.conceptual_architect
rollup-detail: '[[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roll-up-2026-07-16]]'
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase626-tertiary-20260716T061100Z
factory_feed_gate_status: green
body_compact_status: complete
body_chars_pre_recompact: 1397
body_chars_claimed: 1149
body_chars_cap: 1200
body_over_cap: false
factory_feed_gate_reason: manual_chat_recompact_1200
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.2.6 — DMCamTransitionSlot DM Cam

Decomposes **beat 6 (DM cam)** from [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **DMCamTransitionSlot**, **player_fp**→**WorldCam** via `fp_to_worldcam_demo`, guards + DMPauseGate,…

## Scope

**In:** lifecycle; eligibility + hotkey/cue; `fp_to_worldcam_demo`; guards; DMPauseGate; WorldCam-only; HUD badge; beat 6 gates. **Out:** 6.2.1–6.2.5; 6.2.7–6.2.8; full DMRigPolicyMatrix; MapCam/Sensorium; factory; exec — advisory.

## Behavior

awaiting_eligibility → awaiting_trigger → guard_evaluating → transitioning → dm_active | blocked | rejected. Detail → [[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roll-up-2026-07-16]].

## Interfaces

Imports: `demo.rule_check_complete` + rule outcome (6.2.5); `demo.fp_active` (6.2.2); play_region_ready (6.1.2); ModeTransitionGraph/guards (4.2); DMPauseGate (3.1); HUDLayerStack (6.1.3). Exports: `demo.dm_cam_active`; `presentation.mode_badge_dm`. Consumers: 6.2.7; 6.2.8.

## Roll-up

Edges/OQs → [[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roll-up-2026-07-16]].

## Handoff

**85%** — tertiary feedstock. Exec-deferred — advisory. Body ≤1200.
