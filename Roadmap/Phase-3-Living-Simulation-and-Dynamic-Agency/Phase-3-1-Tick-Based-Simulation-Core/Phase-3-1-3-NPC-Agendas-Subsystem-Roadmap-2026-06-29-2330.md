---
title: Phase 3.1.3 — NPC Agendas Subsystem
roadmap-level: tertiary
phase-number: 3
subphase-index: 3.1.3
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
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
- npc-agendas
- lore-hooks
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-3-1-3-NPC-Agendas-Subsystem-Roll-up-2026-06-29]]'
links:
- '[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roadmap-2026-06-29-2205]]'
- '[[Phase-3-1-2-Weather-Environmental-State-Subsystem-Roadmap-2026-06-29-2230]]'
- '[[Phase-3-1-4-FactionGraph-Subsystem-Roadmap-2026-06-30-0015]]'
- '[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 3.1.3 — NPC Agendas Subsystem

**NPCAgendaSubsystem** — second **SimTickPipeline** slot after weather; agenda slots + lore hooks → **NPCAgendaTickDelta**. Parent [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]; nouns + bus only.

## Scope

**In:** **AgendaSlotRegistry**, **AvailabilityWindowPolicy**, **LoreHookBindingIndex**, **AgendaProgressState**, **NPCAgendaTickDelta**, **AgendaConflictPolicy**, **OffScreenAgendaDegradePolicy**. **Out:** faction (**3.1.4**); off-screen (**3.2**); DM (**3.3**); factory/L5; Godot AI.

## Behavior

Per-tick: snapshot + clock + mood → scope NPCs → availability + hook fire → pick-one conflict → degrade background → **NPCAgendaTickDelta** (canon > faction > NPC > weather).

## Interfaces

Imports: **3.1.1** clock; **3.1.2** mood; **2.2** hooks; **2.1** seed; slot `npc_agendas`. Exports: **AgendaSlotRegistry**, **NPCAgendaTickDelta** → **ConsequenceResolver**, **3.2**.

## Roll-up

Actors, lifecycle, sketch, edge cases → [[Phase-3-1-3-NPC-Agendas-Subsystem-Roll-up-2026-06-29]].

## Handoff

**80%** — NL complete; detail in rollup. Exec-deferred: Godot NPC nodes, typed structs, HR gates.
