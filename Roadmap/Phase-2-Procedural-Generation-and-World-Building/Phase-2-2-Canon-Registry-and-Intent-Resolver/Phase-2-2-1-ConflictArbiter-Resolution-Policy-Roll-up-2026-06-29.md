---
title: Phase 2.2.1 — Roll-up & Conflict Resolution Tables
roadmap-level: rollup
phase-number: 2
subphase-index: 2.2.1
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-2
- rollup
- conflict-arbiter
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Actors

| Actor | Role |
|-------|------|
| **ConflictArbiter** | Detects mutual exclusion between proposed and incumbent CanonFacts; selects resolution mode per policy binding |
| **ConflictManifest** | Human-readable bundle: fact A, fact B, conflict class, suggested modes, provenance links |
| **ResolutionPolicyBinding** | Maps `conflict_class` → default mode + whether auto-resolution is forbidden |
| **MergeTablePolicy** | Governs when `table_merge` is legal — requires explicit table quorum, never silent |
| **CanonFactValidator** | Upstream duplicate/conflict detector; delegates to ConflictArbiter when classes match |
| **IntentResolver** | Queues mid-pipeline intents as `proposed` without mutating in-flight compile (parent 2.2 edge case) |
| **DMWorkbenchQueue** | Presentation sink for unresolved conflicts (Phase 4+ consumes this contract) |

## Conflict classes (conceptual v1)

| conflict_class | Description | Default mode | Auto forbidden |
|----------------|-------------|--------------|----------------|
| `duplicate_identity` | Same entity+slot, incompatible attribute values | `prefer_incumbent` | yes — DM must confirm override |
| `timeline_contradiction` | Mutually exclusive era ordering for same thread | `defer_to_dm` | yes |
| `location_mutex` | Two accepted facts claim exclusive occupancy | `table_merge` or `split_thread` | yes |
| `tone_violation` | Fact fails ToneCompatibilityGate vs active bundle | `reject_new` | no — validator may auto-reject with manifest |
| `player_collision` | Two player-lite intents on same canon slot | `defer_to_dm` | yes |

## Resolution ordering (six-step loop)

1. **CanonFactValidator** flags candidate → **ConflictArbiter** classifies → **ConflictManifest** emitted
2. If mode allows auto path (e.g. `tone_violation` → `reject_new`) → reject with reason manifest on `canon.fact_rejected`
3. Else → queue on **DMWorkbenchQueue** with `session.conflict_surfaced`
4. DM/table selects mode: accept A, accept B, merge per **MergeTablePolicy**, or `split_thread` (fork narrative thread id)
5. On resolution → **ProvenanceEnvelope** records `conflict_resolution_id`, chosen mode, actor → promote winner to `accepted` or leave both `proposed`
6. Mid-pipeline compile in progress → resolution never mutates **CompiledWorldManifest**; re-compile path via **2.1** DryRunValidator only

## Interface tables

### Imports from parent 2.2 and Phase 1

| Source | Consumption |
|--------|-------------|
| CanonFact lifecycle (2.2) | Conflict detection at `proposed` → `accepted` transition |
| Intent pipeline (1.2.2) | Player-lite vs table intent collision boundaries |
| LoreHookRegistry (2.2) | `split_thread` may fork hook namespace without orphaning sim-active hooks |
| RegistrySnapshot + DryRunValidator (1.3) | Post-resolution snapshot must replay before compile |
| CollaborativeRefinementLoop (2.1.1) | Table merge votes may align with pause-point accept semantics — no shared UI |
| `session.*` / `canon.*` bus (1.1) | `canon.conflict_detected`, `canon.conflict_resolved`, `session.conflict_surfaced` |

### Exports

| Export | Consumer |
|--------|----------|
| **ConflictArbiter** policy index | Half A catalog mint; execution track mirror |
| **ResolutionPolicyBinding** | DM workbench UX (Phase 4+) |
| Conflict audit **ProvenanceEnvelope** fields | Factory feed gate evidence |

## Edge cases

- **Three-way conflict:** Emit composite **ConflictManifest** with pairwise classes; DM resolves serially — no automatic pairwise merge cascade.
- **Incumbent sim-active, challenger proposed:** Default `prefer_incumbent` with explicit DM override required to demote sim-active fact.
- **Table absent / timeout:** Unresolved conflicts remain `proposed`; pipeline compile blocked at affected stage handoff — not silent accept.
- **MergeTablePolicy quorum not met:** Fall back to `defer_to_dm`; log `merge_quorum_failed` on provenance.
- **Conflict during session 0 bulk accept:** Partial accept manifest lists per-fact conflict ids; valid facts still promote (parent 2.2 edge case preserved).

## Open questions

- **Auto-reject threshold for low-severity tone drift:** Session policy toggle — deferred to factory catalog / Operator Loop 2.
- **split_thread namespace convention:** Thread fork id format — execution-deferred / catalog mint.
- **Player vs DM priority when both online:** Session policy — DM workbench UX authority (Phase 4+).

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — modes, bindings, merge policy; Phase 4/execution boundaries explicit |
| Behavior (actors, ordering) | pass | § Behavior — five conflict classes + six-step resolution loop |
| Interfaces (adjacent contracts) | pass | § Interfaces — 2.2 lifecycle + 1.2.2 + 2.1.1 coordination |
| Edge cases | pass | § Edge cases — three-way, sim-active incumbent, quorum, bulk accept |
| Open questions | pass | § Open questions — tone threshold, thread id, priority deferred |
| Pseudo-code readiness | pass | § Pseudo-code readiness — conflict detect → classify → resolve traceable |
| **`handoff_readiness` aggregate** | **80%** | factory feed gate `phase_2_tertiary_tree` mint 2.2.1; parent 2.2 `handoff_readiness: 79` hostile ceiling |

> Execution-deferred / advisory on conceptual track: DM widget layout, Godot merge implementations, REGISTRY-CI receipts, factory catalog rows — resolved on execution track or factory harness (`1373c0c3408d`).

## Pseudo-code readiness

A reader can trace validator flag → conflict class → policy mode → manifest → DM resolution → provenance → registry promotion without guessing merge authority or silent overwrite rules. No API signatures on conceptual track; execution deepen mints typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

Builds on parent 2.2 and Phase 1 intent pipeline (no new pre-deepen research this run):

- PMG collaborative forge — contradictory player intents must surface to table, never silent merge
- Intent pipeline decomposition — [[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]
- Influence conceptual deepen proc-gen — [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]

## Responsibilities (rollup authority)

- [x] Name **ConflictArbiter** resolution modes and **ResolutionPolicyBinding** catalog
- [x] Document **MergeTablePolicy** — explicit table quorum, no silent merge
- [x] Bind conflict lifecycle `canon.*` / `session.*` events for Presentation handoff

## Tasks (rollup authority)

- [x] Mint 2.2.1 tertiary with conflict resolution policy and default class table
- [ ] Optional refine: expand three-way conflict UX when DM workbench matures (owner: Phase 4+)
