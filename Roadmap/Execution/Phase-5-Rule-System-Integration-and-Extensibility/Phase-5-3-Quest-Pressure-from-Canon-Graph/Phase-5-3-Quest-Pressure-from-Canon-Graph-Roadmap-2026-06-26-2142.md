---
title: Phase 5.3 — Quest Pressure from Canon Graph (Execution)
roadmap-level: secondary
phase-number: 5
subphase-index: "5.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-3-Quest-Pressure-from-Canon-Graph/Phase-5-3-Quest-Pressure-from-Canon-Graph-Roadmap-2026-06-26-2142]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_living_world_continuity
priority: high
progress: 60
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
- quest-pressure
- canon-graph
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-3-Quest-Pressure-from-Canon-Graph/Phase-5-3-Quest-Pressure-from-Canon-Graph-Roadmap-2026-06-26-2142]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata/Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 5.3 — Quest Pressure from Canon Graph (Execution)

Execution secondary: **QuestPressureManifest** + **QuestPressureRegistry** + **CanonGraphPressureIndex** + **QuestPressureRulePlugin**. Urgency from **CanonRegistry** graph via **RuleEngineCore** → **RuleEffectBus** `quest_pressure`. Composes with 5.2 under **RuleConflictArbiter** (bands 200–299; default `defer_to_spell`). Parallel spine under `Execution/Phase-5-…/Phase-5-3-…/`. **No Half B.** L5/SERIES advisory — quest pressure from canon graph is DM-retconnable hinting; players do not author canon. **No 5.3.x twin invent.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Quest pressure from canon graph ([[conceptual 5.3]]) |
| Inspiration / L5 bar (advisory) | Canon-graph pressure hints; DM retconnable; players observe pressure not author canon |
| Inspiration (studied) | (1) Conceptual 5.3. (2) Execution 5.1 EffectBus/Arbiter. (3) 2.2 CanonRegistry / IntentResolver. (4) 3.1 SimTick / WorldEventLog RO |
| L5 / package crosswalk | phase-aligned `[[ux_living_world_continuity]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + secondary pseudo for index → signals → IntentResolver hints |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 5.3 |
| `dispatch_scope` | Execution secondary **5.3** mint (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| — | _(no conceptual tertiaries under 5.3)_ | n/a |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Quest.QuestPressureFromCanon` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_canon_pipeline_feel` | `CanonGraphPressureIndex` → QuestPressureSignal | direct WorldState mutate → reject | pressure hint |
| intent only | IntentResolver consumes signals | quest leaf ≠ faction/NPC writer | IntentEnvelope hint |
| weather/agenda | **not owned** | pressure ≠ weather/agenda module | — |
| plugin | QuestPressureRulePlugin | unbound → Unavailable | signal batch |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-intent-lore-loop` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Quest.QuestPressureFromCanon` |
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Quest.QuestPressureFromCanon` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Quest.QuestPressureFromCanon` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility | Owner |
|--------|----------------|-------|
| `QuestPressureManifest` | Declared pressure rules + bands | 5.3 |
| `QuestPressureRegistry` | quest_thread_id → pressure state | 5.3 |
| `CanonGraphPressureIndex` | Index CanonRegistry → urgency signals | 5.3 |
| `QuestPressureSignal` | thread_urgency / entity_stake / location_tension / hook_decay | 5.3 |
| `QuestPressureRulePlugin` | RulesetPlugin band 200–299 | 5.3 |

## Interfaces

```text
QuestPressureSignal (RefCounted):
  + kind: StringName   # thread_urgency | entity_stake | location_tension | hook_decay
  + subject_id: StringName
  + magnitude: float
  + tick: int
  + to_dict() -> Dictionary

CanonGraphPressureIndex (RefCounted):
  + rebuild(canon: CanonRegistry) -> Error
  + signals_for(thread_id: StringName) -> Array  # of QuestPressureSignal
  + snapshot() -> Dictionary

QuestPressureRegistry (RefCounted):
  + upsert(thread_id: StringName, pressure: Dictionary) -> Error
  + get(thread_id: StringName) -> Dictionary
  + decay_tick(tick: int) -> Error

QuestPressureManifest (RefCounted):
  + thread_id: StringName
  + predicates: Array   # pressure_above | thread_decay_is
  + priority: int       # within quest band 200–299
  + to_dict() -> Dictionary

