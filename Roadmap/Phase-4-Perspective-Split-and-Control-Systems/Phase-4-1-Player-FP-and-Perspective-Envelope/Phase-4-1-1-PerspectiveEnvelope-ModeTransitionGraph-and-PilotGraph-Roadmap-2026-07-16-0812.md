---
title: Phase 4.1.1 — PerspectiveEnvelope / ModeTransitionGraph / PilotGraph
roadmap-level: tertiary
phase-number: 4
subphase-index: 4.1.1
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: green
body_compact_status: complete
body_chars_cap: 1200
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-4
- perspective-envelope
- mode-transition
- pilot-graph
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
- '[[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]'
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roll-up-2026-07-16]]'
rollup-detail: '[[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roll-up-2026-07-16]]'
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.1.1 — PerspectiveEnvelope / ModeTransitionGraph / PilotGraph

**PerspectiveEnvelope** = legal modes + intent vs observe. **ModeTransitionGraph** = edges + guards. **PilotGraph** = self → dominate → absent-proxy. No Godot / factory/L5.

## Scope

**In:** Modes `player_fp`/`dm_world`/`dm_map`/`dm_sensorium_attach`; intent vs observe; edges+guards; PilotGraph; `presentation.mode_changed`.

**Out:** 4.1.2 scene/interpolator/FPRig; 4.1.3 FOV; 4.2/4.3 matrix/glue; Camera3D; passenger_fp (P5); factory/L5.

## Behavior

Intent → guards → deactivate → interpolator (4.1.2) → activate → envelope → PilotGraph → emit. Detail → [[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roll-up-2026-07-16]].

## Interfaces

**In:** PresentationShell/InputIntent (1.1); DMPauseGate (3.1); NarrativeDeltaVetoPolicy (3.3). **Out:** Envelope+graph → 4.2; PilotGraph → 4.3; mode IDs → 4.1.2/4.1.3.

## Handoff

**80%** nouns named. Slice green; **4.1.2**/**4.1.3**/**4.2.1**/**4.2.2**/**4.2.3** cleared ≤1200; live next **5.1.3** (`1353>1200`). Cap ≤1200. (5.1.2 cleared 1197≤1200.)
