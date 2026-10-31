---
title: Phase 1.1.3 — Roll-up & Per-Layer Interface Contract Tables
roadmap-level: rollup
phase-number: 1
subphase-index: 1.1.3
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roadmap-2026-06-29-1007]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- rollup
- interface-contracts
- layer-decoupling
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Scope (detail)

**In scope:** four per-layer contract tables (guarantees, expectations, publish/subscribe topics, forbidden actions); cross-layer invariant summary; degraded-session contract propagation per layer; canon-gate placement per layer relative to SimWriteGuard; query-handle vocabulary for WorldState projections.

**Out of scope:** Bus serialization format and typed payloads — execution-deferred; factory catalog rows; proc-gen DAG stage registry — Phase 1.2; modularity seam swap contracts — Phase 1.3; pseudo-code and execution-track mirrors.

## Behavior (detail)

**Actors:** ContractTableCurator (maintains four tables as session-stable reference), LayerGraph (from 1.1.1 — supplies binding state), BusCategoryRegistry (from 1.1.2 — supplies topic ownership), CanonCommitBoundary (from 1.1.2 — gates Simulation writes).

**Ordering:**

1. SessionComposer completes LayerGraph (`session.layer_graph_ready` or `session.degraded` per 1.1.1).
2. BusCategoryRegistry manifest published to all mandatory layers (1.1.2).
3. ContractTableCurator attaches per-layer tables to LayerGraph read handle — tables are **read-only reference** for the session; mutations require explicit teardown + re-bootstrap.
4. Each layer implementation must satisfy its table before SessionLifecycleCoordinator transitions graph to `active`.
5. On teardown: tables discarded with graph — no cross-session leakage of binding-specific overrides.

**Inputs / outputs:**

- *In:* LayerGraph schema, BusCategoryRegistry manifest, CanonCommitBoundary state vocabulary.
- *Out:* four contract tables (this note); `session.contract_tables_bound` intent on `session.*` (topic name only).

## Per-layer contract tables

### WorldState

| Dimension | Contract |
|-----------|----------|
| **Layer ID** | `WorldState` |
| **Mandatory slot** | yes (per 1.1.1) |
| **Upstream guarantees** | Append-only event log for categories `canon.*` (post-gate transitions), `sim.*` (domain events), `session.*` (lifecycle markers); immutable history — no in-place mutation of committed events; snapshot projections materialized on demand for rewind/replay |
| **Downstream expectations** | Simulation and Presentation consume **query handles only** — no direct event-log mutation; projections are **eventually consistent** within tick boundary; rewind requests return consistent snapshot at requested logical time |
| **Publish topics** | none (WorldState is projection sink — events ingested via internal projector, not direct layer publish) |
| **Subscribe topics** | `canon.accepted`, `canon.hooked`, `canon.sim_active`, `sim.*` (domain events), `session.layer_graph_ready`, `session.degraded`, `session.teardown` |
| **Forbidden actions** | Direct writes from Presentation; accepting `canon.proposed` without CanonCommitBoundary advancement; deleting committed log segments |
| **Degraded session** | When optional layers absent, WorldState still projects mandatory `sim.*` and `canon.*` transitions; marks projection gaps explicitly in snapshot metadata |
| **Canon gate relation** | Observes canon lifecycle transitions; does **not** advance lifecycle — CanonCommitBoundary owns state machine |

### Simulation

| Dimension | Contract |
|-----------|----------|
| **Layer ID** | `Simulation` |
| **Mandatory slot** | yes |
| **Upstream guarantees** | Deterministic tick contract within declared seed + ruleset context; tick orchestration emits `sim.*` events only through approved channels; **no render scene mutation**; respects SimWriteGuard — consumes canon facts only in `hooked` or `sim-active` state |
| **Downstream expectations** | WorldState ingests `sim.*` for projection; Presentation reads projected state via query handles; InputIntent receives tick-bound feedback only through Presentation (not direct sim callback) |
| **Publish topics** | `sim.tick_start`, `sim.tick_complete`, `sim.domain_event.*` (per-domain subcategories per OQ-1.1.2-003), `sim.write_rejected` (when SimWriteGuard blocks) |
| **Subscribe topics** | `canon.hooked`, `canon.sim_active`, `session.layer_graph_ready`, `session.degraded`, `input.intent_accepted` (post-gate intents only) |
| **Forbidden actions** | Mutating Presentation scene graph; writing canon facts in `proposed` state; bypassing SimWriteGuard; subscribing to `presentation.*` for control flow |
| **Degraded session** | When optional off-screen sim extension absent, core tick pipeline still runs; deferred domains documented in `sim.degraded_domain.*` events |
| **Canon gate relation** | **SimWriteGuard** enforces boundary — Simulation is the primary gated writer to world-domain state |

### Presentation

| Dimension | Contract |
|-----------|----------|
| **Layer ID** | `Presentation` |
| **Mandatory slot** | yes |
| **Upstream guarantees** | Mode graph operational (FP default; DM WorldCam / MapCam / Sensorium Attach per PMG); subscribes to projected state only; routes player/DM intents **upward** via InputIntent — never downward into Simulation |
| **Downstream expectations** | InputIntent receives mode feedback on `presentation.*`; WorldState projections drive visual state; Simulation never depends on Presentation frame timing for correctness |
| **Publish topics** | `presentation.mode_changed`, `presentation.mode_badge_*`, `presentation.perception_bind` (Sensorium Attach — read-only), `presentation.intent_surface_ready` |
| **Subscribe topics** | WorldState query handles (not bus — conceptual read API); `session.layer_graph_ready`, `session.degraded`, `sim.tick_complete` (for display sync only) |
| **Forbidden actions** | **Any direct Simulation or WorldState mutation**; agency delegation without InputIntent envelope; treating Sensorium Attach as agency pilot |
| **Degraded session** | May reduce visual fidelity when projections incomplete — must surface `presentation.degraded` on `presentation.*` |
| **Canon gate relation** | Read-only observer of `canon.*` — no publish on `canon.*` |

