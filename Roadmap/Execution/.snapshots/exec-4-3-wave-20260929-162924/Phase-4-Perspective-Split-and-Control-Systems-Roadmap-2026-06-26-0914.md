---
title: Phase 4 — Perspective Split and Control Systems (Execution)
roadmap-level: primary
phase-number: 4
subphase-index: "4"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
status: active
priority: high
progress: 55
handoff_readiness: 74
updated: 2026-09-29
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-28
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-4
- perspective
- control-systems
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
catalog_row_ids:
- ux_camera_control_envelopes
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4 — Perspective Split and Control Systems (Execution)

Execution primary enrich (FAST map-gen): role-tailored views, Player FP envelope, DM mode graph, agency/pilot glue. Parallel spine under `Execution/Phase-4-Perspective-Split-and-Control-Systems/`. **No Half B. No L5.** Secondaries **4.1 / 4.2 / 4.3** next DFS.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Perspective envelopes + seamless mode transitions ([[conceptual Phase 4]]) |
| Inspiration (studied) | (1) Conceptual Phase 4 + 4.1–4.3. (2) Execution Phase-3 DMPauseGate / NarrativeDeltaVeto. (3) Phase-1.1 PresentationShell |
| L5 / package crosswalk | _(n/a — no L5)_ |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + primary pseudo for envelope modes + transition guards |
| Validation | **4.1** DFS minted (4.1+4.1.1–4.1.3); next **4.2**; nested V/IRA batch-later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | _(advisory)_ |
| `package_id` | _(Phase-4 TBD)_ |
| `l5_path` | `Roadmap/User-Story/scopes/ux_camera_control_envelopes/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual Phase 4 + 4.1–4.3 |
| `dispatch_scope` | Execution primary **Phase 4**; secondary **4.1** DFS closed this wave |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 4.1 | Player FP and Perspective Envelope | **minted** (+ 4.1.1–4.1.3) |
| 4.2 | DM Rigs and Mode Transition Graph | **next** |
| 4.3 | Agency Envelope and Pilot Machinery Glue | pending |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_camera_control_envelopes` |
| Label | Perspective and control envelopes can change and cleanly return |
| Seats | `player`, `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Perspective.ICameraRig` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | players get free third-person orbit as default; soft camera without hard restore |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_baseline_fp` | `Genesis.Perspective.ICameraRig` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `enter_exit_declare` | `Genesis.Perspective.ICameraRig` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `hard_restore` | `Genesis.Perspective.ICameraRig` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `dm_rail_first_class` | `Genesis.Perspective.ICameraRig` / leaf modules | wrong seat / out of contract | lasting readable residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.ICameraRig` |
| `stack-input-intent` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.ICameraRig` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.ICameraRig` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility | Owner secondary |
|--------|----------------|-----------------|
| `PerspectiveEnvelope` | Active view mode + InputIntent routing | 4.1 |
| `UnifiedSceneGraph` | Single scene ownership for cameras/rigs | 4.1 |
| `CameraInterpolatorRegistry` | Blend between FOV/rig endpoints | 4.1 |
| `PlayerFPRig` | First-person player presentation | 4.1 |
| `DMRigPolicyMatrix` | Allowed DM rigs per mode | 4.2 |
| `ModeTransitionGraph` | WorldCam ↔ MapCam ↔ SensoriumAttach | 4.2 |
| `TransitionGuardRegistry` | Block illegal transitions / overwrite veto | 4.2 |
| `AgencyEnvelope` | Dominate / absent-proxy bounds | 4.3 |
| `PilotMachineryGlue` | Pilot handoff coordinator | 4.3 |
| `AgencyPersistenceLedger` | Persist agency state across sessions | 4.3 |

## Interfaces

```text
enum PerspectiveMode { PLAYER_FP, WORLD_CAM, MAP_CAM, SENSORIUM_ATTACH, DM_RAIL }

InputIntent (RefCounted):
  + intent_id: StringName
  + source_mode: int
  + payload: Dictionary
  + to_dict() -> Dictionary

PerspectiveEnvelope (RefCounted):
  + mode() -> int
  + set_mode(mode: int, reason: StringName) -> Error
  + route_intent(intent: InputIntent) -> Error
  signals: mode_changed(from_mode, to_mode)

UnifiedSceneGraph (Node under Presentation — NOT Autoload world root):
  + attach_rig(rig_id: StringName, node: Node) -> Error
  + detach_rig(rig_id: StringName) -> Error

CameraInterpolatorRegistry (RefCounted):
  + blend(from_id: StringName, to_id: StringName, t: float) -> void
  signals: blend_complete(to_id)

DMRigPolicyMatrix (RefCounted):
  + allows(mode: int, rig_id: StringName) -> bool

ModeTransitionGraph (RefCounted):
  + can_transition(from_mode: int, to_mode: int) -> bool
  + next_edges(from_mode: int) -> Array

TransitionGuardRegistry (RefCounted):
  + check(from_mode: int, to_mode: int, context: Dictionary) -> Error
  # may consult Phase-3 OverwritePatchLayer / DMPauseGate

AgencyEnvelope (RefCounted):
  + dominate(target_id: StringName) -> Error
  + absent_proxy(target_id: StringName) -> Error
  signals: agency_changed(kind, target_id)

PilotMachineryGlue (RefCounted):
  + handoff(from_id: StringName, to_id: StringName) -> Error

AgencyPersistenceLedger (RefCounted):
  + record(event: Dictionary) -> Error
  + replay(session_id: StringName) -> Array
```

