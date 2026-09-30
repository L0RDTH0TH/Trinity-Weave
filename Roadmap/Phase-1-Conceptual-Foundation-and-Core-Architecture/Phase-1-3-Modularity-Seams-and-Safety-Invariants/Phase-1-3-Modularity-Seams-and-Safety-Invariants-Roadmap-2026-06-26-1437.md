---
title: Phase 1.3 — Modularity Seams and Safety Invariants
roadmap-level: secondary
phase-number: 1
subphase-index: '1.3'
project-id: genesis-mythos-master
status: active
priority: high
progress: 100
handoff_readiness: 80
factory_feedstock_slice: phase_1_secondary_tree
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-1
- modularity-seams
- safety-invariants
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 1.3 — Modularity Seams and Safety Invariants

Finalize the **replaceability contract** across generation, rules, simulation bus, and input — and embed **iteration-safe invariants** (seed snapshots, dry-run validation, provenance) at design level. This slice names **seam nouns and safety gates** — not implementation paths.

## Scope

**In scope:** four modularity seam families aligned to PMG modularity boundaries; seam **swap contract** (what may change without renegotiating neighbors); cross-links to Phase 1.2 stage replaceability seams; **SeedSnapshot** contract (when, what, where — conceptual); **DryRunValidator** contract (pre-commit estimate without world write); **ProvenanceEnvelope** (traceability of inputs, rulesets, and modules per world element); session-scoped composition over global gameplay loops (inherits 1.1).

**Out of scope:** Godot addon folder layout, C# interface signatures, factory catalog row mint, execution-track pseudo-code, HR rollup gates (execution-deferred / advisory on conceptual track), community contribution packaging (Phase 5 documentation).

## Behavior

**Actors:**

| Actor | Role |
|-------|------|
| **SeamRegistry** | Canonical index of replaceability seams — generation stages, rule hooks, bus subscriptions, input parsers — each with swap contract and neighbor guarantees |
| **StageExecutorPort** | Generation seam — one port per canonical stage (`terrain` … `sim_bootstrap`); inherits per-node contracts from [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]] |
| **RulePluginPort** | Rule engine seam — core primitives only; rulesets declare hook points and conflict resolution policy |
| **BusSubscriptionPort** | Simulation event bus seam — behaviors subscribe to `sim.*` / `canon.*` categories without owning the bus implementation |
| **IntentParserPort** | Input loop seam — intent envelope parsing + population resolver; extensible for voice, forms, chat without rewriting Simulation |
| **SeedSnapshotAuthority** | Captures immutable snapshot of SeedBundle + ToneProfile + accepted CanonFacts + active ruleset IDs before destructive generation or DM overwrite |
| **DryRunValidator** | Read-only pre-flight on proposed generation compile or DM structural overwrite — estimates validity and performance envelope; **no world write** until pass |
| **ProvenanceRecorder** | Attaches provenance metadata to CompiledWorldManifest elements and sim graph nodes — which seeds, rulesets, and stage executors shaped each artifact |

**Ordering:**

1. **SeamRegistry** published after 1.1 layer IDs and 1.2 stage DAG are stable — 1.3 **finalizes** seam labels referenced in 1.2.1 replaceability columns
2. Before any **CompiledWorldManifest** commit or DM structural re-generation: **SeedSnapshotAuthority** captures snapshot → **DryRunValidator** runs → on pass, commit proceeds; on fail, DM-visible rejection with provenance cite
3. Community or operator swaps (stage executor, ruleset, input parser) touch **only** the named port — neighbors consume typed manifests/events unchanged

**Inputs / outputs:**

- *Into safety path:* proposed generation compile or structural overwrite request + current session state handles
- *Out of safety path:* `dry_run.pass` | `dry_run.fail` bus events; optional `SeedSnapshot` handle for rollback; ProvenanceEnvelope attached to committed artifacts

## Interfaces

**Imports from Phase 1.1:**

| 1.1 Export | How 1.3 consumes it |
|-----------|---------------------|
| Layer IDs (WorldState, Simulation, Presentation, InputIntent) | Each seam family maps to exactly one primary layer owner; bus seams span Simulation + WorldState |
| Bus category registry (`canon.*`, `sim.*`, `session.*`, `presentation.*`) | BusSubscriptionPort declares allowed categories per subscriber class |
| Session composer (composition root) | Only session composer may wire concrete seam implementations — no global autoload gameplay loops |

**Imports from Phase 1.2:**

