---
title: Phase 5.2.1 — SpellMetadataRegistry / SpellAgencyPerspectiveManifest (Execution)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.2.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata/Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
status: active
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
- roadmap
- genesis-mythos-master
- phase-5
- spell-metadata-registry
- spell-agency-manifest
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata/Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata/Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 5.2.1 — SpellMetadataRegistry / SpellAgencyPerspectiveManifest (Execution)

Execution tertiary (invented — **no conceptual tertiary twin**; pins parent conceptual **5.2**): **SpellMetadataRegistry** + **SpellAgencyPerspectiveManifest** + thin **SpellRulesetPlugin** collect path (band 100–199). Dominate/overlay/liminal bindings → later 5.2.x. Parallel spine under `Execution/Phase-5-…/Phase-5-2-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Spell metadata registry + manifest ([[conceptual 5.2]]) |
| Inspiration (studied) | (1) Conceptual 5.2. (2) Execution 5.2 secondary. (3) 5.1.2 RulesetPlugin. (4) 5.1.3 EffectBus |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | RefCounted registry + manifest; plugin collect → RulePrimitive candidates |
| Validation | Missing spell_id → empty collect; never writes CanonRegistry |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 5.2 (parent — no tertiary twin) |
| `dispatch_scope` | Execution tertiary **5.2.1** invent mint (FAST DFS) |

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
```

## Invariants

| ID | Rule |
|----|------|
| I-5.2.1-001 | SpellRulesetPlugin never writes CanonRegistry |
| I-5.2.1-002 | Band clamped 100–199 for spell collect |
| I-5.2.1-003 | Missing registry entry → empty candidates (no Error spam) |
| I-5.2.1-004 | Dominate/overlay apply deferred to later 5.2.x bindings |

## Acceptance

- [x] Parallel spine under Phase-5-2 folder
- [x] `conceptual_counterpart` → parent conceptual 5.2 (invented tertiary)
- [x] Interfaces + tertiary pseudo for registry/manifest/plugin collect
- [ ] Nested Validator batch-later

## Status

This node’s execution subtree is **complete on disk**. Batch validate/IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8` / `batched_validator_ira`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.
