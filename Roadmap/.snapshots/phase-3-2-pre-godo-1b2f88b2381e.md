---
title: Phase 3.2 — Off-Screen Faction / Tribe Activity
roadmap-level: secondary
phase-number: 3
subphase-index: "3.2"
project-id: genesis-mythos-master
status: in-progress
priority: high
progress: 33
handoff_readiness: secondary_minted
created: 2026-06-26
tags: [roadmap, genesis-mythos-master, phase-3, off-screen, faction, tribe, narrative-delta]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]"
  - "[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]"
  - "[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]"
  - "[[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]"
  - "[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]"
  - "[[genesis-mythos-master-goal]]"
---

## Phase 3.2 — Off-Screen Faction / Tribe Activity

Package **off-screen faction and tribe evolution** into player-facing **"since you left…"** narrative deltas without re-running the full tick loop at session load. This slice owns **delta surfacing**, **absence windows**, and **narrative compilers** that read committed simulation history — while **3.1** retains authoritative graph math and per-tick commit boundaries.

## Scope

**In scope:** **OffScreenActivityWindow** (wall-clock and sim-time absence tracking per session); **FactionGraphDeltaExtractor** (diffs reputation/tension edges and tribe membership between two **CommittedTickRecord** anchors); **TribeActivityScheduler** (threshold rules for off-screen raids, migrations, treaty shifts when player is absent); **SinceYouLeftCompiler** (turns delta bundles into DM-reviewable narrative briefs); **NarrativeSurfacingPolicy** (what auto-surfaces vs what queues for DM table); **AbsenceCatchupBridge** (coordinates with **3.1** **TickScheduler** catch-up caps — narrative packaging only, not tick re-execution); **LoreHookRegistry** thread bindings for faction/tribe named entities; **ToneProfileNarrativeWeights** for how consequence severity reads in surfaced copy (extends **2.3** bundle contract).

**Out of scope:** Per-tick **FactionGraphSubsystem** graph math and **ConsequenceResolver** merge (secondary **3.1**); DM overwrite vs deliberate re-generation policy (secondary **3.3**); Godot UI panels for delta review; execution-track typed delta serializers and rollup HR gates (**execution-deferred / advisory on conceptual track**); weather/NPC agenda detail (3.1 tertiaries or refine passes).

## Behavior

**Actors:**

| Actor | Role |
|-------|------|
| **OffScreenActivityWindow** | Records `last_player_presence_tick` and `last_session_wall_clock`; defines absence span for delta compilation |
| **FactionGraphDeltaExtractor** | Reads **WorldState** snapshots at tick anchors; emits **FactionGraphDelta** (edge weight changes, node promotions/demotions, tribe split/merge markers) |
| **TribeActivityScheduler** | Applies off-screen event templates when absence exceeds thresholds (e.g. border tension → skirmish hook); outputs scheduled **OffScreenEvent** proposals consumed by **3.1** tick loop when catch-up runs |
| **SinceYouLeftCompiler** | Merges **FactionGraphDelta** + selected **WorldEventLog** entries into ranked **NarrativeDelta** items with provenance |
| **NarrativeSurfacingPolicy** | Routes deltas: `auto_brief` (low stakes), `dm_queue` (canon-touching), `suppress` (spoiler / unrevealed threads) |
| **AbsenceCatchupBridge** | Signals **3.1** **TickScheduler** how many ticks to simulate for absence; receives **CommittedTickRecord** stream for compiler input — does not mutate **WorldState** directly |
| **ThreadRevealGate** | Ensures faction/tribe reveals respect **LoreHookRegistry** `sim-active` vs `hooked-only` visibility |
| **ToneProfileNarrativeWeights** | Maps consequence severity bands to narrative tone (grim vs whimsical) per active **ToneProfileBundle** |

**Flow (player returns after absence):**

1. **OffScreenActivityWindow** computes absence span (sim ticks + wall-clock markers)
2. **AbsenceCatchupBridge** requests capped catch-up ticks from **3.1** (or reads already-committed log if catch-up deferred)
3. **FactionGraphDeltaExtractor** diffs graph state: `tick_at_departure` → `tick_at_return`
4. **SinceYouLeftCompiler** ranks **NarrativeDelta** items; **ToneProfileNarrativeWeights** styles copy bands
5. **NarrativeSurfacingPolicy** splits auto-brief vs DM queue
6. Publish `narrative.since_you_left_compiled` on `narrative.*` bus — Presentation subscribes read-only

**Inputs / outputs:**

- *Into 3.2:* **CommittedTickRecord** + **WorldEventLog** from **3.1**; **SimGraphSeed** / **LoreHookRegistry** faction-tribe hooks from **2.2**; **ToneProfileBundle** from **2.3**
- *Out of 3.2:* **NarrativeDelta** bundles for session open; **OffScreenEvent** proposals for tick catch-up; DM queue entries for canon-touching shifts

