---
title: Phase 2.2.1 — ConflictArbiter Resolution Policy (Execution)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]]'
status: active
priority: high
progress: 55
handoff_readiness: 74
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
- conflict-arbiter
- canon-registry
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-1-CollaborativeRefinementLoop-Pause-Point-Registry-Roadmap-2026-06-29-1830]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 2.2.1 — ConflictArbiter Resolution Policy (Execution)

Execution tertiary: **ConflictArbiter**, five conflict classes, **ResolutionPolicyBinding**, **ConflictManifest**, **MergeTablePolicy**. Parallel spine under `Execution/Phase-2-…/Phase-2-2-…/`. **No Half B.** L5/SERIES are **read-only paint feedstock** — meaning goes into junior work-order pseudo (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Explicit resolution modes when CanonFacts contradict ([[conceptual 2.2.1]]) |
| Inspiration / L5 bar | L5 — every world-hitting change is DM-retconnable; table can shape; players do not author first world |
| Inspiration (studied) | (1) Conceptual 2.2.1 + rollup. (2) Execution 2.2 ConflictArbiter stub. (3) Execution 2.1.1 table-accept semantics. (4) Execution 1.2.2 intent pipeline |
| Execution mechanism | GDScript policy index + classify → auto-reject or DM queue; never mute CompiledWorldManifest mid-compile |
| Validation | Catalog paint DoD met; mid-pipeline resolve never mutates compiled manifest; DryRun re-compile only |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Frozen conceptual 2.2.1 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only) |
|-------|--------------------------------------|
| `row_id` | `ux_world_generation` |
| Label | DM can create (table can shape) a persistent living world |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Own L5 clause | Every world-hitting change is DM-retconnable (never silent merge) |
| `does_not_mandate` | one-world=one-campaign forever; Session-0-checkbox-only; players author first world; unconstrained fresh-noise; default-next = PC creation |
| Pin color keys | Blue (Phase-2 Behavior) · Cyan (CanonCommitBoundary) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Every world-hitting change DM-retconnable | `ConflictArbiter.open` → `resolve` | mid-compile → ERR_BUSY | `conflict_resolved` + provenance |
| Table can shape (merge) | `TABLE_MERGE` + `MergeTablePolicy.quorum_met` | quorum fail → unauthorized | accept_merged fact |
| Players do not author first world | resolve actor must be author seat (DM/table) | player actor refused upstream | none / blocked |
| Silent conflict banned | no auto-merge when `auto_forbidden` | tone auto-reject only | ConflictManifest queued |
| Deferred DM retcon | `DEFER_TO_DM` → `DMWorkbenchQueue` | unresolved blocks stage handoff | `conflict_deferred` |
| Split living-world threads | `SPLIT_THREAD` → `fork_thread` | — | forked fact thread |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-intent-lore-loop` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Canon.ConflictArbiter` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Canon.ConflictArbiter` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility |
|--------|----------------|
| `ConflictArbiter` | Classify + select mode per binding |
| `ConflictManifest` | Human-readable A/B + class + suggested modes + provenance |
| `ResolutionPolicyBinding` | `conflict_class` → default mode + `auto_forbidden` |
| `MergeTablePolicy` | Quorum gate for `table_merge` (never silent) |
| `DMWorkbenchQueue` | Sink for unresolved conflicts (Phase 4+ consumer) |
| `ProvenanceEnvelope` | Records `conflict_resolution_id` + mode + actor |

## Interfaces

```text
enum ConflictClass {
  DUPLICATE_IDENTITY, TIMELINE_CONTRADICTION, LOCATION_MUTEX,
  TONE_VIOLATION, PLAYER_COLLISION
}
enum ResolutionMode {
  REJECT_NEW, PREFER_INCUMBENT, TABLE_MERGE, DEFER_TO_DM, SPLIT_THREAD
}

ConflictManifest (RefCounted):
  + conflict_id: StringName
  + class_: ConflictClass
  + fact_a: Dictionary
  + fact_b: Dictionary
  + suggested_modes: Array
  + auto_forbidden: bool
  + to_dict() -> Dictionary

ResolutionPolicyBinding (RefCounted):
  + class_: ConflictClass
  + default_mode: ResolutionMode
  + auto_forbidden: bool

MergeTablePolicy (RefCounted):
  + quorum_met(votes: Array) -> bool
  + apply_merge(fact_a: Dictionary, fact_b: Dictionary, votes: Array) -> Dictionary

