---
title: Phase 5.1.3 — RuleConflictArbiter / RuleEffectBus (Roll-up)
roadmap-level: rollup
phase-number: 5
subphase-index: 5.1.3
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags:
- roadmap
- rollup
- genesis-mythos-master
- phase-5
- rule-conflict-arbiter
- rule-effect-bus
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roll-up-2026-07-15]]'
- '[[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 5.1.3 roll-up — RuleConflictArbiter / RuleEffectBus

Canonical compact tertiary: [[Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]. Detail preserved off the ≤1200 body (`followup-deepen-gmm-5-1-3-20260717T050633Z` recompact 1353→1196).

## Purpose

Name the **conflict resolution and effect routing surface** — Arbiter resolves same-frame conflicts; EffectBus delivers surviving effects to Phase 3/4/2.2 subsystems. Closes the **5.1 tertiary branch** under `phase_5_tertiary_tree`.

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **RuleConflictArbiter** | Veto → priority → merge → overflow for conflicting effects on the same target/frame |
| **RuleEffectBus** | Routes resolved effect classes to subsystem queues (async-by-default) |
| **`rule_conflict_max_active`** | Conceptual overflow constant; execution track sets numeric value |

**Out:** RuleEngineCore / RulePrimitive / RuleContextFrame (`5.1.1`); RulesetPlugin / PluginHookManifest / PluginLoader (`5.1.2`); 5.2 spell metadata; 5.3 quest pressure; DM runtime priority stack (OQ-5.1-003); factory/L5; execution pins.

## Behavior detail

### RuleConflictArbiter — resolution order

1. **Veto pass** — any plugin with `veto_classes` containing the effect class may veto; first veto wins; log `veto_reason` + `plugin_id` to WorldEventLog.
2. **Priority chain** — non-vetoed effects ordered by Manifest `priority` (lower = higher precedence); single-target conflicts (e.g. one `modify_agency` per entity per frame) keep the winner.
3. **Merge** — commutative effects (e.g. multiple `append_canon_fact` proposals) batch to IntentResolver lifecycle gate.
4. **Overflow guard** — when remaining count > `rule_conflict_max_active`, log `arbiter_overflow` and keep top-N by priority.

### RuleEffectBus — channels

| Effect class | Route | Subsystem |
|---|---|---|
| `world_delta` | Direct write path | WorldStateCommitter (3.1); DMPauseGate may hold during DM pause |
| `world_event` | Append to tick log | WorldEventLog (3.1) |
| `agency_transition` | Request queue | AgencyEnvelope (4.3) + AgencyTransitionGuardExtension |
| `perspective_transition` | Request queue | PerspectiveEnvelope (4.1); ModeTransitionGraph guards (4.2) |
| `canon_proposal` | Intent lifecycle | IntentResolver (2.2) → CanonRegistry |
| `tone_bias` | Adapter signal | ToneProfileConsequenceWeights (3.1) |

Dispatch is **asynchronous-by-default** (posted to per-subsystem queues). Ordering within a tick phase is deterministic by priority; across phases follows SimTickPipeline (3.1).

## Edge cases

- **Conflicting effects same entity/frame:** veto → priority → merge; overflow guard.
- **Plugin vetoes core effect:** allowed; audit trail via WorldEventLog.
- **DM pause:** `world_delta` held; other channels proceed.
- **Spell vs quest priority bands:** spell 100–199 / quest 200–299 declared by 5.2/5.3 plugins — Arbiter consumes Manifest priority only (this tertiary owns the algorithm, not band tables).

## Open questions

- **OQ-5.1-003** (static vs DM-adjustable priority) — static Manifest priority locked for 5.1; DM override deferred to 5.3 / extensibility seam.
- **OQ-5.1-001** (DSL format) — behaviour-first; serialization execution-deferred (parent rollup).

## Handoff criteria

- [x] RuleConflictArbiter / RuleEffectBus nouns named
- [x] Resolution order + channel table stated
- [x] Overflow + DMPauseGate behavior stated
- [x] 5.1.1 / 5.1.2 ownership boundaries clear
- [x] **5.1 tertiary branch closed** (5.1.1–5.1.3)
- [x] Next DFS **5.2.1** SpellAgencyPerspectiveManifest / SpellMetadataRegistry

**80%** handoff_readiness — implementer can place arbiter/bus ownership without guessing plugin load or evaluator loop. Slice green ≤1200; project harness RED next Phase-4-3-3 body_over_cap:1224>1200 (Phase-4 tertiary re-drift).
