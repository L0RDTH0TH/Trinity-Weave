---
title: Phase 4 — Perspective Split and Control Systems (Execution)
roadmap-level: primary
phase-number: 4
subphase-index: "4"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_camera_control_envelopes
priority: high
progress: 85
handoff_readiness: 80
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
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[ux_camera_control_envelopes]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_camera_control_envelopes/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4 — Perspective Split and Control Systems (Execution)

Execution primary: role-tailored views, Player FP envelope, DM mode graph, agency/pilot glue. Parallel spine under `Execution/Phase-4-Perspective-Split-and-Control-Systems/`. **No Half B.** L5/SERIES are **read-only advisory feedstock** — seat-gated perspective (player FP vs DM rail) + agency envelopes **enable** shared-table / DM-as-player / privileged views without players authoring the world.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Perspective envelopes + seamless mode transitions |
| Inspiration / L5 bar (advisory) | Seats shared_table / dm_as_player / privileged_access; player FP ≠ DM rail; players do not author world; DM-retconnable transitions via Phase-3 guards |
| Inspiration (studied) | (1) Conceptual Phase 4 + 4.1–4.3. (2) Execution Phase-3 DMPauseGate / NarrativeDeltaVeto. (3) Phase-1.1 PresentationShell |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + primary pseudo for envelope modes + transition guards |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_camera_control_envelopes` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_camera_control_envelopes/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual Phase 4 + 4.1–4.3 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

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
| `ux_baseline_fp` | `PlayerFPRig` / PerspectiveEnvelope | DM rail without handoff → Unauthorized | active FP camera |
| `ux_dm_worldcam` | `ICameraRig` WorldCam | player seat → Unauthorized | Current camera WorldCam |
| mode transitions | ModeTransitionGraph + TransitionGuardRegistry | guard fail → Busy/Unauthorized | mode restored or held |
| agency handoff | AgencyEnvelope enter/exit | dominate without release → reject | handoff ledger row |

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
enum PerspectiveMode { PLAYER_FP, DM_WORLD, DM_MAP, DM_SENSORIUM_ATTACH, DM_RAIL }

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
  + evaluate(from_mode: int, to_mode: int, context: Dictionary) -> Error
  # may consult Phase-3 OverwritePatchLayer / DMPauseGate

AgencyEnvelope (RefCounted):
  + set_agency(cls: int, target_id: StringName, reason: StringName) -> Error
  + classify_and_retarget(mode: int, hint: Dictionary) -> Error
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
#
# === JUNIOR WORK-ORDER (ux_camera_control_envelopes L5 — advisory) ===
# Seats: shared_table / dm_as_player / privileged_access — TransitionGuardRegistry
#   rejects wrong-seat / illegal edges (never invent mode).
# Players do not author world: PLAYER_FP intents never write Simulation WorldState.
# DM rail vs player FP: ModeTransitionGraph edges only; DM_RAIL/WORLD/MAP ≠ FP author.
# DM-retconnable: consult Phase-3 DMPauseGate / overwrite veto before blend.
# Agency bound: AgencyEnvelope / PilotMachineryGlue own dominate handoff (4.3) — not here invent.
# ===========================================================

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
	# JUNIOR WORK-ORDER: illegal edge = seat/contract refuse — never invent transition
	if not _transitions.can_transition(from_mode, to_mode):
		return ERR_INVALID_PARAMETER
	var ctx := {"reason": reason, "dm_paused": false}
	if _pause_gate != null:
		ctx["dm_paused"] = _pause_gate.is_paused()
	# JUNIOR WORK-ORDER: DM-retconnable — Phase-3 pause/veto may block
	var gerr := _guards.evaluate(from_mode, to_mode, ctx)
	if gerr != OK:
		return gerr
	var err := _envelope.set_mode(to_mode, reason)
	if err != OK:
		return err
	_interp.blend(StringName(str(from_mode)), StringName(str(to_mode)), 0.0)
	mode_changed.emit(from_mode, to_mode)  # Presentation only — never WorldState author
	return OK

# Ordering: 4.1 envelope/scene → 4.2 DM rigs/graph → 4.3 agency/pilot ledger.
# Player FP never Autoload Simulation; SensoriumAttach RO into WorldState.

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, stack-input-intent, engine-godot-463-dotnet | Catalog: ux_camera_control_envelopes | Type: Genesis.Perspective.ICameraRig

// JUNIOR WORK-ORDER (ux_camera_control_envelopes): implement `Genesis.Perspective.ICameraRig` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Perspective;
// Index B3 — canonical
public interface ICameraRig {
    StringName RigId { get; }
    Error Activate(PerspectiveMode mode, SeatContext seat);
    void ApplyFov(FovContract contract);
    // Must-fail: player on DM WorldCam → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4-001 | PerspectiveDirector lives under Presentation — never Autoload Simulation root |
| I-4-002 | SensoriumAttach is read-only into Simulation WorldState |
| I-4-003 | Illegal ModeTransitionGraph edges rejected before CameraInterpolator blend |
| I-4-004 | TransitionGuardRegistry may block when Phase-3 DMPauseGate / overwrite veto fires |
| I-4-005 | Agency set_agency during DM rail requires PilotMachineryGlue handoff (4.3) |
| I-4-006 | **L5:** seats + player-FP≠DM-rail + no player world-author preserved by guards |

## Acceptance

- [x] Parallel spine path `Execution/Phase-4-…/` (primary)
- [x] Path-qualified `conceptual_counterpart` → frozen Phase 4
- [x] Module map + child index for 4.1 / 4.2 / 4.3
- [x] Interfaces + primary pseudo for PerspectiveDirector
- [x] Secondary **4.1** Player FP + tertiaries 4.1.1–4.1.3
- [x] Secondary **4.2** DM Rigs (+ 4.2.1–4.2.3)
- [x] Secondary **4.3** Agency (+ 4.3.1–4.3.3)
- [x] **UX Catalog paint** — L5 seats / FP vs DM rail / no player world-author as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `ICameraRig.Activate(mode, seat)` returns `Error.Unauthorized` when seat mismatches rail (player on DM WorldCam/MapCam; never bare OK) — row `ux_camera_control_envelopes`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player seat, **When** ICameraRig.Activate(DmWorldCam), **Then** Unauthorized
- [ ] **Given** dominate without release path, **When** AgencyEnvelope exit, **Then** reject and prior mode held
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Research integration

- Presentation-layer Node placement; WorldShell regen does not Autoload cameras.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. **Paint** secondary **4.1** then tertiary **4.1.1** (this wave).
2. Next paint cursor: **4.1.2**.

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.1**.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
