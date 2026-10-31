---
title: Phase 4.3 — Agency Envelope and Pilot Machinery Glue
roadmap-level: secondary
phase-number: 4
subphase-index: '4.3'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
feedstock_qualified_at: 2026-07-16
feedstock_qualify_queue: architect-rr-gmm-remi-20c5587d
breadth_mint_complete: true
secondary_feedstock_qualified: true
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-4
- agency
- pilot-glue
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roll-up-2026-07-15]]'
- '[[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]'
- '[[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roadmap-2026-07-16-0729]]'
- '[[Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roadmap-2026-07-16-0749]]'
rollup-detail: '[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roll-up-2026-07-15]]'
factory_feed_gate_status: green
body_compact_status: complete
body_compact_at: 2026-07-16
body_compact_queue: architect-rr-gmm-remi-20c5587d
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.3 — Agency Envelope and Pilot Machinery Glue

**AgencyEnvelope** + **PilotMachineryGlue** join **PilotGraph** (4.1) to **DMRigPolicyMatrix** / **TransitionGuardRegistry** (4.2). Persist dominate / absent-proxy across mode transitions.

## Scope

**In:** AgencyEnvelope; PilotMachineryGlue; PilotHandoffCoordinator; DominateSessionBinding; AbsentProxyPolicyTable; AgencyPersistenceLedger; RailStatePersistence; AgencyTransitionGuardExtension. **Out:** Rig nouns (4.1); DM matrix (4.2); Camera3D; passenger_fp (P5); factory/L5.

## Behavior

Intent → PilotGraph → handoff (if dominate) → AgencyTransitionGuardExtension + 4.2 registry → deactivate/interpolator/activate → AgencyEnvelope retargets → ledger → `presentation.agency_changed`. Detail → [[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roll-up-2026-07-15]].

## Interfaces

Imports: 4.1 PilotGraph/envelope/shell; 4.2 guards/matrix/DMRailUXContract; 3.2/3.3. Exports: AgencyPersistenceLedger + AgencyEnvelope → Phase 5+.

## Roll-up

Actors, ordering, edge cases, open Qs, tasks, dataview → [[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roll-up-2026-07-15]].

## Handoff

**80** — NL complete; **4.3.1–4.3.3** minted; **4.3** branch closed; `secondary_feedstock_qualified: true`; next feedstock **4.2**.
