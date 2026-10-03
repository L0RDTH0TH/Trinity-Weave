---
title: Phase 2 — Procedural Generation and World Building (Execution)
roadmap-level: primary
phase-number: 2
subphase-index: "2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 88
handoff_readiness: 84
roadmap_track: execution
package_id: pkg_world_shell
catalog_row_ids:
- ux_world_generation
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
deepen_complete: phase2_tree_complete
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
created: 2026-09-28
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
weave_pass: exec-weave-stack-ux-20260929
---
## Phase 2 — Execution primary (`pkg_world_shell`)

First execution spine for alpha package **pkg_world_shell** / catalog row **ux_world_generation**. Parallel path mirrors conceptual Phase-2 primary. **No Half B code.** L5/SERIES are **read-only paint feedstock** — meaning goes into junior work-order pseudo (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Durable living-world container — DM creates / table shapes; players do not author first world ([[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914#Behavior]]) |
| Inspiration / L5 bar | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` — wizard+preview, retconnable, import/attach first-class |
| Execution mechanism | Long-lived `WorldShellController` Node under Main → World; disposable gen stages as children of a generated container; regenerate by swapping World children (not deleting `SceneTree.root`) |
| Validation signal | Catalog paint DoD met on this note; secondaries 2.1–2.3 inherit paint pattern; Half B later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Phase-2 primary + supporting SeedSnapshot (1.3.2) — conceptual frozen |
| `dispatch_scope` | **paint_ux_catalog** gold-standard deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only) |
|-------|--------------------------------------|
| `row_id` | `ux_world_generation` |
| Label | DM can create (table can shape) a persistent living world |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| `catalog_face` / `experience_mode` | `living_world` / `world_generation` |
| Child surface | `ux_worldgen_gui` — propose → refine → preview → accept/regenerate |
| `does_not_mandate` | one-world=one-campaign forever; Session-0-checkbox-only (no container); players author first world; unconstrained multi-knob fresh-noise every create; default-next = player character creation |
| Pin color keys | Blue (Phase-2 Behavior) · Cyan (SeedSnapshot supporting) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Enter worldgen GUI / wizard+preview | `WorldShellController.preview_scaffold` + `ux_worldgen_gui` host | wrong seat → `shell_blocked` | PreviewHandle (not yet durable world) |
| Durable container — DM creates initial form | `bootstrap` / `accept_preview` | players cannot call accept | `world_accepted` + WorldContainerId |
| Table can shape; players do not author first world | seat check before accept/regenerate | player seat → refuse | none / blocked code |
| Physical/settlement + monster-region tags | stage manifests via **2.1** (terrain→…→entities) | dry-run fail | layer tags on container |
| Import/attach first-class | `attach_import(WorldImportManifest)` | invalid pack → ShellError | same durable container path |
| Every world-hitting change DM-retconnable | `regenerate_container(RetconReason)` | non-DM → blocked | `world_regenerated`; prior container queue_free |
| Multiple campaigns attach same world | attach API on accepted id (campaign bind later) | — | WorldContainerId reusable |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.WorldShellController` |
| `stack-world-gen-pipeline` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.WorldShellController` |
| `stack-procedural-terrain` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.WorldShellController` |
| `stack-procedural-maps-gaea-parallel` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.WorldShellController` |
| `stack-seed-authority` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.WorldShellController` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility |
|--------|----------------|
| `WorldShellController` | Long-lived Node; owns World host; exposes accept/regenerate/attach API |
| `WorldHost` | Persistent child under Main; children = current generated container |
| `GenerationPipelineStages` | Disposable stage DAG under generated container (seed → sim bootstrap) — **2.1** |
| `CollaborativeRefinementLoop` | Optional DM/table pause points between stages — **2.1.1** tertiary next |
| `CanonIntentBridge` | Interfaces to CanonRegistry / IntentResolver — **2.2** |
| `ToneProfileBundleWire` | Session-0 ToneProfile inject — **2.3** |
| `SafetyGateChain` | SeedSnapshot → DryRunValidator → ProvenanceEnvelope (imports Execution **1.3**) |

## Interfaces

```text
WorldShellController (Node):
  + bootstrap(seed: SeedSnapshot) -> Result[WorldContainerId, ShellError]
  + preview_scaffold(shape_family: ToneAwareShape) -> PreviewHandle
  + accept_preview(handle: PreviewHandle) -> WorldContainerId
  + regenerate_container(reason: RetconReason) -> void  # DM-gated
  + attach_import(pack: WorldImportManifest) -> Result[WorldContainerId, ShellError]
  signals: world_accepted(id), world_regenerated(id), shell_blocked(code)

WorldHost (Node):
  + swap_generated_child(next: Node) -> void   # queue_free prior container
  + active_container() -> Node?

GenerationStage (Node, disposable):
  + run(ctx: GenContext) -> StageResult
  + cancel() -> void
```

## Pseudo-code

```pseudo
# WorldShell bootstrap — citation authority from Godot 4 stable docs.
# Prefer Main → World → generated container; swap children to regenerate.
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 / SERIES) ===
# Seat gate: shared_table | dm_as_player | privileged_access only for accept/regenerate/import.
# Players NEVER author the first world (does_not_mandate + L5 clause 2).
# Path A: wizard+preview → accept_preview (durable). Path B: attach_import (first-class).
# Retcon: regenerate_container is DM-gated; every world-hitting change must call it (not silent mutate).
# Anti-mandate: do NOT force one-campaign-per-world; do NOT treat worldgen as Session-0 checkbox
#   with no persistent container; do NOT default-next into player character creation.
# Child GUI: ux_worldgen_gui owns propose/refine/preview dialogue; this controller owns durability.
# Layers: physical/settlement + monster-region tags land via GenerationPipelineStages (2.1) manifests.
# ===========================================================

class_name WorldShellController
extends Node

@onready var world_host: Node = $World   # typed stage host under Main
var _seat: SeatContext                   # injected from session (Phase 4/1 glue)

func _require_world_author_seat() -> Error:
	# JUNIOR WORK-ORDER: refuse player seat — table may shape; players do not create first world
	if not _seat.allows_any(["shared_table", "dm_as_player", "privileged_access"]):
		shell_blocked.emit("wrong_seat")
		return ERR_UNAUTHORIZED
	return OK

func preview_scaffold(shape_family: ToneAwareShape) -> PreviewHandle:
	# JUNIOR WORK-ORDER: L5 moment — wizard+preview (tone-aware shape families; cached assets OK)
	# Residue: PreviewHandle only — NOT WorldContainerId until accept_preview
	var h := PreviewHandle.new()
	h.shape_family = shape_family
	h.scaffold = build_preview_scaffold(shape_family)  # soft propose; no WorldHost swap yet
	return h

func accept_preview(handle: PreviewHandle) -> Result:
	if _require_world_author_seat() != OK:
		return Err(ShellError.WRONG_SEAT)
	# JUNIOR WORK-ORDER: promote preview → durable living world container
	var seed := SeedSnapshot.from_preview(handle)
	return bootstrap(seed)

func bootstrap(seed: SeedSnapshot) -> Result:
	if _require_world_author_seat() != OK:
		return Err(ShellError.WRONG_SEAT)
	# Survivors stay on controller / GUI / Autoload; disposable stages under container
	var container := GeneratedWorldContainer.new()
	container.name = "GeneratedWorld"
	# JUNIOR WORK-ORDER: run 2.1 DAG so physical/settlement + monster-region tags exist on manifests
	for stage in build_pipeline_stages(seed):
		container.add_child(stage)
	world_host.swap_generated_child(container)
	# Do NOT delete SceneTree.root; avoid setting current_scene alone
	world_accepted.emit(container.id)  # lasting readable state (L5 residue)
	return Ok(container.id)

func regenerate_container(reason: RetconReason) -> void:
	# JUNIOR WORK-ORDER: every world-hitting change is DM-retconnable
	if _require_world_author_seat() != OK:
		return
	var next := GeneratedWorldContainer.new()
	# rebuild from sealed seed + retcon reason; swap frees prior stages
	world_host.swap_generated_child(next)
	world_regenerated.emit(next.id)

func attach_import(pack: WorldImportManifest) -> Result:
	# JUNIOR WORK-ORDER: import/attach first-class (alt to wizard-create — alternatives_not_banned)
	if _require_world_author_seat() != OK:
		return Err(ShellError.WRONG_SEAT)
	var container := GeneratedWorldContainer.from_import(pack)
	world_host.swap_generated_child(container)
	world_accepted.emit(container.id)
	return Ok(container.id)

func WorldHost.swap_generated_child(next: Node) -> void:
	var prev := get_child(0) if get_child_count() > 0 else null
	if prev:
		prev.queue_free()   # frees node AND all children (pipeline stages)
	add_child(next)

# Full main-scene replace ONLY when intentionally leaving shell:
# get_tree().change_scene_to_file(...) / change_scene_to_node(...)
# For simultaneous shell + overlay: get_tree().root.add_child(overlay)

# === WEAVE C# / .NET (Godot 4.6.3) — Terrain3D / Gaea / IWorldGenStage ===
# Manifest: engine-godot-463-dotnet, stack-world-gen-pipeline, stack-procedural-terrain, stack-procedural-maps-gaea-parallel, stack-seed-authority | Catalog: ux_world_generation
# JUNIOR-MANDATORY adapt recipes: [[Docs/Junior-Tech-Adapt-How-To]] (Terrain3D A–B, Gaea C) — not "spike required" alone
namespace Genesis.WorldGen;

public interface ITerrainAuthority {
    Error ImportHeightmap(Image heightmap, float minH, float maxH, Vector3 worldOrigin);
    Error ApplySplatFromBiomeGrid(Image biomeGridOrControl, SeedSnapshot seed);
    Error ApplyHeightAndSplat(SeedSnapshot seed, GenContext ctx); // convenience: Import + Splat from ctx.WorldMapData
}
public interface IMapGenAuthority {
    WorldMapData Generate(WorldSeedState seed); // first-party or Gaea adapter → WorldMapData only
}
public interface IWorldGenStage {
    StringName StageId { get; }
    StageResult Run(GenContext ctx);
}
// Terrain3D: res://addons/terrain_3d/ via ITerrainAuthority only — Gaea ≠ terrain authority
// Gaea: stack-procedural-maps-gaea-parallel — overland → WorldMapData → TerrainAdmitStage
public sealed class Terrain3DAuthority : ITerrainAuthority {
    // JUNIOR WORK-ORDER: dry-run leaves no durable WorldHost child; regen swaps container children
    public Error ImportHeightmap(Image heightmap, float minH, float maxH, Vector3 worldOrigin) {
        if (heightmap == null || heightmap.GetWidth() < 2) return Error.InvalidParameter;
        // Terrain3D import RF/R16 at worldOrigin; streaming bounds update — see Junior-Tech-Adapt-How-To §1
        return Error.Ok;
    }
    public Error ApplySplatFromBiomeGrid(Image biomeGridOrControl, SeedSnapshot seed) {
        if (biomeGridOrControl == null) return Error.InvalidParameter;
        // biome/control → Terrain3D control maps (IBiomeStage) — refuse if gen.stage.biomes unpublished
        return Error.Ok;
    }
    public Error ApplyHeightAndSplat(SeedSnapshot seed, GenContext ctx) {
        var map = ctx.RequireWorldMapData();
        var err = ImportHeightmap(map.HeightmapImage, map.MinH, map.MaxH, map.Origin);
        if (err != Error.Ok) return err;
        return ApplySplatFromBiomeGrid(map.BiomeGridOrControl, seed);
    }
}
public sealed class TerrainAdmitStage : IWorldGenStage {
    public StringName StageId => "terrain";
    private readonly ITerrainAuthority _terrain;
    public TerrainAdmitStage(ITerrainAuthority terrain) => _terrain = terrain;
    public StageResult Run(GenContext ctx) {
        var err = _terrain.ApplyHeightAndSplat(ctx.Seed, ctx);
        return err == Error.Ok ? StageResult.Ok() : StageResult.Fail(err);
    }
}

```

## Acceptance criteria (execution — stub→playable ladder)

- [x] Parallel spine note exists under `Roadmap/Execution/Phase-2-…/` (not flat heap)
- [x] Path-qualified `conceptual_counterpart` → frozen conceptual Phase-2 primary
- [x] Pseudo-code + interfaces for WorldShell host / regenerate semantics
- [x] **UX Catalog paint** — L5/SERIES moments bound as JUNIOR WORK-ORDER in pseudo (gold pattern)
- [x] Godot stable verbatim citations in Research integration
- [x] Secondary execution mirrors **2.1 / 2.2 / 2.3** minted (map gen)
- [x] Tertiary stage notes with edge-case ACs (2.1.1 / 2.2.1 / 2.3.1 minted)
- [x] Catalog `execution_pins` coverage audited green for package row (primary-only pin policy)
- [x] Secondaries/tertiaries **2.1–2.3.1** paint_ux_catalog (Phase-2 paint complete)
- [ ] `execution_factory_handoff_ready` / Half B (later)

## Junior acceptance / verify (weave)

- [ ] **Verify** `WorldShellController` primary entry refuses wrong seat with `Unauthorized` (leaf-true; never silent OK) — row `ux_world_generation` · type `Genesis.World.WorldShellController`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_world_generation` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** terrain via `ITerrainAuthority.ImportHeightmap` + splat (Terrain3D); Gaea = `WorldMapData` parallel only — see [[Docs/Junior-Tech-Adapt-How-To]] §1–2

## Research integration

### Key takeaways

- Prefer **Main → World → (generated container)**; swap World children for regen.
- `SceneTree.root` is permanent; `current_scene` is usually its child beside Autoloads — do not delete root.
- Setting `current_scene` alone does **not** add/remove nodes.
- `change_scene_to_node`: outgoing scene removed immediately; freed end-of-frame; SceneTree owns/frees new node on next change.
- Manual shell: `get_tree().root.add_child(scene)`.
- `queue_free()` frees the node **and all children**.
- `class_name WorldShellController extends Node` + `@onready` typed stage refs.

### Verbatim quotes + stable URLs

> "Finally, when a node is freed with Object.free() or queue_free(), it will also free all its children."
> — https://docs.godotengine.org/en/stable/classes/class_node.html

> "The root node of the currently loaded main scene, usually as a direct child of root."
> "Warning: Setting this property directly may not work as expected, as it does not add or remove any nodes from this tree."
> — https://docs.godotengine.org/en/stable/classes/class_scenetree.html

> "When changing levels, you can then swap out the children of the \"World\" node."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "get_tree().root.add_child(simultaneous_scene)"
> — https://docs.godotengine.org/en/stable/tutorials/scripting/change_scenes_manually.html

> "class_name MyNode extends Node"
> — https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html

### Links

- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next (execution paint DFS)

1. ~~Gold-standard paint on Phase-2 primary~~ done.
2. ~~Paint secondaries/tertiaries **2.1–2.3.1**~~ done (`phase2_paint_complete`).
3. Phase-order paint continues on Phases 1→6 (campaign cursor owned by `roadmap-state-execution.md`).
4. No Half B. No inventing new twins.

## Status

Phase-2 execution tree **fully UX Catalog painted** (`paint_status: woven` on primary + 2.1–2.3.1). Gold junior-work-order pattern for `pkg_world_shell` / `ux_world_generation`. Campaign continues phase-order on remaining spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