QuestPressureRulePlugin (RefCounted):  # RulesetPlugin
  + collect(trigger: StringName, ctx: RuleContextFrame) -> Array
  + apply_effect(payload: Dictionary, intent: IntentResolver) -> Error
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# Seats: quest pressure from canon graph only — refuse invent 5.3.x twins.
# Players do not author world: pressure emits hints/effects; players do not invent canon.
# DM rail vs player FP: DM retcon may clear/redirect pressure; FP observes.
# Agency: pressure never grants dominate WorldState author without P4 path.
# ===========================================================

# 5.3 — Quest pressure from canon graph secondary (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; RuleEffectBus quest_pressure.
# Reject: quest journal UI; CanonRegistry mutation from pressure plugin;
#         WorldState direct writes; overriding spell band without Arbiter.

class_name QuestPressureRulePlugin
extends RefCounted

var _index: CanonGraphPressureIndex
var _registry: QuestPressureRegistry
var _intent: IntentResolver
var _canon: CanonRegistry

func on_sim_tick(tick: int) -> Error:
	var err := _index.rebuild(_canon)
	if err != OK:
		return err
	return _registry.decay_tick(tick)

func collect(trigger: StringName, ctx: RuleContextFrame) -> Array:
	if trigger != &"quest_pressure_eval" and trigger != &"sim.tick_committed":
		return []
	var out: Array = []
	var snap: Dictionary = ctx.quest_pressure_snapshot
	for thread_id in snap.keys():
		var m := QuestPressureManifest.new()
		m.thread_id = thread_id
		m.priority = int(snap[thread_id].get("priority", 0))
		m.predicates = snap[thread_id].get("predicates", [])
		var rule := RulePrimitive.new()
		rule.rule_id = StringName("quest." + str(thread_id))
		rule.band = 200
		rule.priority = m.priority
		rule.trigger = trigger
		rule.effect_set = [{
			"id": &"quest_pressure",
			"payload": {
				"thread_id": thread_id,
				"signals": _index.signals_for(thread_id),
				"manifest": m.to_dict()
			}
		}]
		out.append(rule)
	return out

func apply_effect(payload: Dictionary) -> Error:
	# IntentResolver hints only — never WorldStateCommitter.write
	var hints := {
		"kind": &"quest_pressure",
		"thread_id": payload.get("thread_id"),
		"signals": payload.get("signals", [])
	}
	return _intent.enqueue_hint(hints)

# Band 200–299; RuleConflictArbiter default defer_to_spell vs 5.2.
# Phase 6 may consume QuestPressureRegistry for presentation — not this note.

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-intent-lore-loop, stack-rules-engine, engine-godot-463-dotnet | Catalog: ux_living_world_continuity | Type: Genesis.Quest.QuestPressureFromCanon

// JUNIOR WORK-ORDER (ux_living_world_continuity): implement `Genesis.Quest.QuestPressureFromCanon` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Quest;
// Index B4 — quest pressure → IntentResolver hints only; never direct WorldState mutate
public interface IQuestPressureFromCanon {
    Error ResolveHints(CanonGraphSnapshot graph, SeatContext seat);
    // Must-fail: observe-only / player world-write → Unauthorized; WorldState mutate → reject
}

```

## Invariants

| ID | Rule |
|----|------|
| I-5.3-001 | CanonGraphPressureIndex is read-only over CanonRegistry |
| I-5.3-002 | Quest pressure emits IntentResolver hints only — no WorldStateCommitter writes |
| I-5.3-003 | Priority band 200–299; conflicts with spell band defer_to_spell by default |
| I-5.3-004 | No quest journal / factory L5 in this secondary |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine `Execution/Phase-5-…/Phase-5-3-…/`
- [x] Path-qualified conceptual counterpart
- [x] Module map + interfaces + secondary pseudo
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `QuestPressureFromCanon.ResolveHints` never mutates WorldState; observe-only seat → Unauthorized — row `ux_living_world_continuity`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** QuestPressureSignal path, **When** direct WorldState mutate, **Then** reject — IntentResolver hints only
- [ ] **Given** unbound QuestPressureRulePlugin, **When** emit, **Then** Unavailable

## Subphase next

1. Execution tree complete on disk for this node.
2. Batch validate / residual IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8`.


## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **Phase-6 primary**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
