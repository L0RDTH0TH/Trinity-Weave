---
title: Phase 6.2.3 — IntentPipelineStub Intent Stub
roadmap-level: tertiary
phase-number: 6
subphase-index: 6.2.3
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
- intent-stub
- beat-3
- half-a
para-type: Project
roadmap_track: conceptual
factory_track: false
horizon_demo_track: true
links:
- '[[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]'
- '[[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roll-up-2026-07-16]]'
handoff_readiness: 85
product_factory_run_id: c1dc1d565ea2
parent_secondary: '6.2'
depth_first_backfill: true
demo_loop_beat: 3
persona_id: half_a.conceptual_architect
rollup-detail: '[[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roll-up-2026-07-16]]'
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase622-tertiary-20260716T033640Z
factory_feed_gate_status: green
body_compact_status: complete
body_chars_pre_recompact: 1243
body_chars_claimed: 1067
body_chars_cap: 1200
body_over_cap: false
factory_feed_gate_reason: manual_chat_recompact_1200
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.2.3 — IntentPipelineStub Intent Stub

Decomposes **beat 3 (Intent stub)** from [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **IntentPipelineStub**, interact sample → `intent.demo_interact` on `input.*`, `demo.intent_labeled` on…

## Scope

**In:** stub lifecycle; interact capture; `intent.demo_interact` on `input.*` (1.1); `demo.intent_labeled` on `session.*`; beat 3 gates; no canon touch. **Out:** 6.2.1–6.2.2; 6.2.4–6.2.8; IntentResolver/CanonRegistry; factory; exec — advisory.

## Behavior

awaiting_fp → awaiting_interact → labeling → labeled | blocked. Detail → [[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roll-up-2026-07-16]].

## Interfaces

Imports: `demo.fp_active` + interact (6.2.2); InputIntent/`input.*` (1.1); PerspectiveEnvelope self (4.1); DMPauseGate. Exports: `intent.demo_interact`; `demo.intent_labeled`. Consumers: 6.2.4 SimTickStub.

## Roll-up

Edges/OQs → [[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roll-up-2026-07-16]].

## Handoff

**85%** — tertiary feedstock. Exec-deferred — advisory. Body ≤1200.
