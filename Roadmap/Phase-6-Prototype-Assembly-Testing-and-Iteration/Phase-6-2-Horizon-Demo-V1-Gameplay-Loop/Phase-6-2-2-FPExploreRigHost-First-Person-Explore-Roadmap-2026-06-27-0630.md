---
title: Phase 6.2.2 — FPExploreRigHost First-Person Explore
roadmap-level: tertiary
phase-number: 6
subphase-index: 6.2.2
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
- fp-explore
- beat-2
- half-a
para-type: Project
roadmap_track: conceptual
factory_track: false
horizon_demo_track: true
links:
- '[[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roll-up-2026-07-15]]'
handoff_readiness: 85
product_factory_run_id: c1dc1d565ea2
parent_secondary: '6.2'
depth_first_backfill: true
demo_loop_beat: 2
persona_id: half_a.conceptual_architect
rollup-detail: '[[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roll-up-2026-07-15]]'
body_compact_at: 2026-07-15
body_compact_queue: followup-deepen-phase622-tertiary-20260716T033640Z
factory_feed_gate_status: green
body_compact_status: complete
body_chars_pre_recompact: 1312
body_chars_claimed: 1101
body_chars_cap: 1200
body_over_cap: false
factory_feed_gate_reason: manual_chat_recompact_1200
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.2.2 — FPExploreRigHost First-Person Explore

Decomposes **beat 2 (FP explore)** from [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **FPExploreRigHost**, **PerspectiveEnvelope** `player_fp`, locomotion/look, `demo.fp_active`.…

## Scope

**In:** host lifecycle; `player_fp` activation (4.1; OQ-6.2.1-003); move/look on `input.*`; `demo.fp_active` on `session.*`; beat 2 gates; **DMPauseGate** respect. **Out:** 6.2.1 spawn; 6.2.3–6.2.8; factory KH; exec — advisory.

## Behavior

awaiting_spawn → activating → exploring → beat_exit | blocked. Spawn_complete + FPRig → `player_fp` → input → emit. Detail → [[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roll-up-2026-07-15]].

## Interfaces

Imports: spawn_complete + FPRig (6.2.1); PerspectiveEnvelope (4.1); PlayRegionHost (6.1.2); `input.*`; DMPauseGate. Exports: `demo.fp_active`; FPRig `fp_active`. Consumers: 6.2.3; beat 6 guard.

## Roll-up

Edges/OQs → [[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roll-up-2026-07-15]].

## Handoff

**85%** — tertiary feedstock. Exec-deferred — advisory. Body ≤1200.
