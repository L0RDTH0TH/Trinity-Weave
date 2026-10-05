---
title: Phase 5.1.1 — RuleEngineCore / RulePrimitive / RuleContextFrame (Execution)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
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
- phase-5
- rule-engine-core
- rule-primitive
- rule-context-frame
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 5.1.1 — RuleEngineCore / RulePrimitive / RuleContextFrame (Execution)

Execution tertiary: **RuleEngineCore** condition→effect loop + cycle detector; **RulePrimitive** atom library; **RuleContextFrame** per-eval snapshot. Plugins/arbiter/bus → **5.1.2–5.1.3**. Parallel spine under `Execution/Phase-5-…/Phase-5-1-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Core evaluate loop + primitives + frame ([[conceptual 5.1.1]]) |
| Inspiration (studied) | (1) Conceptual 5.1.1. (2) Execution 5.1 secondary. (3) SeamRegistry `rule` (1.3). (4) WorldState tick (3.1) |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | GDScript RefCounted Core + Primitive + Frame; evaluate returns candidates for Arbiter |
| Validation | Cycle abort on `rule_id` re-entry; nil-actor quiet-skip |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 5.1.1 |
| `dispatch_scope` | Execution tertiary **5.1.1** mint (FAST DFS) |

## Module map

| Module | Responsibility |
|--------|----------------|
| `RuleEngineCore` | Session evaluate loop; cycle seen-set |
| `RulePrimitive` | `{rule_id, condition_set, effect_set, trigger, band, priority}` |
| `RuleContextFrame` | actor, scene, session, tick, canon, envelopes, tone, spell_metadata, quest_pressure_snapshot, active_plugin_ids, clone_shallow, to_dict |

## Interfaces

```text
RulePrimitive (RefCounted):
  + rule_id: StringName
  + trigger: StringName
  + band: int
  + priority: int
  + condition_set: Array
  + effect_set: Array
  + to_dict() -> Dictionary

RuleContextFrame (RefCounted):
  + actor_id: StringName
  + scene_id: StringName
  + session_id: StringName
  + tick: int
  + canon_snapshot: Dictionary
  + agency: RefCounted
  + perspective: RefCounted
  + tone: Dictionary
  + spell_metadata: Dictionary
  + quest_pressure_snapshot: Dictionary
  + active_plugin_ids: Array
  + clone_shallow() -> RuleContextFrame
  + to_dict() -> Dictionary

RuleEngineCore (RefCounted):
  + register_collector(plugin: RefCounted) -> Error
  + evaluate(trigger: StringName, ctx: RuleContextFrame) -> Array  # RulePrimitive candidates
  + last_cycle_abort() -> StringName
  signals: evaluation_started(trigger), evaluation_complete(result)
```

## Pseudo-code

```pseudo
# 5.1.1 — RuleEngineCore / RulePrimitive / RuleContextFrame (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
# Reject: Autoload global rule table; silent cycle; evaluating without frame;
#         Arbiter/Bus ownership (5.1.3); PluginLoader (5.1.2).

class_name RuleEngineCore
extends RefCounted

signal evaluation_started(trigger)
signal evaluation_complete(result)

var _collectors: Array = []
var _last_cycle: StringName = &""

func evaluate(trigger: StringName, ctx: RuleContextFrame) -> Array:
	evaluation_started.emit(trigger)
	if ctx.actor_id == &"" and not _allow_nil_actor(trigger):
		evaluation_complete.emit({"ok": true, "skipped": true, "candidates": []})
		return []
	var seen: Dictionary = {}
	var candidates: Array = []
	for plugin in _collectors:
		var batch: Array = plugin.collect(trigger, ctx)
		for r in batch:
			var rid: StringName = r.rule_id
			if seen.has(rid):
				_last_cycle = rid
				evaluation_complete.emit({"ok": false, "cycle": rid, "candidates": []})
				return []
			seen[rid] = true
			if not _conditions_pass(r.condition_set, ctx):
				continue
			candidates.append(r)
	evaluation_complete.emit({"ok": true, "candidates": candidates})
	return candidates

func _conditions_pass(conds: Array, ctx: RuleContextFrame) -> bool:
	for c in conds:
		if not _eval_atom(c, ctx):
			return false
	return true

func last_cycle_abort() -> StringName:
	return _last_cycle
```

## Invariants

| ID | Rule |
|----|------|
| I-5.1.1-001 | Cycle detector aborts on duplicate `rule_id` in one evaluate |
| I-5.1.1-002 | Nil-actor triggers quiet-skip unless allowlisted |
| I-5.1.1-003 | Core never applies effects — returns candidates only |
| I-5.1.1-004 | Frame clone is shallow; mutating frame mid-eval is #review-needed |

## Acceptance

- [x] Parallel spine under Phase-5-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 5.1.1
- [x] Interfaces + tertiary pseudo for Core/Primitive/Frame
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
