---
title: Phase 4.3.1 — AgencyEnvelope and Active Agency Modes (Roll-up)
roadmap-level: rollup
phase-number: 4
subphase-index: "4.3.1"
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags: [roadmap, rollup, genesis-mythos-master, phase-4, agency-envelope]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]"
  - "[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]"
---

# Phase 4.3.1 roll-up — AgencyEnvelope / active agency modes

Canonical compact tertiary: [[Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]. Detail preserved off the ≤1400 feedstock body (`followup-deepen-phase431-tertiary-20260716T110555Z`).

## Purpose

Name the **AgencyEnvelope** as the session contract that decides whether the current presentation mode may carry **active_agency** or is **observe_only**, without owning handoff choreography or persistence (siblings).

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **AgencyEnvelope** | Superset of **PerspectiveEnvelope**: legal agency class per mode |
| `active_agency` | Modes that may own InputIntent (`player_fp`, dominate-possessed target) |
| `observe_only` | All DM rails (WorldCam / MapCam / SensoriumAttach) — no dominate without handoff path |
| `agency_class` | Result of envelope classify after a mode pass |
| `passenger_fp_overlay` | Reserved hook for Phase 5 victim overlay — not a legal mode entry here |

**Out:** PilotMachineryGlue / PilotHandoffCoordinator (`4.3.2`); AgencyPersistenceLedger / AbsentProxyPolicyTable / RailStatePersistence (`4.3.3`); Camera3D; serializers; factory/L5; execution pins.

## Behavior detail

1. Mode-switch or dominate request reaches Presentation (after 4.2 guards when applicable).
2. **AgencyEnvelope** reads target mode + PilotGraph agency intent.
3. Classify: `active_agency` vs `observe_only`.
4. Illegal: dominate / active_agency on observe-only without an explicit handoff path → reject (chrome may surface via 4.2.3).
5. Legal pass: update envelope; InputIntent router retargets per 1.1; emit `presentation.agency_changed`.
6. Dominate + WorldCam: **allowed** — envelope keeps dominate binding; DM rail stays observe_only for the camera, agency remains on possessed target (binding owned by sibling glue).

## Edge cases

- **SensoriumAttach + dominate:** Blocked unless release/handoff staged (4.3.2 owns choreography; envelope only declares illegality).
- **FP return while dominate active:** Envelope expects release before `player_fp` reclaim — glue clears binding first.
- **Concurrent classify vs rail chrome:** Envelope does not own `blocked_reason` copy; it supplies agency-class reject reason ids only.
- **passenger_fp_overlay:** Named reservation only — no legal mode table row in 4.3.1.

## Open questions

- **Observe-only intent bleed:** Whether any DM rail may ever hold limited agency (e.g. annotation-only) — lean no; annotations stay 4.2.2 intent class.
- **Envelope snapshot granularity:** Full PerspectiveEnvelope clone vs agency-class delta — deferred to 4.3.3 ledger.

## Handoff criteria

- [x] AgencyEnvelope noun + active_agency / observe_only named
- [x] Dominate legality vs observe-only / SensoriumAttach without handoff explicit
- [x] Exports pointed at 4.3.2 glue + Phase 5 hook
- [x] Next DFS pointed (`4.3.2` PilotMachineryGlue / PilotHandoffCoordinator)

**80%** handoff_readiness — implementer can classify agency vs observe without guessing Sensorium+dominate. Slice feed **green** `1158≤1200`. Project harness **red** `project_RED:5.1.1:1415>1200` (4.3.2 cleared 1189≤1200).
