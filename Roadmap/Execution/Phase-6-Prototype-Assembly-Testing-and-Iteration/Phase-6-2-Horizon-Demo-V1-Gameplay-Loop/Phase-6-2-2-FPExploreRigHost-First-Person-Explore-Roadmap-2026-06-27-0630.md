---
title: Phase 6.2.2 — FPExploreRigHost First-Person Explore (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_baseline_fp
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
- fp-explore
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_baseline_fp/L5]]'
- '[[ux_baseline_fp]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Godot-Implementation-Decision-Matrix]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Godot-Stock-Patterns]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.2.2 — FPExploreRigHost First-Person Explore (Execution)

> **Stock Godot FPS (mandatory):** [[Godot-Implementation-Decision-Matrix]] + [[Godot-Stock-Patterns]] (+ [[PIN-stock_godot_fps]]). **Supersedes** any reading that FPExploreRigHost / PerspectiveEnvelope / “FP rail” / host Move·Look·HandleInput **owns** locomotion. Host = **selector**: set envelope mode `player_fp`, set eye `Camera3D.Current`, **enable** stock FPS on `res://player/Player.tscn` (`CharacterBody3D`). Stock pattern implements walk+look.

Execution tertiary: **FPExploreRigHost** (beat 2) — activate `player_fp` on **PerspectiveEnvelope** (selector), enable stock FPS locomotion/look, emit `demo_fp_active`. Prereq: 6.2.1 `demo_spawn_complete`. Respects **DMPauseGate**. Consumers: **6.2.3**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B.** L5/SERIES advisory — FP explore host is PLAYER_FP seat; not DM rail; not world-author.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | FP explore host after spawn ([[conceptual 6.2.2]]) |
| Inspiration / L5 bar (advisory) | PLAYER_FP explore host; distinct from DM rail; no world-author via look |
| Inspiration (studied) | (1) Conceptual 6.2.2. (2) Execution 6.2.1. (3) PerspectiveEnvelope / PlayerFPRig (4.1) as **selector**. (4) PlayRegionHost (6.1.2). (5) Stock FPS matrix |
| L5 / package crosswalk | phase-aligned `[[ux_baseline_fp]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Host Node; envelope RO activate; enable stock CharacterBody3D FPS (not custom binder) |
| Validation | Catalog paint DoD met; playable claim needs operator F5 |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_baseline_fp` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_baseline_fp/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2.2 |
| `dispatch_scope` | Execution tertiary **6.2.2** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_baseline_fp` |
| Label | Default embodied first-person play |
| Seats | `player`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.FpExploreRigHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | third-person orbit default; player WorldCam |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| FP explore | `FPExploreRigHost` → ICameraRig + PerspectiveEnvelope | wrong seat → Unauthorized | FP current |
| DemoCamera | **forbidden** | must type real ICameraRig | — |
| intent | observe only this beat | WorldState write → reject | explore pose |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.FpExploreRigHost` |
| `stack-input-intent` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.FpExploreRigHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.FpExploreRigHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `FPExploreRigHost` | awaiting_spawn → activating → exploring → beat_exit \| blocked |
| `PerspectiveEnvelopeActivator` | Set envelope mode `player_fp` (RO to ModeTransitionGraph) — **selector only** |
| `StockFpEnableGate` | Enable stock FPS on mounted `Player.tscn` + set eye cam `Current` (**supersedes** `FPLocomotionBinder` as mover) |
| `DMPauseGateListener` | Block explore while paused |

## Interfaces

