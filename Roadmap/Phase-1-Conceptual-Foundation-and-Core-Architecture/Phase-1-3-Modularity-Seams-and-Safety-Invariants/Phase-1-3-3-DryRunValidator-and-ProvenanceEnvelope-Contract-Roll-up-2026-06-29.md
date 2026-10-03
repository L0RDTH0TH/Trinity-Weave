---
title: Phase 1.3.3 — Roll-up & DryRun / Provenance Tables
roadmap-level: rollup
phase-number: 1
subphase-index: 1.3.3
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-1-3-3-DryRunValidator-and-ProvenanceEnvelope-Contract-Roadmap-2026-06-29-1205]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- rollup
- dry-run-validator
- provenance-envelope
- modularity-seams
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Scope (detail)

**In scope:** **DryRunValidator** actor and gate matrix (which operations require dry-run vs estimate-only); **validation check catalog** (DAG pre-flight, rule conflict scan, spatial overlap estimate, unreachable NPC reference check); **estimate-only compile** branch (DeterministicCompiler read-only profile — no world write); **outcome vocabulary** (`dry_run.pass`, `dry_run.fail`, `dry_run.estimate_only`); **ProvenanceEnvelope** field schema; **ProvenanceRecorder** attachment rules; **envelope inheritance** on CompiledWorldManifest elements and sim graph seeds; ordering relative to [[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]] snapshot → dry-run → commit path.

**Out of scope:** SeedSnapshot capture mechanics (1.3.2); SeamRegistry index (1.3.1); snapshot storage paths; dry-run performance budgets (Phase 6); metadata export file format; factory catalog row mint; User-Story / L5 scopes; execution-track pseudo-code under `Roadmap/Execution/`.

## Behavior (detail)

**Actors:** DryRunValidator (orchestrates read-only checks), EstimateOnlyCompiler (DeterministicCompiler profile — structural validation without manifest commit), RuleConflictScanner (ruleset hook + conflict pre-scan), SpatialOverlapEstimator (POI/entity overlap heuristic), NPCReachabilityChecker (unresolved lore/NPC reference scan), ProvenanceRecorder (stamps envelopes on committed artifacts), ProvenanceInspector (DM / operator read surface — conceptual only).

**Ordering:**

1. **SeedSnapshotAuthority** must have sealed a snapshot for the operation class (inherits 1.3.2 trigger matrix) — dry-run without snapshot → `dry_run.snapshot_missing` on `session.*`.
2. **SeamRegistry** must be `published` — dry-run cites `affected_seam_ids` from registry.
3. DryRunValidator runs **check catalog** in stable order (see § Interfaces); on all pass → `dry_run.pass` on `session.*` + optional `dry_run.estimate_only` when operation class is estimate-only compile.
4. On any hard fail → `dry_run.fail` with cited check id + provenance cite; commit path blocked.
5. On commit success → **ProvenanceRecorder** attaches **ProvenanceEnvelope** to each CompiledWorldManifest element and sim graph seed node before WorldEventLog append.

**Inputs / outputs:**

- *In:* operation class; snapshot handle (1.3.2); affected seam ids; proposed compile payload or DM structural overwrite descriptor; active ruleset ids; dry-run profile id (`full` | `estimate_only`).
- *Out:* `dry_run.pass` | `dry_run.fail` | `dry_run.estimate_only` on `session.*`; failure report with check id + seam cite; on commit — stamped ProvenanceEnvelope per artifact.

## DryRunValidator gate matrix

