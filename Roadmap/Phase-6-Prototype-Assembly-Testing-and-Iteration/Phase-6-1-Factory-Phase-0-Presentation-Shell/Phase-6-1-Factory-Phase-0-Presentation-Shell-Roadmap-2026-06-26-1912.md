---
title: Phase 6.1 — Factory Phase 0 Presentation Shell
roadmap-level: secondary
phase-number: 6
subphase-index: '6.1'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
branch_open: false
depth_backfill: true
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-6
- factory
- presentation-shell
- half-a
para-type: Project
roadmap_track: conceptual
breadth_mint_complete: true
secondary_feedstock_qualified: true
factory_track: true
horizon_demo_track: false
links:
- '[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
handoff_readiness: 80
product_factory_run_id: f35ff65cfb4f
rollup-detail: '[[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roll-up-2026-07-15]]'
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase61-20260716T202501Z
factory_feed_gate_status: green
body_compact_status: complete
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.1 — Factory Phase 0 Presentation Shell

**Factory catalog row** (Half A): presentation shell launch → PlayRegion → HUD. Factory spine only — not 6.2 demo loop.

## Scope

**In:** PresentationShellManifest (`ui_presentation_shell`); LaunchFlowController; PlayRegionHost; HUDLayerStack; KinestheticHonestyChecklist; DevLeakageGuard; 1.1/4.1 read-only hooks. **Out:** 6.2 demo/M0–M8; 6.3 glue; proc-gen; Godot/C#/HR — exec-deferred/advisory.

## Behavior

Launch → PlayRegion → HUD. LaunchFlowController: bootstrap + DevLeakageGuard → PresentationSessionHandle. PlayRegionHost: single viewport + sockets; `presentation.play_region_ready`. HUDLayerStack Base/Mode/Context/Transient; reflects mode, does not drive ModeTransitionGraph (4.2). KH-6.1-001–004. Detail → [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roll-up-2026-07-15]].

## Interfaces

Imports: presentation.* (1.1); InputIntent; PerspectiveEnvelope (4.1); ModeTransitionGraph awareness (4.2); SeamRegistry. Exports: PresentationShellManifest; PlayRegionHost → 6.2; HUD/KH/DevLeakageGuard. Non-import: RuleEngine (5.x), SimTick (3.x).

## Roll-up

Tables, KH, edges, OQs, tasks → [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roll-up-2026-07-15]].

## Handoff

**80** — NL complete; secondary feedstock qualified; tertiaries 6.1.1–6.1.3; next DFS **6.2**. Exec-deferred scene graph / checklist UI — advisory.
