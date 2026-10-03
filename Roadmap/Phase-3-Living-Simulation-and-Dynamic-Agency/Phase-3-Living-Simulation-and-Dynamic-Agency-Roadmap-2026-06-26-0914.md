---
title: Phase 3 — Living Simulation and Dynamic Agency
roadmap-level: primary
phase-number: 3
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 84
conceptual_map_slice: roll_up_gates_added
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase
para-type: Project
roadmap_track: conceptual
links:
- '[[genesis-mythos-master-Roadmap-2026-06-26-0914]]'
rollup-detail: '[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roll-up-2026-06-29]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 3 — Living Simulation and Dynamic Agency

Persistent, balanced simulation with DM authority respected. Tick weather, NPC agendas, off-screen faction activity, DM overwrites vs re-generation.

- [x] 3.1 Tick simulation → [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600|3.1]]
- [x] 3.2 Off-screen factions → [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615|3.2]]
- [x] 3.3 DM overwrite policy → [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630|3.3]]

## Scope

SimClock + SimTickPipeline + WorldEventLog (3.1); OffScreenActivityWindow + SinceYouLeftCompiler (3.2); DMOverwriteClass + OverwritePatchLayer + ReGenerationIntentQueue (3.3). Out: Godot wiring, factory/L5, execution serializers — execution-deferred. Secondaries complete; 3.1.1–3.1.4 minted; tertiary body compact pending 3.1.2–3.1.3 (3.1.1 compact 2026-06-30).

## Behavior

Tick spine (3.1) before delta surfacing (3.2); DM policy (3.3) integrates DMPauseGate + dm_queue veto. Advance-phase 3→4 at handoff ~84% (2026-06-26).

## Interfaces

Exports: CommittedTickRecord (3.1); NarrativeDelta (3.2); ReGenerationIntent (3.3). Imports: SimGraphSeed (2.1), LoreHookRegistry (2.2), ToneProfileBundle (2.3). See [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600|3.1]], [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615|3.2]], [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630|3.3]].

## Edge cases

Partial 3.x does not block Phase 4 sketch. DMPauseGate queues speculative deltas — 3.3 reconciler on resume. Off-screen overflow defers per TickScheduler caps.

## Roll-up & handoff

Handoff + roll-up gates → [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roll-up-2026-06-29]] (84%).

## Subphases

Tree index + dataview → [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roll-up-2026-06-29#Subphases & notes|rollup § Subphases]].
