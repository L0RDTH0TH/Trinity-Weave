---
title: Phase 1 — Conceptual Foundation and Core Architecture (Execution)
roadmap-level: primary
phase-number: 1
subphase-index: "1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
status: active
priority: high
progress: 35
handoff_readiness: 68
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-28
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase
- execution
para-type: Project
links:
- '[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1 — Conceptual Foundation and Core Architecture (Execution)

Execution primary for session-scoped layer graph, proc-gen DAG host contracts, and modularity/safety seams. Parallel spine mirrors conceptual Phase-1. **No Half B code. No L5 / factory.** Package cursor deferred until phase-order walk leaves Phase 1.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Decouple WorldState / Simulation / Presentation / InputIntent; compose per session; seed-snapshot + dry-run before canon commit ([[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914#Behavior]]) |
| Inspiration / L5 bar | _(none this slice — phase-order foundation; no package pin)_ |
| Execution mechanism | Long-lived `SessionComposer` Node under Main; four layers as **session children** (not Autoloads); bus + seam registry as injected services; StageDAG host interfaces owned by secondary 1.2 |
| Validation signal | Secondaries 1.1–1.3 execution mirrors carry layer / DAG / seam interfaces; playable exit remains Half B later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | _(empty — phase-order walk; no package)_ |
| `package_id` | _(cleared)_ |
| `l5_path` | _(n/a — no L5 this deepen)_ |
| `conceptual_pin` | Phase-1 primary + secondaries 1.1–1.3 (frozen conceptual) |
| `dispatch_scope` | Execution Phase-1 **primary** refine only (single structural artifact) |

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
  + bind_layer_graph(spec: LayerGraphSpec) -> Result[void, ComposeError]
  + layer(id: LayerId) -> Node?          # mediated lookup only
  + inject_service(name: StringName, svc: Object) -> void
  + teardown_session(reason: SessionEndReason) -> void  # queue_free self
  signals: session_bound(), session_degraded(code), session_torn_down(reason)

LayerGraphSpec:
  layers: Array[LayerId]   # WorldState, Simulation, Presentation, InputIntent
  bus_categories: PackedStringArray
  optional_layers: Array[LayerId]  # may emit session.degraded

ILayer (Node contract):
  + on_bind(composer: SessionComposer) -> void
  + on_unbind() -> void

CanonCommitBoundary (service, injected):
  + propose(fact: CanonProposal) -> DryRunEstimate
  + accept(fact_id: StringName) -> Result[void, CanonError]  # only accepted → gen/sim
```

## Pseudo-code

```pseudo
# SessionComposer — citation authority: Godot 4 stable docs (Research integration).
# Prefer Main → SessionComposer → {WorldState, Simulation, Presentation, InputIntent}.
# Do NOT Autoload the four gameplay layers.

class_name SessionComposer
extends Node

var _layers: Dictionary = {}   # LayerId -> Node
var _bus: BusCategoryRegistry
var _canon: CanonCommitBoundary

func bind_layer_graph(spec: LayerGraphSpec) -> Result:
    for id in spec.layers:
        var layer := _spawn_layer(id)
        add_child(layer)                 # session-scoped lifetime
        layer.on_bind(self)
        _layers[id] = layer
    _wire_signals()                      # ancestor mediates; no hard sibling paths
    for opt in spec.optional_layers:
        if not _layers.has(opt):
            session_degraded.emit("missing_optional:%s" % opt)
    session_bound.emit()
    return Ok()

func _wire_signals() -> void:
    # Parent connects; children emit past-tense events only
    var sim: Node = _layers.get(LayerId.SIMULATION)
    var ws: Node = _layers.get(LayerId.WORLD_STATE)
    if sim and ws:
        sim.sim_event_emitted.connect(ws.on_sim_event)

func teardown_session(reason: SessionEndReason) -> void:
    for id in _layers.keys():
        var layer: Node = _layers[id]
        if layer:
            layer.on_unbind()
    # Frees this node AND all layer children — never free Autoloads
    queue_free()

# Forbidden patterns (engine / architecture):
# - Autoload WorldStateLayer / SimulationLayer / …
# - free() / queue_free() on Autoload singletons
# - Presentation mutating Simulation directly
```

## Acceptance criteria (execution — stub→playable ladder)

- [x] Parallel spine note under `Roadmap/Execution/Phase-1-…/` (not flat heap)
- [x] `conceptual_counterpart` links frozen conceptual Phase-1 primary
- [x] Pseudo-code + interfaces for SessionComposer / layer bind / teardown
- [x] Godot stable verbatim citations in Research integration
- [ ] Secondary execution mirrors 1.1 / 1.2 / 1.3 minted
- [ ] Tertiary notes with edge-case ACs under each secondary
- [ ] `execution_factory_handoff_ready` / package pins (later phases — deferred)

## Research integration

### Key takeaways

- SessionComposer = session composition root; four layers as children whose lifetime matches the session (`queue_free` parent frees layers).
- Prefer `Main → SessionComposer → {WorldState, Simulation, Presentation, InputIntent}`; do **not** collapse layers into one Autoload.
- Autoload only for self-contained broad managers; systems that modify other systems' data stay as regular nodes/scenes.
- Never `free`/`queue_free` Autoloads; session teardown frees SessionComposer subtree only.
- Cross-layer: ancestor mediates; child emits past-tense signals; parent connects / injects callables or Node refs.
- Use `class_name … extends Node` for typed layer APIs.
- WorldShell / level swaps stay Phase-2; this deepen is session layer graph only.

### Decisions / constraints

- **Reject Autoload for WorldState / Simulation / Presentation / InputIntent.**
- SessionComposer mediates sibling layer refs (no hard cross-layer NodePaths).
- Layers `emit` past-tense events; SessionComposer owns `.connect` after bind.
- Teardown = `SessionComposer.queue_free()` only — never Autoload nodes.

### Verbatim anchors

> "Finally, when a node is freed with Object.free() or queue_free(), it will also free all its children."
> — https://docs.godotengine.org/en/stable/classes/class_node.html

> "Warning: Autoloads must not be removed using free() or queue_free() at runtime, or the engine will crash."
> — https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html

> "If you have systems that modify other systems' data, you should define those as their own scripts or scenes, rather than autoloads."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "Nodes which are siblings should only be aware of their own hierarchies while an ancestor mediates their communications and references."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

### Links

- [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Subphase next (execution DFS)

1. Mint **1.1** execution secondary under `Execution/Phase-1-…/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/` (parallel spine).
2. Then 1.2 StageDAG / Intent pipeline, 1.3 SeamRegistry + SeedSnapshot + DryRun.
3. Re-assess handoff readiness toward secondary tree complete (still no package jump to Phase 2).

## Status

`deepen_complete: true` for Phase-1 **primary** execution refine (scaffold stub → SessionComposer contracts). `harness_material_change_required: satisfied`. Next: RESUME_ROADMAP deepen → Phase-1-1 layer decoupling (execution).
