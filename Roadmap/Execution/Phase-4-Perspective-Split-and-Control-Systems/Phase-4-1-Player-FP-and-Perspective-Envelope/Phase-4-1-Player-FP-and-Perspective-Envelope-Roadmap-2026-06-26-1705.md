---
title: Phase 4.1 — Player FP and Perspective Envelope (Execution)
roadmap-level: secondary
phase-number: 4
subphase-index: "4.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_baseline_fp
priority: high
progress: 70
handoff_readiness: 78
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-4
- perspective
- player-fp
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[ux_baseline_fp]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_baseline_fp/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.1 — Player FP and Perspective Envelope (Execution)

Execution secondary: **PlayerFP baseline** + **PerspectiveEnvelope** (legal modes, intent vs observe) wired to **UnifiedSceneGraph**, **CameraInterpolatorRegistry**, DM FOV rigs, and **PilotGraph**. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — player FP vs DM observe/rail seats + observe-only guards **enable** shared-table play without players authoring the world.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | FP baseline + legal mode envelope |
| Inspiration / L5 bar (advisory) | PLAYER_FP seat vs DM observe modes; players do not author WorldState; PilotGraph agency edges; DM-retconnable via pause/veto |
| Inspiration (studied) | (1) Conceptual 4.1 + 4.1.1–4.1.3. (2) Execution Phase-4 primary. (3) Phase-1.1 InputIntent. (4) Phase-3 DMPauseGate |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + secondary pseudo for mode request → guards → blend → activate → PilotGraph |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_baseline_fp` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_baseline_fp/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.1 + tertiaries 4.1.1–4.1.3 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_baseline_fp` |
| Label | Default embodied first-person play |
| Seats | `player`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Perspective.PlayerFpRig` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | third-person orbit default; player WorldCam |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_baseline_fp` | `PlayerFPRig` activate | wrong seat → Unauthorized | FP camera current |
| mode envelope | `PerspectiveEnvelope` + ModeTransitionGraph | illegal edge → reject | mode id |
| pilot graph | PilotGraph bind | missing pilot → Unconfigured | pilot binding |
| WorldCam/MapCam | **delegate 4.1.3** | FP leaf ≠ WorldCam owner | (see SparkyDmFreeCamRig) |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.PlayerFpRig` |
| `stack-input-intent` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.PlayerFpRig` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.PlayerFpRig` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility | Owner tertiary |
|--------|----------------|----------------|
| `PerspectiveEnvelope` | Active mode + intent vs observe routing | 4.1.1 |
| `ModeTransitionGraph` | Legal edges between modes | 4.1.1 |
| `PilotGraph` | self → dominate → absent-proxy reconcile | 4.1.1 |
| `UnifiedSceneGraph` | Single presentation composition root | 4.1.2 |
| `CameraInterpolatorRegistry` | Named blends / snap_cut fallback | 4.1.2 |
| `PlayerFPRig` | Default FP agency anchor | 4.1.2 |
| `WorldCamFOV` | DM tactical overview FOV (RO WorldState) | 4.1.3 |
| `MapCamFOV` | Strategic map FOV overlays | 4.1.3 |
| `SensoriumAttachFOV` | Entity sensorium FOV — never dominate | 4.1.3 |

## Interfaces

```text
enum PerspectiveMode { PLAYER_FP, DM_WORLD, DM_MAP, DM_SENSORIUM_ATTACH, DM_RAIL }

InputIntent (RefCounted):  # import Phase-1.1
  + intent_id: StringName
  + source_mode: int
  + payload: Dictionary
  + to_dict() -> Dictionary

PerspectiveEnvelope (RefCounted):
  + mode() -> int
  + set_mode(mode: int, reason: StringName) -> Error
  + route_intent(intent: InputIntent) -> Error
  + is_observe_only(mode: int) -> bool
  signals: mode_changed(from_mode, to_mode)

ModeTransitionGraph (RefCounted):
  + can_transition(from_mode: int, to_mode: int) -> bool
  + next_edges(from_mode: int) -> Array

PilotGraph (RefCounted):
  + reconcile(active_mode: int, agency_hint: StringName) -> Error
  signals: agency_edge_changed(from_kind, to_kind)

UnifiedSceneGraph (Node under Presentation — NOT Autoload):
  + attach_rig(rig_id: StringName, node: Node) -> Error
  + detach_rig(rig_id: StringName) -> Error
  + set_active_rig(rig_id: StringName) -> Error
  + active_rig_id() -> StringName

CameraInterpolatorRegistry (RefCounted):
  + blend(from_id: StringName, to_id: StringName, profile: StringName) -> Error
  + resolve_profile(profile: StringName) -> StringName  # missing → snap_cut
  signals: blend_complete(to_id)

PlayerFPRig (Node):
  + rig_id() -> StringName  # &"fp_baseline_rig"
  + activate() -> Error
  + deactivate() -> Error
```

## Pseudo-code

```pseudo
# 4.1 — Player FP / Perspective Envelope secondary (Godot 4 stable).
# Citations: Node under Presentation; RefCounted policies; Error/OK; StringName; signals.
#
# === JUNIOR WORK-ORDER (ux_baseline_fp L5 — advisory) ===
# Seats: shared_table / dm_as_player / privileged — illegal edges refuse (never invent mode).
# Players do not author world: observe-only modes reject non-mode_switch intents;
#   PLAYER_FP Presentation never writes Simulation WorldState.
# DM rail vs player FP: _rig_for_mode maps FP ↔ world/map/sensorium/rail distinctly.
# DM-retconnable: DMPauseGate + NarrativeDeltaVeto RO may block request_mode.
# Agency: PilotGraph.reconcile after set_mode — Sensorium never dominate (4.1.1/4.3).
# ===========================================================