### InputIntent

| Dimension | Contract |
|-----------|----------|
| **Layer ID** | `InputIntent` |
| **Mandatory slot** | yes |
| **Upstream guarantees** | Agency delegation envelopes validated (self, dominate, absent-proxy per PMG); intent envelopes typed at conceptual level; **no sim write** — routes to Simulation only after canon gate passes |
| **Downstream expectations** | Simulation receives `input.intent_accepted` only for gate-passed intents; Presentation receives mode-appropriate feedback; rejected intents return `input.intent_rejected` with reason code |
| **Publish topics** | `input.intent_proposed`, `input.intent_accepted`, `input.intent_rejected`, `input.agency_delegation_changed` |
| **Subscribe topics** | `presentation.mode_changed`, `presentation.intent_surface_ready`, `canon.validated`, `canon.rejected` (for pre-route gating), `session.layer_graph_ready` |
| **Forbidden actions** | Emitting `sim.*` directly; bypassing CanonValidator dry-run path for canon-touching intents; mutating WorldState |
| **Degraded session** | When Presentation degraded, InputIntent still accepts intents but tags `input.degraded_route` |
| **Canon gate relation** | Proposal ingress for player/DM intents that touch canon — must not forward to Simulation until lifecycle reaches **`accepted`** or **`hooked`** (or **`sim-active`**); `canon.validated` / `canon.rejected` are dry-run signals within **`proposed`** only (per 1.1.2) |

## Cross-layer invariant summary

| Invariant | Layers involved | Rule |
|-----------|-----------------|------|
| **I-1.1.3-001** | All | Presentation never mutates sim state — parent § Behavior |
| **I-1.1.3-002** | InputIntent → Simulation | Intents reach Simulation only post canon gate |
| **I-1.1.3-003** | Simulation → WorldState | All world changes flow through `sim.*` events |
| **I-1.1.3-004** | WorldState → Presentation | Read via query handles only |
| **I-1.1.3-005** | SessionComposer | Only authority that binds implementations to slots (1.1.1) |
| **I-1.1.3-006** | CanonCommitBoundary | `proposed` facts never reach Simulation (1.1.2) |
| **I-1.1.3-007** | All mandatory | Degraded session does not bypass invariants — only reduces optional capability |

## Interfaces (detail)

**Imports from siblings:**

| Source | Import |
|--------|--------|
| 1.1.1 | LayerGraph schema, mandatory/optional slots, `session.degraded` vocabulary |
| 1.1.2 | BusCategoryRegistry manifest, topic families, CanonCommitBoundary states, SimWriteGuard |
| Parent 1.1 | Four layer IDs, rollback/event-log backbone |

**Exports:**

| Export | Consumer |
|--------|----------|
| **Per-layer contract tables** (this note) | Phase 1.2 proc-gen handoff; Phase 1.3 modularity seams; Half A catalog stable names |
| **Cross-layer invariant IDs** | Phase 1.3 DryRunValidator + SeedSnapshot contracts |
| **`session.contract_tables_bound`** | Session audit trail |

**Adjacent slices:** [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]] — Simulation + WorldState layer IDs for CompiledWorldManifest load; [[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]] — BusSubscriptionPort inherits subscribe columns from these tables.

## Edge cases (detail)

- **Contract drift mid-session:** Tables are immutable post-bind — implementation swap requires SessionComposer teardown (1.1.1 double-bootstrap rejection applies).
- **Topic not in registry:** Layer must not publish ad-hoc topics — register in BusCategoryRegistry first (execution track) or emit `session.contract_violation` on `session.*`.
- **Query handle stale read:** Presentation must tolerate one-tick staleness; critical DM adjudication uses explicit snapshot request, not live mutation.
- **Cross-layer circular subscribe:** InputIntent must not subscribe to `input.*` echoes — registry enforces acyclic pub/sub per 1.1.2 ownership rules.

## Open questions (detail)

- OQ-1.1.3-001: Query-handle versioning when event log schema evolves — execution-deferred; lean snapshot version tag on projections.
- OQ-1.1.3-002: Whether `sim.domain_event.*` subcategory depth matches Phase 3 tick domains — cross-ref OQ-1.1.2-003.
- OQ-1.1.3-003: Contract table diff across sessions for replay debugging — lean append-only audit on `session.*`, not mutable tables.

## Pseudo-code readiness (detail)

A reader can verify layer boundaries, topic bindings, and canon-gate placement from the four tables without API signatures. Execution track mirrors under `Roadmap/Execution/` parallel spine when execution deepen begins.

## Handoff readiness (detail)

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — four tables + invariants; serialization deferred |
| Behavior (actors, ordering) | pass | § Behavior — bind after LayerGraph + registry |
| Interfaces (adjacent contracts) | pass | § Per-layer contract tables + § Interfaces exports |
| Edge cases | pass | § Edge cases — drift, ad-hoc topics, stale read |
| Open questions | pass | § Open questions — OQ-1.1.3-001..003 documented |
| Pseudo-code readiness | pass | § Pseudo-code readiness — tables diagrammable |
| **`handoff_readiness` aggregate** | **80%** | factory feed tertiary mint; **1.1 branch closed** (1.1.1–1.1.3 complete) |
