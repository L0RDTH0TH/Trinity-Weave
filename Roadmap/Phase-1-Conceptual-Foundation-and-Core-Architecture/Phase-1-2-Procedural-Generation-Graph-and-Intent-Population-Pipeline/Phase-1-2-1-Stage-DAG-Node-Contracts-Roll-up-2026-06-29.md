---
title: Phase 1.2.1 — Roll-up & Contract Tables
roadmap-level: rollup
phase-number: 1
subphase-index: 1.2.1
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- rollup
- dag-contracts
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Per-stage contract tables

### terrain

| Dimension | Contract |
|-----------|----------|
| **Stage ID** | `terrain` |
| **Consumes** | SeedBundle (map seed + ToneProfile terrain weights) |
| **Emits** | TerrainManifest |
| **Upstream deps** | none (DAG root after SeedBundle) |
| **ToneProfile touchpoint** | terrain density, elevation bias, water fraction weights |
| **Replaceability seam** | `gen.stage.terrain` — swap executor; preserve TerrainManifest schema |
| **Failure manifest** | `terrain_failure` — partial heightfield rejected; no downstream dispatch |
| **session.*** topics | `session.stage_ready.terrain`, `session.stage_failed.terrain` |

### biomes

| Dimension | Contract |
|-----------|----------|
| **Stage ID** | `biomes` |
| **Consumes** | TerrainManifest + ToneProfile biome mix weights |
| **Emits** | BiomeManifest |
| **Upstream deps** | `terrain` |
| **ToneProfile touchpoint** | biome rarity, climate band, vegetation density |
| **Replaceability seam** | `gen.stage.biomes` |
| **Failure manifest** | `biomes_failure` — biome label collision or unmapped terrain class |
| **session.*** topics | `session.stage_ready.biomes`, `session.stage_failed.biomes` |

### POIs

| Dimension | Contract |
|-----------|----------|
| **Stage ID** | `POIs` |
| **Consumes** | BiomeManifest + accepted CanonFacts (via IntentResolver cross-cut) |
| **Emits** | POIManifest (may reference LoreHookRegistry hook ids) |
| **Upstream deps** | `biomes` |
| **ToneProfile touchpoint** | POI density, ruin vs settlement bias |
| **Replaceability seam** | `gen.stage.pois` |
| **Failure manifest** | `pois_failure` — spatial overlap with prior POI class (structural) |
| **session.*** topics | `session.stage_ready.pois`, `session.stage_failed.pois` |

### entities

| Dimension | Contract |
|-----------|----------|
| **Stage ID** | `entities` |
| **Consumes** | POIManifest + LoreHookRegistry draft (IntentResolver cross-cut) |
| **Emits** | EntityManifest (entity placements + hook id refs) |
| **Upstream deps** | `POIs` |
| **ToneProfile touchpoint** | entity rarity, hostility band defaults |
| **Replaceability seam** | `gen.stage.entities` |
| **Failure manifest** | `entities_failure` — unreachable NPC reference or orphan hook id |
| **session.*** topics | `session.stage_ready.entities`, `session.stage_failed.entities` |

### sim_bootstrap

| Dimension | Contract |
|-----------|----------|
| **Stage ID** | `sim_bootstrap` |
| **Consumes** | EntityManifest + LoreHookRegistry finalized graph seeds |
| **Emits** | SimGraphSeed |
| **Upstream deps** | `entities` |
| **ToneProfile touchpoint** | event tone defaults on initial sim graph edges (lean) |
| **Replaceability seam** | `gen.stage.sim_bootstrap` |
| **Failure manifest** | `sim_bootstrap_failure` — faction graph seed inconsistency |
| **session.*** topics | `session.stage_ready.sim_bootstrap`, `session.stage_failed.sim_bootstrap` |

## StageDAG edge registry

| from_stage | to_stage | input_manifest_type | output_manifest_type | optional? |
|------------|----------|---------------------|----------------------|-----------|
| SeedBundle | terrain | SeedBundle | TerrainManifest | no |
| terrain | biomes | TerrainManifest | BiomeManifest | no |
| biomes | POIs | BiomeManifest | POIManifest | no |
| POIs | entities | POIManifest | EntityManifest | no |
| entities | sim_bootstrap | EntityManifest | SimGraphSeed | no |
| sim_bootstrap | DeterministicCompiler | SimGraphSeed + all prior manifests | CompiledWorldManifest | no (parent 1.2) |

**DAG invariant I-1.2.1-001:** No backward edges; DAGValidator rejects any cycle before StageOrchestrator starts.

**DAG invariant I-1.2.1-002:** Partial manifest from any stage blocks all transitive downstream stages until failure manifest is cleared or operation aborted.

## ToneProfile injection point registry

