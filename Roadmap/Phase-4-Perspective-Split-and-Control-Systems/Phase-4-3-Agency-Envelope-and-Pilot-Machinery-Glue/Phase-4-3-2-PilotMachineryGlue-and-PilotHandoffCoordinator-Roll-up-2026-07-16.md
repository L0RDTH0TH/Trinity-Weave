---
title: Phase 4.3.2 — PilotMachineryGlue and PilotHandoffCoordinator (Roll-up)
roadmap-level: rollup
phase-number: 4
subphase-index: 4.3.2
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags:
- roadmap
- rollup
- genesis-mythos-master
- phase-4
- pilot-glue
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roadmap-2026-07-16-0729]]'
- '[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 4.3.2 roll-up — PilotMachineryGlue / PilotHandoffCoordinator

Canonical compact tertiary: [[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roadmap-2026-07-16-0729]]. Detail preserved off the ≤1400 feedstock body (`followup-deepen-phase432-tertiary-20260716T111951Z`); tertiary recompact ≤1200 **1318→1189** (`followup-deepen-gmm-4-3-2-20260717T025252Z`).

## Purpose

Name the **orchestrator** that joins PilotGraph agency intents to ModeTransitionGraph edge fires, and the **handoff state machine** that keeps dominate binding coherent across DM rail navigation — without owning envelope classify or persistence ledger.

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **PilotMachineryGlue** | Single-flight entry: mode transition requested → PilotGraph → AgencyTransitionGuardExtension → 4.2 TransitionGuardRegistry → post-transition intent reconcile |
| **PilotHandoffCoordinator** | States: `idle` → `dominate_pending` → `dominate_active` → `dominate_release` → `idle`; waits CameraInterpolatorRegistry blend before intent router swap |
| **DominateSessionBinding** | `{target_entity_id, source_rig_id, envelope_snapshot}` for dominate duration; cleared on release or narrative veto (3.3) |
| **AgencyTransitionGuardExtension** | Predicates layered on 4.2: `dominate_compatible`, `proxy_active`, `agency_envelope_legal`, `handoff_complete` |
| `presentation.agency_busy` | Reject/queue second concurrent dominate+rail intent through Glue single-flight |

**Out:** AgencyEnvelope classify (`4.3.1`); AgencyPersistenceLedger / AbsentProxyPolicyTable / RailStatePersistence (`4.3.3`); Camera3D; serializers; factory/L5; execution pins.

## Behavior detail

1. Presentation receives mode-switch or dominate request.
2. **PilotMachineryGlue** reads **PilotGraph** (`self` \| `dominate` \| `absent-proxy`).
3. If dominate-related: **PilotHandoffCoordinator** enters `dominate_pending` / stages release; may defer 4.2 edge until `handoff_complete`.
4. AgencyTransitionGuardExtension + TransitionGuardRegistry evaluate.
5. On pass: interpolator blend → Coordinator reaches `handoff_complete` → intent router retargets → binding set or cleared → emit `presentation.agency_changed`.
6. Dominate + WorldCam: Glue keeps binding active; DM rail observe-only for camera; agency stays on possessed target (envelope class from 4.3.1).

## Edge cases

- **Dominate release mid-interpolator:** Coordinator waits blend `handoff_complete` before clearing DominateSessionBinding — no dangling intent target.
- **Concurrent dominate + DM rail:** Serialize through Glue single-flight; second intent queues or rejects with `presentation.agency_busy`.
- **SensoriumAttach + dominate:** Envelope (4.3.1) declares illegality without handoff path; Glue only stages when envelope class allows.
- **FP return while dominate active:** Coordinator must release binding before `player_fp` reclaim edge.
- **Narrative veto (3.3):** Binding clear treated as forced `dominate_release` — no silent WorldState write from Presentation.

## Open questions

- **Queue vs reject on agency_busy:** Prefer reject with chrome reason (4.2.3) for operator clarity; queue only for same-source debounce — deferred to execution UX.
- **envelope_snapshot depth:** Full PerspectiveEnvelope clone vs agency-class delta — owned by 4.3.3 ledger export shape.

## Handoff criteria

- [x] PilotMachineryGlue + PilotHandoffCoordinator nouns named
- [x] DominateSessionBinding ownership + handoff state machine explicit
- [x] AgencyTransitionGuardExtension predicates named vs 4.2 registry
- [x] Exports pointed at 4.3.3 ledger/proxy/rail persist
- [x] Tertiary body recompact ≤1200 (**1318→1189**) — slice feed **green**
- [x] Next DFS **4.3.3** body recompact ≤1200 — **cleared** 1412→1173 (`followup-deepen-gmm-4-3-3-20260717T033631Z`); live next **5.1.3** `1353>1200`. Slice feed **green** `1189≤1200`. Project harness remains **red** for **Phase-5-1-3** `body_over_cap:1353>1200` (5.1.2 cleared 1379→1197; Phase-4-3-3 cleared 1173≤1200) (Phase-4 tertiary tree is **closed** — `phase_4_tertiary_tree_complete: true`; FIX-009: not tree-incomplete).
