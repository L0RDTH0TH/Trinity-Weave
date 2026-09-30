---
title: Phase 2.1.1 — CollaborativeRefinementLoop Pause-Point Registry (Execution)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-1-CollaborativeRefinementLoop-Pause-Point-Registry-Roadmap-2026-06-29-1830]]'
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
- pause-point-registry
- collaborative-refinement
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-1-CollaborativeRefinementLoop-Pause-Point-Registry-Roadmap-2026-06-29-1830]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-3-DryRun-and-Provenance-Replay-Contract-Roadmap-2026-06-29-1120]]'
- '[[ux_world_generation]]'
- '[[ux_worldgen_gui]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/children-of-ux_world_generation/ux_worldgen_gui/WALK]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 2.1.1 — CollaborativeRefinementLoop Pause-Point Registry (Execution)

Execution tertiary: **PausePointRegistry**, five default slots, **ScaffoldPreviewBuilder**, **RevisionAcceptancePolicy**, **PauseTimeoutArbiter**. Parallel spine under `Execution/Phase-2-…/Phase-2-1-…/`. **No Half B.** L5 parent + child WALK `ux_worldgen_gui` are **read-only paint feedstock** — collaborative dialogue meaning in junior work-order pseudo (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Registry-driven collaborative pauses between GenerationPipeline stages ([[conceptual 2.1.1]]) |
| Inspiration / L5 bar | Parent L5 + `ux_worldgen_gui` WALK — propose scaffolds, choose/refine, preview, accept/regenerate |
| Inspiration (studied) | (1) Conceptual 2.1.1 + rollup. (2) Execution 2.1 CollaborativeRefinementLoop hooks. (3) Execution 1.3 DryRun + SeedSnapshot. (4) WorldShell research note |
| Execution mechanism | GDScript interfaces + pseudo for registry lookup → preview → accept/revise/timeout → `pause_cleared` |
| Validation | Catalog paint DoD met; 1.3 dry-run never overridden by pause accept |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (+ child `ux_worldgen_gui`) |
| `package_id` | `pkg_world_shell` |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `child_walk` (read-only) | `…/ux_worldgen_gui/WALK.md` |
| `conceptual_pin` | Frozen conceptual 2.1.1 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 / WALK — read-only) |
|-------|---------------------------------------------|
| `row_id` (parent) | `ux_world_generation` |
| Child surface | `ux_worldgen_gui` — Collaborative generation dialogue |
| Label (child) | Propose scaffolds → choose/refine → preview → accept/regenerate |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` (inherits parent) |
| `does_not_mandate` (parent) | one-world=one-campaign; Session-0-checkbox-only; players author first world; unconstrained fresh-noise; default-next = PC creation |
| Child `alternatives_not_banned` | Propose/refine dialogue vs one-shot generate-and-accept; Preview before persist vs write-through; Thin prompt vs deep scaffold menu |
| Pin color keys | Blue (Phase-2 Behavior) · Cyan (SeedSnapshot) |

### Moment → module map (junior)

| L5 / WALK moment | Module / API | Guard | Residue |
|------------------|--------------|-------|---------|
| Enter worldgen GUI / propose scaffolds | `ScaffoldPreviewBuilder.build` + `session_scaffold_preview_ready` | preview_failed → default accept | ScaffoldPreviewManifest (not durable world) |
| Choose/refine | `RevisionAcceptancePolicy.evaluate` revise loop | revision_cap → force accept | revisions dict on accept |
| Preview before persist | pause slots between stages; no WorldHost swap here | DryRun veto wins (I-2.1.1-003) | preview only |
| Accept / regenerate path | `refinement_accepted` / `pause_cleared` → pipeline resumes | REQUIRED slot silently skipped = reject | `session_pause_cleared` |
| Players do not author first world | seat still WorldShell; pause UI only for author seats | wrong seat never arms loop | none |
| Headless / CI | `PausePointRegistry.headless_profile(true)` | all slots disabled | provenance `headless_profile: true` |
| Timeout | `PauseTimeoutArbiter` → default accept | never silent | `session_pause_timeout_defaulted` |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-world-gen-pipeline` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.CollaborativeRefinementLoop` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.WorldGen.CollaborativeRefinementLoop` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility |
|--------|----------------|
| `PausePointRegistry` | Canonical `pause_id` → binding (pre/post stage, policy, enabled) |
| `PausePointBinding` | Slot metadata + default policy + optional composite gate |
| `ScaffoldPreviewBuilder` | Upstream manifests → **ScaffoldPreviewManifest** for active slot |
| `RevisionAcceptancePolicy` | accept / revise / defer / timeout-default outcomes |
| `PauseTimeoutArbiter` | Session timeout → default accept + `session.pause_timeout_defaulted` |
| `CollaborativeRefinementLoop` | Orchestrates registry consult before StageOrchestrator advance |

## Interfaces

