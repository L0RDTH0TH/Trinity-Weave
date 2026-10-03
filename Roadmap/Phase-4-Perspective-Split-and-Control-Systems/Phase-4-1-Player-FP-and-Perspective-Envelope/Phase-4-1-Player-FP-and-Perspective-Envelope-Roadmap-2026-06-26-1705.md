---
title: Phase 4.1 — Player FP and Perspective Envelope
roadmap-level: secondary
phase-number: 4
subphase-index: '4.1'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
feedstock_qualified_at: 2026-07-16
feedstock_qualify_queue: followup-deepen-phase627-tertiary-20260716T064200Z
breadth_mint_complete: true
body_compact_status: complete
factory_feed_gate_status: green
secondary_feedstock_qualified: true
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-4
- perspective
- player-fp
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roll-up-2026-07-15]]'
body_compact_at: 2026-07-15
body_compact_queue: followup-deepen-phase41-20260715T222400Z
links:
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]'
- '[[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]'
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.1 — Player FP and Perspective Envelope

Player **FP baseline** + **PerspectiveEnvelope** (legal modes, intent vs read-only). Nouns: **UnifiedSceneGraph**, **CameraInterpolatorRegistry**, DM rigs (**WorldCam**/**MapCam**/**SensoriumAttach**), **PilotGraph** (dominate/absent-proxy).

## Scope

**In:** PerspectiveEnvelope; UnifiedSceneGraph; CameraInterpolatorRegistry; WorldCam/MapCam/SensoriumAttach; PilotGraph; PlayerFPRig; ModeTransitionGraph; InputIntent (1.1); WorldState / `sim.tick_committed` (3.1) RO. **Out:** 4.2 matrix; 4.3 glue; Camera3D; passenger_fp (P5); factory/L5.

## Behavior

Envelope modes → ModeTransitionGraph guards → interpolator blend → PilotGraph agency reconcile → `presentation.mode_changed`. Detail → [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roll-up-2026-07-15]].

## Interfaces

Imports: 1.1 PresentationShell/InputIntent; 3.1 DMPauseGate/`sim.tick_committed`; 3.3 NarrativeDeltaVetoPolicy. Exports: ModeTransitionGraph + rig IDs → **4.2**; PilotGraph → **4.3**.

## Roll-up

Actors, ordering, edge cases, open Qs, tasks, dataview → [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roll-up-2026-07-15]].

## Handoff

**80** — NL complete; **4.1.1–4.1.3** minted; **4.1–4.3** branches closed; `phase_4_tertiary_tree` complete; next **5.1.1**.
