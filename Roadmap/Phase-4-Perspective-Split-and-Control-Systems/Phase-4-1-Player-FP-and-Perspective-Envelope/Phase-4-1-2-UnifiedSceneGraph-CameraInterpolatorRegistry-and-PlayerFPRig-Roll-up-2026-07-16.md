---
title: Phase 4.1.2 — UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig
  (Roll-up)
roadmap-level: rollup
phase-number: 4
subphase-index: 4.1.2
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags:
- roadmap
- rollup
- genesis-mythos-master
- phase-4
- unified-scene-graph
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roll-up-2026-07-15]]'
- '[[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 4.1.2 roll-up — UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig

Canonical compact tertiary: [[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]. Detail preserved off the ≤1200 feedstock body (mint `followup-deepen-phase412-tertiary-20260716T122709Z`; recompact `followup-deepen-gmm-4-1-2-20260716T213643Z` 1407→1188).

## Purpose

Name the **composition nouns** that own scene attachment, camera blend selection, and the default player FP agency rig — without owning envelope legality, DM FOV contracts, or Camera3D paths.

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **UnifiedSceneGraph** | Single scene composition root; all perspective rigs attach as **PerspectiveAnchor** nodes; no duplicate world-mutation paths from Presentation |
| **PerspectiveAnchor** | Attach point for a rig; PresentationShell enforces at most one **active_rig_id** |
| **CameraInterpolatorRegistry** | Named interpolators (`ease_default`, `snap_cut`, `dm_orbit`) selectable per ModeTransitionGraph edge without rewiring the graph |
| **PlayerFPRig** | Default FP agency anchor; binds local player avatar presentation; routes self-agency intents upward; attaches to `fp_baseline_rig` socket (6.2.1) |
| Fallback emit | Missing interpolator → `snap_cut` + `presentation.interpolator_fallback` (never silent ease) |

**Out:** PerspectiveEnvelope / ModeTransitionGraph / PilotGraph (`4.1.1`); WorldCam / MapCam / SensoriumAttach FOV (`4.1.3`); 4.2 DMRigPolicyMatrix / TransitionGuardRegistry / DMRailUXContract; 4.3 AgencyEnvelope / glue / ledger; Camera3D / SubViewport; factory/L5; execution pins.

## Behavior detail

1. ModeTransitionGraph guards pass (4.1.1).
2. Source rig **deactivate**; flush any in-flight interpolator on its PerspectiveAnchor.
3. **CameraInterpolatorRegistry** resolves edge interpolator ID; missing → `snap_cut` + fallback emit.
4. Blend or snap from source PerspectiveAnchor to target over `transition_ms` (exec-deferred default).
5. Target activate; PerspectiveEnvelope updates legal intent routes (4.1.1).
6. PilotGraph reconciles agency (4.1.1 / 4.3 consumers).
7. Emit `presentation.mode_changed`.

## Edge cases

- **Dual-anchor claim:** Two rigs claim same PerspectiveAnchor — PresentationShell keeps secondary dormant; only `active_rig_id` may emit InputIntent.
- **Interpolator missing:** Always `snap_cut` + audible bus fallback — never silent `ease_default`.
- **Blend during DMPauseGate:** Finish committed visual blend; never leave half-active dual rigs writing intents.
- **PlayerFPRig vs dominate:** Dominate transfers InputIntent router (PilotGraph); PlayerFPRig remains the default self-agency socket when not dominated.

## Open questions

- **Default transition_ms** per edge — factory catalog / execution; not conceptual.
- **SubViewport vs single-camera stack:** Execution; conceptual requires UnifiedSceneGraph single-authority only.

## Handoff criteria

- [x] UnifiedSceneGraph + CameraInterpolatorRegistry + PlayerFPRig nouns named
- [x] PerspectiveAnchor + active_rig_id exclusivity stated
- [x] Fallback interpolator contract named
- [x] Exports pointed at 4.1.3 / 4.2 / 6.2.1
- [x] Next DFS advanced: Phase-4-1-3 / 4.2.1 / 4.2.2 cleared ≤1200; live next Phase-4-2-3 body recompact

**80%** handoff_readiness — implementer can place scene composition, blend selection, and FP baseline without guessing envelope or DM FOV ownership. Phase-4 tertiary tree is **closed**. Slice feedstock is **green** **1176≤1200** (recompact `followup-deepen-gmm-4-1-2-20260716T213643Z` + sibling scrub); historical 4.2.x trail cleared; live next DFS Phase-5-1-3 `body_over_cap:1353>1200` (5.1.2 cleared 1197≤1200).
