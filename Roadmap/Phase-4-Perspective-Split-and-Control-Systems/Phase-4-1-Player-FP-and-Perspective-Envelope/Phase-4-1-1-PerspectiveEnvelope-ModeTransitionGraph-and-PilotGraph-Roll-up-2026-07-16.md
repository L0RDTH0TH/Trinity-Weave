---
title: Phase 4.1.1 — PerspectiveEnvelope / ModeTransitionGraph / PilotGraph (Roll-up)
roadmap-level: rollup
phase-number: 4
subphase-index: 4.1.1
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags:
- roadmap
- rollup
- genesis-mythos-master
- phase-4
- perspective-envelope
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roll-up-2026-07-15]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 4.1.1 roll-up — PerspectiveEnvelope / ModeTransitionGraph / PilotGraph

Canonical compact tertiary: [[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]. Detail preserved off the feedstock body — mint ≤1400 (`followup-deepen-phase411-tertiary-20260716T120213Z`); **recompact ≤1200** (`architect-rr-gmm-remi-fd0e8a04`, Config `max_note_body_chars.tertiary: 1200`).

## Purpose

Name the **control nouns** that declare legal perspective modes, legal transitions among them, and agency delegation states — without owning scene composition, interpolator curves, or per-rig FOV.

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **PerspectiveEnvelope** | Legal modes (`player_fp`, `dm_world`, `dm_map`, `dm_sensorium_attach`); which modes may emit **InputIntent** vs read-only observe; passenger_fp / spell-bound overlay is **not** an envelope mode (Phase 5) |
| **ModeTransitionGraph** | Directed edges among modes/rigs; guard predicates: DM session authority, **DMPauseGate** (3.1), **NarrativeDeltaVetoPolicy** (3.3) |
| **PilotGraph** | Agency state machine: **self** → **dominate** (possess target) → **absent-proxy** (NPC acts per policy while player away) |
| Emit contract | `presentation.mode_changed` / `presentation.rig_active` on `presentation.*` bus (1.1) |

**Out:** UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig (`4.1.2`); WorldCam/MapCam/SensoriumAttach FOV contracts (`4.1.3`); 4.2 DMRigPolicyMatrix / TransitionGuardRegistry / DMRailUXContract; 4.3 AgencyEnvelope / glue / ledger; Camera3D; factory/L5; execution pins.

## Behavior detail

1. Mode intent arrives (player or DM).
2. **ModeTransitionGraph** evaluates guards (DM authority, pause, narrative veto).
3. Source rig **deactivate** (flush pending interpolator — registry owned by 4.1.2).
4. Interpolator blend or snap (4.1.2) from source **PerspectiveAnchor** to target.
5. Target activate; **PerspectiveEnvelope** updates legal intent routes.
6. **PilotGraph** reconciles agency (dominate transfers InputIntent router; absent-proxy installs proxy without Presentation→WorldState write).
7. Emit `presentation.mode_changed`.

## Edge cases

- **Dominate vs SensoriumAttach:** SensoriumAttach is read-only; dominate transfers InputIntent — envelope rejects dominate while SensoriumAttach active without explicit ModeTransitionGraph edge.
- **Transition during DMPauseGate:** Finish blend or snap — never half-active dual rigs writing intents.
- **Interpolator missing:** Fallback `snap_cut` (4.1.2); this slice only names the emit seam.
- **passenger_fp:** Dominator possess branch only here; victim overlay deferred Phase 5.

## Open questions

- **Default transition_ms** per edge — factory catalog / execution; not conceptual.
- **SubViewport vs single-camera:** Execution; conceptual requires UnifiedSceneGraph single-authority (4.1.2).

## Handoff criteria

- [x] PerspectiveEnvelope + ModeTransitionGraph + PilotGraph nouns named
- [x] Imports from 1.1 / 3.1 / 3.3 restated
- [x] Exports pointed at 4.2 / 4.3 / sibling 4.1.x tertiaries
- [x] Next DFS 4.1.2 UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig

**80%** handoff_readiness — implementer can distinguish envelope legality, transition guards, and pilot agency without guessing scene/interpolator ownership. Phase-4 tertiary tree is **closed** (`phase_4_tertiary_tree_complete: true`). Phase-4-1-1 slice body **1061≤1200** (under cap; slice green). Phase-4-1-2 live **1176≤1200**; Phase-4-1-3 cleared **1153≤1200**; 4.2.1–4.2.3 cleared ≤1200. Project harness remains **red** because Phase-5-1-3 body **1353>1200** under Config tertiary cap (next DFS body recompact; 5.1.1 cleared 1186≤1200; 5.1.2 cleared 1197≤1200). Phase-4-3-1 cleared **1158≤1200**.
