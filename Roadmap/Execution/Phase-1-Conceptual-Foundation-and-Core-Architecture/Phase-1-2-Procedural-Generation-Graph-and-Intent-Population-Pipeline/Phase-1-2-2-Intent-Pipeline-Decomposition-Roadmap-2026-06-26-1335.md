---
title: Phase 1.2.2 — Intent Pipeline Decomposition (Execution)
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]'
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
- intent-pipeline
- lore-hooks
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.2.2 — Intent Pipeline Decomposition (Execution)

Execution tertiary: CanonFact lifecycle gate → IntentResolver cross-cut → LoreHookRegistry → SimGraphSeed. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — intent pipeline **enables** table-shaped accepted facts only (players do not author via PROPOSED leak).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Only `accepted` facts populate hooks; IntentResolver is not a DAG slot; append-only registry |
| Inspiration / L5 bar (advisory) | Table shapes via accepted facts; proposed leak → hard reject; conflict = DM-retconnable flag |
| Inspiration (studied) | (1) Conceptual rollup 1.2.2 schema. (2) Execution 1.1.2 CanonCommitBoundary. (3) Execution 1.2.1 stage cross-cut timing. |
| Execution mechanism | LoreHookRegistry + IntentResolver + ConflictAdjudicator; Error/OK + canon.* signals |
| Validation | Catalog paint DoD met; cursor → 1.3 paint |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Conceptual 1.2.2 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Intent enablement | LoreHookRegistry append only after `is_accepted`; ConflictAdjudicator = retconnable flag |
| `does_not_mandate` | PROPOSED facts in hooks; IntentResolver as DAG slot; soft-continue on leak |
| Pin color keys | Foundation Cyan · Blue (Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Players do not author first world | `LoreHookRegistry.append` | not `is_accepted` → ERR_UNAUTHORIZED | hook_rejected |
| Table can shape (accepted facts) | `IntentResolver.resolve_for_stage` | ACCEPTED\|HOOKED only | lore hooks |
| Every world-hitting change DM-retconnable | `ConflictAdjudicator.check_pair` | conflict_detected + flag | first-wins |
| Durable living world seed | `sim_graph_seed` promote | proposed never flows | SimGraphSeed |
| Collaborative GUI signals | canon.* / session.* | — | hook_appended |

## Module map

| Module | Responsibility |
|--------|----------------|
| `CanonCommitBoundary` (injected) | Dual-gate: `is_accepted` (ACCEPTED\|HOOKED) for intent/registry reads; `is_sim_write_allowed` (HOOKED-only) for Simulation mutators |
| `IntentResolver` | Cross-cut POIs / entities / sim_bootstrap |
| `LoreHookRegistry` | Append-only hooks; lex sort `(canon_fact_id, hook_kind, hook_id)` |
| `ConflictAdjudicator` | Emit `canon.conflict_detected`; first-encountered wins + DM flag |
| `SimGraphSeedAssembler` | Promote faction/tribe seeds → Simulation bootstrap payload |

## Interfaces

```text
LoreHookRegistry (RefCounted):
  + append(entry: Dictionary) -> Error   # requires accepted canon_fact_id
  + entries_sorted() -> Array[Dictionary]
  + has_hook(hook_id: StringName) -> bool
  signals: hook_appended(hook_id), hook_rejected(hook_id, reason), hook_unanchored(hook_id)

IntentResolver (RefCounted):
  + bind_boundary(boundary: CanonCommitBoundary) -> void
  + resolve_for_stage(stage_id: StageId) -> Error
  + lore_hooks() -> Array[Dictionary]
  + sim_graph_seed() -> Dictionary  # { nodes: Array, edges: Array, sim_active: bool }
  signals: conflict_detected(fact_a, fact_b), resolve_failed(stage_id, reason)

ConflictAdjudicator (RefCounted):
  + check_pair(a: Dictionary, b: Dictionary) -> Error  # OK or emit conflict
```

### Cross-cut timing (execution)

| Stage | Read | Write | SimGraphSeed |
|-------|------|-------|--------------|
| terrain / biomes | none | none | none |
| POIs | accepted facts | draft poi-bound hooks | none |
| entities | draft + POIManifest | enrich npc/tribe links | none |
| sim_bootstrap | finalized registry | promote sim-active | **emit** |

**Invariants:** I-1.2.2-001 no write without accepted fact; I-1.2.2-002 hook_id unique per run; proposed fact leak → abort that fact's intent pass (not soft warn).

## Pseudo-code

```pseudo
# 1.2.2 — Intent pipeline (Godot 4 stable Error/OK + signals).
# Depends on Execution 1.1.2 CanonCommitBoundary dual-gate.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# LoreHookRegistry.append REQUIRES boundary.is_accepted — PROPOSED never flows (players do not author).
# IntentResolver is cross-cut only — never a DAG slot; table shapes via accepted facts.
# ConflictAdjudicator: first-wins + DM flag = retconnable — no silent merge.
# Simulation mutators still need is_sim_write_allowed (HOOKED) — dual-gate preserved.
# ===========================================================

class_name LoreHookRegistry
extends RefCounted

signal hook_appended(hook_id)
signal hook_rejected(hook_id, reason)
signal hook_unanchored(hook_id)

var _rows: Dictionary = {}  # StringName -> Dictionary
var _boundary: CanonCommitBoundary

func append(entry: Dictionary) -> Error:
	var fact_id: StringName = entry.get("canon_fact_id", &"")
	var hook_id: StringName = entry.get("hook_id", &"")
	if fact_id == &"" or hook_id == &"":
		return ERR_INVALID_PARAMETER
	# JUNIOR WORK-ORDER: proposed must never flow — players do not author first world
	if not _boundary.is_accepted(fact_id):
		hook_rejected.emit(hook_id, "not_accepted")
		return ERR_UNAUTHORIZED
	if _rows.has(hook_id):
		hook_rejected.emit(hook_id, "duplicate")
		return ERR_ALREADY_IN_USE
	_rows[hook_id] = entry
	hook_appended.emit(hook_id)
	return OK

class_name IntentResolver
extends RefCounted

signal conflict_detected(fact_a, fact_b)
signal resolve_failed(stage_id, reason)

var _registry: LoreHookRegistry
var _boundary: CanonCommitBoundary

func resolve_for_stage(stage_id: StageId) -> Error:
	# JUNIOR WORK-ORDER: cross-cut only at POIs/entities/sim_bootstrap — not a DAG slot
	match stage_id:
		StageId.POIS:
			return _draft_poi_hooks()
		StageId.ENTITIES:
			return _enrich_entity_hooks()
		StageId.SIM_BOOTSTRAP:
			return _finalize_sim_graph()
		_:
			return OK  # terrain/biomes: no intent cross-cut

func sim_graph_seed() -> Dictionary:
	var nodes: Array = []
	var edges: Array = []
	for row in _registry.entries_sorted():
		if row.get("hook_kind") == "faction_seed":
			nodes.append(row)
		elif row.get("hook_kind") == "tribe_seed":
			edges.append(row)
	return {"nodes": nodes, "edges": edges, "sim_active": not nodes.is_empty()}
```

## Edge-case ACs

- [ ] Proposed CanonFact in resolver → reject write; no soft continue
- [ ] Contradicting accepted facts → `conflict_detected`; first-encountered wins + flag
- [ ] Zero faction/tribe seeds → `sim_active: false` empty graph (valid degraded)
- [ ] Orphan hook → `hook_unanchored`; compile may warn, not crash
- [x] **UX Catalog paint** — L5 seats/guards as JUNIOR WORK-ORDER (gold pattern)

## Research integration

> "OK = 0 — Methods that return Error return OK when no error occurred."
> — https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#enum-globalscope-error

> "To use signals you need to connect them first…"
> — https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html

> "RefCounted… automatically freed when no longer in use."
> — https://docs.godotengine.org/en/stable/classes/class_refcounted.html

> "Dictionaries are associative containers…"
> — https://docs.godotengine.org/en/stable/classes/class_dictionary.html

## Status

`deepen_complete: true` + **`paint_status: painted`** (`exec-ux-paint-20260929`). **1.2 tertiary paint complete.** Next: **1.3**.
