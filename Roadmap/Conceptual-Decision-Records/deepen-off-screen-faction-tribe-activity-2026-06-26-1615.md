---
title: "CDR — Off-Screen Faction / Tribe Activity (3.2)"
created: 2026-06-26
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-3]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T161500Z-phase3-2
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: reconciled
related_research: []
---

## Summary

Chose a **delta-surfacing layer** separate from **3.1** tick authority: **OffScreenActivityWindow**, **FactionGraphDeltaExtractor**, **SinceYouLeftCompiler**, and **NarrativeSurfacingPolicy** package faction/tribe graph changes into "since you left…" briefs without **3.2** writing **WorldState** directly. Catch-up tick requests flow through **AbsenceCatchupBridge** to **3.1** **TickScheduler** caps.

## PMG alignment

Supports the master goal's **living world** and **DM-respected agency** pillars: the world evolves while the player is absent, but surfaced narrative remains reviewable (auto-brief vs DM queue) and canon-touching shifts route to the table — consistent with collaborative canon from Phase 2.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Merge surfacing into **FactionGraphSubsystem** (3.1) | Fewer actors | Blurs tick math vs narrative packaging; blocks independent refine | **3.1** owns commit truth; **3.2** owns player-facing packaging |
| Re-simulate full absence on session load (no log diff) | Simpler mental model | Non-deterministic load times; breaks event-sourced continuity | **CommittedTickRecord** anchors + log diff align with **1.3** replay |
| Always auto-surface all deltas | Faster player feedback | Spoilers and canon conflicts reach player without DM gate | **NarrativeSurfacingPolicy** with `dm_queue` for canon-touching items |

## Validation evidence

- Pattern: idle/offline progression narrative packaging separated from sim authority — Phase 1.1 Simulation/Presentation boundary
- Parent **3.1** [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]] explicitly defers narrative surfacing to **3.2**
- Validator reconciliation: [[.technical/Validator/roadmap-auto-validation-20260626T161800Z-godo-followup-20260626T161500Z-phase3-2]]; second pass: [[.technical/Validator/roadmap-auto-validation-20260626T142002Z-godo-followup-20260626T161500Z-phase3-2-second-pass]]
- **2.2** **LoreHookRegistry** faction/tribe hooks provide named entity attribution for deltas

## Links

- Workflow log: 2026-06-26 16:15 deepen Phase-3-2-Off-Screen-Faction-Tribe-Activity
- Parent phase: [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]
- Prior slice: [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]
