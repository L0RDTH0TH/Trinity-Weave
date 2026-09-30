---
title: Phase 1.1 — Layer Decoupling and Interface Contracts (Execution)
roadmap-level: secondary
phase-number: 1
subphase-index: "1.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
status: active
priority: high
progress: 45
handoff_readiness: 72
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
- layer-decoupling
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.1 — Layer Decoupling and Interface Contracts (Execution)

Execution secondary for four runtime layers, bus category registry, and canon-commit boundary. Parallel spine under `Roadmap/Execution/Phase-1-…/Phase-1-1-…/`. **No Half B code.** L5/SERIES are **read-only advisory feedstock** — layer contracts + canon gate **enable** world-shell seats/guards (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Named runtime layers with explicit contracts; session-scoped composition; bus taxonomy + read-only canon gate ([[conceptual 1.1#Behavior]]) |
| Inspiration / L5 bar (advisory) | Seats + "players do not author first world" + DM-retconnable canon — enforced at InputIntent / CanonCommitBoundary before Phase-2 WorldShell |
| Inspiration (studied) | (1) [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]] / GodotSharpDI — DI Scope bound to scene-tree / mission lifecycle → SessionComposer children. (2) Same research / Ikki World Kernel — rules+roles+tone before play → seed/dry-run before canon. (3) [[1-Projects/genesis-mythos-master/Roadmap/Conceptual-Decision-Records/deepen-layer-decoupling-2026-06-26-1200]] — four layers + bus nouns. |
| Execution mechanism | Typed GDScript interfaces + pseudo for SessionComposer, BusCategoryRegistry, CanonCommitBoundary; layers as session children |
| Validation signal | Catalog paint DoD met; tertiaries 1.1.1–1.1.3 inherit pattern |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Frozen conceptual 1.1 + tertiaries 1.1.1–1.1.3 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Layer enablement | Presentation hosts GUI; InputIntent carries seat; CanonCommitBoundary blocks player world-author; WorldState holds durable projections |
| `does_not_mandate` | players author first world; Session-0-checkbox-only Autoload layers; unconstrained fresh-noise |
| Pin color keys | Foundation Cyan · Blue (downstream Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Players do not author first world | `IInputIntentLayer.route_intent` + seat check | player seat → ERR_UNAUTHORIZED | intent rejected |
| Table can shape / DM retcon | `CanonCommitBoundary.accept` / reject | not_proposed → reject | fact_accepted / fact_rejected |
| Durable truth before sim | `hook` only after accept | sim write before hook banned | HOOKED stage |
| Collaborative dialogue host | `IPresentationLayer` + `session.*` bus | Presentation must not mutate Simulation | scaffold signals |
| World-shell seat inject | SessionComposer `inject_service(&"seat")` | missing seat → degraded | SeatContext |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SessionComposer` | Bind LayerGraph; inject bus + canon services; teardown |
| `LayerGraphSpec` | Mandatory/optional LayerId slots |
| `BusCategoryRegistry` | Topic namespaces `canon.*` / `sim.*` / `session.*` / `presentation.*` |
| `CanonCommitBoundary` | propose → dry-run → accept; blocks sim until hooked |
| `ILayer` ×4 | WorldState / Simulation / Presentation / InputIntent contracts |

## Interfaces

```text
enum LayerId { WORLD_STATE, SIMULATION, PRESENTATION, INPUT_INTENT }

BusCategoryRegistry (RefCounted / Object):
  + register_category(ns: StringName, owner: LayerId) -> Error
  + assert_topic(topic: StringName, owner: LayerId) -> Error
  + manifest() -> PackedStringArray
  signals: categories_ready(), category_rejected(topic, reason)

CanonCommitBoundary (Object, injected):
  + propose(fact: CanonProposal) -> Dictionary  # dry-run estimate; no side effects
  + accept(fact_id: StringName) -> Error       # proposed→accepted only
  + hook(fact_id: StringName) -> Error         # accepted→hooked → sim-eligible
  + is_accepted(fact_id: StringName) -> bool  # ACCEPTED|HOOKED — generation reads
  + is_sim_write_allowed(fact_id: StringName) -> bool  # HOOKED only — sim writes
  signals: fact_proposed(id), fact_rejected(id, reason), fact_accepted(id), fact_hooked(id)

IWorldStateLayer (Node):
  + on_bind(composer) -> void
  + on_unbind() -> void
  + on_sim_event(ev: Dictionary) -> void
  + request_projection(handle: StringName) -> Variant
  # MUST NOT mutate Presentation or Autoload globals

ISimulationLayer (Node):
  + on_bind(composer) -> void
  + on_unbind() -> void
  + tick(dt: float) -> void
  + apply_canon(fact_id: StringName) -> Error  # only if boundary.is_sim_write_allowed
  signals: sim_event_emitted(ev)

IPresentationLayer (Node):
  + on_bind(composer) -> void
  + on_unbind() -> void
  + bind_projection(handle: StringName, payload: Variant) -> void
  # MUST NOT call Simulation mutate APIs directly

IInputIntentLayer (Node):
  + on_bind(composer) -> void
  + on_unbind() -> void
  + route_intent(envelope: Dictionary) -> Error  # via CanonCommitBoundary before sim
```

## Pseudo-code

```pseudo
# Phase 1.1 — layer decoupling (Godot 4 stable Error/OK + signals).
# Citations: docs.godotengine.org/en/stable/ (Node, Autoload, scene organization, signals).
# Reject: Autoload gameplay layers; Result[T,E]; sibling hard NodePaths.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# CanonCommitBoundary + InputIntent seat checks ENABLE "players do not author first world".
# Accept/hook path is DM-retconnable foundation for Phase-2 ConflictArbiter / WorldShell.
# Presentation may host ux_worldgen_gui; MUST NOT mutate Simulation (table shapes via intent/canon).
# session.* / canon.* bus topics carry seat and scaffold residues to Phase-2 consumers.
# ===========================================================

class_name BusCategoryRegistry
extends RefCounted

signal categories_ready
signal category_rejected(topic, reason)

var _owners: Dictionary = {}  # StringName -> LayerId

func register_category(ns: StringName, owner: LayerId) -> Error:
	if String(ns).is_empty():
		return ERR_INVALID_PARAMETER
	if _owners.has(ns) and _owners[ns] != owner:
		category_rejected.emit(ns, "owner_conflict")
		return ERR_ALREADY_IN_USE
	_owners[ns] = owner
	return OK

func assert_topic(topic: StringName, owner: LayerId) -> Error:
	var ns := StringName(String(topic).get_slice(".", 0) + ".*")
	# coarse ns check — fine topics validated in 1.1.2 tertiary
	if not _owners.has(ns) and not _owners.has(topic):
		category_rejected.emit(topic, "unknown_category")
		return ERR_DOES_NOT_EXIST
	return OK


class_name CanonCommitBoundary
extends RefCounted

signal fact_proposed(id)
signal fact_rejected(id, reason)
signal fact_accepted(id)
signal fact_hooked(id)

enum Stage { PROPOSED, ACCEPTED, HOOKED, REJECTED }
var _stage: Dictionary = {}  # StringName -> Stage
var _seat: SeatContext       # injected — L5 world-author seats

func propose(fact: Dictionary) -> Dictionary:
	# JUNIOR WORK-ORDER: table may propose; not yet durable living-world law
	var id: StringName = fact.get("id", &"")
	if id == &"":
		return {"ok": false, "error": ERR_INVALID_PARAMETER}
	_stage[id] = Stage.PROPOSED
	fact_proposed.emit(id)
	# dry-run estimate only — no WorldState / Simulation mutation
	return {"ok": true, "id": id, "estimate": fact.get("estimate", {})}

func accept(fact_id: StringName) -> Error:
	# JUNIOR WORK-ORDER: refuse player seat — players do not author first world / lasting canon
	if _seat != null and not _seat.allows_any(["shared_table", "dm_as_player", "privileged_access"]):
		fact_rejected.emit(fact_id, "wrong_seat")
		return ERR_UNAUTHORIZED
	if _stage.get(fact_id) != Stage.PROPOSED:
		fact_rejected.emit(fact_id, "not_proposed")
		return ERR_INVALID_PARAMETER
	_stage[fact_id] = Stage.ACCEPTED
	fact_accepted.emit(fact_id)  # durable accepted-fact signal
	return OK

func hook(fact_id: StringName) -> Error:
	# JUNIOR WORK-ORDER: only hooked facts may hit Simulation — durable gate before world-hitting sim
	if _stage.get(fact_id) != Stage.ACCEPTED:
		return ERR_INVALID_PARAMETER
	_stage[fact_id] = Stage.HOOKED
	fact_hooked.emit(fact_id)
	return OK

func is_accepted(fact_id: StringName) -> bool:
	var st = _stage.get(fact_id, Stage.PROPOSED)
	return st == Stage.ACCEPTED or st == Stage.HOOKED

func is_sim_write_allowed(fact_id: StringName) -> bool:
	return _stage.get(fact_id) == Stage.HOOKED

# SessionComposer.bind_layer_graph — see Execution Phase-1 primary.
# After bind: inject BusCategoryRegistry + CanonCommitBoundary + SeatContext via inject_service.
# Parent connects layer signals; children emit past-tense only.
# JUNIOR WORK-ORDER: IInputIntentLayer.route_intent must call seat check before boundary.accept.
```

## Acceptance criteria (execution)

- [x] Parallel spine path under `Execution/Phase-1-…/Phase-1-1-…/` (not flat)
- [x] Path-qualified `conceptual_counterpart` → conceptual 1.1
- [x] Interfaces + pseudo for BusCategoryRegistry + CanonCommitBoundary + four ILayer surfaces
- [x] **UX Catalog paint** — L5 seats/guards in JUNIOR WORK-ORDER (layer enablement for world-shell)
- [x] Godot stable citations in Research integration (whitelist)
- [x] Tertiary execution mirrors 1.1.1 / 1.1.2 / 1.1.3 minted
- [x] Edge-case ACs drafted on each tertiary (unchecked items = Half B / playable later)

## Research integration

### Key takeaways

- SessionComposer owns layer children; freeing SessionComposer frees layers (Node tree).
- Autoload gameplay layers forbidden; Autoloads must never be `queue_free`d.
- Ancestor mediates sibling communication (SessionComposer `.connect`).
- Fallible APIs return GlobalScope `Error` / `OK`; custom signals declared on owner.

### Verbatim anchors

> "Finally, when a node is freed with Object.free() or queue_free(), it will also free all its children."
> — https://docs.godotengine.org/en/stable/classes/class_node.html

> "Warning: Autoloads must not be removed using free() or queue_free() at runtime, or the engine will crash."
> — https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html

> "Nodes which are siblings should only be aware of their own hierarchies while an ancestor mediates their communications and references."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "OK = 0 — Methods that return Error return OK when no error occurred."
> — https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#enum-globalscope-error

> "To use signals you need to connect them first… define a custom signal… signal my_signal"
> — https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html

### Links

- [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Subphase next (execution DFS)

1. ~~Paint **1.1**~~ done.
2. Paint **1.1.1** (this wave) then **1.1.2** / **1.1.3** / **1.2**.

## Status

`deepen_complete: true` + **`paint_status: painted`** for Execution **1.1** (`exec-ux-paint-20260929`). Foundation enables world-shell seats.
