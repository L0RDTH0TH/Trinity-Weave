---
title: Phase 1.2 — Procedural Generation Graph and Intent Population Pipeline
roadmap-level: secondary
phase-number: 1
subphase-index: '1.2'
project-id: genesis-mythos-master
status: active
priority: high
progress: 80
handoff_readiness: 79
factory_feedstock_slice: phase_1_secondary_tree
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-1
- proc-gen
- intent-pipeline
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 1.2 — Procedural Generation Graph and Intent Population Pipeline

Define the conceptual shape of the procedural generation stage DAG and the intent population pipeline that transforms session 0 canon entries into world hooks, faction seeds, and sim-active graph nodes. This slice names the **nouns and flow** — not implementation paths.

## Scope

**In scope:** the procedural generation stage DAG (directed acyclic graph with forward-progress invariant); stage identities and typed outputs (SeedBundle → terrain → biomes → POIs → entities → sim bootstrap → CompiledWorldManifest); the intent population pipeline from session 0 CanonFacts through LoreHookRegistry to sim-active faction/tribe graph seeds; ToneProfile injection points across generation stages; the DeterministicCompiler contract (deterministic compile as first-class design requirement, not Phase 6 afterthought); the CanonCommitBoundary interaction — only `accepted` CanonFacts may flow into generation stages.

**Out of scope:** Godot C# implementation of stage executors or DAG traversal runtime, factory catalog rows and slot shapes, execution-track typed interfaces, Phase 3 off-screen tick details, multiplayer session synchronization, full biome archetype specifications (Phase 2 scope).

## Behavior

**Actors:**

| Actor | Role |
|-------|------|
| **SeedParser** | Reads raw session 0 inputs (player/DM intents, ToneProfile choice, map seeds) and assembles a **SeedBundle** — the canonical input to the generation graph |
| **DAGValidator** | Pre-flight one-shot pass on the stage graph; guarantees forward progress (no cycles, all stage input dependencies resolvable) before StageOrchestrator may begin |
| **StageOrchestrator** | Traverses stage nodes in topological order; dispatches each node with its typed input manifest; collects typed output manifests |
| **StageNode[terrain..sim_bootstrap]** | Per-stage manifest I/O and replaceability seams — see child [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]] |
| **ToneProfileInjector** | Cross-cutting; injects ToneProfile weights into each receptive stage (terrain density, biome mix, entity rarity, event tone defaults) without owning a stage slot |
| **IntentResolver** | Runs alongside entities and sim_bootstrap stages; maps `accepted` CanonFacts → LoreHookRegistry entries + faction/tribe graph seeds — full decomposition in [[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]] |
| **DeterministicCompiler** | Consumes the final assembly (all stage manifests) → emits **CompiledWorldManifest**; rejects unknown stage outputs, overlapping spatial allocations, unreachable NPC references; same SeedBundle + ToneProfile → byte-stable CompiledWorldManifest (required for dry-run and save/load) |

**Ordering:**

1. Session 0 closes → **SeedBundle** formed: ToneProfile + validated map seed + player/DM accepted CanonFacts
2. **DAGValidator** pre-flight: confirms no cycles; rejects if dependency chain unresolvable
3. **StageOrchestrator** traverses in topological order: `terrain → biomes → POIs → entities → sim_bootstrap`
4. **ToneProfileInjector** applied at each receptive stage node (cross-cutting; not a separate slot in the DAG traversal)
5. **IntentResolver** resolves accepted CanonFacts into LoreHookRegistry entries during POIs/entities/sim_bootstrap passes
6. **DeterministicCompiler** emits **CompiledWorldManifest**
7. **WorldEventLog** initialized from CompiledWorldManifest (append-only event-sourced backbone for world continuity — see Phase 3)

**Inputs / outputs:**

- *Into pipeline:* SeedBundle (ToneProfile + map seed + session 0 CanonFacts)
- *Out of pipeline:* CompiledWorldManifest (deterministic world DSL) + initialized WorldEventLog + LoreHookRegistry (faction/tribe hook set for sim bootstrap)

## Interfaces

**Imports from Phase 1.1 (layer IDs + bus categories):**

