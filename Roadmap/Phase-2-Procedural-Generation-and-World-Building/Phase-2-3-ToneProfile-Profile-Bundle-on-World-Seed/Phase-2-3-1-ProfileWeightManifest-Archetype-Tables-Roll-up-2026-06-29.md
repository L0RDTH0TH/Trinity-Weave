---
title: Phase 2.3.1 — Roll-up & ProfileWeightManifest Archetype Tables
roadmap-level: rollup
phase-number: 2
subphase-index: 2.3.1
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roadmap-2026-06-29-2115]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-2
- rollup
- tone-profile
- profile-weight-manifest
- archetype-registry
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Actors

| Actor | Role |
|-------|------|
| **ArchetypeRegistry** | Stable id → default **ProfileWeightManifest** + display metadata |
| **ProfileWeightManifest** | Namespaced bias tables consumed by **ToneProfileInjector** at receptive stage nodes |
| **PaletteVetoKey** | Dot-path key within a namespace that table/DM may suppress without changing `profile_id` |
| **NamespaceDefaultResolver** | When all keys in a namespace are vetoed → archetype defaults for that namespace only |
| **ToneProfileInjector** | Applies manifest slices per **ReceptiveNodeBinding** (Phase 1.2.1 stage DAG mapping) |

## ReceptiveNodeBinding index (conceptual v1)

| Namespace | Receptive stage node | Stage executor |
|-----------|---------------------|----------------|
| `terrain.*` | `gen.stage.terrain` | TerrainStageExecutor |
| `biome.*` | `gen.stage.biomes` | BiomeStageExecutor |
| `weather.*` | `gen.stage.biomes` | BiomeStageExecutor (weather bias channel) |
| `entity.*` | `gen.stage.entities` | EntityStageExecutor |
| `event.*` | `gen.stage.sim_bootstrap` | SimBootstrapStageExecutor |
| `quest.*` | `gen.stage.sim_bootstrap` | SimBootstrapStageExecutor (quest framing channel) |

## Built-in archetype weight summary (conceptual v1)

| Archetype id | terrain.* bias | biome.* bias | weather.* bias | entity.* bias | event.* bias | quest.* bias |
|--------------|----------------|--------------|----------------|---------------|--------------|--------------|
| `tone.high_fantasy` | elevated relief, wonder landforms | magic-dense biomes favored | dramatic swings tolerated | rare entities more common | heroic framing default | wonder-forward moral tone |
| `tone.medium_fantasy` | balanced relief | neutral biome mix | moderate variance | baseline rarity | neutral gray events | standard quest pressure |
| `tone.low_fantasy` | muted supernatural terrain features | political/human-scale biomes | grounded weather | rare overt magic entities | grounded consequences | rare overt magic in quests |
| `tone.grimdark` | harsh/ bleak landform bias | bleak biome mixes | persistent harsh weather | scar-prone entity defaults | costly hope events | grim moral tone |

## Session 0 materialization flow

1. **Session0ToneSelector** picks archetype id → **ArchetypeRegistry** lookup yields default manifest
2. Optional **Palette** applies **PaletteVetoKey** list → **NamespaceDefaultResolver** fills gaps
3. **ToneProfileBundle** seals `profile_id`, manifest fingerprint, veto list, **ProvenanceEnvelope**
4. **SeedBundleToneAttachment** embeds bundle reference (parent 2.3 six-step flow)
5. **ToneProfileInjector** consults **ReceptiveNodeBinding** at each 2.1 stage traversal

## Interface tables

### Imports

| Source | Consumption |
|--------|-------------|
| Stage DAG contracts (1.2.1) | Namespace → stage executor mapping for **ReceptiveNodeBinding** |
| SeedParser + GenerationPipeline (2.1) | Injection touchpoints during stage traversal |
| CanonFactValidator (2.2) | **ToneCompatibilityGate** reads active `profile_id` + manifest bounds |
| `session.*` bus (1.1) | `session.tone_selected`, `session.palette_veto_applied`, `session.tone_fallback_applied` |

### Exports

| Export | Consumer |
|--------|----------|
| **ArchetypeRegistry** canonical index | Half A catalog mint (`1373c0c3408d`); execution mirror |
| **ProfileWeightManifest** namespace tables | 2.1 stage executors; Phase 3 weather/NPC defaults |
| **PaletteVetoKey** schema | DM workbench (Phase 4+) |
| **ReceptiveNodeBinding** index | **ToneProfileInjector** orchestration |

## Edge cases

- **Unknown `profile_id` post-selection:** **ToneFallbackResolver** → `tone.medium_fantasy` + `session.tone_fallback_applied` (parent 2.3).
- **Veto removes all keys in `weather.*`:** **NamespaceDefaultResolver** restores archetype weather defaults only; bundle id unchanged.
- **Community extension id:** Registry lookup miss → same fallback path; extension format deferred to execution catalog.
- **Mid-campaign tone change:** Requires **SeedSnapshot** + full regen — partial namespace hot-swap forbidden on conceptual track.
- **Canon fact vs profile bounds:** **ToneCompatibilityGate** (2.2) rejects or flags — manifest tables do not override arbiter policy.

## Open questions

- **Per-key table edit vs archetype swap at session 0:** DM workbench UX — Phase 4+.
- **Horizon M0 minimum namespace subset:** Which namespaces required for first playable — operator attestation via factory catalog.
- **Community archetype JSON manifest vs catalog row:** Execution-deferred / Half A catalog mint.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | Registry, manifest namespaces, veto schema; factory/L5 boundaries explicit |
| Behavior (actors, ordering) | pass | Four archetype table + five-step materialization |
| Interfaces (adjacent contracts) | pass | 1.2.1, 2.1, 2.2 adjacency |
| Edge cases | pass | Fallback, veto empty namespace, mid-campaign change |
| Open questions | pass | UX + M0 subset deferred |
| Pseudo-code readiness | pass | Selection → manifest → inject traceable |
| **`handoff_readiness` aggregate** | **80%** | factory feed gate `phase_2_tertiary_tree` third mint 2.3.1; parent 2.3 `handoff_readiness: 80` |

> Execution-deferred / advisory on conceptual track: `data/archetypes/` layout, Godot loaders, REGISTRY-CI, HR rollup gates — resolved on execution track or factory harness (`1373c0c3408d`).

## Pseudo-code readiness

A reader can trace archetype selection → registry lookup → manifest namespaces → veto application → SeedBundle attachment → per-stage injector binding without guessing weight ownership or namespace semantics. No API signatures on conceptual track; execution deepen mints typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

Builds on parent 2.3 research integration (no new pre-deepen research this run):

- PMG single-bundle mandate — one profile biases world gen, weather, sim, lore, quest framing — [[genesis-mythos-master-goal]]
- Phase 1.2 **ToneProfileInjector** cross-cutting model retained; namespace tables named here for 2.1 stage executors
- Execution rollup / catalog archetype path gates are **execution-deferred / advisory** on conceptual track

## Responsibilities

- [x] **ArchetypeRegistry** index with four PMG built-in ids and namespace bias summaries
- [x] **ProfileWeightManifest** namespace table contract (`terrain` through `quest`)
- [x] **PaletteVetoKey** schema + **NamespaceDefaultResolver** edge semantics
- [x] **ReceptiveNodeBinding** index linking namespaces to 1.2.1 stage DAG receptive nodes
- [x] Integration spine with **2.1** injector touchpoints and **2.2** ToneCompatibilityGate bounds
