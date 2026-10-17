---
title: Phase 3.3 — Roll-up & DM Overwrite / Re-Generation Policy Tables
roadmap-level: rollup
phase-number: 3
subphase-index: '3.3'
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-secondary: '[[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-3
- rollup
- dm-authority
- overwrite
- re-generation
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Actors

| Actor | Role |
|-------|------|
| **DMOverwriteClass** | Labels each DM action: `live_patch`, `canon_touching_patch`, `structural_re_gen` |
| **LiveOverwriteRegistry** | Allowlist of mutable fields per class; rejects structural edits at registry boundary |
| **StructuralChangeDetector** | Scans proposed DM edit against topology/seed invariants; escalates to re-gen when thresholds crossed |
| **OverwritePatchLayer** | Ordered patch stack applied at **WorldStateCommitter** boundary; patches carry `dm_authority: true` provenance |
| **ReGenerationIntentQueue** | Holds deferred region/full-world jobs; DM confirms cost + downtime narrative before execution |
| **DMPauseGate** | **3.1** hook — overwrites apply only when tick advance halted or between atomic commits |
| **SpeculativeDeltaReconciler** | When DM patches conflict with queued speculative **TickDelta** proposals, arbiter picks DM authority or defers to re-gen |
| **NarrativeDeltaVetoPolicy** | For **3.2** `dm_queue` items: `accept`, `retroactive_veto`, `trigger_re_gen`, or `fork_thread` |
| **CanonConflictArbiter** | Escalates canon-touching patches to **2.2** **IntentResolver** before commit |
| **RollbackWindow** | DM may pop last N live patches within session; beyond window → re-gen or log reconcile |

## Policy matrix

| Edit kind | Default class | Tick interaction | Re-gen required |
|-----------|---------------|------------------|-----------------|
| Move map token / marker | `live_patch` | Apply at next commit boundary | No |
| Nudge weather variable | `live_patch` | Merge via **ConsequenceResolver** as DM-weighted delta | No |
| Fire one-shot scripted event | `live_patch` | Append **WorldEventLog** DM event envelope | No |
| NPC whisper / hidden agenda nudge | `canon_touching_patch` | Pause auto-brief (**3.2**); arbiter if hook conflict | No unless hook demands |
| Faction edge weight override | `canon_touching_patch` | May veto **3.2** surfaced delta retroactively | No unless graph surgery |
| Terrain reshape / biome move | `structural_re_gen` | **DMPauseGate** hold; queue re-gen job | Yes (region minimum) |
| Seed / graph topology surgery | `structural_re_gen` | Block live patches; full or regional re-gen | Yes |

## Live patch flow

```
DMPauseGate → DMOverwriteClass → StructuralChangeDetector?
  → LiveOverwriteRegistry → CanonConflictArbiter?
  → OverwritePatchLayer + ProvenanceEnvelope
  → SpeculativeDeltaReconciler → WorldStateCommitter
  → NarrativeDeltaVetoPolicy → dm.overwrite_applied
```

## Structural re-gen flow

```
StructuralChangeDetector | explicit DM → ReGenerationIntent
→ DMPauseGate hold (live patches frozen)
→ DM confirms scope + cost copy (ToneProfile)
→ handoff Phase 2.1 generation spine (exec owns DAG)
→ SeedSnapshot + WorldEventLog fork/merge per 1.3
→ invalidate 3.2 "since you left" anchors → dm.re_gen_queued
```

## Interface tables

### Imports from 3.1

| Export | Consumption |
|--------|-------------|
| **DMPauseGate** | Overwrite window; tick halt during structural re-gen |
| **Speculative delta queue** | **SpeculativeDeltaReconciler** merge/veto |
| **WorldStateCommitter** | Patch layer at commit boundary |
| **WorldEventLog** | DM events as provenance-tagged entries |
| **CommittedTickRecord** | Rollback window anchors |

### Imports from 3.2 / Phase 2 / 1

| Export | Consumption |
|--------|-------------|
| **NarrativeSurfacingPolicy** `dm_queue` (**3.2**) | **NarrativeDeltaVetoPolicy** |
| **NarrativeDelta** / **ThreadRevealGate** (**3.2**) | Veto/fork without leaking suppressions |
| **IntentResolver** / **LoreHookRegistry** (**2.2**) | Canon-touching arbitration |
| **ToneProfileBundle** (**2.3**) | DM confirmation copy tone |
| **ProvenanceEnvelope** + replay (**1.3**) | Auditable mutations; re-gen fork policy |

### Exports

| Export | Consumer |
|--------|----------|
| **DM authority classification** | Phase 4 perspective locks |
| **ReGenerationIntent** | Phase 2.1 execution pipeline |
| `dm.overwrite_applied` / `dm.re_gen_queued` | Audit / presentation buses |

## Edge cases

- **Patch during catch-up:** Complete current **3.1** commit, then hold; patches before resume.
- **Conflicting DM patches:** Stack order wins; reorder within **RollbackWindow**.
- **Retroactive veto vs player knowledge:** `fork_thread` + **WorldEventLog** fork marker.
- **Partial regional re-gen:** Default full-region job; sub-region attestation deferred to factory catalog.
- **Overwrite on empty world:** Valid on degenerate **SimGraphSeed**.
- **ToneProfile missing:** (a) unknown `profile_id` → **ToneFallbackResolver** Medium Fantasy + `narrative.tone_fallback_applied`; (b) missing bundle at session 0 → block structural re-gen auto-copy; corruption → block + DM reconcile.
- **Replay after patch stack:** **1.3** log-hash; unreproducible patches → block + DM reconcile.

## Open questions

- Patch stack depth before forced re-gen audit — factory catalog attestation.
- Multi-DM concurrent authority — deferred Phase 5+; v1 single DM seat.
- Re-gen compute cost — narrative downtime only on conceptual; compute execution-deferred.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | Parent § Scope |
| Behavior (actors, ordering) | pass | § Actors + matrix + flows |
| Interfaces (adjacent contracts) | pass | § Interface tables |
| Edge cases | pass | § Edge cases |
| Open questions | pass | § Open questions |
| Pseudo-code readiness | pass | Live patch / re-gen paths traceable |
| **`handoff_readiness` aggregate** | **80%** | factory feed body compact 2026-07-15 |

> Execution-deferred / advisory: typed serializers, HR gates — execution track or factory harness (`1373c0c3408d`).

## Responsibilities (rollup authority)

- [x] Overwrite classification, patch layer, re-generation intent queue
- [x] Policy matrix + live vs structural flows
- [x] Integration spine with **3.1** pause/speculative queue and **3.2** dm_queue veto
- [x] Phase 3 secondary breadth closure (3.1–3.3)

## Tasks (rollup authority)

- [x] Preserve full NL tables after secondary body compact under feed cap 1400
- [ ] Optional tertiaries (allowlist detail, re-gen scope templates, rollback rules) — deferred breadth-first
