---
title: Phase 1.1.2 — Roll-up & Bus Registry Tables
roadmap-level: rollup
phase-number: 1
subphase-index: 1.1.2
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- rollup
- bus-registry
- canon-commit
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Scope (detail)

**In scope:** BusCategoryRegistry (authoritative topic namespace); four top-level families (`canon.*`, `sim.*`, `session.*`, `presentation.*`) with subcategory slots; CanonCommitBoundary lifecycle (`proposed → accepted → hooked → sim-active` per [[genesis-mythos-master-goal]] and [[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]); CanonValidator read-only dry-run within `proposed` (emits `canon.validated` | `canon.rejected` without advancing lifecycle state); rejection path that never mutates WorldState or Simulation; topic ownership rules (which layer may publish vs subscribe).

**Out of scope:** Per-layer upstream/downstream guarantee tables — sibling 1.1.3; bus serialization format and typed payloads — execution-deferred; proc-gen DAG stage registry — Phase 1.2; factory catalog rows; Godot signal/autoload wiring; rollup HR gates (execution-deferred / advisory on conceptual track).

## Behavior (detail)

**Actors:** BusCategoryRegistry (namespace curator), CanonCommitBoundary (gate authority), CanonValidator (read-only dry-run evaluator), ProposalIngress (accepts `canon.proposed` envelopes), SimWriteGuard (blocks Simulation until `accepted` or `sim-active`).

**Ordering:**

1. SessionComposer completes LayerGraph (`session.layer_graph_ready` per 1.1.1) — registry is session-scoped but names are global-stable across sessions.
2. BusCategoryRegistry publishes category manifest to all bound layers (conceptual broadcast — no wire format here).
3. Upstream systems emit `canon.proposed` with CanonFact candidates — **never** direct sim writes; lifecycle state remains **`proposed`** until acceptance.
4. CanonValidator evaluates proposal read-only → emits `canon.validated` (pass) or `canon.rejected` (fail, no side effects) — **dry-run signals only**, not lifecycle states.
5. On acceptance path: `canon.accepted` — CanonFact enters registry index per Phase 2.2.
6. Hook materialization: IntentResolver / HookMaterializer → `canon.hooked` when LoreHookRegistry entry is bound (distinct **`hooked`** lifecycle state).
7. Simulation acknowledgment: `canon.sim_active` when Simulation consumes hooked entries; CanonCommitBoundary opens sim-eligible window only after **`hooked`**.
8. Simulation may consume only facts in **`hooked`** or **`sim-active`** state; Presentation and InputIntent observe `canon.*` read-only except intent routing pre-gate.

**Inputs / outputs:**

- *In:* `canon.proposed` envelopes (opaque payload at this slice).
- *Out:* `canon.validated` | `canon.rejected` (dry-run signals within `proposed`) | `canon.accepted` | `canon.hooked` | `canon.sim_active`; registry manifest version handle for 1.1.3 interface tables.

## Interfaces (detail)

**Imports from 1.1.1:** LayerGraph must be `active` or `degraded` before registry bind; `session.degraded` does not skip canon gate — mandatory layers still enforce boundary.

**Exports:**

| Export | Consumer |
|--------|----------|
| **BusCategoryRegistry manifest** (topic → owning layer, pub/sub) | 1.1.3 per-layer interface tables; Phase 1.2 SeedParser / canon pipeline |
| **CanonCommitBoundary states** | Phase 1.2 intent population; Phase 3 DM overwrite policy |
| **SimWriteGuard contract** | Simulation tick orchestrator; WorldState projector |

**Topic families (draft registry):**

| Family | Owner (publish) | Primary subscribers | Notes |
|--------|-----------------|---------------------|-------|
| `canon.*` | Canon pipeline / ProposalIngress | Simulation (post-gate), WorldState (projections) | Validator is read-only |
| `sim.*` | Simulation | WorldState, Presentation (read) | No render mutation |
| `session.*` | SessionComposer / SessionLifecycleCoordinator | All mandatory layers | Includes `session.degraded` |
| `presentation.*` | Presentation shell | InputIntent (mode feedback) | Never mutates sim |

**Adjacent slices:** [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]] hooks CompiledWorldManifest at `canon.accepted`; [[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]] owns seed/dry-run invariants that align with CanonValidator read-only posture.

## Edge cases (detail)

- **Canon vs sim race:** Facts in `proposed` must not reach Simulation even if LayerGraph is `active` — SimWriteGuard is mandatory, not advisory.
- **Validator rejection storm:** Burst `canon.rejected` must not poison session — rate-limit vocabulary deferred to execution; conceptual rule: rejections are idempotent read-only.
- **Partial acceptance batch:** Multi-fact proposals may split — boundary documents per-fact state; batch atomicity is OQ (see below).
- **Degraded session:** Optional layers absent do not bypass CanonCommitBoundary — canon gate applies whenever Simulation slot is bound.
- **Rollback / rewind:** Event log categories must tag `canon.*` transitions for WorldState projector replay — aligns with parent rollback edge case.

## Open questions (detail)

- OQ-1.1.2-001: Batch atomicity for multi-fact `canon.proposed` — all-or-nothing vs per-fact acceptance — lean per-fact with explicit batch correlation id.
- OQ-1.1.2-002: ToneProfile bundle attach point — session composer bootstrap vs `canon.accepted` — cross-ref parent OQ; lean `accepted` per PMG canon pipeline.
- OQ-1.1.2-003: Subcategory depth limit for `sim.*` (per-tick vs per-domain) — defer to Phase 3 tick simulation core.

## Pseudo-code readiness (detail)

A reader can draw the canon state machine, registry table, and gate placement between ProposalIngress and Simulation without API signatures or serialization schemas. Execution track mirrors under `Roadmap/Execution/` parallel spine when execution deepen begins.

## Handoff readiness (detail)

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — registry + CanonCommitBoundary; serialization deferred |
| Behavior (actors, ordering) | pass | § Behavior — proposed → accepted → hooked → sim-active (PMG); validated/rejected are dry-run signals within proposed |
| Interfaces (adjacent contracts) | pass | § Interfaces — registry manifest + topic table + 1.2/1.3 adjacency |
| Edge cases | pass | § Edge cases — race, rejection storm, degraded session |
| Open questions | pass | § Open questions — OQ-1.1.2-001..003 documented |
| Pseudo-code readiness | pass | § Pseudo-code readiness — state machine diagrammable |
| **`handoff_readiness` aggregate** | **78%** | factory feed tertiary mint; **1.1 branch closed** (1.1.1–1.1.3 complete) |
