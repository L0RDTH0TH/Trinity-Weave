---
title: Phase 6.1.2 — PlayRegionHost Mount Lifecycle
roadmap-level: tertiary
phase-number: 6
subphase-index: 6.1.2
project-id: genesis-mythos-master
status: active
priority: high
progress: 100
created: 2026-06-27
tags:
- roadmap
- genesis-mythos-master
- phase-6
- factory
- play-region
- presentation-shell
- half-a
para-type: Project
roadmap_track: conceptual
factory_track: true
horizon_demo_track: false
links:
- '[[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
- '[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
handoff_readiness: 84
product_factory_run_id: f35ff65cfb4f
parent_secondary: '6.1'
branch_split_reason: parent_6.1_oversized_secondary
rollup-detail: '[[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roll-up-2026-07-15]]'
body_compact_at: 2026-07-15
body_compact_queue: followup-deepen-phase612-tertiary-20260716T021200Z
factory_feed_gate_status: green
body_compact_status: complete
body_chars_pre_recompact: 1400
body_chars_claimed: 1060
body_chars_cap: 1200
body_over_cap: false
factory_feed_gate_reason: manual_chat_recompact_1200
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 6.1.2 — PlayRegionHost Mount Lifecycle

Decomposes **PlayRegion** from parent [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]: PlayRegionHost mount, rig sockets, `presentation.play_region_ready`, handoff from…

## Scope

**In:** PlayRegionHost states; prereq handle + launch_complete; play_region_ready; sockets (fp_baseline_rig, dm_worldcam_slot; mapcam stub); single-active-PlayRegion; fail rollback; MountContractGlue ids (6.2/6.3). **Out:** 6.1.1; 6.1.3; 6.2 demo; exec viewport — advisory.

## Behavior

launch_complete + valid handle → mount → sockets → play_region_ready → 6.1.3 may init. Duplicate ready → `duplicate_play_region`. Detail → [[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roll-up-2026-07-15]].

## Interfaces

Imports: launch_complete + handle (6.1.1); presentation.* (1.1); PerspectiveEnvelope (4.1); SeamRegistry (1.3). Exports: play_region_ready; PlayRegionMountReceipt; fail codes. Consumers: HUDLayerStack; 6.2 via MountContractGlue; KH-6.1-003.

## Handoff

**84%** — tertiary feedstock. Body ≤1200.
