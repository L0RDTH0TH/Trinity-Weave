---
title: Phase 6.1.2 — PlayRegionHost Mount Lifecycle (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
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
- play-region
- mount-lifecycle
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 6.1.2 — PlayRegionHost Mount Lifecycle (Execution)

Execution tertiary: **PlayRegionHost** mount + rig sockets + **PlayRegionMountReceipt** + `presentation_play_region_ready`. Prereq: 6.1.1 launch_complete. HUD → **6.1.3**. Parallel spine under `Execution/Phase-6-…/Phase-6-1-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Single PlayRegion mount + sockets after launch ([[conceptual 6.1.2]]) |
| Inspiration (studied) | (1) Conceptual 6.1.2. (2) Execution 6.1 / 6.1.1. (3) PerspectiveEnvelope (4.1). (4) SeamRegistry (1.3) |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | Node host; single-active viewport; MountContractGlue ids for 6.2/6.3 |
| Validation | Duplicate ready → `duplicate_play_region`; fail rollback |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 6.1.2 |
| `dispatch_scope` | Execution tertiary **6.1.2** mint (FAST DFS) |

## Module map

| Module | Responsibility |
|--------|----------------|
| `PlayRegionHost` | Single viewport + socket table |
| `PlayRegionMountReceipt` | Mount id + handle echo |
| `RigSocketTable` | fp_baseline_rig, dm_worldcam_slot; mapcam stub |
| `MountLifecycle` | idle → mounting → ready \| failed |

## Interfaces

```text
PlayRegionMountReceipt (RefCounted):
  + mount_id: StringName
  + session_id: StringName
  + host_instance_id: int

PlayRegionHost (Node):
  + ensure_single_viewport() -> Error
  + mount(handle: PresentationSessionHandle) -> Error
  + receipt() -> PlayRegionMountReceipt
  + socket(name: StringName) -> Node
  signals: presentation_play_region_ready(host_id), presentation_play_region_failed(code)
```

## Pseudo-code

```pseudo
# 6.1.2 — PlayRegionHost Mount Lifecycle (Godot 4 stable).
# Citations: Node; RefCounted; Error/OK; StringName; signals.
# Reject: second concurrent PlayRegion; mount without launch_complete;
#         HUD ownership (6.1.3); demo content (6.2); Half B/L5.

class_name PlayRegionHost
extends Node

signal presentation_play_region_ready(host_id)
signal presentation_play_region_failed(code)

var _ready: bool = false
var _receipt: PlayRegionMountReceipt
var _sockets: Dictionary = {}

func mount(handle: PresentationSessionHandle) -> Error:
	if handle == null:
		presentation_play_region_failed.emit(&"missing_handle")
		return ERR_INVALID_PARAMETER
	if _ready:
		presentation_play_region_failed.emit(&"duplicate_play_region")
		return ERR_ALREADY_EXISTS
	var err: Error = ensure_single_viewport()
	if err != OK:
		presentation_play_region_failed.emit(&"viewport_fail")
		return err
	_bind_sockets()
	_receipt = PlayRegionMountReceipt.new()
	_receipt.mount_id = StringName("pr_%s" % str(get_instance_id()))
	_receipt.session_id = handle.session_id
	_receipt.host_instance_id = get_instance_id()
	_ready = true
	presentation_play_region_ready.emit(get_instance_id())
	return OK

func ensure_single_viewport() -> Error:
	# Exactly one SubViewport under this host; fail closed otherwise.
	return OK

func _bind_sockets() -> void:
	_sockets[&"fp_baseline_rig"] = get_node_or_null("Sockets/FPBaseline")
	_sockets[&"dm_worldcam_slot"] = get_node_or_null("Sockets/DMWorldCam")
	# mapcam stub intentionally null until Phase-4 mapcam wire
```

## Invariants

| ID | Rule |
|----|------|
| I-6.1.2-001 | Single-active PlayRegion only |
| I-6.1.2-002 | Mount requires valid PresentationSessionHandle |
| I-6.1.2-003 | Duplicate ready emits `duplicate_play_region` |
| I-6.1.2-004 | Does not init HUDLayerStack |

## Acceptance

- [x] Parallel spine under Phase-6-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.1.2
- [x] Interfaces + tertiary pseudo for Host/Receipt/sockets
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
