---
title: Phase 1.2.2 — Roll-up & Contract Tables
roadmap-level: rollup
phase-number: 1
subphase-index: 1.2.2
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- rollup
- intent-pipeline
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Behavior (detail)

**Actors:**

| Actor | Role |
|-------|------|
| **CanonCommitBoundary** | Read-only gate; only `accepted` CanonFacts are visible to IntentResolver; emits `canon.accepted` on the `canon.*` bus when facts transition to accepted |
| **IntentResolver** | Maps accepted CanonFacts → LoreHookRegistry entries + faction/tribe graph seeds; runs as cross-cut during POIs, entities, and sim_bootstrap passes (not a DAG stage slot) |
| **LoreHookRegistry** | Append-only registry of lore hooks (faction seeds, tribe seeds, NPC placement hooks) keyed for sim bootstrap and Phase 3 continuity |
| **CanonFactCollector** | Aggregates session 0 player/DM inputs into CanonFact candidates (`proposed` until adjudicated) |
| **ConflictAdjudicator** | Surfaces contradicting accepted facts; emits `canon.conflict_detected`; does not silently merge incompatible attributes |

**CanonFact lifecycle (PMG-aligned):**

1. **proposed** — CanonFactCollector ingests session 0 intent; not visible to IntentResolver
2. **accepted** — DM/player adjudication complete; CanonCommitBoundary opens read access; `canon.accepted` emitted
3. **hooked** — IntentResolver writes LoreHookRegistry entry referencing the accepted fact
4. **sim-active** — sim_bootstrap consumes graph seeds derived from hooked entries; WorldState receives initial faction graph

**Ordering (cross-cut with stage DAG):**

1. SeedBundle formed; DAGValidator pre-flight passes (parent 1.2)
2. StageOrchestrator begins topological traversal per [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]
3. **POIs stage:** IntentResolver reads accepted CanonFacts relevant to place hooks; drafts LoreHookRegistry entries for location-bound lore
4. **entities stage:** IntentResolver enriches registry with entity-bound hooks; EntityManifest may reference hook ids
5. **sim_bootstrap stage:** IntentResolver finalizes faction/tribe graph seeds; SimGraphSeed assembled for Simulation layer bootstrap
6. Parent **DeterministicCompiler** consumes assembled manifests (intent outputs are inputs to compile, not post-compile)

**Inputs / outputs:**

- *Into intent pipeline:* CanonFact candidates (session 0), adjudication outcomes, ToneProfile (bias names only — not owner of intent flow)
- *Out of intent pipeline:* LoreHookRegistry (hook set), SimGraphSeed (faction/tribe graph), POI/entity manifest hook references

## LoreHookRegistry schema

Authoritative entry shapes for conceptual feedstock. All entries are **append-only** during world gen; ordering is deterministic by `(canon_fact_id, hook_kind, hook_id)` lexicographic sort.

### Common entry header (all hook kinds)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hook_id` | string | yes | Stable registry key (`lh.<kind>.<slug>`) |
| `hook_kind` | enum | yes | `faction_seed` \| `tribe_seed` \| `npc_hook` |
| `canon_fact_id` | string | yes | Back-link to accepted CanonFact |
| `lifecycle_state` | enum | yes | `hooked` until sim_bootstrap promotes graph rows to `sim-active` |
| `anchor_kind` | enum | yes | `poi` \| `entity` \| `graph_only` |
| `anchor_ref` | string | no | POI id or entity manifest row when `anchor_kind` ≠ `graph_only` |
| `tone_bias_tags` | string[] | no | ToneProfile label refs (names only) |
| `ordering_key` | string | yes | Deterministic tie-break; derived from fact id + kind |

### faction_seed entry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `faction_id` | string | yes | Graph node id for SimGraphSeed |
| `display_name` | string | yes | Player-visible faction label |
| `alignment_band` | enum | no | `hostile` \| `neutral` \| `friendly` \| `unknown` |
| `initial_strength` | number | no | 0.0–1.0 seed weight; default 0.5 |
| `poi_affinity_ids` | string[] | no | POIs where faction presence is seeded |

