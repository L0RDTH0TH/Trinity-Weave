---
title: Phase 1.2 — Procedural Generation Graph and Intent Population Pipeline (Execution)
roadmap-level: secondary
phase-number: 1
subphase-index: "1.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
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
- proc-gen
- intent-pipeline
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.2 — Procedural Generation Graph and Intent Population Pipeline (Execution)

Execution secondary for StageDAG traversal, SeedBundle → CompiledWorldManifest, and IntentResolver cross-cut. Parallel spine under `Roadmap/Execution/Phase-1-…/Phase-1-2-…/`. **No Half B.** L5/SERIES are **read-only advisory feedstock** — StageDAG + IntentResolver **enable** world-shell seats/guards (players do not author first world; accepted facts only; DM-retconnable promote).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Typed stage DAG with forward-progress invariant; intent population via CanonCommitBoundary gate; deterministic compile |
| Inspiration / L5 bar (advisory) | System authors first world via SeedBundle+DAG; table shapes via accepted facts; no silent player authorship mid-pipeline |
| Inspiration (studied) | (1) Conceptual 1.2 + rollups 1.2.1/1.2.2. (2) Godot citations research. (3) Execution 1.1 Bus+Canon inject. |
| Execution mechanism | Typed GDScript interfaces + pseudo for SeedBundle, DAGValidator, StageOrchestrator, ToneProfileInjector, IntentResolver, DeterministicCompiler |
| Validation signal | Catalog paint DoD met; tertiaries 1.2.1–1.2.2 next paint |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Frozen conceptual 1.2 + tertiaries 1.2.1–1.2.2 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Pipeline enablement | SeedBundle+StageDAG = system-authored first world; IntentResolver = table-shaped accepted facts only |
| `does_not_mandate` | player-authored SeedBundle; Autoload StageOrchestrator; unseeded RNG; proposed-only facts in IntentResolver |
| Pin color keys | Foundation Cyan · Blue (Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Players do not author first world | `SeedParser` + session-0 SeedBundle | refuse player seat on bundle assemble | SeedBundle |
| Table can shape (accepted facts) | `IntentResolver.resolve_for_stage` | `is_accepted` only — never PROPOSED | lore hooks |
| Every world-hitting change DM-retconnable | conflict path / pipeline_aborted | reject mid-stage → no silent merge | stage_failed |
| Deterministic living world | `DeterministicCompiler.compile` | forbid wall-clock / unseeded rand | CompiledWorldManifest |
| Collaborative GUI preview | stage_ready → presentation.* | session Node orchestrator | scaffold residues |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SeedParser` | Assemble SeedBundle from session 0 inputs |
| `DAGValidator` | Pre-flight: no cycles; deps resolvable |
| `StageOrchestrator` | Topological dispatch of stage nodes |
| `ToneProfileInjector` | Cross-cut weights; never a DAG slot |
| `IntentResolver` | Cross-cut accepted CanonFacts → LoreHookRegistry |
| `DeterministicCompiler` | SeedBundle+manifests → byte-stable CompiledWorldManifest |
| `StageNode` ×5 | terrain → biomes → POIs → entities → sim_bootstrap |

## Interfaces

```text
enum StageId { TERRAIN, BIOMES, POIS, ENTITIES, SIM_BOOTSTRAP }

SeedBundle (RefCounted):
  + tone_profile_id: StringName
  + map_seed: int
  + accepted_fact_ids: PackedStringArray
  + to_dict() -> Dictionary

DAGValidator (RefCounted):
  + preflight(edge_registry: Array[Dictionary]) -> Error
  signals: dag_validated(), dag_rejected(reason)

StageOrchestrator (Node, session-scoped child — NOT Autoload):
  + run(bundle: SeedBundle, edges: Array[Dictionary]) -> Error
  + last_manifests() -> Dictionary  # StageId -> Dictionary
  signals: stage_ready(stage_id), stage_failed(stage_id, reason), pipeline_complete(), pipeline_aborted(reason)

ToneProfileInjector (RefCounted):
  + apply(stage_id: StageId, profile_id: StringName, receptive: Dictionary) -> Dictionary
  # unknown variant → Medium Fantasy defaults + emit tone_fallback_applied

IntentResolver (RefCounted, injected CanonCommitBoundary):
  + bind_boundary(boundary: CanonCommitBoundary) -> void
  + resolve_for_stage(stage_id: StageId) -> Error
  + lore_hooks() -> Array[Dictionary]
  + sim_graph_seed() -> Dictionary
  signals: hook_written(hook_id), conflict_detected(fact_a, fact_b)

DeterministicCompiler (RefCounted):
  + compile(bundle: SeedBundle, manifests: Dictionary, hooks: Array) -> Dictionary
  # returns { ok: bool, manifest: Dictionary, incomplete: bool, error: Error }
  signals: world_manifest_ready(path_hint), world_manifest_failed(reason)
```

## Pseudo-code

```pseudo
# Phase 1.2 — StageDAG + Intent pipeline (Godot 4 stable Error/OK + signals).
# Citations: docs.godotengine.org/en/stable/ (Node, RefCounted, Dictionary, signals, GlobalScope.Error).
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# System authors first world: SeedBundle from session-0 — refuse player seat on assemble.
# IntentResolver reads ACCEPTED|HOOKED only — table shapes via CanonCommitBoundary, never PROPOSED.
# Conflict / stage_failed = DM-retconnable abort — no silent merge mid-pipeline.
# DeterministicCompiler: map_seed only — forbid wall-clock / unseeded randi().
# StageOrchestrator = session Node child (NOT Autoload) — presentation.* may listen stage_ready.
# ===========================================================

class_name DAGValidator
extends RefCounted

signal dag_validated
signal dag_rejected(reason)

func preflight(edge_registry: Array) -> Error:
	if edge_registry.is_empty():
		dag_rejected.emit("empty_registry")
		return ERR_INVALID_PARAMETER
	if _has_cycle(edge_registry):
		dag_rejected.emit("cycle")
		return ERR_INVALID_PARAMETER
	if not _deps_resolvable(edge_registry):
		dag_rejected.emit("unresolvable_deps")
		return ERR_DOES_NOT_EXIST
	dag_validated.emit()
	return OK

class_name StageOrchestrator
extends Node

signal stage_ready(stage_id)
signal stage_failed(stage_id, reason)
signal pipeline_complete
signal pipeline_aborted(reason)

var _manifests: Dictionary = {}
var _injector: ToneProfileInjector
var _intent: IntentResolver
var _compiler: DeterministicCompiler
var _dag: DAGValidator

func run(bundle: SeedBundle, edges: Array) -> Error:
	# JUNIOR WORK-ORDER: bind CanonCommitBoundary — IntentResolver gate for table-shaped facts
	# _intent.bind_boundary(composer.service(&"CanonCommitBoundary")) at session bind
	var err := _dag.preflight(edges)
	if err != OK:
		pipeline_aborted.emit("dag_preflight")
		return err
	var order: Array = [StageId.TERRAIN, StageId.BIOMES, StageId.POIS, StageId.ENTITIES, StageId.SIM_BOOTSTRAP]
	for sid in order:
		var weights := _injector.apply(sid, bundle.tone_profile_id, {})
		if sid in [StageId.POIS, StageId.ENTITIES, StageId.SIM_BOOTSTRAP]:
			# JUNIOR WORK-ORDER: accepted facts only — players do not inject PROPOSED mid-stage
			err = _intent.resolve_for_stage(sid)
			if err != OK:
				stage_failed.emit(sid, "intent_gate")
				pipeline_aborted.emit("intent")  # DM-retconnable abort
				return err
		var m := _run_stage(sid, _upstream(sid), weights)
		if m.get("partial", false):
			stage_failed.emit(sid, m.get("reason", "partial"))
			pipeline_aborted.emit("stage_partial")
			return ERR_BUG
		_manifests[sid] = m
		stage_ready.emit(sid)  # JUNIOR: presentation.* scaffold may preview
	var compiled := _compiler.compile(bundle, _manifests, _intent.lore_hooks())
	if not compiled.get("ok", false):
		pipeline_aborted.emit("compile")
		return int(compiled.get("error", ERR_BUG))
	pipeline_complete.emit()
	return OK

# DeterministicCompiler: identical SeedBundle + ToneProfile + accepted facts → byte-stable Dictionary.
# Forbidden: Time.get_ticks_msec(), randi() without explicit seed from map_seed.
```

## Acceptance criteria (execution)

- [x] Parallel spine path under `Execution/Phase-1-…/Phase-1-2-…/` (not flat)
- [x] Path-qualified `conceptual_counterpart` → conceptual 1.2
- [x] Interfaces + pseudo for DAGValidator + StageOrchestrator + IntentResolver + DeterministicCompiler
- [x] Godot stable citations in Research integration (whitelist)
- [x] Tertiary execution mirrors 1.2.1 / 1.2.2 minted
- [x] Edge-case ACs drafted on each tertiary (unchecked items = Half B / playable later)
- [x] **UX Catalog paint** — L5 seats/guards as JUNIOR WORK-ORDER (gold pattern)

## Research integration

### Key takeaways

- StageOrchestrator is a **session Node child**, not an Autoload gameplay singleton.
- Fallible APIs return GlobalScope `Error` / `OK`; past-tense signals on owners.
- Deterministic compile forbids wall-clock / unseeded entropy (save/load + dry-run).
- IntentResolver reads only `accepted` facts via CanonCommitBoundary (Execution 1.1).

### Verbatim anchors

> "Finally, when a node is freed with Object.free() or queue_free(), it will also free all its children."
> — https://docs.godotengine.org/en/stable/classes/class_node.html

> "OK = 0 — Methods that return Error return OK when no error occurred."
> — https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#enum-globalscope-error

> "To use signals you need to connect them first… define a custom signal… signal my_signal"
> — https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html

> "Dictionaries are associative containers… Keys can be of any Variant type…"
> — https://docs.godotengine.org/en/stable/classes/class_dictionary.html

> "RefCounted… automatically freed when no longer in use."
> — https://docs.godotengine.org/en/stable/classes/class_refcounted.html

### Links

- [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Subphase next (execution DFS)

1. ~~Mint tertiaries 1.2.1–1.2.2~~ done.
2. **Paint** tertiaries **1.2.1** then **1.2.2** (`paint_ux_catalog`).
3. Then execution **1.3** secondary. Still Phase 1 — no Phase-2 jump for paint order.

## Status

`deepen_complete: true` + **`paint_status: painted`** (`exec-ux-paint-20260929`). Next paint: **1.2.1**.
