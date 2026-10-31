---
title: Phase 5.1.1 — RuleEngineCore / RulePrimitive / RuleContextFrame (Roll-up)
roadmap-level: rollup
phase-number: 5
subphase-index: 5.1.1
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags:
- roadmap
- rollup
- genesis-mythos-master
- phase-5
- rule-engine-core
- rule-primitive
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roll-up-2026-07-15]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 5.1.1 roll-up — RuleEngineCore / RulePrimitive / RuleContextFrame

Canonical compact tertiary: [[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]. Detail preserved off the ≤1400 feedstock body (`followup-deepen-phase511-tertiary-20260716T130049Z`).

## Purpose

Name the **core evaluator nouns** — evaluation loop, atomic condition/effect library, and per-evaluation context snapshot — without owning plugin load, conflict arbitration, or effect routing (sibling tertiaries).

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **RuleEngineCore** | Condition→effect evaluation loop; per-frame `rule_id` cycle detector; quiet-skip on failed actor-dependent conditions |
| **RulePrimitive** | Atomic condition atoms (`actor_has_tag`, `state_is`, `canon_has`, `agency_class_is`, `perspective_mode_is`, `tone_weight_above`) + effect atoms (`apply_delta`, `trigger_event`, `modify_agency`, `override_perspective`, `append_canon_fact`, `tone_bias_signal`) |
| **RuleContextFrame** | Snapshot: `actor_entity_id`, `scene_context`, `trigger_class`, `world_state_snapshot`, `canon_read_handle`, agency/perspective envelopes, `tone_weights`, `active_plugin_ids` (forward field — **ownership: 5.1.2 PluginLoader**; 5.1.1 only names the import slot on the frame) |
| Rule triple | `{condition_set, effect_set, trigger}` — AND default; OR explicit |

**Out:** RulesetPlugin / PluginHookManifest / PluginLoader (`5.1.2`); RuleConflictArbiter / RuleEffectBus (`5.1.3`); 5.2 spell metadata; 5.3 quest pressure; typed DSL; factory/L5; execution pins.

**Ownership note:** `active_plugin_ids` is a **5.1.2-owned import** on RuleContextFrame — PluginLoader populates the sorted loaded-plugin list; this tertiary does not own load/validation semantics.

## Behavior detail

1. Trigger event selects candidate rules (registry ownership deferred to 5.1.2 PluginLoader).
2. Assemble **RuleContextFrame** from 2.x/3.x/4.x read handles.
3. Evaluate **RulePrimitive** conditions against the frame (nil actor → actor-dependent atoms false, no throw).
4. On pass, collect effect atoms; **RuleEngineCore** cycle seen-set aborts re-entry of same `rule_id` in-frame (`rule_cycle_detected` → WorldEventLog).
5. Resolved effect list handed to **RuleConflictArbiter** / **RuleEffectBus** (5.1.3) — this tertiary does not own dispatch.

## Edge cases

- **Nil actor on global tick:** frame `actor_entity_id = null`; actor-dependent conditions false; rule body does not fire.
- **Circular chain:** cycle detector aborts second occurrence; first effects may still proceed to arbiter.
- **Unknown primitive atom at evaluate time:** treat as failed condition / rejected effect — plugin validation ownership is 5.1.2; core must not invent atoms.

## Open questions

- **OQ-5.1-001** (DSL format) — behaviour-first contract here; serialization execution-deferred (parent rollup).
- **OQ-5.1-005** (`actor_has_tag` / UnifiedSceneGraph tag seam) — advisory; Phase 4.1.2 implies entity-node tags; confirm on execution track.

## Handoff criteria

- [x] RuleEngineCore / RulePrimitive / RuleContextFrame nouns named
- [x] Rule triple + AND/OR + cycle abort stated
- [x] Plugin/arbiter/bus deferred to 5.1.2–5.1.3
- [x] Exports pointed at 5.1.2 / 5.1.3 / 5.2
- [x] Next DFS **5.1.2** minted and cleared **1379→1197≤1200**; live next **5.1.3** `body_over_cap:1353>1200` RuleConflictArbiter / RuleEffectBus

**80%** handoff_readiness — implementer can place evaluator ownership without guessing plugin load or effect bus routing. Slice green; project harness stays RED on `phase_5_tertiary_tree`.
