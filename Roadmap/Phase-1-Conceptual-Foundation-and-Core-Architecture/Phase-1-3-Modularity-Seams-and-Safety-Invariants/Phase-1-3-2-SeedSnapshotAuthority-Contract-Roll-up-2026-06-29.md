---
title: Phase 1.3.2 — Roll-up & SeedSnapshot Schema Tables
roadmap-level: rollup
phase-number: 1
subphase-index: 1.3.2
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- rollup
- seed-snapshot
- modularity-seams
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Scope (detail)

**In scope:** **SeedSnapshotAuthority** actor and responsibilities; **trigger matrix** (which operations require snapshot before proceed); **SeedSnapshot schema** (conceptual field names + semantics); **capture ordering** relative to [[Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]] published registry and [[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]] accepted CanonFacts boundary; **rollback intent** (restore invalidates subsequent event log tail — DM-visible); **session-scoped snapshot vault** as conceptual noun (execution track names persistence); minimum **one restorable snapshot** before first world commit.

**Out of scope:** DryRunValidator gate matrix and estimate-only compile (1.3.3); ProvenanceEnvelope field schema (1.3.3); snapshot retention count policy (execution / operator); Godot serialization, file paths, HR rollup gates; factory catalog row mint; User-Story / L5 scopes.

## Behavior (detail)

**Actors:** SeedSnapshotAuthority (capture + seal authority), SnapshotSealer (marks snapshot immutable after capture), RollbackOrchestrator (restores from snapshot handle — coordinates with WorldEventLog tail invalidation), SnapshotVault (session-scoped catalog of sealed snapshots — conceptual only).

**Ordering:**

1. **SeamRegistry** must be `published` before SeedSnapshotAuthority accepts capture requests that cite `gen.stage.*` seam ids — unpublished registry → `snapshot.registry_unpublished` on `session.*`.
2. On any **triggered operation** (see matrix): SeedSnapshotAuthority **captures** → SnapshotSealer **seals** → operation may proceed to DryRunValidator (1.3.3) and commit path.
3. **Partial seam swap mid-session** (parent edge case): new capture required; cannot hot-swap mid-DAG without orchestrator abort and restart from last sealed snapshot.
4. **Rollback:** RollbackOrchestrator restores snapshot handle; subsequent WorldEventLog entries after snapshot timestamp are invalidated; DM receives `snapshot.restored` intent on `session.*` with cited snapshot id.

**Inputs / outputs:**

- *In:* trigger event (operation class + affected seam ids from registry); current SeedBundle fingerprint; ToneProfile id; accepted CanonFact set hash; active ruleset ids; session clock.
- *Out:* **SeedSnapshot** handle (opaque id); `snapshot.captured` on `session.*`; sealed record in SnapshotVault; optional cite for DryRunValidator pre-flight (1.3.3).

## SeedSnapshot schema (conceptual fields)

| Field | Semantics | Source |
|-------|-----------|--------|
| `snapshot_id` | Opaque session-unique handle | SeedSnapshotAuthority mint |
| `captured_at` | Session monotonic clock | SessionComposer |
| `seed_bundle_fingerprint` | Hash of active SeedBundle | WorldState layer |
| `tone_profile_id` | Active ToneProfile variant | 1.2 ToneProfileInjector touchpoint |
| `accepted_canon_facts_hash` | Hash of **accepted** CanonFacts only | CanonCommitBoundary (1.1.2) |
| `active_ruleset_ids` | Ordered list of bound ruleset ids | RulePluginPort bindings |
| `seam_registry_revision` | Published registry version / hash | SeamRegistry (1.3.1) |
| `trigger_operation` | Operation class that caused capture | Trigger matrix row |
| `affected_seam_ids` | Subset of registry ids touched | From trigger + operation payload |

## Trigger matrix (design-level)

