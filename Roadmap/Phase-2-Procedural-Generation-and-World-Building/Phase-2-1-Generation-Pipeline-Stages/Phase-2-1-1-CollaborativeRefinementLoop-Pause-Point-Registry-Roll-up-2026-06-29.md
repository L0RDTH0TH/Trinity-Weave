---
title: Phase 2.1.1 — Roll-up & Pause-Point Tables
roadmap-level: rollup
phase-number: 2
subphase-index: 2.1.1
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-2-1-1-CollaborativeRefinementLoop-Pause-Point-Registry-Roadmap-2026-06-29-1830]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-2
- rollup
- pause-point-registry
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Actors

| Actor | Role |
|-------|------|
| **PausePointRegistry** | Authoritative list of pause slots keyed by `pause_id`; each entry names pre-stage, post-stage, optional composite gate, and default policy |
| **CollaborativeRefinementLoop** | Orchestrator that consults registry before advancing **StageOrchestrator** dispatch |
| **ScaffoldPreviewBuilder** | Assembles human-readable scaffold delta from upstream manifest snapshot |
| **RevisionAcceptancePolicy** | Evaluates DM/table response: accepted revisions mutate downstream inputs only after commit |
| **PauseTimeoutArbiter** | Applies session policy timeout → default accept scaffold as proposed (logged on `session.*`) |
| **StageOrchestrator** | Respects `pause_cleared` token before next executor runs |

## Default registry entries (conceptual v1)

| pause_id | After stage / before stage | Default policy | Notes |
|----------|---------------------------|----------------|-------|
| `pre_terrain_preview` | SeedBundle validated → terrain | optional | DM may preview terrain scaffold before commit (parent 2.1 step 4) |
| `post_terrain_biomes` | terrain → biomes | optional | Composite preview of terrain+biome weights |
| `post_biomes_pois` | biomes → POIs | optional | CanonFact hook density visible before POI placement |
| `post_pois_entities` | POIs → entities | optional | LoreHookRegistry draft attachment review |
| `pre_compile_review` | sim_bootstrap → DeterministicCompiler | recommended | Final manifest review before dry-run + compile |

## Ordering (six-step loop)

1. **StageOrchestrator** reaches registry-bound transition → **CollaborativeRefinementLoop** intercepts
2. **ScaffoldPreviewBuilder** emits **ScaffoldPreviewManifest** for active `pause_id`
3. DM/table accepts, revises, or defers per **RevisionAcceptancePolicy**
4. On accept (explicit or timeout-default) → downstream stage inputs updated → `session.pause_cleared` → dispatch continues
5. On revise → loop re-enters preview with mutated scaffold until accept or policy cap
6. Registry may mark slot `disabled` for automated / headless generation profiles (logged, not silent)

## Interface tables

### Imports from parent 2.1 and Phase 1

| Source | Consumption |
|--------|-------------|
| Stage executor registry (2.1) | Pre/post stage names for **PausePointBinding** |
| Stage DAG contracts (1.2.1) | Manifest type names for scaffold snapshots |
| `session.*` bus (1.1) | `session.scaffold_preview_ready`, `session.pause_revision_submitted`, `session.pause_cleared`, `session.pause_timeout_defaulted` |
| DryRunValidator + SeedSnapshot (1.3) | `pre_compile_review` gate coordinates with pre-compile dry-run — no duplicate safety authority |

### Exports

| Export | Consumer |
|--------|----------|
| **PausePointRegistry** canonical index | Phase 4+ DM workbench UX; Half A catalog mint |
| **RevisionAcceptancePolicy** contract | Execution track mirror under `Roadmap/Execution/` |
| Pause lifecycle `session.*` events | Presentation layer feedback (Phase 6 demo stubs reference pause badges only) |

## Edge cases

- **All pause slots disabled:** Pipeline runs uninterrupted; registry records `headless_profile: true` on provenance envelope — not an error.
- **Revise loop cap exceeded:** Session policy max revisions → force accept with `revision_cap_exceeded` flag on manifest; DM notified via Presentation.
- **Timeout during table absence:** **PauseTimeoutArbiter** applies default accept; event `session.pause_timeout_defaulted` — matches parent 2.1 collaborative loop timeout edge case.
- **Conflicting revision vs DryRunValidator:** If accepted revision would break SeedSnapshot replay → block at pre-compile; pause registry does not override 1.3 safety gates.
- **Sparse world path:** Zero POI yield still allows `post_pois_entities` pause with empty scaffold — valid degraded preview, not skipped silently.

## Open questions

- **Granularity default:** Pause after every stage vs only `pre_terrain_preview` + `pre_compile_review` — deferred to operator attestation via factory catalog (parent 2.1 OQ).
- **Horizon M0 minimum pause subset:** Which `pause_id` entries required for first playable loop — execution-deferred / catalog mint.
- **Composite gate UX:** Whether `post_terrain_biomes` ships as one preview or two chained pauses — DM workbench design authority (Phase 4+).

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — registry, policies, bindings; 2.2/2.3/Phase 4 boundaries explicit |
| Behavior (actors, ordering) | pass | § Behavior — five default pause entries + six-step loop |
| Interfaces (adjacent contracts) | pass | § Interfaces — 2.1 stage registry + 1.2.1 manifests + 1.3 dry-run coordination |
| Edge cases | pass | § Edge cases — headless, cap, timeout, dry-run conflict, sparse world |
| Open questions | pass | § Open questions — granularity + M0 subset deferred to catalog |
| Pseudo-code readiness | pass | § Pseudo-code readiness — traceable without API signatures |
| **`handoff_readiness` aggregate** | **79%** | factory feed gate `phase_2_tertiary_tree` first mint 2.1.1; parent 2.1 `handoff_readiness: 78` hostile ceiling |

> Execution-deferred / advisory on conceptual track: DM workbench widgets, Godot pause UI, factory catalog row shapes, HR rollup gates — resolved on execution track or factory harness (`1373c0c3408d`).

## Pseudo-code readiness

A reader can trace registry lookup → scaffold preview → accept/revise/timeout → pause_cleared → stage dispatch without guessing pause ownership or event names. No API signatures on conceptual track; execution deepen mints typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

Builds on Phase 2.1 parent research integration (no new pre-deepen research this run):

- Collaborative forge aligns with PMG "generation is collaborative dialogue" — pause registry makes choice loops explicit between stage commits
- Stage DAG manifest contracts — [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]
- Influence conceptual deepen proc-gen — [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]

## Responsibilities (rollup authority)

- [x] Name **PausePointRegistry** entries and **RevisionAcceptancePolicy** for CollaborativeRefinementLoop
- [x] Bind default pause slots to 2.1 stage executor transitions
- [x] Document `session.*` pause lifecycle events for Presentation handoff

## Tasks (rollup authority)

- [x] Mint 2.1.1 tertiary with pause-point registry and default policy table
- [ ] Optional refine: expand composite gate semantics when DM workbench UX matures (owner: Phase 4+)