| 1.1 Export | How 1.2 consumes it |
|-----------|---------------------|
| `WorldState` layer ID | CompiledWorldManifest loaded into WorldState as initial event-sourced snapshot |
| `Simulation` layer ID | SimGraphSeed handed to Simulation bootstrap at session start |
| `canon.*` bus category | CanonCommitBoundary emits `canon.accepted` events before IntentResolver reads CanonFacts |
| `session.*` bus category | SeedParser emits `session.seed_bundle_ready`; DeterministicCompiler emits `session.world_manifest_ready` or `session.world_manifest_failed` |
| CanonCommitBoundary (read-only gate) | IntentResolver checks `accepted` status via the same read-only gate contract before populating LoreHookRegistry |

**Exports to Phase 2+:**

| Export | Consuming phase |
|--------|----------------|
| **SeedBundle schema** (field names + ToneProfile link) | Phase 2 generation pipeline implementation |
| **StageDAG edge registry** (stage identities, input/output manifest types by name) | Phase 2 stage executor contracts |
| **LoreHookRegistry initial population** (faction/tribe/NPC hook shapes) | Phase 3 off-screen faction activity |
| **CompiledWorldManifest schema** (deterministic world DSL shape) | Phase 2 and Phase 3 sim bootstrap |
| **ToneProfile injection point registry** (which stages accept ToneProfile; bias names) | Phase 2 biome/weather generation, Phase 3 NPC/event defaults |

**Adjacent slices:**
- Phase 1.3 (modularity seams + safety invariants): DAG injection seams are *named* here; 1.3 finalizes the seam contract and seed-snapshot/dry-run invariants at design level.
- Phase 2: materializes stage executor implementations and full canon registry from these stage definitions.

## Edge cases

- **DAG cycle prevention:** Circular stage dependencies (e.g. entities → POIs → entities) must be detected and rejected at DAGValidator pre-flight — not at runtime. Generation must not start if any cycle exists.
- **Partial generation failure:** A failed stage must emit a failure manifest (not crash); StageOrchestrator routes to an error sink; CompiledWorldManifest is flagged `incomplete: true`; Presentation must surface this state to the DM, not silently use an inconsistent world.
- **ToneProfile mismatch / unknown variant:** If a stage does not recognize a ToneProfile variant (e.g. a community-added profile), fall back to Medium Fantasy defaults and emit `session.tone_fallback_applied` on the `session.*` bus — logged, DM-visible, not a crash.
- **Intent collision (contradicting CanonFacts):** Two `accepted` CanonFacts that contradict each other (same entity, conflicting attributes) during IntentResolver must emit `canon.conflict_detected`; generation may proceed with first-encountered wins, flagged for DM adjudication; do not silently discard one fact.
- **Missing sim_bootstrap stage:** If IntentResolver yields zero faction/tribe seeds, CompiledWorldManifest emits with `sim_active: false`; WorldState initializes with empty faction graph — valid degraded start, not an error condition.
- **Seed replay determinism:** Given identical SeedBundle + ToneProfile + accepted CanonFacts, DeterministicCompiler must produce a byte-stable CompiledWorldManifest. Non-determinism here breaks save/load and dry-run validation. Any source of entropy (timestamps, random without explicit seed) is forbidden in the compile stage.
- **CanonFact at `proposed` state in IntentResolver:** Proposed facts must never flow into generation. IntentResolver reads only `accepted` via CanonCommitBoundary gate; a proposed fact that leaks is a contract violation (not a soft warning).

## Open questions

