---
title: Conceptual decision record — Phase 5.1.3 RuleConflictArbiter/RuleEffectBus tertiary
created: 2026-07-16
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-5, tertiary-tree]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase513-tertiary-20260716T134105Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
---

# Conceptual decision record

## Summary

Minted Phase **5.1.3** tertiary under live `phase_5_tertiary_tree` for **RuleConflictArbiter** + **RuleEffectBus** — third Phase 5.1 tertiary; closes the **5.1 tertiary branch**. Advances DFS without factory/L5 or pseudo-code.

## PMG alignment

Deepens Phase 5 rule-system extensibility by naming the conflict-resolution and effect-routing surface that consumes 5.1.1 evaluator outputs and 5.1.2 Manifest priority/veto metadata, and exports channels to spell (5.2) and quest (5.3) plugins.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Fold arbiter into 5.1.1 | Fewer notes | Mixes evaluate + resolve; body over cap | Tertiary DFS requires distinct 5.1.3 |
| Mint spell 5.2.1 before closing 5.1 | Faster spell progress | Leaves EffectBus nouns unowned; 5.1.2 export dangling | Parent exports require 5.1.3 next |
| Split Arbiter and EffectBus into two tertiaries | Finer grain | Exceeds single-artifact deepen; parent groups them | Queue + single-structural-mint |

**Chosen:** mint `5.1.3` RuleConflictArbiter / RuleEffectBus; close 5.1 tertiary branch; queue `5.2.1` SpellAgencyPerspectiveManifest / SpellMetadataRegistry next.

## Validation evidence

- Queue: `followup-deepen-phase513-tertiary-20260716T134105Z`
- Gate: `factory_feed_gate` / `phase_5_tertiary_tree`
- Persona: `half_a.conceptual_architect`
- Artifact: `Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941.md`
- Pattern: parent 5.1 rollup RuleConflictArbiter/RuleEffectBus sections + Phase 5.1.1–5.1.2 tertiary shape
- MCP backup probe failed (connection); `run_mode: full_run_inline`
- Validator first pass: `needs_work` / `state_hygiene_failure` — report [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase513-tertiary-20260716T134105Z-20260716T134725Z.md]]
- IRA call 1 applied: [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-phase513-tertiary-20260716T134105Z.md]]
- Validator second pass: `needs_work` / `safety_unknown_gap` (codes_cleared: state_hygiene_failure) — [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase513-tertiary-20260716T134105Z-20260716T135520Z-second-pass.md]]
- FIX-008: workflow_state `deepen_complete` paid via handoff-audit repair `repair-handoff-audit-phase513-20260716T140302Z` (balance_triad on disk)

## Links

- Parent: [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]
- Prior tertiaries: [[Phase-5-1-1-RuleEngineCore-RulePrimitive-and-RuleContextFrame-Roadmap-2026-07-16-0910]], [[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]
- New tertiary: [[Phase-5-1-3-RuleConflictArbiter-and-RuleEffectBus-Roadmap-2026-07-16-0941]]
- PMG: [[genesis-mythos-master-goal]]
