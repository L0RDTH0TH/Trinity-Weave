---
title: Phase 5 — Rule System Integration and Extensibility
roadmap-level: primary
phase-number: 5
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 84
conceptual_map_slice: roll_up_gates_added
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase
para-type: Project
roadmap_track: conceptual
links:
- '[[genesis-mythos-master-Roadmap-2026-06-26-0914]]'
rollup-detail: '[[Phase-5-Rule-System-Integration-and-Extensibility-Roll-up-2026-07-15]]'
body_compact_at: 2026-07-15
body_compact_queue: followup-deepen-phase5-primary-20260716T003545Z
factory_feed_gate_status: green
body_compact_status: complete
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 5 — Rule System Integration and Extensibility

RPG mechanics with open-source remixing. Core rule engine + plugins; spell agency/perspective metadata; quest pressure from canon graph; community seams.

- [x] 5.1 Rule engine + plugin hooks — [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045|5.1]]
- [x] 5.2 Spell agency/perspective metadata — [[Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115|5.2]]
- [x] 5.3 Quest pressure from canon graph — [[Phase-5-3-Quest-Pressure-from-Canon-Graph-Roadmap-2026-06-26-2142|5.3]]

## Scope

In: 5.1 RuleEngineCore/RulePrimitive/RulesetPlugin/RuleConflictArbiter/RuleEffectBus; 5.2 SpellAgencyPerspectiveManifest/DominateSpellBinding via AgencyEnvelope (4.3) + PerspectiveEnvelope (4.1); 5.3 QuestPressureManifest/CanonGraphPressureIndex/QuestPressureRulePlugin. Consumes SeamRegistry `rule` (1.3), CanonRegistry (2.2). Out: Godot C# evaluator, typed DSL, factory/L5, REGISTRY-CI/HR — execution-deferred/advisory.

## Behavior

Actors span 5.1–5.3. Order: 5.1 → 5.2 → 5.3 under RuleConflictArbiter bands (spell 100–199, quest 200–299). Advance 5→6 ~84% (2026-06-26); tertiary 0% OK conceptual_v1.

## Interfaces

Exports: RuleEffectBus; SpellMetadataRegistry; QuestPressureRegistry + CanonGraphPressureIndex. Imports: Agency/Perspective/PilotGraph (4.x); WorldStateCommitter/DMPauseGate (3.x); CanonRegistry (2.x). See 5.1–5.3 links above.

## Edge cases

Partial 5.x ≠ block Phase 6. Dominate via PilotGraph — passenger_fp_overlay only. Quest pressure via IntentResolver only. Spell vs quest priority needs band alignment. Factory/L5 out of scope.

## Roll-up & handoff

Handoff table, gates, open Qs, consistency, dataview → [[Phase-5-Rule-System-Integration-and-Extensibility-Roll-up-2026-07-15]] (84%).

## Subphases

Tree → [[Phase-5-Rule-System-Integration-and-Extensibility-Roll-up-2026-07-15#Subphases & notes|rollup]].
