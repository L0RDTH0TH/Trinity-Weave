---
title: Phase 3.3 — DM Overwrite vs Deliberate Re-Generation Policy
roadmap-level: secondary
phase-number: 3
subphase-index: "3.3"
project-id: genesis-mythos-master
status: in-progress
priority: high
progress: 33
handoff_readiness: secondary_minted
created: 2026-06-26
tags: [roadmap, genesis-mythos-master, phase-3, dm-authority, overwrite, re-generation, narrative-policy]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]"
  - "[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]"
  - "[[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]"
  - "[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]"
  - "[[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]"
  - "[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]"
  - "[[genesis-mythos-master-goal]]"
product_factory_run_id: f35ff65cfb4f
---

## Phase 3.3 — DM Overwrite vs Deliberate Re-Generation Policy

Define **when the DM may mutate live simulation state** (overwrite patches) versus **when structural change must trigger deliberate re-generation** of regions or the full world. This slice owns **authority classification**, **patch-layer semantics**, **re-generation queue contracts**, and **reconciliation** with **3.1** tick commit boundaries and **3.2** narrative delta DM queues — without Godot implementation paths on conceptual track.

## Scope

**In scope:** **DMOverwriteClass** taxonomy (live patch vs structural re-gen); **LiveOverwriteRegistry** (token moves, weather nudges, one-shot events, NPC whispers, faction edge nudges within canon-safe bands); **StructuralChangeDetector** (terrain reshape, biome relocation, graph topology surgery, seed-altering edits); **ReGenerationIntentQueue** (region-scoped vs full-world jobs with cost/intent envelope); **OverwritePatchLayer** (DM edits as ordered patches atop **WorldState** without invalidating **WorldEventLog** replay when possible); **DMPauseGate** coordination (overwrite application only while paused or between ticks per **3.1**); **SpeculativeDeltaReconciler** (merge or veto **3.1** speculative queue entries against DM patches); **NarrativeDeltaVetoPolicy** (retroactive handling of **3.2** `dm_queue` entries); **CanonConflictArbiter** (routes to **2.2** intent resolver when overwrite touches **LoreHookRegistry**); **ProvenanceEnvelope** for every DM-authored mutation (extends **1.3**); **RollbackWindow** (how far back DM may undo live patches before re-gen required).

**Out of scope:** Per-tick **SimTickPipeline** ordering and **ConsequenceResolver** merge math (**3.1**); **SinceYouLeftCompiler** narrative packaging (**3.2**); proc-gen DAG execution and region mesh rebuild (**Phase 2.1** execution deepen); Godot editor tooling for DM table; execution-track typed overwrite serializers and rollup HR gates (**execution-deferred / advisory on conceptual track**).

## Behavior

**Actors:**

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

**Policy matrix (conceptual):**

| Edit kind | Default class | Tick interaction | Re-gen required |
|-----------|---------------|------------------|-----------------|
| Move map token / marker | `live_patch` | Apply at next commit boundary | No |
| Nudge weather variable | `live_patch` | Merge via **ConsequenceResolver** as DM-weighted delta | No |
| Fire one-shot scripted event | `live_patch` | Append **WorldEventLog** DM event envelope | No |
| NPC whisper / hidden agenda nudge | `canon_touching_patch` | Pause auto-brief (**3.2**); arbiter if hook conflict | No unless hook demands |
| Faction edge weight override | `canon_touching_patch` | May veto **3.2** surfaced delta retroactively | No unless graph surgery |
| Terrain reshape / biome move | `structural_re_gen` | **DMPauseGate** hold; queue re-gen job | Yes (region minimum) |
| Seed / graph topology surgery | `structural_re_gen` | Block live patches; full or regional re-gen | Yes |

**Flow (DM applies live patch):**

1. **DMPauseGate** engaged (or between ticks)
2. **DMOverwriteClass** classifies edit; **StructuralChangeDetector** short-circuits to re-gen queue if structural
3. **LiveOverwriteRegistry** validates field allowlist
4. **CanonConflictArbiter** runs for `canon_touching_patch`
5. **OverwritePatchLayer** pushes ordered patch with **ProvenanceEnvelope**
6. **SpeculativeDeltaReconciler** resolves conflicts with **3.1** speculative queue
7. On tick resume: **WorldStateCommitter** applies patch layer before subsystem proposals
8. **NarrativeDeltaVetoPolicy** updates **3.2** queue entries if retroactive veto needed
9. Publish `dm.overwrite_applied` on `narrative.*` bus — audit trail for session

**Flow (DM triggers deliberate re-generation):**

1. **StructuralChangeDetector** or explicit DM command enqueues **ReGenerationIntent**
2. **DMPauseGate** holds tick advance; live patches frozen
3. DM confirms scope (region id vs full world) and narrative cost copy
4. Handoff to **Phase 2.1** generation pipeline (conceptual contract only — execution owns DAG run)
5. On completion: new **SeedSnapshot** + **WorldEventLog** genesis fork or merge policy per **1.3** replay contract
6. **3.2** compilers invalidated for pre-re-gen anchors — brief "world reshaped" not "since you left" deltas

**Inputs / outputs:**

