---
title: Phase 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader (Execution)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
status: active
priority: high
progress: 55
handoff_readiness: 74
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-5
- ruleset-plugin
- plugin-hook-manifest
- plugin-loader
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader (Execution)

Execution tertiary: **RulesetPlugin** contract; **PluginHookManifest** hooks + bands; **PluginLoader** Resource/disk load + SeamRegistry gate. Mid-session swap via ReGen (3.3). Parallel spine under `Execution/Phase-5-…/Phase-5-1-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Plugin load + hook manifest ([[conceptual 5.1.2]]) |
| Inspiration (studied) | (1) Conceptual 5.1.2. (2) Execution 5.1.1 Core. (3) SeamRegistry `rule`. (4) ReGenerationIntentQueue (3.3) |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | RefCounted plugin + loader; `ResourceLoader` path; refuse on seam deny |
| Validation | Duplicate `rule_id` reject; mid-session only via ReGen safe tick |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 5.1.2 |
| `dispatch_scope` | Execution tertiary **5.1.2** mint (FAST DFS) |

## Module map

| Module | Responsibility |
|--------|----------------|
| `PluginHookManifest` | plugin_id, hooks, band_min/max |
| `RulesetPlugin` | lifecycle + `collect(trigger, ctx)` |
| `PluginLoader` | load_from_path + validate_manifest + seam check |

## Interfaces

```text
PluginHookManifest (RefCounted):
  + plugin_id: StringName
  + hooks: Array
  + band_min: int
  + band_max: int
  + to_dict() -> Dictionary

RulesetPlugin (RefCounted):
  + manifest_id() -> StringName
  + manifest() -> PluginHookManifest
  + collect(trigger: StringName, ctx: RuleContextFrame) -> Array
  + on_load(engine: RuleEngineCore) -> Error
  + on_unload() -> Error

PluginLoader (RefCounted):
  + load_from_path(path: String, seams: SeamRegistry) -> RulesetPlugin
  + validate_manifest(m: PluginHookManifest) -> Error
  + enqueue_mid_session_swap(plugin_id: StringName, path: String, queue: RefCounted) -> Error
```

## Pseudo-code

```pseudo
# 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; ResourceLoader.
# Reject: Autoload plugin table; mid-session swap without ReGen; silent seam deny;
#         Arbiter/Bus (5.1.3); Core ownership (5.1.1).

class_name PluginLoader
extends RefCounted

func load_from_path(path: String, seams: RefCounted) -> RefCounted:
	var m_res = ResourceLoader.load(path)
	if m_res == null:
		return null
	var plugin: RulesetPlugin = m_res as RulesetPlugin
	if plugin == null:
		push_error("PluginLoader: not RulesetPlugin at %s" % path)
		return null
	var m := plugin.manifest()
	if validate_manifest(m) != OK:
		return null
	if not seams.allows(&"rule", m.plugin_id):
		push_error("PluginLoader: SeamRegistry denied %s" % m.plugin_id)
		return null
	return plugin

func validate_manifest(m: PluginHookManifest) -> Error:
	if m.plugin_id == &"":
		return ERR_INVALID_PARAMETER
	if m.band_min > m.band_max:
		return ERR_INVALID_PARAMETER
	if m.hooks.is_empty():
		return ERR_INVALID_PARAMETER
	return OK

func enqueue_mid_session_swap(plugin_id: StringName, path: String, queue: RefCounted) -> Error:
	# ReGenerationIntentQueue (3.3) — apply at safe tick only.
	return queue.enqueue({
		"kind": &"plugin_swap",
		"plugin_id": plugin_id,
		"path": path
	})
```

## Invariants

| ID | Rule |
|----|------|
| I-5.1.2-001 | Loader refuses when SeamRegistry `rule` denies `plugin_id` |
| I-5.1.2-002 | Mid-session swap only via ReGenerationIntentQueue at safe tick |
| I-5.1.2-003 | Duplicate `rule_id` across loaded plugins → reject register |
| I-5.1.2-004 | Frame `active_plugin_ids` = sorted loaded IDs after successful load |

## Acceptance

- [x] Parallel spine under Phase-5-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 5.1.2
- [x] Interfaces + tertiary pseudo for Plugin/Loader
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
