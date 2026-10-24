---
title: Phase 4.1.3 — WorldCam / MapCam / SensoriumAttach FOV
roadmap-level: tertiary
phase-number: 4
subphase-index: 4.1.3
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: green
factory_feed_gate_reason: ''
body_compact_status: complete
body_chars_cap: 1200
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-4
- worldcam
- mapcam
- sensorium-attach
- fov
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]'
- '[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roll-up-2026-07-16]]'
rollup-detail: '[[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roll-up-2026-07-16]]'
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.1.3 — WorldCam / MapCam / SensoriumAttach FOV

**WorldCam** = DM tactical overview FOV (read-only WorldState). **MapCam** = strategic map FOV (faction/terrain overlays). **SensoriumAttach** = read-only entity sensorium FOV — not dominate. No Godot / factory/L5.

## Scope

**In:** Per-rig FOV contracts; WorldCam/`dm_world`; MapCam/`dm_map`; SensoriumAttach/`dm_sensorium_attach`; RO InputIntent ban except mode-switch; FOV after 4.1.2 activate.

**Out:** Envelope/ModeTransitionGraph/PilotGraph (`4.1.1`); UnifiedSceneGraph/Interpolator/PlayerFPRig (`4.1.2`); 4.2/4.3; Camera3D/SubViewport; passenger_fp (P5); factory/L5.

## Behavior

Guards (4.1.1) → deactivate → blend (4.1.2) → activate FOV → envelope RO routes → PilotGraph non-dominate on SensoriumAttach → `presentation.mode_changed`. Detail → [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roll-up-2026-07-16]].

## Interfaces

**In:** Mode IDs/guards (4.1.1); Scene/Interpolator (4.1.2); PresentationShell (1.1); tick RO (3.1). **Out:** FOV rig nouns → **4.2** / **6.1** / **6.2**.

## Handoff

**80%** DM FOV nouns. Slice green; siblings 4.1.1=1035 / 4.1.2=1176. Cap ≤1200.
