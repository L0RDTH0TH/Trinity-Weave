---
title: Phase 6.2.5 — RuleCheckProbe Rule Check (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.5"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]'
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
- phase-6
- horizon-demo
- rule-check
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_combat_play_surface/L5]]'
- '[[ux_combat_play_surface]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/PF1-Ruleset-Content-Scaffold]]'
weave_pass: exec-weave-stack-ux-20260929
ruleset_lock: pathfinder_pf1
---
# Phase 6.2.5 — RuleCheckProbe Rule Check (Execution)

Execution tertiary: **RuleCheckProbe** (beat 5) — after `demo_sim_tick_committed` build a **RuleContextFrame** stub + **demo_ruleset_pf1**, run **one** RuleEngineCore pass → `rule_demo_pass` | `rule_demo_fail` → `demo_rule_check_complete`. Halt-on-fail default. Consumers: **6.2.6**, **6.2.8**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B.** L5/SERIES advisory — RuleCheckProbe proves seat-legal rule eval in demo.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Single demo rule eval after sim tick ([[conceptual 6.2.5]]) |
| Inspiration / L5 bar (advisory) | Demo rule probe; seats in RuleContextFrame; refuse illegal |
| Inspiration (studied) | (1) Conceptual 6.2.5. (2) Execution 6.2.4. (3) RuleEngineCore / RuleContextFrame / RuleEffectBus (5.1). (4) halt-on-fail policy |
| L5 / package crosswalk | phase-aligned `[[ux_combat_play_surface]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Stub Node; ≤1 eval; EffectBus pass/fail; session signal |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_combat_play_surface` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_combat_play_surface/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2.5 |
| `dispatch_scope` | Execution tertiary **6.2.5** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_combat_play_surface` |
| Label | Combat/rules resolve by authored paths including non-win ends |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.RuleCheckProbe` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | win-only ends; SRD 5.1 / D&D first-plugin lock (superseded); AGPL dice libs |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |
| `ruleset_lock` | **pathfinder_pf1** (CDR `rules-base-pathfinder-pf1-2026-09-29`) — host ruleset-agnostic; first plugin = PF1; **not** SRD 5.1 / D&D |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `rule_check` | `RuleCheckProbe` → IRulesPluginHost | unbound → Unavailable | CheckResult |
| `dice_behind_host` | host.Roll → IDiceRoller | UI direct roll → Unauthorized | DiceAudit |
| PF1 | ActiveRuleset pathfinder_pf1 | DemoRuleEngine **forbidden** | plugin id |
| empty expr | RollExpression | empty → InvalidParameter | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.RuleCheckProbe` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.RuleCheckProbe` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `RuleCheckProbe` | awaiting_context → frame_built → evaluating → pass \| fail \| blocked |
| `DemoRuleContextBuilder` | Stub RuleContextFrame from WorldEventLog row |
| `DemoRulesetBinder` | Bind demo_ruleset_pf1 (no PluginLoader) |
| `RuleEffectBusBridge` | Emit rule_demo_pass / rule_demo_fail |

## Interfaces

```text
RuleCheckProbe (Node):
  + arm_after_tick(event_id: StringName, log_row: Dictionary) -> Error
  + evaluate_once() -> Error
  + last_outcome() -> StringName
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: demo_rule_check_complete(outcome), rule_demo_pass(codes), rule_demo_fail(codes)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_combat_play_surface L5 — advisory) ===
# Seats: probe uses FP RuleContextFrame — refuse invent DM-author success.
# Players do not author world: probe effects are demo-bounded.
# DM rail vs player FP: DM cam transition is next beat (6.2.6).
# Agency: rule tags align with P5 — no silent dominate.
# ===========================================================

# 6.2.5 — RuleCheckProbe (Godot 4 stable).
# Citations: Node; Dictionary; StringName; Error/OK; signals.
# Reject: multi-eval loops; PluginLoader; RuleConflictArbiter; spell/quest
#         plugins; commit without sim_tick_committed; Half B/L5.

class_name RuleCheckProbe
extends Node

signal demo_rule_check_complete(outcome)
signal rule_demo_pass(codes)
signal rule_demo_fail(codes)

enum State { AWAITING_CONTEXT, FRAME_BUILT, EVALUATING, PASS, FAIL, BLOCKED }
var _state: State = State.AWAITING_CONTEXT
var _event_id: StringName = &""
var _frame: Dictionary = {}
var _outcome: StringName = &""
var _evals_done: int = 0

var _armed_event_id: StringName = &""
var _armed_log_row: Dictionary = {}

func run_beat() -> Error:
	var err := arm_after_tick(_armed_event_id, _armed_log_row)
	if err != OK:
		return err
	return evaluate_once()

func arm_after_tick(event_id: StringName, log_row: Dictionary) -> Error:
	if event_id == &"" or log_row.is_empty():
		_block(&"missing_tick_context")
		return ERR_INVALID_PARAMETER
	_event_id = event_id
	_frame = {"event_id": event_id, "log_row": log_row, "ruleset": &"demo_ruleset_pf1"}
	_state = State.FRAME_BUILT
	return OK

func evaluate_once() -> Error:
	if _state != State.FRAME_BUILT:
		_block(&"bad_state")
		return ERR_UNAVAILABLE
	if _evals_done >= 1:
		_block(&"eval_cap")
		return ERR_ALREADY_EXISTS
	_state = State.EVALUATING
	_evals_done = 1
	# GAP4: call real IRulesPluginHost.Evaluate / Roll → IDiceRoller (Phase 5.1) — demo binder only; no PluginLoader
	# var candidates = _rules_host.Evaluate(RuleContextFrame.from_dict(_frame))
	var passed: bool = true  # stand-in until Half B; types = Genesis.Rules.*
	if passed:
		_outcome = &"pass"
		_state = State.PASS
		rule_demo_pass.emit([&"demo_ok"])
	else:
		_outcome = &"fail"
		_state = State.FAIL
		rule_demo_fail.emit([&"demo_fail"])
	demo_rule_check_complete.emit(_outcome)
	return OK

func last_outcome() -> StringName:
	return _outcome

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	_outcome = code
	demo_rule_check_complete.emit(code)

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
| I-6.2.5-001 | arm_after_tick requires demo_sim_tick_committed payload |
| I-6.2.5-002 | At most one RuleEngineCore pass per armed tick |
| I-6.2.5-003 | Halt-on-fail: FAIL still emits demo_rule_check_complete |
| I-6.2.5-004 | No PluginLoader / Arbiter on demo path |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.5
- [x] Interfaces + tertiary pseudo for RuleCheckProbe
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `RuleCheckProbe` bind/evaluate/roll refuse paths emit Unauthorized/Unavailable (never silent OK); Roll→IDiceRoller when applicable — row `ux_combat_play_surface`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** unbound IRulesPluginHost, **When** RuleCheckProbe, **Then** Unavailable
- [ ] **Given** empty expression, **When** host.Roll / RollExpression, **Then** InvalidParameter
- [ ] **Verify** demo/plugin binder uses **PF1** (`pathfinder_pf1`); no SRD 5.1 / 5e-bits first-plugin lock
- [ ] **Verify** rolls go through `IDiceRoller` / `IRulesPluginHost.Roll` (DiceRoller MIT) — not AGPL dice libs

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.2.6**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
