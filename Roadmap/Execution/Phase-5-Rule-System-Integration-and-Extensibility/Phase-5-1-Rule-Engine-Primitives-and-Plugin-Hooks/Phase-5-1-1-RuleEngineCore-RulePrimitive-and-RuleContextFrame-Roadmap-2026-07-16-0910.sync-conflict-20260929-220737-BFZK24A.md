---
title: Phase 5.1.1 — RuleEngineCore / RulePrimitive / RuleContextFrame (Execution)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
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
- rule-engine-core
- rule-primitive
- rule-context-frame
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_combat_play_surface/L5]]'
- '[[ux_combat_play_surface]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/PF1-Ruleset-Content-Scaffold]]'
weave_pass: exec-weave-stack-ux-20260929
ruleset_lock: pathfinder_pf1
---
# Phase 5.1.1 — RuleEngineCore / RulePrimitive / RuleContextFrame (Execution)

Execution tertiary: **RuleEngineCore** condition→effect loop + cycle detector; **RulePrimitive** atom library; **RuleContextFrame** per-eval snapshot. Plugins/arbiter/bus → **5.1.2–5.1.3**. Parallel spine under `Execution/Phase-5-…/Phase-5-1-…/`. **No Half B.** L5/SERIES advisory — RuleEngineCore + RuleContextFrame bind seats; observe frames do not author WorldState.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Core evaluate loop + primitives + frame ([[conceptual 5.1.1]]) |
| Inspiration / L5 bar (advisory) | Core evaluate; context frame seats; refuse world-author from observe frame |
| Inspiration (studied) | (1) Conceptual 5.1.1. (2) Execution 5.1 secondary. (3) SeamRegistry `rule` (1.3). (4) WorldState tick (3.1) |
| L5 / package crosswalk | phase-aligned `[[ux_combat_play_surface]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | C# / .NET (Godot 4.6.3) RefCounted Core + Primitive + Frame; evaluate returns candidates for Arbiter |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_combat_play_surface` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_combat_play_surface/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 5.1.1 |
| `dispatch_scope` | Execution tertiary **5.1.1** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_combat_play_surface` |
| Label | Combat/rules resolve by authored paths including non-win ends |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Rules.RuleEngineCore` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | win-only ends; SRD 5.1 / D&D first-plugin lock (superseded); AGPL dice libs |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |
| `ruleset_lock` | **pathfinder_pf1** (CDR `rules-base-pathfinder-pf1-2026-09-29`) — host ruleset-agnostic; first plugin = PF1; **not** SRD 5.1 / D&D |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `rule_check` | `RuleEngineCore.Evaluate` + RuleContextFrame | null frame → InvalidParameter | CheckResult |
| primitives | `RulePrimitive` apply | unknown primitive → DoesNotExist | primitive audit |
| seed channel | frame.RulesSubSeed | missing seed → Unconfigured | DiceAudit via host |
| plugin tables | **not owned** — loader leaf | core ≠ content remint writer | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.RuleEngineCore` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.RuleEngineCore` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `RuleEngineCore` | Session evaluate loop; cycle seen-set |
| `RulePrimitive` | `{rule_id, condition_set, effect_set, trigger, band, priority}` |
| `RuleContextFrame` | actor, scene, session, tick, canon, envelopes, tone, spell_metadata, quest_pressure_snapshot, active_plugin_ids, clone_shallow, to_dict |

## Interfaces

```text
RulePrimitive (RefCounted):
  + rule_id: StringName
  + trigger: StringName
  + band: int
  + priority: int
  + condition_set: Array
  + effect_set: Array
  + to_dict() -> Dictionary

RuleContextFrame (RefCounted):
  + actor_id: StringName
  + scene_id: StringName
  + session_id: StringName
  + tick: int
  + canon_snapshot: Dictionary
  + agency: RefCounted
  + perspective: RefCounted
  + tone: Dictionary
  + spell_metadata: Dictionary
  + quest_pressure_snapshot: Dictionary
  + active_plugin_ids: Array
  + clone_shallow() -> RuleContextFrame
  + to_dict() -> Dictionary

RuleEngineCore (RefCounted):
  + register_collector(plugin: RefCounted) -> Error
  + evaluate(trigger: StringName, ctx: RuleContextFrame) -> Array  # RulePrimitive candidates
  + last_cycle_abort() -> StringName
  signals: evaluation_started(trigger), evaluation_complete(result)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_combat_play_surface L5 — advisory) ===
# Seats: RuleContextFrame must carry legal perspective — refuse invent seats.
# Players do not author world: observe-frame evaluations emit RO effects only.
# DM rail vs player FP: frame pins distinguish FP vs DM rail evaluation context.
# Agency: never invent ACTIVE_DOMINATE in frame without P4 handoff path.
# ===========================================================

# 5.1.1 — RuleEngineCore / RulePrimitive / RuleContextFrame (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
# Reject: Autoload global rule table; silent cycle; evaluating without frame;
#         Arbiter/Bus ownership (5.1.3); PluginLoader (5.1.2).

class_name RuleEngineCore
extends RefCounted

signal evaluation_started(trigger)
signal evaluation_complete(result)

var _collectors: Array = []
var _last_cycle: StringName = &""

func evaluate(trigger: StringName, ctx: RuleContextFrame) -> Array:
	evaluation_started.emit(trigger)
	if ctx.actor_id == &"" and not _allow_nil_actor(trigger):
		evaluation_complete.emit({"ok": true, "skipped": true, "candidates": []})
		return []
	var seen: Dictionary = {}
	var candidates: Array = []
	for plugin in _collectors:
		var batch: Array = plugin.collect(trigger, ctx)
		for r in batch:
			var rid: StringName = r.rule_id
			if seen.has(rid):
				_last_cycle = rid
				evaluation_complete.emit({"ok": false, "cycle": rid, "candidates": []})
				return []
			seen[rid] = true
			if not _conditions_pass(r.condition_set, ctx):
				continue
			candidates.append(r)
	evaluation_complete.emit({"ok": true, "candidates": candidates})
	return candidates

func _conditions_pass(conds: Array, ctx: RuleContextFrame) -> bool:
	for c in conds:
		if not _eval_atom(c, ctx):
			return false
	return true

func last_cycle_abort() -> StringName:
	return _last_cycle

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
| I-5.1.1-001 | Cycle detector aborts on duplicate `rule_id` in one evaluate |
| I-5.1.1-002 | Nil-actor triggers quiet-skip unless allowlisted |
| I-5.1.1-003 | Core never applies effects — returns candidates only |
| I-5.1.1-004 | Frame clone is shallow; mutating frame mid-eval is #review-needed |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-5-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 5.1.1
- [x] Interfaces + tertiary pseudo for Core/Primitive/Frame
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `RuleEngineCore` bind/evaluate/roll refuse paths emit Unauthorized/Unavailable (never silent OK); Roll→IDiceRoller when applicable — row `ux_combat_play_surface`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** null RuleContextFrame, **When** RuleEngineCore.Evaluate, **Then** InvalidParameter
- [ ] **Given** missing RulesSubSeed, **When** contested path, **Then** Unconfigured
- [ ] **Verify** demo/plugin binder uses **PF1** (`pathfinder_pf1`); no SRD 5.1 / 5e-bits first-plugin lock
- [ ] **Verify** rolls go through `IDiceRoller` / `IRulesPluginHost.Roll` (DiceRoller MIT) — not AGPL dice libs

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **5.1.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
