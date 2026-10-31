---
title: Phase 2.1 — Generation Pipeline Stages
roadmap-level: secondary
phase-number: 2
subphase-index: '2.1'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 78
factory_feedstock_slice: phase_2_secondary_tree
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-2
- generation-pipeline
- proc-gen
para-type: Project
roadmap_track: conceptual
branch_open: true
phase_2_tertiary_progress: 25
links:
- '[[Phase-2-1-1-CollaborativeRefinementLoop-Pause-Point-Registry-Roadmap-2026-06-29-1830]]'
- '[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 2.1 — Generation Pipeline Stages

Materialize the **collaborative world-forge pipeline** from session 0 through simulation bootstrap: seed parsing → terrain → biomes → POIs → entities → simulation bootstrap. This slice names **Phase 2 stage executors**, collaborative refinement loops, and safety hooks — building on Phase 1 DAG contracts without Godot implementation paths.

## Scope

**In scope:** **SeedParser** assembly of **SeedBundle** from session 0 outputs (map seed, ToneProfile choice, accepted CanonFacts summary); **GenerationPipeline** orchestration wrapping DAGValidator + StageOrchestrator; per-stage **executor contracts** for `terrain`, `biomes`, `POIs`, `entities`, `sim_bootstrap`; **CollaborativeRefinementLoop** (system proposes scaffolds, table accepts/revises before compile); **DryRunValidator** + **SeedSnapshot** gates from Phase 1.3 at pipeline entry and pre-compile; **DeterministicCompiler** handoff emitting **CompiledWorldManifest**; **WorldEventLog** initialization contract.

**Out of scope:** Canon registry + IntentResolver population detail (secondary **2.2**); **ToneProfile** profile bundle on world seed (secondary **2.3**); Godot C# stage implementations; factory catalog row shapes; execution-track typed interfaces and rollup HR gates (execution-deferred / advisory on conceptual track); off-screen faction tick behavior (Phase 3).

## Behavior

**Actors:**

| Actor | Role |
|-------|------|
| **SeedParser** | Consumes session 0 closure payload: validated map seed, **ToneProfile** selection (required — blocks bundle if absent), DM/table bounds, **accepted** CanonFacts index; emits **SeedBundle** with provenance envelope |
| **DAGValidator** | Pre-flight on stage graph (imported from Phase 1.2); rejects cycles and unresolved dependencies before any stage runs |
| **StageOrchestrator** | Topological dispatch over stage executors; routes failure manifests to error sink |
| **TerrainStageExecutor** | SeedBundle + ToneProfile terrain weights → **TerrainManifest** |
| **BiomeStageExecutor** | TerrainManifest + ToneProfile biome weights → **BiomeManifest** |
| **POIStageExecutor** | BiomeManifest + accepted CanonFact hooks (draft) → **POIManifest** |
| **EntityStageExecutor** | POIManifest + LoreHookRegistry draft → **EntityManifest** |
| **SimBootstrapStageExecutor** | EntityManifest + LoreHookRegistry → **SimGraphSeed** |
| **ToneProfileInjector** | Cross-cutting bias application at each receptive stage (Phase 1.2 contract) |
| **CollaborativeRefinementLoop** | Between stages (optional pause points): presents scaffold deltas to DM/table; only **accepted** revisions mutate downstream inputs |
| **DryRunValidator** | Runs on SeedBundle and again pre-compile; uses **SeedSnapshot** for replay comparison |
| **DeterministicCompiler** | All stage manifests → **CompiledWorldManifest**; byte-stable given identical inputs |
| **WorldEventLogInitializer** | Seeds append-only log from CompiledWorldManifest for world continuity backbone |

**Ordering:**

1. Session 0 closes → **SeedParser** forms **SeedBundle** + **ProvenanceEnvelope** (validates ToneProfile bundle present — missing tone blocks formation per **2.3**)
2. **DryRunValidator** dry-run on SeedBundle (no world mutation)
3. **DAGValidator** pre-flight
4. **CollaborativeRefinementLoop** optional gate: DM may request scaffold preview before terrain commit
5. Stage traversal: `terrain → biomes → POIs → entities → sim_bootstrap` with **ToneProfileInjector** at receptive nodes
6. **IntentResolver** cross-cut at POIs/entities/sim_bootstrap (boundary with **2.2** — this slice documents stage I/O only; resolver detail deferred)
7. **DryRunValidator** pre-compile check against **SeedSnapshot**
8. **DeterministicCompiler** → **CompiledWorldManifest**
9. **WorldEventLogInitializer** → session-ready world state handoff to Phase 3 simulation entry

**Inputs / outputs:**

- *Into pipeline:* Session 0 closure (SeedBundle ingredients), SeamRegistry generation ports (Phase 1.3)
- *Out of pipeline:* CompiledWorldManifest, initialized WorldEventLog, SimGraphSeed for simulation bootstrap

## Interfaces

**Imports from Phase 1:**

| Phase 1 export | How 2.1 consumes it |
|----------------|----------------------|
| Stage DAG contracts (1.2.1) | Stage executor identities and manifest I/O table |
| Intent pipeline (1.2.2) | CanonFact lifecycle boundaries at POI/entity stages — detail in 2.2 |
| SeamRegistry + generation ports (1.3) | Swap stage executors without renegotiating DAG topology |
| SeedSnapshot + DryRunValidator (1.3) | Entry and pre-compile safety gates |
| `session.*` bus (1.1) | `session.seed_bundle_ready`, `session.stage_failed`, `session.world_manifest_ready` |

