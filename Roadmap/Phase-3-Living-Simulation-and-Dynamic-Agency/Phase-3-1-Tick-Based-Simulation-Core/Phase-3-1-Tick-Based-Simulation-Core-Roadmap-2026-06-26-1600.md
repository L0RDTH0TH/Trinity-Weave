---
title: Phase 3.1 — Tick-Based Simulation Core
roadmap-level: secondary
phase-number: 3
subphase-index: '3.1'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 78
factory_feedstock_slice: phase_3_secondary_tree
body_compact_status: complete
factory_feed_gate_status: green
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-3
- simulation
- tick-core
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-3-1-Tick-Based-Simulation-Core-Roll-up-2026-07-15]]'
links:
- '[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
- '[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[genesis-mythos-master-goal]]'
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 3.1 — Tick-Based Simulation Core

Authoritative **tick loop** independent of rendering: **SimClock**, **TickScheduler**, **SimTickPipeline**, **WorldEventLog** commit, **ToneProfileConsequenceWeights**. Spine for **3.2** / **3.3** — nouns + policy only.

## Scope

**In:** SimClock, TickScheduler, SimTickPipeline (weather → NPC → faction → consequence), WorldState commit, WorldEventLog, SimGraphSeed, DMPauseGate; tertiaries **3.1.1–3.1.4** minted. **Out:** **3.2** narrative; **3.3** overwrite policy; Godot process wiring; exec-deferred HR gates; Phase 4 perspective.

## Behavior

DMPauseGate → clock step → subsystem pass → ConsequenceResolver + tone weights → WorldStateCommitter → WorldEventLog → `sim.tick_committed` (non-blocking for Presentation).

## Interfaces

Imports: Phase 2 SimGraphSeed / LoreHookRegistry / ToneProfile; Phase 1 sim.* bus + provenance. Exports: pipeline order, CommittedTickRecord, pause + speculative queue → **3.2** / **3.3** / Phase 4.

## Roll-up

Actors, ordering, edge cases → [[Phase-3-1-Tick-Based-Simulation-Core-Roll-up-2026-07-15]].

## Handoff

**78%** — NL complete; detail in rollup. Exec-deferred: typed tick interfaces, HR gates.
