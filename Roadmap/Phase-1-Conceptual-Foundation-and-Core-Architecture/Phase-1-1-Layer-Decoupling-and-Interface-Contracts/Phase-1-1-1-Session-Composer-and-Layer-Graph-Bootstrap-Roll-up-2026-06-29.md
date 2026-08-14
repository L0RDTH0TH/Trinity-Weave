---
title: Phase 1.1.1 — Roll-up & Session Composer Tables
roadmap-level: rollup
phase-number: 1
subphase-index: 1.1.1
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-1-1-1-Session-Composer-and-Layer-Graph-Bootstrap-Roadmap-2026-06-29-0847]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- rollup
- session-composer
- layer-graph
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Scope (detail)

**In scope:** SessionComposer lifecycle (bootstrap → active → teardown); **LayerGraph** node registry (layer id → implementation binding); mandatory vs optional layer slots; **degraded session** contract when optional layers are absent; prohibition on global gameplay-loop autoloads for session-bound behavior; handoff of layer IDs to downstream slices (bus registry in 1.1.2+, per-layer interface tables in 1.1.3+).

**Out of scope:** Bus topic taxonomy (`canon.*`, `sim.*`, …) — sibling tertiaries; CanonCommitBoundary dry-run gate — 1.1.2; per-layer upstream/downstream guarantee tables — 1.1.3; proc-gen DAG (1.2); factory catalog rows; execution-track pseudo-code.

## Behavior (detail)

**Actors:** SessionComposer (sole wiring authority), LayerGraph (in-memory registry), LayerSlot descriptors (mandatory | optional), SessionLifecycleCoordinator (bootstrap/teardown orchestration).

**Ordering:**

1. Session 0 / play start → SessionComposer receives session manifest (ToneProfile ref, seed handles, accepted CanonFacts pointer — not resolved here).
2. LayerGraph instantiated empty; SessionComposer registers four **mandatory** slots: `WorldState`, `Simulation`, `Presentation`, `InputIntent`.
3. Optional slots (e.g. off-screen sim extension) registered only when manifest declares them — absent optional slots do **not** block bootstrap.
4. SessionComposer binds concrete layer implementations to slots (conceptual binding — no folder paths).
5. SessionLifecycleCoordinator transitions graph `bootstrapping → active`; emits `session.layer_graph_ready` on `session.*` bus (topic name only — serialization deferred).
6. On teardown: reverse order unbind; graph cleared; no dangling global singletons.

**Degraded session:** When one or more **optional** layers are missing, graph enters `degraded` sub-state; SessionComposer emits `session.degraded` with missing slot list; **mandatory** layers must still reach `active`.

**Inputs / outputs:**

- *In:* session manifest handle (opaque at this slice).
- *Out:* populated LayerGraph with four mandatory bindings; `session.layer_graph_ready` or `session.degraded` event intent.

## Interfaces (detail)

**Imports from parent 1.1:** four layer IDs; rule that Presentation never mutates sim state directly; rule that InputIntent routes upward only after canon gate (gate detail in 1.1.2).

**Exports:**

| Export | Consumer |
|--------|----------|
| **LayerGraph schema** (slot id, mandatory flag, binding state) | 1.1.2 bus registry, 1.1.3 interface tables |
| **SessionComposer authority boundary** | Phase 1.2 SeedParser / session 0 close handoff |
| **Degraded session vocabulary** | Phase 1.3 modularity seams |

**Adjacent slices:** [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]] consumes WorldState + Simulation layer IDs after CompiledWorldManifest load — SessionComposer must expose graph read handle, not re-wire mid-session without explicit teardown.

## Edge cases (detail)

- **Double bootstrap:** Second SessionComposer invocation while graph `active` → reject; emit `session.bootstrap_rejected` (no silent rebind).
- **Mandatory slot unbind failure on teardown:** Log + force-clear graph; session must not leave global gameplay hooks attached (aligns with parent rollback / event-log backbone).
- **ToneProfile attach timing:** Whether ToneProfile bundles attach at composer bootstrap vs canon-commit — lean `accepted` stage per parent OQ; document as open question cross-ref, not resolved here.

## Open questions (detail)

- OQ-1.1.1-001: Minimum optional layer set for Horizon M0 — deferred to Phase 6 / Half A catalog.
- OQ-1.1.1-002: Session manifest schema versioning — execution-deferred.
- OQ-1.1.1-003: Hot-swap layer implementation mid-session — out of scope; requires explicit teardown per PMG continuity model.

## Pseudo-code readiness (detail)

A reader can diagram SessionComposer → LayerGraph → four mandatory slots and degraded path without API signatures. Execution track mirrors under `Roadmap/Execution/` parallel spine when execution deepen begins.

## Handoff readiness (detail)

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — SessionComposer, LayerGraph; bus taxonomy deferred to 1.1.2+ |
| Behavior (actors, ordering) | pass | § Behavior — bootstrap → active → teardown; degraded session contract |
| Interfaces (adjacent contracts) | pass | § Interfaces — LayerGraph schema exports to 1.1.2 / 1.1.3 siblings |
| Edge cases | pass | § Edge cases — double bootstrap, teardown failure, ToneProfile timing OQ |
| Open questions | pass | § Open questions — OQ-1.1.1-001..003 documented |
| Pseudo-code readiness | pass | § Pseudo-code readiness — diagrammable without API signatures |
| **`handoff_readiness` aggregate** | **77%** | factory feed tertiary mint; **1.1 branch closed** (1.1.1–1.1.3 complete) |
