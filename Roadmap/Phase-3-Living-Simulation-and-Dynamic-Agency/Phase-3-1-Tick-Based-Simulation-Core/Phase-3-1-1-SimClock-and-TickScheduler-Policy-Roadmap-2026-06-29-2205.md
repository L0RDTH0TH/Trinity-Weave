---
title: Phase 3.1.1 — SimClock and TickScheduler Policy
roadmap-level: tertiary
phase-number: 3
subphase-index: 3.1.1
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 79
factory_feedstock_slice: phase_3_tertiary_tree
body_compact_status: complete
factory_feed_gate_status: green
branch_open: false
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-3
- simulation
- sim-clock
- tick-scheduler
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roll-up-2026-06-29]]'
links:
- '[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
- '[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 3.1.1 — SimClock and TickScheduler Policy

**SimClock** step-mode registry + **TickScheduler** frame-budget policy for authoritative tick loop. Parent [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]; nouns + bus contracts only.

## Scope

**In:** **SimClockPolicyRegistry**, **TickBudgetManifest**, **CatchupDeferralPolicy**, **SessionTimeSyncBinding**, **DMPauseGate** clock integration. **Out:** **SimTickPipeline** ordering; weather/NPC/faction (**3.1.2–3.1.4**); off-screen (**3.2**); DM overwrite (**3.3**); factory/L5.

## Behavior

**DMPauseGate** pause-first → **TickBudgetManifest** caps ticks → **SimClock** advance → **SimTickPipeline** handoff; backlog overflow → `sim.catchup_deferred`.

## Interfaces

Imports: parent 3.1 **DMPauseGate**, **WorldStateCommitter**; Phase 1 `sim.*`; Phase 1.3 **ProvenanceEnvelope**. Exports: policy registry + budget manifest → **3.2** **AbsenceCatchupBridge**.

## Roll-up

Actors, step modes, scheduling sketch, edge cases → [[Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roll-up-2026-06-29]].

## Handoff

**79%** — NL complete; detail in rollup. Execution-deferred: Godot frame hooks, typed scheduler interfaces, HR gates.