| 1.2 Export | How 1.3 consumes it |
|-----------|---------------------|
| StageDAG edge registry + replaceability seams (1.2.1) | **StageExecutorPort** inherits stage id → manifest I/O; 1.3 adds swap contract and DryRun hooks |
| DeterministicCompiler | DryRunValidator invokes compiler in **estimate-only** mode; SeedSnapshot required before full compile commit |
| CanonCommitBoundary | SeedSnapshot captures only `accepted` CanonFacts; proposed facts excluded |
| ToneProfileInjector touchpoints | ProvenanceRecorder logs ToneProfile variant per affected stage output |

**Modularity seam families (swap contract summary):**

| Seam family | Replaceable unit | Neighbor guarantee | Swap without renegotiating |
|-------------|------------------|--------------------|-----------------------------|
| **Generation pipeline** | Per-stage executor behind StageExecutorPort | Upstream/downstream manifest types fixed per 1.2.1 table | DAG topology, stage ids, manifest type names |
| **Rule engine** | Ruleset plugin behind RulePluginPort | Core primitive vocabulary + hook declaration schema | Simulation tick orchestration, WorldState projection |
| **Event bus** | Bus transport + subscription adapter | Event category names and delivery semantics per 1.1 | Subscriber behavior implementations |
| **Input loop** | Intent parser + population resolver | Intent envelope shape + canon gate routing | Simulation consume path, Presentation feedback |

**Safety invariants (design-level):**

| Invariant | Contract (conceptual) |
|-----------|----------------------|
| **SeedSnapshot** | Trigger: before CompiledWorldManifest commit, DM structural re-generation, or ruleset swap affecting live world. Captures: SeedBundle fingerprint, ToneProfile id, accepted CanonFact set hash, active ruleset ids, timestamp. Store: session-scoped snapshot vault (execution track names storage path). Rollback: restore from snapshot invalidates subsequent event log tail — DM-visible |
| **DryRunValidator** | Trigger: same gates as SeedSnapshot. Validates: DAG pre-flight (inherits DAGValidator), rule conflict scan, spatial overlap estimate, unreachable NPC reference check — mirrors DeterministicCompiler checks in read-only mode. Outcome: `dry_run.pass` enables commit; `dry_run.fail` blocks with cited provenance |
| **ProvenanceEnvelope** | Every CompiledWorldManifest element and sim graph seed carries: originating stage executor id (or `default`), ruleset id, SeedBundle fingerprint, ToneProfile id. DM and export tooling may inspect in-session or via metadata export (execution-deferred format) |

**Exports to Phase 2+:**

| Export | Consuming phase |
|--------|----------------|
| **SeamRegistry** (seam id → port owner → swap contract) | Phase 2 stage executor mint; Phase 5 community seam docs |
| **SeedSnapshot schema** (field names + trigger matrix) | Phase 2 generation pipeline; Phase 6 iteration harness |
| **DryRunValidator gate matrix** (which operations require dry-run) | Phase 2 DM overwrite flows; Phase 6 testing |
| **ProvenanceEnvelope schema** | Phase 5 extensibility; operator debug surfaces |

**Adjacent slices:** Phase 1 primary glue task complete when 1.1 + 1.2 + **this note** satisfy breadth-first Phase 1 checklist. Phase 2 materializes executors behind each port. Execution track will mint typed port contracts under `Roadmap/Execution/` mirror spine.

## Edge cases

- **Partial seam swap mid-session:** Swapping a stage executor after partial generation requires new SeedSnapshot + full dry-run; cannot hot-swap mid-DAG traversal without orchestrator abort and restart from last snapshot.
- **Ruleset conflict without dry-run:** RulePluginPort registration must declare conflicts; DryRunValidator surfaces unresolved conflicts before sim tick adoption — no silent merge.
- **Bus subscriber ordering:** BusSubscriptionPort does not guarantee delivery order across subscribers unless explicitly declared per category — document ordering assumptions in seam registry, not implicit global order.
- **Input parser extension:** New input type (e.g. voice) adds parser behind IntentParserPort; must not bypass CanonCommitBoundary — same envelope shape as player-lite intents.
- **Snapshot storage pressure:** Multiple snapshots per session — retention policy (keep last N or last per structural operation) deferred to execution track; conceptual layer requires **at least one** restorable snapshot before first world commit.
- **Dry-run false positive:** Estimate-only mode may diverge from full compile on edge cases — ProvenanceRecorder logs dry-run profile id; execution track may tighten parity tests (advisory on conceptual).
- **Community ruleset without provenance:** Rulesets missing ProvenanceEnvelope declaration rejected at RulePluginPort registration — not at runtime crash.

## Open questions