| Operation class | Requires dry-run | Profile | Requires snapshot (1.3.2) | Cites seam families | Notes |
|-----------------|------------------|---------|---------------------------|---------------------|-------|
| `compile_world_manifest_commit` | **yes** | `full` | **yes** | `gen.stage.*` | All check catalog rows; blocks commit on fail |
| `dm_structural_regeneration` | **yes** | `full` | **yes** | `gen.stage.*`, `rule.core.*` | Includes NPC reachability + spatial overlap |
| `ruleset_swap_live` | **yes** | `full` | **yes** | `rule.core.*`, `rule.conflict.*` | RuleConflictScanner mandatory |
| `stage_executor_swap` | **yes** | `estimate_only` | **yes** | single `gen.stage.<id>` | Estimate-only compile for swapped stage only; no full manifest commit |
| `tone_profile_swap` | **yes** | `full` | **yes** | cross-cutting on receptive stages | Lean full regen path per 1.3.2 OQ-1.3.2-003 |
| `intent_parser_swap` | **yes** | `estimate_only` | **yes** | `input.intent.*` | Envelope shape unchanged; parser validation only |
| `dry_run_estimate_only` | **yes** | `estimate_only` | **no** | optional `gen.stage.*` | Operator preview / iteration harness — **no world write**; read-only DeterministicCompiler |
| `bus_subscriber_swap` | **no** (default) | — | **no** | `bus.*` | Unless subscriber owns world projection — operator waiver |

**Estimate-only compile branch:** When profile is `estimate_only`, EstimateOnlyCompiler invokes DeterministicCompiler checks (DAGValidator inheritance from 1.2.1, manifest type chain validation) **without** persisting CompiledWorldManifest or mutating WorldState. Outcome emits `dry_run.estimate_only` (not `dry_run.pass` for commit) — operator may promote to full dry-run + commit in a separate operation class. Parity gap between estimate-only and full compile is logged via `dry_run_profile_id` on ProvenanceEnvelope when commit eventually proceeds (OQ-1.3.3-002).

## Validation check catalog

| check_id | Check | Hard fail? | Mirrors (1.2) |
|----------|-------|------------|----------------|
| `dag.preflight` | Stage DAG topology + manifest I/O chain | yes | DAGValidator |
| `rule.conflict_scan` | Unresolved ruleset hook conflicts | yes | RulePluginPort registration |
| `spatial.overlap_estimate` | POI/entity bounding overlap heuristic | yes (structural) | DeterministicCompiler spatial pass |
| `npc.reachability` | Unresolved LoreHookRegistry / NPC refs | yes | EntityManifest validation |
| `canon.boundary` | Proposed CanonFacts excluded from compile input | yes | CanonCommitBoundary (1.1.2) |
| `registry.seam_cite` | All affected seam ids exist in published registry | yes | SeamRegistry (1.3.1) |
| `snapshot.sealed` | Valid snapshot handle for operation class | yes | SeedSnapshotAuthority (1.3.2) |

## ProvenanceEnvelope field schema

| Field | Semantics | Required on |
|-------|-----------|-------------|
| `provenance_id` | Opaque unique stamp per envelope | all stamped artifacts |
| `stamped_at` | Session monotonic clock at commit | all |
| `originating_stage_executor_id` | Seam id or `default` for stage output | manifest elements |
| `ruleset_id` | Active ruleset that shaped artifact | manifest elements, sim seeds |
| `seed_bundle_fingerprint` | From snapshot / active SeedBundle | all |
| `tone_profile_id` | ToneProfile variant at commit | manifest elements from receptive stages |
| `accepted_canon_facts_hash` | Hash of accepted CanonFacts only | all |
| `seam_registry_revision` | Published registry version | all |
| `snapshot_id` | Sealed snapshot handle cited | all commit-path artifacts |
| `dry_run_profile_id` | `full` \| `estimate_only` \| `none` | all — `none` only for operator-waived bus swaps |
| `dry_run_check_report_hash` | Hash of last passing check catalog run | commit-path artifacts |
| `affected_seam_ids` | Seam ids touched by operation | all |

**ProvenanceRecorder rules:**

- Every **CompiledWorldManifest** element receives one envelope before event log append.
- Every **sim graph seed** node receives envelope at sim_bootstrap commit.
- Rulesets missing mandatory envelope declaration rejected at **RulePluginPort** registration (parent edge case) — not at runtime crash.
- DM and export tooling may inspect envelopes in-session; export serialization deferred to execution track.

