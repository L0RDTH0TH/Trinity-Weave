---
title: Phase 3.2 — Roll-up & Off-Screen Narrative Delta Tables
roadmap-level: rollup
phase-number: 3
subphase-index: '3.2'
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-secondary: '[[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-3
- rollup
- off-screen
- faction
- tribe
- narrative-delta
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Actors

| Actor | Role |
|-------|------|
| **OffScreenActivityWindow** | Records `last_player_presence_tick` + `last_session_wall_clock`; defines absence span |
| **FactionGraphDeltaExtractor** | Diffs reputation/tension edges + tribe membership between two **CommittedTickRecord** anchors |
| **TribeActivityScheduler** | Threshold rules for off-screen raids, migrations, treaty shifts while player absent |
| **SinceYouLeftCompiler** | Merges **FactionGraphDelta** + selected **WorldEventLog** into ranked **NarrativeDelta** |
| **NarrativeSurfacingPolicy** | Routes: `auto_brief` / `dm_queue` / `suppress` |
| **AbsenceCatchupBridge** | Coordinates with **3.1** **TickScheduler** catch-up caps — packaging only |
| **ThreadRevealGate** | Faction/tribe reveals respect **LoreHookRegistry** `sim-active` vs `hooked-only` |
| **ToneProfileNarrativeWeights** | Severity → narrative tone per **ToneProfileBundle** |

## Absence → narrative flow

```
window = OffScreenActivityWindow.span(session)
catchup = AbsenceCatchupBridge.request_or_read(window)  # capped by 3.1 TickScheduler
delta = FactionGraphDeltaExtractor.diff(tick_depart, tick_return)
items = SinceYouLeftCompiler.compile(delta, WorldEventLog, ToneProfileNarrativeWeights)
routed = NarrativeSurfacingPolicy.split(items, ThreadRevealGate)
publish narrative.since_you_left_compiled  # Presentation read-only
```

## Interface tables

### Imports from 3.1

| Export | Consumption |
|--------|-------------|
| **CommittedTickRecord** | Diff anchors |
| **FactionGraphSubsystem** (via log/state) | Raw edge changes — 3.2 packages only |
| **TickScheduler** catch-up caps | **AbsenceCatchupBridge** respects; overflow → deferred narrative |
| **DMPauseGate** | Compiler pauses auto-surfacing while DM holds authority |

### Imports from Phase 2

| Export | Consumption |
|--------|-------------|
| **LoreHookRegistry** faction/tribe hooks (**2.2**) | Named entities / thread ids on **NarrativeDelta** |
| **ToneProfileBundle** (**2.3**) | **ToneProfileNarrativeWeights** |

### Exports

| Export | Consumer |
|--------|----------|
| **NarrativeDelta** | Phase 4 perspective (read-only) |
| **OffScreenEvent** proposals | **3.1** tick loop during catch-up |
| **DM queue delta entries** | **3.3** overwrite / re-gen policy |

## Edge cases

- **Zero absence:** Empty brief; not an error.
- **Catch-up deferred:** Use last committed tick + `sim.catchup_deferred`; no fabricated future.
- **Conflicting thread reveals:** Both to DM queue; no auto-brief.
- **Empty faction graph:** Weather/NPC-only notes if log exists; else empty.
- **ToneProfile missing:** (a) unknown `profile_id` → **ToneFallbackResolver** Medium Fantasy + `narrative.tone_fallback_applied`; (b) missing bundle at session 0 → block auto-brief; corruption → block + DM reconcile.
- **Spoiler suppression:** Undiscovered faction → `suppress` + `dm_queue` hint.

## Open questions

- Brief length budget — factory catalog attestation.
- Tribe vs faction granularity — lean single **FactionGraphDelta** + `entity_kind`.
- Multiplayer absence — deferred Phase 5+; v1 single-party.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | Parent § Scope |
| Behavior (actors, ordering) | pass | § Actors + flow |
| Interfaces (adjacent contracts) | pass | § Interface tables |
| Edge cases | pass | § Edge cases |
| Open questions | pass | § Open questions |
| Pseudo-code readiness | pass | Absence→delta→narrative traceable |
| **`handoff_readiness` aggregate** | **79%** | factory feed body compact 2026-07-15 |

> Execution-deferred / advisory: typed delta serializers, HR gates — execution track or factory harness (`1373c0c3408d`).

## Responsibilities (rollup authority)

- [x] Off-screen window, delta extractor, SinceYouLeft compiler
- [x] Surfacing policy + DM queue routing
- [x] Integration spine with **3.1** tick anchors and **2.2** lore hooks
- [x] Handoff closure with **3.3**

## Tasks (rollup authority)

- [x] Preserve full NL tables after secondary body compact under feed cap 1400
- [ ] Optional tertiaries (delta schema, tribe templates, surfacing tiers) — deferred breadth-first