- **Snapshot retention count** per session — execution track / operator preference (conceptual requires existence, not count).
- **Dry-run performance budget** for large worlds — Phase 6 iteration harness; conceptual names the gate only.
- **SeamRegistry packaging** for community contributors — Phase 5 documentation; 1.3 names seam ids only.
- **Cross-seam dependency:** Whether ToneProfile swap requires full regen vs. partial stage replay — lean full snapshot + regen for structural safety; operator may relax on execution track with explicit waiver.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — four seam families + three safety invariants; execution paths deferred |
| Behavior (actors, ordering) | pass | § Behavior — SeamRegistry through ProvenanceRecorder; snapshot → dry-run → commit ordering |
| Interfaces (adjacent contracts) | pass | § Interfaces — 1.1/1.2 imports + Phase 2+ exports; swap contract table |
| Edge cases | pass | § Edge cases — partial seam swap, ruleset conflict, snapshot pressure, dry-run false positive |
| Open questions | pass | § Open questions — retention count, dry-run budget, seam packaging deferred |
| Pseudo-code readiness | pass | § Pseudo-code readiness — seam families mappable without API signatures |
| Tertiary coverage (1.3.x) | pass | [[Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]] (1.3.1); [[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]] (1.3.2); [[Phase-1-3-3-DryRunValidator-and-ProvenanceEnvelope-Contract-Roadmap-2026-06-29-1205]] (1.3.3) — **branch closed** |
| **`handoff_readiness` aggregate** | **80%** | factory feed gate reconcile `phase_1_secondary_tree` slice 1.3 — **Phase 1 secondary tree complete** |

> Execution-deferred / advisory on conceptual track: Godot port contracts, factory catalog rows, snapshot storage paths, HR rollup gates — resolved on execution track or factory harness (`1373c0c3408d`). Phase-1 **tertiary tree** complete for 1.1 + 1.2 + 1.3 branches. Factory feed gate may remain **RED** for Phase 1 primary oversize or other harness targets — not tertiary incompleteness. **1.3 branch closed** (1.3.1–1.3.3).

## Pseudo-code readiness

A reader can map four seam families to Phase 1.1 layers and Phase 1.2 stage ports, and can list the three safety invariants (SeedSnapshot, DryRunValidator, ProvenanceEnvelope) with trigger gates — without API signatures. Execution deepen mints typed port contracts and snapshot schemas under `Roadmap/Execution/` mirror spine.

## Research integration

Key takeaways (consistent with chain research consumed on 1.1/1.2):

- **Replaceability by construction:** PMG mandates every generation stage, sim tick, camera controller, and input loop swappable via clear interfaces — SeamRegistry makes that mandate auditable [[genesis-mythos-master-goal]]
- **Deterministic compile + dry-run pairing:** WorldGen compiler pattern requires estimate-only pass before commit — aligns DeterministicCompiler (1.2) with DryRunValidator (1.3) [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]
- **Session-scoped DI:** Greenfield Godot guidance — wire seams at session composer, not global autoload loops (inherits 1.1) [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-godot-gmm-033500Z]]
- **Living world continuity:** SeedSnapshot + event log backbone — snapshot before structural change preserves rewind narrative (WorldLines influence via 1.1)


## Tasks

- [x] Mint secondary 1.3 — modularity seams + safety invariants (four seam families; SeedSnapshot; DryRunValidator; ProvenanceEnvelope)
- [x] CDR + decisions-log closure — [[Conceptual-Decision-Records/deepen-modularity-seams-safety-invariants-2026-06-26-1437]] validated
- [x] Primary Phase 1 glue checkbox + progress rollup (IRA 2026-06-26)
- [x] Advance-phase gate evaluation — Phase 1→2 (godo-advance-phase-20260626; handoff ~82%; RECAL deferred advisory on conceptual track)
- [x] Mint **1.3.1** SeamRegistry canonical index tertiary — [[Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]] (`architect-rr-gmm-remi-phase1-131-tertiary`)
- [x] Mint **1.3.2** SeedSnapshotAuthority contract tertiary — [[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]] (`architect-rr-gmm-remi-phase1-132-tertiary`)
- [x] Mint **1.3.3** DryRunValidator + ProvenanceEnvelope tertiary — [[Phase-1-3-3-DryRunValidator-and-ProvenanceEnvelope-Contract-Roadmap-2026-06-29-1205]] (`architect-rr-gmm-remi-phase1-133-tertiary`)
- [ ] OQ-defer-1.3.3-001: Cross-link DryRun gate matrix to Phase 2 generation pipeline (deferred — parent owns)
- [ ] OQ-defer-1.3.3-002: Cross-link ProvenanceEnvelope to Phase 5 extensibility (deferred — parent owns)

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