ConflictArbiter (RefCounted):
  + classify(fact_a: Dictionary, fact_b: Dictionary) -> ConflictClass
  + open(fact_a: Dictionary, fact_b: Dictionary) -> Dictionary
  # { ok:bool, manifest:ConflictManifest, mode:ResolutionMode, deferred:bool }
  + resolve(conflict_id: StringName, chosen: ResolutionMode, actor: StringName) -> Error
  signals: conflict_detected(manifest), conflict_resolved(conflict_id, mode)
  signals: conflict_deferred(conflict_id), fact_rejected(fact_id, reason)

DMWorkbenchQueue (RefCounted):
  + enqueue(manifest: ConflictManifest) -> Error
  + peek() -> ConflictManifest
  signals: conflict_surfaced(conflict_id)
```

### Policy index (execution v1)

| conflict_class | Default mode | Auto forbidden |
|----------------|--------------|----------------|
| `duplicate_identity` | PREFER_INCUMBENT | yes |
| `timeline_contradiction` | DEFER_TO_DM | yes |
| `location_mutex` | TABLE_MERGE (or SPLIT_THREAD) | yes |
| `tone_violation` | REJECT_NEW | no (auto-reject OK) |
| `player_collision` | DEFER_TO_DM | yes |

## Pseudo-code

```pseudo
# 2.2.1 — ConflictArbiter resolution policy (Godot 4 stable).
# Citations: Error/OK, signals — docs.godotengine.org/en/stable/
# Reject: silent merge; mutate CompiledWorldManifest mid-pipeline; Autoload arbiter.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 / SERIES) ===
# Own L5 clause: every world-hitting change is DM-retconnable — NEVER silent merge.
# Table may shape via TABLE_MERGE (quorum) or SPLIT_THREAD; DEFER_TO_DM queues workbench.
# Players do not author first world — resolve actor is DM/table seat (enforced at CanonRegistry).
# Anti-mandate: do NOT Autoload one-campaign arbiter; session RefCounted is correct.
# Mid-compile lock: retcon after compile requires 2.1 DryRun re-compile path (durable residue safe).
# ===========================================================

class_name ConflictArbiter
extends RefCounted

signal conflict_detected(manifest)
signal conflict_resolved(conflict_id, mode)
signal conflict_deferred(conflict_id)
signal fact_rejected(fact_id, reason)

var _bindings: Dictionary = {}   # ConflictClass -> ResolutionPolicyBinding
var _open: Dictionary = {}       # conflict_id -> ConflictManifest
var _merge: MergeTablePolicy
var _queue: DMWorkbenchQueue
var _registry: CanonRegistry
var _bus: Object
var _compile_locked: bool = false  # true while DeterministicCompiler active

func seed_bindings() -> void:
	_bind(ConflictClass.DUPLICATE_IDENTITY, ResolutionMode.PREFER_INCUMBENT, true)
	_bind(ConflictClass.TIMELINE_CONTRADICTION, ResolutionMode.DEFER_TO_DM, true)
	_bind(ConflictClass.LOCATION_MUTEX, ResolutionMode.TABLE_MERGE, true)
	_bind(ConflictClass.TONE_VIOLATION, ResolutionMode.REJECT_NEW, false)
	_bind(ConflictClass.PLAYER_COLLISION, ResolutionMode.DEFER_TO_DM, true)

func open(fact_a: Dictionary, fact_b: Dictionary) -> Dictionary:
	# JUNIOR WORK-ORDER: surface contradiction — lasting readable ConflictManifest residue
	var cls := classify(fact_a, fact_b)
	var bind: ResolutionPolicyBinding = _bindings[cls]
	var mid := StringName("cf_%s_%s" % [fact_a.get("fact_id"), fact_b.get("fact_id")])
	var manifest := ConflictManifest.new()
	manifest.conflict_id = mid
	manifest.class_ = cls
	manifest.fact_a = fact_a
	manifest.fact_b = fact_b
	manifest.auto_forbidden = bind.auto_forbidden
	manifest.suggested_modes = _suggest(cls)
	_open[mid] = manifest
	conflict_detected.emit(manifest)
	_bus.emit_signal("canon_conflict_detected", mid)
	# Auto path only when not forbidden
	if not bind.auto_forbidden and bind.default_mode == ResolutionMode.REJECT_NEW:
		# JUNIOR WORK-ORDER: tone auto-reject OK; still explicit (not silent merge)
		_registry.reject(fact_b.get("fact_id"), "tone_violation")
		fact_rejected.emit(fact_b.get("fact_id"), "tone_violation")
		conflict_resolved.emit(mid, ResolutionMode.REJECT_NEW)
		return {"ok": true, "manifest": manifest, "mode": ResolutionMode.REJECT_NEW, "deferred": false}
	# JUNIOR WORK-ORDER: DM-retconnable defer — queue workbench; block stage handoff until resolved
	_queue.enqueue(manifest)
	_bus.emit_signal("session_conflict_surfaced", mid)
	conflict_deferred.emit(mid)
	return {"ok": true, "manifest": manifest, "mode": bind.default_mode, "deferred": true}

