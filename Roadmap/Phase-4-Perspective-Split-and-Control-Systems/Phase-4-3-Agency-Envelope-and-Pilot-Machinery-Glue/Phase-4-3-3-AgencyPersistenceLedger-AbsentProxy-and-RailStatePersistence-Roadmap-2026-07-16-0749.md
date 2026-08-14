---
title: Phase 4.3.3 — AgencyPersistenceLedger / AbsentProxy / RailStatePersistence
roadmap-level: tertiary
phase-number: 4
subphase-index: 4.3.3
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: green
factory_feed_gate_reason: tertiary_body_recompact_1200_complete
body_over_cap: false
body_chars_claimed: 1100
body_chars_cap: 1200
body_chars_pre_recompact: 1223
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-4
- agency-ledger
- absent-proxy
- rail-persist
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]'
- '[[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roadmap-2026-07-16-0729]]'
- '[[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]'
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roll-up-2026-07-16]]'
rollup-detail: '[[Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roll-up-2026-07-16]]'
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.3.3 — AgencyPersistenceLedger / AbsentProxy / RailStatePersistence

**AgencyPersistenceLedger** checkpoints dominate / absent-proxy / last rail. **AbsentProxyPolicyTable** installs proxy intents while away. **RailStatePersistence** holds DM rail cursor (session-local).

## Scope

**In:** Ledger append+checkpoint (bindings, `proxy_policy_id`, last `edge_id`, `active_rig_id`); AbsentProxyPolicyTable; RailStatePersistence; D-4.3-001/002/003.

**Out:** AgencyEnvelope (`4.3.1`); Glue/Coordinator (`4.3.2`); Camera3D; serializers; factory/L5; exec pins.

## Behavior

Handoff complete → ledger append `{edge_id, pilot_state, binding_delta}` → proxy install → optional rail export. Cross-load dominate needs ledger checkpoint (D-4.3-003).

## Interfaces

**Imports:** Envelope (4.3.1); Glue/Coordinator (4.3.2); DMRailUXContract (4.2.3); SinceYouLeft (3.2). **Exports:** ledger + proxy + rail → Phase 5+.

## Roll-up

Edge cases + OQs → [[Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roll-up-2026-07-16]].

## Handoff

**80%** — persistence nouns explicit. Exec-deferred — advisory. Body ≤1200.
