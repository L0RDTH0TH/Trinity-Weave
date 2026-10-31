---
title: Phase 5.3 — Quest Pressure from Canon Graph
roadmap-level: secondary
phase-number: 5
subphase-index: '5.3'
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
- quest-pressure
- canon-graph
- rule-engine
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
- '[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-5-3-Quest-Pressure-from-Canon-Graph-Roll-up-2026-07-15]]'
rollup-detail: '[[Phase-5-3-Quest-Pressure-from-Canon-Graph-Roll-up-2026-07-15]]'
factory_feed_gate_status: green
body_compact_status: complete
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase53-20260716T201302Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 5.3 — Quest Pressure from Canon Graph

**QuestPressureManifest** + **QuestPressureRegistry** + **CanonGraphPressureIndex** + **QuestPressureRulePlugin**. Urgency from **CanonRegistry** graph via **RuleEngineCore** → **RuleEffectBus** `quest_pressure`. Composes with 5.2 under **RuleConflictArbiter**. Conceptual — quest UI exec-deferred.

## Scope

**In:** QuestPressureManifest; QuestPressureRegistry; CanonGraphPressureIndex; QuestPressureSignal; QuestPressureRulePlugin; quest_pressure_snapshot; RuleEffectBus quest_pressure; priority bands 200–299. **Out:** Quest scripts; Godot journal; CanonRegistry writes; spell metadata (5.2); factory/L5.

## Behavior

Index → signals (`thread_urgency`, `entity_stake`, `location_tension`, `hook_decay`) → `pressure_above` / `thread_decay_is` → bus. Default `defer_to_spell`. Detail → [[Phase-5-3-Quest-Pressure-from-Canon-Graph-Roll-up-2026-07-15]].

## Interfaces

Imports: 5.1 RuleEngineCore/EffectBus/Arbiter/SeamRegistry; 5.2 SpellMetadata (optional); 2.2 CanonRegistry/LoreHookRegistry/IntentResolver; 3.x SimTick/WorldEventLog. Exports: manifests + index + bands → Phase 6.

## Roll-up

Schemas, signals, bands, edge cases, OQs, tasks → [[Phase-5-3-Quest-Pressure-from-Canon-Graph-Roll-up-2026-07-15]].

## Handoff

**80** — NL complete; secondary feedstock qualified; next DFS **6.1**. Exec-deferred: quest journal, serializers — advisory.
