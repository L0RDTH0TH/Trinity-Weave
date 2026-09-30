---
title: Phase 1 — Conceptual Foundation and Core Architecture (Execution)
roadmap-level: primary
phase-number: 1
subphase-index: "1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
status: active
priority: high
progress: 85
handoff_readiness: 68
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
repair_pending: false
deepen_complete: phase1_tree_complete
ira_applied: true
paint_ux_catalog: true
paint_status: painted
paint_campaign_id: exec-ux-paint-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_world_generation
created: 2026-09-28
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
- '[[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]'
---

# Phase 1 — Conceptual Foundation and Core Architecture (Execution)

Execution primary for session-scoped layer graph, proc-gen DAG host contracts, and modularity/safety seams. Parallel spine mirrors conceptual Phase-1. **No Half B code.** L5/SERIES are **read-only advisory feedstock** (`ux_world_generation` / `pkg_world_shell`) — SessionComposer/layers **enable** world-shell seats; paint meaning into junior work-order pseudo (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Decouple WorldState / Simulation / Presentation / InputIntent; compose per session; seed-snapshot + dry-run before canon commit ([[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914#Behavior]]) |
| Inspiration / L5 bar (advisory) | `ux_world_generation` seats `shared_table` / `dm_as_player` / `privileged_access` — injected via session services so Phase-2 WorldShell can gate accept/regenerate |
| Inspiration (studied) | (1) [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]] / GodotSharpDI — DI Scope bound to scene-tree / mission lifecycle; session-scoped services cleared on exit → maps to SessionComposer children, not Autoload gameplay loops. (2) Same research / Ikki World Kernel — rules+roles+tone as generative substrate **before** play → supports seed-snapshot + dry-run before canon commit. (3) [[1-Projects/genesis-mythos-master/Roadmap/User-Story/Inspiration-UX-Feedstock/cards/session-prep-accelerator-loop]] — session-boundary prep loop (session host lifetime). CDR evidence (not sole inspiration): [[1-Projects/genesis-mythos-master/Roadmap/Conceptual-Decision-Records/deepen-layer-decoupling-2026-06-26-1200]]. |
| Execution mechanism | Long-lived `SessionComposer` Node under Main; four layers as **session children** (not Autoloads); bus + seam registry as injected services; StageDAG host interfaces owned by secondary 1.2 |
| Validation signal | Catalog paint DoD met on this note; secondaries 1.1–1.3 inherit paint pattern; Half B later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory — foundation enables world-shell seats) |
| `package_id` | `pkg_world_shell` (advisory package context) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Phase-1 primary + secondaries 1.1–1.3 (frozen conceptual) |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Label | DM can create (table can shape) a persistent living world |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Foundation role | SessionComposer injects `SeatContext` + CanonCommitBoundary so Phase-2 WorldShell / InputIntent can refuse player authoring of first world |
| `does_not_mandate` | one-world=one-campaign; Session-0-checkbox-only; players author first world; unconstrained fresh-noise; default-next = PC creation |
| Pin color keys | Foundation Cyan (session host) · Blue (Phase-2 Behavior downstream) |

### Moment → module map (junior)

| L5 moment / clause | Module / API (Phase-1) | Guard | Residue |
|--------------------|------------------------|-------|---------|
| Seats for world author | `SessionComposer.inject_service(&"seat", SeatContext)` | missing seat → world-shell blocked upstream | session-scoped SeatContext |
| Players do not author first world | InputIntentLayer + CanonCommitBoundary before sim/world write | player seat → refuse accept path (Phase-2 consumes) | `session.*` / `canon.*` bus |
| Table can shape | PresentationLayer hosts `ux_worldgen_gui` dialogue; session bus | wrong seat | scaffold preview signals |
| Durable container after accept | WorldStateLayer projections + CanonCommitBoundary accept/hook | dry-run / propose-only | accepted/hooked facts |
| Every world-hitting change DM-retconnable | CanonCommitBoundary reject + session teardown/rebind | silent Autoload mutate banned | provenance via seams (1.3) |
| Import/attach first-class | session services stay available across WorldShell attach | — | same SeatContext / canon |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SessionComposer` | Session composition root; binds LayerGraph; mediates sibling refs; owns teardown |
| `WorldStateLayer` | Append-only projections / query handles — no Presentation mutation |
| `SimulationLayer` | Deterministic tick + domain events; respects CanonCommitBoundary |
| `PresentationLayer` | FP / DM rail shells; subscribes to projections only |
| `InputIntentLayer` | Agency envelopes → Simulation only after canon gate |
| `BusCategoryRegistry` | Topic namespaces `canon.*` / `sim.*` / `session.*` / `presentation.*` (detail → 1.1) |
| `StageDAGHost` | Proc-gen stage graph host API (detail → 1.2) |
| `SeamRegistry` + `SeedSnapshotAuthority` + `DryRunValidator` | Modularity + safety (detail → 1.3) |

## Interfaces

```text
SessionComposer (Node):
  + bind_layer_graph(spec: LayerGraphSpec) -> Error
  + layer(id: LayerId) -> Node?          # mediated lookup only
  + inject_service(name: StringName, svc: Object) -> void
  + teardown_session(reason: SessionEndReason) -> void  # emit torn_down then queue_free
  signals: session_bound(), session_degraded(code), session_torn_down(reason)

LayerGraphSpec:
  layers: Array[LayerId]   # WorldState, Simulation, Presentation, InputIntent
  bus_categories: PackedStringArray
  optional_layers: Array[LayerId]  # may emit session.degraded

ILayer (Node contract):
  + on_bind(composer: SessionComposer) -> void
  + on_unbind() -> void

CanonCommitBoundary (service, injected):
  + propose(fact: CanonProposal) -> Dictionary  # dry-run estimate fields
  + accept(fact_id: StringName) -> Error        # proposed→accepted
  + hook(fact_id: StringName) -> Error          # accepted→hooked
  + is_accepted(fact_id: StringName) -> bool    # ACCEPTED|HOOKED — generation/intent reads
  + is_sim_write_allowed(fact_id: StringName) -> bool  # HOOKED only — Simulation mutators
```

## Pseudo-code

```pseudo
# SessionComposer — citation authority: Godot 4 stable docs (Research integration).
# Prefer Main → SessionComposer → {WorldState, Simulation, Presentation, InputIntent}.
# Do NOT Autoload the four gameplay layers.
# Returns use GlobalScope Error / OK — not foreign Result[T,E].
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory foundation) ===
# This Phase-1 host ENABLES world-shell seats — it does not mint WorldShell itself (Phase-2).
# Inject SeatContext (shared_table | dm_as_player | privileged_access) before any world-author API.
# Players do not author the first world: InputIntent + CanonCommitBoundary refuse player seat writes.
# Presentation hosts ux_worldgen_gui dialogue; WorldState holds durable projections after accept.
# Anti-mandate: do NOT Autoload layers as Session-0 checkbox with no session container.
# Teardown clears seat/canon services with the session — lasting world lives under Phase-2 WorldHost.
# ===========================================================

class_name SessionComposer
extends Node

signal session_bound
signal session_degraded(code)
signal session_torn_down(reason)

var _layers: Dictionary = {}   # LayerId -> Node
var _bus: BusCategoryRegistry
var _canon: CanonCommitBoundary
var _seat: SeatContext         # JUNIOR WORK-ORDER: L5 seats for Phase-2 WorldShell

func bind_layer_graph(spec: LayerGraphSpec) -> Error:
	if spec == null or spec.layers.is_empty():
		return ERR_INVALID_PARAMETER
	for id in spec.layers:
		var layer := _spawn_layer(id)
		add_child(layer)                 # session-scoped lifetime
		layer.on_bind(self)
		_layers[id] = layer
	_wire_signals()                      # ancestor mediates; no hard sibling paths
	# JUNIOR WORK-ORDER: inject seat + canon before session_bound — world-shell consumers require both
	inject_service(&"seat", _seat)
	inject_service(&"canon", _canon)
	inject_service(&"bus", _bus)
	for opt in spec.optional_layers:
		if not _layers.has(opt):
			session_degraded.emit("missing_optional:%s" % opt)
	session_bound.emit()  # lasting readable session state (L5 residue pattern at session altitude)
	return OK

func _wire_signals() -> void:
	# Parent connects; children emit past-tense events only
	var sim: Node = _layers.get(LayerId.SIMULATION)
	var ws: Node = _layers.get(LayerId.WORLD_STATE)
	if sim and ws:
		sim.sim_event_emitted.connect(ws.on_sim_event)

func require_world_author_seat() -> Error:
	# JUNIOR WORK-ORDER: refuse player seat — table may shape; players do not create first world
	if _seat == null or not _seat.allows_any(["shared_table", "dm_as_player", "privileged_access"]):
		session_degraded.emit("wrong_seat")
		return ERR_UNAUTHORIZED
	return OK

func teardown_session(reason: SessionEndReason) -> void:
	# JUNIOR WORK-ORDER: clear session seat/services — durable world remains under Phase-2 WorldHost
	for id in _layers.keys():
		var layer: Node = _layers[id]
		if layer:
			layer.on_unbind()
	session_torn_down.emit(reason)
	# Frees this node AND all layer children — never free Autoloads
	queue_free()

# Forbidden patterns (engine / architecture):
# - Autoload WorldStateLayer / SimulationLayer / …
# - free() / queue_free() on Autoload singletons
# - Presentation mutating Simulation directly
# - Result[T,E] / Ok() as if native GDScript (use Error / OK)
# JUNIOR WORK-ORDER: never Autoload SeatContext as global player-author bypass
```

## Acceptance criteria (execution — stub→playable ladder)

- [x] Parallel spine note under `Roadmap/Execution/Phase-1-…/` (not flat heap)
- [x] Path-qualified `conceptual_counterpart` → conceptual Phase-1 (exclude Execution/)
- [x] Pseudo-code + interfaces for SessionComposer / layer bind / teardown (Error/OK + declared signals)
- [x] **UX Catalog paint** — L5 seats/guards bound as JUNIOR WORK-ORDER (foundation enables world-shell)
- [x] Godot stable verbatim citations in Research integration (incl. Error + signals)
- [x] Studied inspiration anchors split from L5/package advisory
- [x] Secondary execution mirror **1.1** minted
- [x] Secondary execution mirrors 1.2 / 1.3 minted
- [x] Tertiary notes 1.1.1–1.1.3 with edge-case ACs under secondary 1.1
- [ ] `execution_factory_handoff_ready` / Half B later

## Research integration

### Key takeaways

- SessionComposer = session composition root; four layers as children whose lifetime matches the session (`queue_free` parent frees layers).
- Prefer `Main → SessionComposer → {WorldState, Simulation, Presentation, InputIntent}`; do **not** collapse layers into one Autoload.
- Autoload only for self-contained broad managers; systems that modify other systems' data stay as regular nodes/scenes.
- Never `free`/`queue_free` Autoloads; session teardown frees SessionComposer subtree only.
- Cross-layer: ancestor mediates; child emits past-tense signals; parent connects / injects callables or Node refs.
- Use `class_name … extends Node` for typed layer APIs; use GlobalScope `Error` / `OK` for fallible APIs (not foreign `Result`).
- WorldShell / level swaps stay Phase-2; this deepen is session layer graph only.

### Decisions / constraints

- **Reject Autoload for WorldState / Simulation / Presentation / InputIntent.**
- SessionComposer mediates sibling layer refs (no hard cross-layer NodePaths).
- Layers `emit` past-tense events; SessionComposer declares + owns `.connect` after bind.
- Teardown emits `session_torn_down` then `SessionComposer.queue_free()` — never Autoload nodes.

### Verbatim anchors

> "Finally, when a node is freed with Object.free() or queue_free(), it will also free all its children."
> — https://docs.godotengine.org/en/stable/classes/class_node.html

> "Warning: Autoloads must not be removed using free() or queue_free() at runtime, or the engine will crash."
> — https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html

> "If you have systems that modify other systems' data, you should define those as their own scripts or scenes, rather than autoloads."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "Nodes which are siblings should only be aware of their own hierarchies while an ancestor mediates their communications and references."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "OK = 0 — Methods that return Error return OK when no error occurred."
> — https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#enum-globalscope-error

> "To use signals you need to connect them first… define a custom signal… signal my_signal"
> — https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html

### Links

- [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]
- [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]

## Subphase next (execution DFS)

1. ~~Mint Phase-1 tree~~ done.
2. ~~Paint Phase-1 primary~~ done (`paint_ux_catalog: true`).
3. Paint wave continues **1.1** / **1.1.1** then **1.1.2** / **1.1.3** / **1.2**.

## Status

`deepen_complete: phase1_tree_complete` + **`paint_status: painted`** (`exec-ux-paint-20260929`). Advisory `pkg_world_shell` / `ux_world_generation` — foundation enables world-shell seats. Paint ≠ mint L5 files.
