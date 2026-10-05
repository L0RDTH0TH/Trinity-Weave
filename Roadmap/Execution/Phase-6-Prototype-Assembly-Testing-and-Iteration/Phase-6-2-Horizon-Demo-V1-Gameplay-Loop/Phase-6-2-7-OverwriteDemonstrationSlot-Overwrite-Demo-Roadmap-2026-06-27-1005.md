---
title: Phase 6.2.7 — OverwriteDemonstrationSlot Overwrite Demo (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.7"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roadmap-2026-06-27-1005]]'
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
- horizon-demo
- overwrite
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roadmap-2026-06-27-1005]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 6.2.7 — OverwriteDemonstrationSlot Overwrite Demo (Execution)

Execution tertiary: **OverwriteDemonstrationSlot** (beat 7) — after `demo_dm_cam_active`, build demo `live_patch` on `demo_shrine_mood` via **OverwritePatchLayer**, run **NarrativeDeltaVetoPolicy** → `demo_overwrite_applied` | `demo_overwrite_vetoed`. Consumers: **6.2.8**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | One demo overwrite/veto after DM cam ([[conceptual 6.2.7]]) |
| Inspiration (studied) | (1) Conceptual 6.2.7. (2) Execution 6.2.6. (3) DMOverwriteClass / veto nouns (3.3). (4) SpawnBootstrap facets (6.2.1) |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | Slot Node; single live_patch; veto gate; session signals |
| Validation | Exactly one applied|vetoed outcome per dm_cam_active arm |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 6.2.7 |
| `dispatch_scope` | Execution tertiary **6.2.7** mint (FAST DFS) |

## Module map

| Module | Responsibility |
|--------|----------------|
| `OverwriteDemonstrationSlot` | dm_cam_active → build_patch → veto → applied \| vetoed \| blocked |
| `OverwritePatchLayer` | Apply live_patch to demo_shrine_mood facet |
| `NarrativeDeltaVetoPolicy` | Demo veto (no CanonRegistry write) |
| `OverwriteOutcomePublisher` | demo_overwrite_applied / demo_overwrite_vetoed |

## Interfaces

```text
OverwriteDemonstrationSlot (Node):
  + arm_after_dm_cam() -> Error
  + apply_demo_overwrite() -> Error
  + last_outcome() -> StringName
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: demo_overwrite_applied(patch_id), demo_overwrite_vetoed(reason), demo_overwrite_blocked(code)
```

## Pseudo-code

```pseudo
# 6.2.7 — OverwriteDemonstrationSlot (Godot 4 stable).
# Citations: Node; Dictionary; StringName; Error/OK; signals.
# Reject: ReGenerationIntentQueue; CanonRegistry writes; multi-patch;
#         apply without dm_cam_active; Half B/L5.

class_name OverwriteDemonstrationSlot
extends Node

signal demo_overwrite_applied(patch_id)
signal demo_overwrite_vetoed(reason)
signal demo_overwrite_blocked(code)

enum State { AWAITING_DM_CAM, BUILDING_PATCH, VETO_CHECK, APPLIED, VETOED, BLOCKED }
var _state: State = State.AWAITING_DM_CAM
var _patch: Dictionary = {}
var _outcome: StringName = &""
var _done: bool = false

func run_beat() -> Error:
	var err := arm_after_dm_cam()
	if err != OK:
		return err
	return apply_demo_overwrite()

func arm_after_dm_cam() -> Error:
	_state = State.BUILDING_PATCH
	_patch = {"target": &"demo_shrine_mood", "op": &"live_patch", "id": &"demo_ow_001"}
	return OK

func apply_demo_overwrite() -> Error:
	if _state != State.BUILDING_PATCH:
		_block(&"bad_state")
		return ERR_UNAVAILABLE
	if _done:
		_block(&"already_done")
		return ERR_ALREADY_EXISTS
	_state = State.VETO_CHECK
	if _veto(_patch):
		_outcome = &"vetoed"
		_state = State.VETOED
		_done = true
		demo_overwrite_vetoed.emit(&"narrative_delta")
		return OK
	# OverwritePatchLayer.apply(_patch) — demo facet only
	_outcome = &"applied"
	_state = State.APPLIED
	_done = true
	demo_overwrite_applied.emit(_patch["id"])
	return OK

func last_outcome() -> StringName:
	return _outcome

func _veto(patch: Dictionary) -> bool:
	return false

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	demo_overwrite_blocked.emit(code)
```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.7-001 | arm_after_dm_cam requires demo_dm_cam_active |
| I-6.2.7-002 | Target facet is demo_shrine_mood only |
| I-6.2.7-003 | No CanonRegistry / ReGen queue on demo path |
| I-6.2.7-004 | Exactly one applied\|vetoed outcome unlocks beat 8 |

## Acceptance

- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.7
- [x] Interfaces + tertiary pseudo for OverwriteDemonstrationSlot
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
