---
title: "CDR — Phase 1.2.2 Intent pipeline decomposition feedstock"
created: 2026-06-29
tags: [roadmap, cdr, genesis-mythos-master, phase-1, intent-pipeline]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-122-20260629T125200Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: pending_validator
related_research: []
---

## Summary

Chose **LoreHookRegistry typed schema** (faction_seed / tribe_seed / npc_hook entry shapes + invariants) and **per-stage IntentResolver cross-cut registry tables** (POIs / entities / sim_bootstrap read-write contracts) as the authoritative feedstock for tertiary **1.2.2**, matching the factory feed gate pattern on sibling **1.2.1**. Stage DAG manifest I/O remains on **1.2.1** to avoid duplication.

## PMG alignment

Supports PMG session-0 canon → world-gen intent population: accepted CanonFacts flow through CanonCommitBoundary into LoreHookRegistry and SimGraphSeed without execution-track pseudo-code, enabling Half A `pmg_phases` catalog mint.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Merge registry schema into 1.2.1 per-stage tables | Single file | Blurs DAG vs intent cross-cut ownership | 1.2.1 scope is manifest I/O only |
| API-signature pseudo-code at depth 4 | Execution-ready | Violates conceptual_architect persona | Deferred to execution mirror |
| Keep narrative-only Behavior § without typed tables | Smaller note | Failed `feedstock_incomplete` harness gate | Material change required |

## Validation evidence

- Pattern: [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]] per-stage table + edge registry shape
- Pattern: [[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]] CanonFact lifecycle alignment
- Parent: [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]] § Behavior ordering

## Links

- workflow_state log: 2026-06-29 12:55 deepen Phase-1-2-2-Intent-Pipeline-Decomposition
- queue: `resume-deepen-gmm-122-20260629T125200Z`
- persona: `half_a.conceptual_architect`
- product_factory_run_id: `1373c0c3408d`
- validator: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-resume-deepen-gmm-122-20260629T125200Z-20260629T130428Z]]
- ira: [[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-resume-deepen-gmm-122-20260629T125200Z.md]]
