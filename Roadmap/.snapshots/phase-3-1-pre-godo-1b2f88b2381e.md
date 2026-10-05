---
title: Phase 3.1 — Tick-Based Simulation Core
roadmap-level: secondary
phase-number: 3
subphase-index: "3.1"
project-id: genesis-mythos-master
status: in-progress
priority: high
progress: 33
handoff_readiness: secondary_minted
created: 2026-06-26
tags: [roadmap, genesis-mythos-master, phase-3, simulation, tick-core]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]"
  - "[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]"
  - "[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]"
  - "[[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]"
  - "[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]"
  - "[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]"
  - "[[genesis-mythos-master-goal]]"
---

## Phase 3.1 — Tick-Based Simulation Core

Define the **authoritative tick loop** that advances world state independently of rendering: global sim clock, tick scheduling, subsystem ordering, commit boundaries to **WorldEventLog**, and **ToneProfile-weighted** consequence propagation. This slice is the simulation spine Phase 3 siblings (off-screen faction activity, DM overwrite policy) plug into — without Godot implementation paths on conceptual track.

## Scope

**In scope:** **SimClock** (fixed vs variable step policy, pause/resume, session-time sync); **TickScheduler** (frame budget vs sim catch-up); **SimTickPipeline** ordering registry (weather → NPC agendas → faction graphs → consequence resolver); **WorldState** mutation contract per tick (what commits vs what stays speculative); **WorldEventLog** append semantics (one event envelope per committed tick); **SimGraphSeed** consumption from Phase 2 **SimBootstrapStageExecutor**; **ToneProfileConsequenceWeights** applied at consequence resolution; **Presentation decoupling** invariant (sim never blocks on render); **DM pause authority** hook (sim halts tick advance when session policy demands).

**Out of scope:** Off-screen faction/tribe delta narratives and "since you left…" surfacing (secondary **3.2**); DM overwrite vs deliberate re-generation policy (secondary **3.3**); Godot `_process` / `_physics_process` wiring; execution-track typed tick interfaces and rollup HR gates (execution-deferred / advisory on conceptual track); perspective split and input routing (Phase 4).

## Behavior

**Actors:**

| Actor | Role |
|-------|------|
| **SimClock** | Owns sim time `t`, tick index `n`, and step mode (`fixed` default); exposes pause/resume; syncs wall-clock session markers without coupling to frame rate |
| **TickScheduler** | Decides how many ticks run per session frame given budget; supports catch-up caps to prevent spiral-of-death |
| **SimTickPipeline** | Ordered registry of tick subsystems; each subsystem receives read-only **WorldState** snapshot + emits **TickDelta** proposals |
| **WeatherSubsystem** | Advances region-scoped environmental variables (cycles, mood modifiers) — contract only; detail deferred to tertiaries |
| **NPCAgendaSubsystem** | Advances agenda slots and availability windows bound to **LoreHookRegistry** sim-active hooks |
| **FactionGraphSubsystem** | Updates reputation/tension edges from threshold rules and scheduled off-screen events (graph math only; narrative surfacing in **3.2**) |
| **ConsequenceResolver** | Merges **TickDelta** proposals; applies **ToneProfileConsequenceWeights**; rejects conflicting deltas with arbiter precedence |
| **WorldStateCommitter** | Atomically applies accepted deltas to **WorldState**; emits **CommittedTickRecord** |
| **WorldEventLogAppender** | Append-only log entry per committed tick with provenance envelope (Phase 1.3 pattern) |
| **DMPauseGate** | Session policy hook: when DM holds narrative authority, tick advance stops; queued deltas remain speculative |

**Ordering (per committed tick):**

1. **DMPauseGate** check — if paused, skip tick advance (speculative deltas may queue)
2. **SimClock** increment `n`, advance `t` by `Δt` per step mode
3. Subsystem pass (read-only snapshot): `weather → npc_agendas → faction_graph`
4. **ConsequenceResolver** merge + **ToneProfileConsequenceWeights**
5. **WorldStateCommitter** apply accepted deltas
6. **WorldEventLogAppender** record **CommittedTickRecord** with `tick_index`, `sim_time`, delta hash
7. Publish `sim.tick_committed` on `sim.*` bus (Phase 1.1) — Presentation may subscribe but must not block step 1–6

**Inputs / outputs:**

- *Into tick core:* **SimGraphSeed** + **CompiledWorldManifest** handoff from Phase 2.1; **RegistrySnapshot** + sim-active **LoreHookRegistry** from 2.2; **ToneProfileBundle** weights from 2.3
- *Out of tick core:* Mutating **WorldState**, append-only **WorldEventLog**, `sim.tick_committed` events for Phase 3.2+ and Presentation layer

## Interfaces

**Imports from Phase 2:**

