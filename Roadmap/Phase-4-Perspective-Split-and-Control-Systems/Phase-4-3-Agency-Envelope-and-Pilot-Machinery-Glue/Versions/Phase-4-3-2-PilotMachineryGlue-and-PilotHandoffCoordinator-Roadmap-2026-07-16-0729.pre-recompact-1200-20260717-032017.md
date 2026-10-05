---
title: Phase 4.3.2 — PilotMachineryGlue and PilotHandoffCoordinator
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.3.2"
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: red
factory_feed_gate_reason: body_over_cap:1318>1200
created: 2026-07-16
tags: [roadmap, genesis-mythos-master, phase-4, pilot-glue, handoff-coordinator]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]"
  - "[[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]"
  - "[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]"
  - "[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]"
  - "[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]"
  - "[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]"
  - "[[genesis-mythos-master-goal]]"
  - "[[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roll-up-2026-07-16]]"
rollup-detail: "[[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roll-up-2026-07-16]]"
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
---

## Phase 4.3.2 — PilotMachineryGlue and PilotHandoffCoordinator

**PilotMachineryGlue** joins **PilotGraph** (4.1) to **TransitionGuardRegistry** (4.2). **PilotHandoffCoordinator** stages dominate across DM rails.

## Scope

**In:** Glue single-flight; Coordinator (`idle`→`dominate_pending`→`dominate_active`→`dominate_release`→`idle`); DominateSessionBinding; AgencyTransitionGuardExtension (`dominate_compatible`, `proxy_active`, `agency_envelope_legal`, `handoff_complete`).

**Out:** AgencyEnvelope (`4.3.1`); ledger / proxy / rail persist (`4.3.3`); Camera3D; serializers; factory/L5; exec pins.

## Behavior

Mode request → Glue → Coordinator if dominate → guards + 4.2 registry → wait `handoff_complete` → intent swap → binding set/clear → `presentation.agency_changed`. Detail → [[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roll-up-2026-07-16]].

## Interfaces

**Imports:** AgencyEnvelope (4.3.1); PilotGraph (4.1); TransitionGuardRegistry + interpolator (4.2). **Exports:** handoff + binding → **4.3.3** + Phase 5+.

## Roll-up

Edge cases + OQs → [[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roll-up-2026-07-16]].

## Handoff

**80%** — glue/handoff nouns explicit. Slice **red** `body_over_cap` pending self recompact ≤1200. Next DFS **4.3.2** — not 4.3.3 / factory/L5.

