---
title: Phase 6.2.7 — OverwriteDemonstrationSlot Overwrite Demo
roadmap-level: tertiary
phase-number: 6
subphase-index: 6.2.7
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
- overwrite
- beat-7
- half-a
para-type: Project
roadmap_track: conceptual
factory_track: false
horizon_demo_track: true
links:
- '[[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]'
- '[[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]'
- '[[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roll-up-2026-07-17]]'
handoff_readiness: 85
product_factory_run_id: c1dc1d565ea2
parent_secondary: '6.2'
depth_first_backfill: true
demo_loop_beat: 7
persona_id: half_a.conceptual_architect
body_chars_pre_recompact: 10937
body_chars_claimed: 1149
body_chars_cap: 1200
body_over_cap: false
factory_feed_gate_reason: manual_chat_recompact_1200
body_compact_status: complete
rollup-detail: '[[Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roll-up-2026-07-17]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.2.7 — OverwriteDemonstrationSlot Overwrite Demo

Beat **7 (Overwrite)** of [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **OverwriteDemonstrationSlot** applies demo `live_patch` on `demo_shrine_mood` via **OverwritePatchLayer**, runs **NarrativeDeltaVetoPolicy**, publishes outcome. Nouns/ordering only.

## Scope

**In:** OverwriteDemonstrationSlot; live_patch on demo_shrine_mood; OverwritePatchLayer; NarrativeDeltaVetoPolicy (demo); demo.overwrite_applied / demo.overwrite_vetoed; beat 7 after demo.dm_cam_active (6.2.6). **Out:** ReGenerationIntentQueue; CanonRegistry writes; Godot applicators; factory/L5; exec — advisory.

## Behavior

dm_cam_active → build live_patch → veto policy → commit or veto → emit overwrite_* → unlock beat 8. Detail → [[Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roll-up-2026-07-17]].

## Interfaces

**Imports:** demo.dm_cam_active (6.2.6); stub facets (6.2.1); DMOverwriteClass nouns (3.3). **Exports:** overwrite_applied/vetoed on session.*. **Consumers:** 6.2.8 PlayerFeedbackChannel.

## Handoff

**85%** — tertiary feedstock. Exec-deferred — advisory. Body ≤1200.
