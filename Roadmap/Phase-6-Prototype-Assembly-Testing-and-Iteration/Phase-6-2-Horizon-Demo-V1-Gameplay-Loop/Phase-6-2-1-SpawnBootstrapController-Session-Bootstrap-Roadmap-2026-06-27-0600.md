---
title: Phase 6.2.1 — SpawnBootstrapController Session Bootstrap
roadmap-level: tertiary
phase-number: 6
subphase-index: 6.2.1
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
- spawn-bootstrap
- beat-1
- half-a
para-type: Project
roadmap_track: conceptual
factory_track: false
horizon_demo_track: true
links:
- '[[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
- '[[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
- '[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roll-up-2026-07-15]]'
handoff_readiness: 85
product_factory_run_id: c1dc1d565ea2
parent_secondary: '6.2'
depth_first_backfill: true
demo_loop_beat: 1
rollup-detail: '[[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roll-up-2026-07-15]]'
body_compact_at: 2026-07-15
body_compact_queue: followup-deepen-phase621-tertiary-20260716T030605Z
factory_feed_gate_status: green
body_compact_status: complete
body_chars_pre_recompact: 1382
body_chars_claimed: 1147
body_chars_cap: 1200
body_over_cap: false
factory_feed_gate_reason: manual_chat_recompact_1200
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.2.1 — SpawnBootstrapController Session Bootstrap

Decomposes **beat 1 (Spawn)** from [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **SpawnBootstrapController**, stub facet, **PlayerFPRig** attach, `demo.spawn_complete`. Nouns/ordering only.

## Scope

**In:** controller lifecycle; session handle; stub `demo_shrine_v1`/`demo_shrine_mood`; FPRig → `fp_baseline_rig`; `demo.spawn_complete` on `session.*`; DemoLoopOrchestrator beat 1. **Out:** CompiledWorldManifest; 6.2.2–6.2.8; factory attestation; exec — advisory.

## Behavior

idle → bootstrapping → spawned | failed. Ready + handle → stub → FPRig → emit. Detail → [[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roll-up-2026-07-15]].

## Interfaces

Imports: play_region_ready + receipt (6.1.2); PresentationSessionHandle (6.1.1); fp_baseline_rig; PlayerFPRig (4.1); WorldEventLog (3.1). Exports: spawn_complete; stub ids; FPRig inactive. Consumers: 6.2.2; beat 7.

## Roll-up

Edges/OQs → [[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roll-up-2026-07-15]].

## Handoff

**85%** — tertiary feedstock. Exec-deferred — advisory. Body ≤1200.
