---
title: Phase 4.3 — Agency Envelope and Pilot Machinery Glue (Roll-up)
roadmap-level: rollup
phase-number: 4
subphase-index: '4.3'
project-id: genesis-mythos-master
status: complete
priority: high
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-4
- agency
- pilot-glue
- rollup
para-type: Project
roadmap_track: conceptual
rollup_of: '[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
links:
- '[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
body_compact_source_queue: followup-deepen-phase43-20260715T230400Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 4.3 — Roll-up detail (factory feed-gate compact)

Canonical NL detail preserved from secondary body compact 2026-07-15 (queue followup-deepen-phase43-20260715T230400Z). Secondary keeps nouns + scope; this note holds tables, ordering, edge cases, open questions, tasks, dataview.

## Phase 4.3 — Agency Envelope and Pilot Machinery Glue

Integrate **PilotGraph** agency states (4.1) with **DMRigPolicyMatrix** + **TransitionGuardRegistry** mode rails (4.2) via an **AgencyEnvelope** that persists dominate / absent-proxy bindings across mode transitions and session boundaries. This slice owns **pilot machinery glue** — how **InputIntent** routing, **PerspectiveEnvelope** legal modes, and DM observation rails stay coherent when agency delegates or proxies — without Godot wiring (execution-deferred).

## Scope

**In scope:** **AgencyEnvelope** (session-scoped + cross-session persistence contract for agency-bearing vs read-only modes); **PilotMachineryGlue** (orchestrator reconciling **PilotGraph** with **ModeTransitionGraph** edge fires); **PilotHandoffCoordinator** (ordered handoff when dominate starts/ends during DM rail navigation); **DominateSessionBinding** (target entity + envelope snapshot while dominate active); **AbsentProxyPolicyTable** (NPC proxy behavior while player away — tone-weighted lean per 4.1); **AgencyPersistenceLedger** (durable dominate/absent-proxy + last rail state for save/load); **RailStatePersistence** (DM rail cursor: last `rig_id`, optional map annotation handles — session-local default, ledger export optional); **AgencyTransitionGuardExtension** (extra predicates layered on 4.2 registry: `dominate_compatible`, `proxy_active`, `agency_envelope_legal`, `handoff_complete`); **PresentationShell** glue hooks (4.1) invoked before/after 4.2 guard stacks.

**Out of scope:** Rig nouns and interpolator registry (4.1); exhaustive DM matrix rows and edge catalog (4.2); Godot scene/input wiring; execution-track typed interfaces and rollup HR gates (execution-deferred / advisory on conceptual track); spell-bound victim **passenger_fp** overlay (Phase 5); **ToneProfileNarrativeWeights** table definition (Phase 2/3 — 4.3 consumes hints only).

## Behavior

**Actors:**

| Actor | Role |
|-------|------|
| **AgencyEnvelope** | Superset of **PerspectiveEnvelope** (4.1): declares which modes may hold **active_agency** (`player_fp`, dominate-possessed target) vs **observe_only** (all DM rigs); blocks illegal dominate while SensoriumAttach active without handoff |
| **PilotMachineryGlue** | Single entry for "mode transition requested" → consult **PilotGraph** → **AgencyTransitionGuardExtension** → delegate to 4.2 **TransitionGuardRegistry** → reconcile intents post-transition |
| **PilotHandoffCoordinator** | State machine: `idle` → `dominate_pending` → `dominate_active` → `dominate_release` → `idle`; coordinates with **CameraInterpolatorRegistry** blend completion before intent router swap |
| **DominateSessionBinding** | Records `{target_entity_id, source_rig_id, envelope_snapshot}` for dominate duration; cleared on release or narrative veto (3.3) |
| **AbsentProxyPolicyTable** | Rows: `proxy_policy_id` → {allowed_intents, surfacing_hints_from_3.2, max_duration_ticks}; installed when **PilotGraph** enters absent-proxy |
| **AgencyPersistenceLedger** | Append-only session log + checkpoint export: dominate bindings, proxy policy id, last `edge_id` traversed, `active_rig_id` |
| **RailStatePersistence** | Optional persistence of **DMRailUXContract** cursor (last rig, map zoom band) — default session-local; ledger may export for "resume DM session" UX |
| **AgencyTransitionGuardExtension** | Predicates appended to 4.2 guard stacks on agency-sensitive edges |

