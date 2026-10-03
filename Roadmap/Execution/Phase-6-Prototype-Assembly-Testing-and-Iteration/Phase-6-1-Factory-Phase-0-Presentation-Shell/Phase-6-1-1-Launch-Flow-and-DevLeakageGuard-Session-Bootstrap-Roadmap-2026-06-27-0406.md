---
title: Phase 6.1.1 — Launch Flow and DevLeakageGuard Session Bootstrap (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
status: active
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
- phase-6
- launch-flow
- dev-leakage
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 6.1.1 — Launch Flow and DevLeakageGuard Session Bootstrap (Execution)

Execution tertiary: **LaunchFlowController** states + bootstrap checklist + **DevLeakageGuard** + **PresentationSessionHandle**. Owns `presentation_launch_complete`. Mount/HUD → **6.1.2 / 6.1.3**. Parallel spine under `Execution/Phase-6-…/Phase-6-1-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | App start → checklist → DevLeakageGuard → launch_complete ([[conceptual 6.1.1]]) |
| Inspiration (studied) | (1) Conceptual 6.1.1. (2) Execution 6.1 secondary. (3) presentation.* / InputIntent (1.1). (4) PerspectiveEnvelope RO (4.1) |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | RefCounted controller; fail-closed guard; handle mint |
| Validation | Guard never waived for player attestation; rollback on fail |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 6.1.1 |
| `dispatch_scope` | Execution tertiary **6.1.1** mint (FAST DFS) |

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
```

## Invariants

| ID | Rule |
|----|------|
| I-6.1.1-001 | DevLeakageGuard never waived for player attestation |
| I-6.1.1-002 | launch_complete emits only with non-null handle |
| I-6.1.1-003 | failed state rolls back — no partial host mount |
| I-6.1.1-004 | Does not own PlayRegionHost or HUDLayerStack |

## Acceptance

- [x] Parallel spine under Phase-6-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.1.1
- [x] Interfaces + tertiary pseudo for Launch/Guard/Handle
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
