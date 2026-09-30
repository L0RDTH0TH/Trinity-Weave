---
title: Phase 4.3 — Agency Envelope and Pilot Machinery Glue (Execution)
roadmap-level: secondary
phase-number: 4
subphase-index: "4.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_agency_handoff_enter_exit
priority: high
progress: 70
handoff_readiness: 78
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
- agency
- pilot-glue
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_agency_handoff_enter_exit/L5]]'
- '[[ux_agency_handoff_enter_exit]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-2-Off-Screen-Faction-Tribe-Activity/Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.3 — Agency Envelope and Pilot Machinery Glue (Execution)

Execution secondary: **AgencyEnvelope** + **PilotMachineryGlue** join **PilotGraph** (4.1) to **DMRigPolicyMatrix** / **TransitionGuardRegistry** (4.2); persist dominate / absent-proxy across mode rails. Secondary: Agency envelope + pilot glue + persistence. **No Half B.** L5/SERIES are **read-only advisory feedstock** — AgencyEnvelope + PilotMachineryGlue bound agency (SELF/DOMINATE/ABSENT_PROXY); Sensorium never dominate without release; players do not author world from observe agency.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Agency envelope + pilot glue + persistence ([[conceptual 4.3]]) |
| Inspiration / L5 bar (advisory) | active_agency vs observe_only; dominate handoff guarded; AbsentProxy + rail persistence; SensoriumAttach + dominate without release refused |
| Inspiration (studied) | (1) Conceptual 4.3 + 4.3.1–4.3.3. (2) Execution 4.1 PilotGraph / 4.2 guards. (3) Phase-3.2 SinceYouLeft / 3.3 veto |
| L5 / package crosswalk | phase-aligned `[[ux_agency_handoff_enter_exit]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + secondary pseudo for glue → guards → envelope → ledger |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_agency_handoff_enter_exit` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_agency_handoff_enter_exit/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.3 + tertiaries 4.3.1–4.3.3 |
| `dispatch_scope` | Execution secondary **4.3** mint (FAST DFS wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 4.3.1 | AgencyEnvelope / Active Agency Modes | **minted** |
| 4.3.2 | PilotMachineryGlue / PilotHandoffCoordinator | **minted** |
| 4.3.3 | AgencyPersistenceLedger / AbsentProxy / RailState | **minted** |

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
| enter agency | `AgencyEnvelope.AssertEnter` | FP≠DM mismatch → Unauthorized | active agency mode |
| exit / release | AgencyEnvelope release path | dominate without release → reject | ledger exit row |
| pilot handoff | PilotHandoffCoordinator | missing handoff → Unconfigured | handoff receipt |
| persistence | AgencyPersistenceLedger | absent proxy without ledger → reject | rail state persisted |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.AgencyEnvelope` |
| `stack-input-intent` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.AgencyEnvelope` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.AgencyEnvelope` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility | Owner tertiary |
|--------|----------------|----------------|
| `AgencyEnvelope` | active_agency vs observe_only; InputIntent retarget | 4.3.1 |
| `PilotMachineryGlue` | Single-flight mode+agency orchestration | 4.3.2 |
| `PilotHandoffCoordinator` | Dominate handoff state machine | 4.3.2 |
| `DominateSessionBinding` | Target + envelope snapshot while dominate | 4.3.2 |
| `AgencyTransitionGuardExtension` | Extra predicates on 4.2 registry | 4.3.2 |
| `AgencyPersistenceLedger` | Checkpoint dominate/proxy/rail | 4.3.3 |
| `AbsentProxyPolicyTable` | Proxy intents while player away | 4.3.3 |
| `RailStatePersistence` | DM rail cursor (session-local default) | 4.3.3 |

## Interfaces

```text
# Imports from 4.1 / 4.2 / 3.x (RO consumers)
PilotGraph (RefCounted)                 # 4.1
PerspectiveEnvelope (RefCounted)        # 4.1.1
ModeTransitionGraph (RefCounted)        # 4.1.1
CameraInterpolatorRegistry (RefCounted) # 4.1.2
TransitionGuardRegistry (RefCounted)    # 4.2.1
DMRigPolicyMatrix (RefCounted)          # 4.2
DMRailUXContract (RefCounted)           # 4.2.3
NarrativeDeltaVetoPolicy (RefCounted)   # 3.3

enum AgencyClass { ACTIVE_SELF, ACTIVE_DOMINATE, OBSERVE_ONLY, ABSENT_PROXY }

AgencyEnvelope (RefCounted):
  + agency_class() -> int
  + set_agency(cls: int, target_id: StringName, reason: StringName) -> Error
  + classify_and_retarget(mode: int, hint: Dictionary) -> Error
  + legal_for_mode(mode: int, cls: int) -> bool
  + retarget_intent_router() -> Error
  signals: agency_changed(cls, target_id)

PilotMachineryGlue (RefCounted):
  + request_mode_with_agency(to_mode: int, reason: StringName, agency_hint: Dictionary) -> Error
  + is_busy() -> bool
  signals: agency_busy(), presentation_agency_changed(cls, target_id)

PilotHandoffCoordinator (RefCounted):
  + stage_dominate(target_id: StringName) -> Error
  + release_dominate(reason: StringName) -> Error
  + handoff_complete() -> bool
  + binding() -> DominateSessionBinding

AgencyPersistenceLedger (RefCounted):
  + append(event: Dictionary) -> Error
  + checkpoint(slot_id: StringName) -> Error
  + restore(slot_id: StringName) -> Error
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_agency_handoff_enter_exit L5 — advisory) ===
# Seats: illegal agency modes refuse — never invent DOMINATE on observe seats.
# Players do not author world: observe_only agency retargets/refuses world-author intents.
# DM rail vs player FP: glue coordinates mode+agency; FP vs DM rail stay distinct seats.
# Agency: SensoriumAttach + dominate without release refused; ledger owns persistence (4.3.3).
# ===========================================================