**Exports to Phase 2 siblings and Phase 3:**

| Export | Consumer |
|--------|----------|
| **GenerationPipeline** orchestration contract | 2.2 canon registry integration; 2.3 ToneProfile bundle attachment |
| **Stage executor registry** (names + manifest types) | Execution track mirror spine; Half A catalog mint |
| **CollaborativeRefinementLoop** pause-point registry | DM workbench UX (Phase 4+) |
| **CompiledWorldManifest** + WorldEventLog init | Phase 3 living simulation entry |

**Adjacent slices:**

- **2.2** owns Canon registry + IntentResolver materialization; 2.1 exposes stage handoff points only.
- **2.3** owns ToneProfile bundle on world seed; 2.1 consumes ToneProfile via SeedParser and ToneProfileInjector.

## Edge cases

- **Session 0 incomplete:** SeedParser rejects bundle formation; pipeline does not start; DM sees explicit missing-field list (not silent defaults on canon).
- **Collaborative loop timeout:** Table does not respond to scaffold preview — default **accept scaffold as proposed** after session policy timeout; event logged on `session.*` bus.
- **Stage partial failure:** Failure manifest routes to error sink; downstream stages blocked; CompiledWorldManifest flagged `incomplete: true`; Presentation surfaces DM recovery options (re-seed stage, skip with degradation).
- **DryRunValidator mismatch:** SeedSnapshot replay differs from live compile → block manifest emit; DM must reconcile seed drift before play.
- **Zero POI / entity yield:** Valid degraded manifest with `sparse_world: true` — not an error; sim_bootstrap may emit empty faction graph (Phase 1.2 contract).
- **ToneProfile missing at SeedParser:** Block **SeedBundle** formation (same severity as missing map seed) — session 0 must select tone before closure; aligns with **2.3** SeedBundle attachment contract.
- **ToneProfile unknown `profile_id` (post-selection):** Medium Fantasy fallback + `session.tone_fallback_applied` before terrain stage — **ToneFallbackResolver** (**2.3**).

## Open questions

- **Refinement loop granularity:** Pause after every stage vs. only after terrain+biomes composite — deferred to DM workbench UX / Half A catalog.
- **Horizon M0 minimum stage subset:** Which executors required for first playable loop — operator attestation via factory catalog, not resolved on conceptual track.
- **CompiledWorldManifest DSL format:** Named requirement here; format locked on execution track / catalog mint.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — stage executors, collaborative loop, compile handoff; 2.2/2.3 boundaries explicit |
| Behavior (actors, ordering) | pass | § Behavior — SeedParser through WorldEventLogInitializer; nine-step ordering |
| Interfaces (adjacent contracts) | pass | § Interfaces — Phase 1 imports + 2.2/2.3 adjacency + Phase 3 export |
| Edge cases | pass | § Edge cases — session 0 incomplete, dry-run mismatch, sparse world, tone missing |
| Open questions | pass | § Open questions — refinement granularity, M0 subset deferred to catalog |
| Pseudo-code readiness | pass | § Pseudo-code readiness — pipeline traceable without API signatures |
| Integration spine (2.2 + 2.3) | pass | § Responsibilities — resolver cross-cuts + ToneProfile bundle attachment closed |
| **`handoff_readiness` aggregate** | **78%** | factory feed gate reconcile `phase_2_secondary_tree` slice 2.1; **Phase 2 secondary tree complete** (2.2+2.3 qualified 2026-06-29) |

> Execution-deferred / advisory on conceptual track: Godot stage executors, factory catalog rows, CompiledWorldManifest binary format, HR rollup gates — resolved on execution track or factory harness (`1373c0c3408d`).

## Pseudo-code readiness

A reader can trace seed parse → dry-run → DAG validate → optional collaborative gates → stage traversal → pre-compile dry-run → deterministic compile → event log init without guessing stage order or actor ownership. No API signatures on conceptual track; execution deepen mints typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

Builds on Phase 1 research consumption (no new pre-deepen research this run):

- Stage DAG + deterministic compile as first-class rows — [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]
- Collaborative forge aligns with PMG "generation is collaborative dialogue" — scaffolds proposed, table refines
- SeedSnapshot + dry-run gates — Phase 1.3 safety invariants applied at Phase 2 pipeline boundaries

## Responsibilities

- [x] Name GenerationPipeline stage executors and manifest handoffs (seed parsing → sim bootstrap)
- [x] CollaborativeRefinementLoop pause-point registry — [[Phase-2-1-1-CollaborativeRefinementLoop-Pause-Point-Registry-Roadmap-2026-06-29-1830]] (minted 2026-06-29)
- [x] Integration spine with 2.2 canon registry handoffs — [[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]] (minted 2026-06-26; resolver cross-cuts documented in 2.2 §Interfaces)
- [x] Integration spine with 2.3 ToneProfile bundle attachment — [[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]] (minted 2026-06-26; bundle + injector manifests in 2.3 §Interfaces)

## Tasks

- [x] Mint 2.1 secondary with stage executor registry and pipeline ordering
- [x] Tertiary 2.1.1: CollaborativeRefinementLoop pause-point registry — [[Phase-2-1-1-CollaborativeRefinementLoop-Pause-Point-Registry-Roadmap-2026-06-29-1830]] (minted 2026-06-29)
- [x] Handoff closure with 2.2 + 2.3 integration spines — 2.2 [[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]] closed; 2.3 [[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]] closed (2026-06-26)

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
