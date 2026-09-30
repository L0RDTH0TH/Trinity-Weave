---
title: Phase 3.2 — Off-Screen Faction / Tribe Activity
roadmap-level: secondary
phase-number: 3
subphase-index: '3.2'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 79
factory_feedstock_slice: phase_3_secondary_tree
body_compact_status: complete
factory_feed_gate_status: green
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-3
- off-screen
- faction
- tribe
- narrative-delta
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roll-up-2026-07-15]]'
links:
- '[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
- '[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 3.2 — Off-Screen Faction / Tribe Activity

Package off-screen faction/tribe evolution into **"since you left…"** narrative deltas. Owns delta surfacing + absence windows; **3.1** keeps graph math / tick commit. Nouns + bus only.

## Scope

**In:** **OffScreenActivityWindow**, **FactionGraphDeltaExtractor**, **TribeActivityScheduler**, **SinceYouLeftCompiler**, **NarrativeSurfacingPolicy**, **AbsenceCatchupBridge**, **ThreadRevealGate**, **ToneProfileNarrativeWeights**. **Out:** **3.1** FactionGraph math; **3.3** DM overwrite; UI; factory/L5.

## Behavior

Return after absence: window → catch-up bridge (capped) → graph diff → compile + tone → surfacing tiers → `narrative.since_you_left_compiled`.

## Interfaces

Imports: **3.1** **CommittedTickRecord** / catch-up caps / **DMPauseGate**; **2.2** lore hooks; **2.3** tone. Exports: **NarrativeDelta**, **OffScreenEvent** → **3.1**; DM queue → **3.3**.

## Roll-up

Actors, flow sketch, edge cases → [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roll-up-2026-07-15]].

## Handoff

**79%** — NL complete; detail in rollup. Exec-deferred: typed serializers, HR gates.
