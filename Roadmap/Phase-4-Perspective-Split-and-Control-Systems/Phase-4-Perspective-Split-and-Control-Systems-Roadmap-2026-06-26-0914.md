---
title: Phase 4 — Perspective Split and Control Systems
roadmap-level: primary
phase-number: 4
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 85
conceptual_map_slice: roll_up_gates_added
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase
para-type: Project
roadmap_track: conceptual
links:
- '[[genesis-mythos-master-Roadmap-2026-06-26-0914]]'
rollup-detail: '[[Phase-4-Perspective-Split-and-Control-Systems-Roll-up-2026-07-15]]'
body_compact_at: 2026-07-15
body_compact_queue: followup-deepen-phase4-20260715T221000Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4 — Perspective Split and Control Systems

Role-tailored views with seamless transitions. Player FP; perspective/agency envelopes; DM mode graph (WorldCam ↔ MapCam ↔ SensoriumAttach); pilot dominate/absent-proxy; unified scene graph + camera interpolator.

- [x] 4.1 Player FP + perspective — [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705|4.1]]
- [x] 4.2 DM rigs + mode graph — [[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730|4.2]]
- [x] 4.3 Agency + pilot glue — [[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945|4.3]]

## Scope

In: 4.1 PerspectiveEnvelope/UnifiedSceneGraph/PilotGraph; 4.2 DMRigPolicyMatrix/TransitionGuardRegistry/ModeTransitionGraph; 4.3 AgencyEnvelope/PilotMachineryGlue/AgencyPersistenceLedger. Consumes Phase 1.1 presentation decoupling + Phase 3 DMPauseGate/NarrativeDeltaVetoPolicy. Out: Godot Camera3D, passenger_fp (P5), factory/L5, typed rigs, REGISTRY-CI/HR — execution-deferred/advisory.

## Behavior

Actors span 4.1–4.3 (PerspectiveEnvelope → AgencyPersistenceLedger). Order: 4.1 → 4.2 → 4.3. Advance 4→5 ~85% (2026-06-26); tertiary 0% OK conceptual_v1.

## Interfaces

Exports: envelope modes + InputIntent; mode_changed + DM rail; dominate/absent-proxy + ledger schema. Imports: Phase 3 pause/veto/overwrite; Phase 1 PresentationShell/InputIntent/SeamRegistry. See 4.1–4.3 links above.

## Edge cases

Partial 4.x ≠ block Phase 5 sketch. Dominate during DM rail needs PilotHandoffCoordinator blend. SensoriumAttach read-only. OverwritePatchLayer may veto via TransitionGuardRegistry. Factory/L5 out of scope.

## Roll-up & handoff

Handoff table, gates, open Qs, consistency, dataview → [[Phase-4-Perspective-Split-and-Control-Systems-Roll-up-2026-07-15]] (85%).

## Subphases

Tree → [[Phase-4-Perspective-Split-and-Control-Systems-Roll-up-2026-07-15#Subphases & notes|rollup]].