### tribe_seed entry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tribe_id` | string | yes | Graph node id (may nest under faction) |
| `parent_faction_id` | string | no | Owning faction node when applicable |
| `display_name` | string | yes | Tribe label |
| `mobility_band` | enum | no | `sedentary` \| `nomadic` \| `unknown` |
| `entity_hook_ids` | string[] | no | Cross-refs to `npc_hook` rows |

### npc_hook entry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `npc_hook_id` | string | yes | Alias of `hook_id` when kind is `npc_hook` |
| `entity_manifest_ref` | string | no | EntityManifest row id once entities pass runs |
| `role_tag` | enum | no | `leader` \| `envoy` \| `guard` \| `civilian` \| `lorekeeper` |
| `placement_policy` | enum | yes | `poi_bound` \| `wander` \| `absent_proxy` |
| `dialogue_seed_ref` | string | no | Lore text handle (execution-deferred) |

### Registry invariants

| Invariant | Rule |
|-----------|------|
| **I-1.2.2-001** | No registry write without `canon_fact_id` at `accepted` lifecycle |
| **I-1.2.2-002** | `hook_id` uniqueness enforced within a single generation run |
| **I-1.2.2-003** | `graph_only` faction/tribe seeds may exist without POI/entity anchor until sim_bootstrap |
| **I-1.2.2-004** | Orphan hooks emit `hook.unanchored` on `canon.*` — compile may proceed with warning manifest |

## Intent cross-cut registry tables

IntentResolver is **not** a DAG stage slot. These tables define **when** each stage pass may read/write registry state.

### POIs stage cross-cut

| Dimension | Contract |
|-----------|----------|
| **Stage ID** | `POIs` (per [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]) |
| **IntentResolver reads** | Accepted CanonFacts with `place` / `location` attributes; existing LoreHookRegistry draft (empty on first pass) |
| **IntentResolver writes** | `npc_hook` rows with `anchor_kind: poi`; draft `faction_seed` rows with `poi_affinity_ids` |
| **Manifest side-effect** | POIManifest columns may reference `hook_id` list |
| **Precondition** | CanonCommitBoundary batch sealed for session 0 accepted facts |
| **Bus topics** | `canon.accepted` (observe); `hook.unanchored` (emit on orphan) |
| **Failure mode** | Proposed fact leak → abort intent pass for that fact |

### entities stage cross-cut

| Dimension | Contract |
|-----------|----------|
| **Stage ID** | `entities` |
| **IntentResolver reads** | POIManifest + LoreHookRegistry draft from POIs pass |
| **IntentResolver writes** | Enrich `npc_hook` with `entity_manifest_ref`; link `tribe_seed.entity_hook_ids` |
| **Manifest side-effect** | EntityManifest hook id column populated |
| **Precondition** | POIs stage `session.stage_ready.pois` emitted |
| **Bus topics** | `canon.conflict_detected` on contradictory accepted facts |
| **Failure mode** | Orphan hook id on manifest → `entities_failure` per 1.2.1 |

### sim_bootstrap stage cross-cut

| Dimension | Contract |
|-----------|----------|
| **Stage ID** | `sim_bootstrap` |
| **IntentResolver reads** | Finalized LoreHookRegistry; EntityManifest hook refs |
| **IntentResolver writes** | Promote `faction_seed` / `tribe_seed` to `sim-active`; assemble **SimGraphSeed** |
| **Manifest side-effect** | SimGraphSeed `{ nodes: faction[], edges: tribe[] }` or empty-graph sentinel |
| **Precondition** | entities stage `session.stage_ready.entities` emitted |
| **Bus topics** | `session.stage_ready.sim_bootstrap` (downstream of IntentResolver finalize) |
| **Failure mode** | Graph seed inconsistency → `sim_bootstrap_failure` |

### Cross-cut timing summary

| DAG stage | Registry read scope | Registry write scope | SimGraphSeed touch |
|-----------|--------------------|-----------------------|-------------------|
| terrain | none | none | none |
| biomes | none | none | none |
| POIs | accepted facts + draft | draft hooks (poi-bound) | none |
| entities | draft + POIManifest | enrich hooks + tribe links | none |
| sim_bootstrap | finalized registry | promote to sim-active | **emit** |

## Interfaces (detail)

