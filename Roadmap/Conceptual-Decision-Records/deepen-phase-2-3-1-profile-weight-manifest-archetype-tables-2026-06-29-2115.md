---
title: "Deepen — Phase 2.3.1 ProfileWeightManifest archetype tables"
created: 2026-06-29
tags: [roadmap, cdr, genesis-mythos-master, phase-2, tone-profile]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roadmap-2026-06-29-2115]]"
decision_kind: deepen
queue_entry_id: architect-rr-gmm-remi-phase2-tertiary-next-20260629T211500Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: pending_validator_second_pass
related_research: []
persona_id: half_a.conceptual_architect
---

# Deepen — Phase 2.3.1 ProfileWeightManifest archetype tables

## Summary

Minted **2.3.1 — ProfileWeightManifest Archetype Tables** as third Phase 2 tertiary under factory feed gate cursor `phase_2_tertiary_tree`. Materializes **ArchetypeRegistry** index rows, six-namespace **ProfileWeightManifest** bias summaries for four PMG archetypes, **PaletteVetoKey** schema, and **ReceptiveNodeBinding** index deferred in parent 2.3 § Responsibilities.

## PMG alignment

PMG mandates one bundled tone profile per campaign consumed across world gen, weather, sim defaults, lore events, and quest framing. Parent 2.3 named actors and session 0 flow; this tertiary makes per-archetype weight tables explicit for factory feedstock and **ToneProfileInjector** stage bindings.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| 2.1.2 stage executor detail tertiary | Deepens 2.1 branch (still `branch_open: true`) | Breaks breadth-first tertiary tree rhythm (2.1.1 → 2.2.1 → 2.3) | Harness cursor `phase_2_tertiary_tree` follows one-first-tertiary-per-secondary before branch depth |
| 2.2.2 RegistrySnapshot schema | Completes optional 2.2 backlog | Lower factory-feed priority vs closing 2.3 first tertiary | Parent 2.3 defers weight tables; 2.3.1 closes first warranted 2.3 tertiary |
| Palette veto schema as separate 2.3.2 | Smaller slice | Extra mint before tree breadth closure | Veto schema folded into 2.3.1 scope per Half A nouns-first bundling |

**Chosen path:** 2.3.1 ProfileWeightManifest archetype tables as third Phase 2 tertiary.

## Validation evidence

- Pattern: parent 2.3 § Behavior built-in archetypes table + § Interfaces ProfileWeightManifest namespaces
- Pattern: Phase 1.2.1 stage DAG receptive node mapping for injector bindings
- Parent deferral: 2.3 § Responsibilities optional per-archetype weight table — now minted

## Links

- Minted tertiary: [[Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roadmap-2026-06-29-2115]]
- Workflow anchor: 2026-06-29 21:15 | Phase-2-3-1-ProfileWeightManifest-Archetype-Tables | architect-rr-gmm-remi-phase2-tertiary-next-20260629T211500Z
- Persona: half_a.conceptual_architect | product_factory_run_id: 1373c0c3408d

## Validator trace

- `validator_first: needs_work` | `primary_code: state_hygiene_failure` | `reason_codes: state_hygiene_failure,contradictions_detected,safety_unknown_gap,missing_task_decomposition`
- `report: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-phase2-tertiary-next-20260629T211500Z-20260629T211800Z]]`
- `ira_applied: true` | `ira_report: [[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-architect-rr-gmm-remi-phase2-tertiary-next-20260629T211500Z.md]]`
- `body_compact: pending` | next: validator second pass → 2.3.1 body compact queue
