---
title: Phase 6.2.6 — DMCamTransitionSlot DM Cam (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.6"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]'
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
- phase-6
- horizon-demo
- dm-cam
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_dm_worldcam/L5]]'
- '[[ux_dm_worldcam]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.2.6 — DMCamTransitionSlot DM Cam (Execution)

Execution tertiary: **DMCamTransitionSlot** (beat 6) — on eligible `demo_rule_check_complete` + cue/hotkey, run **fp_to_worldcam_demo** guards (+ **DMPauseGate**) → WorldCam-only + HUD badge → `demo_dm_cam_active`. Consumers: **6.2.7**, **6.2.8**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B.** L5/SERIES advisory — DMCamTransitionSlot proves FP≠DM rail with observe-only WorldCam; no player world-author.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Demo FP→WorldCam transition after rule check ([[conceptual 6.2.6]]) |
| Inspiration / L5 bar (advisory) | FP→WorldCam demo; DM observe seat; players do not author from WorldCam |
| Inspiration (studied) | (1) Conceptual 6.2.6. (2) Execution 6.2.5 / 6.2.2. (3) ModeTransitionGraph / guards (4.2). (4) HUDLayerStack (6.1.3); DMPauseGate |
| L5 / package crosswalk | phase-aligned `[[ux_dm_worldcam]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Slot Node; single transition; WorldCam only; badge signal |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_dm_worldcam` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_dm_worldcam/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2.6 |
| `dispatch_scope` | Execution tertiary **6.2.6** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_dm_worldcam` |
| Label | Free-flight DM observation rail (WorldCam / Sparky) |
| Seats | `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.DmCamTransitionSlot` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | players use WorldCam; Sensorium transfers intent; MapCam==tilted WorldCam |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| DM cam | `DMCamTransitionSlot` → ICameraRig WorldCam | player seat → Unauthorized | WorldCam current |
| transition | ModeTransitionGraph | guard fail → Busy | mode attested |
| DemoDmCam | **forbidden** | real ICameraRig only | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.DmCamTransitionSlot` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.DmCamTransitionSlot` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `DMCamTransitionSlot` | awaiting_eligibility → awaiting_trigger → guard_evaluating → transitioning → dm_active \| blocked \| rejected |
| `FpToWorldCamDemoEdge` | Named edge `fp_to_worldcam_demo` |
| `TransitionGuardRunner` | Reuse 4.2.1 guard registry (demo subset) |
| `ModeBadgePublisher` | `presentation_mode_badge_dm` |

## Interfaces

```text
DMCamTransitionSlot (Node):
  + arm_after_rule_check(outcome: StringName) -> Error
  + request_transition(trigger: StringName) -> Error
  + is_dm_active() -> bool
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: demo_dm_cam_active(), demo_dm_cam_blocked(code), presentation_mode_badge_dm(active)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_dm_worldcam L5 — advisory) ===
# Seats: FP→WorldCam demo uses TransitionGuardRegistry + DMPauseGate — never silent OK.
# Players do not author world: WorldCam is observe seat in this demo beat.
# DM rail vs player FP: explicit transition proves rails are distinct.
# Agency: DM cam activate ≠ dominate WorldState author.
# ===========================================================

# 6.2.6 — DMCamTransitionSlot (Godot 4 stable).
# Citations: Node; StringName; Error/OK; signals; Camera3D (WorldCam).
# Reject: MapCam/Sensorium; full DMRigPolicyMatrix; transition without
#         rule_check_complete; Half B/L5.

class_name DMCamTransitionSlot
extends Node

signal demo_dm_cam_active
signal demo_dm_cam_blocked(code)
signal presentation_mode_badge_dm(active)

enum State { AWAITING_ELIGIBILITY, AWAITING_TRIGGER, GUARD_EVALUATING, TRANSITIONING, DM_ACTIVE, BLOCKED, REJECTED }
var _state: State = State.AWAITING_ELIGIBILITY
var _rule_outcome: StringName = &""

var _armed_outcome: StringName = &""

func run_beat() -> Error:
	var err := arm_after_rule_check(_armed_outcome)
	if err != OK:
		return err
	return request_transition(&"fp_to_worldcam_demo")

func arm_after_rule_check(outcome: StringName) -> Error:
	if outcome == &"":
		_block(&"missing_rule_outcome")
		return ERR_INVALID_PARAMETER
	_rule_outcome = outcome
	_state = State.AWAITING_TRIGGER
	return OK

func request_transition(trigger: StringName) -> Error:
	if _state != State.AWAITING_TRIGGER:
		_block(&"bad_state")
		return ERR_UNAVAILABLE
	if trigger != &"hotkey" and trigger != &"cue":
		_reject(&"bad_trigger")
		return ERR_INVALID_PARAMETER
	_state = State.GUARD_EVALUATING
	if _dm_paused():
		_block(&"dm_pause")
		return ERR_BUSY
	if not _guards_ok():
		_reject(&"guard_fail")
		return ERR_UNAUTHORIZED
	_state = State.TRANSITIONING
	# Camera swap: player_fp → WorldCam only (demo)
	_state = State.DM_ACTIVE
	presentation_mode_badge_dm.emit(true)
	demo_dm_cam_active.emit()
	return OK

func is_dm_active() -> bool:
	return _state == State.DM_ACTIVE

func _guards_ok() -> bool:
	return true

func _dm_paused() -> bool:
	return false

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	demo_dm_cam_blocked.emit(code)

func _reject(code: StringName) -> void:
	_state = State.REJECTED
	demo_dm_cam_blocked.emit(code)

# === WEAVE C# / .NET (Godot 4.6.3) — ICameraRig / Sparky ===
# Manifest: stack-perspective-camera, engine-godot-463-dotnet | Catalog: ux_dm_worldcam
# GAP4: DMCamTransitionSlot activates real ICameraRig (4.1.3) via ModeTransitionGraph (4.2) — not DemoDmCam
# Index: [[Docs/SeamRegistry-CSharp-Host-Index]] §B3
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

namespace Genesis.Demo;
public sealed partial class DMCamTransitionSlot : Node {
    private ICameraRig _dmRig = null!; // SparkyDmFreeCamRig from 4.1.3
    public Error ArmAfterRuleCheck(SeatContext seat) =>
        _dmRig.Activate(PerspectiveMode.DmWorldCam, seat);
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.6-001 | arm_after_rule_check requires demo_rule_check_complete |
| I-6.2.6-002 | Transition target is WorldCam only (no MapCam/Sensorium) |
| I-6.2.6-003 | DMPauseGate blocks without silent activate |
| I-6.2.6-004 | demo_dm_cam_active is the sole beat-6 success exit |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.6
- [x] Interfaces + tertiary pseudo for DMCamTransitionSlot
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `DmCamTransitionSlot.Activate(mode, seat)` returns `Error.Unauthorized` when seat mismatches rail (player on DM WorldCam/MapCam; never bare OK) — row `ux_dm_worldcam`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player seat, **When** DMCamTransitionSlot → WorldCam, **Then** Unauthorized
- [ ] **Given** DemoDmCam type, **When** bind, **Then** reject
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.2.7**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
