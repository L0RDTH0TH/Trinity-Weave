---
title: Phase 5.1.3 — RuleConflictArbiter / RuleEffectBus (Execution)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]'
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
- rule-conflict-arbiter
- rule-effect-bus
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 5.1.3 — RuleConflictArbiter / RuleEffectBus (Execution)

Execution tertiary: **RuleConflictArbiter** (hard_veto → band → priority → merge → overflow); **RuleEffectBus** fan-out to sim / agency / perspective / canon / tone channels. Parallel spine under `Execution/Phase-5-…/Phase-5-1-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Conflict policy + effect routing ([[conceptual 5.1.3]]) |
| Inspiration (studied) | (1) Conceptual 5.1.3. (2) Execution 5.1.1/5.1.2. (3) DMPauseGate (3.1). (4) envelopes 4.1/4.3 |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | RefCounted Arbiter + Bus; signals for Presentation RO adapters |
| Validation | Overflow recorded never silent; world_delta respects DMPauseGate |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 5.1.3 |
| `dispatch_scope` | Execution tertiary **5.1.3** mint (FAST DFS) |

## Module map

| Module | Responsibility |
|--------|----------------|
| `RuleConflictArbiter` | Resolve candidate RulePrimitives |
| `RuleEffectBus` | subscribe / emit_effect + channel queues |
| `ArbiterOverflowRecord` | top-N dropped candidates for audit |

## Interfaces

```text
RuleConflictArbiter (RefCounted):
  + merge_budget: int  # default 32
  + resolve(candidates: Array, ctx: RuleContextFrame) -> Array
  + last_overflow() -> Array

RuleEffectBus (RefCounted):
  + subscribe(effect_id: StringName, cb: Callable) -> Error
  + emit_effect(effect_id: StringName, payload: Dictionary) -> Error
  + enqueue_channel(channel: StringName, payload: Dictionary) -> Error
  signals: effect_emitted(effect_id, payload)
# channels: world_delta | world_event | agency_transition |
#           perspective_transition | canon_proposal | tone_bias
```

## Pseudo-code

```pseudo
# 5.1.3 — RuleConflictArbiter / RuleEffectBus (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
# Reject: silent overflow; Autoload Simulation mutators on Bus; Core ownership (5.1.1);
#         PluginLoader (5.1.2); spell/quest domain logic (5.2/5.3).

class_name RuleConflictArbiter
extends RefCounted

var merge_budget: int = 32
var _overflow: Array = []

func resolve(candidates: Array, ctx: RuleContextFrame) -> Array:
	_overflow.clear()
	var surviving: Array = []
	for r in candidates:
		if _hard_veto(r, ctx):
			continue
		surviving.append(r)
	surviving.sort_custom(func(a, b):
		if a.band != b.band:
			return a.band < b.band
		return a.priority > b.priority
	)
	var out: Array = []
	for r in surviving:
		if out.size() >= merge_budget:
			_overflow.append(r)
			continue
		if _can_merge(r, out):
			_merge_into(r, out)
		else:
			out.append(r)
	return out

func last_overflow() -> Array:
	return _overflow.duplicate()

class_name RuleEffectBus
extends RefCounted

signal effect_emitted(effect_id, payload)

var _subs: Dictionary = {}
var _pause: RefCounted  # DMPauseGate

func emit_effect(effect_id: StringName, payload: Dictionary) -> Error:
	if effect_id == &"world_delta" and _pause != null and _pause.is_paused():
		return ERR_BUSY
	if _subs.has(effect_id):
		for cb in _subs[effect_id]:
			cb.call(payload)
	effect_emitted.emit(effect_id, payload)
	return OK
```

## Invariants

| ID | Rule |
|----|------|
| I-5.1.3-001 | Overflow never silent — recorded in `last_overflow` / evaluation_complete |
| I-5.1.3-002 | `world_delta` respects DMPauseGate |
| I-5.1.3-003 | Bus subscribers are Presentation/Intent RO — no Autoload Simulation mutators |
| I-5.1.3-004 | Default spell-vs-quest conflict policy: `defer_to_spell` (advisory for 5.2/5.3) |

## Acceptance

- [x] Parallel spine under Phase-5-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 5.1.3
- [x] Interfaces + tertiary pseudo for Arbiter/Bus
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
