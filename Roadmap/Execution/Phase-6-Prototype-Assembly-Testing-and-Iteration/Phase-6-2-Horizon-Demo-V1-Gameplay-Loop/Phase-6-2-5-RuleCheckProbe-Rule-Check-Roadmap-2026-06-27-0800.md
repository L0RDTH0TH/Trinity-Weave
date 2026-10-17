---
title: Phase 6.2.5 — RuleCheckProbe Rule Check (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.5"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]'
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
- rule-check
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 6.2.5 — RuleCheckProbe Rule Check (Execution)

Execution tertiary: **RuleCheckProbe** (beat 5) — after `demo_sim_tick_committed` build a **RuleContextFrame** stub + **demo_ruleset**, run **one** RuleEngineCore pass → `rule_demo_pass` | `rule_demo_fail` → `demo_rule_check_complete`. Halt-on-fail default. Consumers: **6.2.6**, **6.2.8**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Single demo rule eval after sim tick ([[conceptual 6.2.5]]) |
| Inspiration (studied) | (1) Conceptual 6.2.5. (2) Execution 6.2.4. (3) RuleEngineCore / RuleContextFrame / RuleEffectBus (5.1). (4) halt-on-fail policy |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | Stub Node; ≤1 eval; EffectBus pass/fail; session signal |
| Validation | Exactly one rule-check completion per committed tick (or blocked) |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 6.2.5 |
| `dispatch_scope` | Execution tertiary **6.2.5** mint (FAST DFS) |

## Module map

| Module | Responsibility |
|--------|----------------|
| `RuleCheckProbe` | awaiting_context → frame_built → evaluating → pass \| fail \| blocked |
| `DemoRuleContextBuilder` | Stub RuleContextFrame from WorldEventLog row |
| `DemoRulesetBinder` | Bind demo_ruleset (no PluginLoader) |
| `RuleEffectBusBridge` | Emit rule_demo_pass / rule_demo_fail |

## Interfaces

```text
RuleCheckProbe (Node):
  + arm_after_tick(event_id: StringName, log_row: Dictionary) -> Error
  + evaluate_once() -> Error
  + last_outcome() -> StringName
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: demo_rule_check_complete(outcome), rule_demo_pass(codes), rule_demo_fail(codes)
```

## Pseudo-code

```pseudo
# 6.2.5 — RuleCheckProbe (Godot 4 stable).
# Citations: Node; Dictionary; StringName; Error/OK; signals.
# Reject: multi-eval loops; PluginLoader; RuleConflictArbiter; spell/quest
#         plugins; commit without sim_tick_committed; Half B/L5.

class_name RuleCheckProbe
extends Node

signal demo_rule_check_complete(outcome)
signal rule_demo_pass(codes)
signal rule_demo_fail(codes)

enum State { AWAITING_CONTEXT, FRAME_BUILT, EVALUATING, PASS, FAIL, BLOCKED }
var _state: State = State.AWAITING_CONTEXT
var _event_id: StringName = &""
var _frame: Dictionary = {}
var _outcome: StringName = &""
var _evals_done: int = 0

var _armed_event_id: StringName = &""
var _armed_log_row: Dictionary = {}

func run_beat() -> Error:
	var err := arm_after_tick(_armed_event_id, _armed_log_row)
	if err != OK:
		return err
	return evaluate_once()

func arm_after_tick(event_id: StringName, log_row: Dictionary) -> Error:
	if event_id == &"" or log_row.is_empty():
		_block(&"missing_tick_context")
		return ERR_INVALID_PARAMETER
	_event_id = event_id
	_frame = {"event_id": event_id, "log_row": log_row, "ruleset": &"demo_ruleset"}
	_state = State.FRAME_BUILT
	return OK

func evaluate_once() -> Error:
	if _state != State.FRAME_BUILT:
		_block(&"bad_state")
		return ERR_UNAVAILABLE
	if _evals_done >= 1:
		_block(&"eval_cap")
		return ERR_ALREADY_EXISTS
	_state = State.EVALUATING
	_evals_done = 1
	# RuleEngineCore.eval(_frame) — single pass stand-in
	var passed: bool = true
	if passed:
		_outcome = &"pass"
		_state = State.PASS
		rule_demo_pass.emit([&"demo_ok"])
	else:
		_outcome = &"fail"
		_state = State.FAIL
		rule_demo_fail.emit([&"demo_fail"])
	demo_rule_check_complete.emit(_outcome)
	return OK

func last_outcome() -> StringName:
	return _outcome

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	_outcome = code
	demo_rule_check_complete.emit(code)
```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.5-001 | arm_after_tick requires demo_sim_tick_committed payload |
| I-6.2.5-002 | At most one RuleEngineCore pass per armed tick |
| I-6.2.5-003 | Halt-on-fail: FAIL still emits demo_rule_check_complete |
| I-6.2.5-004 | No PluginLoader / Arbiter on demo path |

## Acceptance

- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.5
- [x] Interfaces + tertiary pseudo for RuleCheckProbe
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
