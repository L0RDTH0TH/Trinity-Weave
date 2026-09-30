---
title: Phase 6.3 — Factory vs Demo Track Boundary Glue
roadmap-level: secondary
phase-number: 6
subphase-index: '6.3'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-6
- dual-track
- boundary-glue
- half-a
para-type: Project
roadmap_track: conceptual
breadth_mint_complete: true
secondary_feedstock_qualified: true
factory_track: false
horizon_demo_track: false
dual_track_glue: true
links:
- '[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[genesis-mythos-master-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
handoff_readiness: 80
product_factory_run_id: 1373c0c3408d
rollup-detail: '[[Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roll-up-2026-07-16]]'
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase63-20260716T210004Z
factory_feed_gate_status: green
factory_feed_gate_reason: conceptual_factory_feed_ready:pmg_phases
body_compact_status: complete
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.3 — Factory vs Demo Track Boundary Glue

Seam contracts so **6.1** factory spine and **6.2** horizon demo coexist without authority bleed. Glue only — no beats, no catalog rows.

## Scope

**In:** DualTrackBoundaryManifest; TrackAuthorityRegistry; MountContractGlue; AttestationSeparationPolicy; CrossTrackEventFirewall; FailureRoutingPolicy; BuildProfileSelector (`horizon_demo_in_shell` default). **Out:** 6.1/6.2 internals; proc-gen/multiplayer; Godot/C#/HR — exec-deferred/advisory.

## Behavior

Demo mounts into 6.1 PlayRegionHost/HUD sockets; factory vs demo attestations independent; default integrated profile `horizon_demo_in_shell`. Detail + matrices → [[Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roll-up-2026-07-16]].

## Interfaces

Imports: PresentationShellManifest/DevLeakageGuard (6.1); HorizonDemoManifest (6.2); SeamRegistry (1.3). Exports: DualTrackBoundaryManifest; TrackAuthorityRegistry; BuildProfileSelector → exec / Half A boundary review.

## Roll-up

Tables, OQs, tasks → [[Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roll-up-2026-07-16]].

## Handoff

**80** — NL complete; secondary feedstock qualified; Phase 6 secondaries 6.1–6.3 tree complete; factory_feed_gate **GREEN** `pmg_phases`. Exec-deferred dual-attestation CI — advisory.