- *Into 3.3:* **DMPauseGate** + speculative delta queue (**3.1**); **dm_queue** **NarrativeDelta** entries (**3.2**); **LoreHookRegistry** + **IntentResolver** (**2.2**); **ToneProfileBundle** for DM-facing cost copy tone (**2.3**)
- *Out of 3.3:* **OverwritePatchLayer** contract; **ReGenerationIntent** schema; `dm.overwrite_applied` / `dm.re_gen_queued` events; veto decisions on **3.2** deltas

## Interfaces

**Imports from Phase 3.1:**

| 3.1 export | How 3.3 consumes it |
|------------|---------------------|
| **DMPauseGate** | Overwrite application window; tick halt during structural re-gen |
| **Speculative delta queue** | **SpeculativeDeltaReconciler** merge/veto |
| **WorldStateCommitter** | Patch layer applied at commit boundary |
| **WorldEventLog** append contract | DM events as provenance-tagged log entries |
| **CommittedTickRecord** | Rollback window anchor ticks |

**Imports from Phase 3.2:**

| 3.2 export | How 3.3 consumes it |
|------------|---------------------|
| **NarrativeSurfacingPolicy** `dm_queue` | **NarrativeDeltaVetoPolicy** retroactive handling |
| **NarrativeDelta** schema | Veto/fork metadata on delta items |
| **ThreadRevealGate** | Spoiler-safe veto without leaking suppressed threads |

**Imports from Phase 2 / 1:**

| Export | How 3.3 consumes it |
|--------|---------------------|
| **IntentResolver** (**2.2**) | Canon-touching patch arbitration |
| **ToneProfileBundle** (**2.3**) | DM confirmation copy tone |
| **ProvenanceEnvelope** + replay (**1.3**) | Every DM mutation auditable; re-gen fork policy |

**Exports to Phase 4+:**

| Export | Consumer |
|--------|----------|
| **DM authority classification** | Perspective layers respect DM-held narrative locks |
| **ReGenerationIntent** handoff | Phase 2.1 execution pipeline (when structural) |

**Adjacent slices:**

- **3.1** owns tick truth; **3.3** never bypasses commit atomicity.
- **3.2** surfaces deltas; **3.3** may veto retroactively but does not compile narrative copy.
- Structural re-gen **delegates execution** to Phase 2 generation spine — **3.3** owns policy and queue semantics only.

## Edge cases

- **Patch during catch-up:** **3.1** **TickScheduler** mid-catch-up — **DMPauseGate** completes current commit then holds; patches apply before resuming catch-up.
- **Conflicting DM patches:** Stack order wins; DM may explicitly reorder within **RollbackWindow**.
- **Retroactive veto vs player knowledge:** **NarrativeDeltaVetoPolicy** `fork_thread` preserves player-facing truth while DM branch diverges — requires **WorldEventLog** fork marker.
- **Partial regional re-gen:** Region boundary ambiguous — default queue full-region job; sub-region attestation deferred to factory catalog.
- **Overwrite on empty world:** Valid — registry allows token/weather patches on degenerate **SimGraphSeed**.
- **ToneProfile missing at runtime:** (a) **unknown `profile_id` post-selection** — **ToneFallbackResolver** applies Medium Fantasy narrative weights + `narrative.tone_fallback_applied` (mirrors **3.1** / **3.2** / **2.3**); live patches may still apply with fallback copy; (b) **missing bundle at session boundary** (never selected at session 0) — block DM confirmation auto-copy for structural re-gen per **2.3** SeedBundle attachment + **2.1** SeedParser block; bundle corruption/hash mismatch — block structural re-gen queue + route to DM reconcile (not silent fallback).
- **Replay after DM patch stack:** **1.3** replay compares log hash; DM patches must be reproducible from log or replay blocks with DM reconcile prompt.

## Open questions

- **Patch stack depth limit:** Max live patches per session before forced re-gen audit — operator attestation via factory catalog; not resolved on conceptual track.
- **Multi-DM sessions:** Concurrent DM authority — deferred to Phase 5+; v1 assumes single DM seat.
- **Cost model for re-gen:** Narrative downtime copy only on conceptual track; compute cost execution-deferred.

## Pseudo-code readiness

A reader can trace DM edit → classification → pause gate → patch layer or re-gen queue → speculative reconciliation → narrative veto → bus audit without guessing ownership. **3.3** does not own tick subsystem ordering or delta compilation. No API signatures on conceptual track; execution deepen mints typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

Pattern alignment (no new pre-deepen research this run):

- Live GM override layers atop simulation — separated from structural regen per cost/intent doctrine in PMG
- Event-sourced DM provenance — extends **WorldEventLog** + **ProvenanceEnvelope** from **1.3** / **3.1**
- Retroactive narrative veto — coordinates **3.2** surfacing policy without breaking sim authority

## Responsibilities

- [x] Name overwrite classification, patch layer, and re-generation intent queue
- [x] Document policy matrix and flows for live patch vs structural re-gen
- [x] Integration spine with **3.1** DMPauseGate + speculative queue and **3.2** dm_queue veto
- [x] Phase 3 breadth closure — third secondary minted; tertiaries deferred breadth-first

## Tasks

- [x] Mint 3.3 secondary with DM authority actor registry and policy matrix
- [ ] Optional tertiaries: live overwrite allowlist detail, re-gen scope templates, rollback window rules — deferred breadth-first
- [x] **3.1→3.3** handoff — DMPauseGate + speculative delta queue seams satisfied
- [x] **3.2→3.3** handoff — NarrativeDeltaVetoPolicy + dm_queue integration documented

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
