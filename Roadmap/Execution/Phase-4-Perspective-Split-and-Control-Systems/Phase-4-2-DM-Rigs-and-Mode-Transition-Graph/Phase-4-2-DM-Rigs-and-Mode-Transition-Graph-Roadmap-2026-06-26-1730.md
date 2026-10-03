---
title: Phase 4.2 — DM Rigs and Mode Transition Graph (Execution)
roadmap-level: secondary
phase-number: 4
subphase-index: "4.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_camera_control_envelopes
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
- dm-rigs
- mode-transition
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_camera_control_envelopes/L5]]'
- '[[ux_camera_control_envelopes]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.2 — DM Rigs and Mode Transition Graph (Execution)

Execution secondary: **DMRigPolicyMatrix** (WorldCam / MapCam / SensoriumAttach) + **TransitionGuardRegistry** refining 4.1 `ModeTransitionGraph`, plus DM rail chrome and map-annotation envelope. Secondary: DM rigs + mode transition graph. **No Half B.** L5/SERIES are **read-only advisory feedstock** — TransitionGuardRegistry + map annotations + rail chrome enable **DM rail vs player FP** without silent guard fails or player world-author. AgencyEnvelope → **4.3**.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | DM rig matrix + guard stack + rail UX ([[conceptual 4.2]]) |
| Inspiration / L5 bar (advisory) | FP↔DM guarded transitions; map marks session-local; rail chrome non-silent blocked_reason; players never world-author from DM seats |
| Inspiration (studied) | (1) Conceptual 4.2 + 4.2.1–4.2.3. (2) Execution 4.1 PlayerPerspectiveController. (3) Phase-3.1 DMPauseGate / 3.3 veto+overwrite |
| L5 / package crosswalk | phase-aligned `[[ux_camera_control_envelopes]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + secondary pseudo for guard → deactivate → blend → matrix overlays → envelope |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_camera_control_envelopes` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_camera_control_envelopes/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.2 + tertiaries 4.2.1–4.2.3 |
| `dispatch_scope` | Execution secondary **4.2** mint (FAST DFS wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 4.2.1 | TransitionGuardRegistry / DM Session Authority | **minted** |
| 4.2.2 | Map Annotation Envelope | **minted** |
| 4.2.3 | DM Rail Chrome / DMRailUXContract | **minted** |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_camera_control_envelopes` |
| Label | Perspective and control envelopes can change and cleanly return |
| Seats | `player`, `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Perspective.DmRigHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | players get free third-person orbit as default; soft camera without hard restore |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `dm_rail_first_class` | `DMRigPolicyMatrix` + DMRailUXContract | player on DM rail → Unauthorized | rail chrome state |
| enter/exit declare | ModeTransitionGraph + TransitionGuardRegistry | freeze/pause → Busy | mode attested |
| map annotations | MapAnnotationEnvelope | CanonGate reject invent | annotation marks |
| hard restore | GuardDMSessionAuthority | fail → prior mode | camera restored |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.DmRigHost` |
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.DmRigHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.DmRigHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility | Owner tertiary |
|--------|----------------|----------------|
| `DMRigPolicyMatrix` | Per-mode overlay / RO projection policy rows | 4.2 (secondary) |
| `TransitionGuardRegistry` | Ordered first-failing guard stack | 4.2.1 |
| `DMSessionAuthority` | FP↔DM authority + freeze-compatible RO | 4.2.1 |
| `MapAnnotationEnvelope` | Presentation-local map pins (never WorldState) | 4.2.2 |
| `DMRailUXContract` | Rail chrome order + blocked_reason messaging | 4.2.3 |
| `ModeTransitionGraph` | Consume 4.1 edges (refine, do not fork) | 4.1 import |

## Interfaces

```text
# Imports from 4.1 / 3.x (RO consumers)
PerspectiveMode  # enum from 4.1.1
ModeTransitionGraph (RefCounted)  # 4.1.1
CameraInterpolatorRegistry (RefCounted)  # 4.1.2
UnifiedSceneGraph (Node)  # 4.1.2
DMPauseGate (RefCounted)  # 3.1
NarrativeDeltaVetoPolicy (RefCounted)  # 3.3
OverwritePatchLayer (RefCounted)  # 3.3

DMRigPolicyRow (RefCounted):
  + mode: int
  + rig_id: StringName
  + observe_only: bool
  + overlay_tags: PackedStringArray
  + worldstate_writes: bool  # must be false for DM observe modes

DMRigPolicyMatrix (RefCounted):
  + row_for(mode: int) -> DMRigPolicyRow
  + apply_overlays(mode: int, scene: Node) -> Error
  + clear_overlays(mode: int, scene: Node) -> Error

TransitionGuardRegistry (RefCounted):
  + evaluate(from_mode: int, to_mode: int, ctx: Dictionary) -> Error
  + last_blocked_guard_id() -> StringName
  signals: transition_blocked(guard_id, from_mode, to_mode)

DMRailUXContract (RefCounted):
  + rail_order() -> Array  # PerspectiveMode ints
  + show_blocked(guard_id: StringName, reason: String) -> void
  + request_mode_switch(to_mode: int) -> Error

MapAnnotationEnvelope (RefCounted):
  + add_local(mark: Dictionary) -> Error
  + clear_session() -> void
  + is_sim_mutating(mark: Dictionary) -> bool
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_camera_control_envelopes L5 — advisory) ===
# Seats: illegal FP↔DM edges refuse via TransitionGuardRegistry (4.2.1).
# Players do not author world: DM observe + map annotations are Presentation-local.
# DM rail vs player FP: coordinator routes only after guards; chrome surfaces blocked_reason.
# Agency: bounds deferred to AgencyEnvelope (4.3) — do not invent dominate here.
# ===========================================================