```text
FPExploreRigHost (Node):
  + activate_after_spawn(fp_rig: Node, envelope: RefCounted) -> Error
  + is_fp_active() -> bool
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: demo_fp_active(session_id), demo_fp_blocked(code)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: FPExploreRigHost is PLAYER_FP — refuse conflate with DM rail cams.
# Players do not author world: explore look/move is Presentation binding only.
# DM rail vs player FP: DM cam transition deferred to 6.2.6.
# Agency: explore = ACTIVE_SELF — never invent DOMINATE here.
# ===========================================================

# 6.2.2 — FPExploreRigHost (Godot 4 stable).
# Citations: Node; Camera3D.Current; CharacterBody3D stock FPS; Error/OK; signals.
# Authority: Godot-Implementation-Decision-Matrix + Godot-Stock-Patterns.
# Reject: activate without spawn_complete; owning ModeTransitionGraph;
#         host Move/Look/HandleInput as player controller; ignoring DMPauseGate; Half B/L5.

class_name FPExploreRigHost
extends Node

signal demo_fp_active(session_id)
signal demo_fp_blocked(code)

enum State { AWAITING_SPAWN, ACTIVATING, EXPLORING, BEAT_EXIT, BLOCKED }
var _state: State = State.AWAITING_SPAWN
var _fp_active: bool = false
var _armed_fp: Node
var _armed_envelope: RefCounted


func run_beat() -> Error:
	return activate_after_spawn(_armed_fp, _armed_envelope)

func activate_after_spawn(fp_rig: Node, envelope: RefCounted) -> Error:
	if fp_rig == null or envelope == null:
		_block(&"missing_prereq")
		return ERR_INVALID_PARAMETER
	if _dm_paused():
		_block(&"dm_pause")
		return ERR_BUSY
	_state = State.ACTIVATING
	envelope.call("set_mode", &"player_fp")  # selector — not mover
	# Enable stock FPS on Player.tscn (CharacterBody3D); expose eye Camera3D.Current.
	# Do NOT implement Move/Look/HandleInput on this host (matrix defect).
	fp_rig.set("fp_active", true)
	_enable_stock_fps(fp_rig)
	_fp_active = true
	_state = State.EXPLORING
	demo_fp_active.emit(StringName(str(fp_rig.get_instance_id())))
	return OK

func _enable_stock_fps(fp_rig: Node) -> void:
	# Selector: enable FPS script + Captured mouse; locomotion lives on stock CharacterBody3D.
	# See Godot-Stock-Patterns §1. Supersedes: Wire input.* move/look → FPRig as controller.
	pass

func _dm_paused() -> bool:
	return false  # bind DMPauseGate

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	demo_fp_blocked.emit(code)

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, stack-input-intent, engine-godot-463-dotnet | Catalog: ux_baseline_fp | Type: Genesis.Demo.FpExploreRigHost

namespace Genesis.Demo;
// GAP4: FPExploreRigHost → ICameraRig / PlayerFPRig (4.1) as SELECTOR + stock CharacterBody3D FPS — not DemoCamera mover
public sealed partial class FPExploreRigHost : Node {
    private ICameraRig _fpRig = null!; // PlayerFPRig implements ICameraRig (selector only)
    public Error ActivateAfterSpawn(ICameraRig fpRig, PerspectiveEnvelope envelope, SeatContext seat) {
        if (seat.Id != SeatId.Player && !seat.AllowsSharedTable()) return Error.Unauthorized;
        var err = fpRig.Activate(PerspectiveMode.FirstPerson, seat);
        if (err != Error.Ok) return err;
        envelope.AssertPlayerFpBounds(); // 4.1 contract
        // Then: enable stock CharacterBody3D FPS on Player.tscn (Stock Patterns) — not host Move/Look.
        return Error.Ok;
    }
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.2-001 | activate requires spawn_complete FPRig + envelope |
| I-6.2.2-002 | Does not own ModeTransitionGraph — envelope RO activate only |
| I-6.2.2-003 | DMPauseGate must block explore transitions |
| I-6.2.2-004 | demo_fp_active is the sole beat-2 exit signal |
| I-6.2.2-005 | Host does not own locomotion/look — stock CharacterBody3D only (matrix) |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.2
- [x] Interfaces + tertiary pseudo for FPExplore
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `FpExploreRigHost` wrong-seat → Unauthorized; demo stub_only must not satisfy `ICampaignCapableDoDGate` alone — row `ux_baseline_fp`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** wrong seat, **When** FPExploreRigHost activate, **Then** Unauthorized
- [ ] **Given** DemoCamera bind, **When** host wire, **Then** reject — require ICameraRig
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.2.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
