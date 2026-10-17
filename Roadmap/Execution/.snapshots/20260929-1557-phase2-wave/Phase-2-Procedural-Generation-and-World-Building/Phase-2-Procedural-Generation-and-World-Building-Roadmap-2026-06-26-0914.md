---
title: Phase 2 — Procedural Generation and World Building (Execution)
roadmap-level: primary
phase-number: 2
subphase-index: "2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 25
handoff_readiness: 72
roadmap_track: execution
package_id: pkg_world_shell
catalog_row_ids:
- ux_world_generation
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-28
tags:
- roadmap
- genesis-mythos-master
- phase
- execution
- pkg_world_shell
para-type: Project
conceptual_counterpart: '[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
links:
- '[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[ux_world_generation]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
updated: 2026-09-29
weave_pass: exec-weave-stack-ux-20260929
---
## Phase 2 — Execution primary (`pkg_world_shell`)

First post-bootstrap execution spine for alpha package **pkg_world_shell** / catalog row **ux_world_generation**. Parallel path mirrors conceptual Phase-2 primary. **No Half B code.** **No L5 / factory deepen.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Durable living-world container — DM creates / table shapes; players do not author first world ([[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914#Behavior]]) |
| Inspiration / L5 bar | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` — wizard+preview, retconnable, import/attach first-class |
| Execution mechanism | Long-lived `WorldShellController` Node under Main → World; disposable gen stages as children of a generated container; regenerate by swapping World children (not deleting `SceneTree.root`) |
| Validation signal | Catalog `execution_pins[]` resolves to this note; secondary 2.1–2.3 execution mirrors carry stage interfaces; playable exit criterion remains Loop-3 / Half B later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Phase-2 primary + supporting SeedSnapshot (1.3.2) — conceptual frozen |
| `dispatch_scope` | Execution Phase-2 primary mint only (single structural artifact) |

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
| `GenerationPipelineStages` | Disposable stage DAG under generated container (seed → sim bootstrap) |
| `CanonIntentBridge` | Interfaces to CanonRegistry / IntentResolver (execution secondary 2.2) |
| `ToneProfileBundleWire` | Session-0 ToneProfile inject (execution secondary 2.3) |

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

class_name WorldShellController
extends Node

@onready var world_host: Node = $World   # typed stage host under Main

func bootstrap(seed: SeedSnapshot) -> Result:
    # Survivors stay on controller / GUI / Autoload; disposable stages under container
    var container := GeneratedWorldContainer.new()
    container.name = "GeneratedWorld"
    for stage in build_pipeline_stages(seed):   # 2.1 DAG
        container.add_child(stage)
    world_host.swap_generated_child(container)
    # Do NOT delete SceneTree.root; avoid setting current_scene alone
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

## Acceptance criteria (execution — stub→playable ladder)

- [x] Parallel spine note exists under `Roadmap/Execution/Phase-2-…/` (not flat heap)
- [x] `conceptual_counterpart` links frozen conceptual Phase-2 primary
- [x] Pseudo-code + interfaces for WorldShell host / regenerate semantics
- [x] Godot stable verbatim citations in Research integration
- [ ] Secondary execution mirrors 2.1 / 2.2 / 2.3 minted
- [ ] Tertiary stage notes with edge-case ACs
- [ ] Catalog `execution_pins` coverage audited green for package row
- [ ] `execution_factory_handoff_ready` / fast-mode ready (multi-phase — later)

## Junior acceptance / verify (weave)

- [ ] **Given** seat context allowed for `ux_world_generation`, **When** junior implements `Genesis.World.WorldShellController`, **Then** wrong-seat calls return unauthorized / emit blocked — never silent OK
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_world_generation` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** terrain via `ITerrainAuthority` (Terrain3D); Gaea = parallel-maps path only

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

## Subphase next (execution DFS)

1. Mint **2.1** execution secondary under `Execution/Phase-2-…/Phase-2-1-Generation-Pipeline-Stages/` (parallel spine).
2. Then 2.2 Canon/Intent, 2.3 ToneProfile wires.
3. Re-run pin audit / handoff readiness toward `execution_factory_handoff_ready`.

## Status

`deepen_complete: true` for Phase-2 **primary** execution mint. `harness_material_change_required: satisfied`. Next: RESUME_ROADMAP deepen → Phase-2-1 generation pipeline stages (execution).

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
