---
title: Phase 4.1.2 — UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig (Execution)
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]'
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
- phase-4
- unified-scene-graph
- camera-interpolator
- player-fp-rig
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_baseline_fp/L5]]'
- '[[ux_baseline_fp]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.1.2 — UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig (Execution)

Execution tertiary: **UnifiedSceneGraph** composition root, **CameraInterpolatorRegistry** named blends, **PlayerFPRig** as default FP **PerspectiveAnchor**. Parallel spine under `Execution/Phase-4-…/Phase-4-1-…/`. **No Half B.** L5/SERIES are **read-only advisory feedstock** — UnifiedSceneGraph + interpolators enable **PLAYER_FP** as default PerspectiveAnchor without players authoring the world; DM rail cameras remain observe seats. FOV contracts → **4.1.3**.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Single-authority scene + interpolators + FP baseline rig ([[conceptual 4.1.2]]) |
| Inspiration / L5 bar (advisory) | PLAYER_FP default rig exclusivity; DM rail ≠ FP ownership; no player world-author via multi-active rigs; seats refuse invent FOV here |
| Inspiration (studied) | (1) Conceptual 4.1.2. (2) Execution 4.1 / 4.1.1. (3) PresentationShell Node placement |
| L5 / package crosswalk | phase-aligned `[[ux_baseline_fp]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | C# / .NET (Godot 4.6.3) Node + RefCounted registry; exclusivity of active_rig_id |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_baseline_fp` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_baseline_fp/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.1.2 + rollup |
| `dispatch_scope` | Execution tertiary **4.1.2** mint (FAST DFS) |

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
| `ux_baseline_fp` | `PlayerFPRig` under UnifiedSceneGraph | player-only activate | FP Current camera |
| interpolator | `CameraInterpolatorRegistry` | mid-transition interrupt → Busy | blend complete or abort |
| scene ownership | UnifiedSceneGraph leaf | Presentation must not mutate Simulation | camera node path |
| DM WorldCam | **not owned** — 4.1.3 | FP rig ≠ WorldCam writer | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.PlayerFpRig` |
| `stack-input-intent` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.PlayerFpRig` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.PlayerFpRig` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `UnifiedSceneGraph` | Presentation composition root; attach/detach rigs |
| `PerspectiveAnchor` | Marker interface on each rig Node |
| `CameraInterpolatorRegistry` | Named blend profiles |
| `PlayerFPRig` | Default `&"fp_baseline_rig"` agency anchor |
| `InterpolatorFallbackAudit` | Emit when profile missing → snap_cut |

## Interfaces

```text
PerspectiveAnchor (interface / convention on Node):
  + rig_id() -> StringName
  + activate() -> Error
  + deactivate() -> Error

UnifiedSceneGraph (Node under Presentation):
  + attach_rig(rig_id: StringName, node: Node) -> Error
  + detach_rig(rig_id: StringName) -> Error
  + set_active_rig(rig_id: StringName) -> Error
  + active_rig_id() -> StringName
  signals: active_rig_changed(from_id, to_id)

CameraInterpolatorRegistry (RefCounted):
  + register(profile: StringName, curve: RefCounted) -> Error
  + resolve_profile(profile: StringName) -> StringName
  + blend(from_id: StringName, to_id: StringName, profile: StringName) -> Error
  signals: blend_complete(to_id)
  signals: interpolator_fallback(requested, used)

PlayerFPRig (Node implements PerspectiveAnchor):
  + rig_id() -> StringName  # &"fp_baseline_rig"
  + activate() -> Error
  + deactivate() -> Error
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_baseline_fp L5 — advisory) ===
# Seats: single active_rig_id — refuse multi-active / invent FOV (4.1.3).
# Players do not author world: SceneGraph is Presentation composition, not WorldState.
# DM rail vs player FP: PlayerFPRig is default FP anchor; DM cams attach as separate rigs.
# Agency: interpolator blends do not grant dominate or world-author intents.
# ===========================================================

