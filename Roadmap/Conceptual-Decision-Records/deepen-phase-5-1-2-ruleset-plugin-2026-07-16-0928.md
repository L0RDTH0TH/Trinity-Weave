---
title: Conceptual decision record — Phase 5.1.2 RulesetPlugin/PluginHookManifest/PluginLoader tertiary
created: 2026-07-16
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-5, tertiary-tree]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase512-tertiary-20260716T132542Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
---

# Conceptual decision record

## Summary

Minted Phase **5.1.2** tertiary under live `phase_5_tertiary_tree` for **RulesetPlugin** + **PluginHookManifest** + **PluginLoader** — second Phase 5 tertiary after 5.1.1 evaluator core. Advances DFS without factory/L5 or pseudo-code.

## PMG alignment

Deepens Phase 5 rule-system extensibility by naming the plugin load surface that registers rulesets into RuleEngineCore and supplies priority/veto metadata to the arbiter/bus tertiary.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Fold plugins into 5.1.1 | Fewer notes | Mixes evaluator + load ownership; body over cap | Tertiary DFS requires distinct 5.1.2 |
| Mint arbiter+bus with plugins | Faster stack | Exceeds single-artifact deepen | Queue + single-structural-mint |
| Skip to 5.2 spell plugins | Spell progress | Leaves load nouns unowned; 5.1.1 export dangling | Parent exports require 5.1.2 next |

**Chosen:** mint `5.1.2` RulesetPlugin / PluginHookManifest / PluginLoader; queue `5.1.3` RuleConflictArbiter / RuleEffectBus next.

## Validation evidence

- Queue: `followup-deepen-phase512-tertiary-20260716T132542Z`
- Gate: `factory_feed_gate` / `phase_5_tertiary_tree`
- Persona: `half_a.conceptual_architect`
- Artifact: `Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928.md`
- Pattern: parent 5.1 rollup RulesetPlugin/PluginHookManifest/PluginLoader sections + Phase 5.1.1 tertiary shape
- MCP backup probe returned empty; `run_mode: full_run_inline`
- Validator first pass: `needs_work` / `state_hygiene_failure` — report [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase512-tertiary-20260716T132542Z-20260716T133240Z.md]]
- IRA call 1 applied: [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-phase512-tertiary-20260716T132542Z.md]]

## Links

- Parent: [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]
- Prior tertiary: [[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]]
- New tertiary: [[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]
- PMG: [[genesis-mythos-master-goal]]
