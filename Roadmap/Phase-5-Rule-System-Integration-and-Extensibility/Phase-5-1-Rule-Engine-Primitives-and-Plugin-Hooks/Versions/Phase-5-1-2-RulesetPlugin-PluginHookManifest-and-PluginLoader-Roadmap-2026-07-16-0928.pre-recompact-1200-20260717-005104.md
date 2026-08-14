---
title: Phase 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.2"
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_reason: body_over_cap:1379>1200
body_over_cap: true
body_chars_claimed: 1379
body_chars_cap: 1200
factory_feed_gate_status: red
created: 2026-07-16
tags: [roadmap, genesis-mythos-master, phase-5, ruleset-plugin, plugin-hook-manifest, plugin-loader]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]"
  - "[[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]"
  - "[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]"
  - "[[genesis-mythos-master-goal]]"
  - "[[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roll-up-2026-07-16]]"
rollup-detail: "[[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roll-up-2026-07-16]]"
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
---

## Phase 5.1.2 — RulesetPlugin / PluginHookManifest / PluginLoader

**RulesetPlugin** = bounded ruleset module (id, version, lifecycle). **PluginHookManifest** = rules + priority + veto/seam subscriptions. **PluginLoader** = session-init / boundary load; validates atoms vs RulePrimitive; owns `active_plugin_ids` on Frame. Arbiter/bus → **5.1.3**. No Godot / factory/L5.

## Scope

**In:** Plugin contract; Manifest fields; Loader init + boundary swap; duplicate `rule_id` reject; atom validation; SeamRegistry `rule`.

**Out:** Core/Primitive/Frame (`5.1.1`); Arbiter/EffectBus (`5.1.3`); spell (5.2); quest (5.3); mid-batch hot-swap; factory/L5.

## Behavior

Session-init: Loader reads SeamRegistry `rule` → `declare_hooks()` → validate atoms → register. Mid-session swaps defer to next boundary (ReGen 3.3). Duplicate `rule_id` → reject. Frame `active_plugin_ids` = sorted loaded IDs. Detail → [[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roll-up-2026-07-16]].

## Interfaces

**Imports:** RulePrimitive + Frame slot (`5.1.1`); SeamRegistry `rule` (1.3); ReGen (3.3). **Exports:** loaded registry + Manifest priority/veto → **5.1.3** / **5.2**.

## Roll-up

Contract shapes, load edges, OQs → rollup.

## Handoff

**80%** — plugin nouns explicit. Exec-deferred — advisory. Body **1379>1200**; slice red. Next DFS **self** recompact ≤1200 — not factory/L5.