---
title: Phase 4.3.2 — PilotMachineryGlue and PilotHandoffCoordinator (Execution)
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.3.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roadmap-2026-07-16-0729]]'
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
- pilot-glue
- handoff-coordinator
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_agency_handoff_enter_exit/L5]]'
- '[[ux_agency_handoff_enter_exit]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roadmap-2026-07-16-0729]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.3.2 — PilotMachineryGlue and PilotHandoffCoordinator (Execution)

Execution tertiary: **PilotMachineryGlue** single-flight orchestration; **PilotHandoffCoordinator** dominate state machine; **AgencyTransitionGuardExtension** on 4.2 registry. Tertiary: PilotMachineryGlue + PilotHandoffCoordinator. **No Half B.** L5/SERIES are **read-only advisory feedstock** — guarded dominate handoff; wait blend before intent swap; never clear binding mid-interpolator; agency bounds enforced.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Glue + dominate handoff ([[conceptual 4.3.2]]) |
| Inspiration / L5 bar (advisory) | idle→pending→active→release; first-failing agency guards; never clear DominateSessionBinding before handoff_complete |
| Inspiration (studied) | (1) Conceptual 4.3.2. (2) Execution 4.3.1 / 4.2.1 guards. (3) 4.1.2 interpolator |
| L5 / package crosswalk | phase-aligned `[[ux_agency_handoff_enter_exit]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted coordinator + guard predicates; wait blend before intent swap |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_agency_handoff_enter_exit` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_agency_handoff_enter_exit/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.3.2 + rollup |
| `dispatch_scope` | Execution tertiary **4.3.2** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_agency_handoff_enter_exit` |
| Label | Agency handoff enter/exit with clean return |
| Seats | `player`, `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Agency.PilotMachineryGlue` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | permanent dominate without exit; Sensorium as pilot |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| handoff request | `PilotHandoffCoordinator.Request` | wrong seat → Unauthorized | handoff ticket |
| glue bind | `PilotMachineryGlue` | missing pilot → Unconfigured | binding |
| complete handoff | Coordinator.Complete | incomplete → Busy | receipt |
| agency envelope | must call envelope assert | bypass envelope → Unauthorized | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.PilotMachineryGlue` |
| `stack-input-intent` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.PilotMachineryGlue` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.PilotMachineryGlue` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `PilotMachineryGlue` | Single entry mode+agency; busy gate |
| `PilotHandoffCoordinator` | idle→pending→active→release→idle |
| `DominateSessionBinding` | `{target_entity_id, source_rig_id, envelope_snapshot}` |
| `AgencyTransitionGuardExtension` | agency_envelope_legal / dominate_compatible / proxy_active / handoff_complete |

## Interfaces