## Pseudo-code

```pseudo
# Phase 4 primary — Perspective split spine (Godot 4 stable).
# Citations: Node under Presentation; RefCounted policies; Error/OK; signals.
# Reject: Autoload camera as world authority; SensoriumAttach write into Simulation;
#         mode transition while TransitionGuardRegistry fails; inventing Phase-5 passenger_fp here.

class_name PerspectiveDirector
extends Node

signal mode_changed(from_mode, to_mode)

var _envelope: PerspectiveEnvelope
var _transitions: ModeTransitionGraph
var _guards: TransitionGuardRegistry
var _interp: CameraInterpolatorRegistry
var _pause_gate: RefCounted   # Phase-3 DMPauseGate (RO consult)

func request_mode(to_mode: int, reason: StringName) -> Error:
	var from_mode: int = _envelope.mode()
	if not _transitions.can_transition(from_mode, to_mode):
		return ERR_INVALID_PARAMETER
	var ctx := {"reason": reason, "dm_paused": false}
	if _pause_gate != null:
		ctx["dm_paused"] = _pause_gate.is_paused()
	var gerr := _guards.check(from_mode, to_mode, ctx)
	if gerr != OK:
		return gerr
	var err := _envelope.set_mode(to_mode, reason)
	if err != OK:
		return err
	_interp.blend(StringName(str(from_mode)), StringName(str(to_mode)), 0.0)
	mode_changed.emit(from_mode, to_mode)
	return OK

# Ordering: 4.1 envelope/scene → 4.2 DM rigs/graph → 4.3 agency/pilot ledger.
# Phase-3 NarrativeDeltaVeto / OverwritePatchLayer may veto via TransitionGuardRegistry.

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, stack-input-intent, engine-godot-463-dotnet | Catalog: ux_camera_control_envelopes | Type: Genesis.Perspective.ICameraRig

namespace Genesis;
// JUNIOR WORK-ORDER (ux_camera_control_envelopes): implement `Genesis.Perspective.ICameraRig` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
public interface ILeafContract { Error Execute(SeatContext seat); }

```

## Invariants

| ID | Rule |
|----|------|
| I-4-001 | PerspectiveDirector lives under Presentation — never Autoload Simulation root |
| I-4-002 | SensoriumAttach is read-only into Simulation WorldState |
| I-4-003 | Illegal ModeTransitionGraph edges rejected before CameraInterpolator blend |
| I-4-004 | TransitionGuardRegistry may block when Phase-3 DMPauseGate / overwrite veto fires |
| I-4-005 | Agency dominate during DM rail requires PilotMachineryGlue handoff (4.3) |

## Acceptance

- [x] Parallel spine path `Execution/Phase-4-…/` (primary)
- [x] Path-qualified `conceptual_counterpart` → frozen Phase 4
- [x] Module map + child index for 4.1 / 4.2 / 4.3
- [x] Interfaces + primary pseudo for PerspectiveDirector
- [x] Secondary **4.1** Player FP + tertiaries 4.1.1–4.1.3
- [ ] Secondary **4.2** DM Rigs next
- [ ] Half B / playable ladder later
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Given** seat context allowed for `ux_camera_control_envelopes`, **When** junior implements `Genesis.Perspective.ICameraRig`, **Then** wrong-seat calls return unauthorized / emit blocked — never silent OK
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_camera_control_envelopes` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Research integration

- Presentation-layer Node placement; WorldShell regen does not Autoload cameras.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Mint **4.2** DM Rigs and Mode Transition Graph (DFS).
2. Then **4.3**.

## Status

`deepen_complete: true` for Execution **Phase 4** primary; **4.1** DFS closed. Nested V/IRA skipped (operator batch-later). Next secondary **4.2**.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
