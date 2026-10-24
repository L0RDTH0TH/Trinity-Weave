---
title: Phase 5.1.3 — RuleConflictArbiter / RuleEffectBus
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.3"
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: red
created: 2026-07-16
tags: [roadmap, genesis-mythos-master, phase-5, rule-conflict-arbiter, rule-effect-bus]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]"
  - "[[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]"
  - "[[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]"
  - "[[genesis-mythos-master-goal]]"
  - "[[Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roll-up-2026-07-16]]"
rollup-detail: "[[Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roll-up-2026-07-16]]"
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
factory_feed_gate_reason: body_over_cap:1353>1200
body_over_cap: true
body_chars_claimed: 1353
body_chars_cap: 1200
---

## Phase 5.1.3 — RuleConflictArbiter / RuleEffectBus

**RuleConflictArbiter** = veto → priority → merge → overflow. **RuleEffectBus** = routes resolved effects to 3.1 / 4.1 / 4.3 / IntentResolver. Manifest priority/veto from **5.1.2**; Frame/Primitives from **5.1.1**. No Godot / factory/L5.

## Scope

**In:** Arbiter order; `rule_conflict_max_active`; EffectBus channels (`world_delta`, `world_event`, `agency_transition`, `perspective_transition`, `canon_proposal`, `tone_bias`); async dispatch; DMPauseGate on `world_delta`.

**Out:** Core/Primitive/Frame (`5.1.1`); Plugin/Manifest/Loader (`5.1.2`); spell (5.2); quest (5.3); DM priority stack (OQ-5.1-003); factory/L5.

## Behavior

Effects → Arbiter: veto (`veto_reason`) → priority (lower wins) → merge commutative → overflow `arbiter_overflow` top-N. Bus → subsystem queues; SimTickPipeline (3.1) order. Detail → [[Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roll-up-2026-07-16]].

## Interfaces

**Imports:** Frame+Primitives (`5.1.1`); Manifest priority/veto (`5.1.2`); DMPauseGate (3.1); envelopes (4.3/4.1); IntentResolver (2.2). **Exports:** Arbiter+EffectBus → **5.2**/**5.3**.

## Roll-up

Channels, edges, OQs → rollup.

## Handoff

**80%** — arbiter/bus nouns explicit. Exec-deferred — advisory. Body **1353>1200**; slice red. Next DFS **self** recompact ≤1200 — not factory/L5.
