---
title: Phase 4.1.1 — PerspectiveEnvelope / ModeTransitionGraph / PilotGraph (Execution)
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_camera_control_envelopes
priority: high
progress: 55
handoff_readiness: 74
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-4
- perspective-envelope
- mode-transition
- pilot-graph
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[ux_camera_control_envelopes]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_camera_control_envelopes/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.1.1 — PerspectiveEnvelope / ModeTransitionGraph / PilotGraph (Execution)

Execution tertiary: **PerspectiveEnvelope** (legal modes + intent vs observe), **ModeTransitionGraph** (edges + lightweight guards), **PilotGraph** (self → dominate → absent-proxy). Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — seat-legal edges + observe-only + PilotGraph agency **enable** DM rail vs player FP without players authoring the world. Full TransitionGuardRegistry matrix lives in **4.2**.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Legal modes + transition edges + pilot agency edges |
| Inspiration / L5 bar (advisory) | PLAYER_FP ↔ DM_RAIL/WORLD/MAP edges; observe-only refuse world-author intents; Sensorium never dominate; seats refuse illegal edges |
| Inspiration (studied) | (1) Conceptual 4.1.1. (2) Execution 4.1 / Phase-4 primary. (3) Phase-1.1 InputIntent |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + pseudo for set_mode + edge check + PilotGraph reconcile |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_camera_control_envelopes` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_camera_control_envelopes/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.1.1 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_camera_control_envelopes` |
| Label | Perspective and control envelopes can change and cleanly return |
| Seats | `player`, `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Perspective.PerspectiveEnvelope` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | players get free third-person orbit as default; soft camera without hard restore |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| enter/exit declare | `PerspectiveEnvelope.Transition` | guard fail → Unauthorized/Busy | prior mode restored |
| mode graph edge | `ModeTransitionGraph` | unknown edge → InvalidParameter | graph walk audit |
| pilot bind | `PilotGraph` | missing pilot → Unconfigured | pilot_id |
| hard restore | restore on fail | never leave half-switched camera | Current camera stable |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.PerspectiveEnvelope` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.PerspectiveEnvelope` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `PerspectiveEnvelope` | Mode authority + observe-only routing |
| `ModeTransitionGraph` | Adjacency of PerspectiveMode edges |
| `ModeEdgeGuardLite` | Pause/veto hooks (full registry → 4.2) |
| `PilotGraph` | Agency kind edges: self / dominate / absent_proxy |
| `ModeChangedBus` | Signal fan-out `presentation.mode_changed` |

## Interfaces

```text
enum PerspectiveMode { PLAYER_FP, DM_WORLD, DM_MAP, DM_SENSORIUM_ATTACH, DM_RAIL }
enum PilotAgencyKind { SELF, DOMINATE, ABSENT_PROXY }

PerspectiveEnvelope (RefCounted):
  + mode() -> int
  + set_mode(mode: int, reason: StringName) -> Error
  + route_intent(intent: RefCounted) -> Error
  + is_observe_only(mode: int) -> bool
  signals: mode_changed(from_mode, to_mode)

ModeTransitionGraph (RefCounted):
  + can_transition(from_mode: int, to_mode: int) -> bool
  + next_edges(from_mode: int) -> Array
  + seed_default_edges() -> void

ModeEdgeGuardLite (RefCounted):
  + evaluate(from_mode: int, to_mode: int, ctx: Dictionary) -> Error

PilotGraph (RefCounted):
  + current_kind() -> int
  + reconcile(active_mode: int, agency_hint: StringName) -> Error
  + allowed_kinds(mode: int) -> Array
  signals: agency_edge_changed(from_kind, to_kind)
```

## Pseudo-code

