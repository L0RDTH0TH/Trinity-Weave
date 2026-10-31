---
title: "CDR — Player FP and Perspective Envelope (4.1)"
created: 2026-06-26
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-4]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T164100Z-phase4-deepen-4-1
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: reconciled
related_research: []
---

## Summary

Chose a **unified scene graph** with **swappable camera interpolator registry** and explicit **PerspectiveEnvelope** separating read-only DM rigs (WorldCam, MapCam, SensoriumAttach) from agency-bearing **PlayerFPRig** and **PilotGraph** states (dominate, absent-proxy). Mode transitions flow through **ModeTransitionGraph** with guards from Phase 3 pause/veto seams.

## PMG alignment

Serves PMG goals for role-tailored views with seamless transitions: player FP baseline, DM observation without accidental sim mutation, and agency delegation (dominate / absent-proxy) as first-class Presentation nouns — matching master goal emphasis on perspective split and control systems without premature Godot implementation.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|------------------|
| Separate scene trees per mode | Simpler per-mode isolation | Duplicate world authority; drift risk | Violates 1.1 Presentation read-only projection invariant |
| Single fixed camera stack (no interpolator registry) | Less moving parts | Hard-coded transitions; poor DM rail UX | PMG calls for seamless transitions; registry enables swap without graph rewire |
| SensoriumAttach as dominate shortcut | Faster DM possess flow | Conflates read-only observe with agency (1.1 edge case) | Explicit **PilotGraph** edge required |

## Validation evidence

- Validator first pass (IRA reconciled): [[.technical/Validator/roadmap-auto-validation-20260626T171200Z-godo-followup-20260626T164100Z-phase4-deepen-4-1]] — `primary_code: safety_unknown_gap`; victim/passenger deferral row added to 4.1 Open questions; `execution_gaps_advisory: true` for rollup gates
- Pattern: Phase 1.1 Presentation mode graph + InputIntent agency table — [[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]
- Pattern: Phase 3.1 DMPauseGate + tick subscribe boundary — [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]
- Pattern: Phase 3.3 narrative veto on live patches — [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]

## Links

- Parent slice: [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]
- Workflow anchor: 2026-06-26 17:05 | deepen | Phase-4-1-Player-FP-and-Perspective-Envelope
- Master goal: [[genesis-mythos-master-goal]]
