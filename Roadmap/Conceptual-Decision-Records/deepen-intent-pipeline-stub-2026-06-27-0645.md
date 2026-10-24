---
title: CDR — IntentPipelineStub Intent Stub (6.2.3)
created: 2026-06-27
tags: [roadmap, cdr, genesis-mythos-master, phase-6, horizon-demo, intent-stub]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260627T064500Z-6-2-3
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
persona_id: half_a.conceptual_architect
---

## Summary

Mint tertiary **6.2.3** for **IntentPipelineStub** — beat 3 (Intent stub) of the eight-beat horizon demo loop. Decomposes interact sample capture, `intent.demo_interact` token publication on `input.*`, and `demo.intent_labeled` exit gate from parent **6.2** secondary. Depth-first continuation after **6.2.2** FP explore.

## PMG alignment

PMG requires the horizon demo to prove **InputIntent → simulation-relevant signal** before tick/rule/DM beats. Isolating beat 3 validates the intent seam without conflating FP input consumption (beat 2) or sim tick commit (beat 4) — supporting living-sim pillar felt in the playable loop.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Merge beats 2–3 in one tertiary | Fewer files | Violates eight-beat decomposition; FP explore and intent labeling have distinct gates | One-beat-per-tertiary precedent (6.2.1, 6.2.2) |
| Route labeled token on `session.*` only | Single bus | Breaks 1.1 **InputIntent** layer authority; parent beat table specifies `input.*` | Token on `input.*`; stage signal on `session.*` |
| Invoke full **IntentResolver** in demo | Richer canon path | Scope creep; beat 3 is stub only per parent 6.2 | Stub token only; resolver execution-deferred |
| Multi-intent catalog in v1 | Teaches variety | Over-engineers demo v1 loop teaching path | Single `intent.demo_interact` per OQ-6.2.3-001 |

## Validation evidence

- Parent 6.2 beat table: beat 3 **IntentPipelineStub** with interact sample input and `intent.demo_interact` on `input.*`.
- 6.2.2 export: `demo.fp_active` + interact sample closing beat 2.
- 1.1 **InputIntent** layer: self-agency envelopes on `input.*` bus.
- OQ resolutions: OQ-6.2.3-001 single token; OQ-6.2.3-002 no proximity gate v1; OQ-6.2.3-003 bus split input vs session.
- Validator: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-godo-followup-20260627T064500Z-6-2-3-20260627T065000Z]]; second pass: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-godo-followup-20260627T064500Z-6-2-3-20260627T071000Z-second-pass]]

## Links

- Parent: [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]
- Prior beat: [[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]
- Tertiary note: [[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]
- Workflow log target: Phase-6-2-3-IntentPipelineStub-Intent-Stub (2026-06-27 06:45)
- Queue: `godo-followup-20260627T064500Z-6-2-3`
