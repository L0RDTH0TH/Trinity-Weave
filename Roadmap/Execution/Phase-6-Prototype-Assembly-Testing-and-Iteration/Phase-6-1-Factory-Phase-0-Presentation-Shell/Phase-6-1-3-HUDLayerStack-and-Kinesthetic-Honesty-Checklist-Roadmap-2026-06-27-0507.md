---
title: Phase 6.1.3 — HUDLayerStack and Kinesthetic Honesty Checklist (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]'
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
- hud
- kinesthetic-honesty
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 6.1.3 — HUDLayerStack and Kinesthetic Honesty Checklist (Execution)

Execution tertiary: **HUDLayerStack** (Base/Mode/Context/Transient) + **KinestheticHonestyChecklist** KH-6.1-001..004 + `presentation_hud_active`. Prereq: 6.1.2 play_region_ready. Transient consumers → **6.2**. Closes **6.1** DFS. Parallel spine under `Execution/Phase-6-…/Phase-6-1-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | HUD layers + KH gates after PlayRegion ready ([[conceptual 6.1.3]]) |
| Inspiration (studied) | (1) Conceptual 6.1.3. (2) Execution 6.1 / 6.1.2. (3) PerspectiveEnvelope (4.1). (4) ModeTransitionGraph (4.2) RO reflect |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | CanvasLayer stack + RefCounted KH checklist |
| Validation | Mode chrome reflects envelope; KH fail aborts hud_active |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 6.1.3 |
| `dispatch_scope` | Execution tertiary **6.1.3** mint (FAST DFS) |

## Module map

| Module | Responsibility |
|--------|----------------|
| `HUDLayerStack` | Base / Mode / Context / Transient layers |
| `HUDLayerRegistry` | Layer id → CanvasLayer |
| `KinestheticHonestyChecklist` | KH-6.1-001..004 gates |
| `ModeChromeReflector` | RO bind to PerspectiveEnvelope |

## Interfaces

```text
KinestheticHonestyChecklist (RefCounted):
  + run_all(ctx: Dictionary) -> Error
  + last_fail_id() -> StringName  # KH-6.1-00N

HUDLayerRegistry (RefCounted):
  + register(layer_id: StringName, node: CanvasLayer) -> Error
  + get_layer(layer_id: StringName) -> CanvasLayer

HUDLayerStack (Node):
  + activate(receipt: PlayRegionMountReceipt, envelope: RefCounted) -> Error
  + registry() -> HUDLayerRegistry
  signals: presentation_hud_active(stack_id), presentation_hud_failed(code)
```

## Pseudo-code

```pseudo
# 6.1.3 — HUDLayerStack / KinestheticHonestyChecklist (Godot 4 stable).
# Citations: Node; CanvasLayer; RefCounted; Error/OK; StringName; signals.
# Reject: HUD driving ModeTransitionGraph; activate without play_region_ready;
#         skipping KH gates; Half B/L5.

class_name HUDLayerStack
extends Node

signal presentation_hud_active(stack_id)
signal presentation_hud_failed(code)

var _registry: HUDLayerRegistry
var _kh: KinestheticHonestyChecklist
var _active: bool = false

func activate(receipt: PlayRegionMountReceipt, envelope: RefCounted) -> Error:
	if receipt == null:
		presentation_hud_failed.emit(&"missing_receipt")
		return ERR_INVALID_PARAMETER
	var err: Error = _kh.run_all({"receipt": receipt, "envelope": envelope})
	if err != OK:
		presentation_hud_failed.emit(_kh.last_fail_id())
		return err
	_ensure_layers()
	_reflect_mode(envelope)
	_active = true
	presentation_hud_active.emit(StringName(str(get_instance_id())))
	return OK

func _ensure_layers() -> void:
	for lid in [&"base", &"mode", &"context", &"transient"]:
		_registry.register(lid, get_node("Layers/%s" % String(lid)))

func _reflect_mode(envelope: RefCounted) -> void:
	# RO: Mode chrome mirrors PerspectiveEnvelope; never owns ModeTransitionGraph.
	pass
```

## Invariants

| ID | Rule |
|----|------|
| I-6.1.3-001 | KH-6.1-001..004 must pass before hud_active |
| I-6.1.3-002 | Mode chrome is RO reflect — not ModeTransitionGraph owner |
| I-6.1.3-003 | activate requires PlayRegionMountReceipt |
| I-6.1.3-004 | Transient layer is the only 6.2 consumer surface |

## Acceptance

- [x] Parallel spine under Phase-6-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.1.3
- [x] Interfaces + tertiary pseudo for HUD/KH
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