```text
enum PausePolicy { OPTIONAL, RECOMMENDED, REQUIRED, DISABLED }

PausePointBinding (RefCounted):
  + pause_id: StringName
  + after_stage: int          # StageId or -1 for seed gate
  + before_stage: int
  + policy: PausePolicy
  + enabled: bool
  + to_dict() -> Dictionary

ScaffoldPreviewManifest (RefCounted):
  + pause_id: StringName
  + stage_context: Dictionary
  + scaffold_delta: Dictionary
  + partial: bool
  + to_dict() -> Dictionary

PausePointRegistry (RefCounted):
  + is_headless() -> bool
  + register(binding: PausePointBinding) -> Error
  + get_binding(pause_id: StringName) -> PausePointBinding
  + binding_for_transition(after_stage: int, before_stage: int) -> PausePointBinding
  + set_enabled(pause_id: StringName, enabled: bool) -> Error
  + headless_profile(enabled: bool) -> void
  signals: pause_slot_changed(pause_id), headless_profile_set(active)

ScaffoldPreviewBuilder (RefCounted):
  + build(pause_id: StringName, upstream: Dictionary) -> Dictionary
  # { ok:bool, preview:ScaffoldPreviewManifest, error:Error }

RevisionAcceptancePolicy (RefCounted):
  + evaluate(decision: Dictionary, preview: Dictionary) -> Dictionary
  # returns { outcome:String, revisions:Dictionary, reason:String }
  # outcome in accept|revise|defer|timeout_default|cap_force_accept

PauseTimeoutArbiter (RefCounted):
  + arm(timeout_sec: float) -> void
  + cancel() -> void
  signals: timeout_fired(pause_id)

CollaborativeRefinementLoop (RefCounted):  # refined from 2.1 stub
  + should_pause(after_stage: int, before_stage: int) -> bool
  + present(preview: Dictionary) -> void
  + await_decision(timeout_sec: float) -> Dictionary
  signals: refinement_accepted(pause_id), refinement_revised(pause_id)
  signals: refinement_timeout(pause_id), pause_cleared(pause_id)
```

### Default registry entries (execution v1)

| pause_id | After → before | Default policy |
|----------|----------------|----------------|
| `pre_terrain_preview` | seed validated → terrain | OPTIONAL |
| `post_terrain_biomes` | terrain → biomes | OPTIONAL |
| `post_biomes_pois` | biomes → POIs | OPTIONAL |
| `post_pois_entities` | POIs → entities | OPTIONAL |
| `pre_compile_review` | sim_bootstrap → DeterministicCompiler | RECOMMENDED |

## Pseudo-code