```text
const GUARD_AGENCY_ENVELOPE_LEGAL := &"agency_envelope_legal"
const GUARD_DOMINATE_COMPATIBLE := &"dominate_compatible"
const GUARD_PROXY_ACTIVE := &"proxy_active"
const GUARD_HANDOFF_COMPLETE := &"handoff_complete"

enum HandoffState { IDLE, DOMINATE_PENDING, DOMINATE_ACTIVE, DOMINATE_RELEASE }

DominateSessionBinding (RefCounted):
  + target_entity_id: StringName
  + source_rig_id: StringName
  + envelope_snapshot: Dictionary
  + to_dict() -> Dictionary
  + clear() -> void

PilotHandoffCoordinator (RefCounted):
  + state() -> int
  + stage_dominate(target_id: StringName, source_rig: StringName) -> Error
  + release_dominate(reason: StringName) -> Error
  + on_blend_complete(to_id: StringName) -> void
  + handoff_complete() -> bool
  + binding() -> DominateSessionBinding
  signals: handoff_state_changed(from_state, to_state)

AgencyTransitionGuardExtension (RefCounted):
  + install_on(registry: TransitionGuardRegistry) -> void
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_agency_handoff_enter_exit L5 — advisory) ===
# Seats: agency_envelope_legal / dominate_compatible / proxy_active / handoff_complete.
# Players do not author world: handoff SM never grants WorldState write.
# DM rail vs player FP: glue single-entry mode+agency; busy gate blocks illegal swaps.
# Agency: never clear DominateSessionBinding before interpolator handoff_complete.
# ===========================================================

# 4.3.2 — PilotHandoffCoordinator + AgencyTransitionGuardExtension (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
# Reject: AgencyEnvelope classify (4.3.1); ledger/proxy (4.3.3); Camera3D;
#         clearing DominateSessionBinding before blend handoff_complete.

class_name PilotHandoffCoordinator
extends RefCounted

signal handoff_state_changed(from_state, to_state)

var _state: int = HandoffState.IDLE
var _binding: DominateSessionBinding = DominateSessionBinding.new()
var _awaiting_blend: bool = false
var _interp: CameraInterpolatorRegistry

func handoff_complete() -> bool:
	return not _awaiting_blend and _state != HandoffState.DOMINATE_PENDING \
		and _state != HandoffState.DOMINATE_RELEASE

func stage_dominate(target_id: StringName, source_rig: StringName) -> Error:
	if _state != HandoffState.IDLE and _state != HandoffState.DOMINATE_ACTIVE:
		return ERR_BUSY
	var prev: int = _state
	_state = HandoffState.DOMINATE_PENDING
	_binding.target_entity_id = target_id
	_binding.source_rig_id = source_rig
	_awaiting_blend = true
	handoff_state_changed.emit(prev, _state)
	return OK

func on_blend_complete(to_id: StringName) -> void:
	if not _awaiting_blend:
		return
	_awaiting_blend = false
	var prev: int = _state
	if _state == HandoffState.DOMINATE_PENDING:
		_state = HandoffState.DOMINATE_ACTIVE
	elif _state == HandoffState.DOMINATE_RELEASE:
		_binding.clear()
		_state = HandoffState.IDLE
	handoff_state_changed.emit(prev, _state)

func release_dominate(reason: StringName) -> Error:
	if _state != HandoffState.DOMINATE_ACTIVE:
		return ERR_INVALID_PARAMETER
	var prev: int = _state
	_state = HandoffState.DOMINATE_RELEASE
	_awaiting_blend = true
	handoff_state_changed.emit(prev, _state)
	return OK

# AgencyTransitionGuardExtension.install_on: register
# agency_envelope_legal, dominate_compatible, proxy_active, handoff_complete
# AFTER 4.2.1 default stack — first failing wins.

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, stack-input-intent, engine-godot-463-dotnet | Catalog: ux_agency_handoff_enter_exit | Type: Genesis.Agency.PilotMachineryGlue

// JUNIOR WORK-ORDER (ux_agency_handoff_enter_exit): implement `Genesis.Agency.PilotMachineryGlue` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Agency;
// Index B3 — PilotHandoff
public interface IPilotMachineryGlue {
    Error Handoff(PilotGraph graph, SeatContext seat);
    // Must-fail: wrong seat → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.3.2-001 | Single-flight glue — second intent → ERR_BUSY / agency_busy |
| I-4.3.2-002 | Never clear DominateSessionBinding while `_awaiting_blend` |
| I-4.3.2-003 | Agency guards append after 4.2 stack — first failing wins |
| I-4.3.2-004 | SensoriumAttach while dominate → blocked unless release staged |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-4-3 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 4.3.2
- [x] Interfaces + tertiary pseudo for handoff + guard extension
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `PilotMachineryGlue` Assert/Handoff/Persist refuses wrong seat with `Unauthorized` and never silent OK — row `ux_agency_handoff_enter_exit`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** missing pilot, **When** PilotMachineryGlue bind, **Then** Unconfigured
- [ ] **Given** handoff bypassing AgencyEnvelope assert, **When** Complete, **Then** Unauthorized
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.3.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