| Phase 2 export | How 3.1 consumes it |
|----------------|----------------------|
| **SimGraphSeed** (2.1 sim_bootstrap) | Initial faction/NPC graph topology and seed agendas |
| **WorldEventLogInitializer** (2.1) | Log genesis record; 3.1 defines per-tick append contract |
| **LoreHookRegistry** sim-active hooks (2.2) | NPC agenda bindings and canon-triggered sim events |
| **ToneProfileBundle** + **ProfileWeightManifest** (2.3) | **ToneProfileConsequenceWeights** at ConsequenceResolver |

**Imports from Phase 1:**

| Phase 1 export | How 3.1 consumes it |
|----------------|----------------------|
| Simulation / WorldState layer boundary (1.1) | Sim owns mutation; Presentation read-only |
| `sim.*` bus category (1.1) | `sim.tick_committed`, `sim.pause`, `sim.resume` |
| **ProvenanceEnvelope** + **SeedSnapshot** replay (1.3) | CommittedTickRecord carries provenance; replay compares log hash |

**Exports to Phase 3 siblings:**

| Export | Consumer |
|--------|----------|
| **SimTickPipeline** ordering registry | 3.2 off-screen faction activity (delta surfacing) |
| **CommittedTickRecord** schema | 3.2 "since you left…" narrative compiler |
| **DMPauseGate** + speculative delta queue | 3.3 DM overwrite vs re-generation policy |
| **WorldEventLog** per-tick append contract | Phase 4 perspective layers (read-only subscribe) |

**Adjacent slices:**

- **3.2** owns off-screen narrative packaging; 3.1 owns graph math and commit boundaries only.
- **3.3** owns whether DM edits mutate WorldState directly vs trigger re-generation; 3.1 exposes pause + speculative queue seam.

## Edge cases

- **Catch-up spiral:** Player away long wall-clock period — **TickScheduler** caps catch-up ticks per frame; overflow spills to background batch with `sim.catchup_deferred` event; DM notified if world state lags session narrative.
- **Conflicting TickDeltas:** Two subsystems propose incompatible WorldState patches — **ConsequenceResolver** uses arbiter precedence (canon hooks > faction rules > weather noise); unresolved conflicts block commit and emit `sim.tick_blocked`.
- **Pause during commit:** **DMPauseGate** engaged mid-tick — finish current commit (atomicity) then halt; no partial WorldState visible to Presentation.
- **Empty SimGraphSeed:** Valid degenerate world — tick loop runs with zero NPC/faction nodes; weather-only ticks still commit; not an error.
- **ToneProfile missing at runtime:** Distinguish (a) **unknown `profile_id` post-selection** — **ToneFallbackResolver** applies Medium Fantasy weights + `sim.tone_fallback_applied` (mirrors **2.1** line 104 / **2.3** fallback contract); (b) **missing bundle at session boundary** (never selected at session 0) — block sim advance per **2.3** SeedBundle attachment + **2.1** SeedParser block (lines 103–104); bundle corruption/hash mismatch — block commit + DM reconcile (not silent fallback).
- **WorldEventLog disk/session loss:** Replay from **SeedSnapshot** + log rebuild contract (1.3); if hash mismatch, block sim advance until DM reconciles — not silent repair.

## Open questions

- **Fixed vs variable Δt default:** Fixed step favored for determinism; variable step for long off-screen gaps — operator attestation via factory catalog, not resolved on conceptual track.
- **Subsystem plugin registration:** Static registry in v1 vs **SeamRegistry** sim ports (1.3) — lean toward SeamRegistry for modularity; tertiary refine pass.
- **Minimum tick rate for first playable:** Coupled to Horizon M0 — deferred to Half A catalog / execution track.

## Pseudo-code readiness

A reader can trace SimGraphSeed ingest → clock init → per-frame scheduler → ordered subsystem pass → consequence merge with tone weights → atomic WorldState commit → event log append → bus publish without guessing ownership or ordering. No API signatures on conceptual track; execution deepen mints typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

Pattern alignment (no new pre-deepen research this run):

- Deterministic sim loop decoupled from render — Phase 1.1 Simulation/Presentation boundary
- Event-sourced world continuity — **WorldEventLog** + **CommittedTickRecord** extends Phase 2.1 initializer
- Tone-weighted consequences — **ToneProfileConsequenceWeights** extends 2.3 bundle contract

## Responsibilities

- [x] Name SimClock, TickScheduler, SimTickPipeline, and per-tick commit path
- [x] Document subsystem ordering and ConsequenceResolver + tone weights
- [x] Integration spine with Phase 2 sim bootstrap and event log init
- [x] DMPauseGate seam for 3.3 overwrite policy

## Tasks

- [x] Mint 3.1 secondary with tick core actor registry and ordering
- [ ] Optional tertiaries: SimClock detail, weather subsystem, NPC agendas, faction graph — deferred breadth-first (owner: 3.1 refine or depth-first branch)
- [x] Handoff closure with 3.2 off-screen activity — [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]] minted 2026-06-26

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
