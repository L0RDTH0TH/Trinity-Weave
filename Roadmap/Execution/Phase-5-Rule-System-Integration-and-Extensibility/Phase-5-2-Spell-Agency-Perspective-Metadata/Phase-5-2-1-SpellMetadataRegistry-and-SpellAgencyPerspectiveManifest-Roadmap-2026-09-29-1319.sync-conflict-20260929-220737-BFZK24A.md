---
title: Phase 5.2.1 — SpellMetadataRegistry / SpellAgencyPerspectiveManifest (Execution)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.2.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata/Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_combat_play_surface
invented_tertiary: true
invented_reason: no_conceptual_tertiary_twin_pins_parent_5_2
priority: high
progress: 55
handoff_readiness: 72
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
- spell-metadata-registry
- spell-agency-manifest
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_combat_play_surface/L5]]'
- '[[ux_combat_play_surface]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata/Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata/Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/PF1-Ruleset-Content-Scaffold]]'
weave_pass: exec-weave-stack-ux-20260929
ruleset_lock: pathfinder_pf1
---
# Phase 5.2.1 — SpellMetadataRegistry / SpellAgencyPerspectiveManifest (Execution)

Execution tertiary (invented — **no conceptual tertiary twin**; pins parent conceptual **5.2**): **SpellMetadataRegistry** + **SpellAgencyPerspectiveManifest** + thin **SpellRulesetPlugin** collect path (band 100–199). Dominate/overlay/liminal bindings → later 5.2.x. Parallel spine under `Execution/Phase-5-…/Phase-5-2-…/`. **No Half B.** L5/SERIES advisory — SpellMetadataRegistry + perspective manifest bind seats. **No 5.2.2+ invent.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Spell metadata registry + manifest ([[conceptual 5.2]]) |
| Inspiration / L5 bar (advisory) | Registry lookup; manifest seats; refuse illegal perspective cast; DM retconnable metadata |
| Inspiration (studied) | (1) Conceptual 5.2. (2) Execution 5.2 secondary. (3) 5.1.2 RulesetPlugin. (4) 5.1.3 EffectBus |
| L5 / package crosswalk | phase-aligned `[[ux_combat_play_surface]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted registry + manifest; plugin collect → RulePrimitive candidates |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_combat_play_surface` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_combat_play_surface/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 5.2 (parent — no tertiary twin) |
| `dispatch_scope` | Execution tertiary **5.2.1** invent mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_combat_play_surface` |
| Label | Combat/rules resolve by authored paths including non-win ends |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Rules.SpellMetadataRegistry` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | win-only ends; SRD 5.1 / D&D first-plugin lock (superseded); AGPL dice libs |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |
| `ruleset_lock` | **pathfinder_pf1** (CDR `rules-base-pathfinder-pf1-2026-09-29`) — host ruleset-agnostic; first plugin = PF1; **not** SRD 5.1 / D&D |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `rule_check` / spell resolve | SpellMetadataRegistry lookup | CanonRegistry write forbidden | overlay tags |
| passenger FP overlay | SpellAgencyPerspectiveManifest | victim-only; no dominate invent | PerspectiveEnvelope retarget |
| agency handoff | PilotHandoff release path (4.3) | missing release → reject | agency residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.SpellMetadataRegistry` |
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.SpellMetadataRegistry` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.SpellMetadataRegistry` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SpellAgencyPerspectiveManifest` | Declared agency_ops + overlay + liminal + priority |
| `SpellMetadataRegistry` | spell_id → manifest; apply_to_frame |
| `SpellRulesetPlugin` | RulesetPlugin collect for spell_cast / spell_release |

## Interfaces

