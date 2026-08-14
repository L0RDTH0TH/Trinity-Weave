---
title: Phase 6 — Prototype Assembly, Testing, and Iteration
roadmap-level: primary
phase-number: 6
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 86
conceptual_map_slice: roll_up_gates_added
roadmap_track: conceptual
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase
para-type: Project
links:
- '[[genesis-mythos-master-Roadmap-2026-06-26-0914]]'
- '[[Conceptual-Decision-Records/reference-exemplar-dual-goal-2026-08-01]]'
- '[[REFERENCE-EXEMPLAR-CHARTER]]'
rollup-detail: '[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roll-up-2026-07-15]]'
body_compact_at: 2026-07-15
body_compact_queue: followup-deepen-phase6-primary-20260716T010600Z
factory_feed_gate_status: green
body_compact_status: complete
frozen: true
conceptual_frozen_at: '2026-08-02T03:45:00Z'
operator_triad_rewrite_at: '2026-08-01'
---

## Phase 6 — Prototype Assembly, Testing, and Iteration

**Three tracks** — factory spine, playable demo proof, and Reference Exemplar. Do not conflate.

| Track | Phase | Purpose |
|-------|-------|---------|
| Factory | 6.1 | Launch → PlayRegion → HUD; kinesthetic honesty |
| Horizon demo | 6.2 | ~30 min proof loop (may stub gen) |
| Glue | 6.3 | Factory vs demo boundary |
| **Reference Exemplar** | **6.4** | Medium Fantasy default pack; campaign-capable gen + coherent graphics |

- [x] 6.1 Factory Phase 0 presentation shell — [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912|6.1]]
- [x] 6.2 Horizon demo v1 gameplay loop — [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951|6.2]]
- [x] 6.3 Factory vs demo track boundary glue — [[Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roadmap-2026-06-26-2031|6.3]]
- [x] 6.4 Reference Exemplar — [[Phase-6-4-Reference-Exemplar-Roadmap-2026-08-01|6.4]] (operator manual mint; deepen skipped)

CDR: [[Conceptual-Decision-Records/reference-exemplar-dual-goal-2026-08-01]]. Charter: [[REFERENCE-EXEMPLAR-CHARTER]]. 6.1–6.3 bodies unchanged.

## Scope

In: 6.1 PresentationShellManifest/LaunchFlowController/PlayRegionHost/HUDLayerStack/DevLeakageGuard/KinestheticHonestyChecklist (`ui_presentation_shell`); 6.2 HorizonDemoManifest/DemoLoopOrchestrator eight-beat mount into 6.1; 6.3 DualTrackBoundaryManifest/MountContractGlue/AttestationSeparationPolicy; **6.4 ReferenceExemplarManifest intent + DoD pointers** (not factory start). Consumes 1.1/3.x/4.x/5.x + Phase 2 for Exemplar gen bar. Out: Godot/C#, factory/L5 art bible, REGISTRY-CI/HR — execution-deferred/advisory.

## Behavior

Actors span 6.1–6.4. Order: 6.1 before 6.2; 6.2 mounts PlayRegionHost/HUDLayerStack only; 6.3 seam policy; **6.4 delivery track** uses shell, distinct from demo attestation. Factory attestation ≠ demo.loop_complete; Exemplar ≠ horizon demo bar.

## Interfaces

Exports: PresentationShellManifest; PlayRegionHost sockets; presentation.*/session.*/demo.* bus; HorizonDemoManifest; DualTrackBoundaryManifest; ReferenceExemplarManifest (conceptual). Imports: RuleEffectBus (5.x); PerspectiveEnvelope (4.1); DMOverwriteClass (3.x); InputIntent (1.x); Phase 2 gen contracts (Exemplar). See 6.1–6.4.

## Edge cases

Partial 6.x ≠ block map freeze. No second PlayRegionHost; DevLeakageGuard intact. Sim stub ≤1 tick/loop (demo). Exemplar campaign-capable gen is delivery DoD — not satisfied by demo stubs alone. Factory/L5 out of scope on this leaf.

## Roll-up & handoff

Handoff table, gates, open Qs, consistency, dataview → [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roll-up-2026-07-15]] (86%). Operator triad rewrite 2026-08-01; 6.4 rollup [[Phase-6-4-Reference-Exemplar-Roll-up-2026-08-01]].

## Subphases

Tree → [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roll-up-2026-07-15#Subphases & notes|rollup]] + 6.4 folder.
