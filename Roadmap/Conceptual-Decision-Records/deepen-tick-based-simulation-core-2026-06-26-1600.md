---
title: "CDR — Tick-Based Simulation Core (3.1)"
created: 2026-06-26
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-3]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T134500Z-phase3-1
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: reconciled
related_research: []
---

# Decision record — Tick-Based Simulation Core (3.1)

## Summary

Chose a **single authoritative tick pipeline** (SimClock → ordered subsystems → ConsequenceResolver with ToneProfile weights → atomic WorldState commit → WorldEventLog append) as the Phase 3.1 secondary, decoupled from Presentation and with **DMPauseGate** for DM authority. Off-screen narrative surfacing and overwrite policy remain in 3.2/3.3.

## PMG alignment

Supports PMG goals for a **living world** that continues when the table looks away, **DM authority** over narrative pauses, and **ToneProfile-driven** consequence feel — without binding to Godot implementation on conceptual track.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Event-driven only (no fixed tick) | Fewer wasted updates when idle | Harder determinism and replay; awkward catch-up | Tick scheduler + cap pattern preserves determinism and bounded catch-up |
| Merge weather/NPC/faction into one monolithic tick fn | Simpler v0 sketch | Violates Phase 1 modularity seams; blocks 3.2 plugin narrative | Subsystem registry + ConsequenceResolver keeps seams open |
| Defer WorldEventLog to execution track | Smaller 3.1 note | Breaks continuity spine from Phase 2.1 initializer | Log append per committed tick is core contract for "living" world |

## Validation evidence

- Phase 1.1 Simulation/Presentation decoupling — [[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]
- Phase 2.1 WorldEventLogInitializer + SimGraphSeed — [[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]
- Phase 2.3 ToneProfile weights — [[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]
- Pattern: event-sourced sim loops in persistent world games (no external URL this run)
- Validator (first pass): [[.technical/Validator/roadmap-auto-validation-20260626T160000Z-godo-followup-20260626T134500Z-phase3-1]] — `primary_code: missing_task_decomposition`; IRA reconciled progress metadata + tone edge-case + traceability (2026-06-26)

## Links

- Parent: [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]
- Workflow anchor: 2026-06-26 16:00 deepen Phase-3-1-Tick-Based-Simulation-Core
- Queue: `godo-followup-20260626T134500Z-phase3-1`
