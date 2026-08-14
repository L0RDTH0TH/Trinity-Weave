---
title: Phase 1.3.2 — SeedSnapshotAuthority Contract
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.3.2
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 79
factory_feed_gate_status: green
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- modularity-seams
- seed-snapshot
- safety-invariants
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roll-up-2026-06-29]]'
links:
- '[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]]'
- '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 1.3.2 — SeedSnapshotAuthority Contract

**SeedSnapshotAuthority** — immutable pre-mutation snapshot before manifest commit, DM structural regen, or ruleset swap. Parent [[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]; nouns only.

## Scope

**In:** trigger matrix; SeedSnapshot schema; ordering vs 1.3.1 registry + 1.1.2 canon; rollback intent. **Out:** DryRun/Provenance (1.3.3); storage; factory catalog.

## Behavior

Registry `published` before `gen.stage.*` capture; capture → seal → proceed; seam swap aborts to last snapshot; rollback invalidates event log tail.

## Roll-up

Tables + edge cases → [[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roll-up-2026-06-29]].

## Handoff

**79%** — NL complete; detail in rollup. Execution-deferred: vault storage, serialization.
