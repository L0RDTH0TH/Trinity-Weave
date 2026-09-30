---
title: Phase 2.3.1 — ProfileWeightManifest Archetype Tables (Execution)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed/Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roadmap-2026-06-29-2115]]'
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
- tone-profile
- profile-weight-manifest
- archetype-registry
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed/Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roadmap-2026-06-29-2115]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 2.3.1 — ProfileWeightManifest Archetype Tables (Execution)

Execution tertiary: **ArchetypeRegistry**, four built-in tone ids, six **ProfileWeightManifest** namespaces, **PaletteVetoKey**, **ReceptiveNodeBinding**, **NamespaceDefaultResolver**. Parallel spine under `Execution/Phase-2-…/Phase-2-3-…/`. **No Half B.** L5/SERIES are **read-only paint feedstock** — meaning goes into junior work-order pseudo (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Canonical archetype weight tables for ToneProfileInjector ([[conceptual 2.3.1]]) |
| Inspiration / L5 bar | Tone-aware shape families + directional world-tone × campaign-tone (alternatives_not_banned); anti unconstrained fresh-noise |
| Inspiration (studied) | (1) Conceptual 2.3.1 + rollup. (2) Execution 2.3 ToneProfileInjector. (3) Execution 1.2.1 stage DAG. (4) Execution 2.1 receptive stages |
| Execution mechanism | Registry + namespace tables + veto/fallback → injector at stage nodes |
| Validation | Catalog paint DoD met; unknown id → medium_fantasy + signal; missing tone still blocks SeedParser |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Frozen conceptual 2.3.1 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only) |
|-------|--------------------------------------|
| `row_id` | `ux_world_generation` |
| Label | DM can create (table can shape) a persistent living world |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Own L5 clause | Cached/pre-existing tone-aware shape families (High/Medium/Low/Grimdark tables) |
| `does_not_mandate` | unconstrained multi-knob fresh-noise every create |
| Alternatives not banned | Directional world-tone × campaign-tone; Palette veto without changing profile_id |
| Pin color keys | Blue (Phase-2 Behavior) · Cyan (SeedSnapshot) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Tone-aware families as tables | `ArchetypeRegistry.seed_builtins` + `ProfileWeightManifest` | four ids required before Session0 | registered manifests |
| Stage layer bias (physical/settlement path) | `ReceptiveNodeBinding` → injector slices | empty after veto → NamespaceDefaultResolver | ns weights per stage |
| Table Palette shaping | `PaletteVetoKey` suppressions | full-ns veto → defaults only for that ns | sealed bundle still durable |
| Anti fresh-noise | bias tables not free knobs | — | deterministic weights |
| Unknown / import attach | fallback `tone.medium_fantasy` | silent missing banned | `tone_fallback_applied` |
| Missing tone still blocks | parent SeedParser (2.1/2.3) | tables do not waive | ERR_INVALID_PARAMETER |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-seed-authority` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.ProfileWeightManifest` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.ProfileWeightManifest` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility |
|--------|----------------|
| `ArchetypeRegistry` | Stable `profile_id` → default ProfileWeightManifest + metadata |
| `ProfileWeightManifest` | Namespaced bias tables (`terrain`…`quest`) |
| `PaletteVetoKey` | Dot-path suppressions without changing `profile_id` |
| `NamespaceDefaultResolver` | When namespace fully vetoed → archetype defaults for that ns only |
| `ReceptiveNodeBinding` | Namespace → stage seam / executor |
| `ToneProfileInjector` | Applies slices at GenerationPipeline stage traversal (2.1 / 2.3) |

## Interfaces

```text
ProfileWeightManifest (RefCounted):
  + profile_id: StringName
  + namespaces: Dictionary   # StringName -> Dictionary of bias keys
  + fingerprint() -> String
  + slice(ns: StringName) -> Dictionary
  + to_dict() -> Dictionary

ArchetypeRegistry (RefCounted):
  + register(profile_id: StringName, manifest: ProfileWeightManifest, meta: Dictionary) -> Error
  + lookup(profile_id: StringName) -> ProfileWeightManifest
  + known_ids() -> PackedStringArray
  signals: archetype_registered(profile_id), archetype_missing(profile_id)

PaletteVetoKey:
  # value type: StringName dot-path e.g. &"terrain.elevated_relief"

NamespaceDefaultResolver (RefCounted):
  + resolve(ns: StringName, remaining: Dictionary, defaults: Dictionary) -> Dictionary

ReceptiveNodeBinding (RefCounted):
  + ns: StringName
  + seam_id: StringName
  + stage_id: int
  + to_dict() -> Dictionary

ToneProfileInjector (RefCounted):  # refined from 2.3
  + apply(stage_id: int, profile_id: StringName, vetoes: Array) -> Dictionary
  signals: weights_applied(stage_id, ns), tone_fallback_applied(profile_id)
```

### ReceptiveNodeBinding index (execution v1)

| Namespace | seam_id | StageId |
|-----------|---------|---------|
| `terrain` | `gen.stage.terrain` | TERRAIN |
| `biome` | `gen.stage.biomes` | BIOMES |
| `weather` | `gen.stage.biomes` | BIOMES |
| `entity` | `gen.stage.entities` | ENTITIES |
| `event` | `gen.stage.sim_bootstrap` | SIM_BOOTSTRAP |
| `quest` | `gen.stage.sim_bootstrap` | SIM_BOOTSTRAP |

### Built-in archetype ids

`tone.high_fantasy` | `tone.medium_fantasy` | `tone.low_fantasy` | `tone.grimdark`

## Pseudo-code

```pseudo
# 2.3.1 — ArchetypeRegistry + ProfileWeightManifest (Godot 4 stable).
# Citations: class_name / RefCounted / Error/OK — docs.godotengine.org/en/stable/
# Reject: Autoload tone singleton; unknown id without fallback signal; empty-tone SeedBundle.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 / SERIES) ===
# Own the tone-aware shape-family TABLES (High/Medium/Low/Grimdark) — cached bias, not free noise.
# Anti-mandate: do NOT force unconstrained multi-knob fresh-noise; inject bias slices only.
# Alternatives: Palette veto without changing profile_id; directional tone combinations via tables.
# Missing tone still blocks SeedParser — these tables do NOT waive the durable-container gate.
# ===========================================================

