---
title: "CDR — Agency Envelope and Pilot Machinery Glue (4.3)"
created: 2026-06-26
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-4]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T164100Z-phase4-deepen-4-3
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: reconciled
related_research: []
---

## Summary

Chose **AgencyEnvelope** + **PilotMachineryGlue** as the integration layer: **PilotHandoffCoordinator** serializes dominate handoffs with 4.2 guard stacks via **AgencyTransitionGuardExtension**, and **AgencyPersistenceLedger** checkpoints dominate/absent-proxy + optional rail state across transitions. Rejected merging agency into **DMRigPolicyMatrix** rows (keeps 4.2 read-only matrix clean) and rejected dominate-without-handoff during SensoriumAttach (preserves 4.1/4.2 distinction).

## PMG alignment

Serves PMG pilot graph for dominate and absent-proxy agency — ensuring role-tailored views (4.2 DM rails) stay coherent when agency delegates, proxies off-screen activity (3.2), or persists across session boundaries without Presentation mutating Simulation.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|------------------|
| Agency columns inside DMRigPolicyMatrix | Single table | Conflates read-only DM rigs with agency-bearing modes | 4.2 matrix stays observation-only; agency lives in **AgencyEnvelope** |
| No persistence ledger (session-ephemeral only) | Simpler | Breaks save/resume dominate and DM rail UX | PMG implies long sessions; ledger contract deferred to execution |
| Allow dominate during SensoriumAttach | Faster DM POV switch | Violates observe-vs-agency boundary (4.1, 4.2) | Explicit block + handoff path via **PilotHandoffCoordinator** |
| Per-campaign ledger (D-4.3-001 alt) | Single campaign continuity | Breaks per-save-slot resume UX | **Conceptual authority:** per-save-slot checkpoint lean |
| Runtime DM proxy matrix override (D-4.3-002 alt) | Flexible steward behavior | Conflates 4.2 read-only matrix with agency policy | Static table + session token for `proxy_quest_steward` only |
| Session-ephemeral dominate across load (D-4.3-003 alt) | Simpler load path | Loses dominate binding on scene transition | **AgencyPersistenceLedger** checkpoint required; format → execution track |

## Validation evidence

- Pattern: agency delegation persistence across mode rails — aligned with 4.1 **PilotGraph** + 4.2 **TransitionGuardRegistry**
- Pattern: Phase 1.1 InputIntent routing under **PerspectiveEnvelope** legal modes
- Pattern: 3.2 **SinceYouLeftCompiler** surfacing for absent-proxy (read-only consumption)
- Parent slices: [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]], [[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]
- Validator first pass (IRA reconciled): [[.technical/Validator/roadmap-auto-validation-20260626T162942Z-godo-followup-20260626T164100Z-phase4-deepen-4-3]]
- Open question anchors: **D-4.3-001** .. **D-4.3-003** in [[decisions-log#Phase 4.3 open question anchors]]

## Links

- Parent slice: [[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]
- Workflow anchor: 2026-06-26 19:45 | deepen | Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue
- Master goal: [[genesis-mythos-master-goal]]
