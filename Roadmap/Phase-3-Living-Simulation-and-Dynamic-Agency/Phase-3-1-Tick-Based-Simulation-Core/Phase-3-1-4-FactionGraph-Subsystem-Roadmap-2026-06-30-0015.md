---
title: Phase 3.1.4 — Faction Graph Subsystem
roadmap-level: tertiary
phase-number: 3
subphase-index: 3.1.4
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feedstock_slice: phase_3_tertiary_tree
body_compact_status: complete
factory_feed_gate_status: green
branch_open: false
created: 2026-06-30
tags:
- roadmap
- genesis-mythos-master
- phase-3
- simulation
- faction-graph
- reputation
- tension
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-3-1-4-FactionGraph-Subsystem-Roll-up-2026-06-30]]'
links:
- '[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]'
- '[[Phase-3-1-2-Weather-Environmental-State-Subsystem-Roadmap-2026-06-29-2230]]'
- '[[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 3.1.4 — Faction Graph Subsystem

**FactionGraphSubsystem** — third **SimTickPipeline** slot after agendas; edges + thresholds → **FactionGraphTickDelta**. Parent [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]; math + bus only — packaging in **3.2**.

## Scope

**In:** **FactionGraphRegistry**, **EdgeWeightPolicy**, **ThresholdRuleIndex**, **OffScreenEventScheduler**, **FactionGraphTickDelta**, **GraphConflictPolicy**, **TribeMembershipIndex**. **Out:** narrative (**3.2**); DM (**3.3**); agendas (**3.1.3**); factory/L5; Godot graphs.

## Behavior

Per-tick: snapshot + clock + NPC side-effects (RO) → scope → decay → thresholds → off-screen → conflict pick-one → **FactionGraphTickDelta** (canon > faction > NPC > weather).

## Interfaces

Imports: **3.1.3** side-effects; **3.1.2** mood; **3.1.1** clock; **2.1** seed; **2.2** hooks; slot `faction_graph`. Exports: registry + delta → **ConsequenceResolver**, **3.2**.

## Roll-up

Actors, edge kinds, sketch, edge cases → [[Phase-3-1-4-FactionGraph-Subsystem-Roll-up-2026-06-30]].

## Handoff

**80%** — NL complete; detail in rollup. Exec-deferred: Godot graph nodes, typed structs, HR gates.
