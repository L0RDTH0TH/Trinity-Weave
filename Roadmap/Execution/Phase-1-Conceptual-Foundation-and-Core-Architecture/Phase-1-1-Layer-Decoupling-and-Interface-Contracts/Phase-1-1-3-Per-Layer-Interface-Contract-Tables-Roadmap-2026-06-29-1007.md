---
title: Phase 1.1.3 — Per-Layer Interface Contract Tables (Execution)
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roadmap-2026-06-29-1007]]'
status: active
priority: high
progress: 60
handoff_readiness: 76
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
- interface-contracts
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roadmap-2026-06-29-1007]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.1.3 — Per-Layer Interface Contract Tables (Execution)

Execution tertiary: typed per-layer contracts + cross-layer invariants. Closes execution **1.1** tertiary wave. **No Half B.** L5/SERIES are **read-only advisory feedstock** — per-layer tables **enable** world-shell seats/guards (Presentation hosts GUI; InputIntent seat-routes; WorldState durable projections).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Per-layer upstream/downstream guarantees as callable GDScript surfaces |
| Inspiration / L5 bar (advisory) | Table can shape via Presentation/InputIntent; players do not author first world; durable WorldState after accept |
| Inspiration (studied) | (1) Conceptual 1.1.3 contract tables. (2) [[1-Projects/genesis-mythos-master/Roadmap/Conceptual-Decision-Records/deepen-layer-decoupling-2026-06-26-1200]]. (3) [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]. |
| Execution mechanism | Four ILayer tables + `ContractTableCurator` bind after graph+bus ready |
| Validation | Catalog paint DoD met; cross-layer invariants checklist |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Conceptual 1.1.3 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Layer→L5 map | Presentation = ux_worldgen_gui host · InputIntent = seat gate · WorldState = durable projections · Simulation = hooked-only writes |
| `does_not_mandate` | Presentation mutates Simulation; players author via silent InputIntent; Autoload layers |
| Pin color keys | Foundation Cyan · Blue (Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Collaborative dialogue host | `IPresentationLayer.bind_projection` / view mode | no Simulation mutate API | presentation.* |
| Players do not author first world | `IInputIntentLayer.route_intent` + seat | wrong seat → ERR_UNAUTHORIZED | canon.* propose only |
| Durable living world projections | `IWorldStateLayer.request_projection` | append-only | projection handles |
| World-hitting sim changes retconnable | `ISimulationLayer.apply_canon` + hook gate | not hooked → unauthorized | sim_event_emitted |
| Table can shape | InputIntent → CanonCommitBoundary | Presentation never direct-writes WorldState | accepted/hooked facts |

## Per-layer contract tables

### WorldStateLayer

| Guarantee | Downstream expectation |
|-----------|------------------------|
| Append-only projections from `sim.*` / hooked canon | Simulation + Presentation read via `request_projection` only |
| No Presentation mutation | No Autoload writes |

```text
+ on_bind(composer) -> void
+ on_unbind() -> void
+ on_sim_event(ev: Dictionary) -> void
+ request_projection(handle: StringName) -> Variant
+ snapshot_mark(label: StringName) -> Error
```

### SimulationLayer

| Guarantee | Downstream expectation |
|-----------|------------------------|
| Deterministic `tick`; no render tree mutation | Emits `sim_event_emitted`; respects CanonCommitBoundary |
| Applies only hooked facts | Presentation never calls mutate APIs |

```text
+ on_bind(composer) -> void
+ on_unbind() -> void
+ tick(dt: float) -> void
+ apply_canon(fact_id: StringName) -> Error
signals: sim_event_emitted(ev)
```

### PresentationLayer

| Guarantee | Downstream expectation |
|-----------|------------------------|
| FP / DM shells subscribe to projections | Routes intents upward via InputIntent only |
| Mode graph local; **ux_worldgen_gui host surface** | Never mutates Simulation / WorldState directly |

```text
+ on_bind(composer) -> void
+ on_unbind() -> void
+ bind_projection(handle: StringName, payload: Variant) -> void
+ set_view_mode(mode: StringName) -> Error
```

### InputIntentLayer

| Guarantee | Downstream expectation |
|-----------|------------------------|
| Agency envelopes validated + **seat check** | Routes through CanonCommitBoundary before Simulation |
| No silent sim writes | Bus publish under `canon.*` / `session.*` only |

```text
+ on_bind(composer) -> void
+ on_unbind() -> void
+ route_intent(envelope: Dictionary) -> Error
```

## Cross-layer invariants

1. Sibling layers: no hard NodePaths — SessionComposer injects refs / connects signals.
2. Canon gate: Simulation `apply_canon` requires `is_sim_write_allowed`.
3. Degraded session: missing optional layer propagates `session_degraded`; mandatory tables still bind.
4. Teardown: discard contract tables with graph; never free Autoloads.
5. **L5:** InputIntent seat refuse + Presentation no-sim-mutate preserve "players do not author first world".

## Pseudo-code

```pseudo
# 1.1.3 — Per-layer contract tables (Godot 4 stable).
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# Presentation hosts collaborative worldgen GUI — NEVER mutate Simulation/WorldState.
# InputIntent.route_intent MUST seat-check before CanonCommitBoundary.accept.
# WorldState holds durable projections after hooked canon / Phase-2 accept.
# Simulation.apply_canon only when is_sim_write_allowed (DM-retconnable hook path).
# ===========================================================

class_name ContractTableCurator
extends RefCounted

signal contract_tables_bound

func bind_after_ready(composer: SessionComposer, bus: BusCategoryRegistry) -> Error:
	if composer.graph_state() == &"torn_down":
		return ERR_INVALID_PARAMETER
	if bus.manifest().is_empty():
		return ERR_DOES_NOT_EXIST
	# JUNIOR WORK-ORDER: tables document L5 layer duties for junior implementers
	composer.inject_service(&"ContractTables", self)
	contract_tables_bound.emit()
	return OK

func IInputIntentLayer.route_intent(envelope: Dictionary) -> Error:
	# JUNIOR WORK-ORDER: refuse player seat — players do not author first world
	var seat: SeatContext = composer.service(&"seat")
	if seat == null or not seat.allows_any(["shared_table", "dm_as_player", "privileged_access"]):
		return ERR_UNAUTHORIZED
	return composer.service(&"canon").propose(envelope).get("ok", false) and OK or ERR_BUSY

func ISimulationLayer.apply_canon(fact_id: StringName) -> Error:
	# JUNIOR WORK-ORDER: world-hitting change only after hook (retconnable promote)
	var boundary: CanonCommitBoundary = composer.service(&"canon")
	return SimWriteGuard.apply_if_allowed(boundary, fact_id, Callable(self, "_mutate_from_canon"))
```

## Edge-case ACs

- [ ] Presentation calling Simulation mutate → documented forbid (lint/review gate; no API exposed)
- [ ] Degraded session still binds WorldState+Simulation+Presentation+InputIntent mandatory contracts
- [ ] `contract_tables_bound` only after bus `categories_ready`
- [x] **UX Catalog paint** — L5 layer duties as JUNIOR WORK-ORDER (gold pattern)

## Research integration

> "Each subsystem within your game should have its own section within the SceneTree."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "If you have systems that modify other systems' data, you should define those as their own scripts or scenes, rather than autoloads."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "Warning: Autoloads must not be removed using free() or queue_free() at runtime…"
> — https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html

Links: [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Status

`deepen_complete: true` + **`paint_status: painted`** (`exec-ux-paint-20260929`). **1.1 tertiary paint complete.** Next: **1.2**.
