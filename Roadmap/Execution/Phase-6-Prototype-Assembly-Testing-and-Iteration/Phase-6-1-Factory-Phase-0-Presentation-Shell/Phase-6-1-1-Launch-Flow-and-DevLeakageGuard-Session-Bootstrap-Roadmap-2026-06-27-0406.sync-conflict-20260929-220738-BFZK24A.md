---
title: Phase 6.1.1 — Launch Flow and DevLeakageGuard Session Bootstrap (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
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
- launch-flow
- dev-leakage
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_early_game/L5]]'
- '[[ux_early_game]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.1.1 — Launch Flow and DevLeakageGuard Session Bootstrap (Execution)

Execution tertiary: **LaunchFlowController** states + bootstrap checklist + **DevLeakageGuard** + **PresentationSessionHandle**. Owns `presentation_launch_complete`. Mount/HUD → **6.1.2 / 6.1.3**. Parallel spine under `Execution/Phase-6-…/Phase-6-1-…/`. **No Half B.** L5/SERIES advisory — LaunchFlow + DevLeakageGuard refuse leak seats; players do not author at bootstrap.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | App start → checklist → DevLeakageGuard → launch_complete ([[conceptual 6.1.1]]) |
| Inspiration / L5 bar (advisory) | Checklist → DevLeakageGuard → launch_complete; refuse leak seats |
| Inspiration (studied) | (1) Conceptual 6.1.1. (2) Execution 6.1 secondary. (3) presentation.* / InputIntent (1.1). (4) PerspectiveEnvelope RO (4.1) |
| L5 / package crosswalk | phase-aligned `[[ux_early_game]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted controller; fail-closed guard; handle mint |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_early_game` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_early_game/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.1.1 |
| `dispatch_scope` | Execution tertiary **6.1.1** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_early_game` |
| Label | Early-game / session bootstrap surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Ui.LaunchFlowController` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | skip Session-0; leak dev chrome into player launch |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `launch_flow` | `LaunchFlowController.Begin` | DevLeakageGuard fail → Unavailable | PresentationSessionHandle |
| `spawn_bootstrap` | BootstrapChecklist | incomplete checklist → Unconfigured | checklist receipt |
| `seat_bootstrap` | seat inject | missing seat → degraded | SeatContext |
| play region | **delegate 6.1.2** | launch ≠ mount owner | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.LaunchFlowController` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.LaunchFlowController` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `LaunchFlowController` | idle → bootstrapping → launch_complete \| failed |
| `DevLeakageGuard` | Catalog scan + fail path |
| `PresentationSessionHandle` | session_id + shell_id receipt |
| `BootstrapChecklist` | Ordered prereq steps before guard |

## Interfaces

```text
PresentationSessionHandle (RefCounted):
  + session_id: StringName
  + shell_id: StringName
  + to_dict() -> Dictionary

DevLeakageGuard (RefCounted):
  + check(paths: Array) -> Error
  + last_leak_id() -> StringName

LaunchFlowController (RefCounted):
  + run(shell: RefCounted) -> Error
  + state() -> StringName
  + handle() -> PresentationSessionHandle
  signals: presentation_launch_complete(handle), presentation_launch_failed(code)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_early_game L5 — advisory) ===
# Seats: DevLeakageGuard blocks illegal/dev-only authority bleed.
# Players do not author world: launch checklist is Presentation/session only.
# DM rail vs player FP: launch stays seat-neutral until PlayRegion/demo.
# Agency: no agency escalate at launch_complete alone.
# ===========================================================

# 6.1.1 — Launch Flow / DevLeakageGuard (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; Time; signals.
# Reject: waiving DevLeakageGuard; mounting PlayRegion here (6.1.2);
#         HUD init here (6.1.3); Half B/L5.

class_name LaunchFlowController
extends RefCounted

signal presentation_launch_complete(handle)
signal presentation_launch_failed(code)

var _state: StringName = &"idle"
var _guard: DevLeakageGuard
var _handle: PresentationSessionHandle

func run(shell: RefCounted) -> Error:
	_state = &"bootstrapping"
	var err: Error = _run_checklist(shell)
	if err != OK:
		_state = &"failed"
		presentation_launch_failed.emit(&"checklist_fail")
		return err
	err = _guard.check(shell.leak_scan_paths())
	if err != OK:
		_state = &"failed"
		presentation_launch_failed.emit(_guard.last_leak_id())
		return err
	_handle = PresentationSessionHandle.new()
	_handle.session_id = StringName(str(Time.get_ticks_msec()))
	_handle.shell_id = shell.shell_id
	_state = &"launch_complete"
	presentation_launch_complete.emit(_handle)
	return OK

func state() -> StringName:
	return _state

func handle() -> PresentationSessionHandle:
	return _handle

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, engine-godot-463-dotnet | Catalog: ux_early_game | Type: Genesis.Ui.LaunchFlowController

// JUNIOR WORK-ORDER (ux_early_game): implement `Genesis.Ui.LaunchFlowController` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Ui;
public interface ILaunchFlowController {
    Error BootstrapSession(SeatContext seat, DevLeakageGuard guard);
    // Must-fail: DevLeakageGuard fail → Unavailable; non-compose seat → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.1.1-001 | DevLeakageGuard never waived for player attestation |
| I-6.1.1-002 | launch_complete emits only with non-null handle |
| I-6.1.1-003 | failed state rolls back — no partial host mount |
| I-6.1.1-004 | Does not own PlayRegionHost or HUDLayerStack |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.1.1
- [x] Interfaces + tertiary pseudo for Launch/Guard/Handle
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `LaunchFlowController` mount/bootstrap fails closed on DevLeakageGuard / double-mount / wrong seat (Unavailable|AlreadyExists|Unauthorized) — row `ux_early_game`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** DevLeakageGuard fail, **When** LaunchFlowController.Begin, **Then** Unavailable and no PresentationSessionHandle
- [ ] **Given** incomplete BootstrapChecklist, **When** spawn_bootstrap, **Then** Unconfigured

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.1.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
