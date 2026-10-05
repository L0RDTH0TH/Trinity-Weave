---
title: Phase 2.3 — ToneProfile Profile Bundle on World Seed (Execution)
roadmap-level: secondary
phase-number: 2
subphase-index: "2.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
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
- tone-profile
- world-seed
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 2.3 — ToneProfile Profile Bundle on World Seed (Execution)

Execution secondary for session-0 ToneProfileBundle attachment on SeedBundle, ArchetypeRegistry, ProfileWeightManifest inject, ToneCompatibilityGate, and ToneFallbackResolver. Parallel spine under `Roadmap/Execution/Phase-2-…/Phase-2-3-…/`. **No Half B code.** L5/SERIES are **read-only paint feedstock** — meaning goes into junior work-order pseudo (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | One replaceable campaign tone contract biasing proc-gen + canon gates ([[conceptual 2.3#Behavior]]) |
| Inspiration / L5 bar | L5 wizard+preview tone-aware shape families; anti-mandate unconstrained multi-knob fresh-noise every create |
| Inspiration (studied) | (1) Conceptual 2.3 + tertiary 2.3.1 ProfileWeightManifest. (2) Execution 1.2 ToneProfileInjector. (3) Execution 2.1 SeedParser tone-required gate. (4) Execution 2.2 CanonFactValidator tone gate. |
| Execution mechanism | GDScript interfaces + pseudo for ArchetypeRegistry, ToneProfileBundle, SeedBundleToneAttachment, ToneProfileInjector, ToneCompatibilityGate, ToneFallbackResolver |
| Validation signal | Catalog paint DoD met; tertiary **2.3.1** paints weight tables |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Frozen conceptual 2.3 + 2.3.1 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only) |
|-------|--------------------------------------|
| `row_id` | `ux_world_generation` |
| Label | DM can create (table can shape) a persistent living world |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Own L5 clause | Wizard+preview uses **tone-aware shape families** (cached/pre-existing assets OK) |
| `does_not_mandate` | unconstrained multi-knob fresh-noise every create; Session-0-checkbox-only (no container); one-world=one-campaign; players author first world; default-next = PC creation |
| Alternatives not banned | Directional world-tone × campaign-tone combinations; thin vs deep wizard |
| Pin color keys | Blue (Phase-2 Behavior) · Cyan (SeedSnapshot) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Tone-aware shape families | `ToneProfileInjector.apply` per 2.1 stage | missing tone → SeedParser block | weights on stage context |
| Durable container needs tone | `SeedBundleToneAttachment.attach` | null tone → ERR_INVALID_PARAMETER | tone_fingerprint on SeedBundle |
| Table/DM chooses tone | `Session0ToneSelector.select` | wrong seat upstream | ToneProfileBundle sealed |
| Anti fresh-noise mandate | ArchetypeRegistry + weight tables (2.3.1) | — | bias tables, not free knobs |
| Canon tone bounds | `ToneCompatibilityGate.check` (2.2 accept) | tone fail → reject fact | tone_compat_fail |
| Unknown / import attach | `ToneFallbackResolver` → medium_fantasy | silent unknown banned | `tone_fallback_applied` |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-seed-authority` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.ToneProfileBundle` |
| `stack-world-gen-pipeline` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.ToneProfileBundle` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.ToneProfileBundle` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility |
|--------|----------------|
| `ArchetypeRegistry` | Built-in High / Medium / Low / Grimdark profiles |
| `Session0ToneSelector` | Table/DM choice + Palette veto hooks |
| `ToneProfileBundle` | Immutable-for-session: profile_id + weight_manifest + provenance |
| `ProfileWeightManifest` | Namespaced bias tables (detail → **2.3.1**) |
| `SeedBundleToneAttachment` | Embed tone fingerprint into SeedBundle |
| `ToneProfileInjector` | Apply weights at receptive 2.1 stages |
| `ToneCompatibilityGate` | CanonFactValidator hook (2.2) |
| `ToneFallbackResolver` | Unknown profile_id → Medium Fantasy + bus event |

## Interfaces

```text
enum ToneArchetypeId {
  HIGH_FANTASY,      # tone.high_fantasy
  MEDIUM_FANTASY,    # tone.medium_fantasy (default fallback)
  LOW_FANTASY,       # tone.low_fantasy
  GRIMDARK           # tone.grimdark
}

ToneProfileBundle (RefCounted):
  + profile_id: StringName
  + weight_manifest: Dictionary  # terrain.* biome.* weather.* entity.* event.* quest.*
  + palette_overrides: PackedStringArray
  + fingerprint: String
  + provenance: Dictionary
  + to_dict() -> Dictionary

ArchetypeRegistry (RefCounted):
  + register(profile_id: StringName, manifest: ProfileWeightManifest, meta: Dictionary) -> Error
  + lookup(profile_id: StringName) -> ProfileWeightManifest
  + known_ids() -> PackedStringArray

Session0ToneSelector (RefCounted):
  + select(profile_id: StringName, palette_vetoes: PackedStringArray) -> Dictionary
  # returns { ok:bool, bundle:ToneProfileBundle, error:Error }
  signals: tone_selected(profile_id), palette_veto_applied(keys)

SeedBundleToneAttachment (RefCounted):
  + attach(bundle: SeedBundle, tone: ToneProfileBundle) -> Error
  # missing tone → ERR_INVALID_PARAMETER (same severity as missing map_seed)

ToneProfileInjector (RefCounted):
  + apply(stage_id: int, profile_id: StringName, vetoes: Array) -> Dictionary
  signals: weights_applied(stage_id, profile_id), tone_fallback_applied(profile_id)

ToneCompatibilityGate (RefCounted):
  + check(fact: Dictionary, active: ToneProfileBundle) -> Dictionary
  # { ok:bool, reasons:PackedStringArray }
  signals: tone_compat_pass(fact_id), tone_compat_fail(fact_id, reasons)

ToneFallbackResolver (RefCounted):
  + resolve(profile_id: StringName) -> StringName
  # unknown → &"tone.medium_fantasy" + emit session.tone_fallback_applied
```

## Pseudo-code

```pseudo
# Phase 2.3 — ToneProfile on world seed (Godot 4 stable Error/OK + signals).
# Citations: docs.godotengine.org/en/stable/ (RefCounted, Dictionary, StringName, signals).
# Reject: Autoload ToneProfileBundle; silent missing tone; unknown id without fallback event.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 / SERIES) ===
# Own L5: wizard+preview uses tone-aware shape families (cached assets OK) — NOT free multi-knob noise.
# Anti-mandate: do NOT force unconstrained fresh-noise every create; ArchetypeRegistry supplies bias tables.
# Durable living world requires tone on SeedBundle (same severity as missing map_seed).
# Table/DM selects at Session0; players do not author first world (seat at WorldShell/Session0).
# Alternatives allowed: directional world-tone × campaign-tone; thin vs deep wizard.
# ===========================================================

class_name SeedBundleToneAttachment
extends RefCounted

func attach(seed: SeedBundle, tone: ToneProfileBundle) -> Error:
	# JUNIOR WORK-ORDER: durable container gate — missing tone blocks like missing map_seed
	if tone == null or tone.profile_id == &"":
		return ERR_INVALID_PARAMETER  # SeedParser treats same as missing map_seed
	seed.tone_profile_id = tone.profile_id
	seed.tone_fingerprint = tone.fingerprint
	return OK


class_name ToneProfileInjector
extends RefCounted

signal weights_applied(stage_id, profile_id)
signal tone_fallback_applied(profile_id)

var _registry: ArchetypeRegistry
var _fallback: ToneFallbackResolver

func apply(stage_id: int, profile_id: StringName, vetoes: Array) -> Dictionary:
	# JUNIOR WORK-ORDER: L5 tone-aware shape families → stage weight slices (2.1 DAG)
	var manifest: ProfileWeightManifest = _registry.lookup(profile_id)
	if manifest == null:
		var fb := _fallback.resolve(profile_id)
		# JUNIOR WORK-ORDER: unknown/import path — explicit residue, never silent
		tone_fallback_applied.emit(profile_id)
		manifest = _registry.lookup(fb)
		profile_id = fb
	if manifest == null:
		return {}
	# Palette vetoes already stripped at Session0ToneSelector; expose via slice tables
	var weights: Dictionary = {}
	for ns in [&"terrain", &"biome", &"weather", &"entity", &"event", &"quest"]:
		weights[ns] = manifest.slice(ns).duplicate(true)
	var out: Dictionary = {}
	out["weights"] = weights
	out["profile_id"] = profile_id
	weights_applied.emit(stage_id, profile_id)
	return out


class_name ToneCompatibilityGate
extends RefCounted

signal tone_compat_pass(fact_id)
signal tone_compat_fail(fact_id, reasons)

func check(fact: Dictionary, active: ToneProfileBundle) -> Dictionary:
	# JUNIOR WORK-ORDER: canon accept path — tone bounds are DM-retconnable via reject, not silent
	var reasons: PackedStringArray = []
	# Example bound: grimdark rejects wonder-forward quest framing tags on accept path
	if active.profile_id == &"tone.grimdark" and fact.get("payload", {}).get("framing", "") == "wonder":
		reasons.append("tone_bound_wonder")
	var ok := reasons.is_empty()
	if ok:
		tone_compat_pass.emit(fact.get("fact_id", &""))
	else:
		tone_compat_fail.emit(fact.get("fact_id", &""), reasons)
	return {"ok": ok, "reasons": reasons}

# Built-in archetypes (lean ids): tone.high_fantasy | tone.medium_fantasy |
# tone.low_fantasy | tone.grimdark — defaults, not stereotypes; Palette may veto keys.

# === WEAVE C# / .NET (Godot 4.6.3) — Terrain3D / Gaea / IWorldGenStage ===
# Manifest: stack-seed-authority, stack-world-gen-pipeline, engine-godot-463-dotnet | Catalog: ux_world_generation
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

- [x] Parallel spine path under `Execution/Phase-2-…/Phase-2-3-…/` (not flat)
- [x] Path-qualified `conceptual_counterpart` → conceptual 2.3
- [x] Interfaces + pseudo for ToneProfileBundle / Injector / CompatibilityGate / Fallback
- [x] Tone required on SeedBundle (block severity = missing map seed)
- [x] **UX Catalog paint** — L5/SERIES moments bound as JUNIOR WORK-ORDER in pseudo (gold pattern)
- [x] Tertiary **2.3.1** ProfileWeightManifest Archetype Tables minted
- [x] Edge-case ACs on tertiary (unknown id fallback, Palette veto, grimdark bounds)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `ToneProfileBundle` primary entry refuses wrong seat with `Unauthorized` (leaf-true; never silent OK) — row `ux_world_generation` · type `Genesis.World.ToneProfileBundle`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_world_generation` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** terrain via `ITerrainAuthority` (Terrain3D); Gaea = parallel-maps path only

## Research integration

### Key takeaways

- Tone attachment is **session-scoped RefCounted**, not Autoload gameplay singleton.
- Missing tone blocks SeedBundle formation (2.1 SeedParser) at same severity as missing map seed.
- Unknown profile_id → Medium Fantasy + explicit `tone_fallback_applied` signal/bus event.
- ToneCompatibilityGate is invoked from CanonFactValidator (2.2) — not from stage executors directly.

### Verbatim anchors

> "OK = 0 — Methods that return Error return OK when no error occurred."
> — https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#enum-globalscope-error

> "class_name MyNode extends Node"
> — https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html

### Links

- [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Subphase next

1. ~~Paint **2.3**~~ → done (`paint_ux_catalog: true`).
2. Paint **2.3.1** (this wave) → Phase-2 paint complete → Phase-1 paint start.

## Child links

- [[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed/Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roadmap-2026-06-29-2115|2.3.1 ProfileWeightManifest Archetype Tables]]

## Status

`deepen_complete: true` + **`paint_status: woven`** for Execution **2.3** (`exec-ux-paint-20260929`). Paint ≠ mint L5 files.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