**Imports from Phase 1.1:**

| 1.1 Export | How 1.2.2 consumes it |
|-----------|------------------------|
| `canon.*` bus category | CanonCommitBoundary and ConflictAdjudicator event topics |
| CanonCommitBoundary (read-only gate) | IntentResolver queries `accepted` status before any registry write |
| `Simulation` layer ID | SimGraphSeed targets Simulation bootstrap at session start |

**Imports from sibling 1.2.1:**

| 1.2.1 Export | How 1.2.2 consumes it |
|--------------|------------------------|
| POIManifest | Receives hook references from LoreHookRegistry draft during POIs pass |
| EntityManifest | Consumes enriched LoreHookRegistry during entities pass |
| SimGraphSeed slot | Final graph seed output at sim_bootstrap handoff |

**Exports to parent 1.2 / Phase 2+:**

| Export | Consumer |
|--------|----------|
| **LoreHookRegistry schema** (hook kinds, fact back-links) | Phase 2 canon registry implementation |
| **IntentResolver cross-cut contract** (when each stage may read/write hooks) | Phase 2 stage executor orchestration |
| **SimGraphSeed shape** (faction nodes, tribe edges, empty-graph sentinel) | Phase 3 off-screen simulation |

## Edge cases

- **Proposed fact leak:** Any CanonFact at `proposed` reaching IntentResolver is a **contract violation** — generation must abort the intent pass for that fact, not downgrade to soft warning.
- **Intent collision:** Two `accepted` facts contradicting on the same entity → `canon.conflict_detected`; first-encountered wins for generation with DM-visible flag; no silent discard.
- **Zero faction/tribe seeds:** Valid degraded start — CompiledWorldManifest may set `sim_active: false`; empty faction graph is not an error.
- **Orphan hook:** LoreHookRegistry entry with no matching POI/entity anchor → flagged `hook.unanchored` on `canon.*` bus; compile may proceed with warning manifest.
- **Replay determinism:** Identical accepted CanonFact set + SeedBundle must yield identical LoreHookRegistry ordering and SimGraphSeed — IntentResolver must not introduce nondeterministic ordering (no timestamp-based tie-break).

## Open questions

- **Hook eviction at gen time:** Maximum LoreHookRegistry size at world gen vs runtime growth — deferred to Phase 3 (parent 1.2).
- **Partial adjudication:** Session 0 closes with mix of `proposed` and `accepted` facts — generation proceeds on accepted subset only; proposed facts remain queued for post-gen DM session (Phase 2 UX).
- **NPC hook vs entity manifest overlap:** Whether every entity manifest row requires a registry hook or allows anonymous spawns — deferred to Phase 2 catalog mint.

## Pseudo-code readiness

Intent pass sketch (conceptual — not API signatures):

```
ON session.dag_validated:
  registry := LoreHookRegistry.empty()
  FOR stage IN (POIs, entities, sim_bootstrap):
    facts := CanonCommitBoundary.query_accepted(stage_filter[stage])
    registry := IntentResolver.cross_cut(stage, facts, registry, upstream_manifests)
  seed := IntentResolver.finalize_graph(registry)
  HANDOFF seed TO sim_bootstrap StageExecutor
```

A reader can trace session 0 facts through CanonCommitBoundary → IntentResolver → LoreHookRegistry → SimGraphSeed without guessing stage timing or actor ownership. Execution track will mint typed hook schemas and bus payloads under `Roadmap/Execution/` mirror spine.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — lifecycle + actors; DAG I/O owned by 1.2.1 |
| Behavior (actors, ordering) | pass | § Behavior — CanonFact lifecycle + cross-cut ordering |
| Interfaces (adjacent contracts) | pass | § LoreHookRegistry schema + § Intent cross-cut registry tables + § Interfaces |
| Edge cases | pass | § Edge cases — proposed leak, collision, orphan, determinism |
| Open questions | pass | § Open questions — three OQs documented |
| Pseudo-code readiness | pass | § Pseudo-code readiness — cross-cut sketch diagrammable |
| **`handoff_readiness` aggregate** | **80%** | factory feed tertiary feedstock; **1.2 branch closed** (1.2.1 + 1.2.2 feedstock complete) |
