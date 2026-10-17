---
title: Phase 4.3.3 — AgencyPersistenceLedger / AbsentProxy / RailStatePersistence (Roll-up)
roadmap-level: rollup
phase-number: 4
subphase-index: "4.3.3"
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags: [roadmap, rollup, genesis-mythos-master, phase-4, agency-ledger]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roadmap-2026-07-16-0749]]"
  - "[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]"
  - "[[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roadmap-2026-07-16-0729]]"
---

# Phase 4.3.3 roll-up — AgencyPersistenceLedger / AbsentProxy / RailStatePersistence

Canonical compact tertiary: [[Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roadmap-2026-07-16-0749]]. Detail preserved off the ≤1400 feedstock body (`followup-deepen-phase433-tertiary-20260716T114316Z`); tertiary recompact ≤1200 (`followup-deepen-gmm-4-3-3-20260717T033631Z`) **1412→1173**.

## Purpose

Name the **persistence nouns** that keep dominate / absent-proxy / DM rail cursor coherent across mode transitions and session boundaries — without owning envelope classify or handoff choreography.

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **AgencyPersistenceLedger** | Append-only session log + checkpoint export: dominate bindings, `proxy_policy_id`, last `edge_id`, `active_rig_id`; per-save-slot lean (D-4.3-001) |
| **AbsentProxyPolicyTable** | Static rows: `proxy_policy_id` → {allowed_intents, surfacing_hints, max_duration_ticks}; DM session token override for `proxy_quest_steward` only (D-4.3-002) |
| **RailStatePersistence** | DM rail cursor: last `rig_id`, optional map zoom band — session-local default; optional ledger export for resume-DM UX |
| Cross-load dominate | Ledger checkpoint required before scene load while dominate active (D-4.3-003); serialization format execution-deferred |
| `envelope_snapshot` depth | Agency-class delta vs full PerspectiveEnvelope clone — ledger export shape owned here |

**Out:** AgencyEnvelope classify (`4.3.1`); PilotMachineryGlue / PilotHandoffCoordinator (`4.3.2`); Camera3D; typed serializers; factory/L5; execution pins; passenger_fp overlay (Phase 5).

## Sample proxy rows (conceptual)

| proxy_policy_id | allowed_intents | surfacing | max_duration_ticks |
|-----------------|-----------------|-----------|-------------------|
| `proxy_idle_guard` | patrol, ambient_dialogue | since_you_left_minor | 0 (until return) |
| `proxy_quest_steward` | quest_progress_local, faction_ping | since_you_left_major | bounded |
| `proxy_combat_stand_in` | defensive_only | combat_alert | short |

## Behavior detail

1. Glue/Coordinator reaches `handoff_complete` (4.3.2).
2. **AgencyPersistenceLedger** appends `{edge_id, pilot_state, binding_delta}`.
3. If PilotGraph enters absent-proxy: install **AbsentProxyPolicyTable** row; SinceYouLeft hints inform surfacing only — no WorldState write from Presentation.
4. **RailStatePersistence** updates session-local DM cursor; may export via ledger when operator enables resume-DM.
5. On cross-load dominate: require ledger checkpoint before load (D-4.3-003).
6. On hard freeze overwrite (3.3): export binding for audit; clear live binding when continuation blocked.

## Edge cases

- **Proxy + player return during DMPauseGate:** Proxy intents frozen per 3.1; resume reconciles PilotGraph to `self` before FP edge.
- **Ledger vs session-local rail:** Default session-local map annotations; ledger export opt-in — not forced on conceptual track.
- **DM override scope:** Only `proxy_quest_steward` may take session token override; no runtime DMRigPolicyMatrix column mutation (D-4.3-002).
- **envelope_snapshot depth:** Prefer agency-class delta for checkpoint lean; full clone only if Phase 5 spell metadata requires it — deferred.

## Open questions

- **Serializer format (D-4.3-001/003):** Execution track chooses binary/JSON shape at Phase 5+ handoff — conceptual contract is checkpoint presence + fields named here.
- **Resume-DM UX chrome:** Whether rail export surfaces in 4.2.3 chrome or Phase 5 catalog — deferred to factory Loop 2 / execution.

## Handoff criteria

- [x] AgencyPersistenceLedger / AbsentProxyPolicyTable / RailStatePersistence nouns named
- [x] Cross-load dominate checkpoint (D-4.3-003) explicit
- [x] Exports pointed at Phase 5+
- [x] Tertiary body recompact ≤1200 (`1412→1173`) — not factory/L5

**80%** handoff_readiness — implementer can persist dominate/proxy/rail without guessing envelope vs glue ownership. Slice feed **green** `tertiary_body_recompact_1200_complete`. Phase-4 tertiary recompact trail **closed**. Project harness next: Phase-5-1-1 tertiary body_over_cap (~1415>1200) — not factory/L5.