## Interfaces

**Imports from Phase 3.1:**

| 3.1 export | How 3.2 consumes it |
|------------|---------------------|
| **CommittedTickRecord** | Anchor endpoints for graph diff |
| **FactionGraphSubsystem** outputs (via log/state) | Raw edge changes — 3.2 packages only |
| **TickScheduler** catch-up caps | **AbsenceCatchupBridge** respects caps; overflow → deferred batch narrative |
| **DMPauseGate** | Compiler pauses auto-surfacing while DM holds authority |

**Imports from Phase 2:**

| Phase 2 export | How 3.2 consumes it |
|----------------|---------------------|
| **LoreHookRegistry** faction/tribe hooks (**2.2**) | Named entities and thread ids for **NarrativeDelta** attribution |
| **ToneProfileBundle** (**2.3**) | **ToneProfileNarrativeWeights** for surfaced copy |

**Exports to Phase 3 siblings:**

| Export | Consumer |
|--------|----------|
| **NarrativeDelta** schema | Phase 4 perspective layers (read-only subscribe) |
| **OffScreenEvent** proposals | **3.1** tick loop during catch-up |
| **DM queue delta entries** | **3.3** overwrite policy (canon conflict resolution) |

**Adjacent slices:**

- **3.1** owns tick commit truth; **3.2** never writes **WorldState** except via proposals routed through **3.1** catch-up.
- **3.3** decides whether a surfaced delta may be retroactively vetoed or triggers re-generation.

## Edge cases

- **Zero absence:** Player never left region — compiler emits empty brief; not an error.
- **Catch-up deferred:** **TickScheduler** hit cap — compiler uses last committed tick + `sim.catchup_deferred` marker; brief notes "world still catching up" without fabricating future state.
- **Conflicting thread reveals:** Two **NarrativeDelta** items imply contradictory canon — **ThreadRevealGate** routes both to DM queue; no auto-brief.
- **Empty faction graph:** Valid degenerate world — compiler surfaces weather/NPC-only absence notes if log entries exist; otherwise empty brief.
- **ToneProfile missing at runtime:** Mirror **3.1** line 106 — distinguish (a) **unknown `profile_id` post-selection** — **ToneFallbackResolver** applies Medium Fantasy narrative weights + `narrative.tone_fallback_applied`; (b) **missing bundle at session boundary** (never selected at session 0) — block narrative auto-brief per **2.3** SeedBundle attachment + **2.1** SeedParser block; bundle corruption/hash mismatch — block surfacing + DM reconcile (not silent fallback).
- **Spoiler suppression:** Faction the player has not discovered — **NarrativeSurfacingPolicy** `suppress` with `dm_queue` hint only.

## Open questions

- **Brief length budget:** Max auto-brief items per return — operator attestation via factory catalog; not resolved on conceptual track.
- **Tribe vs faction granularity:** Single **FactionGraphDelta** schema with `entity_kind` discriminator vs parallel extractors — lean toward single schema with kind tag for modularity.
- **Multiplayer absence:** Per-player presence windows — deferred to Phase 5+; v1 assumes single-party presence anchor.

## Pseudo-code readiness

A reader can trace absence window → catch-up bridge → tick anchor diff → narrative compiler → surfacing policy → bus publish without guessing ownership. **3.2** does not own tick ordering or WorldState commit. No API signatures on conceptual track; execution deepen mints typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

Pattern alignment (no new pre-deepen research this run):

- Idle/offline progression narrative packaging — common live-service "while you were away" pattern; separated from sim authority per Phase 1.1 layers
- Event-sourced delta narration — **WorldEventLog** + **CommittedTickRecord** anchors from **3.1**
- Tone-weighted player-facing copy — extends **2.3** **ToneProfileNarrativeWeights**

## Responsibilities

- [x] Name off-screen window, delta extractor, and SinceYouLeft compiler
- [x] Document surfacing policy and DM queue routing
- [x] Integration spine with **3.1** tick anchors and **2.2** lore hooks
- [x] Handoff closure with **3.3** DM overwrite policy — [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]] minted 2026-06-26

## Tasks

- [x] Mint 3.2 secondary with off-screen actor registry and absence flow
- [ ] Optional tertiaries: delta schema detail, tribe scheduler templates, surfacing policy tiers — deferred breadth-first
- [x] **3.1→3.2** handoff — satisfied by [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]] Tasks handoff `[x]` 2026-06-26
- [x] **3.2→3.3** handoff — dm_queue + NarrativeDeltaVetoPolicy spine documented in [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-2-Off-Screen-Faction-Tribe-Activity"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
