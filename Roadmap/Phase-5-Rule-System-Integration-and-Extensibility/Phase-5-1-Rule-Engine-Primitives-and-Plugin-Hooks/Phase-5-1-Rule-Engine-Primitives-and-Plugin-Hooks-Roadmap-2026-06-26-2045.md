---
title: Phase 5.1 — Rule Engine Primitives and Plugin Hooks
roadmap-level: secondary
phase-number: 5
subphase-index: '5.1'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
breadth_mint_complete: true
secondary_feedstock_qualified: true
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-5
- rule-engine
- plugin-hooks
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roll-up-2026-07-15]]'
rollup-detail: '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roll-up-2026-07-15]]'
factory_feed_gate_status: green
body_compact_status: complete
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase51-20260716T193932Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 5.1 — Rule Engine Primitives and Plugin Hooks

**RuleEngineCore** + **RulePrimitive** + **RulesetPlugin** / **PluginHookManifest** + **PluginLoader** + **RuleConflictArbiter** + **RuleContextFrame** + **RuleEffectBus**. Spells (5.2) / quest-pressure (5.3) = plugins. Godot wiring exec-deferred.

## Scope

**In:** RuleEngineCore; RulePrimitive; RulesetPlugin; PluginHookManifest; PluginLoader; RuleConflictArbiter; RuleContextFrame; RuleEffectBus; SeamRegistry `rule` (1.3). **Out:** Spell metadata (5.2); quest pressure (5.3); serializers/HR; factory/L5.

## Behavior

Rule = `{condition_set, effect_set, trigger}`. Session-init load; mid-session swaps via ReGenerationIntentQueue (3.3). Arbiter: veto → priority → merge → overflow. EffectBus → 3.1 / 4.1 / 4.3 / IntentResolver. Detail → [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roll-up-2026-07-15]].

## Interfaces

Imports: 1.3 SeamRegistry; 2.2 Canon; 2.3 ToneProfile; 3.1 SimTick/WorldState; 3.3 ReGen; 4.1–4.3 envelopes/guards. Exports: RuleEngineCore + EffectBus + ContextFrame + Arbiter → 5.2/5.3.

## Roll-up

Primitives, PluginHookManifest, EffectBus routes, edges, OQs, tasks → [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roll-up-2026-07-15]].

## Handoff

**80** — NL complete; **5.1.1–5.1.3** minted; **5.1** closed; next DFS **5.2** feedstock. Exec-deferred: Godot wiring, serializers — advisory.
