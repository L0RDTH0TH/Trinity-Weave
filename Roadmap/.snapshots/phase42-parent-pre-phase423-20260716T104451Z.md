---
title: Phase 4.2 — DM Rigs and Mode Transition Graph
roadmap-level: secondary
phase-number: 4
subphase-index: "4.2"
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: breadth_complete
breadth_mint_complete: true
created: 2026-06-26
tags: [roadmap, genesis-mythos-master, phase-4, dm-rigs, mode-transition]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]"
  - "[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]"
  - "[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]"
  - "[[Phase-4-2-2-Map-Annotation-Envelope-Roadmap-2026-07-16-0628]]"
  - "[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]"
  - "[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]"
  - "[[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]"
  - "[[genesis-mythos-master-goal]]"
rollup-detail: "[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roll-up-2026-07-15]]"
factory_feed_gate_status: green
body_compact_status: complete
body_compact_at: 2026-07-15
body_compact_queue: followup-deepen-phase42-20260715T224500Z
---

## Phase 4.2 — DM Rigs and Mode Transition Graph

**DMRigPolicyMatrix** (WorldCam / MapCam / SensoriumAttach) + **TransitionGuardRegistry** refining **ModeTransitionGraph** (4.1). Session-authority DM rails, read-only projections, FP↔DM edge predicates. Conceptual — Camera3D/SubViewport exec-deferred.

## Scope

**In:** DMRigPolicyMatrix; WorldCam/MapCam/SensoriumAttach policies; ModeTransitionGraph edges; TransitionGuardRegistry; DMRailUXContract; PresentationShell handshake (4.1). **Out:** PlayerFPRig/PilotGraph (4.1); agency glue (4.3); Camera3D/SubViewport; typed serializers/HR; Phase 3 policy defs (consume only); passenger_fp (Phase 5); factory/L5.

## Behavior

Mode intent → guard stack → source deactivate → interpolator → matrix overlays → PerspectiveEnvelope routes → `presentation.mode_changed`. Detail → [[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roll-up-2026-07-15]].

## Interfaces

Imports: 4.1 graph/envelope/interpolators/PilotGraph; 3.1 DMPauseGate; 3.3 veto/OverwritePatchLayer; 3.2 map hints. Exports: matrix + guards + DMRailUXContract → **4.3**.

## Roll-up

Actors, matrix, edges, guards, ordering, edge cases, open Qs, tasks, dataview → [[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roll-up-2026-07-15]].

## Handoff

Breadth complete; tertiary tree: [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]], [[Phase-4-2-2-Map-Annotation-Envelope-Roadmap-2026-07-16-0628]]; next **4.2.3** DM rail chrome. Exec-deferred: Camera3D/SubViewport, typed serializers — advisory on conceptual track.
