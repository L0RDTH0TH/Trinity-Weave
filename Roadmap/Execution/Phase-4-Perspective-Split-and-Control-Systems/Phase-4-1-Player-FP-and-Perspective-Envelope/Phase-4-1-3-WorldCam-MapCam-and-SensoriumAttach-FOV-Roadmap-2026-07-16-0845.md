---
title: Phase 4.1.3 — WorldCam / MapCam / SensoriumAttach FOV (Execution)
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_dm_worldcam
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
- worldcam
- mapcam
- sensorium-attach
- fov
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_dm_worldcam/L5]]'
- '[[ux_dm_worldcam]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.1.3 — WorldCam / MapCam / SensoriumAttach FOV (Execution)

Execution tertiary: per-rig **FOV contracts** for **WorldCam** (DM tactical RO), **MapCam** (strategic overlays), **SensoriumAttach** (entity sensorium RO — never dominate). Parallel spine under Phase-4-1. **No Half B.** L5/SERIES are **read-only advisory feedstock** — WorldCam/MapCam/SensoriumAttach FOV contracts enable DM observe seats; SensoriumAttach **never** dominates; players do not author world from observe FOVs.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | DM FOV nouns + RO/sensorium non-dominate ([[conceptual 4.1.3]]) |
| Inspiration / L5 bar (advisory) | DM observe FOV nouns; SensoriumAttach never dominate/WorldState write; ObserveOnlyIntentGate blocks non-mode-switch; FP≠DM rail FOV |
| Inspiration (studied) | (1) Conceptual 4.1.3. (2) Execution 4.1.1 / 4.1.2. (3) Phase-3.1 tick RO |
| L5 / package crosswalk | phase-aligned `[[ux_dm_worldcam]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | C# / .NET (Godot 4.6.3) PerspectiveAnchor rigs + FOVContract + RO intent gate |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_dm_worldcam` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_dm_worldcam/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.1.3 + rollup |
| `dispatch_scope` | Execution tertiary **4.1.3** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_dm_worldcam` |
| Label | Free-flight DM observation rail (WorldCam / Sparky) |
| Seats | `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Perspective.SparkyDmFreeCamRig` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | players use WorldCam; Sensorium transfers intent; MapCam==tilted WorldCam |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| DM WorldCam activate | `ICameraRig.Activate(DmWorldCam)` | player seat → Unauthorized | Current camera |
| MapCam ortho | MapCamRig plane-locked | not tilted WorldCam | ortho view |
| Sensorium attach | SensoriumAttach observe-only | no DOMINATE / no WorldState write | FOV contract |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.SparkyDmFreeCamRig` |
| `stack-vtt-overlays` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.SparkyDmFreeCamRig` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.SparkyDmFreeCamRig` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `FOVContract` | Named FOV degrees + clip + overlay flags |
| `WorldCamRig` | `&"world_cam_rig"` — DM tactical overview |
| `MapCamRig` | `&"map_cam_rig"` — strategic map + overlays |
| `SensoriumAttachRig` | `&"sensorium_attach_rig"` — entity RO sensorium |
| `ObserveOnlyIntentGate` | Ban non-mode-switch InputIntent on these modes |

## Interfaces

