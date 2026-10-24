---
title: Phase 1.1.3 — Per-Layer Interface Contract Tables
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.1.3
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: green
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- layer-decoupling
- interface-contracts
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roll-up-2026-06-29]]'
links:
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[Phase-1-1-1-Session-Composer-and-Layer-Graph-Bootstrap-Roadmap-2026-06-29-0847]]'
- '[[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]'
- '[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 1.1.3 — Per-Layer Interface Contract Tables

Per-layer contract tables for **WorldState**, **Simulation**, **Presentation**, and **InputIntent**. Integrates [[Phase-1-1-1-Session-Composer-and-Layer-Graph-Bootstrap-Roadmap-2026-06-29-0847]] and [[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]. Nouns only.

## Scope

**In:** four per-layer tables + cross-layer invariant summary; degraded-session propagation; canon-gate placement per layer. **Out:** bus serialization; factory catalog; proc-gen DAG (1.2); modularity seams (1.3).

## Behavior

ContractTableCurator binds read-only tables after LayerGraph ready + BusCategoryRegistry manifest; emits `session.contract_tables_bound`. Teardown discards tables with graph.

## Roll-up

Full tables + invariants + edge cases + OQs → [[Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roll-up-2026-06-29]].

## Handoff

**80%** — NL complete; detail in rollup. **1.1 branch closed.** Execution-deferred: typed query handles, bus serialization, factory catalog.
