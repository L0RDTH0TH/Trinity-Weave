---
title: "CDR — ToneProfile Profile Bundle on World Seed (Phase 2.3 deepen)"
created: 2026-06-26
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-2]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T153500Z-phase2-3
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research:
  - "[[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]"
  - "[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]"
  - "[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]"
---

## Summary

Minted Phase **2.3** secondary defining **ToneProfileBundle** as the session 0 campaign tone contract: **ArchetypeRegistry** (High / Medium / Low / Grimdark), **ProfileWeightManifest** namespaces, **SeedBundle** attachment via **SeedBundleToneAttachment**, and **ToneCompatibilityGate** at **2.2** CanonFactValidator. Retained cross-cutting **ToneProfileInjector** model from Phase 1.2 with explicit weight namespaces for **2.1** stage executors.

## PMG alignment

Implements PMG **`ToneProfile`** mandate — one bundled profile per campaign consumed by world gen, weather, sim defaults, lore/event tone, and quest framing — not siloed per-subsystem presets. Session 0 choice drives proc-gen and lore-tone defaults on the world seed per Phase 2 primary scope.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Embed tone weights inside **2.1** SeedParser note only | Fewer files | Blurs pipeline vs profile ownership; duplicates PMG glue task | Phase 2 primary lists ToneProfile as distinct glue/integration task (2.3) |
| Explicit ToneProfile port on each DAG edge (1.2 open question) | Stage-local clarity | Re-negotiate DAG on profile updates | Phase 1.2 lean cross-cutting **ToneProfileInjector** retained; namespaces named in 2.3 |
| Silent Medium Fantasy default when tone missing at session 0 | Faster bootstrap | Violates explicit session 0 table agency | SeedParser blocks bundle formation; fallback only for *unknown* profile ids |

## Validation evidence

- PMG ToneProfile archetypes and single-bundle contract — [[genesis-mythos-master-goal]]
- Phase 1.2 ToneProfileInjector cross-cutting model — [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]
- **2.1** SeedParser + injector consumption points — [[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]] § Behavior
- **2.2** tone compatibility at CanonFactValidator — [[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]] § Adjacent slices
- Execution rollup gates **execution-deferred / advisory** on conceptual track per operator guidance
- Hostile validator (first pass): [[.technical/Validator/roadmap-auto-validation-20260626T193500Z-godo-followup-20260626T153500Z-phase2-3]] — primary_code: contradictions_detected; IRA repair applied 2026-06-26
- Validator (second pass): [[.technical/Validator/roadmap-auto-validation-20260626T201500Z-godo-followup-20260626T153500Z-phase2-3-second-pass]] — softened; consume_eligible

## Links

- Workflow log: 2026-06-26 15:35 | Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed | iter 2.3
- Factory run: `product_factory_run_id: f35ff65cfb4f`
- Persona: `half_a.conceptual_architect`
