---
title: Phase 1.2.1 — Stage DAG Node Contracts (Execution)
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
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
- dag-contracts
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.2.1 — Stage DAG Node Contracts (Execution)

Execution tertiary: per-stage I/O manifests, StageDAG edge registry, ToneProfile injection points, `gen.stage.*` replaceability seams. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — stage contracts **enable** system-authored first world + DM-retconnable partial abort (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Five-stage topological chain with typed manifests; ToneProfileInjector cross-cut only |
| Inspiration / L5 bar (advisory) | System authors first world via SeedBundle→stages; partial = DM-retconnable STOP; players do not inject mid-DAG |
| Inspiration (studied) | (1) Conceptual rollup 1.2.1 tables. (2) Execution 1.2 StageOrchestrator. (3) Godot Dictionary/Array for manifest maps. |
| Execution mechanism | `IStageExecutor` + edge registry + injector; Error/OK + `session.stage_*` signals |
| Validation | Catalog paint DoD met; playable Half B later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Conceptual 1.2.1 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| DAG enablement | Typed stage chain = system-authored living world; partial FailureManifest = retconnable abort |
| `does_not_mandate` | player-authored stage payloads; injector as DAG slot; soft-continue on partial |
| Pin color keys | Foundation Cyan · Blue (Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Players do not author first world | `StageEdgeRegistry` + SeedBundle→terrain | refuse player mid-DAG inject | TerrainManifest… |
| Deterministic living world | typed `in_type`/`out_type` chain | unknown stage → reject | topological_order |
| Every world-hitting change DM-retconnable | `FailureManifest.partial` STOP | no soft-continue downstream | session.stage_failed.* |
| Table can shape (tone only) | `ToneProfileInjector.apply` | never a DAG slot | tone_fallback_applied |
| Collaborative GUI preview | stage_ready residues | presentation.* listen | scaffold preview |

## Module map

| Module | Responsibility |
|--------|----------------|
| `IStageExecutor` | `run(upstream, weights) -> Dictionary` per StageId |
| `StageEdgeRegistry` | from→to + manifest type names (immutable schema ids) |
| `ToneProfileInjector` | Per-stage receptive fields; Medium Fantasy fallback |
| `FailureManifest` | `partial: true` + reason; blocks transitive downstream |

## Interfaces

```text
IStageExecutor (RefCounted):
  + stage_id() -> StageId
  + run(upstream: Dictionary, weights: Dictionary) -> Dictionary
  # Dictionary keys: partial:bool, reason:String, payload:Dictionary

StageEdgeRegistry (RefCounted):
  + edges() -> Array[Dictionary]  # {from, to, in_type, out_type, optional:bool}
  + topological_order() -> Array[StageId]
  + assert_unknown_stage(id: StageId) -> Error

ToneProfileInjector (RefCounted) — slice detail:
  + injection_points() -> Dictionary  # StageId -> PackedStringArray field ids
  + apply(stage_id, profile_id, receptive) -> Dictionary
  signals: tone_fallback_applied(stage_id, profile_id)
```

### Edge registry (authoritative names)

| from | to | in_type | out_type |
|------|-----|---------|----------|
| SeedBundle | terrain | SeedBundle | TerrainManifest |
| terrain | biomes | TerrainManifest | BiomeManifest |
| biomes | POIs | BiomeManifest | POIManifest |
| POIs | entities | POIManifest | EntityManifest |
| entities | sim_bootstrap | EntityManifest | SimGraphSeed |

**Invariants:** I-1.2.1-001 no cycles; I-1.2.1-002 partial blocks downstream; I-1.2.1-003 injector never a DAG slot; I-1.2.1-005 seam swap preserves type names.

## Pseudo-code

```pseudo
# 1.2.1 — StageDAG node contracts (Godot 4 stable).
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# System authors first world: SeedBundle → typed stage chain — players do not inject mid-DAG.
# FailureManifest.partial = DM-retconnable STOP — never soft-continue to biomes+.
# ToneProfileInjector is cross-cut only — never a DAG slot (table shapes weights, not topology).
# Preserve in_type/out_type names on executor swap (Phase-2 WorldShell / seams).
# ===========================================================

class_name StageEdgeRegistry
extends RefCounted

var _edges: Array = [
	{"from": "SeedBundle", "to": "terrain", "in_type": "SeedBundle", "out_type": "TerrainManifest", "optional": false},
	{"from": "terrain", "to": "biomes", "in_type": "TerrainManifest", "out_type": "BiomeManifest", "optional": false},
	{"from": "biomes", "to": "POIs", "in_type": "BiomeManifest", "out_type": "POIManifest", "optional": false},
	{"from": "POIs", "to": "entities", "in_type": "POIManifest", "out_type": "EntityManifest", "optional": false},
	{"from": "entities", "to": "sim_bootstrap", "in_type": "EntityManifest", "out_type": "SimGraphSeed", "optional": false},
]

func topological_order() -> Array:
	return ["terrain", "biomes", "POIs", "entities", "sim_bootstrap"]

func run_stage(exec: IStageExecutor, upstream: Dictionary, injector: ToneProfileInjector, profile_id: StringName) -> Dictionary:
	# JUNIOR WORK-ORDER: injector cross-cut — table tone, not player authorship
	var weights := injector.apply(exec.stage_id(), profile_id, {})
	var m := exec.run(upstream, weights)
	if m.get("partial", false):
		# JUNIOR WORK-ORDER: DM-retconnable abort — STOP transitive downstream
		return m  # caller emits session.stage_failed.<stage>; STOP
	return m
```

## Edge-case ACs

- [ ] Unknown stage id in dispatch → DAGValidator reject; traversal never starts
- [ ] Partial TerrainManifest → biomes+ not run; `session.stage_failed.terrain`
- [ ] Unknown ToneProfile variant → Medium Fantasy + `session.tone_fallback_applied`
- [ ] Executor swap mid-pipeline → new SeedSnapshot + dry-run (1.3); edge type names unchanged
- [x] **UX Catalog paint** — L5 seats/guards as JUNIOR WORK-ORDER (gold pattern)

## Research integration

> "Dictionaries are associative containers…"
> — https://docs.godotengine.org/en/stable/classes/class_dictionary.html

> "OK = 0 — Methods that return Error return OK when no error occurred."
> — https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#enum-globalscope-error

> "To use signals you need to connect them first…"
> — https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html

## Status

`deepen_complete: true` + **`paint_status: painted`** (`exec-ux-paint-20260929`). Next paint: **1.2.2**.
