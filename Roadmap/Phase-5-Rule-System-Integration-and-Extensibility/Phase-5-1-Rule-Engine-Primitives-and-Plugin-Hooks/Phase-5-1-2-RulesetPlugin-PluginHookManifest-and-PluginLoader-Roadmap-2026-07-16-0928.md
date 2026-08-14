---
title: Phase 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader
roadmap-level: tertiary
phase-number: 5
subphase-index: 5.1.2
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: green
factory_feed_gate_reason: tertiary_body_recompact_1200_complete
body_over_cap: false
body_chars_claimed: 1197
body_chars_cap: 1200
body_chars_pre_recompact: 1379
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-5
- ruleset-plugin
- plugin-hook-manifest
- plugin-loader
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]'
- '[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roll-up-2026-07-16]]'
rollup-detail: '[[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roll-up-2026-07-16]]'
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader

**RulesetPlugin** = ruleset module (id, version, lifecycle). **PluginHookManifest** = rules + priority + veto/seam subscriptions. **PluginLoader** = session-init / boundary load; owns `active_plugin_ids` on Frame. Arbiter/bus → **5.1.3**. No Godot / factory/L5.

## Scope

**In:** Plugin contract; Manifest; Loader init + boundary swap; duplicate `rule_id` reject; SeamRegistry `rule`.

**Out:** Core/Primitive/Frame (`5.1.1`); Arbiter/EffectBus (`5.1.3`); spell (5.2); quest (5.3); factory/L5.

## Behavior

SeamRegistry `rule` → `declare_hooks()` → validate atoms → register. Mid-session swaps defer to next boundary (ReGen 3.3). Duplicate `rule_id` → reject. Frame `active_plugin_ids` = sorted loaded IDs.

## Interfaces

**Imports:** RulePrimitive + Frame (`5.1.1`); SeamRegistry `rule` (1.3); ReGen (3.3). **Exports:** registry + Manifest priority/veto → **5.1.3** / **5.2**.

## Roll-up

Shapes, load edges, OQs → [[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roll-up-2026-07-16]].

## Handoff

**80%** — plugin nouns explicit. Exec-deferred. Body ≤1200; slice green. Next DFS **5.1.3** — not factory/L5.