# 4.2 — DM Rigs / Mode Transition Graph secondary (Godot 4 stable).
# Citations: Node under Presentation; RefCounted policies; Error/OK; StringName; signals.
# Reject: Autoload camera authority; SensoriumAttach WorldState writes; silent guard fails;
#         Camera3D/SubViewport ownership here (exec-deferred); AgencyEnvelope (4.3).

class_name DMPerspectiveCoordinator
extends Node

signal presentation_mode_changed(from_mode, to_mode)
signal presentation_transition_blocked(guard_id, from_mode, to_mode)

var _graph: ModeTransitionGraph          # 4.1
var _guards: TransitionGuardRegistry     # 4.2.1
var _matrix: DMRigPolicyMatrix
var _scene: UnifiedSceneGraph            # 4.1.2
var _interp: CameraInterpolatorRegistry  # 4.1.2
var _rail: DMRailUXContract              # 4.2.3
var _annotations: MapAnnotationEnvelope  # 4.2.2
var _envelope: RefCounted                # PerspectiveEnvelope 4.1.1

func request_dm_mode(to_mode: int, reason: StringName) -> Error:
	var from_mode: int = _envelope.mode()
	if not _graph.can_transition(from_mode, to_mode):
		return ERR_INVALID_PARAMETER
	var gerr := _guards.evaluate(from_mode, to_mode, {"reason": reason})
	if gerr != OK:
		var gid: StringName = _guards.last_blocked_guard_id()
		_rail.show_blocked(gid, str(gid))
		presentation_transition_blocked.emit(gid, from_mode, to_mode)
		return gerr
	var from_rig: StringName = _scene.active_rig_id()
	var row: DMRigPolicyRow = _matrix.row_for(to_mode)
	if row.worldstate_writes:
		return ERR_UNAUTHORIZED
	_matrix.clear_overlays(from_mode, _scene)
	var berr := _interp.blend(from_rig, row.rig_id, &"ease_default")
	if berr != OK:
		return berr
	var aerr := _scene.set_active_rig(row.rig_id)
	if aerr != OK:
		return aerr
	var oerr := _matrix.apply_overlays(to_mode, _scene)
	if oerr != OK:
		return oerr
	var eerr := _envelope.set_mode(to_mode, reason)
	if eerr != OK:
		return eerr
	presentation_mode_changed.emit(from_mode, to_mode)
	return OK

# Ordering: 4.2.1 guards → 4.2.2 map annotations → 4.2.3 rail chrome.
# 4.3 owns AgencyEnvelope + PilotMachineryGlue + persistence.

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, stack-ui-hosts, engine-godot-463-dotnet | Catalog: ux_camera_control_envelopes | Type: Genesis.Perspective.DmRigHost

// JUNIOR WORK-ORDER (ux_camera_control_envelopes): implement `Genesis.Perspective.DmRigHost` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Perspective;
// Index B3 — DM cam via ICameraRig
public interface IDmRigHost : ICameraRig {
    // Activate(PerspectiveMode, SeatContext); player on DM rail → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.2-001 | DMPerspectiveCoordinator lives under Presentation — never Autoload Simulation |
| I-4.2-002 | TransitionGuardRegistry first-failing; never silent noop on block |
| I-4.2-003 | DM observe modes: `worldstate_writes == false` |
| I-4.2-004 | MapAnnotationEnvelope rejects sim-mutating marks (canon gate) |
| I-4.2-005 | Mode edges still require ModeTransitionGraph.can_transition (4.1) |
| I-4.2-006 | SensoriumAttach never dominate / never write Simulation |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine path `Execution/Phase-4-…/Phase-4-2-…/`
- [x] Path-qualified `conceptual_counterpart` → frozen 4.2
- [x] Child index 4.2.1–4.2.3
- [x] Interfaces + secondary pseudo for DMPerspectiveCoordinator
- [x] Tertiaries 4.2.1–4.2.3 minted this wave
- [ ] Half B / playable ladder later
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `DmRigHost.Activate(mode, seat)` returns `Error.Unauthorized` when seat mismatches rail (player on DM WorldCam/MapCam; never bare OK) — row `ux_camera_control_envelopes`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player on DM rail, **When** DMRigPolicyMatrix apply, **Then** Unauthorized
- [ ] **Given** TransitionGuardRegistry fail, **When** mode switch, **Then** Busy/Unauthorized and hard restore prior mode
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Research integration

- Presentation-layer Node placement; camera/rigs are not Autoload world roots.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Tertiaries **4.2.1–4.2.3** complete this wave.
2. Next secondary **4.3** Agency Envelope and Pilot Machinery Glue.

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.2.1**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
