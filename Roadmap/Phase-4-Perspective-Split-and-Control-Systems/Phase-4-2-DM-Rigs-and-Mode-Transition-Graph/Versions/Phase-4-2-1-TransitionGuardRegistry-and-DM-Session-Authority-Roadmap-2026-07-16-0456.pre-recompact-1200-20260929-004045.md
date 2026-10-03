---
title: Phase 4.2.1 — TransitionGuardRegistry and DM Session Authority
roadmap-level: tertiary
phase-number: 4
subphase-index: 4.2.1
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: green
factory_feed_gate_reason: ''
body_compact_status: complete
body_chars_cap: 1200
body_recompact_1200_at: 2026-07-16
body_recompact_1200_queue: followup-deepen-gmm-4-2-1-20260716T222811Z
body_recompact_1200_status: complete
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-4
- dm-rigs
- transition-guards
- dm-session-authority
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roll-up-2026-07-16]]'
rollup-detail: '[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roll-up-2026-07-16]]'
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase42-feedstock-20260716T085600Z
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.2.1 — TransitionGuardRegistry and DM Session Authority

Guard stack: **DM session authority**, freeze/veto, **SensoriumAttach** safety. No Godot / factory/L5.

## Scope

**In:** `dm_session_authority`; `not_dmpause_frozen`; `narrative_veto_clear`; `overwrite_patch_compatible`; `attach_target_valid`; `not_dominate_active`; first-failing-guard; `presentation.transition_blocked`.

**Out:** Map annotation (`4.2.2`); DM rail chrome (`4.2.3`); Camera3D; serializers; factory/L5; exec pins.

## Behavior

<mark data-highlight-source="agent" style="background: #FFD9A3A6;">Intent → **TransitionGuardRegistry** → allow (`presentation.mode_changed`) or block (first `guard_id`). FP→DM: authority+freeze; inter-DM OK under freeze (RO); DM→FP: veto/overwrite clear. Detail → [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roll-up-2026-07-16]].</mark>

## Interfaces

**In:** ModeTransitionGraph (4.1); DMPauseGate (3.1); NarrativeDeltaVetoPolicy + OverwritePatchLayer (3.3). **Out:** `guard_id` → 4.2/4.3; blocked-reason → DMRailUXContract.

## Handoff

**80%** guard catalog. Cap ≤1200. Siblings 4.1.1=1062 / 4.1.2=1177 / 4.1.3=1154. Next DFS **4.2.3** (`body_over_cap`; 4.2.2 cleared 1032).
