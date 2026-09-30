---
title: Phase 1.2.1 — Stage DAG Node Contracts
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.2.1
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
- proc-gen
- dag-contracts
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roll-up-2026-06-29]]'
links:
- '[[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]'
- '[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 1.2.1 — Stage DAG Node Contracts

**StageNode** contracts for proc-gen DAG: I/O manifests, edge registry, ToneProfile injection, `gen.stage.*` seams. Parent [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]; intent → [[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]].

## Scope

**In:** `terrain→biomes→POIs→entities→sim_bootstrap`; manifest contracts, edge registry, ToneProfileInjector, `session.stage_*`. **Out:** IntentResolver (1.2.2), Godot, factory/L5.

## Behavior

DAGValidator → StageOrchestrator dispatch → per-stage emit → DeterministicCompiler after `sim_bootstrap`. ToneProfileInjector cross-cut (no DAG slot).

## Interfaces

Imports: SeedBundle, DAGValidator (1.2); WorldState IDs (1.1). Exports: registries + seams → Phase 2, 1.3.3 `dag.preflight`.

## Roll-up

Tables, invariants, pseudo-code, handoff → [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roll-up-2026-06-29]].

## Handoff

**80%** — NL complete; tables in rollup. Execution-deferred serializers/executors. **1.2 branch closed.**