```pseudo
# 2.1.1 — PausePointRegistry + CollaborativeRefinementLoop (Godot 4 stable).
# Citations: RefCounted, Error/OK, signals — docs.godotengine.org/en/stable/
# Reject: Autoload pause UI; pause accept overriding DryRunValidator fail; silent skip of REQUIRED slots.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 + child ux_worldgen_gui WALK) ===
# Own the collaborative dialogue: propose scaffolds → choose/refine → preview → accept/regenerate.
# Preview residue is ScaffoldPreviewManifest ONLY — durable world still owned by WorldShell accept.
# Table may shape; players do not author first world (seat gate upstream at WorldShell).
# Alternatives allowed: propose/refine vs one-shot; preview-before-persist vs write-through.
# Anti-mandate (inherited): do NOT treat pauses as Session-0 checkbox replacing persistent container.
# DryRunValidator / SeedSnapshotAuthority ALWAYS beat pause accept (I-2.1.1-003).
# ===========================================================

class_name PausePointRegistry
extends RefCounted

func is_headless() -> bool:
	return _headless


signal pause_slot_changed(pause_id)
signal headless_profile_set(active)

var _slots: Dictionary = {}   # StringName -> PausePointBinding
var _headless: bool = false

func seed_defaults() -> void:
	# JUNIOR WORK-ORDER: five dialogue slots spanning seed→compile (WALK propose/refine points)
	_register_default(&"pre_terrain_preview", -1, StageId.TERRAIN, PausePolicy.OPTIONAL)
	_register_default(&"post_terrain_biomes", StageId.TERRAIN, StageId.BIOMES, PausePolicy.OPTIONAL)
	_register_default(&"post_biomes_pois", StageId.BIOMES, StageId.POIS, PausePolicy.OPTIONAL)
	_register_default(&"post_pois_entities", StageId.POIS, StageId.ENTITIES, PausePolicy.OPTIONAL)
	_register_default(&"pre_compile_review", StageId.SIM_BOOTSTRAP, -2, PausePolicy.RECOMMENDED)

func binding_for_transition(after_stage: int, before_stage: int) -> PausePointBinding:
	for b in _slots.values():
		if b.after_stage == after_stage and b.before_stage == before_stage and b.enabled:
			return b
	return null

func headless_profile(enabled: bool) -> void:
	# JUNIOR WORK-ORDER: CI/headless — disable dialogue; record provenance (never silent skip of REQUIRED in interactive)
	_headless = enabled
	for b in _slots.values():
		b.enabled = not enabled
		pause_slot_changed.emit(b.pause_id)
	headless_profile_set.emit(enabled)


class_name CollaborativeRefinementLoop
extends RefCounted

signal refinement_accepted(pause_id)
signal refinement_revised(pause_id)
signal refinement_timeout(pause_id)
signal pause_cleared(pause_id)

var _registry: PausePointRegistry
var _builder: ScaffoldPreviewBuilder
var _policy: RevisionAcceptancePolicy
var _timeout: PauseTimeoutArbiter
var _bus: Object   # session.* emitter (1.1)
var _revision_count: int = 0
var _revision_cap: int = 3

func should_pause(after_stage: int, before_stage: int) -> bool:
	if _registry.is_headless():
		return false
	var b := _registry.binding_for_transition(after_stage, before_stage)
	return b != null and b.policy != PausePolicy.DISABLED and b.enabled

func await_decision(timeout_sec: float) -> Dictionary:
	var b := _active_binding()
	# JUNIOR WORK-ORDER: L5/WALK moment — propose scaffold preview (not durable WorldContainerId)
	var built := _builder.build(b.pause_id, _upstream_snapshot())
	if not built.get("ok", false):
		return {"accepted": true, "reason": "preview_failed_default_accept"}
	_bus.emit_signal("session_scaffold_preview_ready", b.pause_id, built["preview"])
	_timeout.arm(timeout_sec)
	var raw := _wait_table_or_timeout()  # blocks until decision or timeout
	_timeout.cancel()
	if raw.get("timed_out", false):
		# JUNIOR WORK-ORDER: timeout default accept — explicit residue, never silent
		refinement_timeout.emit(b.pause_id)
		_bus.emit_signal("session_pause_timeout_defaulted", b.pause_id)
		pause_cleared.emit(b.pause_id)
		return {"accepted": true, "timeout_default": true}
	var ev := _policy.evaluate(raw, built["preview"])
	match ev.get("outcome", "accept"):
		"revise":
			# JUNIOR WORK-ORDER: choose/refine loop (WALK alternative: propose/refine dialogue)
			_revision_count += 1
			if _revision_count >= _revision_cap:
				ev["outcome"] = "cap_force_accept"
				ev["reason"] = "revision_cap_exceeded"
			else:
				refinement_revised.emit(b.pause_id)
				return await_decision(timeout_sec)  # re-enter preview
		"defer":
			return {"accepted": false, "deferred": true}
	# accept | timeout_default | cap_force_accept
	# JUNIOR WORK-ORDER: accept clears pause — pipeline resumes toward durable compile (2.1)
	_apply_revisions(ev.get("revisions", {}))
	refinement_accepted.emit(b.pause_id)
	_bus.emit_signal("session_pause_cleared", b.pause_id)
	pause_cleared.emit(b.pause_id)
	_revision_count = 0
	return {"accepted": true, "revisions": ev.get("revisions", {})}

# GenerationPipeline.run (2.1) must call should_pause / await_decision
# BEFORE each stage executor AND before DeterministicCompiler (pre_compile_review).
# DryRunValidator fail ALWAYS wins over pause accept (I-2.1.1-003).
# JUNIOR WORK-ORDER: regenerate path is WorldShell.regenerate_container — this loop only shapes pre-persist.

# === WEAVE C# / .NET (Godot 4.6.3) — Terrain3D / Gaea / IWorldGenStage ===
# Manifest: stack-world-gen-pipeline, engine-godot-463-dotnet | Catalog: ux_world_generation
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
| I-2.1.1-001 | Pause accept never mutates SeedSnapshot / world; only downstream stage inputs |
| I-2.1.1-002 | Headless profile disables all slots and records `headless_profile: true` on provenance |
| I-2.1.1-003 | DryRunValidator / SeedSnapshotAuthority veto overrides pause accept at pre_compile |
| I-2.1.1-004 | Timeout defaults to accept + explicit `session.pause_timeout_defaulted` (never silent) |
| I-2.1.1-005 | Sparse/empty scaffold (e.g. zero POIs) still presents preview — not skipped |

## Acceptance

- [x] Parallel spine under `Execution/Phase-2-…/Phase-2-1-…/` (not flat)
- [x] Path-qualified `conceptual_counterpart` → frozen 2.1.1
- [x] Five default `pause_id` rows + six-step loop in pseudo
- [x] Interfaces for registry / preview / policy / timeout
- [x] **UX Catalog paint** — L5 + `ux_worldgen_gui` WALK moments as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / DM workbench widgets later

## Junior acceptance / verify (weave)

- [ ] **Verify** `CollaborativeRefinementLoop` primary entry refuses wrong seat with `Unauthorized` (leaf-true; never silent OK) — row `ux_world_generation` · type `Genesis.WorldGen.CollaborativeRefinementLoop`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_world_generation` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** terrain via `ITerrainAuthority` (Terrain3D); Gaea = parallel-maps path only

## Research integration

- Disposable pipeline under GeneratedWorldContainer — pause loop is RefCounted, not Autoload UI.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Next

~~Paint **2.1.1**~~ done. Campaign continues **2.2** then **2.2.1** / **2.3** / **2.3.1**.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
