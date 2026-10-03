---
title: Phase 1.1.1 — Session Composer and Layer Graph Bootstrap (Execution)
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-1-Session-Composer-and-Layer-Graph-Bootstrap-Roadmap-2026-06-29-0847]]'
status: active
priority: high
progress: 55
handoff_readiness: 74
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
deepen_complete: true
paint_ux_catalog: true
paint_status: painted
paint_campaign_id: exec-ux-paint-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_world_generation
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- session-composer
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-1-Session-Composer-and-Layer-Graph-Bootstrap-Roadmap-2026-06-29-0847]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.1.1 — Session Composer and Layer Graph Bootstrap (Execution)

Execution tertiary: SessionComposer + LayerGraph bootstrap. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — bootstrap injects world-author seats before `session_bound` so Phase-2 WorldShell can gate accept/regenerate (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Bootstrap four mandatory layers per session; degraded mode if optional missing; teardown reverse order |
| Inspiration / L5 bar (advisory) | Seat injection at bind time — `shared_table` / `dm_as_player` / `privileged_access` available before any world-author API |
| Inspiration (studied) | (1) [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]] — Main→SessionComposer→layers. (2) [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]] / GodotSharpDI session DI scope. (3) [[1-Projects/genesis-mythos-master/Roadmap/Conceptual-Decision-Records/deepen-layer-decoupling-2026-06-26-1200]]. |
| Execution mechanism | `bind_layer_graph` / `teardown_session` with Error/OK + signals + seat/canon inject |
| Validation | Catalog paint DoD met; parent 1.1 checklist advances |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Conceptual 1.1.1 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Bootstrap role | `bind_layer_graph` must inject SeatContext + CanonCommitBoundary **before** `session_bound` |
| `does_not_mandate` | Autoload layers as Session-0 checkbox; players author first world via missing seat inject |
| Pin color keys | Foundation Cyan · Blue (Phase-2 WorldShell) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Seats ready for world author | inject `&"seat"` before `session_bound` | null seat → degraded / unauthorized later | SeatContext |
| Durable session container | four mandatory layers bound | empty layers → ERR_INVALID_PARAMETER | `session_bound` |
| Table can shape (GUI host up) | Presentation layer spawned | missing optional → `session_degraded` | graph_state active/degraded |
| Players do not author first world | seat inject + later InputIntent | wrong seat at WorldShell | none / blocked |
| Retcon / leave shell | `teardown_session` reverse unbind | never Autoload free | `session_torn_down` |

## Interfaces

```text
LayerGraphSpec:
  layers: Array[LayerId]          # mandatory: WORLD_STATE, SIMULATION, PRESENTATION, INPUT_INTENT
  optional_layers: Array[LayerId]
  bus_categories: PackedStringArray

SessionComposer (Node) — bootstrap slice:
  + bind_layer_graph(spec: LayerGraphSpec) -> Error
  + graph_state() -> StringName  # &"active" | &"degraded" | &"torn_down"
  + teardown_session(reason: SessionEndReason) -> void
  signals: session_bound(), session_degraded(code), session_torn_down(reason)
```

## Pseudo-code

```pseudo
# 1.1.1 — LayerGraph bootstrap under SessionComposer (Godot 4 stable).
# Vocab aligned with Phase-1 primary: layers / optional_layers.
# Parent mediates; children emit past-tense signals only.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# Bind order: spawn layers → wire → inject seat/canon/bus → session_bound.
# Without SeatContext inject, Phase-2 WorldShell cannot honest-gate "players do not author first world".
# Anti-mandate: do NOT Autoload layers; session teardown queue_free subtree only.
# Presentation child is the future ux_worldgen_gui host surface (Phase-2 / 2.1.1).
# ===========================================================

func bind_layer_graph(spec: LayerGraphSpec) -> Error:
	if spec == null or spec.layers.is_empty():
		return ERR_INVALID_PARAMETER
	if _graph_state == &"active" or _graph_state == &"degraded":
		return ERR_ALREADY_IN_USE
	for id in spec.layers:
		var layer := _spawn_layer(id)
		if layer == null:
			return ERR_CANT_CREATE
		add_child(layer)
		layer.on_bind(self)
		_layers[id] = layer
	for id in spec.optional_layers:
		if not _layers.has(id):
			session_degraded.emit("missing_optional:%s" % id)
			_graph_state = &"degraded"
	_wire_signals()
	# JUNIOR WORK-ORDER: L5 seats + canon BEFORE session_bound — world-shell consumers require both
	inject_service(&"seat", _seat)
	inject_service(&"canon", _canon)
	inject_service(&"bus", _bus)
	if _seat == null:
		session_degraded.emit("missing_seat_context")
		_graph_state = &"degraded"
	if _graph_state != &"degraded":
		_graph_state = &"active"
	session_bound.emit()  # lasting readable session residue
	return OK

func teardown_session(reason: SessionEndReason) -> void:
	# JUNIOR WORK-ORDER: reverse bind — clear seat services with session; durable world stays on WorldHost
	var keys: Array = _layers.keys()
	keys.reverse()
	for id in keys:
		var layer: Node = _layers[id]
		if layer:
			layer.on_unbind()
	session_torn_down.emit(reason)
	queue_free()  # frees layer children; NEVER Autoload
```

## Edge-case ACs

- [ ] Missing optional layer → `session_degraded` + graph_state `degraded`; mandatory still bound
- [ ] `bind_layer_graph` twice without teardown → `ERR_ALREADY_IN_USE` (or explicit rebind policy logged)
- [ ] Teardown after degraded session still `queue_free`s SessionComposer subtree only
- [x] **UX Catalog paint** — seat inject before `session_bound` as JUNIOR WORK-ORDER (gold pattern)

## Research integration

> "A game should always have an \"entry point\"… In Godot, it's a Main node."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "When autoloading a script… this node will be added to the root viewport before any other scenes are loaded."
> — https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html

> "Finally, when a node is freed… it will also free all its children."
> — https://docs.godotengine.org/en/stable/classes/class_node.html

Links: [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Status

`deepen_complete: true` + **`paint_status: painted`** for Execution **1.1.1** (`exec-ux-paint-20260929`). Next paint: **1.1.2**.
