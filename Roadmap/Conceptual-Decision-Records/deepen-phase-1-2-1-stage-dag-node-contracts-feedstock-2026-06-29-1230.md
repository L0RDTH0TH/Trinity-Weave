---
title: "CDR — Phase 1.2.1 Stage DAG node contracts feedstock"
created: 2026-06-29
tags: [roadmap, cdr, genesis-mythos-master, phase-1, proc-gen]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]"
decision_kind: deepen
queue_entry_id: architect-rr-gmm-remi-c3678396
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: pending_validator
related_research: []
---

## Summary

Chose **per-stage contract tables + StageDAG edge registry + ToneProfile injection point registry** as the authoritative feedstock shape for tertiary **1.2.1**, matching the factory feed gate pattern established on **1.1.3** and **1.3.3**. Intent-population detail remains on sibling **1.2.2** to avoid duplicating LoreHookRegistry flow.

## PMG alignment

Supports PMG procedural generation spine: deterministic stage DAG with typed manifests from SeedBundle through SimGraphSeed, enabling Half A catalog mint (`pmg_phases`) without execution-track pseudo-code.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Merge 1.2.1 + 1.2.2 into one tertiary | Single file for proc-gen | Oversized note; violates single-artifact deepen | Factory feed gate targets one slice per dispatch |
| API-signature pseudo-code at depth 4 | Execution-ready | Violates conceptual_architect persona on conceptual track | Deferred to execution mirror |
| Minimal manifest summary only (pre-deepen body) | Fast | Failed `feedstock_incomplete` harness gate | Material change required |

## Validation evidence

- Pattern: [[Phase-1-1-3-Per-Layer-Interface-Contract-Tables-Roadmap-2026-06-29-1007]] per-layer table shape
- Pattern: [[Phase-1-3-3-DryRunValidator-and-ProvenanceEnvelope-Contract-Roadmap-2026-06-29-1205]] registry + check catalog cite to `dag.preflight`
- Parent: [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]] § Behavior ordering

## Links

- workflow_state log: 2026-06-29 12:35 deepen Phase-1-2-1-Stage-DAG-Node-Contracts
- queue: `architect-rr-gmm-remi-c3678396`
- persona: `half_a.conceptual_architect`
- validator: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-c3678396-20260629T123658Z]]
- validator_second: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-c3678396-20260629T124410Z-second-pass]]
- ira: [[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-architect-rr-gmm-remi-c3678396.md]]
