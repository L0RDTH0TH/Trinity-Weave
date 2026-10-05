---
title: Phase 5 — Rule System Integration and Extensibility (Execution)
roadmap-level: primary
phase-number: 5
subphase-index: "5"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
status: active
deepen_complete: phase5_tree_complete
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
created: 2026-09-28
updated: 2026-09-29
tags:
- paint_ux_catalog
- pkg_world_shell
- roadmap
- genesis-mythos-master
- phase-5
- rule-system
- extensibility
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_combat_play_surface/L5]]'
- '[[ux_combat_play_surface]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Conceptual-Decision-Records/rules-base-pathfinder-pf1-2026-09-29]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
weave_pass: exec-weave-stack-ux-20260929
ruleset_lock: pathfinder_pf1
---
# Phase 5 — Rule System Integration and Extensibility (Execution)

Execution primary enrich (FAST map-gen): rule engine + plugins, spell agency/perspective metadata, quest pressure from canon graph. Parallel spine under `Execution/Phase-5-Rule-System-Integration-and-Extensibility/`. **No Half B.** L5/SERIES are **read-only advisory feedstock** — rule engine + plugins enable seat-legal spell/quest pressure without players authoring the world. **Do not invent 5.2.2+ / 5.3.x twins.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Open rule engine + spell/quest plugins ([[conceptual Phase 5]]) |
| Inspiration / L5 bar (advisory) | Open rule engine seats; plugins refuse illegal agency; DM retcon vs player FP; quest pressure RO hints |
| Inspiration (studied) | (1) Conceptual Phase 5 + 5.1–5.3. (2) Execution 4.3 AgencyEnvelope / PilotHandoff. (3) Execution 1.3 SeamRegistry `rule`. (4) Execution 2.2 CanonRegistry / IntentResolver |
| L5 / package crosswalk | phase-aligned `[[ux_combat_play_surface]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + primary pseudo for RuleEngineCore evaluate → Arbiter → EffectBus |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_combat_play_surface` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_combat_play_surface/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual Phase 5 + 5.1–5.3 |
| `dispatch_scope` | Execution primary **Phase 5** + secondaries **5.1–5.3** (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 5.1 | Rule Engine Primitives and Plugin Hooks | **minted** (+ 5.1.1–5.1.3) |
| 5.2 | Spell Agency / Perspective Metadata | **minted** (+ invented 5.2.1; 5.2.2+ skipped no twin) |
| 5.3 | Quest Pressure from Canon Graph | **minted** (no conceptual tertiaries) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_combat_play_surface` |
| Label | Combat/rules resolve by authored paths including non-win ends |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Rules.IRulesPluginHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | win-only ends; SRD 5.1 / D&D first-plugin lock (superseded); AGPL dice libs |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |
| `ruleset_lock` | **pathfinder_pf1** (CDR `rules-base-pathfinder-pf1-2026-09-29`) — host ruleset-agnostic; first plugin = PF1; **not** SRD 5.1 / D&D |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `rule_check` | `IRulesPluginHost.Evaluate` / RuleEngineCore | wrong seat / unpublished `rules.plugin.core` | CheckResult + audit |
| `pf1_plugin` | `BindPlugin(pathfinder_pf1)` | SRD/5e first-plugin refuse | ActiveRuleset id |
| `dice_behind_host` | `IDiceRoller` via `IRulesPluginHost.Roll` | AGPL dice libs forbidden | DiceAudit |
| `non_win_ends` | RuleEffectBus → IntentResolver / agency | observe-only cannot WorldState-write | structured outcome enum |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-rules-engine` | `IRulesPluginHost` + `IDiceRoller` → DiceRoller NuGet | [[Docs/Junior-Tech-Adapt-How-To]] §3–4 · `Genesis.Rules.IRulesPluginHost` |
| `stack-character-creation` | `ICharacterCreationHost` (PF1 remint F3) | [[Docs/Junior-Tech-Adapt-How-To]] §4 · deepen existing; no 5.2.2+ invent |
| `engine-godot-463-dotnet` | Godot 4.6.3 .NET / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility | Owner secondary |
|--------|----------------|-----------------|
| `RuleEngineCore` | Load/evaluate RulePrimitive sets | 5.1 |
| `RulePrimitive` | condition_set / effect_set / trigger | 5.1 |
| `RulesetPlugin` / `PluginLoader` | Hot-load plugin manifests | 5.1 |
| `RuleConflictArbiter` | veto → priority → merge → overflow | 5.1 |
| `RuleEffectBus` | Route effects to 3.x / 4.x / IntentResolver | 5.1 |
| `RuleContextFrame` | Per-eval context + spell/quest snapshots | 5.1 |
| `SpellMetadataRegistry` | Dominate / passenger overlay / liminal | 5.2 |
| `DominateSpellBinding` | Spell → AgencyEnvelope / PilotHandoff | 5.2 |
| `QuestPressureRegistry` | Urgency signals from canon graph | 5.3 |
| `CanonGraphPressureIndex` | Index CanonRegistry edges → pressure | 5.3 |
| `QuestPressureRulePlugin` | RulesetPlugin for bands 200–299 | 5.3 |

## Interfaces

```text
# Imports (RO consumers)
SeamRegistry (RefCounted)              # 1.3 seam "rule"
CanonRegistry (RefCounted)             # 2.2
IntentResolver (RefCounted)            # 2.2
AgencyEnvelope (RefCounted)            # 4.3
PerspectiveEnvelope (RefCounted)       # 4.1
PilotHandoffCoordinator (RefCounted)   # 4.3
AgencyPersistenceLedger (RefCounted)   # 4.3
WorldStateCommitter (RefCounted)       # 3.1 RO
DMPauseGate (RefCounted)               # 3.1 / 3.3 RO

enum RuleBand { CORE=0, SPELL=100, QUEST=200, COMMUNITY=300 }

RulePrimitive (RefCounted):
  + rule_id: StringName
  + band: int
  + priority: int
  + condition_set: Array
  + effect_set: Array
  + trigger: StringName

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
  + evaluate(trigger: StringName, ctx: RuleContextFrame) -> Array  # candidates only — Core never applies
  signals: ruleset_changed(plugin_id), evaluation_started(trigger), evaluation_complete(result)

RuleConflictArbiter (RefCounted):
  + resolve(candidates: Array, ctx: RuleContextFrame) -> Array
  # order: veto → priority within band → merge → overflow drop

RuleEffectBus (RefCounted):
  + subscribe(effect_id: StringName, cb: Callable) -> Error
  + emit_effect(effect_id: StringName, payload: Dictionary) -> Error
  + enqueue_channel(channel: StringName, payload: Dictionary) -> Error
  signals: effect_emitted(effect_id, payload)
  # routes: modify_agency | passenger_fp_overlay | quest_pressure | intent_hint
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_combat_play_surface L5 — advisory) ===
# Seats: plugins refuse illegal perspective/agency edges — never invent 5.2.2+ twins.
# Players do not author world: rule effects route via bus; no silent WorldState mutate.
# DM rail vs player FP: spell/quest metadata distinguish observe vs author seats.
# Agency: arbiter + AgencyEnvelope (P4) bound dominate/observe — never invent classes.
# ===========================================================

# Phase 5 primary — Rule system spine (Godot 4 stable).
# Citations: RefCounted policies; Error/OK; StringName; signals; Presentation Node consumers.
# Reject: Autoload RuleEngine as Simulation authority; typed C# DSL here; factory/L5;
#         spell writes CanonRegistry; quest UI journal (exec-deferred).

class_name RuleEngineCore
extends RefCounted

signal ruleset_changed(plugin_id)
signal evaluation_started(trigger)
signal evaluation_complete(result)

var _collectors: Array = []            # RefCounted plugin collectors (5.1.1)
var _arbiter: RuleConflictArbiter      # owned at 5.1.3 — caller applies after resolve
var _bus: RuleEffectBus
var _seams: SeamRegistry

func register_collector(plugin: RefCounted) -> Error:
	if plugin == null:
		return ERR_INVALID_PARAMETER
	var mid: StringName = plugin.manifest_id() if plugin.has_method("manifest_id") else &"anon"
	if _seams != null and not _seams.allows(&"rule", mid):
		return ERR_UNAUTHORIZED
	_collectors.append(plugin)
	ruleset_changed.emit(mid)
	return OK

func evaluate(trigger: StringName, ctx: RuleContextFrame) -> Array:
	# Core returns candidates only — Arbiter/Bus apply at 5.1.3 / caller
	evaluation_started.emit(trigger)
	var candidates: Array = []
	for plug in _collectors:
		candidates.append_array(plug.collect(trigger, ctx))
	evaluation_complete.emit({"ok": true, "candidates": candidates})
	return candidates

# Ordering: 5.1 engine/arbiter/bus → 5.2 spell metadata → 5.3 quest pressure.
# Bands: spell 100–199 before quest 200–299; default defer_to_spell on conflict.

# === WEAVE C# / .NET (Godot 4.6.3) — IRulesPluginHost + DiceRoller + PF1 ===
# Manifest: stack-rules-engine, stack-character-creation, engine-godot-463-dotnet | Catalog: ux_combat_play_surface
# JUNIOR-MANDATORY adapt recipes: [[Docs/Junior-Tech-Adapt-How-To]] §3–4 (DiceRoller D, PF1 remint E–F)

# PF1: RulesetPluginId = "pathfinder_pf1"
# Content remint path (F1–F5): inventory SRD/5e strings → res://rules/pathfinder_pf1/ →
#   ICharacterCreationHost + 6.2.5 binder + Exemplar pack_defaults — deepen 5.1/5.2/5.2.1; no 5.2.2+ invent.
# Host remains ruleset-agnostic — do NOT hardcode SRD 5.1 / D&D strings as first plugin.

namespace Genesis.Rules;

public interface IDiceRoller {
    // NuGet DiceRoller (skizzerz MIT) behind this port; pin PRNG from ISeedAuthority channel `rules`
    RollResult Roll(DiceExpression expr, RuleContextFrame frame);
    DiceAudit RollExpression(string expression, ulong rulesSubSeed);
}

public interface IRulesPluginHost {
    Error BindPlugin(RulesetPluginId id); // SeamRegistry rules.plugin.core must authorize
    System.Collections.Generic.IReadOnlyList<RuleCandidate> Evaluate(RuleContextFrame frame);
    RollResult Roll(DiceExpression expr, RuleContextFrame frame); // MUST delegate → IDiceRoller
    RulesetPluginId ActiveRuleset { get; }
}

public sealed class RuleEngineCore : IRulesPluginHost {
    // JUNIOR WORK-ORDER (ux_combat_play_surface): pf1_plugin + rule_check
    // ACCEPT: default BindPlugin = pathfinder_pf1 (NOT srd_5_1)
    // ACCEPT: observe-only frame cannot WorldState-write
    // VERIFY: Roll → IDiceRoller (skizzerz/DiceRoller MIT); no AGPL dice host
    // VERIFY: content tables under res://rules/pathfinder_pf1/ (remint F2) — posture alone ≠ content
    private readonly IDiceRoller _dice;
    private RulesetPluginId _active = new("pathfinder_pf1");
    public RulesetPluginId ActiveRuleset => _active;
    public RuleEngineCore(IDiceRoller dice) => _dice = dice;
    public Error BindPlugin(RulesetPluginId id) {
        if (id.Value.Length == 0) return Error.InvalidParameter;
        // Refuse mid-session without ReGen queue + seam assert (Phase 3.3 / 1.3)
        _active = id;
        return Error.Ok;
    }
    public System.Collections.Generic.IReadOnlyList<RuleCandidate> Evaluate(RuleContextFrame frame) {
        if (frame.ObserveOnly && frame.RequestsWorldWrite) return System.Array.Empty<RuleCandidate>();
        // Load candidates from active PF1 plugin tables (post-remint)
        return System.Array.Empty<RuleCandidate>();
    }
    public RollResult Roll(DiceExpression expr, RuleContextFrame frame) => _dice.Roll(expr, frame);
}

```

## Invariants

| ID | Rule |
|----|------|
| I-5-001 | RuleEngineCore is RefCounted under SessionComposer — never Autoload Simulation root |
| I-5-002 | SeamRegistry `rule` must authorize plugin load / mid-session swap |
| I-5-003 | RuleConflictArbiter applies band order: spell (100–199) before quest (200–299) |
| I-5-004 | Spell effects may retarget AgencyEnvelope / PerspectiveEnvelope only — no CanonRegistry writes |
| I-5-005 | Quest pressure routes via IntentResolver hints only — no direct WorldState mutation |
| I-5-006 | passenger_fp_overlay is victim-only; never invent dominate without PilotHandoff release path |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine path `Execution/Phase-5-…/` (primary)
- [x] Path-qualified `conceptual_counterpart` → frozen Phase 5
- [x] Module map + child index for 5.1 / 5.2 / 5.3
- [x] Interfaces + primary pseudo for RuleEngineCore
- [x] Secondary **5.1** Rule Engine (+ tertiaries **5.1.1–5.1.3**)
- [x] Secondary **5.2** Spell Agency Metadata
- [x] Secondary **5.3** Quest Pressure
- [x] Tertiaries **5.1.1–5.1.3** + invented **5.2.1**; **5.2.2+** skipped (no twin)
- [ ] Half B / playable ladder later
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `IRulesPluginHost` bind/evaluate/roll refuse paths emit Unauthorized/Unavailable (never silent OK); Roll→IDiceRoller when applicable — row `ux_combat_play_surface`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** rules.plugin.core unpublished, **When** IRulesPluginHost.BindPlugin, **Then** Unavailable
- [ ] **Given** empty dice expression, **When** IDiceRoller.RollExpression, **Then** InvalidParameter — never silent Ok
- [ ] **Verify** demo/plugin binder uses **PF1** (`pathfinder_pf1`); no SRD 5.1 / 5e-bits first-plugin lock
- [ ] **Verify** rolls go through `IDiceRoller` / `IRulesPluginHost.Roll` (DiceRoller MIT) — not AGPL dice libs
- [ ] **Verify** content remint path F1–F5 started: inventory SRD/5e strings → `res://rules/pathfinder_pf1/` (deepen 5.1/5.2/5.2.1; **no 5.2.2+ invent**) — see [[Docs/Junior-Tech-Adapt-How-To]] §4

## PF1 content remint path (deepen existing — Gap 5)

Prefer deepen Phase-5 / 5.1 / 5.2 / 5.2.1 over inventing tertiaries. Normative steps (from how-to §4):

| Step | Action | Status |
|------|--------|--------|
| F1 | Inventory Execution Phase-5 notes + any `res://` tables still naming SRD/5e/D&D | posture woven; content inventory **pending Half B** |
| F2 | Remint PF1 tables under `res://rules/pathfinder_pf1/` | **vault scaffold thick** — [[Docs/PF1-Ruleset-Content-Scaffold]] (abilities/skills/conditions + **BAB/saves L1–20** + **spell-slot matrices L1–5** + spell-list scaffold + check_schema/demo); game-repo file mint still Half B |
| F3 | `ICharacterCreationHost` consumes reminted pack | deepen existing character-creation spine — no 5.2.2+ |
| F4 | 6.2.5 RuleCheckProbe binder uses `pathfinder_pf1` / `demo_ruleset_pf1` check schema | demo binder language **present** |
| F5 | Exemplar 6.4 `pack_defaults.ruleset_id` → same plugin id | **present** in Gap 2 assembly map |

CDR: [[Conceptual-Decision-Records/rules-base-pathfinder-pf1-2026-09-29]]. Host stays ruleset-agnostic. How-To ↔ Index: [[Docs/Junior-Tech-Adapt-How-To]] §4 · [[Docs/SeamRegistry-CSharp-Host-Index]] §B4.

## Research integration

- Presentation/SessionComposer ownership; WorldShell regen does not Autoload rule authority.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]
- [[Docs/Junior-Tech-Adapt-How-To]] · [[Docs/SeamRegistry-CSharp-Host-Index]]

## Subphase next

1. Execution tree complete on disk for this node.
2. Batch validate / residual IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8`.


## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **5.1**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