## Interfaces (detail)

**Imports:**

| Source | Consumption |
|--------|-------------|
| [[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]] | Trigger matrix alignment; snapshot handle prerequisite |
| [[Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]] | `affected_seam_ids` + `seam_registry_revision` |
| [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]] | DAG pre-flight + manifest type chain |
| Parent 1.3 § Behavior | snapshot → dry-run → commit ordering |

**Exports to siblings / Phase 2+:**

| Export | Consumer |
|--------|----------|
| **DryRunValidator gate matrix** + check catalog | Phase 2 generation pipeline; Phase 6 iteration harness |
| **estimate-only compile** contract | Operator preview; Phase 6 dry-run parity tests (advisory) |
| **ProvenanceEnvelope schema** | Phase 5 extensibility; operator debug surfaces |
| **ProvenanceRecorder** attachment rules | Phase 3 DM overwrite flows; export tooling |

## Edge cases

- **Dry-run without snapshot:** Rejected for commit-path operation classes — `dry_run.snapshot_missing`; estimate-only preview may omit snapshot only for `dry_run_estimate_only` class.
- **Estimate-only false positive:** Estimate-only may pass while full compile fails on edge cases — `dry_run_profile_id` + `dry_run_check_report_hash` on envelope enables parity audit on execution track (advisory on conceptual).
- **Partial stage dry-run after swap:** `stage_executor_swap` uses estimate-only profile for single stage — full manifest commit still requires separate `compile_world_manifest_commit` dry-run with `full` profile.
- **Community ruleset without provenance:** Rejected at RulePluginPort registration — envelope fields mandatory in ruleset manifest declaration.
- **Provenance on rollback:** After RollbackOrchestrator restore (1.3.2), envelopes on invalidated event log tail are cite-only — new commit restamps fresh envelopes.
- **Dry-run pass but commit veto:** NarrativeDeltaVetoPolicy (Phase 3.3) may still veto DM overwrite after dry-run pass — dry-run gates structural safety, not narrative policy.

## Open questions

- OQ-1.3.3-001: Dry-run performance budget for large worlds — Phase 6 iteration harness; conceptual names gate only.
- OQ-1.3.3-002: Estimate-only vs full compile parity test suite ownership — execution track / Phase 6 advisory.
- OQ-1.3.3-003: Whether `dry_run_check_report_hash` includes failed attempt history or last-pass only — lean last-pass only for envelope size.

## Pseudo-code readiness

A reader can list eight gate matrix rows (including estimate-only branches), seven validation checks, twelve ProvenanceEnvelope fields, and state snapshot → dry-run → commit → provenance stamp ordering without API signatures. Execution track mirrors schemas under `Roadmap/Execution/` parallel spine when execution deepen begins.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — DryRunValidator + ProvenanceEnvelope; implementation deferred |
| Behavior (actors, ordering) | pass | § Behavior — check catalog order; snapshot prerequisite |
| Interfaces (adjacent contracts) | pass | § Interfaces — gate matrix + envelope schema + imports |
| Edge cases | pass | § Edge cases — estimate-only false positive, rollback, narrative veto |
| Open questions | pass | § Open questions — OQ-1.3.3-001..003 |
| Pseudo-code readiness | pass | § Pseudo-code readiness — diagrammable without signatures |
| **`handoff_readiness` aggregate** | **80%** | factory feed tertiary mint; **1.3 branch closed** (1.3.1–1.3.3 complete) |

## Tasks

- [x] Gate matrix + validation check catalog (rollup)
- [x] ProvenanceEnvelope schema + ProvenanceRecorder rules
- [x] Behavior ordering + edge cases + OQs
- [x] Handoff readiness matrix
- [x] Body compact 2026-06-29 — dense tables moved from tertiary parent per 1.2.1/1.2.2/1.3.1 pattern
