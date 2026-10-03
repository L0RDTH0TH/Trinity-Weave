---
title: Phase 1.1 — Layer Decoupling and Interface Contracts
roadmap-level: secondary
phase-number: 1
subphase-index: '1.1'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 82
branch_open: false
factory_feedstock_slice: phase_1_secondary_tree
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-1
- layer-decoupling
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-1-1-Session-Composer-and-Layer-Graph-Bootstrap-Roadmap-2026-06-29-0847]]'
- '[[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]'
- '[[Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roadmap-2026-06-29-1007]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 1.1 — Layer Decoupling and Interface Contracts

Decompose Genesis Mythos into named runtime layers with explicit contracts so world state, simulation, rendering, input, and presentation can evolve independently. This slice establishes **nouns and boundaries** — not implementation paths.

## Scope

**In scope:** four primary runtime layers (WorldState, Simulation, Presentation, InputIntent); bus topic registry draft; canon-commit boundary as a read-only gate adjacent to sim commit; session-scoped composition root (conceptual DI) over global gameplay loops; interface expectations between layers.

**Out of scope:** Godot folder layout, C# interfaces, factory catalog rows, proc-gen DAG stage registry (deferred to 1.2), execution-track pseudo-code, rollup HR gates (execution-deferred / advisory on conceptual track).

## Behavior

**Actors:** Session composer (bootstraps layer graph per play session), WorldState projector (read models from event log), Simulation tick orchestrator, Presentation shell (FP player + DM rail surfaces), InputIntent router (player-lite + DM adjudication envelopes).

**Ordering:** (1) declare layer IDs and ownership; (2) define bus event categories (`canon.*`, `sim.*`, `session.*`, `presentation.*`); (3) document canon validator as read-only dry-run on proposals before any sim write; (4) bind session composer as the only authority that wires concrete implementations — no global autoload gameplay loops for session-bound behavior.

**Inputs / outputs:** InputIntent emits validated intent envelopes; Simulation consumes accepted canon facts and emits domain events; WorldState projects snapshots for Presentation; Presentation never mutates sim state directly.

## Interfaces

| Layer | Upstream guarantees | Downstream expectations |
|-------|---------------------|-------------------------|
| **WorldState** | Append-only event categories; snapshot projections for rewind/replay | Simulation and Presentation read via query handles only |
| **Simulation** | Deterministic tick contract; no render scene mutation | Emits `sim.*` events; respects canon-commit boundary |
| **Presentation** | Mode graph (FP default, DM WorldCam/MapCam/Sensorium Attach) | Subscribes to projected state; routes intents upward |
| **InputIntent** | Agency delegation envelopes (self, dominate, absent-proxy) | Routes to Simulation only after canon gate passes |

**Adjacent slices:** Phase 1.2 owns proc-gen DAG edges; Phase 1.3 owns modularity seams and seed/dry-run invariants. Phase 1.1 exports **layer IDs** and **bus category registry** as stable names for catalog mint.

## Edge cases

- **Partial session bootstrap:** Session composer must tolerate missing optional layers (e.g. off-screen sim deferred) without collapsing the graph — document degraded mode as explicit `session.degraded` bus event.
- **Canon vs sim race:** Proposals in `proposed` state must not reach Simulation; validator gate is read-only — no side effects on rejection.
- **DM Sensorium Attach:** Read-only perception bind — must not be confused with agency delegation pilot envelope (Phase 4 cross-ref).
- **Rollback:** Event log + snapshot pattern (influence: WorldLines) is the continuity backbone — Presentation reads projections, not live mutation.

## Open questions

- Exact bus serialization format — deferred to execution track (conceptual names only here).
- Whether `ToneProfile` bundles attach at session composer or canon-commit boundary — lean session 0 attestation at `accepted` stage per PMG canon pipeline.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — four layers + bus registry; execution paths deferred |
| Behavior (actors, ordering) | pass | § Behavior — session composer, canon gate, bus categories |
| Interfaces (adjacent contracts) | pass | § Interfaces — layer table + 1.2/1.3 adjacency |
| Edge cases | pass | § Edge cases — degraded session, canon race, rollback |
| Open questions | pass | § Open questions — bus format deferred to execution |
| Pseudo-code readiness | pass | § Pseudo-code readiness — sketchable without API signatures |
| **`handoff_readiness` aggregate** | **82%** | factory feed tertiary tree; 1.1.1–1.1.3 minted; **1.1 branch closed** |

> Execution-deferred / advisory on conceptual track: Godot folder layout, typed bus serialization, factory catalog rows, HR rollup gates — resolved on execution track or factory harness (`1373c0c3408d`).

## Pseudo-code readiness

A reader can sketch layer interfaces and bus topic tables without guessing core behavior. No API signatures required on conceptual track; execution deepen will mint typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

**Key takeaways** (from chain research consumable `Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z`):

- Canon pipeline needs explicit state machine + read-only validator gate before sim writes
- Proc-gen graph = stage DAG with deterministic compile stage (names reserved for 1.2)
- Living world continuity = append-only event log + snapshot projections
- Godot greenfield: session-scoped DI over global autoload gameplay loops
- Half A must mint catalog rows before execution-track deepen

**Links**

- [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]
- [[genesis-mythos-master-goal]] — perspective split, canon pipeline `proposed → accepted → hooked → sim-active`

## Tertiary branch (1.1.x)

| Index | Note | Status |
|-------|------|--------|
| 1.1.1 | [[Phase-1-1-1-Session-Composer-and-Layer-Graph-Bootstrap-Roadmap-2026-06-29-0847]] | complete — SessionComposer + LayerGraph bootstrap |
| 1.1.2 | [[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]] | complete — BusCategoryRegistry + CanonCommitBoundary |
| 1.1.3 | [[Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roadmap-2026-06-29-1007]] | complete — per-layer interface contract tables |

**Branch status:** **closed** — 1.1 tertiary tree complete (2026-06-29). Next factory feed work: Phase 1.3 tertiaries.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
