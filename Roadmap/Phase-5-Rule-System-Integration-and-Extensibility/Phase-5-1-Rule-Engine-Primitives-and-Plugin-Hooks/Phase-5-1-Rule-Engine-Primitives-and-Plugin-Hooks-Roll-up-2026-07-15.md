---
title: Phase 5.1 — Rule Engine Primitives and Plugin Hooks (Roll-up)
roadmap-level: rollup
phase-number: 5
subphase-index: '5.1'
project-id: genesis-mythos-master
status: complete
priority: high
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-5
- rule-engine
- plugin-hooks
- rollup
para-type: Project
roadmap_track: conceptual
rollup_of: '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
links:
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
body_compact_source_queue: followup-deepen-phase51-20260715T232300Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 5.1 — Roll-up detail (factory feed-gate compact)

Canonical NL detail preserved from secondary body compact 2026-07-15 (queue followup-deepen-phase51-20260715T232300Z). Secondary keeps nouns + scope; this note holds tables, plugin contract, edge cases, open questions, tasks, dataview.

## Phase 5.1 — Rule Engine Primitives and Plugin Hooks

Core rule engine architecture: primitive evaluator, plugin hook contract, conflict arbiter, effect routing bus. Spells and quest-pressure metadata are downstream consumers (5.2, 5.3); this slice owns the base seam.

## Scope

**In scope:** **RuleEngineCore** (condition-effect evaluation loop); **RulePrimitive** library (atomic conditions and effects); **RulesetPlugin** contract (how rulesets register as plugins); **PluginHookManifest** (declarative hook descriptor); **PluginLoader** (session-init and session-boundary loading); **RuleConflictArbiter** (priority-chain, veto, merge resolution); **RuleContextFrame** (per-evaluation snapshot: actor, scene, canon state); **RuleEffectBus** (routes rule effects to Phase 3/4 subsystems); integration with Phase 1.3 **SeamRegistry** `rule` seam family.

**Out of scope:** Spell-specific agency and perspective metadata declarations (Phase 5.2); quest pressure integration from canon graph (Phase 5.3); execution-track typed interfaces, rollup HR gates, and Godot C# implementation (execution-deferred / advisory on conceptual track); campaign tone profile bias tables for individual spell effects (Phase 2.3 consumes ToneProfileBundle; Phase 5.2 wires spell-bound ToneProfile hooks).

## Behavior

### Rule representation

A rule is a triple: `{condition_set, effect_set, trigger}`.

- **Condition set** — one or more **RulePrimitive** conditions evaluated against a **RuleContextFrame**; all must hold for the rule to fire (AND semantics default; OR operator explicit).
- **Effect set** — one or more **RulePrimitive** effects dispatched via **RuleEffectBus** when conditions pass.
- **Trigger** — the event class that causes the engine to evaluate this rule (e.g. `intent_submitted`, `tick_phase_end`, `canon_fact_accepted`, `mode_transition_complete`).

### RulePrimitive library

**Condition atoms:**

| Primitive ID | Signature (NL) | Notes |
|---|---|---|
| `actor_has_tag` | Actor entity carries a semantic tag | Evaluates against **UnifiedSceneGraph** (4.1) entity node |
| `state_is` | Named world-state key equals value | Reads from **WorldStateCommitter** snapshot (3.1) |
| `canon_has` | CanonRegistry contains fact matching predicate | Read-only via **CanonRegistry** (2.2) |
| `agency_class_is` | Actor's current agency class matches enum | Reads **AgencyEnvelope** (4.3) |
| `perspective_mode_is` | Actor's current perspective mode matches | Reads **PerspectiveEnvelope** (4.1) |
| `tone_weight_above` | ToneProfile weight key exceeds threshold | Reads **ToneProfileBundle** weight map (2.3) |

**Effect atoms:**

| Primitive ID | Signature (NL) | Target subsystem |
|---|---|---|
| `apply_delta` | Emit a **WorldState** delta for committed write | **WorldStateCommitter** (3.1) via **RuleEffectBus** |
| `trigger_event` | Post a **WorldEventLog** event entry | **WorldEventLog** (3.1) via **RuleEffectBus** |
| `modify_agency` | Request agency class transition for entity | **AgencyEnvelope** (4.3) via **RuleEffectBus** |
| `override_perspective` | Request perspective mode switch for entity | **PerspectiveEnvelope** (4.1) via **RuleEffectBus** |
| `append_canon_fact` | Propose a new **CanonFact** (requires arbiter pass) | **IntentResolver** (2.2) lifecycle gate |
| `tone_bias_signal` | Emit tone-bias signal to **ToneProfileBundle** adapter | Consumer: ToneProfileConsequenceWeights (3.1) |

### RuleContextFrame

Assembled per rule evaluation:

| Field | Source |
|---|---|
| `actor_entity_id` | Triggering entity from **UnifiedSceneGraph** (4.1) |
| `scene_context` | Active scene identifier + scene-local state flags (from **UnifiedSceneGraph** 4.1 scene root) |
| `trigger_class` | Enum from triggering event |
| `world_state_snapshot` | Read-only copy from **WorldStateCommitter** (3.1) |
| `canon_read_handle` | Read-only **CanonRegistry** handle (2.2) |
| `agency_envelope_snapshot` | Current **AgencyEnvelope** state (4.3) |
| `perspective_envelope_snapshot` | Current **PerspectiveEnvelope** state (4.1) |
| `tone_weights` | **ToneProfileBundle** weight map (2.3) |
| `active_plugin_ids` | Sorted list of loaded ruleset plugin IDs |

Nil actor context (e.g. global tick trigger without an actor): `actor_entity_id = null`; evaluation proceeds with `actor_has_tag`, `agency_class_is`, `perspective_mode_is` returning false — **no exception thrown**, rule quietly skips actor-dependent conditions.

### RulesetPlugin contract

A plugin is a bounded ruleset module:

```
RulesetPlugin:
  plugin_id: string       # globally unique, lowercase-kebab
  version: semver
  declare_hooks() → PluginHookManifest
  on_load(context: PluginLoadContext) → Result
  on_unload() → Result
```

**PluginHookManifest** declares:

```
PluginHookManifest:
  rules: []Rule            # full rule triples (condition_set, effect_set, trigger)
  priority: int            # arbiter priority; lower = higher precedence
  veto_classes: []string   # effect classes this plugin may veto
  required_condition_atoms: []string   # atoms this plugin extends (seam contract)
  required_effect_atoms: []string      # atoms this plugin uses
  tone_bias_subscriptions: []string    # ToneProfile weight keys consulted
```

### PluginLoader

- Loads all plugins registered in the **SeamRegistry** `rule` seam family at session init.
- Validates each plugin's `required_condition_atoms` and `required_effect_atoms` against the registered **RulePrimitive** library; rejects plugins declaring unknown atoms with a logged `plugin_load_error` in **WorldEventLog**.
- Plugin load order: sort by `priority` ascending (lower number first); ties broken by `plugin_id` lexicographic order (deterministic).
- **Session-boundary hot-swap policy:** New plugins take effect at session boundary (session start or explicit reload event); mid-session plugin installs are queued to the **ReGenerationIntentQueue** (3.3) as `structural_re_gen` class — no live mid-session swap without operator intent.

### RuleConflictArbiter

Resolves when multiple rules fire on the same trigger and produce conflicting effects on the same target.

**Resolution order:**

1. **Veto pass** — any plugin with `veto_classes` containing the effect class may veto it; first veto wins; veto logged in **WorldEventLog** with `veto_reason`.
2. **Priority chain** — non-vetoed effects ordered by plugin `priority`; lowest priority number wins for single-target conflicts (one `modify_agency` effect per entity per frame).
3. **Merge** — commutative effects (e.g. multiple `append_canon_fact` proposals) are merged into a batch submitted to **IntentResolver** lifecycle gate.
4. **Overflow guard** — when more than `rule_conflict_max_active` (conceptual constant, execution track sets value) effects remain after veto+priority, log `arbiter_overflow` to **WorldEventLog** and apply only top-N by priority.

### RuleEffectBus

Routes resolved effects to target subsystems:

| Effect class | Route | Subsystem |
|---|---|---|
| `world_delta` | Direct write path | **WorldStateCommitter** (3.1) |
| `world_event` | Append to tick log | **WorldEventLog** (3.1) |
| `agency_transition` | Request queue | **AgencyEnvelope** (4.3); gated by **AgencyTransitionGuardExtension** |
| `perspective_transition` | Request queue | **PerspectiveEnvelope** (4.1); gated by **ModeTransitionGraph** guard stack (4.2) |
| `canon_proposal` | Intent lifecycle gate | **IntentResolver** (2.2) → **CanonRegistry** |
| `tone_bias` | Adapter signal | **ToneProfileConsequenceWeights** (3.1) |

All dispatches are **asynchronous-by-default** (posted to per-subsystem queues, not inline calls) — ordering within a tick phase is deterministic by priority; across tick phases follows SimTickPipeline schedule (3.1). **DMPauseGate** (3.1) may hold world_delta effects during DM pause; other effect classes proceed.

## Interfaces

**Imports from prior phases:**

| Phase export | How 5.1 consumes it |
|---|---|
| **SeamRegistry** rule family (1.3) | Plugin registration seam; all plugins register hook manifests here |
| **CanonRegistry** + **CanonFact** lifecycle (2.2) | Read handle in **RuleContextFrame**; `append_canon_fact` effect routes through **IntentResolver** |
| **ToneProfileBundle** weights (2.3) | `tone_weight_above` condition atom + `tone_bias` effect class |
| **SimTickPipeline** + **WorldStateCommitter** (3.1) | Trigger point `tick_phase_end`; `world_delta` + `world_event` effect routing |
| **DMPauseGate** (3.1) | Holds `world_delta` dispatches during DM pause |
| **ReGenerationIntentQueue** (3.3) | Session-boundary plugin swap entry point |
| **PerspectiveEnvelope** + **CameraInterpolatorRegistry** (4.1) | `perspective_transition` effect target; guard integration |
| **AgencyEnvelope** + **AgencyTransitionGuardExtension** (4.3) | `agency_transition` effect target; guard integration |
| **ModeTransitionGraph** guard stack (4.2) | Gates `perspective_transition` effects |