```text
FOVContract (RefCounted):
  + fov_degrees: float
  + near_m: float
  + far_m: float
  + overlay_flags: PackedStringArray
  + to_dict() -> Dictionary

WorldCamRig (Node / PerspectiveAnchor):
  + rig_id() -> StringName  # &"world_cam_rig"
  + fov_contract() -> FOVContract
  + activate() -> Error
  + deactivate() -> Error
  + bind_worldstate_ro(snapshot: Dictionary) -> Error

MapCamRig (Node / PerspectiveAnchor):
  + rig_id() -> StringName  # &"map_cam_rig"
  + fov_contract() -> FOVContract
  + set_overlays(flags: PackedStringArray) -> Error
  + activate() -> Error
  + deactivate() -> Error

SensoriumAttachRig (Node / PerspectiveAnchor):
  + rig_id() -> StringName  # &"sensorium_attach_rig"
  + fov_contract() -> FOVContract
  + attach_entity(entity_id: StringName) -> Error
  + activate() -> Error
  + deactivate() -> Error
  # NEVER writes Simulation; NEVER PilotAgencyKind.DOMINATE

ObserveOnlyIntentGate (RefCounted):
  + allow(intent_id: StringName, mode: int) -> bool
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_dm_worldcam L5 — advisory) ===
# Seats: WorldCam/MapCam/Sensorium = observe FOV — not world-author.
# Players do not author world: ObserveOnlyIntentGate blocks non-mode_switch intents.
# DM rail vs player FP: FOVContract binds DM cams; PlayerFPRig FOV stays FP-owned (4.1.2).
# Agency: SensoriumAttach NEVER dominates / writes WorldState.
# ===========================================================

# 4.1.3 — WorldCam / MapCam / SensoriumAttach FOV (Godot 4 stable).
# Citations: Node under UnifiedSceneGraph; RefCounted FOVContract; PackedStringArray; Error/OK.
# Reject: Camera3D as Simulation Autoload; SensoriumAttach dominate / WorldState write;
#         non-mode-switch InputIntent while observe mode active; passenger_fp (P5).

class_name FOVContract
extends RefCounted

var fov_degrees: float = 70.0
var near_m: float = 0.05
var far_m: float = 4000.0
var overlay_flags: PackedStringArray = PackedStringArray()

func to_dict() -> Dictionary:
	return {
		"fov_degrees": fov_degrees,
		"near_m": near_m,
		"far_m": far_m,
		"overlay_flags": Array(overlay_flags),
	}

class_name ObserveOnlyIntentGate
extends RefCounted

func allow(intent_id: StringName, mode: int) -> bool:
	# DM_WORLD / DM_MAP / DM_SENSORIUM_ATTACH
	return intent_id == &"mode_switch"

class_name WorldCamRig
extends Node

var _fov: FOVContract = FOVContract.new()
var _world_ro: Dictionary = {}

func _init() -> void:
	_fov.fov_degrees = 65.0
	_fov.far_m = 8000.0

func rig_id() -> StringName:
	return &"world_cam_rig"

func fov_contract() -> FOVContract:
	return _fov

func bind_worldstate_ro(snapshot: Dictionary) -> Error:
	_world_ro = snapshot.duplicate(true)  # RO copy — never mutate Simulation
	return OK

func activate(mode: int, seat: SeatContext) -> Error:
	# ICameraRig posture — Index B3: player on DM rail → Unauthorized
	if not seat.allows_dm_rail() and (mode == PerspectiveMode.DM_WORLD or mode == PerspectiveMode.DM_MAP or mode == PerspectiveMode.DM_SENSORIUM_ATTACH):
		return ERR_UNAUTHORIZED
	# apply _fov to camera leaf under this rig; Presentation only
	return OK

func deactivate() -> Error:
	_world_ro.clear()
	return OK

class_name MapCamRig
extends Node

var _fov: FOVContract = FOVContract.new()

func _init() -> void:
	_fov.fov_degrees = 55.0
	_fov.overlay_flags = PackedStringArray(["faction", "terrain"])

func rig_id() -> StringName:
	return &"map_cam_rig"

func set_overlays(flags: PackedStringArray) -> Error:
	_fov.overlay_flags = flags
	return OK

func activate(mode: int, seat: SeatContext) -> Error:
	# ICameraRig — player seat cannot Activate DM MapCam
	if not seat.allows_dm_rail() and mode == PerspectiveMode.DM_MAP:
		return ERR_UNAUTHORIZED
	return OK

func deactivate() -> Error:
	return OK

class_name SensoriumAttachRig
extends Node

var _fov: FOVContract = FOVContract.new()
var _entity_id: StringName = &""

func _init() -> void:
	_fov.fov_degrees = 80.0
	_fov.near_m = 0.02
	_fov.far_m = 120.0

func rig_id() -> StringName:
	return &"sensorium_attach_rig"

func attach_entity(entity_id: StringName) -> Error:
	if entity_id == &"":
		return ERR_INVALID_PARAMETER
	_entity_id = entity_id
	return OK

func activate(mode: int, seat: SeatContext) -> Error:
	# RO sensorium — PilotGraph must stay SELF (4.1.1); player invent → Unauthorized
	if not seat.allows_dm_rail() and mode == PerspectiveMode.DM_SENSORIUM_ATTACH:
		return ERR_UNAUTHORIZED
	return OK

func deactivate() -> Error:
	_entity_id = &""
	return OK

# Activation order (caller): 4.1.1 guards → 4.1.2 deactivate/blend/activate → apply FOV here.

# === WEAVE C# / .NET (Godot 4.6.3) — ICameraRig / Sparky ===
# Manifest: stack-perspective-camera, stack-vtt-overlays, engine-godot-463-dotnet | Catalog: ux_dm_worldcam

namespace Genesis.Perspective;

public interface ICameraRig {
    StringName RigId { get; }
    Error Activate(PerspectiveMode mode, SeatContext seat);
    void ApplyFov(FovContract contract);
}

public sealed partial class SparkyDmFreeCamRig : Node3D, ICameraRig {
    // JUNIOR WORK-ORDER (ux_dm_worldcam): players NEVER Activate WorldCam rail
    // ACCEPT: dm_as_player → Current=true; player seat → Error.Unauthorized
    // VERIFY: MapCamRig separate orthographic plane-locked — not tilted WorldCam
    public StringName RigId => new StringName("world_cam_rig");
    private Camera3D _cam = null!;
    public Error Activate(PerspectiveMode mode, SeatContext seat) {
        if (!seat.AllowsDmRail()) return Error.Unauthorized;
        _cam.Current = true;
        ApplyFov(FovContract.For(mode));
        return Error.Ok;
    }
    public void ApplyFov(FovContract contract) => _cam.Fov = contract.Degrees;
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.1.3-001 | WorldCam / MapCam / SensoriumAttach are observe-only for InputIntent (except mode_switch) |
| I-4.1.3-002 | SensoriumAttach never writes Simulation WorldState |
| I-4.1.3-003 | SensoriumAttach never implies PilotAgencyKind.DOMINATE |
| I-4.1.3-004 | FOV applied only after UnifiedSceneGraph.set_active_rig succeeds |
| I-4.1.3-005 | Camera3D leaf ownership stays under Presentation / UnifiedSceneGraph |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine path under Phase-4-1
- [x] Path-qualified conceptual_counterpart
- [x] Interfaces + pseudo for three FOV rigs + ObserveOnlyIntentGate
- [x] 4.1 tertiary wave complete
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `SparkyDmFreeCamRig.Activate(mode, seat)` returns `Error.Unauthorized` when seat mismatches rail (player on DM WorldCam/MapCam; never bare OK) — row `ux_dm_worldcam`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player seat, **When** ICameraRig.Activate(DmWorldCam), **Then** Unauthorized — Current camera unchanged
- [ ] **Given** SensoriumAttach, **When** DOMINATE or WorldState write attempted, **Then** reject (observe-only)
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
