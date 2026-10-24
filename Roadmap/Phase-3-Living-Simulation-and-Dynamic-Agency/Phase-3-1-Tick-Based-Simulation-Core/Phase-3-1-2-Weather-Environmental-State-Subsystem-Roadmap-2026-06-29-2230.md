---
title: Phase 3.1.2 — Weather and Environmental State Subsystem
roadmap-level: tertiary
phase-number: 3
subphase-index: 3.1.2
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
- weather
- environmental-state
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-3-1-2-Weather-Environmental-State-Subsystem-Roll-up-2026-06-29]]'
links:
- '[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roadmap-2026-06-29-2205]]'
- '[[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 3.1.2 — Weather and Environmental State Subsystem

**WeatherSubsystem** — first **SimTickPipeline** slot after **SimClock**; region weather + mood deltas → **ConsequenceResolver** (low prec.). Parent [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]; nouns + bus only.

## Scope

**In:** **RegionWeatherRegistry**, **EnvironmentalCycleProfile**, **MoodModifierBinding**, **WeatherTickDelta**, **RegionScopeResolver**, **WeatherNoisePolicy**. **Out:** NPC (**3.1.3**); faction (**3.1.4**); off-screen (**3.2**); VFX; factory/L5.

## Behavior

Per-tick: **WorldState** snapshot + **SimClock** → **RegionScopeResolver** → cycle + mood drift → **WeatherNoisePolicy** clamp → **WeatherTickDelta** (canon > faction > weather).

## Interfaces

Imports: **3.1.1** clock; **2.1** seed; **2.3** tone; slot `weather`; `sim.*` subscribe until commit. Exports: **RegionWeatherRegistry**, **WeatherTickDelta** → **ConsequenceResolver**, **3.2**.

## Roll-up

Actors, keys, sketch, edge cases → [[Phase-3-1-2-Weather-Environmental-State-Subsystem-Roll-up-2026-06-29]].

## Handoff

**80%** — NL complete; detail in rollup. Exec-deferred: Godot weather, typed structs, HR gates.
