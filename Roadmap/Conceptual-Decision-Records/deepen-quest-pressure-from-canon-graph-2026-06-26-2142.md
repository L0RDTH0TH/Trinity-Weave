---
title: "CDR: Quest pressure from canon graph (Phase 5.3)"
created: 2026-06-26
tags: [conceptual-decision-record, genesis-mythos-master, phase-5]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-3-Quest-Pressure-from-Canon-Graph-Roadmap-2026-06-26-2142]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T214200Z-phase5-deepen-5-3
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: reconciled
related_research:
  - "[[.technical/Validator/roadmap-auto-validation-20260626T215000Z-godo-followup-20260626T214200Z-phase5-deepen-5-3]]"
  - "[[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-godo-followup-20260626T214200Z-phase5-deepen-5-3.md]]"
---

## Summary

Chose **CanonGraphPressureIndex** as a read-only projection over **CanonRegistry** / **LoreHookRegistry** graph edges, with **QuestPressureManifest** plugins registering via **SeamRegistry** `rule` family and dispatching through a new **RuleEffectBus** `quest_pressure` channel. Spell vs quest conflicts use static **priority bands** (spell agency 100–199, quest core 200–299) extending 5.2 conventions — resolving OQ-5.1-003 at the conceptual layer as banded static priority, not runtime DM stack.

## PMG alignment

PMG canon pipeline (`proposed → accepted → hooked → sim-active`) and world-continuity goal require quests to integrate with the world graph, not generic fetch loops. **CanonGraphPressureIndex** ties urgency to thread/entity/hook state; **canon_proposal** effects route through **IntentResolver** preserving collaborative canon authority.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Procedural quest template table independent of canon | Simpler authoring for kill-fetch quests | Violates PMG systemic depth; disconnected from canon graph | Rejected — antipattern per PMG |
| Direct **CanonRegistry** writes from quest rules | Faster state mutation | Bypasses **IntentResolver** / DM table authority | Rejected — uses `canon_proposal` + lifecycle gate only |
| Runtime DM-adjustable priority stack (OQ-5.1-003) | Flexible narrative fiat | Scope creep; duplicates **NarrativeDeltaVetoPolicy** | Deferred execution / Half A extensibility seam |
| Merge quest + spell into single manifest type | Fewer plugin types | Blurs 5.2 / 5.3 ownership; harder community remix | Rejected — separate manifests with `spell_interaction_policy` |

## Validation evidence

- Pattern: [[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]] CanonFact lifecycle + LoreHookRegistry
- Pattern: [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]] RuleEffectBus + RuleConflictArbiter
- Pattern: [[Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]] priority_hint + spell_interaction exports
- PMG: [[genesis-mythos-master-goal]] § Canon pipeline + world continuity

## Links

- workflow_state Log: 2026-06-26 21:42 | Phase-5-3-Quest-Pressure-from-Canon-Graph
- queue_entry_id: godo-followup-20260626T214200Z-phase5-deepen-5-3
- product_factory_run_id: f35ff65cfb4f
