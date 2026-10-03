---
title: Phase 4.1.3 — WorldCam / MapCam / SensoriumAttach FOV (Roll-up)
roadmap-level: rollup
phase-number: 4
subphase-index: 4.1.3
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags:
- roadmap
- rollup
- genesis-mythos-master
- phase-4
- worldcam
- mapcam
- sensorium-attach
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roll-up-2026-07-15]]'
- '[[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 4.1.3 roll-up — WorldCam / MapCam / SensoriumAttach FOV

Canonical compact tertiary: [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]. Detail preserved off feedstock; body recompact **1331→1153≤1200** (`followup-deepen-gmm-4-1-3-20260716T220407Z`); prior mint ≤1400 (`followup-deepen-phase413-tertiary-20260716T124026Z`).

## Purpose

Name the **DM observation FOV nouns** that bind read-only perspective frusta to envelope modes — without owning transition legality, scene composition, or Camera3D paths.

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **WorldCam** | DM tactical overview FOV; projects WorldState for `dm_world`; no **InputIntent** except mode-switch envelopes |
| **MapCam** | Strategic map FOV; faction/terrain overlays from projected state for `dm_map`; read-only |
| **SensoriumAttach** | Read-only bind to NPC/entity sensorium FOV for `dm_sensorium_attach` — **not** agency delegation (distinct from **PilotGraph** dominate) |
| FOV contract | Each rig declares its envelope mode ID + read-only intent ban; activated only after UnifiedSceneGraph PerspectiveAnchor swap (4.1.2) |

**Out:** PerspectiveEnvelope / ModeTransitionGraph / PilotGraph (`4.1.1`); UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig (`4.1.2`); 4.2 DMRigPolicyMatrix / TransitionGuardRegistry / DMRailUXContract; 4.3 AgencyEnvelope / glue / ledger; Camera3D / SubViewport; factory/L5; execution pins.

## Behavior detail

1. ModeTransitionGraph guards pass (4.1.1).
2. Source rig deactivate; interpolator blend/snap (4.1.2).
3. Target FOV rig activate on its PerspectiveAnchor (`WorldCam` / `MapCam` / `SensoriumAttach`).
4. PerspectiveEnvelope updates legal intent routes to read-only for that mode (4.1.1).
5. PilotGraph must **not** enter dominate while SensoriumAttach is active unless an explicit ModeTransitionGraph edge exits sensorium first.
6. Emit `presentation.mode_changed` with `active_rig_id` + FOV mode ID.

## Edge cases

- **Dominate vs SensoriumAttach:** SensoriumAttach is read-only perception; dominate transfers InputIntent — envelope rejects dominate while SensoriumAttach FOV active without explicit edge.
- **MapCam optional at factory Phase 0:** Per D-6.1.2-003 / D-6.1.3-002 — MapCam may be stubbed; WorldCam required for DM overview. Conceptual still names MapCam FOV here for 4.1 completeness.
- **WorldCam during DMPauseGate:** FOV may remain visually active; InputIntent stays mode-switch-only; sim pause does not unlock write paths.
- **Dual FOV claim:** PresentationShell enforces single `active_rig_id` — secondary FOV rig stays dormant.

## Open questions

- **Default FOV degrees / clipping** per rig — factory catalog / execution; not conceptual.
- **SubViewport vs single-camera stack for MapCam:** Execution; conceptual requires FOV noun + read-only contract only.

## Handoff criteria

- [x] WorldCam + MapCam + SensoriumAttach FOV nouns named
- [x] Read-only InputIntent ban stated per rig
- [x] Dominate vs SensoriumAttach disambiguation restated
- [x] Exports pointed at 4.2 / 6.1 / 6.2
- [x] Phase 4.1 tertiary branch closed; live next DFS Phase-5-1-3 body recompact ≤1200 (1353>1200); 5.1.2 cleared 1197≤1200; 4.2.x trail cleared; mint-era next 5.1.1 superseded

**80%** handoff_readiness — implementer can place DM FOV ownership without guessing envelope or scene-graph composition. Phase-4 tertiary tree closed; body recompact **1331→1153≤1200**; project harness **RED** next Phase-5-1-3 `body_over_cap:1353>1200` (4.2.x trail cleared ≤1200).
