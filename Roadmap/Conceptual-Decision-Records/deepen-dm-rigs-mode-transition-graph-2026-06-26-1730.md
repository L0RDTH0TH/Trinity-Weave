---
title: "CDR — DM Rigs and Mode Transition Graph (4.2)"
created: 2026-06-26
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-4]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T164100Z-phase4-deepen-4-2
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: reconciled
related_research: []
---

## Summary

Chose an explicit **DMRigPolicyMatrix** (per-rig projection, overlay, intent_eligibility rows) plus a **TransitionGuardRegistry** of composable predicates that refine **ModeTransitionGraph** edges from 4.1. Rejected direct FP ↔ SensoriumAttach shortcuts; all DM observation transitions route through guard stacks integrating **DMPauseGate** (3.1) and **NarrativeDeltaVetoPolicy** (3.3).

## PMG alignment

Serves PMG role-tailored DM views (WorldCam / MapCam / SensoriumAttach read-only) with seamless, guarded transitions — separating observation policy from agency (4.1 PilotGraph) and preventing accidental sim mutation during mode rails.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|------------------|
| Inline guards per edge only (no registry) | Fewer nouns | Duplicated predicate logic across edges | Registry enables reuse and audit (`guard_id` vocabulary) |
| Unified DM rig (single camera mode) | Simpler matrix | Loses tactical vs strategic vs sensorium distinction | PMG explicitly names three DM rigs |
| Allow FP → SensoriumAttach direct edge | Faster DM POV | Conflates observe with agency; violates 4.1 PilotGraph | Explicit **rejected** edge; route via WorldCam or dominate |

## Validation evidence

- Validator first pass (IRA reconciled): [[.technical/Validator/roadmap-auto-validation-20260626T180600Z-godo-followup-20260626T164100Z-phase4-deepen-4-2]] — `primary_code: contradictions_detected`; overwrite guard wired on DM exit edges post-IRA
- Validator second pass: [[.technical/Validator/roadmap-auto-validation-20260626T182000Z-godo-followup-20260626T164100Z-phase4-deepen-4-2-second-pass]] — `primary_code: missing_roll_up_gates`; `recommended_action: log_only`; inter-DM pause exemption documented in 4.2 TransitionGuardRegistry
- Validator third pass: [[.technical/Validator/roadmap-auto-validation-20260626T194500Z-godo-followup-20260626T164100Z-phase4-deepen-4-2]] — `log_only`; pause exemption cleared; 4.2 FM progress hygiene applied
- IRA report: [[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-godo-followup-20260626T164100Z-phase4-deepen-4-2.md]]

## Links

- Parent slice: [[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]
- Workflow anchor: 2026-06-26 17:30 | deepen | Phase-4-2-DM-Rigs-and-Mode-Transition-Graph
- Master goal: [[genesis-mythos-master-goal]]
