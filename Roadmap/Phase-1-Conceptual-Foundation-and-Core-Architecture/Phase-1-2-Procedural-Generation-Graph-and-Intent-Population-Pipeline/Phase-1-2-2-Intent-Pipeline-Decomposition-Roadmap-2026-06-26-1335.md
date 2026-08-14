---
title: Phase 1.2.2 — Intent Pipeline Decomposition
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.2.2
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: green
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-1
- intent-pipeline
- lore-hooks
- canon
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roll-up-2026-06-29]]'
links:
- '[[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 1.2.2 — Intent Pipeline Decomposition

**CanonFacts** (`proposed→accepted→hooked→sim-active`) via **CanonCommitBoundary** → **IntentResolver** cross-cut → **LoreHookRegistry** → **SimGraphSeed**. Parent [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]; DAG from [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]].

## Scope

**In:** intent lifecycle; CanonCommitBoundary; IntentResolver; LoreHookRegistry; SimGraphSeed; `canon.*`. **Out:** DAG I/O (1.2.1); Godot; factory catalog.

## Behavior

CanonCommitBoundary gates reads; IntentResolver cross-cuts POIs/entities/sim_bootstrap; LoreHookRegistry append-only; ConflictAdjudicator on contradictions.

## Interfaces

Imports: `canon.*` (1.1); manifests + SimGraphSeed slot (1.2.1). Exports: registry schema, cross-cut contract, graph seed → Phase 2–3.

## Roll-up

Schema, cross-cut tables, edge cases, pseudo-code, handoff → [[Phase-1-2-2-Intent-Pipeline-Decomposition-Roll-up-2026-06-29]].

## Handoff

**80%** — NL complete; detail in rollup. **1.2 branch closed.** Execution-deferred serializers/executors.
