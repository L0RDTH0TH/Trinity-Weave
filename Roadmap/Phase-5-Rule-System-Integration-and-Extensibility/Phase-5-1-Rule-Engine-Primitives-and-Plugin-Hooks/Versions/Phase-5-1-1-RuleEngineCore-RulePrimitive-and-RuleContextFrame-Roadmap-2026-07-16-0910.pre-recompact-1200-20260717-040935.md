---
title: Phase 5.1.1 — RuleEngineCore / RulePrimitive / RuleContextFrame
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.1"
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: red
created: 2026-07-16
tags: [roadmap, genesis-mythos-master, phase-5, rule-engine-core, rule-primitive, rule-context-frame]
para-type: Project
roadmap_track: conceptual
links:
  - "[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]"
  - "[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]"
  - "[[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]"
  - "[[genesis-mythos-master-goal]]"
  - "[[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roll-up-2026-07-16]]"
rollup-detail: "[[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roll-up-2026-07-16]]"
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
factory_feed_gate_reason: body_over_cap:1415>1200
body_over_cap: true
body_chars_claimed: 1415
body_chars_cap: 1200

---

## Phase 5.1.1 — RuleEngineCore / RulePrimitive / RuleContextFrame

**RuleEngineCore** = condition→effect loop + cycle detector. **RulePrimitive** = condition/effect atom library. **RuleContextFrame** = per-eval snapshot (actor, scene, canon, envelopes, tone). Plugins/arbiter/bus → **5.1.2–5.1.3**. No Godot / factory/L5.

## Scope

**In:** Core loop; Primitive atoms; ContextFrame fields; rule `{condition_set, effect_set, trigger}`; nil-actor quiet-skip; cycle abort.

**Out:** RulesetPlugin/PluginHookManifest/PluginLoader (`5.1.2`); Arbiter/EffectBus (`5.1.3`); spell (5.2); quest (5.3); DSL; factory/L5.

## Behavior

Trigger → frame → Primitive conditions (AND default) → collect effects → cycle seen-set on `rule_id` aborts loops. Dispatch → **5.1.3**. Detail → [[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roll-up-2026-07-16]].

## Interfaces

**Imports:** SeamRegistry `rule` (1.3); Canon (2.2); ToneProfile (2.3); WorldState (3.1); envelopes (4.1/4.3). **Exports:** Core + Primitive + Frame → **5.1.2** / **5.1.3** / **5.2**.

## Roll-up

Atom tables, frame fields, OQs → [[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roll-up-2026-07-16]].

## Handoff

**80%** — evaluator nouns explicit. Slice **green**; project **RED** (`phase_5_tertiary_tree`); **5.1.2–5.1.3 minted**; **5.1 branch closed**; next **5.2.1** SpellAgencyPerspectiveManifest / SpellMetadataRegistry.
