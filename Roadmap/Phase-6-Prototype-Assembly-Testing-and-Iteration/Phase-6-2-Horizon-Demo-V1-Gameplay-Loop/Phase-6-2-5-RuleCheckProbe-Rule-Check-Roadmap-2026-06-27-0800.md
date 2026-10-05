---
title: Phase 6.2.5 — RuleCheckProbe Rule Check
roadmap-level: tertiary
phase-number: 6
subphase-index: 6.2.5
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
- rule-check
- beat-5
- half-a
para-type: Project
roadmap_track: conceptual
factory_track: false
horizon_demo_track: true
links:
- '[[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]'
- '[[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roll-up-2026-07-16]]'
handoff_readiness: 85
product_factory_run_id: c1dc1d565ea2
parent_secondary: '6.2'
depth_first_backfill: true
demo_loop_beat: 5
persona_id: half_a.conceptual_architect
rollup-detail: '[[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roll-up-2026-07-16]]'
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase625-tertiary-20260716T054400Z
factory_feed_gate_status: green
body_compact_status: complete
body_chars_pre_recompact: 1378
body_chars_claimed: 1098
body_chars_cap: 1200
body_over_cap: false
factory_feed_gate_reason: manual_chat_recompact_1200
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.2.5 — RuleCheckProbe Rule Check

Decomposes **beat 5 (Rule check)** from [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **RuleCheckProbe**, post-tick **RuleContextFrame** stub + **demo_ruleset** → one **RuleEngineCore** pass →…

## Scope

**In:** probe lifecycle; frame stub; demo_ruleset; single eval; RuleEffectBus pass/fail; `demo.rule_check_complete`; beat 5 gates; halt-on-fail default. **Out:** 6.2.1–6.2.4; 6.2.6–6.2.8; PluginLoader; RuleConflictArbiter; spell/quest plugins; factory; exec — advisory.

## Behavior

awaiting_context → frame_built → evaluating → pass | fail | blocked. Detail → [[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roll-up-2026-07-16]].

## Interfaces

Imports: `demo.sim_tick_committed` + log row (6.2.4); RuleEngineCore/RuleContextFrame/RuleEffectBus (5.1). Exports: `rule.demo_pass`/`rule.demo_fail`; `demo.rule_check_complete`. Consumers: 6.2.6 DMCam; 6.2.8 feedback.

## Roll-up

Edges/OQs → [[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roll-up-2026-07-16]].

## Handoff

**85%** — tertiary feedstock. Exec-deferred — advisory. Body ≤1200.