| stage_id | injection_point_id | receptive fields | fallback |
|----------|-------------------|------------------|----------|
| terrain | `tpi.terrain.weights` | density, elevation, water | Medium Fantasy default |
| biomes | `tpi.biomes.mix` | biome labels, climate band | Medium Fantasy default |
| POIs | `tpi.pois.density` | ruin/settlement ratio | Medium Fantasy default |
| entities | `tpi.entities.rarity` | hostility, spawn band | Medium Fantasy default |
| sim_bootstrap | `tpi.sim.event_tone` | initial edge tone defaults | Medium Fantasy default |

On unknown ToneProfile variant at any node → Medium Fantasy fallback + `session.tone_fallback_applied` (parent 1.2 contract).

## Cross-stage invariant summary

| Invariant | Rule |
|-----------|------|
| **I-1.2.1-003** | ToneProfileInjector never occupies a DAG traversal slot |
| **I-1.2.1-004** | Only `accepted` CanonFacts enter POIs/entities manifest inputs (1.2.2 + 1.1.2) |
| **I-1.2.1-005** | Replaceability seam swap must not change manifest type names in edge registry |
| **I-1.2.1-006** | DAGValidator mirrors check catalog `dag.preflight` in 1.3.3 DryRunValidator |
| **I-1.2.1-007** | Unknown stage id in orchestrator dispatch → reject at DAGValidator |

## Interfaces (detail)

**Imports from parent 1.2:** SeedBundle schema; DAGValidator pre-flight invariant; StageOrchestrator dispatch contract; `session.*` bus topics for stage ready/failed.

**Imports from Phase 1.1:** `WorldState` / `Simulation` layer IDs for SimGraphSeed handoff; `canon.*` bus for accepted-fact visibility at POIs/entities.

**Exports:**

| Export | Consumer |
|--------|----------|
| **StageDAG edge registry** (this note) | Phase 2 stage executors; 1.3.3 `dag.preflight` |
| **Per-stage contract tables** | Half A catalog stable stage names |
| **ToneProfile injection point registry** | Phase 2 ToneProfileInjector binding |
| **Replaceability seam ids** (`gen.stage.*`) | Phase 1.3 SeamRegistry rows |

**Adjacent slices:** [[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]] — LoreHookRegistry + SimGraphSeed intent path; [[Phase-1-3-3-DryRunValidator-and-ProvenanceEnvelope-Contract-Roadmap-2026-06-29-1205]] — DAG pre-flight check catalog.

## Edge cases

- **Unknown stage id** in orchestrator dispatch → reject at DAGValidator; never start traversal.
- **Partial manifest** from a stage → failure manifest + error sink; downstream stages must not run on incomplete inputs.
- **ToneProfile variant unknown** at a node → Medium Fantasy fallback + `session.tone_fallback_applied`.
- **Executor swap mid-pipeline** → requires new SeedSnapshot + dry-run per 1.3.2/1.3.3; edge registry unchanged.
- **IntentResolver lag** — POIs stage must not proceed if accepted CanonFacts batch not sealed (1.2.2 ordering).

## Open questions

- OQ-1.2.1-001: Minimum stage subset for Horizon M0 — deferred to Phase 2 / Half A catalog.
- OQ-1.2.1-002: Explicit ToneProfile port on DAG edge vs cross-cutting injector only — lean injector-only per parent 1.2; revisit on execution track.
- OQ-1.2.1-003: Parallel stage fan-out within biomes sub-regions — deferred; single topological chain authoritative for conceptual_v1.

## Pseudo-code readiness

```
ON session.seed_bundle_ready:
  IF NOT DAGValidator.preflight(edge_registry) THEN EMIT session.dag_validation_failed; STOP
  EMIT session.dag_validated
  FOR stage IN topological_order(terrain, biomes, POIs, entities, sim_bootstrap):
    ToneProfileInjector.apply(stage, injection_point_registry[stage])
    manifest := StageExecutor[stage].run(upstream_manifests)
    IF manifest.partial THEN EMIT session.stage_failed.<stage>; STOP
    EMIT session.stage_ready.<stage>
  HANDOFF SimGraphSeed + manifests TO DeterministicCompiler
```

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — five stages + registries; intent detail deferred to 1.2.2 |
| Behavior (actors, ordering) | pass | § Behavior — DAGValidator → orchestrator → per-stage emit |
| Interfaces (adjacent contracts) | pass | § Per-stage contract tables + § StageDAG edge registry + § Interfaces |
| Edge cases | pass | § Edge cases — unknown stage, partial manifest, executor swap |
| Open questions | pass | § Open questions — OQ-1.2.1-001..003 documented |
| Pseudo-code readiness | pass | § Pseudo-code readiness — dispatch sketch diagrammable |
| **`handoff_readiness` aggregate** | **80%** | factory feed tertiary feedstock; **1.2 branch closed** |

## Tasks

- [x] Per-stage contract tables + StageDAG edge registry (rollup)
- [x] ToneProfile injection point registry
- [x] Handoff readiness § + frontmatter `handoff_readiness: 80`
- [x] Sibling **1.2.2** feedstock completion — intent pipeline decomposition
- [x] Authority sync: parent **1.2** child rollup cites this note
- [x] Body compact 2026-06-29 — dense tables moved to this rollup child
