---
title: Phase 2.2 — Canon Registry + Intent Resolver
roadmap-level: secondary
phase-number: 2
subphase-index: '2.2'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 79
factory_feedstock_slice: phase_2_secondary_tree
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-2
- canon-registry
- intent-resolver
- proc-gen
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]]'
- '[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 2.2 — Canon Registry + Intent Resolver

Materialize the **collaborative canon backbone** for world generation: a durable **CanonRegistry** that tracks facts from session 0 through simulation-active hooks, and an **IntentResolver** that routes player/DM intents into accepted canon, LoreHookRegistry entries, and stage inputs for the Phase 2 generation pipeline. This slice names registry actors, lifecycle states, resolver routing rules, and integration handoffs with **2.1** stage executors — without Godot implementation paths or execution-track rollup gates.

## Scope

**In scope:** **CanonRegistry** storage and indexing of **CanonFact** records with lifecycle `proposed → accepted → hooked → sim-active`; **IntentResolver** ingestion from session 0 intent inbox, DM workbench revisions, and player-lite submissions; **LoreHookRegistry** as the hook projection layer consumed by POI/entity/sim_bootstrap stages; **CanonFactValidator** (schema + table-policy gates before accept); **HookMaterializer** bridging accepted facts to systemic hooks; **ProvenanceEnvelope** attachment on every registry mutation; **RegistrySnapshot** for dry-run replay alignment with Phase 1.3 **SeedSnapshot**; cross-cut resolver calls at POI/entity/sim_bootstrap boundaries documented in **2.1**.

**Out of scope:** Generation pipeline stage ordering and executor contracts (secondary **2.1**); **ToneProfile** profile bundle on world seed (secondary **2.3**); Godot C# registry implementations; factory catalog row shapes; execution-track typed interfaces, REGISTRY-CI, and rollup HR gates (**execution-deferred / advisory on conceptual track**); off-screen faction simulation detail (Phase 3); DM workbench UI layout (Phase 4+).

## Behavior

**Actors:**

| Actor | Role |
|-------|------|
| **CanonRegistry** | Authoritative store for CanonFacts; indexes by era, entity, location, thread; emits `canon.fact_*` bus events |
| **IntentResolver** | Parses intent payloads (player-lite inbox, session 0 table, DM revise) → candidate CanonFacts; routes to validator |
| **CanonFactValidator** | Enforces schema, table bounds, and duplicate/conflict policy before `accepted`; delegates tone bounds to **ToneCompatibilityGate** |
| **ToneCompatibilityGate** | Validates canon facts against active **ToneProfileBundle** bounds; invoked by CanonFactValidator (**2.3** rules export) |
| **LoreHookRegistry** | Projects `hooked` facts into hook records with sim-facing tags consumed by POI/entity stages |
| **HookMaterializer** | Transforms accepted facts into hook candidates; DM/table accept gate before `hooked` promotion |
| **ProvenanceEnvelope** | Immutable audit trail: source intent id, actor, timestamp, revision chain |
| **RegistrySnapshot** | Point-in-time export for DryRunValidator replay against **2.1** pipeline inputs |
| **ConflictArbiter** | Surfaces contradictory facts to DM workbench; never silent merge on conceptual track |

**CanonFact lifecycle:**

1. **proposed** — IntentResolver creates draft from intent payload; visible in DM workbench queue
2. **accepted** — CanonFactValidator pass + table/DM accept; enters CanonRegistry index
3. **hooked** — HookMaterializer + DM confirm; LoreHookRegistry entry materialized
4. **sim-active** — Generation pipeline or Phase 3 sim consumes hook; WorldEventLog may record ripple

**Resolver routing (high level):**

1. Session 0 closes → bulk accept path for table-agreed canon bundle (with per-fact provenance)
2. Runtime intents → IntentResolver → CanonFactValidator → proposed queue OR auto-reject with reason manifest
3. At **2.1** POI stage → resolver supplies **accepted** location/thread hooks (draft POI hooks from `proposed` blocked)
4. At **2.1** entity stage → LoreHookRegistry lookup by entity/lineage tags
5. At **2.1** sim_bootstrap → sim-active hooks seed faction/thread graph entry points

**Inputs / outputs:**

- *Into registry:* Session 0 canon bundle, player-lite intents, DM revisions, collaborative refinement acceptances from **2.1**
- *Out of registry:* LoreHookRegistry exports, RegistrySnapshot for dry-run, resolver handoff manifests for stage executors

## Interfaces

**Imports from Phase 1 and 2.1:**

| Source | How 2.2 consumes it |
|--------|---------------------|
| Intent pipeline decomposition (1.2.2) | CanonFact lifecycle states and population boundaries |
| Stage DAG contracts (1.2.1) | Stage handoff points where resolver cross-cuts |
| SeamRegistry (1.3) | Swap registry backends without renegotiating resolver API |
| SeedSnapshot + DryRunValidator (1.3) | RegistrySnapshot alignment for pipeline dry-run |
| GenerationPipeline (2.1) | POI/entity/sim_bootstrap resolver invocation points |
| `session.*` bus (1.1) | `session.intent_received`, `session.canon_accepted`, `session.hook_materialized` |

