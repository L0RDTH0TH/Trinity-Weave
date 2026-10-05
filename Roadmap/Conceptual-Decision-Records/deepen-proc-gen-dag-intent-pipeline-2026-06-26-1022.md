---
title: CDR — Phase 1.2 Proc-Gen Stage DAG + Intent Population Pipeline
zettel-type: conceptual-decision-record
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]"
queue_entry_id: godo-9e6f65ddccde
created: 2026-06-26
validation_status: validated
tags: [cdr, genesis-mythos-master, proc-gen, intent-pipeline, conceptual]
---

## Decision summary

Phase 1.2 establishes the **stage DAG with forward-progress invariant** as the conceptual spine of all procedural generation in Genesis Mythos. The key architectural commitment: generation is a **deterministic compile**, not an open-ended generative stream — DeterministicCompiler is a first-class design row, not a Phase 6 detail.

## Chosen path

- **Stage DAG** (Directed Acyclic Graph) with typed outputs per stage: `SeedBundle → terrain → biomes → POIs → entities → sim_bootstrap → CompiledWorldManifest`
- **ToneProfileInjector** as cross-cutting concern injected by StageOrchestrator — not a dedicated DAG slot — keeps stage nodes independent of profile knowledge
- **IntentResolver** maps `accepted` CanonFacts through CanonCommitBoundary into LoreHookRegistry (faction/tribe/NPC seeds) before sim bootstrap
- **DeterministicCompiler** required for byte-stable output given identical inputs (save/load, dry-run validation, and replay correctness all depend on it)

## PMG alignment

- PMG Phase 1: "Outline the procedural generation graph and intent population pipeline (seeds, overrides, lore injections)" — fully addressed
- PMG Phase 2: "Generation pipeline: seed parsing → terrain → biomes → POIs → entities → simulation bootstrap" — stage identities and DAG edges match PMG Phase 2 ordering exactly
- PMG canon pipeline: `proposed → accepted → hooked → sim-active` — CanonCommitBoundary gate and IntentResolver flow are direct conceptual implementations
- PMG ToneProfile: "one bundled profile per campaign … consumed by world gen, weather, sim defaults, lore events, quest framing via one replaceable profile contract" — satisfied by cross-cutting ToneProfileInjector design

## Alternatives considered

1. **Monolithic generative output** (no explicit compile stage): risks non-determinism and untestable world seeds; rejected per WorldGen pattern research and academic narrative-to-deterministic-assembly work
2. **ToneProfile as explicit DAG stage node**: creates a synchronization dependency between profile and every downstream stage; increases coupling; cross-cutting injector preserves stage independence and is simpler to swap

## Evidence links

- [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]] — WorldGen Director→Validator→Critic→Compiler; DAG-for-proceduralism; canon pipeline noun proposals
- [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-godot-gmm-033500Z]] — bus delivery semantics for session.* events; two-pipeline dry-run (validation pipeline only)
- [[genesis-mythos-master-goal]] — PMG stage order, ToneProfile mandate, canon pipeline contract
