---
title: Phase 2.2.1 — ConflictArbiter Resolution Policy
roadmap-level: tertiary
phase-number: 2
subphase-index: 2.2.1
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feedstock_slice: phase_2_tertiary_tree
body_compact_status: complete
factory_feed_gate_status: green
branch_open: false
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-2
- canon-registry
- conflict-arbiter
- intent-resolver
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roll-up-2026-06-29]]'
links:
- '[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]'
- '[[Phase-2-1-1-CollaborativeRefinementLoop-Pause-Point-Registry-Roadmap-2026-06-29-1830]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 2.2.1 — ConflictArbiter Resolution Policy

**ConflictArbiter** resolution policy when **CanonRegistry** receives contradictory **CanonFact** proposals. Parent [[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]; nouns + bus contracts only.

## Scope

**In:** modes (`reject_new`, `prefer_incumbent`, `table_merge`, `defer_to_dm`, `split_thread`); **ConflictManifest**; **ResolutionPolicyBinding**; **MergeTablePolicy**; `session.*`/`canon.*`. **Out:** DM workbench (Phase 4+), LoreHook detail, ToneProfile (**2.3**), factory/L5, execution merge.

## Behavior

Validator → classify → manifest → auto-reject or DM queue (`session.conflict_surfaced`). Five conflict classes; six-step loop; mid-pipeline compile never mutates **CompiledWorldManifest**.

## Interfaces

Imports: 2.2 lifecycle, 1.2.2 intent, 2.1.1 table merge, 1.3 dry-run. Exports: policy index, bindings, provenance audit → factory mint / execution mirror.

## Roll-up

Tables, edge cases, handoff → [[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roll-up-2026-06-29]].

## Handoff

**80%** — NL complete; detail in rollup. Execution-deferred: DM widgets, Godot merge, factory catalog, HR gates.