**AgencyTransitionGuardExtension predicates:**

| guard_id | Predicate (NL) | Blocks when |
|----------|----------------|-------------|
| `agency_envelope_legal` | Target mode permits requested agency class | Dominate requested while target mode is read-only without dominate handoff path |
| `dominate_compatible` | **PilotGraph** state allows edge | Dominate active but edge would drop binding without release choreography |
| `proxy_active` | Absent-proxy policy still valid | Proxy expired or superseded by player return |
| `handoff_complete` | **PilotHandoffCoordinator** not mid-transition | Interpolator or intent router swap incomplete |

**PilotGraph × ModeTransitionGraph glue (ordering):**

1. Mode-switch intent arrives (DM rail, envelope, or dominate command)
2. **PilotMachineryGlue** reads **PilotGraph** state (`self` \| `dominate` \| `absent-proxy`)
3. If dominate-related: **PilotHandoffCoordinator** stages handoff; may defer edge until `handoff_complete`
4. **AgencyTransitionGuardExtension** + 4.2 **TransitionGuardRegistry** evaluate combined stack
5. On pass: 4.1 deactivate → interpolator → 4.2 matrix activate (unchanged from 4.2)
6. **AgencyEnvelope** updates `active_agency` vs `observe_only`; **InputIntent** router retargets per 1.1
7. **AgencyPersistenceLedger** appends `{edge_id, pilot_state, binding_delta}`
8. Emit `presentation.agency_changed` + `presentation.mode_changed` on `presentation.*` bus

**Dominate + DM rail interaction:**

| Scenario | Glue behavior |
|----------|---------------|
| Dominate active + WorldCam request | **Allowed** — dominate does not block DM observation (4.2); **AgencyEnvelope** keeps dominate binding; intents route to possessed target |
| Dominate active + SensoriumAttach request | **Blocked** via 4.2 `not_dominate_active` unless explicit `dominate_release` handoff first |
| Dominate active + FP return | **PilotHandoffCoordinator** releases binding → `world_to_fp` or `sensorium_to_fp` per 4.2 edge catalog |
| Absent-proxy + off-screen sim (3.2) | **AbsentProxyPolicyTable** row drives proxy intents; **SinceYouLeftCompiler** hints inform surfacing only — no **WorldState** write from Presentation |

**Absent-proxy policy table (conceptual sample rows):**

| proxy_policy_id | allowed_intents | surfacing | max_duration_ticks |
|-----------------|-----------------|-----------|-------------------|
| `proxy_idle_guard` | patrol, ambient_dialogue | since_you_left_minor | 0 (until return) |
| `proxy_quest_steward` | quest_progress_local, faction_ping | since_you_left_major | bounded |
| `proxy_combat_stand_in` | defensive_only | combat_alert | short |

**Inputs / outputs:**

- *Into 4.3:* **PilotGraph** states + **PerspectiveEnvelope** (4.1); **DMRigPolicyMatrix**, **TransitionGuardRegistry**, **ModeTransitionGraph** edges (4.2); **SinceYouLeftCompiler** hints (3.2); **NarrativeDeltaVetoPolicy** may force dominate release (3.3)
- *Out of 4.3:* Phase 4 breadth glue complete; **AgencyPersistenceLedger** contract for Phase 5 spell metadata; factory catalog rows for agency + rail resume UX

## Interfaces

**Imports from Phase 4.1:**

| 4.1 export | How 4.3 consumes it |
|------------|---------------------|
| **PilotGraph** | Core state machine; glue extends with handoff coordinator |
| **PerspectiveEnvelope** | **AgencyEnvelope** specializes legal agency vs observe modes |
| **PresentationShell** | Glue hooks before/after rig activation |
| **ModeTransitionGraph** | Edge targets for handoff choreography |

**Imports from Phase 4.2:**

| 4.2 export | How 4.3 consumes it |
|------------|----------------------|
| **TransitionGuardRegistry** | Base stack; 4.3 appends **AgencyTransitionGuardExtension** |
| **DMRigPolicyMatrix** | `intent_eligible` informs **AgencyEnvelope** |
| **DMRailUXContract** | **RailStatePersistence** optional export |

