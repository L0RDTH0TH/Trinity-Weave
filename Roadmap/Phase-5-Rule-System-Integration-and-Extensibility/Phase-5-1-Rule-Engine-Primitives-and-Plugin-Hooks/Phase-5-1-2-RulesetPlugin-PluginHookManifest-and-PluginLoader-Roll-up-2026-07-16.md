---
title: Phase 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader (Roll-up)
roadmap-level: rollup
phase-number: 5
subphase-index: 5.1.2
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags:
- roadmap
- rollup
- genesis-mythos-master
- phase-5
- ruleset-plugin
- plugin-loader
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roll-up-2026-07-15]]'
- '[[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 5.1.2 roll-up — RulesetPlugin / PluginHookManifest / PluginLoader

Canonical compact tertiary: [[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]. Detail preserved off the ≤1400 feedstock body (`followup-deepen-phase512-tertiary-20260716T132542Z`).

## Purpose

Name the **plugin load surface** — ruleset module contract, declarative hook manifest, and session-boundary loader — that feeds RuleEngineCore (5.1.1) and supplies priority/veto metadata to Arbiter/EffectBus (5.1.3).

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **RulesetPlugin** | Bounded module: `plugin_id` (lowercase-kebab), `version` (semver), `declare_hooks()` → Manifest, `on_load` / `on_unload` lifecycle |
| **PluginHookManifest** | `rules[]` (full rule triples), `priority` (lower = higher precedence), `veto_classes[]`, `required_condition_atoms[]`, `required_effect_atoms[]`, `tone_bias_subscriptions[]` |
| **PluginLoader** | Session-init load from SeamRegistry `rule`; atom validation vs RulePrimitive; duplicate `rule_id` reject; session-boundary swap; owns `active_plugin_ids` on RuleContextFrame |

**Out:** RuleEngineCore / RulePrimitive / RuleContextFrame field ownership (`5.1.1`); RuleConflictArbiter / RuleEffectBus (`5.1.3`); 5.2 spell metadata; 5.3 quest pressure; mid-batch hot-swap; factory/L5; execution pins.

**Ownership note:** `active_plugin_ids` on RuleContextFrame is **this tertiary's export** — PluginLoader populates the sorted loaded-plugin list after successful load; 5.1.1 only names the import slot.

## Behavior detail

1. At session init, **PluginLoader** enumerates SeamRegistry `rule` seam registrations.
2. Each **RulesetPlugin** returns a **PluginHookManifest** via `declare_hooks()`.
3. Loader validates `required_condition_atoms` / `required_effect_atoms` against registered **RulePrimitive** library; unknown atoms → `plugin_load_error` in WorldEventLog; plugin rejected.
4. Duplicate `rule_id` across plugins → `duplicate_rule_id`; first-registered wins by load order.
5. Successful loads update RuleContextFrame `active_plugin_ids` (sorted). Mid-session arrivals defer to next session boundary (ReGenerationIntentQueue 3.3); mid-batch snapshot immutable.
6. Manifest `priority` / `veto_classes` consumed by **RuleConflictArbiter** (5.1.3) — this tertiary does not own arbitration.

## Edge cases

- **Unknown atom at load time:** reject plugin; do not invent primitives.
- **Duplicate rule_id:** reject second registration; log `duplicate_rule_id`.
- **Session-boundary swap race:** defer new registrations; evaluation batch sees immutable plugin set.
- **Plugin unload mid-session:** only at boundary; in-flight frames keep prior `active_plugin_ids`.

## Open questions

- **OQ-5.1-002** (hot-swap mid-session) — session-boundary policy locked; OverwritePatchLayer (3.3) for emergency structural patches; further nuance execution-deferred.
- **OQ-5.1-001** (DSL format) — behaviour-first; serialization execution-deferred (parent rollup).

## Handoff criteria

- [x] RulesetPlugin / PluginHookManifest / PluginLoader nouns named
- [x] Atom validation + duplicate rule_id + boundary deferral stated
- [x] `active_plugin_ids` ownership claimed for this tertiary
- [x] Arbiter/bus deferred to 5.1.3
- [x] Tertiary body recompact ≤1200 (`1379→1197≤1200`; `followup-deepen-gmm-5-1-2-20260717T042415Z`)

**80%** handoff_readiness — implementer can place plugin-load ownership without guessing arbiter merge or effect routing. Slice green; project harness **RED** next Phase-5-1-3 `body_over_cap:1353>1200` — not factory/L5.
