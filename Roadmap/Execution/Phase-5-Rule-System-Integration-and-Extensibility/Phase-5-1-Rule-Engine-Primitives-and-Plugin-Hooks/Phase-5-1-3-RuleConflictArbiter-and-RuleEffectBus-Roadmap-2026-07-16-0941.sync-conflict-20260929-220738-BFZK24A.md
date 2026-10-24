---
title: Phase 5.1.3 — RuleConflictArbiter / RuleEffectBus (Execution)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]'
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
- rule-conflict-arbiter
- rule-effect-bus
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_combat_play_surface/L5]]'
- '[[ux_combat_play_surface]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/PF1-Ruleset-Content-Scaffold]]'
weave_pass: exec-weave-stack-ux-20260929
ruleset_lock: pathfinder_pf1
---
# Phase 5.1.3 — RuleConflictArbiter / RuleEffectBus (Execution)

Execution tertiary: **RuleConflictArbiter** (hard_veto → band → priority → merge → overflow); **RuleEffectBus** fan-out to sim / agency / perspective / canon / tone channels. Parallel spine under `Execution/Phase-5-…/Phase-5-1-…/`. **No Half B.** L5/SERIES advisory — arbiter + effect bus refuse silent illegal conflicts; players do not author via effect invent.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Conflict policy + effect routing ([[conceptual 5.1.3]]) |
| Inspiration / L5 bar (advisory) | First-failing conflict policy; effect bus non-silent; DM retcon vs player FP routing |
| Inspiration (studied) | (1) Conceptual 5.1.3. (2) Execution 5.1.1/5.1.2. (3) DMPauseGate (3.1). (4) envelopes 4.1/4.3 |
| L5 / package crosswalk | phase-aligned `[[ux_combat_play_surface]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted Arbiter + Bus; signals for Presentation RO adapters |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_combat_play_surface` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_combat_play_surface/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 5.1.3 |
| `dispatch_scope` | Execution tertiary **5.1.3** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_combat_play_surface` |
| Label | Combat/rules resolve by authored paths including non-win ends |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Rules.RuleConflictArbiter` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | win-only ends; SRD 5.1 / D&D first-plugin lock (superseded); AGPL dice libs |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |
| `ruleset_lock` | **pathfinder_pf1** (CDR `rules-base-pathfinder-pf1-2026-09-29`) — host ruleset-agnostic; first plugin = PF1; **not** SRD 5.1 / D&D |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| conflict | `RuleConflictArbiter.Arbitrate` | overflow → ArbiterOverflowRecord | winner effect |
| `non_win_ends` | `RuleEffectBus.Emit` | silent drop forbidden | effect row |
| observe-only | bus must not WorldState-write | observe write → reject | — |
| dice | **not owned** — IDiceRoller | arbiter ≠ roller | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.RuleConflictArbiter` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.RuleConflictArbiter` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `RuleConflictArbiter` | Resolve candidate RulePrimitives |
| `RuleEffectBus` | subscribe / emit_effect + channel queues |
| `ArbiterOverflowRecord` | top-N dropped candidates for audit |

## Interfaces

```text
RuleConflictArbiter (RefCounted):
  + merge_budget: int  # default 32
  + resolve(candidates: Array, ctx: RuleContextFrame) -> Array
  + last_overflow() -> Array

RuleEffectBus (RefCounted):
  + subscribe(effect_id: StringName, cb: Callable) -> Error
  + emit_effect(effect_id: StringName, payload: Dictionary) -> Error
  + enqueue_channel(channel: StringName, payload: Dictionary) -> Error
  signals: effect_emitted(effect_id, payload)
# channels: world_delta | world_event | agency_transition |
#           perspective_transition | canon_proposal | tone_bias
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_combat_play_surface L5 — advisory) ===
# Seats: first-failing arbiter — never silent-pass illegal conflicts.
# Players do not author world: bus refuses invent WorldState from observe effects.
# DM rail vs player FP: effect channels split FP vs DM rail presentation.
# Agency: effect agency tags cannot escalate to dominate without P4 path.
# ===========================================================

# 5.1.3 — RuleConflictArbiter / RuleEffectBus (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
# Reject: silent overflow; Autoload Simulation mutators on Bus; Core ownership (5.1.1);
#         PluginLoader (5.1.2); spell/quest domain logic (5.2/5.3).

class_name RuleConflictArbiter
extends RefCounted

var merge_budget: int = 32
var _overflow: Array = []

func resolve(candidates: Array, ctx: RuleContextFrame) -> Array:
	_overflow.clear()
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
	for r in surviving:
		if out.size() >= merge_budget:
			_overflow.append(r)
			continue
		if _can_merge(r, out):
			_merge_into(r, out)
		else:
			out.append(r)
	return out

func last_overflow() -> Array:
	return _overflow.duplicate()

class_name RuleEffectBus
extends RefCounted

signal effect_emitted(effect_id, payload)

var _subs: Dictionary = {}
var _pause: RefCounted  # DMPauseGate

func emit_effect(effect_id: StringName, payload: Dictionary) -> Error:
	if effect_id == &"world_delta" and _pause != null and _pause.is_paused():
		return ERR_BUSY
	if _subs.has(effect_id):
		for cb in _subs[effect_id]:
			cb.call(payload)
	effect_emitted.emit(effect_id, payload)
	return OK

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
| I-5.1.3-001 | Overflow never silent — recorded in `last_overflow` / evaluation_complete |
| I-5.1.3-002 | `world_delta` respects DMPauseGate |
| I-5.1.3-003 | Bus subscribers are Presentation/Intent RO — no Autoload Simulation mutators |
| I-5.1.3-004 | Default spell-vs-quest conflict policy: `defer_to_spell` (advisory for 5.2/5.3) |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-5-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 5.1.3
- [x] Interfaces + tertiary pseudo for Arbiter/Bus
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `RuleConflictArbiter` bind/evaluate/roll refuse paths emit Unauthorized/Unavailable (never silent OK); Roll→IDiceRoller when applicable — row `ux_combat_play_surface`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** arbiter overflow, **When** Arbitrate, **Then** ArbiterOverflowRecord and no silent drop
- [ ] **Given** observe-only, **When** RuleEffectBus would WorldState-write, **Then** reject
- [ ] **Verify** demo/plugin binder uses **PF1** (`pathfinder_pf1`); no SRD 5.1 / 5e-bits first-plugin lock
- [ ] **Verify** rolls go through `IDiceRoller` / `IRulesPluginHost.Roll` (DiceRoller MIT) — not AGPL dice libs

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **5.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
