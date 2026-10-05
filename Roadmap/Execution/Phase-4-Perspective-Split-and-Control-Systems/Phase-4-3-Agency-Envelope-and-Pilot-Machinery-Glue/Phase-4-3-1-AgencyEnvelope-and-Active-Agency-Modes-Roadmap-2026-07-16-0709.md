---
title: Phase 4.3.1 — AgencyEnvelope and Active Agency Modes (Execution)
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.3.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_agency_handoff_enter_exit
priority: high
progress: 55
handoff_readiness: 74
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- paint_ux_catalog
- pkg_world_shell
- roadmap
- genesis-mythos-master
- phase-4
- agency-envelope
- active-agency
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_agency_handoff_enter_exit/L5]]'
- '[[ux_agency_handoff_enter_exit]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.3.1 — AgencyEnvelope and Active Agency Modes (Execution)

Execution tertiary: **AgencyEnvelope** specializes **PerspectiveEnvelope** — `active_agency` (`player_fp`, dominate) vs `observe_only` (DM rails). Tertiary: AgencyEnvelope + active agency modes. **No Half B.** L5/SERIES are **read-only advisory feedstock** — classify ACTIVE_SELF / ACTIVE_DOMINATE / OBSERVE; illegal dominate on observe-only without handoff → Error; players do not author world.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Agency class vs observe modes ([[conceptual 4.3.1]]) |
| Inspiration / L5 bar (advisory) | agency class vs observe modes; InputIntent retarget; illegal ACTIVE_DOMINATE on SensoriumAttach without handoff → Error |
| Inspiration (studied) | (1) Conceptual 4.3.1. (2) Execution 4.1.1 PerspectiveEnvelope. (3) 4.2 DMRigPolicyMatrix intent_eligible |
| L5 / package crosswalk | phase-aligned `[[ux_agency_handoff_enter_exit]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted envelope + InputIntent retarget; emit `agency_changed` |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_agency_handoff_enter_exit` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_agency_handoff_enter_exit/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.3.1 + rollup |
| `dispatch_scope` | Execution tertiary **4.3.1** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_agency_handoff_enter_exit` |
| Label | Agency handoff enter/exit with clean return |
| Seats | `player`, `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Agency.AgencyEnvelope` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | permanent dominate without exit; Sensorium as pilot |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| enter | `AgencyEnvelope.AssertEnter` | wrong seat → Unauthorized | ActiveAgencyModes |
| exit | `AgencyEnvelope.Release` | no release path → reject | mode cleared |
| mode set | ActiveAgencyModes registry | unknown mode → InvalidParameter | mode id |
| dominate | dominate flag | without release path → reject | hold |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.AgencyEnvelope` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.AgencyEnvelope` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `AgencyEnvelope` | Classify mode → agency class; retarget InputIntent |
| `AgencyClass` | ACTIVE_SELF / ACTIVE_DOMINATE / OBSERVE_ONLY / ABSENT_PROXY |
| `PassengerFpOverlayHook` | Reserved Phase-5 hook (no legal mode yet) |

## Interfaces

```text
enum AgencyClass { ACTIVE_SELF, ACTIVE_DOMINATE, OBSERVE_ONLY, ABSENT_PROXY }

AgencyEnvelope (RefCounted):
  + mode() -> int
  + agency_class() -> int
  + target_id() -> StringName
  + legal_for_mode(mode: int, cls: int) -> bool
  + set_mode(mode: int, reason: StringName) -> Error
  + set_agency(cls: int, target_id: StringName, reason: StringName) -> Error
  + classify_and_retarget(mode: int, hint: Dictionary) -> Error
  + retarget_intent_router() -> Error
  + passenger_fp_overlay_reserved() -> bool
  signals: agency_changed(cls, target_id), mode_changed(from_mode, to_mode)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_agency_handoff_enter_exit L5 — advisory) ===
# Seats: refuse ACTIVE_DOMINATE on observe-only without handoff path.
# Players do not author world: OBSERVE agency blocks world-author intents.
# DM rail vs player FP: classify from PerspectiveEnvelope mode — FP≠DM observe agency.
# Agency: ACTIVE_SELF / ACTIVE_DOMINATE / OBSERVE only — never invent classes.
# ===========================================================

# 4.3.1 — AgencyEnvelope + active agency modes (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
# Reject: PilotHandoffCoordinator (4.3.2); ledger/proxy (4.3.3); Camera3D;
#         granting ACTIVE_DOMINATE on SensoriumAttach without handoff path.

class_name AgencyEnvelope
extends RefCounted

signal agency_changed(cls, target_id)
signal mode_changed(from_mode, to_mode)

var _mode: int = 0
var _cls: int = AgencyClass.ACTIVE_SELF
var _target: StringName = &""
var _intent_router: RefCounted
var _perspective: RefCounted

func legal_for_mode(mode: int, cls: int) -> bool:
	if mode == PerspectiveMode.DM_SENSORIUM_ATTACH and cls == AgencyClass.ACTIVE_DOMINATE:
		return false
	if _is_dm_observe(mode) and cls == AgencyClass.ACTIVE_SELF:
		return false
	return true

func classify_and_retarget(mode: int, hint: Dictionary) -> Error:
	var want: int = int(hint.get("agency_class", _default_class_for(mode)))
	var tid: StringName = StringName(str(hint.get("target_id", "")))
	if not legal_for_mode(mode, want):
		return ERR_UNAUTHORIZED
	var merr := set_mode(mode, StringName(str(hint.get("reason", &"classify"))))
	if merr != OK:
		return merr
	var aerr := set_agency(want, tid, &"classify")
	if aerr != OK:
		return aerr
	return retarget_intent_router()

func set_agency(cls: int, target_id: StringName, reason: StringName) -> Error:
	if not legal_for_mode(_mode, cls):
		return ERR_UNAUTHORIZED
	_cls = cls
	_target = target_id
	agency_changed.emit(_cls, _target)
	return OK

func retarget_intent_router() -> Error:
	return _intent_router.retarget(_cls, _target)

func passenger_fp_overlay_reserved() -> bool:
	return true

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, engine-godot-463-dotnet | Catalog: ux_agency_handoff_enter_exit | Type: Genesis.Agency.AgencyEnvelope

// JUNIOR WORK-ORDER (ux_agency_handoff_enter_exit): implement `Genesis.Agency.AgencyEnvelope` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Agency;
// Index B3
public interface IAgencyEnvelope {
    Error AssertSeat(SeatContext seat, AgencyMode mode);
    Error Release(SeatContext seat);
    // Must-fail: wrong seat → Unauthorized; dominate without release → reject
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.3.1-001 | OBSERVE_ONLY modes never write Simulation via InputIntent |
| I-4.3.1-002 | ACTIVE_DOMINATE illegal on SensoriumAttach without handoff |
| I-4.3.1-003 | Agency class change emits `agency_changed` (never silent) |
| I-4.3.1-004 | passenger_fp_overlay is reserved — no PerspectiveMode entry in 4.3 |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-4-3 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 4.3.1
- [x] Interfaces + tertiary pseudo for AgencyEnvelope
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `AgencyEnvelope` Assert/Handoff/Persist refuses wrong seat with `Unauthorized` and never silent OK — row `ux_agency_handoff_enter_exit`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** wrong seat, **When** AgencyEnvelope.AssertEnter, **Then** Unauthorized
- [ ] **Given** unknown mode id, **When** ActiveAgencyModes set, **Then** InvalidParameter
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.3.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