func resolve(conflict_id: StringName, chosen: ResolutionMode, actor: StringName) -> Error:
	if _compile_locked:
		# JUNIOR WORK-ORDER: never mute CompiledWorldManifest mid-pipeline — re-compile via 2.1
		return ERR_BUSY
	var m: ConflictManifest = _open.get(conflict_id)
	if m == null:
		return ERR_DOES_NOT_EXIST
	match chosen:
		ResolutionMode.REJECT_NEW:
			_registry.reject(m.fact_b.get("fact_id"), "arbiter_reject_new")
		ResolutionMode.PREFER_INCUMBENT:
			_registry.reject(m.fact_b.get("fact_id"), "prefer_incumbent")
		ResolutionMode.TABLE_MERGE:
			# JUNIOR WORK-ORDER: table can shape — quorum required (I-2.2.1-001)
			if not _merge.quorum_met(_pending_votes(conflict_id)):
				_bus.emit_signal("provenance_flag", "merge_quorum_failed")
				return ERR_UNAUTHORIZED
			var merged := _merge.apply_merge(m.fact_a, m.fact_b, _pending_votes(conflict_id))
			merged["provenance_actor"] = actor
			var mid: StringName = merged.get("fact_id", m.fact_a.get("fact_id", &""))
			_registry.accept_merged(mid, merged)
		ResolutionMode.SPLIT_THREAD:
			# JUNIOR WORK-ORDER: alternative living-world thread (alternatives_not_banned)
			var fork := {"fact_a": m.fact_a, "fact_b": m.fact_b, "provenance_actor": actor}
			var fid: StringName = m.fact_a.get("fact_id", &"")
			_registry.fork_thread(fid, fork)
		ResolutionMode.DEFER_TO_DM:
			return ERR_BUSY  # still deferred
	_stamp_provenance(conflict_id, chosen, actor)
	_open.erase(conflict_id)
	conflict_resolved.emit(conflict_id, chosen)
	_bus.emit_signal("canon_conflict_resolved", conflict_id, chosen)
	return OK

# Three-way: emit composite manifests pairwise; resolve serially (no cascade merge).
# Timeout / table absent: leave proposed; block stage handoff that needs accepted facts.

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

## Invariants

| ID | Rule |
|----|------|
| I-2.2.1-001 | No silent merge — TABLE_MERGE requires MergeTablePolicy quorum |
| I-2.2.1-002 | Mid-compile resolutions return ERR_BUSY; re-compile via 2.1 DryRun only |
| I-2.2.1-003 | Auto-reject allowed only when `auto_forbidden == false` (tone_violation) |
| I-2.2.1-004 | Sim-active incumbent demotion requires explicit DM override |
| I-2.2.1-005 | Unresolved deferred conflicts block affected stage handoffs (not silent accept) |

## Acceptance

- [x] Parallel spine under `Execution/Phase-2-…/Phase-2-2-…/` (not flat)
- [x] Path-qualified `conceptual_counterpart` → frozen 2.2.1
- [x] Five conflict classes + policy index + six-step loop
- [x] Interfaces for arbiter / manifest / merge / DM queue
- [x] **UX Catalog paint** — L5/SERIES moments bound as JUNIOR WORK-ORDER in pseudo (gold pattern)
- [ ] Half B / DM workbench later

## Junior acceptance / verify (weave)

- [ ] **Verify** `ConflictArbiter` primary entry refuses wrong seat with `Unauthorized` (leaf-true; never silent OK) — row `ux_world_generation` · type `Genesis.Canon.ConflictArbiter`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_world_generation` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** terrain via `ITerrainAuthority` (Terrain3D); Gaea = parallel-maps path only

## Research integration

- Session-scoped RefCounted arbiter (not Autoload); Error/OK + past-tense signals.
- [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Next

~~Paint **2.2.1**~~ done. Phase-2 paint wave finishes with **2.3** / **2.3.1**; then Phase-1 paint start.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