```text
SpellAgencyPerspectiveManifest (RefCounted):
  + spell_id: StringName
  + agency_ops: Array
  + overlay: StringName
  + liminal: bool
  + priority: int
  + to_dict() -> Dictionary

SpellMetadataRegistry (RefCounted):
  + register(m: SpellAgencyPerspectiveManifest) -> Error
  + lookup(spell_id: StringName) -> SpellAgencyPerspectiveManifest
  + apply_to_frame(spell_id: StringName, ctx: RuleContextFrame) -> Error

SpellRulesetPlugin (RefCounted):  # implements RulesetPlugin
  + collect(trigger: StringName, ctx: RuleContextFrame) -> Array
  + manifest() -> PluginHookManifest
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_combat_play_surface L5 — advisory) ===
# Seats: manifest rows only — refuse invent 5.2.2+ spell twin notes.
# Players do not author world: registry is RO metadata, not WorldState writer.
# DM rail vs player FP: each spell row declares FP vs DM-rail eligibility.
# Agency: agency column must align with P4 envelopes — no silent escalate.
# ===========================================================

# 5.2.1 — SpellMetadataRegistry / Manifest / SpellRulesetPlugin collect (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName.
# Reject: Dominate/PilotHandoff apply (later 5.2.x); CanonRegistry writes;
#         passenger_fp on caster; quest band ownership (5.3).

class_name SpellMetadataRegistry
extends RefCounted

var _by_id: Dictionary = {}

func register(m: SpellAgencyPerspectiveManifest) -> Error:
	if m.spell_id == &"":
		return ERR_INVALID_PARAMETER
	_by_id[m.spell_id] = m
	return OK

func lookup(spell_id: StringName) -> SpellAgencyPerspectiveManifest:
	return _by_id.get(spell_id, null)

func apply_to_frame(spell_id: StringName, ctx: RuleContextFrame) -> Error:
	var m := lookup(spell_id)
	if m == null:
		return ERR_DOES_NOT_EXIST
	ctx.spell_metadata = m.to_dict()
	return OK

class_name SpellRulesetPlugin
extends RefCounted

var _registry: SpellMetadataRegistry

func collect(trigger: StringName, ctx: RuleContextFrame) -> Array:
	if trigger != &"spell_cast" and trigger != &"spell_release":
		return []
	var spell_id: StringName = ctx.spell_metadata.get("spell_id", &"")
	var m := _registry.lookup(spell_id)
	if m == null:
		return []
	var rule := RulePrimitive.new()
	rule.rule_id = StringName("spell." + str(spell_id))
	rule.band = 100
	rule.priority = m.priority
	rule.trigger = trigger
	rule.effect_set = [{"id": &"modify_agency", "payload": m.to_dict()}]
	return [rule]

# === WEAVE C# / .NET (Godot 4.6.3) — IRulesPluginHost + DiceRoller + PF1 ===
# Manifest: stack-rules-engine, stack-perspective-camera, engine-godot-463-dotnet | Catalog: ux_combat_play_surface

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
| I-5.2.1-001 | SpellRulesetPlugin never writes CanonRegistry |
| I-5.2.1-002 | Band clamped 100–199 for spell collect |
| I-5.2.1-003 | Missing registry entry → empty candidates (no Error spam) |
| I-5.2.1-004 | Dominate/overlay apply deferred to later 5.2.x bindings |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-5-2 folder
- [x] `conceptual_counterpart` → parent conceptual 5.2 (invented tertiary)
- [x] Interfaces + tertiary pseudo for registry/manifest/plugin collect
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `SpellMetadataRegistry` bind/evaluate/roll refuse paths emit Unauthorized/Unavailable (never silent OK); Roll→IDiceRoller when applicable — row `ux_combat_play_surface`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** CanonRegistry write from spell registry, **When** attempted, **Then** reject
- [ ] **Given** unknown spell, **When** lookup, **Then** DoesNotExist
- [ ] **Verify** demo/plugin binder uses **PF1** (`pathfinder_pf1`); no SRD 5.1 / 5e-bits first-plugin lock
- [ ] **Verify** rolls go through `IDiceRoller` / `IRulesPluginHost.Roll` (DiceRoller MIT) — not AGPL dice libs

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **5.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