```pseudo
# 4.1.1 — Envelope + ModeTransitionGraph + PilotGraph (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
#
# === JUNIOR WORK-ORDER (ux_camera_control_envelopes L5 — advisory) ===
# Seats: illegal ModeTransitionGraph edges refuse — never invent mode.
# Players do not author world: is_observe_only → only mode_switch intents.
# DM rail vs player FP: seed_default_edges wires PLAYER_FP ↔ DM_RAIL/WORLD/MAP.
# Agency: PilotGraph — SensoriumAttach NEVER reconciles to DOMINATE.
# Full TransitionGuardRegistry matrix deferred to 4.2 (ModeEdgeGuardLite here).
# ===========================================================

class_name PerspectiveEnvelope
extends RefCounted

signal mode_changed(from_mode, to_mode)

var _mode: int = PerspectiveMode.PLAYER_FP
var _graph: ModeTransitionGraph
var _guards: ModeEdgeGuardLite
var _pilot: PilotGraph

func mode() -> int:
	return _mode

func is_observe_only(mode: int) -> bool:
	# JUNIOR WORK-ORDER: DM observe seats — not world-author
	return mode == PerspectiveMode.DM_WORLD \
		or mode == PerspectiveMode.DM_MAP \
		or mode == PerspectiveMode.DM_SENSORIUM_ATTACH

func set_mode(to_mode: int, reason: StringName) -> Error:
	var from_mode: int = _mode
	if from_mode == to_mode:
		return OK
	# JUNIOR WORK-ORDER: seat/edge refuse — never invent transition
	if not _graph.can_transition(from_mode, to_mode):
		return ERR_INVALID_PARAMETER
	var gerr := _guards.evaluate(from_mode, to_mode, {"reason": reason})
	if gerr != OK:
		return gerr
	_mode = to_mode
	_pilot.reconcile(to_mode, &"self")
	mode_changed.emit(from_mode, to_mode)
	return OK

func route_intent(intent: RefCounted) -> Error:
	# JUNIOR WORK-ORDER: players do not author world from observe seats
	if is_observe_only(_mode) and intent.intent_id != &"mode_switch":
		return ERR_UNAUTHORIZED
	return OK

class_name ModeTransitionGraph
extends RefCounted

var _edges: Dictionary = {}

func seed_default_edges() -> void:
	# JUNIOR WORK-ORDER: DM rail vs player FP — explicit legal edges only
	_edges[PerspectiveMode.PLAYER_FP] = [
		PerspectiveMode.DM_WORLD, PerspectiveMode.DM_MAP, PerspectiveMode.DM_RAIL
	]
	_edges[PerspectiveMode.DM_WORLD] = [
		PerspectiveMode.PLAYER_FP, PerspectiveMode.DM_MAP,
		PerspectiveMode.DM_SENSORIUM_ATTACH, PerspectiveMode.DM_RAIL
	]
	_edges[PerspectiveMode.DM_MAP] = [
		PerspectiveMode.PLAYER_FP, PerspectiveMode.DM_WORLD, PerspectiveMode.DM_RAIL
	]
	_edges[PerspectiveMode.DM_SENSORIUM_ATTACH] = [
		PerspectiveMode.DM_WORLD, PerspectiveMode.PLAYER_FP
	]
	_edges[PerspectiveMode.DM_RAIL] = [
		PerspectiveMode.PLAYER_FP, PerspectiveMode.DM_WORLD, PerspectiveMode.DM_MAP
	]

func can_transition(from_mode: int, to_mode: int) -> bool:
	var arr: Array = _edges.get(from_mode, [])
	return to_mode in arr

class_name PilotGraph
extends RefCounted

signal agency_edge_changed(from_kind, to_kind)

var _kind: int = PilotAgencyKind.SELF

func reconcile(active_mode: int, agency_hint: StringName) -> Error:
	var next_kind: int = PilotAgencyKind.SELF
	if agency_hint == &"dominate" and active_mode != PerspectiveMode.DM_SENSORIUM_ATTACH:
		next_kind = PilotAgencyKind.DOMINATE
	elif agency_hint == &"absent_proxy":
		next_kind = PilotAgencyKind.ABSENT_PROXY
	# JUNIOR WORK-ORDER: SensoriumAttach never dominate (agency bound)
	if active_mode == PerspectiveMode.DM_SENSORIUM_ATTACH:
		next_kind = PilotAgencyKind.SELF
	if next_kind != _kind:
		var prev: int = _kind
		_kind = next_kind
		agency_edge_changed.emit(prev, next_kind)
	return OK

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, engine-godot-463-dotnet | Catalog: ux_camera_control_envelopes | Type: Genesis.Perspective.PerspectiveEnvelope

// JUNIOR WORK-ORDER (ux_camera_control_envelopes): implement `Genesis.Perspective.PerspectiveEnvelope` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Perspective;
public interface IPerspectiveEnvelope {
    Error Transition(PerspectiveMode from, PerspectiveMode to, SeatContext seat);
    // Must-fail: guard refuse → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.1.1-001 | Illegal ModeTransitionGraph edges never call set_mode success path |
| I-4.1.1-002 | Observe-only modes reject non-mode-switch intents |
| I-4.1.1-003 | SensoriumAttach never reconciles to DOMINATE |
| I-4.1.1-004 | Full guard matrix deferred to 4.2 TransitionGuardRegistry |
| I-4.1.1-005 | **L5:** seats + FP≠DM-rail + no player world-author preserved |

## Acceptance

- [x] Parallel spine path under Phase-4-1
- [x] Path-qualified conceptual_counterpart
- [x] Interfaces + pseudo for Envelope / Graph / PilotGraph
- [x] **UX Catalog paint** — L5 seats / FP vs DM rail / observe-only as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `PerspectiveEnvelope` transition/guard refuses unauthorized edges with `Unauthorized` — row `ux_camera_control_envelopes`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** unknown graph edge, **When** ModeTransitionGraph walk, **Then** InvalidParameter and camera not half-switched
- [ ] **Given** missing pilot, **When** PilotGraph bind, **Then** Unconfigured
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Subphase next

1. Next paint cursor: **4.1.2** UnifiedSceneGraph / CameraInterpolator / PlayerFPRig.

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.1.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
