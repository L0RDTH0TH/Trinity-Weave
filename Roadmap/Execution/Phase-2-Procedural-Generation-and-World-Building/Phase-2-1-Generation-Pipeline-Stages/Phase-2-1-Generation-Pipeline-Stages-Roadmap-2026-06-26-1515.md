---
title: Phase 2.1 — Generation Pipeline Stages (Execution)
roadmap-level: secondary
phase-number: 2
subphase-index: "2.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
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
- generation-pipeline
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 2.1 — Generation Pipeline Stages (Execution)

Execution secondary for SeedParser → stage DAG (`terrain → biomes → POIs → entities → sim_bootstrap`) → DeterministicCompiler under disposable generated-world container. Parallel spine under `Roadmap/Execution/Phase-2-…/Phase-2-1-…/`. **No Half B code.** L5/SERIES are **read-only paint feedstock** — meaning goes into junior work-order pseudo (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Collaborative world-forge pipeline with dry-run gates + optional refinement pauses ([[conceptual 2.1#Behavior]]) |
| Inspiration / L5 bar | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` — physical/settlement layers + monster-region tags via stage manifests; table can shape between stages |
| Inspiration (studied) | (1) Conceptual 2.1 + tertiary 2.1.1. (2) Execution 1.2 StageOrchestrator / DeterministicCompiler. (3) Execution Phase-2 WorldShell swap semantics. (4) [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]] |
| Execution mechanism | GDScript interfaces + pseudo for SeedParser, GenerationPipeline, stage executors, CollaborativeRefinementLoop hooks, DryRun + compile |
| Validation signal | Catalog paint DoD met on this note; tertiary **2.1.1** paints collaborative dialogue; Half B later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Frozen conceptual 2.1 + 2.1.1 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only) |
|-------|--------------------------------------|
| `row_id` | `ux_world_generation` |
| Label | DM can create (table can shape) a persistent living world |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| `catalog_face` / `experience_mode` | `living_world` / `world_generation` |
| Child surface | `ux_worldgen_gui` — propose → refine → preview → accept (pause hooks → **2.1.1**) |
| `does_not_mandate` | one-world=one-campaign forever; Session-0-checkbox-only (no container); players author first world; unconstrained multi-knob fresh-noise every create; default-next = player character creation |
| Pin color keys | Blue (Phase-2 Behavior) · Cyan (SeedSnapshot supporting) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Physical/settlement + monster-region tags | stage DAG `Terrain→Biomes→POIs→Entities→SimBootstrap` → manifests | dry-run fail / partial stage | layer tags on compiled container |
| Table can shape (between stages) | `CollaborativeRefinementLoop` pause hooks | headless / DISABLED → skip | `refinement_pause` scaffold_delta |
| Durable container after accept | `DeterministicCompiler` + `pipeline_complete` | pre_compile dry-run veto | `CompiledWorldManifest` id |
| Wizard+preview tone-aware families | `ToneProfileInjector.apply` per stage | missing tone → SeedParser block | tone_fingerprint on SeedBundle |
| Players do not author first world | seat check at WorldShell (parent); pipeline assumes author seat already cleared | wrong seat never reaches `run` | none / blocked upstream |
| Import/attach first-class | import path still runs same DAG under imported seed | invalid pack → ShellError upstream | same manifest residue path |
| Every world-hitting change DM-retconnable | regen swaps container → new `GenerationPipeline.run` | non-DM blocked at WorldShell | prior container `queue_free` |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-world-gen-pipeline` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.GenerationPipeline` |
| `stack-procedural-terrain` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.GenerationPipeline` |
| `stack-procedural-maps` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.GenerationPipeline` |
| `stack-hydrology` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.GenerationPipeline` |
| `stack-biome-assignment` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.GenerationPipeline` |
| `stack-poi-settlement` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.GenerationPipeline` |
| `stack-entity-bootstrap` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.GenerationPipeline` |
| `stack-procedural-maps-gaea-parallel` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.GenerationPipeline` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.GenerationPipeline` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility |
|--------|----------------|
| `SeedParser` | Session-0 → SeedBundle + ProvenanceEnvelope; blocks if tone missing |
| `GenerationPipeline` | Owns DAGValidator + StageOrchestrator under generated container |
| `TerrainStageExecutor` | SeedBundle + tone weights → TerrainManifest |
| `BiomeStageExecutor` | TerrainManifest → BiomeManifest |
| `POIStageExecutor` | BiomeManifest + accepted hooks → POIManifest |
| `EntityStageExecutor` | POIManifest + LoreHookRegistry → EntityManifest |
| `SimBootstrapStageExecutor` | EntityManifest → SimGraphSeed |
| `CollaborativeRefinementLoop` | Optional pause points (registry detail → **2.1.1**) |
| `DryRunValidator` | Entry + pre-compile (import Execution 1.3.3) |
| `DeterministicCompiler` | Manifests → byte-stable CompiledWorldManifest |
| `WorldEventLogInitializer` | Seed append-only log from compiled manifest |

## Interfaces

```text
enum StageId { TERRAIN, BIOMES, POIS, ENTITIES, SIM_BOOTSTRAP }

SeedBundle (RefCounted):
  + map_seed: int
  + tone_profile_id: StringName
  + accepted_fact_ids: PackedStringArray
  + tone_fingerprint: String
  + to_dict() -> Dictionary

SeedParser (RefCounted):
  + parse(session_closure: Dictionary) -> Dictionary
  # { ok:bool, bundle:SeedBundle, error:Error, missing:PackedStringArray }
  signals: seed_bundle_ready(fingerprint), seed_bundle_blocked(missing)

IStageExecutor (RefCounted):
  + stage_id() -> StageId
  + run(upstream: Dictionary, weights: Dictionary) -> Dictionary
  # returns manifest Dictionary; may set partial:true + reason

GenerationPipeline (Node, disposable under GeneratedWorldContainer — NOT Autoload):
  + run(bundle: SeedBundle) -> Error
  + last_manifests() -> Dictionary
  + last_compiled() -> Dictionary
  signals: stage_ready(stage_id), stage_failed(stage_id, reason)
  signals: pipeline_complete(manifest_id), pipeline_aborted(reason)
  signals: refinement_pause(stage_id, scaffold_delta)

CollaborativeRefinementLoop (RefCounted):
  + should_pause(after_stage: int, before_stage: int) -> bool
  + present(scaffold_delta: Dictionary) -> void
  + await_decision(timeout_sec: float) -> Dictionary  # {accepted:bool, revisions:Dictionary}
  signals: refinement_accepted(stage_id), refinement_timeout(stage_id)

WorldEventLogInitializer (RefCounted):
  + init_from(manifest: Dictionary) -> Error
  signals: world_event_log_ready(path_hint)
```

## Pseudo-code

```pseudo
# Phase 2.1 — Generation pipeline under disposable container (Godot 4 stable).
# Citations: docs.godotengine.org/en/stable/ (Node, RefCounted, Error/OK, queue_free children).
# Reject: Autoload GenerationPipeline; world write inside DryRunValidator; unseeded RNG in compile.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 / SERIES) ===
# Own L5 clause 3: Physical/settlement layers + monster-region tags land as stage manifests.
# Table can shape between stages via CollaborativeRefinementLoop (ux_worldgen_gui dialogue → 2.1.1).
# Durable residue = CompiledWorldManifest after DeterministicCompiler — NOT preview scaffolds.
# Anti-mandate: do NOT treat this DAG as Session-0 checkbox with no persistent container
#   (WorldShell owns container; this Node is disposable under it).
# Anti-mandate: do NOT force unconstrained multi-knob fresh-noise every stage — ToneProfileInjector
#   weights are tone-aware shape families / cached bias, not free-noise knobs.
# Seat gate is WorldShell's job; pipeline assumes author seat already cleared before run().
# Retcon path: WorldShell.regenerate_container → new container → this run() again; prior queue_free.
# ===========================================================

class_name GenerationPipeline
extends Node

signal stage_ready(stage_id)
signal stage_failed(stage_id, reason)
signal pipeline_complete(manifest_id)
signal pipeline_aborted(reason)
signal refinement_pause(stage_id, scaffold_delta)

var _dag: DAGValidator          # from Execution 1.2
var _dry_run: DryRunValidator   # from Execution 1.3
var _snapshot: SeedSnapshotAuthority
var _injector: ToneProfileInjector
var _intent: IntentResolver     # boundary with 2.2
var _compiler: DeterministicCompiler
var _loop: CollaborativeRefinementLoop
var _executors: Dictionary      # StageId -> IStageExecutor
var _manifests: Dictionary = {}

func run(bundle: SeedBundle) -> Error:
	# JUNIOR WORK-ORDER: entry dry-run — refuse world write on fail (L5 guard / residue gate)
	var snap := _snapshot.last_sealed()
	var entry := _dry_run.validate({"phase": "entry", "bundle": bundle.to_dict()}, snap)
	if entry.get("outcome", "") == "fail":
		pipeline_aborted.emit("dry_run_entry")
		return ERR_INVALID_PARAMETER
	var err := _dag.preflight(_default_edges())
	if err != OK:
		pipeline_aborted.emit("dag_preflight")
		return err
	# JUNIOR WORK-ORDER: L5 physical/settlement + monster-region path = ordered stage DAG
	var order: Array = [StageId.TERRAIN, StageId.BIOMES, StageId.POIS, StageId.ENTITIES, StageId.SIM_BOOTSTRAP]
	var prev_sid: int = -1
	for sid in order:
		if _loop.should_pause(prev_sid, int(sid)):
			# JUNIOR WORK-ORDER: table can shape — pause feeds ux_worldgen_gui propose/refine (2.1.1)
			var delta := {"stage": sid, "upstream": _upstream(sid)}
			refinement_pause.emit(sid, delta)
			var decision := _loop.await_decision(session_policy_timeout())
			if not decision.get("accepted", true):
				# timeout default accept is encoded in CollaborativeRefinementLoop
				pass
		# JUNIOR WORK-ORDER: tone-aware shape families (cached assets OK) — not free multi-knob noise
		var weights := _injector.apply(sid, bundle.tone_profile_id, [])
		if sid in [StageId.POIS, StageId.ENTITIES, StageId.SIM_BOOTSTRAP]:
			err = _intent.resolve_for_stage(sid, null)
			if err != OK:
				stage_failed.emit(sid, "intent_gate")
				pipeline_aborted.emit("intent")
				return err
		var m: Dictionary = _executors[sid].run(_upstream(sid), weights)
		if m.get("partial", false):
			stage_failed.emit(sid, m.get("reason", "partial"))
			pipeline_aborted.emit("stage_partial")
			return ERR_BUG
		# JUNIOR WORK-ORDER: residue — layer tags / manifests accumulate on container context
		_manifests[sid] = m
		stage_ready.emit(sid)
		prev_sid = int(sid)
	var pre := _dry_run.validate({"phase": "pre_compile", "manifests": _manifests}, snap)
	if pre.get("outcome", "") == "fail":
		pipeline_aborted.emit("dry_run_pre_compile")
		return ERR_BUSY
	# JUNIOR WORK-ORDER: promote stage manifests → durable CompiledWorldManifest (living-world residue)
	var compiled := _compiler.compile(bundle, _manifests, _intent.lore_hooks())
	if not compiled.get("ok", false):
		pipeline_aborted.emit("compile")
		return int(compiled.get("error", ERR_BUG))
	pipeline_complete.emit(str(compiled.get("manifest_id", "")))
	return OK

# Stages live as children of GeneratedWorldContainer; WorldHost.swap_generated_child
# queue_free() frees prior container AND all pipeline nodes (stable Node docs).
# JUNIOR WORK-ORDER: retcon = swap new container + re-run — never silent mutate prior manifests.

# === WEAVE C# / .NET (Godot 4.6.3) — Terrain3D / Gaea / IWorldGenStage ===
# JUNIOR-MANDATORY: [[Docs/Junior-Tech-Adapt-How-To]] §1–2 (ImportHeightmap→splat; Gaea≠terrain)
# Manifest: stack-world-gen-pipeline, stack-procedural-terrain, stack-procedural-maps, stack-hydrology, stack-biome-assignment, stack-poi-settlement, stack-entity-bootstrap, stack-procedural-maps-gaea-parallel, engine-godot-463-dotnet | Catalog: ux_world_generation
namespace Genesis.WorldGen;

public interface ITerrainAuthority {
    Error ImportHeightmap(Image heightmap, float minH, float maxH, Vector3 worldOrigin);
    Error ApplySplatFromBiomeGrid(Image biomeGridOrControl, SeedSnapshot seed);
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
    public Error ImportHeightmap(Image heightmap, float minH, float maxH, Vector3 worldOrigin) {
        if (heightmap == null || heightmap.GetWidth() < 2) return Error.InvalidParameter;
        return Error.Ok; // Terrain3D RF import — see Junior-Tech-Adapt-How-To §1
    }
    public Error ApplySplatFromBiomeGrid(Image biomeGridOrControl, SeedSnapshot seed) {
        if (biomeGridOrControl == null) return Error.InvalidParameter;
        return Error.Ok;
    }
    public Error ApplyHeightAndSplat(SeedSnapshot seed, GenContext ctx) {
        var map = ctx.RequireWorldMapData();
        var err = ImportHeightmap(map.HeightmapImage, map.MinH, map.MaxH, map.Origin);
        return err != Error.Ok ? err : ApplySplatFromBiomeGrid(map.BiomeGridOrControl, seed);
    }
}

```

## Acceptance criteria (execution)

- [x] Parallel spine path under `Execution/Phase-2-…/Phase-2-1-…/` (not flat)
- [x] Path-qualified `conceptual_counterpart` → conceptual 2.1
- [x] Interfaces + pseudo for SeedParser / GenerationPipeline / stage executors / DryRun gates
- [x] **UX Catalog paint** — L5/SERIES moments bound as JUNIOR WORK-ORDER in pseudo (gold pattern)
- [x] Godot stable citations in Research integration (whitelist)
- [x] Tertiary **2.1.1** CollaborativeRefinementLoop pause-point registry minted
- [x] Edge-case ACs on tertiary (timeout accept, sparse_world, dry-run veto)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `GenerationPipeline` primary entry refuses wrong seat with `Unauthorized` (leaf-true; never silent OK) — row `ux_world_generation` · type `Genesis.WorldGen.GenerationPipeline`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_world_generation` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** terrain via `ITerrainAuthority` (Terrain3D); Gaea = parallel-maps path only

## Research integration

### Key takeaways

- Pipeline Node is **disposable** under generated container — not Autoload; regen swaps World children.
- `queue_free()` on container frees all stage children (WorldShell primary contract).
- Fallible APIs return GlobalScope `Error` / `OK`; past-tense signals on owners.
- DryRunValidator never mutates world; DeterministicCompiler forbids wall-clock / unseeded entropy.

### Verbatim anchors

> "Finally, when a node is freed with Object.free() or queue_free(), it will also free all its children."
> — https://docs.godotengine.org/en/stable/classes/class_node.html

> "When changing levels, you can then swap out the children of the \"World\" node."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "OK = 0 — Methods that return Error return OK when no error occurred."
> — https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#enum-globalscope-error

### Links

- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]
- [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Subphase next

1. ~~Paint **2.1**~~ → done (`paint_ux_catalog: true`).
2. Paint wave continues **2.1.1** / **2.2** (this campaign) then **2.2.1** / **2.3** / **2.3.1**.

## Child links

- [[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-1-CollaborativeRefinementLoop-Pause-Point-Registry-Roadmap-2026-06-29-1830|2.1.1 Pause-Point Registry]]

## Status

`deepen_complete: true` + **`paint_status: woven`** for Execution **2.1** (`exec-ux-paint-20260929`). Paint ≠ mint L5 files.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