**Imports from Phase 3:**

| Phase 3 export | How 4.3 consumes it |
|----------------|----------------------|
| **SinceYouLeftCompiler** (3.2) | Absent-proxy surfacing hints |
| **NarrativeDeltaVetoPolicy** (3.3) | May force dominate release or block proxy continuation |

**Exports to Phase 5+:**

| Export | Consumer |
|--------|----------|
| **AgencyPersistenceLedger** | Spell-bound victim / passenger_fp overlay metadata |
| **AgencyEnvelope** | Execution track mirror; catalog L5 agency rows |

**Adjacent slices:**

- **4.1** owns PilotGraph states; **4.3** owns cross-transition glue and persistence.
- **4.2** owns DM policy matrix; **4.3** layers agency guards without renaming `guard_id` vocabulary.

## Edge cases

- **Dominate release mid-interpolator:** **PilotHandoffCoordinator** waits for blend `handoff_complete` before clearing **DominateSessionBinding** — no dangling intent router target.
- **Proxy active + player returns during DMPauseGate:** Proxy intents frozen per 3.1; resume reconciles **PilotGraph** to `self` before FP edge fires.
- **Ledger checkpoint during hard freeze overwrite (3.3):** Export dominate binding for audit; live binding cleared when `overwrite_patch_compatible` blocks agency continuation.
- **Concurrent dominate command + DM rail:** Serialize through **PilotMachineryGlue** single-flight — second intent queues or rejects with `presentation.agency_busy`.
- **RailStatePersistence vs session-local:** Default session-local map annotations; operator may enable ledger export — not resolved on conceptual track.

## Open questions

- **Ledger storage scope (D-4.3-001):** Per-campaign vs per-save-slot — **Conceptual authority:** per-save-slot checkpoint lean; factory catalog attestation; execution track chooses serialization format (see [[decisions-log#Phase 4.3 open question anchors]]).
- **Proxy policy authority (D-4.3-002):** Static table vs runtime DM override — **Conceptual authority:** static **AbsentProxyPolicyTable** + DM session token for `proxy_quest_steward` only; no runtime matrix column mutation.
- **Dominate across scene load (D-4.3-003):** **AgencyPersistenceLedger** checkpoint required on cross-load dominate — serialization format deferred to execution track; conceptual contract named here.
- **Victim passenger_fp pairing (PMG):** Dominator branch documented; victim overlay deferred Phase 5 — **AgencyEnvelope** reserves `passenger_fp_overlay` hook without legal mode entry.

## Pseudo-code readiness

A reader can trace dominate command → **PilotHandoffCoordinator** staging → combined guard stack pass → DM WorldCam while binding persists → absent-proxy install on session away → ledger checkpoint → return release dominate before FP edge — without guessing agency vs observation separation or rail persistence. No API signatures on conceptual track.

## Research integration

Pattern alignment (no new pre-deepen research this run):

- Agency delegation persistence across camera/mode changes — aligns with 4.1 PilotGraph + 4.2 guard discipline
- Session-scoped intent routing — Phase 1.1 InputIntent canon gate
- Absent-player NPC proxy policies — 3.2 off-screen activity surfacing consumed read-only

## Responsibilities

- [x] Name AgencyEnvelope, PilotMachineryGlue, PilotHandoffCoordinator, AgencyPersistenceLedger
- [x] Document AgencyTransitionGuardExtension predicates building on 4.2 registry
- [x] DominateSessionBinding + AbsentProxyPolicyTable sample rows
- [x] Integration spine with 4.1 PilotGraph and 4.2 DMRigPolicyMatrix / TransitionGuardRegistry

## Tasks

- [x] Mint 4.3 secondary with agency envelope + pilot machinery glue
- [ ] Optional tertiaries: per-proxy-policy detail, ledger checkpoint format, handoff state diagram — deferred breadth-first
- [x] Phase 4 breadth complete — advance-phase gate passed 2026-06-26 (godo-followup-20260626T203800Z-phase4-advance); Phase 5.1 deepen next

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
