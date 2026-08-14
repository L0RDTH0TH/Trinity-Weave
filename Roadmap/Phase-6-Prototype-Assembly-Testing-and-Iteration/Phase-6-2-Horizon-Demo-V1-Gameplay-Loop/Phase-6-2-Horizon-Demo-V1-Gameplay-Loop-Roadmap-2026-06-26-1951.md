---
title: Phase 6.2 — Horizon Demo v1 Gameplay Loop
roadmap-level: secondary
phase-number: 6
subphase-index: '6.2'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-6
- horizon-demo
- gameplay-loop
- half-a
para-type: Project
roadmap_track: conceptual
breadth_mint_complete: true
branch_open: false
depth_first_backfill: true
secondary_feedstock_qualified: true
factory_track: false
horizon_demo_track: true
links:
- '[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[genesis-mythos-master-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
handoff_readiness: 80
product_factory_run_id: 1373c0c3408d
rollup-detail: '[[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roll-up-2026-07-16]]'
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase62-20260716T204442Z
factory_feed_gate_status: green
body_compact_status: complete
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.2 — Horizon Demo v1 Gameplay Loop

Playable **horizon demo v1** loop: spawn → FP explore → intent stub → sim stub → rule check → DM cam → overwrite → feedback. Mounts into **6.1** PlayRegionHost — not factory spine.

## Scope

**In:** HorizonDemoManifest; SpawnBootstrapController; FPExploreRigHost; IntentPipelineStub; SimTickStub; RuleCheckProbe; DMCamTransitionSlot; OverwriteDemonstrationSlot; PlayerFeedbackChannel; DemoLoopOrchestrator (8 beats). **Out:** 6.1 factory attestation; 6.3 glue; proc-gen/multiplayer; Godot/C#/HR — exec-deferred/advisory.

## Behavior

Eight ordered beats via DemoLoopOrchestrator; stage signals `demo.*` on `session.*`. Detail + beat tables → [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roll-up-2026-07-16]].

## Interfaces

Imports: PlayRegionHost/HUD (6.1); PlayerFPRig (4.1); InputIntent (1.1); SimTick/WorldEventLog (3.1); RuleEngine (5.1); ModeTransitionGraph (4.2); OverwritePatch (3.3). Exports: HorizonDemoManifest; DemoLoopOrchestrator stage ids → 6.3 / exec.

## Roll-up

Tables, OQs, tasks, tertiary tree → [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roll-up-2026-07-16]].

## Handoff

**80** — NL complete; secondary feedstock qualified; tertiaries 6.2.1–6.2.8 closed; next DFS **6.3**. Exec-deferred demo scene / playtest HR — advisory.