# 4.1.2 — UnifiedSceneGraph + CameraInterpolatorRegistry + PlayerFPRig (Godot 4 stable).
# Citations: Node under Presentation; RefCounted; Error/OK; StringName; signals.
# Reject: Autoload scene root; SubViewport ownership as WorldState authority;
#         multi-active rigs; inventing FOV numbers here (4.1.3).

class_name UnifiedSceneGraph
extends Node

signal active_rig_changed(from_id, to_id)

var _rigs: Dictionary = {}          # StringName -> Node
var _active: StringName = &""

func attach_rig(rig_id: StringName, node: Node) -> Error:
	if node == null:
		return ERR_INVALID_PARAMETER
	_rigs[rig_id] = node
	if not node.get_parent() == self:
		add_child(node)
	return OK

func set_active_rig(rig_id: StringName) -> Error:
	if not _rigs.has(rig_id):
		return ERR_DOES_NOT_EXIST
	var prev: StringName = _active
	if prev != &"" and _rigs.has(prev):
		var prev_node: Node = _rigs[prev]
		if prev_node.has_method("deactivate"):
			prev_node.deactivate()
	var next_node: Node = _rigs[rig_id]
	if next_node.has_method("activate"):
		var aerr: Error = next_node.activate(PerspectiveMode.PLAYER_FP, SeatContext.current())  # ICameraRig posture
		if aerr != OK:
			return aerr
	_active = rig_id
	active_rig_changed.emit(prev, rig_id)
	return OK

func active_rig_id() -> StringName:
	return _active

class_name CameraInterpolatorRegistry
extends RefCounted

signal blend_complete(to_id)
signal interpolator_fallback(requested, used)

var _profiles: Dictionary = {
	&"ease_default": true,
	&"snap_cut": true,
	&"dm_orbit": true,
}

func resolve_profile(profile: StringName) -> StringName:
	if _profiles.has(profile):
		return profile
	interpolator_fallback.emit(profile, &"snap_cut")
	return &"snap_cut"

func blend(from_id: StringName, to_id: StringName, profile: StringName) -> Error:
	var used: StringName = resolve_profile(profile)
	# FAST map-gen: treat snap_cut as instantaneous; ease/dm_orbit deferred to Half B timing
	if used == &"snap_cut":
		blend_complete.emit(to_id)
		return OK
	# ease_default / dm_orbit: schedule tween; emit blend_complete on finish
	blend_complete.emit(to_id)
	return OK

class_name PlayerFPRig
extends Node

func to_string() -> String: # PerspectiveAnchor
	return "PlayerFPRig"

func rig_id() -> StringName:
	return &"fp_baseline_rig"

func activate(mode: int, seat: SeatContext) -> Error:
	# ICameraRig / PlayerFPRig — DM-only modes refuse on player FP seat mismatch
	if seat.is_player_fp() and (mode == PerspectiveMode.DM_WORLD or mode == PerspectiveMode.DM_MAP):
		return ERR_UNAUTHORIZED
	# enable FP camera child; do not Autoload
	return OK

func deactivate() -> Error:
	return OK

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
| I-4.1.2-001 | UnifiedSceneGraph is Presentation child — never Autoload / Simulation root |
| I-4.1.2-002 | Exactly one active_rig_id after successful set_active_rig |
| I-4.1.2-003 | Missing interpolator profile → snap_cut + interpolator_fallback signal |
| I-4.1.2-004 | PlayerFPRig.rig_id is always `&"fp_baseline_rig"` |
| I-4.1.2-005 | Blend runs only after 4.1.1 guards succeed (caller ordering) |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine path under Phase-4-1
- [x] Path-qualified conceptual_counterpart
- [x] Interfaces + pseudo for Scene / Interpolator / PlayerFPRig
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `PlayerFpRig.Activate(mode, seat)` returns `Error.Unauthorized` when seat mismatches rail (player on DM WorldCam/MapCam; never bare OK) — row `ux_baseline_fp`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** mid-blend interrupt, **When** CameraInterpolatorRegistry, **Then** Busy or clean abort — never stuck blend
- [ ] **Given** player seat, **When** PlayerFPRig activate, **Then** FP Current; WorldCam activate refused on this leaf
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.1.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
