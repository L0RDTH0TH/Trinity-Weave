---
title: Phase 6.2.4 — SimTickStub Sim Stub (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.4"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]'
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
- sim-stub
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 6.2.4 — SimTickStub Sim Stub (Execution)

Execution tertiary: **SimTickStub** (beat 4) — on `intent_demo_interact` run **one** SimTickPipeline stand-in tick + **WorldEventLog** append → `demo_sim_tick_committed`. Prereq: 6.2.3 `demo_intent_labeled`. Respects **DMPauseGate**. Consumers: **6.2.5**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Single demo sim tick after intent ([[conceptual 6.2.4]]) |
| Inspiration (studied) | (1) Conceptual 6.2.4. (2) Execution 6.2.3. (3) SimTickPipeline / WorldEventLog / SimClock (3.1). (4) DMPauseGate |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | Stub Node; ≤1 tick; log append; session signal |
| Validation | Exactly one committed tick per labeled intent (or pause/block) |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 6.2.4 |
| `dispatch_scope` | Execution tertiary **6.2.4** mint (FAST DFS) |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SimTickStub` | awaiting_intent → tick_pending → committing → committed \| paused \| blocked |
| `DemoTickRunner` | One-shot stand-in for SimTickPipeline |
| `WorldEventLogAppender` | Append `demo_interact_observed` |
| `DMPauseGateListener` | Pause path without commit |

## Interfaces

```text
SimTickStub (Node):
  + arm_after_intent(intent: Dictionary) -> Error
  + commit_one_tick() -> Error
  + last_event_id() -> StringName
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: demo_sim_tick_committed(event_id), demo_sim_tick_paused(code), demo_sim_tick_blocked(code)
```

## Pseudo-code

```pseudo
# 6.2.4 — SimTickStub (Godot 4 stable).
# Citations: Node; Dictionary; StringName; Error/OK; signals.
# Reject: multi-tick loops; OffScreen/full SimTickPipeline; commit without
#         intent_labeled; Half B/L5.

class_name SimTickStub
extends Node

signal demo_sim_tick_committed(event_id)
signal demo_sim_tick_paused(code)
signal demo_sim_tick_blocked(code)

enum State { AWAITING_INTENT, TICK_PENDING, COMMITTING, COMMITTED, PAUSED, BLOCKED }
var _state: State = State.AWAITING_INTENT
var _intent: Dictionary = {}
var _last_event: StringName = &""
var _ticks_done: int = 0

var _armed_intent: Dictionary = {}

func run_beat() -> Error:
	var err := arm_after_intent(_armed_intent)
	if err != OK:
		return err
	return commit_one_tick()

func arm_after_intent(intent: Dictionary) -> Error:
	if intent.is_empty():
		_block(&"missing_intent")
		return ERR_INVALID_PARAMETER
	_intent = intent
	_state = State.TICK_PENDING
	return OK

func commit_one_tick() -> Error:
	if _state != State.TICK_PENDING:
		_block(&"bad_state")
		return ERR_UNAVAILABLE
	if _dm_paused():
		_state = State.PAUSED
		demo_sim_tick_paused.emit(&"dm_pause")
		return ERR_BUSY
	if _ticks_done >= 1:
		_block(&"tick_cap")
		return ERR_ALREADY_EXISTS
	_state = State.COMMITTING
	_last_event = &"demo_interact_observed"
	# WorldEventLog.append(_last_event, _intent) — stand-in only
	_ticks_done = 1
	_state = State.COMMITTED
	demo_sim_tick_committed.emit(_last_event)
	return OK

func _dm_paused() -> bool:
	return false

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	demo_sim_tick_blocked.emit(code)
```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.4-001 | arm_after_intent requires demo_intent_labeled payload |
| I-6.2.4-002 | At most one tick commit per armed intent |
| I-6.2.4-003 | DMPauseGate yields paused — no silent commit |
| I-6.2.4-004 | demo_sim_tick_committed is the sole beat-4 exit signal |

## Acceptance

- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.4
- [x] Interfaces + tertiary pseudo for SimTickStub
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
