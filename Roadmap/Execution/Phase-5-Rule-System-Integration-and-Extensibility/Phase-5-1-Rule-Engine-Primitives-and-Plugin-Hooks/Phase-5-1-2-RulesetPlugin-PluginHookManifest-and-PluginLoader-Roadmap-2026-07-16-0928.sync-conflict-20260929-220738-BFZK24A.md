---
title: Phase 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader (Execution)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_combat_play_surface
priority: high
progress: 55
handoff_readiness: 74
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- paint_ux_catalog
- pkg_world_shell
- roadmap
- genesis-mythos-master
- phase-5
- ruleset-plugin
- plugin-hook-manifest
- plugin-loader
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_combat_play_surface/L5]]'
- '[[ux_combat_play_surface]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/PF1-Ruleset-Content-Scaffold]]'
weave_pass: exec-weave-stack-ux-20260929
ruleset_lock: pathfinder_pf1
---
# Phase 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader (Execution)

Execution tertiary: **RulesetPlugin** contract; **PluginHookManifest** hooks + bands; **PluginLoader** Resource/disk load + SeamRegistry gate. Mid-session swap via ReGen (3.3). Parallel spine under `Execution/Phase-5-…/Phase-5-1-…/`. **No Half B.** L5/SERIES advisory — PluginLoader + manifest enable seat-legal hooks; undeclared side-effects refuse.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Plugin load + hook manifest ([[conceptual 5.1.2]]) |
| Inspiration / L5 bar (advisory) | Manifest-declared hooks only; refuse undeclared side-effects; seats in loader gate |
| Inspiration (studied) | (1) Conceptual 5.1.2. (2) Execution 5.1.1 Core. (3) SeamRegistry `rule`. (4) ReGenerationIntentQueue (3.3) |
| L5 / package crosswalk | phase-aligned `[[ux_combat_play_surface]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted plugin + loader; `ResourceLoader` path; refuse on seam deny |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_combat_play_surface` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_combat_play_surface/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 5.1.2 |
| `dispatch_scope` | Execution tertiary **5.1.2** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_combat_play_surface` |
| Label | Combat/rules resolve by authored paths including non-win ends |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Rules.RulesetPluginLoader` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | win-only ends; SRD 5.1 / D&D first-plugin lock (superseded); AGPL dice libs |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |
| `ruleset_lock` | **pathfinder_pf1** (CDR `rules-base-pathfinder-pf1-2026-09-29`) — host ruleset-agnostic; first plugin = PF1; **not** SRD 5.1 / D&D |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `pf1_plugin` | `PluginLoader.LoadFromPath` | seam unpublished → Unavailable | loaded plugin |
| hook manifest | `PluginHookManifest` | missing hooks → InvalidParameter | manifest id |
| mid-session swap | only via ReGen + seam assert | Autoload table swap → Unauthorized | swap receipt |
| dice | host Roll only | loader ≠ dice roller | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.RulesetPluginLoader` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.RulesetPluginLoader` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

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
JUNIOR WORK-ORDER (ux_combat_play_surface L5 — advisory) ===
# Seats: only manifest-declared hooks load — refuse invent undeclared hooks.
# Players do not author world: WorldState-writing hooks must be explicit + gated.
# DM rail vs player FP: loader tags hooks with perspective eligibility.
# Agency: plugin agency tags align with P4 AgencyEnvelope — no invent dominate.
# ===========================================================

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

# === WEAVE C# / .NET (Godot 4.6.3) — IRulesPluginHost + DiceRoller + PF1 ===
# Manifest: stack-rules-engine, engine-godot-463-dotnet | Catalog: ux_combat_play_surface

# PF1: RulesetPluginId = "pathfinder_pf1"; vault F2 resolved → [[Docs/PF1-Ruleset-Content-Scaffold]] (BAB/saves L1–20 + spell slots + spell-list scaffold).
# Game-repo res://rules/pathfinder_pf1/ mint = Half B (not this leaf).
# see Junior-Tech-Adapt-How-To §3–4 · SeamRegistry-CSharp-Host-Index §B4
# Host remains ruleset-agnostic — do NOT hardcode SRD 5.1 / D&D strings as first plugin.

namespace Genesis.Rules;

public interface IDiceRoller {
    RollResult Roll(DiceExpression expr, RuleContextFrame frame);
}

public interface IRulesPluginHost {
    Error BindPlugin(RulesetPluginId id);
    System.Collections.Generic.IReadOnlyList<RuleCandidate> Evaluate(RuleContextFrame frame);
    RollResult Roll(DiceExpression expr, RuleContextFrame frame);
}

public sealed class RuleEngineCore : IRulesPluginHost {
    // JUNIOR WORK-ORDER (ux_combat_play_surface): pf1_plugin + rule_check
    // ACCEPT: default BindPlugin = pathfinder_pf1 (NOT srd_5_1)
    // ACCEPT: observe-only frame cannot WorldState-write
    // VERIFY: Roll → IDiceRoller (skizzerz/DiceRoller MIT); no AGPL dice host
    private readonly IDiceRoller _dice;
    private RulesetPluginId _active = new("pathfinder_pf1");
    public RuleEngineCore(IDiceRoller dice) => _dice = dice;
    public Error BindPlugin(RulesetPluginId id) { _active = id; return Error.Ok; }
    public System.Collections.Generic.IReadOnlyList<RuleCandidate> Evaluate(RuleContextFrame frame)
        => System.Array.Empty<RuleCandidate>();
    public RollResult Roll(DiceExpression expr, RuleContextFrame frame) => _dice.Roll(expr, frame);
}

```

## Invariants

| ID | Rule |
|----|------|
| I-5.1.2-001 | Loader refuses when SeamRegistry `rule` denies `plugin_id` |
| I-5.1.2-002 | Mid-session swap only via ReGenerationIntentQueue at safe tick |
| I-5.1.2-003 | Duplicate `rule_id` across loaded plugins → reject register |
| I-5.1.2-004 | Frame `active_plugin_ids` = sorted loaded IDs after successful load |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-5-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 5.1.2
- [x] Interfaces + tertiary pseudo for Plugin/Loader
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `RulesetPluginLoader` bind/evaluate/roll refuse paths emit Unauthorized/Unavailable (never silent OK); Roll→IDiceRoller when applicable — row `ux_combat_play_surface`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** seam unpublished, **When** PluginLoader.LoadFromPath, **Then** Unavailable
- [ ] **Given** Autoload mid-session table swap, **When** attempted, **Then** Unauthorized — require ReGen + seam assert
- [ ] **Verify** demo/plugin binder uses **PF1** (`pathfinder_pf1`); no SRD 5.1 / 5e-bits first-plugin lock
- [ ] **Verify** rolls go through `IDiceRoller` / `IRulesPluginHost.Roll` (DiceRoller MIT) — not AGPL dice libs

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **5.1.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
