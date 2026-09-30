---
title: Phase 4.2.3 — DM Rail Chrome and DMRailUXContract
roadmap-level: tertiary
phase-number: 4
subphase-index: 4.2.3
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: green
factory_feed_gate_reason: ''
body_compact_status: complete
body_chars_cap: 1200
body_over_cap: false
body_chars_before: 1267
body_chars_after: 1060
body_recompact_1200_at: 2026-07-16
body_recompact_1200_queue: followup-deepen-gmm-4-2-3-20260716T232339Z
body_recompact_1200_status: complete
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-4
- dm-rigs
- dm-rail-ux
- rail-chrome
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
- '[[Phase-4-2-2-Map-Annotation-Envelope-Roadmap-2026-07-16-0628]]'
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roll-up-2026-07-16]]'
rollup-detail: '[[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roll-up-2026-07-16]]'
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.2.3 — DM Rail Chrome and DMRailUXContract

**DMRailUXContract** — rail chrome: FP→WorldCam→MapCam→SensoriumAttach + blocked messaging on TransitionGuardRegistry fail. No Godot / factory/L5.

## Scope

**In:** rail order; `blocked_reason`; mode-switch affordances; PresentationShell chrome (4.1); bind guard fails (4.2.1).

**Out:** MapAnnotationEnvelope (`4.2.2`); guard predicates (`4.2.1`); Camera3D; serializers; factory/L5; exec pins; 4.3 persistence / AgencyEnvelope.

## Behavior

Pick rail → PresentationShell mode-switch → TransitionGuardRegistry → fail: show blocked reason (no silent noop); pass: matrix row. Detail → [[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roll-up-2026-07-16]].

## Interfaces

**In:** ModeTransitionGraph + matrix (4.1/4.2); TransitionGuardRegistry (4.2.1); PresentationShell (4.1). **Out:** rail chrome + blocked messaging → **4.3**.

## Handoff

**80%** rail order + blocked messaging. Cap ≤1200. Siblings 4.1.1=1061 / 4.1.2=1176 / 4.1.3=1153 / 4.2.1=1138 / 4.2.2=1031. Next DFS **4.3.1** (`body_over_cap`).
