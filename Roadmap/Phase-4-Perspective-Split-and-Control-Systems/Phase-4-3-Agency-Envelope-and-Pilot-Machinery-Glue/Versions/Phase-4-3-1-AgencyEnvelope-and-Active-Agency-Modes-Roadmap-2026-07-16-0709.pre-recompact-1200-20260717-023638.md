---
title: Phase 4.3.1 — AgencyEnvelope and Active Agency Modes
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.3.1"
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: red
factory_feed_gate_reason: body_over_cap:1271>1200
body_over_cap: true
body_chars_claimed: 1271
body_chars_cap: 1200
body_chars_pre_ira_handoff_honesty: 1296
created: 2026-07-16
tags: [roadmap, genesis-mythos-master, phase-4, agency-envelope, active-agency]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]"
  - "[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]"
  - "[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]"
  - "[[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]"
  - "[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]"
  - "[[genesis-mythos-master-goal]]"
  - "[[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roll-up-2026-07-16]]"
rollup-detail: "[[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roll-up-2026-07-16]]"
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
---

## Phase 4.3.1 — AgencyEnvelope and Active Agency Modes

**AgencyEnvelope** — specializes **PerspectiveEnvelope** (4.1): modes with **active_agency** (`player_fp`, dominate target) vs **observe_only** (DM rails). Conceptual — no Godot, no factory/L5.

## Scope

**In:** `active_agency` vs `observe_only`; dominate vs SensoriumAttach without handoff; post-pass retarget; `passenger_fp_overlay` hook (Phase 5).

**Out:** PilotHandoffCoordinator / glue (`4.3.2`); ledger / proxy / rail persist (`4.3.3`); Camera3D; serializers; factory/L5; exec pins.

## Behavior

Mode pass → AgencyEnvelope classifies → InputIntent retarget (1.1) → `presentation.agency_changed`. Illegal dominate on observe-only without handoff → block. Detail → [[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roll-up-2026-07-16]].

## Interfaces

**Imports:** PerspectiveEnvelope + PilotGraph (4.1); DM matrix / guards / rail chrome (4.2). **Exports:** agency class → **4.3.2** glue + Phase 5+.

## Roll-up

Edge cases + OQs → [[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roll-up-2026-07-16]].

## Handoff

**80%** — agency vs observe explicit. Exec-deferred — advisory. Slice feed **red** `body_over_cap:1271>1200` (pending recompact ≤1200). Next DFS **4.3.1** body recompact — not 4.3.2.