class_name PlayerPerspectiveController
extends Node

signal presentation_mode_changed(from_mode, to_mode)

var _envelope: PerspectiveEnvelope
var _graph: ModeTransitionGraph
var _pilot: PilotGraph
var _scene: UnifiedSceneGraph
var _interp: CameraInterpolatorRegistry
var _pause_gate: RefCounted   # Phase-3.1 DMPauseGate (RO)
var _veto: RefCounted         # Phase-3.3 NarrativeDeltaVetoPolicy (RO)

func request_mode(to_mode: int, reason: StringName) -> Error:
	var from_mode: int = _envelope.mode()
	# JUNIOR WORK-ORDER: illegal edge = seat/contract refuse
	if not _graph.can_transition(from_mode, to_mode):
		return ERR_INVALID_PARAMETER
	if _pause_gate != null and _pause_gate.is_paused() and to_mode == PerspectiveMode.PLAYER_FP:
		# JUNIOR WORK-ORDER: DM-retconnable — pause may gate FP resume
		pass
	if _veto != null and _veto.blocks_presentation(from_mode, to_mode, reason):
		return ERR_BUSY
	var from_rig: StringName = _scene.active_rig_id()
	var to_rig: StringName = _rig_for_mode(to_mode)
	_scene.detach_rig(from_rig)
	var profile: StringName = _interp.resolve_profile(&"ease_default")
	var berr := _interp.blend(from_rig, to_rig, profile)
	if berr != OK:
		return berr
	var aerr := _scene.set_active_rig(to_rig)
	if aerr != OK:
		return aerr
	var eerr := _envelope.set_mode(to_mode, reason)
	if eerr != OK:
		return eerr
	_pilot.reconcile(to_mode, &"self")
	presentation_mode_changed.emit(from_mode, to_mode)  # Presentation only
	return OK

func route_intent(intent: InputIntent) -> Error:
	# JUNIOR WORK-ORDER: players do not author world from observe seats
	if _envelope.is_observe_only(intent.source_mode):
		if intent.intent_id != &"mode_switch":
			return ERR_UNAUTHORIZED
	return _envelope.route_intent(intent)

func _rig_for_mode(mode: int) -> StringName:
	# JUNIOR WORK-ORDER: DM rail / world / map ≠ player FP author path
	match mode:
		PerspectiveMode.PLAYER_FP:
			return &"fp_baseline_rig"
		PerspectiveMode.DM_WORLD:
			return &"world_cam_rig"
		PerspectiveMode.DM_MAP:
			return &"map_cam_rig"
		PerspectiveMode.DM_SENSORIUM_ATTACH:
			return &"sensorium_attach_rig"
		_:
			return &"fp_baseline_rig"

# Ordering: 4.1.1 → 4.1.2 → 4.1.3. 4.2 owns full guard matrix; 4.3 agency glue.

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, stack-input-intent, engine-godot-463-dotnet | Catalog: ux_baseline_fp | Type: Genesis.Perspective.PlayerFpRig

// JUNIOR WORK-ORDER (ux_baseline_fp): implement `Genesis.Perspective.PlayerFpRig` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Perspective;
// Index B3 — FP implements ICameraRig
public interface IPlayerFpRig : ICameraRig {
    // Must-fail: DM-only mode Activate from player-only seat mismatch → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.1-001 | PlayerPerspectiveController lives under Presentation — never Autoload Simulation |
| I-4.1-002 | Mode changes require ModeTransitionGraph.can_transition before blend |
| I-4.1-003 | Observe-only modes reject non-mode-switch InputIntent |
| I-4.1-004 | SensoriumAttach never writes Simulation WorldState |
| I-4.1-005 | active_rig_id exclusivity via UnifiedSceneGraph.set_active_rig |
| I-4.1-006 | Missing interpolator profile → snap_cut + audit (4.1.2) |
| I-4.1-007 | **L5:** seats + no player world-author + FP≠DM-rail preserved |

## Acceptance

- [x] Parallel spine path `Execution/Phase-4-…/Phase-4-1-…/`
- [x] Path-qualified `conceptual_counterpart` → frozen 4.1
- [x] Child index 4.1.1–4.1.3
- [x] Interfaces + secondary pseudo for PlayerPerspectiveController
- [x] Tertiaries 4.1.1–4.1.3 minted this wave
- [x] **UX Catalog paint** — L5 seats / FP vs DM / no world-author as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `PlayerFpRig.Activate(mode, seat)` returns `Error.Unauthorized` when seat mismatches rail (player on DM WorldCam/MapCam; never bare OK) — row `ux_baseline_fp`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** allowed seat, **When** PlayerFPRig activate, **Then** Current camera is FP and wrong-seat activate returns Unauthorized
- [ ] **Given** illegal ModeTransitionGraph edge, **When** PerspectiveEnvelope.Transition, **Then** reject and prior mode restored
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Research integration

- Presentation-layer Node placement; camera/rigs are not Autoload world roots.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. **Paint** tertiary **4.1.1** (this wave).
2. Next paint cursor: **4.1.2**.

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.1.1**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