| Operation class | Requires snapshot | Cites seam families | Notes |
|-----------------|-------------------|---------------------|-------|
| `compile_world_manifest_commit` | **yes** | `gen.stage.*` | Before DeterministicCompiler full commit (1.2) |
| `dm_structural_regeneration` | **yes** | `gen.stage.*`, `rule.core.*` | DM overwrite class structural (inherits 3.3 policy) |
| `ruleset_swap_live` | **yes** | `rule.core.*`, `rule.conflict.*` | No silent merge — snapshot before adoption |
| `stage_executor_swap` | **yes** | single `gen.stage.<id>` | Mid-DAG swap requires abort + restart from snapshot |
| `tone_profile_swap` | **yes** (lean full regen) | cross-cutting on receptive stages | OQ-1.3.2-003 — full snapshot + regen default |
| `intent_parser_swap` | **yes** | `input.intent.*` | Envelope shape unchanged; parser only |
| `dry_run_estimate_only` | **no** | — | DryRunValidator (1.3.3) — read-only path |
| `bus_subscriber_swap` | **no** (default) | `bus.*` | Unless subscriber owns world projection — operator waiver |

## Interfaces (detail)

**Imports:**

| Source | Consumption |
|--------|-------------|
| [[Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]] | `affected_seam_ids` vocabulary; registry must be `published` |
| [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]] | Stage ids for generation triggers; manifest commit boundary |
| [[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]] | accepted vs proposed CanonFacts — only accepted in hash |
| Parent 1.3 § Behavior | SeedSnapshotAuthority ordering before DryRunValidator |

**Exports to siblings / Phase 2+:**

| Export | Consumer |
|--------|----------|
| **SeedSnapshot schema** + trigger matrix | 1.3.3 DryRunValidator (same gates, estimate-only branch) |
| **Snapshot handle** contract | Phase 2 generation pipeline; Phase 6 iteration harness |
| **Rollback intent** | DM overwrite flows (Phase 3.3); event log tail policy |

## Edge cases

- **Snapshot without published registry:** Capture rejected — structural safety over silent capture with orphan seam ids.
- **Proposed CanonFact in snapshot:** Rejected at capture — only `accepted` facts enter hash; proposed facts remain outside snapshot boundary.
- **Multiple snapshots per session:** Conceptual layer requires **at least one** before first commit; retention count (keep last N vs last per operation) deferred to execution track.
- **Rollback during active DM cam:** RollbackOrchestrator coordinates with DMPauseGate read-only posture (Phase 3.1) — conceptual names coordination, not implementation.
- **Snapshot storage pressure:** Operator may purge old sealed snapshots on execution track; conceptual invariant is restorability of **latest sealed** snapshot before each triggered operation class.
- **Cross-seam dependency (ToneProfile):** Full snapshot + regen preferred over partial stage replay for structural safety — execution may relax with explicit operator waiver flag.

## Open questions

- OQ-1.3.2-001: Snapshot retention count per session — execution track / operator preference (conceptual requires existence, not count).
- OQ-1.3.2-002: Whether `bus_subscriber_swap` ever requires snapshot when subscriber mutates WorldState projection — default no; waiver path on execution track.
- OQ-1.3.2-003: ToneProfile swap — confirm full regen vs partial stage replay default (lean full snapshot + regen per parent § Open questions).

## Pseudo-code readiness

A reader can list eight SeedSnapshot schema fields, six mandatory trigger rows, and state the capture → seal → (dry-run) → commit ordering without API signatures. Execution track mirrors schema under `Roadmap/Execution/` parallel spine when execution deepen begins.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — snapshot authority; DryRun / Provenance deferred to 1.3.3 |
| Behavior (actors, ordering) | pass | § Behavior — capture → seal; registry publication gate |
| Interfaces (adjacent contracts) | pass | § Schema + trigger matrix + imports |
| Edge cases | pass | § Edge cases — registry unpublished, proposed canon, retention, ToneProfile |
| Open questions | pass | § Open questions — OQ-1.3.2-001..003 |
| Pseudo-code readiness | pass | § Pseudo-code readiness — diagrammable without signatures |
| **`handoff_readiness` aggregate** | **79%** | factory feed tertiary mint; **1.3 branch closed** (1.3.1–1.3.3 complete) |

## Tasks

- [x] SeedSnapshot schema + trigger matrix tables (rollup)
- [x] Behavior ordering + edge cases + OQs
- [x] Handoff readiness matrix
- [x] Body compact 2026-06-29 — dense tables moved from tertiary parent per 1.3.1 pattern
