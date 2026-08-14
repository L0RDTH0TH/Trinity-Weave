---
title: CDR — RuleCheckProbe Rule Check (6.2.5)
created: 2026-06-27
tags: [roadmap, cdr, genesis-mythos-master, phase-6, horizon-demo, rule-check]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260627T074500Z-6-2-5
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
persona_id: half_a.conceptual_architect
---

## Summary

Mint tertiary **6.2.5** for **RuleCheckProbe** — beat 5 (Rule check) of the eight-beat horizon demo loop. Decomposes post-tick **RuleContextFrame** stub assembly, **demo_ruleset** single-rule evaluation, and `rule.demo_pass` / `rule.demo_fail` exit gates from parent **6.2** secondary. Depth-first continuation after **6.2.4** sim stub.

## PMG alignment

PMG requires the horizon demo to prove **rule hooks** — player actions trigger evaluable conditions before DM overwrite beats. Isolating beat 5 validates the sim log → rule evaluation seam without conflating tick commit (beat 4) or DM cam transition (beat 6).

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Merge beats 4–5 in one tertiary | Fewer files | Violates eight-beat decomposition; tick and rule have distinct gates | One-beat-per-tertiary precedent (6.2.1–6.2.4) |
| Run full **PluginLoader** + multi-plugin arbiter | Production fidelity | Scope creep; beat 5 is probe only per parent 6.2 | Single **demo_ruleset** pass; full loader execution-deferred |
| Always-pass rule (no teachable fail) | Simpler kiosk flow | Misses OQ-6.2-002 teachable fail teaching moment | Fail path documented; halt default per **HorizonDemoManifest** |
| Skip **RuleContextFrame** stub | Faster stub | Breaks 5.1 evaluation contract | Demo-truncated frame required |

## Validation evidence

- Parent 6.2 beat table: beat 5 **RuleCheckProbe** with `demo.sim_tick_committed` + **WorldEventLog** `demo_interact_observed` entry (frame built internally) and **RuleEffectBus** `rule.demo_pass` / `rule.demo_fail` + `demo.rule_check_complete` on `session.*` output.
- 6.2.4 export: **WorldEventLog** `demo_interact_observed` + `demo.sim_tick_committed` on `session.*`.
- 5.1 **RuleEngineCore**, **RuleContextFrame**, **RuleEffectBus**, **RulePrimitive** library (conceptual authority — stubbed depth).
- OQ resolutions: OQ-6.2.5-001 stub frame; OQ-6.2.5-002 pass presentation echo; OQ-6.2.5-003 halt-on-fail default.
- Validator second pass (2026-06-27): [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-godo-followup-20260627T074500Z-6-2-5-20260627T083000Z-second-pass]] — log_only; IRA rollup reconciled.

## Links

- Parent: [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]
- Prior beat: [[Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]
- Tertiary note: [[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]
- Workflow log target: Phase-6-2-5-RuleCheckProbe-Rule-Check (2026-06-27 08:00)
- Queue: `godo-followup-20260627T074500Z-6-2-5`