**Exports to Phase 2 siblings and Phase 3:**

| Export | Consumer |
|--------|----------|
| **CanonRegistry** contract + index schema | Execution track mirror; Half A catalog mint |
| **IntentResolver** routing rules | Player-lite inbox (Phase 4+); DM workbench |
| **LoreHookRegistry** | **2.1** POI/entity/sim_bootstrap stages; Phase 3 living simulation |
| **RegistrySnapshot** | DryRunValidator pre-compile checks in **2.1** |

**Adjacent slices:**

- **2.1** owns pipeline orchestration; 2.2 supplies registry/resolver at documented cross-cut points only.
- **2.3** owns ToneProfile bundle; 2.2 invokes **ToneCompatibilityGate** at CanonFactValidator — validates tone compatibility but does not own profile selection.

## Edge cases

- **Conflicting canon from two players:** ConflictArbiter surfaces both; DM must accept one, merge with table policy, or reject — no silent overwrite.
- **Intent arrives mid-pipeline compile:** Resolver queues as `proposed`; does not mutate in-flight CompiledWorldManifest; requires re-compile path via **2.1** DryRunValidator.
- **Orphan hook (entity removed):** LoreHookRegistry marks `dangling: true`; sim_bootstrap may skip or emit degraded graph per Phase 1.2 sparse-world contract.
- **Session 0 bulk accept partial failure:** Valid facts promote to `accepted`; failures return explicit manifest to table — pipeline may proceed with partial canon (logged).
- **RegistrySnapshot drift vs SeedSnapshot:** DryRunValidator blocks compile; DM reconciles before play (same contract as **2.1** seed drift).
- **Empty intent inbox at session 0:** Valid — registry bootstraps with DM-only seed facts; player-lite may populate later under session policy.

## Open questions

- **Hook granularity for first playable loop:** Minimum hooked fact set for M0 — operator attestation via factory catalog, not resolved on conceptual track.
- **Cross-session canon import:** Power-user canon bundle import path — format locked on execution track / catalog mint.
- **Auto-accept policy for low-risk intents:** Session policy toggle — deferred to DM workbench UX / Half A catalog.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — CanonRegistry, IntentResolver, LoreHookRegistry; 2.1/2.3 boundaries explicit |
| Behavior (actors, ordering) | pass | § Behavior — lifecycle states + resolver routing; five-step high-level flow |
| Interfaces (adjacent contracts) | pass | § Interfaces — Phase 1 + 2.1 imports; Phase 3 exports |
| Edge cases | pass | § Edge cases — conflicts, mid-pipeline intent, orphan hooks, empty inbox |
| Open questions | pass | § Open questions — M0 hook minimum, cross-session import deferred |
| Pseudo-code readiness | pass | § Pseudo-code readiness — registry lifecycle traceable without API signatures |
| Integration spine (2.1) | pass | § Responsibilities — POI/entity/sim_bootstrap cross-cuts documented |
| **`handoff_readiness` aggregate** | **79%** | factory feed gate reconcile `phase_2_secondary_tree` slice 2.2; **Phase 2 secondary tree complete** (2.3 qualified 2026-06-29) |

> Execution-deferred / advisory on conceptual track: REGISTRY-CI receipts, Godot registry implementations, factory catalog rows, HR rollup gates — resolved on execution track or factory harness (`1373c0c3408d`).

## Pseudo-code readiness

A reader can trace intent ingest → validate → accept → hook materialize → stage handoff → sim-active promotion without guessing registry ownership or lifecycle order. No API signatures on conceptual track; execution deepen mints typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

Builds on Phase 1 intent pipeline and PMG canon pipeline (`proposed → accepted → hooked → sim-active`):

- Collaborative forge aligns with PMG "intents become facts, then systemic hooks, then visible ripples"
- RegistrySnapshot + dry-run alignment extends Phase 1.3 safety invariants to canon state
- Execution rollup / REGISTRY-CI gates are **execution-deferred / advisory** on conceptual track — out of scope for conceptual completion

## Responsibilities

- [x] Name CanonRegistry + IntentResolver actors and CanonFact lifecycle states
- [x] LoreHookRegistry projection contract and HookMaterializer accept gate
- [x] Integration spine with **2.1** POI/entity/sim_bootstrap resolver cross-cuts
- [x] ConflictArbiter resolution policy — [[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]] (minted 2026-06-29)

## Tasks

- [x] Mint 2.2 secondary with registry/resolver registry and lifecycle ordering
- [x] Tertiary 2.2.1: ConflictArbiter resolution policy — [[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]] (minted 2026-06-29)
- [ ] Optional tertiary: RegistrySnapshot schema detail — **deferred** to refine pass (owner: 2.2 refine)
- [x] Handoff closure with **2.1** integration spines — documented in §Interfaces

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
