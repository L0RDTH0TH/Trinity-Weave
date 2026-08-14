---
title: Phase 1.3.1 — SeamRegistry Canonical Index
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.3.1
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 78
factory_feed_gate_status: green
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- modularity-seams
- seam-registry
- safety-invariants
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-1-3-1-SeamRegistry-Canonical-Index-Roll-up-2026-06-29]]'
links:
- '[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roadmap-2026-06-29-1007]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 1.3.1 — SeamRegistry Canonical Index

**SeamRegistry** — session-scoped replaceability catalog (generation stages, rule hooks, bus subscriptions, input parsers): **seam id**, **port owner**, **swap contract**, **neighbor guarantee**. Parent [[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]; nouns only.

## Scope

**In:** seam id vocabulary; four families; port bindings; swap fields; draft→published→deprecated; 1.2.1 stage rows; 1.1.3 layer owners. **Out:** SeedSnapshot (1.3.2); DryRun/Provenance (1.3.3); execution ports; factory catalog.

## Behavior

RegistryPublisher ingests 1.2.1 → generation family; completeness gates `published`; PortBinder session-scoped.

## Roll-up

Catalog tables, swap summary, edge cases, OQs → [[Phase-1-3-1-SeamRegistry-Canonical-Index-Roll-up-2026-06-29]].

## Research integration

**Run:** research-20260629T143625Z-3a7574ed · cto_brief. Body oversize blocker; compact before L5 remint (1.2.1/1.2.2 pattern).

## Handoff

**78%** — NL complete; detail in rollup. **1.3 branch closed.** Execution-deferred: port signatures, persistence.