> **Note (OQ-5.1-005):** `actor_has_tag` condition assumes **UnifiedSceneGraph** (4.1) exposes a tag-query seam. Phase 4.1 does not explicitly declare this in its export table. This seam is conceptually implied by the entity-node model but should be confirmed at Phase 4.1 tertiary or execution-track wiring. Flagged as advisory; does not block Phase 5.1 conceptual completion.

**Exports to downstream phases:**

| Export | Consumer |
|---|---|
| **RuleEngineCore** evaluation loop | Phase 5.2: spell-bound conditions and effects registered via plugin |
| **RuleEffectBus** `agency_transition` channel | Phase 5.2: spell-bound dominate → dominator pilot_fp (PilotGraph via **AgencyEnvelope** 4.3); victim `passenger_fp_overlay` hook (reserved in **AgencyEnvelope** 4.3 — not a legal **PerspectiveEnvelope** 4.1 mode); liminal presentation policy declared by spell metadata (5.2) |
| **RuleContextFrame** schema | Phase 5.2: `spell_metadata` field added to frame when spell trigger fires |
| **SeamRegistry** rule family (via plugin contracts) | Phase 5.3: quest-pressure plugin hooks into same seam |
| **RuleConflictArbiter** priority table | Phase 5.2, 5.3: spell effects and quest effects declare plugin priority and veto classes |

## Edge Cases

| Case | Handling |
|---|---|
| Circular rule chain (rule A triggers rule B triggers rule A) | **RuleEngineCore** cycle detector: per-frame seen-set on `rule_id`; on cycle detection log `rule_cycle_detected` to **WorldEventLog**, abort chain — do not fire second occurrence |
| Plugin load order conflict (two plugins declare same `rule_id`) | **PluginLoader** rejects second registration with `duplicate_rule_id` error; first-registered wins (by load order / priority) |
| Nil actor context on actor-dependent condition | Condition returns `false`; evaluation continues; rule body does not fire; no exception |
| Conflicting effects on same entity in same frame | **RuleConflictArbiter** veto → priority → merge; `arbiter_overflow` guard for runaway chains |
| Plugin vetoes core engine effect | Allowed by design (veto in PluginHookManifest); veto logged in **WorldEventLog** with `plugin_id` + `veto_reason` for DM workbench audit trail |
| Session-boundary plugin swap race (new plugin arrives mid-evaluation batch) | **PluginLoader** defers new registrations to next session boundary; mid-batch snapshot is immutable |

## Open Questions

| ID | Question | Conceptual authority decision |
|---|---|---|
| OQ-5.1-001 | Rule DSL format: declarative JSON/YAML manifest vs C# attribute-decorated DSL? | **Behaviour-first**: conceptual contract specifies data-driven condition/effect/trigger triples; execution track chooses DSL/serialization format; both are valid implementations under this secondary |
| OQ-5.1-002 | Plugin hot-swap feasibility during active session (not just session boundary)? | **Session-boundary policy locked** conceptually; emergency patch path exists via **OverwritePatchLayer** (3.3) for structural-class changes; further nuance deferred to execution track |
| OQ-5.1-003 | Arbiter priority table: static per-plugin declaration vs runtime priority stack adjustable by DM? | **Static by default**: plugins declare `priority` in **PluginHookManifest**; DM override API is out of scope for 5.1 conceptual — flagged for Phase 5.3 / extensibility seam |
| OQ-5.1-004 | `tone_weight_above` condition reads static seed weights from **ToneProfileBundle** (2.3); `tone_bias_signal` effect writes to dynamic per-tick **ToneProfileConsequenceWeights** (3.1). Intentional asymmetry or gap requiring read/write alignment? | **Asymmetry intentional by design**: conditions are evaluated against the stable session-seed profile (session-level invariant); effects feed per-tick dynamic weights (run-time). The two are distinct layers in Phase 2.3 vs Phase 3.1 contract. Confirm at execution track — no blocker on conceptual. |

## Consistency Reports

> [!note]
> Post-mint: execution rollup gates, REGISTRY-CI, and HR closure artifacts are execution-deferred / advisory on conceptual track per conceptual_v1 contract.

Minted 2026-06-26 (godo-followup-20260626T204500Z-phase5-deepen-5-1); Phase 5 breadth closed 2026-06-26 advance-phase godo-followup-20260626T221100Z-phase5-advance; persona: half_a.conceptual_architect; product_factory_run_id: f35ff65cfb4f; pre_create_gate: skipped_conceptual_track; execution_gaps_advisory: true.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