# 4.3 — Agency Envelope / Pilot Machinery Glue secondary (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals; Node under Presentation.
# Reject: Autoload agency authority; SensoriumAttach + dominate without release;
#         Camera3D ownership; passenger_fp (Phase 5); silent busy drops.

class_name PilotMachineryGlue
extends RefCounted

signal agency_busy()
signal presentation_agency_changed(cls, target_id)

var _pilot: PilotGraph
var _envelope: AgencyEnvelope
var _handoff: PilotHandoffCoordinator
var _guards: TransitionGuardRegistry
var _matrix: DMRigPolicyMatrix
var _graph: ModeTransitionGraph
var _interp: CameraInterpolatorRegistry
var _ledger: AgencyPersistenceLedger
var _dm_coord: Node
var _busy: bool = false

func is_busy() -> bool:
	return _busy

func request_mode_with_agency(to_mode: int, reason: StringName, agency_hint: Dictionary) -> Error:
	if _busy:
		agency_busy.emit()
		return ERR_BUSY
	_busy = true
	var from_mode: int = _envelope.mode()
	var pilot_state: StringName = _pilot.state()
	if agency_hint.get("dominate", false) or pilot_state == &"dominate":
		var herr := _handoff.stage_or_release(agency_hint)
		if herr != OK:
			_busy = false
			return herr
		if not _handoff.handoff_complete():
			_busy = false
			return ERR_BUSY
	var ctx := {
		"reason": reason,
		"pilot_state": pilot_state,
		"agency_hint": agency_hint,
		"binding": _handoff.binding_dict()
	}
	if not _graph.can_transition(from_mode, to_mode):
		_busy = false
		return ERR_INVALID_PARAMETER
	var gerr := _guards.evaluate(from_mode, to_mode, ctx)
	if gerr != OK:
		_busy = false
		return gerr
	var terr: Error
	if _is_dm_mode(to_mode):
		terr = _dm_coord.request_dm_mode(to_mode, reason)
	else:
		terr = _apply_fp_edge(to_mode, reason)
	if terr != OK:
		_busy = false
		return terr
	var aerr := _envelope.classify_and_retarget(to_mode, agency_hint)
	if aerr != OK:
		_busy = false
		return aerr
	_ledger.append({
		"edge": [from_mode, to_mode],
		"pilot_state": _pilot.state(),
		"binding_delta": _handoff.binding_dict(),
		"reason": reason
	})
	presentation_agency_changed.emit(_envelope.agency_class(), _envelope.target_id())
	_busy = false
	return OK

# Ordering: 4.3.1 envelope → 4.3.2 glue/handoff → 4.3.3 ledger/proxy/rail.
# Phase 5 consumes AgencyPersistenceLedger for passenger_fp metadata.

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, stack-input-intent, engine-godot-463-dotnet | Catalog: ux_agency_handoff_enter_exit | Type: Genesis.Agency.AgencyEnvelope

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
| I-4.3-001 | PilotMachineryGlue is single-flight — concurrent intents → `agency_busy` |
| I-4.3-002 | Dominate + SensoriumAttach requires dominate_release handoff first |
| I-4.3-003 | AgencyEnvelope never grants active_agency on observe_only DM modes without dominate |
| I-4.3-004 | AgencyTransitionGuardExtension appends to 4.2 stack — does not rename guard_ids |
| I-4.3-005 | Ledger append after successful transition; never before handoff_complete |
| I-4.3-006 | passenger_fp_overlay reserved hook only — Phase 5 owns legal mode |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine path `Execution/Phase-4-…/Phase-4-3-…/`
- [x] Path-qualified `conceptual_counterpart` → frozen 4.3
- [x] Child index 4.3.1–4.3.3
- [x] Interfaces + secondary pseudo for PilotMachineryGlue
- [x] Tertiaries 4.3.1–4.3.3 minted this wave
- [ ] Half B / playable ladder later
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `AgencyEnvelope` Assert/Handoff/Persist refuses wrong seat with `Unauthorized` and never silent OK — row `ux_agency_handoff_enter_exit`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** FP≠DM seat mismatch, **When** AgencyEnvelope.AssertEnter, **Then** Unauthorized
- [ ] **Given** dominate without release path, **When** exit attempted, **Then** reject and ledger holds prior mode
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Research integration

- Presentation-layer RefCounted glue; no Autoload agency authority.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Execution tree complete on disk for this node.
2. Batch validate / residual IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8`.


## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.3.1**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
