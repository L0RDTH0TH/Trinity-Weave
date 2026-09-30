---
title: Phase 2.2 — Canon Registry and Intent Resolver (Execution)
roadmap-level: secondary
phase-number: 2
subphase-index: "2.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
status: active
priority: high
progress: 45
handoff_readiness: 72
package_id: pkg_world_shell
catalog_row_ids:
- ux_world_generation
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-2
- canon-registry
- intent-resolver
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 2.2 — Canon Registry and Intent Resolver (Execution)

Execution secondary for CanonRegistry lifecycle (`proposed → accepted → hooked → sim-active`), IntentResolver routing, LoreHookRegistry projection, and ConflictArbiter surface. Parallel spine under `Roadmap/Execution/Phase-2-…/Phase-2-2-…/`. **No Half B code.** L5/SERIES are **read-only paint feedstock** — meaning goes into junior work-order pseudo (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Durable collaborative canon backbone feeding 2.1 POI/entity/sim stages ([[conceptual 2.2#Behavior]]) |
| Inspiration / L5 bar | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` — table can shape lasting world truth; every world-hitting change DM-retconnable; players do not author first world |
| Inspiration (studied) | (1) Conceptual 2.2 + tertiary 2.2.1 ConflictArbiter. (2) Execution 1.1 CanonCommitBoundary. (3) Execution 1.2 IntentResolver stub. (4) Execution 2.1 stage cross-cut points. |
| Execution mechanism | GDScript interfaces + pseudo for CanonRegistry, IntentResolver, LoreHookRegistry, CanonFactValidator, HookMaterializer, RegistrySnapshot |
| Validation signal | Catalog paint DoD met on this note; tertiary **2.2.1** paints conflict policy next; Half B later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Frozen conceptual 2.2 + 2.2.1 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only) |
|-------|--------------------------------------|
| `row_id` | `ux_world_generation` |
| Label | DM can create (table can shape) a persistent living world |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| `catalog_face` / `experience_mode` | `living_world` / `world_generation` |
| Child surface | `ux_worldgen_gui` (dialogue) — canon accept is durability sibling to GUI preview accept |
| `does_not_mandate` | one-world=one-campaign forever; Session-0-checkbox-only; players author first world; unconstrained multi-knob fresh-noise; default-next = player character creation |
| Pin color keys | Blue (Phase-2 Behavior) · Cyan (SeedSnapshot / CanonCommitBoundary) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Table can shape lasting truth | `CanonRegistry.propose` → `accept` (DM/table seats) | wrong seat / commit_boundary | ACCEPTED fact + `fact_accepted` |
| Players do not author first world | accept path requires author seat + CanonCommitBoundary | player propose may exist; player accept refused | rejected / unauthorized |
| Durable living world (facts feed gen) | `IntentResolver.resolve_for_stage` → LoreHookRegistry | only ACCEPTED/HOOKED feed POI/entity/sim | hooks on stage manifests |
| Every world-hitting change DM-retconnable | reject / accept_merged / fork_thread + arbiter (never silent merge) | conflict → ConflictArbiter open | conflict_surfaced / resolved |
| Physical/settlement + monster-region tags | hooks materialize tags consumed by 2.1 stages | PROPOSED never feeds stages | HOOKED → SIM_ACTIVE |
| Import/attach first-class | imported facts enter propose→accept same path | invalid schema → validator fail | same durable registry |
| Multiple campaigns / same world | RegistrySnapshot + session-scoped registry (not one-campaign Autoload) | — | snapshot fingerprint reusable |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-intent-lore-loop` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Canon.IntentResolver` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Canon.IntentResolver` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility |
|--------|----------------|
| `CanonRegistry` | Store + index CanonFacts by era/entity/location/thread |
| `IntentResolver` | Intent payloads → candidate facts; stage cross-cut for 2.1 |
| `CanonFactValidator` | Schema + table policy + ToneCompatibilityGate before accept |
| `HookMaterializer` | Accepted facts → LoreHookRegistry candidates |
| `LoreHookRegistry` | Hook projection consumed by POI/entity/sim_bootstrap |
| `ConflictArbiter` | Contradictions → DM workbench (detail → **2.2.1**) |
| `RegistrySnapshot` | Point-in-time export for DryRunValidator alignment |
| `ProvenanceRecorder` | Stamp every registry mutation (Execution 1.3) |

## Interfaces

```text
enum CanonLifecycle { PROPOSED, ACCEPTED, HOOKED, SIM_ACTIVE }

CanonFact (Dictionary schema):
  fact_id: StringName
  lifecycle: CanonLifecycle
  era: StringName
  entity_ids: PackedStringArray
  location_ids: PackedStringArray
  thread_ids: PackedStringArray
  payload: Dictionary
  provenance: Dictionary

CanonRegistry (RefCounted, session-scoped — NOT Autoload):
  + propose(fact: Dictionary) -> Error
  + accept(fact_id: StringName) -> Error
  + reject(fact_id: StringName, reason: String) -> Error
  + accept_merged(fact_id: StringName, merged: Dictionary) -> Error
  + fork_thread(fact_id: StringName, fork: Dictionary) -> Error
  + get(fact_id: StringName) -> Dictionary
  + list_lifecycle(state: CanonLifecycle) -> Array[Dictionary]
  + index_query(filters: Dictionary) -> Array[Dictionary]
  signals: fact_proposed(fact_id), fact_accepted(fact_id), fact_rejected(fact_id, reason)

IntentResolver (RefCounted, CanonCommitBoundary injected):
  + ingest(intent: Dictionary) -> Error
  + resolve_for_stage(stage_id: int, facts_gate) -> Error
  + lore_hooks() -> Array[Dictionary]
  + sim_graph_seed() -> Dictionary
  signals: intent_received(intent_id), hook_written(hook_id), conflict_detected(fact_a, fact_b)

CanonFactValidator (RefCounted):
  + validate(fact: Dictionary, tone_gate) -> Dictionary
  # { ok:bool, reasons:PackedStringArray }
  signals: fact_validated(fact_id), fact_invalid(fact_id, reasons)

LoreHookRegistry (RefCounted):
  + materialize(fact_id: StringName, tags: PackedStringArray) -> Error
  + lookup(tags: PackedStringArray) -> Array[Dictionary]
  signals: hook_materialized(hook_id)

RegistrySnapshot (RefCounted):
  + capture(registry: CanonRegistry) -> Dictionary
  + fingerprint() -> String

ConflictArbiter (RefCounted):
  + classify(fact_a: Dictionary, fact_b: Dictionary) -> StringName
  + open(fact_a: Dictionary, fact_b: Dictionary) -> Dictionary
  + resolve(conflict_id: StringName, chosen: ResolutionMode, actor: StringName) -> Error
  signals: conflict_surfaced(conflict_id), conflict_resolved(conflict_id, policy)
```

## Pseudo-code

```pseudo
# Phase 2.2 — Canon + Intent (Godot 4 stable Error/OK + signals).
# Citations: docs.godotengine.org/en/stable/ (RefCounted, Dictionary, signals, GlobalScope.Error).
# Reject: Autoload CanonRegistry; accept without CanonCommitBoundary; silent conflict merge.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 / SERIES) ===
# Own durable table-shaped world truth: propose → accept → hook → feed 2.1 stages.
# Players do not author the first world — accept requires author seat + CanonCommitBoundary.
# Every world-hitting canon change is DM-retconnable: reject / merge / fork / arbiter — NEVER silent merge.
# Anti-mandate: do NOT Autoload one-campaign-forever registry; session-scoped RefCounted is correct.
# Anti-mandate: do NOT treat canon as Session-0 checkbox with no persistent living-world residue.
# Hooks carry physical/settlement / monster-region tags into GenerationPipeline (2.1) manifests.
# ===========================================================

class_name CanonRegistry
extends RefCounted

signal fact_proposed(fact_id)
signal fact_accepted(fact_id)
signal fact_rejected(fact_id, reason)

var _facts: Dictionary = {}  # fact_id -> Dictionary
var _validator: CanonFactValidator
var _boundary  # CanonCommitBoundary from Execution 1.1
var _arbiter: ConflictArbiter
var _hooks: LoreHookRegistry
var _prov: ProvenanceRecorder
var _seat: SeatContext  # injected — shared_table | dm_as_player | privileged_access

func propose(fact: Dictionary) -> Error:
	# JUNIOR WORK-ORDER: table may propose scaffolds of truth; not yet durable living-world law
	var id: StringName = fact.get("fact_id", &"")
	if id == &"":
		return ERR_INVALID_PARAMETER
	fact["lifecycle"] = CanonLifecycle.PROPOSED
	_facts[id] = fact
	fact_proposed.emit(id)
	return OK

func accept(fact_id: StringName) -> Error:
	# JUNIOR WORK-ORDER: refuse player seat — players do not author first world / lasting canon
	if not _seat.allows_any(["shared_table", "dm_as_player", "privileged_access"]):
		fact_rejected.emit(fact_id, "wrong_seat")
		return ERR_UNAUTHORIZED
	if not _facts.has(fact_id):
		return ERR_DOES_NOT_EXIST
	var fact: Dictionary = _facts[fact_id]
	var gate := _validator.validate(fact, /* ToneCompatibilityGate */ null)
	if not gate.get("ok", false):
		fact_rejected.emit(fact_id, "validator")
		return ERR_INVALID_PARAMETER
	if not _boundary.is_accepted(fact.get("fact_id", &"")):
		fact_rejected.emit(fact_id, "commit_boundary")
		return ERR_UNAUTHORIZED
	if _detect_conflict(fact):
		var against: Array = _conflicts_of(fact)
		# JUNIOR WORK-ORDER: retconnable conflict — surface to DM; never silent merge
		_arbiter.open(fact, against[0] if against.size() > 0 else {})
		return ERR_BUSY
	# JUNIOR WORK-ORDER: promote → durable ACCEPTED residue (lasting readable world truth)
	fact["lifecycle"] = CanonLifecycle.ACCEPTED
	fact = _prov.stamp(fact, {"source": "accept"})
	_facts[fact_id] = fact
	fact_accepted.emit(fact_id)
	return OK

func reject(fact_id: StringName, reason: String) -> Error:
	# JUNIOR WORK-ORDER: DM-retconnable undo of proposed/accepted path
	if not _facts.has(fact_id):
		return ERR_DOES_NOT_EXIST
	_facts.erase(fact_id)
	fact_rejected.emit(fact_id, reason)
	return OK

func accept_merged(fact_id: StringName, merged: Dictionary) -> Error:
	# JUNIOR WORK-ORDER: explicit DM merge after arbiter — still retconnable, never silent
	merged["fact_id"] = fact_id
	merged["lifecycle"] = CanonLifecycle.ACCEPTED
	_facts[fact_id] = merged
	fact_accepted.emit(fact_id)
	return OK

func fork_thread(fact_id: StringName, fork: Dictionary) -> Error:
	# JUNIOR WORK-ORDER: alternative living-world thread (Nth campaign scars vs fresh) — not banned
	fork["fact_id"] = fact_id
	_facts[fact_id] = fork
	return OK


class_name IntentResolver
extends RefCounted

signal intent_received(intent_id)
signal hook_written(hook_id)
signal conflict_detected(fact_a, fact_b)

var _registry: CanonRegistry
var _hooks: LoreHookRegistry
var _materializer: HookMaterializer

func resolve_for_stage(stage_id: int, _facts_gate) -> Error:
	# JUNIOR WORK-ORDER: only ACCEPTED (and HOOKED) facts feed POI/entity/sim — never PROPOSED
	# Layer tags / monster-region hooks land here for 2.1 stage manifests
	var accepted := _registry.list_lifecycle(CanonLifecycle.ACCEPTED)
	for fact in accepted:
		var err := _materializer.ensure_hooked(fact)
		if err != OK:
			return err
	return OK

func lore_hooks() -> Array:
	return _hooks.lookup([])

# === WEAVE C# / .NET (Godot 4.6.3) — Terrain3D / Gaea / IWorldGenStage ===
# Manifest: stack-intent-lore-loop, engine-godot-463-dotnet | Catalog: ux_world_generation
namespace Genesis.WorldGen;

public interface ITerrainAuthority {
    Error ApplyHeightAndSplat(SeedSnapshot seed, GenContext ctx);
}
public interface IWorldGenStage {
    StringName StageId { get; }
    StageResult Run(GenContext ctx);
}
// Terrain3D: res://addons/terrain_3d/ via ITerrainAuthority only
// Gaea: stack-procedural-maps-gaea-parallel — overland parallel, not terrain authority
public sealed class Terrain3DAuthority : ITerrainAuthority {
    // JUNIOR WORK-ORDER: dry-run leaves no durable WorldHost child; regen swaps container children
    public Error ApplyHeightAndSplat(SeedSnapshot seed, GenContext ctx) => Error.Ok;
}

```

## Acceptance criteria (execution)

- [x] Parallel spine path under `Execution/Phase-2-…/Phase-2-2-…/` (not flat)
- [x] Path-qualified `conceptual_counterpart` → conceptual 2.2
- [x] Interfaces + pseudo for CanonRegistry / IntentResolver / LoreHookRegistry / ConflictArbiter stub
- [x] **UX Catalog paint** — L5/SERIES moments bound as JUNIOR WORK-ORDER in pseudo (gold pattern)
- [x] Godot stable citations (Error/OK + signals; no Autoload registry)
- [x] Tertiary **2.2.1** ConflictArbiter Resolution Policy minted
- [x] Edge-case ACs on tertiary (duplicate facts, tone reject, mid-compile lock)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `IntentResolver` beat/host wrong-seat → Unauthorized; stub behavior typed against Index hosts — row `ux_world_generation`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_world_generation` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** terrain via `ITerrainAuthority` (Terrain3D); Gaea = parallel-maps path only

## Research integration

### Key takeaways

- CanonRegistry is **session RefCounted**, not Autoload — swap via SeamRegistry (1.3).
- Accept path must pass CanonCommitBoundary (Execution 1.1) + ToneCompatibilityGate (2.3).
- Conflicts surface via ConflictArbiter — never silent merge.
- Stage cross-cut reads only accepted/hooked facts.

### Verbatim anchors

> "OK = 0 — Methods that return Error return OK when no error occurred."
> — https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#enum-globalscope-error

> "Signals are a way to send out a message that can be listened to by other objects."
> — https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html

### Links

- [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Subphase next

1. ~~Paint **2.2**~~ → done (`paint_ux_catalog: true`).
2. Next paint leaves: **2.2.1** / **2.3** / **2.3.1**.

## Child links

- [[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000|2.2.1 ConflictArbiter Resolution Policy]]

## Status

`deepen_complete: true` + **`paint_status: woven`** for Execution **2.2** (`exec-ux-paint-20260929`). Paint ≠ mint L5 files.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
