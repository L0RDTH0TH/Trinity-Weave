---
title: Phase 4.2.3 — DM Rail Chrome and DMRailUXContract (Roll-up)
roadmap-level: rollup
phase-number: 4
subphase-index: 4.2.3
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags:
- roadmap
- rollup
- genesis-mythos-master
- phase-4
- dm-rail-ux
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]'
- '[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 4.2.3 roll-up — DM Rail Chrome / DMRailUXContract

Canonical compact tertiary: [[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]] (body **1267→1060≤1200**, `followup-deepen-gmm-4-2-3-20260716T232339Z`). Detail preserved off the ≤1400 feedstock body (`followup-deepen-phase423-tertiary-20260716T104451Z`).

## Purpose

Name the **operator-facing rail chrome** that sequences DM observation modes and surfaces **why** a TransitionGuardRegistry failure blocked a switch — without sim mutation and without silent noops.

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **DMRailUXContract** | Hotkey / UI rail ordering + blocked-state messaging |
| `rail_order` | Conceptual sequence: FP → WorldCam → MapCam → SensoriumAttach (+ return paths) |
| `blocked_reason` | Human-readable surface when first failing `guard_id` rejects an edge |
| `affordance_class` | Mode-switch chrome only (never locomotion/combat intents) |
| `chrome_handshake` | PresentationShell shows active_rig_id + eligible next rails |

**Out:** Map annotation envelope (`4.2.2`); TransitionGuardRegistry predicate bodies (`4.2.1`); Camera3D / SubViewport; typed serializers; factory/L5; execution pins; 4.3 RailStatePersistence / AgencyEnvelope.

## Behavior detail

1. Operator activates a rail affordance (target `rig_id` / edge).
2. PresentationShell emits mode-switch intent (4.1 handshake).
3. TransitionGuardRegistry evaluates ordered `guard_stack` (4.2.1).
4. **Fail:** DMRailUXContract surfaces `blocked_reason` from first failing `guard_id` — chrome stays on current rig.
5. **Pass:** matrix row activates; chrome updates `active_rig_id` + eligible neighbors; emit `presentation.mode_changed` (conceptual).

## Edge cases

- **Silent noop forbidden:** Any guard failure must produce chrome messaging; never drop the intent without feedback.
- **Inter-DM during DMPauseGate:** World↔Map↔Sensorium affordances remain eligible per 4.2.1 inter-DM pause exemption; FP-return chrome stays blocked while freeze holds.
- **fp_to_sensorium affordance:** Must not appear as direct chrome shortcut — route via WorldCam (rejected edge in parent catalog).
- **Map annotation while on MapCam:** Annotation is separate intent class (`4.2.2`); rail chrome only switches rigs.

## Open questions

- **Blocked-reason copy localization:** Conceptual IDs only; factory/L5 owns operator-facing strings.
- **Rail cursor persistence:** Session-local chrome memory vs 4.3 ledger export — lean session-local until AgencyEnvelope owns it.

## Handoff criteria

- [x] Rail order nouns named
- [x] Blocked-state messaging bound to guard failures
- [x] Mode-switch-only affordance boundary explicit
- [x] 4.2 tertiary branch closed; next DFS pointed (`4.3.1` AgencyEnvelope)

**80%** handoff_readiness — implementer can wire rail chrome without guessing silent-fail behavior. Slice **4.2.3** green **1060≤1200**. Project harness remains **red** (`body_over_cap:1353>1200` on Phase-5-1-3; 5.1.2 cleared 1197≤1200; `phase_4_tertiary_tree_complete: true`). Phase-4-3-1 cleared **1158≤1200**.
