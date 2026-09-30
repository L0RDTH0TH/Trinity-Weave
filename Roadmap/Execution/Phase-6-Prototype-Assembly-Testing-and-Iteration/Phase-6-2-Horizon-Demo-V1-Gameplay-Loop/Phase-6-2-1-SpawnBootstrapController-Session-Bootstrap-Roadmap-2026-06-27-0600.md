---
title: Phase 6.2.1 — SpawnBootstrapController Session Bootstrap (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_early_game
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
- spawn-bootstrap
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_early_game/L5]]'
- '[[ux_early_game]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.2.1 — SpawnBootstrapController Session Bootstrap (Execution)

> **Stock FPS mount (not a custom controller):** Prefer instance `res://player/Player.tscn` (`CharacterBody3D` + eye cam) inactive at spawn; 6.2.2 enables FPS. `PlayerFPRig` / `ICameraRig` remain **selector** hosts — see [[Godot-Implementation-Decision-Matrix]] + [[Godot-Stock-Patterns]].

Execution tertiary: **SpawnBootstrapController** (beat 1) — session handle + stub shrine facet + inactive **PlayerFPRig** / stock Player prefab attach → `demo_spawn_complete`. Prereq: 6.1.2 `play_region_ready`. Consumers: **6.2.2**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B.** L5/SERIES advisory — demo spawn bootstrap is FP-safe; no world-author.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Demo spawn bootstrap ([[conceptual 6.2.1]]) |
| Inspiration / L5 bar (advisory) | Demo spawn; Presentation spawn marker; players do not author canon at spawn |
| Inspiration (studied) | (1) Conceptual 6.2.1. (2) Execution 6.2 / 6.1.2. (3) PresentationSessionHandle (6.1.1). (4) PlayerFPRig (4.1) |
| L5 / package crosswalk | phase-aligned `[[ux_early_game]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Node controller; stub facet ids; signals on session bus |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_early_game` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_early_game/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2.1 |
| `dispatch_scope` | Execution tertiary **6.2.1** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_early_game` |
| Label | Early-game / session bootstrap surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.SpawnBootstrapController` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | skip Session-0; leak dev chrome into player launch |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| spawn | `SpawnBootstrapController` → PlayRegionHost | double spawn → AlreadyExists | spawn receipt |
| seat | SeatContext inject | missing → degraded | SeatContext |
| camera | PlayerFPRig / ICameraRig bind | player on DM rail → Unauthorized | Current camera |
| fake ports | DemoSpawnPort **forbidden** | must use real hosts | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.SpawnBootstrapController` |
| `stack-entity-bootstrap` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.SpawnBootstrapController` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.SpawnBootstrapController` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SpawnBootstrapController` | idle → bootstrapping → spawned \| failed |
| `DemoShrineStubFacet` | `demo_shrine_v1` / `demo_shrine_mood` ids |
| `SpawnSessionBinder` | Bind PresentationSessionHandle + PlayRegionMountReceipt |
| `FPRigAttachSlot` | Attach PlayerFPRig inactive (`fp_baseline_rig`) |

## Interfaces

```text
SpawnBootstrapController (Node):
  + begin_spawn(receipt: PlayRegionMountReceipt, handle: RefCounted) -> Error
  + session_stub_ids() -> Dictionary  # shrine_v1, shrine_mood
  + attached_fp_rig() -> Node  # inactive until 6.2.2
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: demo_spawn_complete(session_id), demo_spawn_failed(code)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: spawn defaults FP-safe — refuse DM-author spawn invent.
# Players do not author world: spawn bootstrap is session/Presentation.
# DM rail vs player FP: spawn prepares FP host; DM cam comes at 6.2.6.
# Agency: spawn does not grant dominate.
# ===========================================================

# 6.2.1 — SpawnBootstrapController (Godot 4 stable).
# Citations: Node; RefCounted; Error/OK; StringName; signals.
# Reject: spawn without play_region_ready; activating FP before 6.2.2;
#         CompiledWorldManifest; Half B/L5.

class_name SpawnBootstrapController
extends Node

signal demo_spawn_complete(session_id)
signal demo_spawn_failed(code)

enum State { IDLE, BOOTSTRAPPING, SPAWNED, FAILED }
var _state: State = State.IDLE
var _fp_rig: Node = null
var _stub: Dictionary = {}
var _armed_receipt: PlayRegionMountReceipt
var _armed_handle: RefCounted


func run_beat() -> Error:
	# DemoLoopOrchestrator (6.2) dispatch entry — requires prereqs armed on host.
	return begin_spawn(_armed_receipt, _armed_handle)

func begin_spawn(receipt: PlayRegionMountReceipt, handle: RefCounted) -> Error:
	if receipt == null or handle == null:
		_fail(&"missing_prereq")
		return ERR_INVALID_PARAMETER
	_state = State.BOOTSTRAPPING
	_stub = {"shrine": &"demo_shrine_v1", "mood": &"demo_shrine_mood"}
	_fp_rig = _attach_fp_inactive(receipt)
	if _fp_rig == null:
		_fail(&"fp_attach_failed")
		return ERR_CANT_CREATE
	_state = State.SPAWNED
	demo_spawn_complete.emit(handle.get("session_id"))
	return OK

func _attach_fp_inactive(receipt: PlayRegionMountReceipt) -> Node:
	# Mount PlayerFPRig under play region; leave inactive for 6.2.2.
	return null  # filled by scene wiring

func _fail(code: StringName) -> void:
	_state = State.FAILED
	demo_spawn_failed.emit(code)

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, stack-entity-bootstrap, engine-godot-463-dotnet | Catalog: ux_early_game | Type: Genesis.Demo.SpawnBootstrapController

namespace Genesis.Demo;
// GAP4: real contracts from 1–5 — stub *behavior* OK; types must not be parallel fakes
// Hosts: PlayRegionHost (6.1.2), PlayerFPRig / ICameraRig FP baseline (4.1), IEntityBootstrapStage (2)
// Index: [[Docs/SeamRegistry-CSharp-Host-Index]]
public sealed partial class SpawnBootstrapController : Node {
    public Error BeginSpawn(PlayRegionMountReceipt receipt, PresentationSessionHandle handle, SeatContext seat) {
        if (!seat.AllowsSharedTable()) return Error.Unauthorized;
        if (receipt == null || handle == null) return Error.InvalidParameter;
        // Attach PlayerFPRig inactive under PlayRegionHost — activate in 6.2.2
        return Error.Ok;
    }
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.1-001 | begin_spawn requires PlayRegionMountReceipt + session handle |
| I-6.2.1-002 | PlayerFPRig remains inactive until 6.2.2 |
| I-6.2.1-003 | Stub facet ids only — no CompiledWorldManifest |
| I-6.2.1-004 | demo_spawn_complete is the sole beat-1 exit signal |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.1
- [x] Interfaces + tertiary pseudo for SpawnBootstrap
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `SpawnBootstrapController` wrong-seat → Unauthorized; demo stub_only must not satisfy `ICampaignCapableDoDGate` alone — row `ux_early_game`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** double spawn, **When** SpawnBootstrapController, **Then** AlreadyExists
- [ ] **Given** DemoSpawnPort type, **When** bind, **Then** reject — require PlayRegionHost + ICameraRig

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.2.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
