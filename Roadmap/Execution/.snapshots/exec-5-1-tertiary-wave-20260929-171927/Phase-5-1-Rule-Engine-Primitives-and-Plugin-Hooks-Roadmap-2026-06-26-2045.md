---
title: Phase 5.1 — Rule Engine Primitives and Plugin Hooks (Execution)
roadmap-level: secondary
phase-number: 5
subphase-index: "5.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
status: active
priority: high
progress: 55
handoff_readiness: 72
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-5
- rule-engine
- plugin-hooks
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
catalog_row_ids:
- ux_combat_play_surface
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
weave_pass: exec-weave-stack-ux-20260929
ruleset_lock: pathfinder_pf2e_orc
---
# Phase 5.1 — Rule Engine Primitives and Plugin Hooks (Execution)

Execution secondary: **RuleEngineCore** + **RulePrimitive** + **RulesetPlugin** / **PluginHookManifest** / **PluginLoader** + **RuleConflictArbiter** + **RuleContextFrame** + **RuleEffectBus**. Spells (5.2) / quest-pressure (5.3) register as plugins. Parallel spine under `Execution/Phase-5-…/Phase-5-1-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Rule primitives + plugin hooks ([[conceptual 5.1]]) |
| Inspiration (studied) | (1) Conceptual 5.1 + 5.1.1–5.1.3. (2) Execution Phase-5 primary. (3) 1.3 SeamRegistry. (4) 3.3 ReGenerationIntentQueue for mid-session swaps |
| L5 / package crosswalk | _(n/a — no L5)_ |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + secondary pseudo for load → collect → arbiter → bus |
| Validation signal | Secondary minted; tertiaries **5.1.1–5.1.3** next DFS; nested V/IRA batch-later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | _(advisory)_ |
| `package_id` | _(Phase-5 TBD)_ |
| `l5_path` | `Roadmap/User-Story/scopes/ux_combat_play_surface/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 5.1 + tertiaries 5.1.1–5.1.3 |
| `dispatch_scope` | Execution secondary **5.1** mint (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 5.1.1 | RuleEngineCore / RulePrimitive / RuleContextFrame | **pending** (next) |
| 5.1.2 | RulesetPlugin / PluginHookManifest / PluginLoader | **pending** |
| 5.1.3 | RuleConflictArbiter / RuleEffectBus | **pending** |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_combat_play_surface` |
| Label | Combat/rules resolve by authored paths including non-win ends |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Rules.IRulesPluginHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | win-only ends; SRD 5.1 / D&D first-plugin lock (superseded); AGPL dice libs |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |
| `ruleset_lock` | **pathfinder_pf2e_orc** (CDR `rules-base-pathfinder-pf2e-orc-2026-09-29`) — host ruleset-agnostic; first plugin = PF2e/ORC; **not** SRD 5.1 / D&D |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `rule_check` | `Genesis.Rules.IRulesPluginHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `pf2e_orc_plugin` | `Genesis.Rules.IRulesPluginHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `non_win_ends` | `Genesis.Rules.IRulesPluginHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `dice_behind_host` | `Genesis.Rules.IRulesPluginHost` / leaf modules | wrong seat / out of contract | lasting readable residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.IRulesPluginHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.IRulesPluginHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility | Owner tertiary |
|--------|----------------|----------------|
| `RuleEngineCore` | Session evaluate loop | 5.1.1 |
| `RulePrimitive` | Atomic rule record | 5.1.1 |
| `RuleContextFrame` | Eval context bag | 5.1.1 |
| `RulesetPlugin` | Plugin contract | 5.1.2 |
| `PluginHookManifest` | Declared hooks + bands | 5.1.2 |
| `PluginLoader` | Disk/resource load + seam check | 5.1.2 |
| `RuleConflictArbiter` | Conflict policy | 5.1.3 |
| `RuleEffectBus` | Effect fan-out | 5.1.3 |

## Interfaces

```text
PluginHookManifest (RefCounted):
  + plugin_id: StringName
  + hooks: Array          # trigger StringNames
  + band_min: int
  + band_max: int
  + to_dict() -> Dictionary

RulesetPlugin (RefCounted):
  + manifest_id() -> StringName
  + manifest() -> PluginHookManifest
  + collect(trigger: StringName, ctx: RuleContextFrame) -> Array  # of RulePrimitive
  + on_load(engine: RuleEngineCore) -> Error
  + on_unload() -> Error

PluginLoader (RefCounted):
  + load_from_path(path: String, seams: SeamRegistry) -> RulesetPlugin
  + validate_manifest(m: PluginHookManifest) -> Error

RuleConflictArbiter (RefCounted):
  + resolve(candidates: Array, ctx: RuleContextFrame) -> Array
  # stages: hard_veto → band_priority → within_band_priority → mergeable → overflow

RuleEffectBus (RefCounted):
  + subscribe(effect_id: StringName, cb: Callable) -> Error
  + emit_effect(effect_id: StringName, payload: Dictionary) -> Error
  signals: effect_emitted(effect_id, payload)
```

## Pseudo-code

```pseudo
# 5.1 — Rule engine / plugin hooks secondary (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals; Resource load.
# Reject: Autoload plugin table; mid-session swap without SeamRegistry + ReGen queue;
#         C# typed DSL; silent overflow (must record).

class_name RuleConflictArbiter
extends RefCounted

func resolve(candidates: Array, ctx: RuleContextFrame) -> Array:
	var surviving: Array = []
	for r in candidates:
		if _hard_veto(r, ctx):
			continue
		surviving.append(r)
	surviving.sort_custom(func(a, b):
		if a.band != b.band:
			return a.band < b.band
		return a.priority > b.priority
	)
	var out: Array = []
	var merge_budget: int = 32
	for r in surviving:
		if out.size() >= merge_budget:
			break
		if _can_merge(r, out):
			_merge_into(r, out)
		else:
			out.append(r)
	return out

# Ordering: 5.1.1 core/primitive/frame → 5.1.2 plugin/loader → 5.1.3 arbiter/bus.
# Mid-session swap: enqueue via Phase-3.3 ReGenerationIntentQueue; apply at safe tick.

# === WEAVE C# / .NET (Godot 4.6.3) — IRulesPluginHost + DiceRoller + PF2e/ORC ===
# Manifest: stack-rules-engine, engine-godot-463-dotnet | Catalog: ux_combat_play_surface

# PF2e/ORC: RulesetPluginId = "pathfinder_pf2e_orc"; content tables remint pending.
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
    // JUNIOR WORK-ORDER (ux_combat_play_surface): pf2e_orc_plugin + rule_check
    // ACCEPT: default BindPlugin = pathfinder_pf2e_orc (NOT srd_5_1)
    // ACCEPT: observe-only frame cannot WorldState-write
    // VERIFY: Roll → IDiceRoller (skizzerz/DiceRoller MIT); no AGPL dice host
    private readonly IDiceRoller _dice;
    private RulesetPluginId _active = new("pathfinder_pf2e_orc");
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
| I-5.1-001 | PluginLoader refuses load when SeamRegistry `rule` denies plugin_id |
| I-5.1-002 | Mid-session plugin swap only via ReGenerationIntentQueue (3.3) at safe tick |
| I-5.1-003 | Arbiter never drops overflow silently — record in evaluation_complete result |
| I-5.1-004 | RuleEffectBus subscribers are Presentation/Intent RO adapters — no Autoload Simulation mutators |

## Acceptance

- [x] Parallel spine `Execution/Phase-5-…/Phase-5-1-…/`
- [x] Path-qualified conceptual counterpart
- [x] Module map + tertiary index 5.1.1–5.1.3
- [x] Interfaces + secondary pseudo
- [ ] Tertiaries 5.1.1–5.1.3 minted
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Given** seat context allowed for `ux_combat_play_surface`, **When** junior implements `Genesis.Rules.IRulesPluginHost`, **Then** wrong-seat calls return unauthorized / emit blocked — never silent OK
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_combat_play_surface` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** demo/plugin binder uses **PF2e/ORC** (`pathfinder_pf2e_orc`); no SRD 5.1 / 5e-bits first-plugin lock
- [ ] **Verify** rolls go through `IDiceRoller` / `IRulesPluginHost.Roll` (DiceRoller MIT) — not AGPL dice libs

## Subphase next

1. Deepen **5.1.1** RuleEngineCore / RulePrimitive / RuleContextFrame.
2. Then 5.1.2 → 5.1.3; Phase-5 secondary wave otherwise closed.

## Status

`deepen_complete: true` for Execution **5.1** secondary (tertiaries pending). Nested V/IRA skipped (operator batch-later).

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
