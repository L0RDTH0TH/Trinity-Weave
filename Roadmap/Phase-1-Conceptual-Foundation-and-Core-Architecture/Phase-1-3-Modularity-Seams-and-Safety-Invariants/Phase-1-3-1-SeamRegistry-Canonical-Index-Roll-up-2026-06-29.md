---
title: Phase 1.3.1 — Roll-up & Seam Catalog Tables
roadmap-level: rollup
phase-number: 1
subphase-index: 1.3.1
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- rollup
- seam-registry
- modularity-seams
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Scope (detail)

**In scope:** canonical **seam id** vocabulary; four **seam families** (generation pipeline, rule engine, event bus, input loop); per-seam **port binding** (StageExecutorPort, RulePluginPort, BusSubscriptionPort, IntentParserPort); **swap contract** fields (replaceable unit, fixed neighbor surface, waiver policy); **registry publication lifecycle** (draft → published → deprecated); inheritance of stage-level replaceability labels from [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]; primary **layer owner** mapping per [[Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roadmap-2026-06-29-1007]].

**Out of scope:** SeedSnapshot capture mechanics — delivered at [[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]] (1.3.2); DryRunValidator gate matrix (1.3.3); ProvenanceEnvelope field schema (1.3.3); community packaging of seam docs (Phase 5); execution-track port contracts under `Roadmap/Execution/`; factory catalog row mint.

## Behavior (detail)

**Actors:** SeamRegistry (canonical index authority), RegistryPublisher (validates completeness before `published`), PortBinder (session-scoped wiring delegate — only SessionComposer may invoke per 1.1), SeamDeprecationMarker (retains read-only history for swapped seams).

**Ordering:**

1. After Phase 1.1 layer graph is `active` and Phase 1.2.1 stage DAG edge registry is stable → RegistryPublisher ingests stage replaceability columns from 1.2.1 into **generation** family entries.
2. SeamRegistry starts `draft`; each seam entry receives: `seam_id`, `family`, `port`, `primary_layer`, `replaceable_unit`, `neighbor_guarantee`, `swap_without_renegotiating` list.
3. RegistryPublisher runs **completeness check**: every canonical stage id (`terrain` … `sim_bootstrap`) has a generation seam entry; every bus category class from 1.1.2 has at least one subscription seam template; rule and input families have minimum seed entries (see index table).
4. On pass → status `published`; SessionComposer may resolve concrete implementations via PortBinder; on fail → `registry.incomplete` on `session.*` with missing seam id list.
5. Operator or community swap: touch **only** the named seam's replaceable unit; PortBinder rebinds without mutating neighbor manifest/event contracts.

**Inputs / outputs:**

- *In:* 1.2.1 StageDAG edge registry; 1.1.2 bus category registry; 1.1.3 per-layer contract tables.
- *Out:* **SeamRegistry index** (published catalog); `registry.published` event intent on `session.*`; seam id → port owner lookup for Phase 2 executor mint.

## Canonical seam index (seed catalog)

| seam_id | Family | Port | Primary layer | Replaceable unit | Neighbor guarantee (fixed surface) |
|---------|--------|------|---------------|------------------|-------------------------------------|
| `gen.stage.terrain` | generation | StageExecutorPort | WorldState | terrain stage executor | Consumes SeedBundle; emits TerrainManifest |
| `gen.stage.biomes` | generation | StageExecutorPort | WorldState | biomes stage executor | Consumes TerrainManifest; emits BiomeManifest |
| `gen.stage.pois` | generation | StageExecutorPort | WorldState | POIs stage executor | Consumes BiomeManifest + accepted CanonFacts; emits POIManifest |
| `gen.stage.entities` | generation | StageExecutorPort | WorldState | entities stage executor | Consumes POIManifest + LoreHookRegistry; emits EntityManifest |
| `gen.stage.sim_bootstrap` | generation | StageExecutorPort | Simulation | sim_bootstrap executor | Consumes EntityManifest; emits SimGraphSeed |
| `rule.core.primitives` | rule engine | RulePluginPort | Simulation | ruleset plugin bundle | Core primitive vocabulary + hook schema unchanged |
| `rule.conflict.arbiter` | rule engine | RulePluginPort | Simulation | conflict resolution policy plugin | Simulation tick orchestration unchanged |
| `bus.sim.tick` | event bus | BusSubscriptionPort | Simulation | sim tick subscriber adapter | `sim.*` category delivery semantics per 1.1.2 |
| `bus.canon.commit` | event bus | BusSubscriptionPort | WorldState | canon commit subscriber | `canon.*` category; no ordering unless declared |
| `bus.session.lifecycle` | event bus | BusSubscriptionPort | Presentation | session lifecycle subscriber | `session.*` category |
| `input.intent.player` | input loop | IntentParserPort | InputIntent | player intent parser | Intent envelope shape + canon gate routing |
| `input.intent.population` | input loop | IntentParserPort | InputIntent | population resolver | Same envelope; LoreHookRegistry mediation |