- **ToneProfile injection architecture:** Cross-cutting injector (current lean — ToneProfileInjector as orchestrator-level concern) vs. explicit ToneProfile input port on each stage node DAG edge. Cross-cutting keeps stage nodes simpler and lets profile updates propagate without renegotiating DAG edges; trade-off deferred to Phase 2 stage executor design.
- **Minimum viable stage set for Horizon demo M0:** Phase 1.2 names all canonical stages; which subset is sufficient for Horizon demo is a Phase 2 / Half A catalog decision (operator attestation required, not resolved here).
- **LoreHookRegistry capacity and eviction:** Scope of faction/tribe hook count at world gen time vs. runtime growth — deferred to Phase 3 (off-screen simulation design).
- **CompiledWorldManifest format (DSL vs. binary):** Conceptual layer names the requirement (deterministic, verifiable); format locked by Half A catalog mint + execution track.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — stage DAG + intent pipeline; execution paths deferred |
| Behavior (actors, ordering) | pass | § Behavior — SeedParser through DeterministicCompiler; seven-step ordering |
| Interfaces (adjacent contracts) | pass | § Interfaces — 1.1 imports + Phase 2 exports; child 1.2.1/1.2.2 adjacency |
| Edge cases | pass | § Edge cases — DAG cycles, partial failure, determinism, canon gate |
| Open questions | pass | § Open questions — ToneProfile architecture, M0 subset deferred |
| Pseudo-code readiness | pass | § Pseudo-code readiness — pipeline flow sketchable without API signatures |
| Tertiary coverage (1.2.1 + 1.2.2) | pass | **Feedstock complete** (2026-06-29): 1.2.1 `handoff_readiness: 80` + 1.2.2 `handoff_readiness: 80`; both `progress: 100` |
| **`handoff_readiness` aggregate** | **82%** | factory feed gate reconcile `phase_1_secondary_tree` slice 1.2; **1.2 branch closed**; **1.2.1 body compact GREEN** 2026-06-29 (`resume-deepen-gmm-121-compact`; body 1077; rollup child) |

> Execution-deferred / advisory on conceptual track: Godot stage executors, factory catalog rows, CompiledWorldManifest binary format, HR rollup gates — resolved on execution track or factory harness (`1373c0c3408d`).

## Pseudo-code readiness

A reader can sketch the generation pipeline flow (seed parse → DAG pre-flight → stage traversal → intent resolution → deterministic compile → world event log init) and the intent population flow (session 0 facts → CanonCommitBoundary gate → IntentResolver → LoreHookRegistry → sim graph seeds) without guessing stage order or actor ownership. No API signatures required on conceptual track; execution deepen will mint typed stage contracts and DAG edge schemas under `Roadmap/Execution/` mirror spine per Phase 1.1 precedent.

## Research integration

Key takeaways consumed from chain research canon (influence research synthesis):

- **Stage DAG with typed outputs and forward-progress invariant:** WorldGen Director→Validator→Critic→Compiler pattern; DAG-for-proceduralism (Infinity Creator Manual) — guarantees no accidental cycles and no undeclared stage inputs [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]
- **Deterministic compile stage as first-class design row:** WorldGen compiler rejects unknown modules, overlaps, and unreachable NPCs; academic narrative→semantic plan→deterministic assembly confirms compile belongs in Phase 1 contracts, not Phase 6 — [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]
- **Intent population → LoreHookRegistry:** PMG canon pipeline (`proposed → accepted → hooked → sim-active`) maps cleanly to IntentResolver flow; influence nouns `CanonStateMachine`, `CanonValidatorGate`, `ProcGenStageDAG`, `CompiledWorldManifest` proposed for catalog mint — [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]
- **ToneProfile as cross-cutting session bundle:** PMG mandates single session-level profile consumed by world gen, weather, sim defaults, lore events, quest framing — injector cross-cutting model preferred over siloed per-subsystem presets
- **Bus delivery for generation events:** `session.*` topics (queued FIFO) carry SeedBundle ready and world manifest ready signals — aligns with Phase 1.1 hybrid bus contracts [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-godot-gmm-033500Z]]

## Child notes

- **1.2.1 Stage DAG node contracts** — [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]: per-stage contract tables + StageDAG edge registry + ToneProfile injection point registry; feedstock `handoff_readiness: 80` (2026-06-29).
- **1.2.2 Intent pipeline decomposition** — [[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]: LoreHookRegistry schema + intent cross-cut registry tables; `handoff_readiness: 80` feedstock complete (2026-06-29).
- **Branch status:** `oversized_pending_children: false` — tertiaries **1.2.1** and **1.2.2** feedstock complete; **1.2 branch closed** (`workflow_state.phase_1_branch_1_2_open: false`). **1.2.1 body compact GREEN** (`cleared_2026-06-29_1.2.1_body_compact_1077_chars`; rollup [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roll-up-2026-06-29]]). **1.2.2 body compact GREEN** (`cleared_2026-06-29_1.2.2_body_compact_1134_chars`; rollup [[Phase-1-2-2-Intent-Pipeline-Decomposition-Roll-up-2026-06-29]]; queue `resume-factory-continue-gmm-post-121-compact-20260629T141500Z`). `integration_spine_retained: true` — parent retains integration spine; intent detail lives in **1.2.2**.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