class_name ArchetypeRegistry
extends RefCounted

signal archetype_registered(profile_id)
signal archetype_missing(profile_id)

var _rows: Dictionary = {}  # StringName -> {manifest, meta}

func seed_builtins() -> void:
	# JUNIOR WORK-ORDER: four L5-aligned tone families registered before Session0 close
	for id in [
		&"tone.high_fantasy", &"tone.medium_fantasy",
		&"tone.low_fantasy", &"tone.grimdark",
	]:
		var m := ProfileWeightManifest.new()
		m.profile_id = id
		m.namespaces = _default_tables_for(id)
		register(id, m, {"display": str(id)})

func register(profile_id: StringName, manifest: ProfileWeightManifest, meta: Dictionary) -> Error:
	if profile_id == StringName():
		return ERR_INVALID_PARAMETER
	_rows[profile_id] = {"manifest": manifest, "meta": meta}
	archetype_registered.emit(profile_id)
	return OK

func lookup(profile_id: StringName) -> ProfileWeightManifest:
	if not _rows.has(profile_id):
		archetype_missing.emit(profile_id)
		return null
	return _rows[profile_id]["manifest"]

func known_ids() -> PackedStringArray:
	return PackedStringArray(_table.keys())


class_name ToneProfileInjector
extends RefCounted

signal weights_applied(stage_id, ns)
signal tone_fallback_applied(profile_id)

var _registry: ArchetypeRegistry
var _bindings: Array = []   # ReceptiveNodeBinding
var _resolver: NamespaceDefaultResolver
const FALLBACK_ID := &"tone.medium_fantasy"

func apply(stage_id: int, profile_id: StringName, vetoes: Array) -> Dictionary:
	var mid := profile_id
	var manifest := _registry.lookup(mid)
	if manifest == null:
		# JUNIOR WORK-ORDER: import/unknown — explicit fallback residue (never silent)
		mid = FALLBACK_ID
		manifest = _registry.lookup(mid)
		tone_fallback_applied.emit(profile_id)
		# bus: session.tone_fallback_applied
	var out: Dictionary = {}
	for b in _bindings:
		if b.stage_id != stage_id:
			continue
		# JUNIOR WORK-ORDER: physical/settlement-adjacent bias lands via ns→stage bindings
		var slice: Dictionary = manifest.slice(b.ns).duplicate(true)
		for v in vetoes:
			# JUNIOR WORK-ORDER: table Palette can shape without changing profile_id
			var key := StringName(v)
			if str(key).begins_with(str(b.ns) + "."):
				slice.erase(str(key).get_slice(".", 1))
		if slice.is_empty():
			slice = _resolver.resolve(b.ns, slice, manifest.slice(b.ns))
		out[b.ns] = slice
		weights_applied.emit(stage_id, b.ns)
	return out

# Session0: ArchetypeRegistry.lookup → optional Palette vetoes →
# NamespaceDefaultResolver → ToneProfileBundle seal → SeedBundleToneAttachment.
# ToneCompatibilityGate (2.2/2.3) reads active profile_id + manifest bounds.
# JUNIOR WORK-ORDER: tables never waive missing-tone SeedParser block (I-2.3.1-004).

# === WEAVE C# / .NET (Godot 4.6.3) — Terrain3D / Gaea / IWorldGenStage ===
# Manifest: stack-seed-authority, engine-godot-463-dotnet | Catalog: ux_world_generation
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
| I-2.3.1-001 | Four built-in ids always registered before Session0 close |
| I-2.3.1-002 | Unknown `profile_id` → medium_fantasy + explicit `tone_fallback_applied` |
| I-2.3.1-003 | Full-namespace veto restores archetype defaults for that namespace only |
| I-2.3.1-004 | Missing tone still blocks SeedParser (parent 2.3 / 2.1) — tables do not waive |
| I-2.3.1-005 | Injector is session RefCounted — not Autoload gameplay singleton |

## Acceptance

- [x] Parallel spine under `Execution/Phase-2-…/Phase-2-3-…/` (not flat)
- [x] Path-qualified `conceptual_counterpart` → frozen 2.3.1
- [x] Four archetypes + six namespaces + ReceptiveNodeBinding index
- [x] Interfaces + pseudo for registry / injector / veto resolver
- [x] **UX Catalog paint** — L5/SERIES moments bound as JUNIOR WORK-ORDER in pseudo (gold pattern)
- [ ] Half B / data loaders later

## Junior acceptance / verify (weave)

- [ ] **Verify** `ProfileWeightManifest` primary entry refuses wrong seat with `Unauthorized` (leaf-true; never silent OK) — row `ux_world_generation` · type `Genesis.World.ProfileWeightManifest`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_world_generation` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** terrain via `ITerrainAuthority` (Terrain3D); Gaea = parallel-maps path only

## Research integration

- Session-scoped tone attachment; class_name + Error/OK patterns from Phase-1 research.
- [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Next

~~Paint **2.3.1**~~ done. **Phase-2 paint complete** (`phase2_remaining: 0`). Next campaign cursor: Phase-1 primary paint start.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