## Swap contract summary

| Family | Swap without renegotiating | Waiver required when |
|--------|---------------------------|----------------------|
| generation | DAG topology, stage ids, manifest type names | Mid-DAG executor swap after partial traversal |
| rule engine | Simulation tick orchestration, WorldState projection | Ruleset without conflict declaration |
| event bus | Category names, delivery semantics | Subscriber assumes global delivery order |
| input loop | Simulation consume path, Presentation feedback | Parser bypasses CanonCommitBoundary |

## Interfaces (detail)

**Imports:**

| Source | Consumption |
|--------|-------------|
| [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]] | Stage id → manifest I/O columns become `gen.stage.*` seam rows |
| [[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]] | Bus category families → subscription seam templates |
| [[Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roadmap-2026-06-29-1007]] | Primary layer owner per seam |

**Exports to siblings / Phase 2+:**

| Export | Consumer |
|--------|----------|
| **SeamRegistry index** (published) | 1.3.2 SeedSnapshotAuthority (trigger matrix cites seam ids); Phase 2 stage executor mint |
| **seam_id vocabulary** | DryRunValidator gate matrix (1.3.2+); ProvenanceRecorder (1.3.3+) |
| **PortBinder authority boundary** | SessionComposer (1.1.1); no global autoload gameplay loops |

## Edge cases

- **Duplicate seam_id:** RegistryPublisher rejects draft publish; no partial catalog — entire registry stays `draft`.
- **Stage added in 1.2 without registry row:** DAGValidator may pass while SeamRegistry incomplete — completeness check blocks `published` until row added (structural safety over silent drift).
- **Deprecated seam mid-session:** SeamDeprecationMarker retains read-only entry; active session continues on bound implementation until teardown; new sessions cannot bind deprecated ids without operator waiver flag.
- **Cross-family swap attempt:** Swapping a rule plugin via a generation port id → PortBinder reject; emit `registry.port_mismatch`.
- **Community seam id collision:** External contributor ids must use reserved prefix `ext.` — core ids (`gen.`, `rule.`, `bus.`, `input.`) are PMG-owned; collisions rejected at publish.

## Open questions

- OQ-1.3.1-001: Minimum published subset for Horizon M0 — defer to Phase 6 / Half A catalog (likely `gen.stage.terrain` through `gen.stage.sim_bootstrap` + `input.intent.player` only).
- OQ-1.3.1-002: Whether ToneProfileInjector touchpoints appear as generation seams or cross-cutting registry annotations — lean cross-cutting annotation on receptive stage rows (inherits 1.2.1).
- OQ-1.3.1-003: Registry versioning when stage DAG adds node — full republish vs incremental delta — defer to execution track; conceptual requires republish gate.

## Pseudo-code readiness

A reader can list twelve seed seam ids, map each to a port and primary layer, and state swap boundaries without API signatures. Execution track mirrors index under `Roadmap/Execution/` parallel spine when execution deepen begins.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — SeamRegistry index; SeedSnapshot delivered at [[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]]; DryRun / Provenance deferred to 1.3.3+ |
| Behavior (actors, ordering) | pass | § Behavior — draft → published lifecycle; PortBinder session scope |
| Interfaces (adjacent contracts) | pass | § Canonical seam index + swap summary |
| Edge cases | pass | § Edge cases — duplicate id, incomplete stage, deprecation, prefix collision |
| Open questions | pass | § Open questions — OQ-1.3.1-001..003 |
| Pseudo-code readiness | pass | § Pseudo-code readiness — index diagrammable without signatures |
| **`handoff_readiness` aggregate** | **78%** | factory feed tertiary mint; **1.3 branch closed** (1.3.1–1.3.3 complete) |

## Tasks

- [x] Per-seam catalog tables + swap contract summary (rollup)
- [x] Behavior ordering + edge cases + OQs
- [x] Handoff readiness matrix
- [x] Body compact 2026-06-29 — dense tables moved from tertiary parent per 1.2.1/1.2.2 pattern
