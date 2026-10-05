---
title: Phase 4.1.2 — UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig
roadmap-level: tertiary
phase-number: 4
subphase-index: 4.1.2
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
- unified-scene-graph
- camera-interpolator
- player-fp-rig
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roll-up-2026-07-16]]'
rollup-detail: '[[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roll-up-2026-07-16]]'
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.1.2 — UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig

**UnifiedSceneGraph** = composition root; rigs as **PerspectiveAnchor**. **CameraInterpolatorRegistry** = named blends (`ease_default`, `snap_cut`, `dm_orbit`). **PlayerFPRig** = default FP agency anchor. No Godot / factory/L5.

## Scope

**In:** Single-authority graph; PerspectiveAnchor; interpolator IDs + missing→`snap_cut`/`presentation.interpolator_fallback`; PlayerFPRig + `fp_baseline_rig`; `active_rig_id` exclusivity; blend after 4.1.1 guards.

**Out:** Envelope/ModeTransitionGraph/PilotGraph (`4.1.1`); WorldCam/MapCam/SensoriumAttach FOV (`4.1.3`); 4.2/4.3; Camera3D/SubViewport; passenger_fp (P5); factory/L5.

## Behavior

Guards (4.1.1) → deactivate → registry blend/snap → activate → envelope → PilotGraph → `presentation.mode_changed`. Detail → [[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roll-up-2026-07-16]].

## Interfaces

**In:** Mode IDs/guards (4.1.1); PresentationShell (1.1); tick RO (3.1). **Out:** Scene/interpolator/FPRig → **4.1.3** / **4.2** / **6.2.1**.

## Handoff

**80%** nouns named. Slice green; 4.1.3 cleared ≤1200. Cap ≤1200.
