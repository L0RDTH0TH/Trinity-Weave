---
title: Phase 2.3 — ToneProfile Profile Bundle on World Seed
roadmap-level: secondary
phase-number: 2
subphase-index: '2.3'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feedstock_slice: phase_2_secondary_tree
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-2
- tone-profile
- world-seed
- proc-gen
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roadmap-2026-06-29-2115]]'
- '[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 2.3 — ToneProfile Profile Bundle on World Seed

Materialize the **session 0 campaign tone contract** as a single **ToneProfile** bundle attached to the world seed: one replaceable profile per campaign that biases proc-gen, weather defaults, simulation baselines, lore/event framing, and quest moral tone — without siloed per-subsystem presets. This slice names profile bundle schema, archetype registry, seed attachment semantics, **ToneProfileInjector** weight tables, and integration handoffs with **2.1** SeedParser and **2.2** CanonFactValidator — without Godot implementation paths or execution-track rollup gates.

## Scope

**In scope:** **ToneProfileBundle** as the canonical session 0 artifact (profile id + weight manifest + provenance); **ArchetypeRegistry** for built-in profiles (High / Medium / Low / Grimdark per PMG); **Session0ToneSelector** (table/DM choice + Palette veto hooks); **ProfileWeightManifest** (terrain, biome, weather, entity rarity, event tone, quest framing bias namespaces); **SeedBundle.tone_profile** attachment contract consumed by **SeedParser**; **ToneProfileInjector** touchpoint registry (cross-cutting at receptive stage nodes per Phase 1.2); **ToneCompatibilityGate** at CanonFactValidator (boundary with **2.2**); **tone_fallback_applied** session bus event when unknown variant encountered; **ProvenanceEnvelope** on profile selection and overrides.

**Out of scope:** Generation pipeline stage ordering (secondary **2.1**); Canon registry lifecycle detail (secondary **2.2**); Godot C# profile loaders; factory catalog row shapes (`data/archetypes/` path locked on execution track); execution-track typed interfaces and rollup HR gates (**execution-deferred / advisory on conceptual track**); Phase 3 off-screen faction tick weight application (references profile id only); DM workbench Palette UI layout (Phase 4+).

## Behavior

**Actors:**

| Actor | Role |
|-------|------|
| **ArchetypeRegistry** | Indexes built-in ToneProfile archetypes with stable ids and default weight manifests |
| **Session0ToneSelector** | Presents archetype choices at session 0; records table/DM selection + optional Palette vetoes |
| **ToneProfileBundle** | Immutable-for-session bundle: `profile_id`, `weight_manifest`, `palette_overrides[]`, `provenance` |
| **ProfileWeightManifest** | Namespaced bias tables: `terrain.*`, `biome.*`, `weather.*`, `entity.*`, `event.*`, `quest.*` |
| **SeedBundleToneAttachment** | Embeds ToneProfileBundle reference + fingerprint into **SeedBundle** at session 0 closure |
| **ToneProfileInjector** | Cross-cutting orchestrator applying manifest slices at receptive nodes (Phase 1.2 contract) |
| **ToneCompatibilityGate** | Invoked by **CanonFactValidator** (**2.2**) — rejects or flags canon facts incompatible with active profile |
| **ToneFallbackResolver** | Maps unknown `profile_id` → Medium Fantasy defaults + `session.tone_fallback_applied` |

**Built-in archetypes (PMG):**

| Archetype | Id (lean) | World-gen bias (summary) | Sim / lore bias (summary) |
|-----------|-----------|--------------------------|---------------------------|
| **High Fantasy** | `tone.high_fantasy` | Elevated magic density, dramatic landforms | Heroic event defaults, wonder-forward quest framing |
| **Medium Fantasy** | `tone.medium_fantasy` | Balanced magic/rarity; default fallback | Neutral moral gray; standard quest pressure |
| **Low Fantasy** | `tone.low_fantasy` | Muted supernatural features; political human scale | Grounded consequences; rare overt magic in events |
| **Grimdark** | `tone.grimdark` | Bleak weather bias, harsh biome mixes | Costly hope; persistent scar defaults; grim quest tone |

Profiles are **defaults**, not stereotypes — **Palette** (table veto layer) may suppress individual weight keys without breaking bundle identity.

**Session 0 attachment flow:**

1. **Session0ToneSelector** presents archetype choices; table selects primary profile (+ optional Palette vetoes on weight keys)
2. **ToneProfileBundle** materialized with **ProvenanceEnvelope** (selector actor, timestamp, revision chain)
3. Session 0 closure → **SeedBundleToneAttachment** embeds bundle reference + fingerprint alongside map seed and accepted CanonFacts index
4. **SeedParser** (**2.1**) validates bundle presence; missing tone → block bundle formation (same severity as missing map seed)
5. **ToneProfileInjector** applies manifest at each receptive stage during **2.1** traversal
6. **ToneCompatibilityGate** runs on canon accept path (**2.2**) — facts violating profile bounds return explicit reject manifest

**Inputs / outputs:**

- *Into bundle:* Session 0 table choice, DM overrides (within policy), Palette veto list, community archetype extensions (registry lookup)
- *Out of bundle:* SeedBundle tone attachment, injector weight tables, compatibility rules for **2.2**, profile id for Phase 3+ sim/weather defaults

## Interfaces

**Imports from Phase 1 and Phase 2 siblings:**

| Source | How 2.3 consumes it |
|--------|---------------------|
| ToneProfileInjector contract (1.2) | Cross-cutting injection model; receptive stage registry |
| Stage DAG contracts (1.2.1) | Per-stage `terrain`/`biome`/… weight namespace mapping |
| SeedSnapshot + ProvenanceEnvelope (1.3) | Bundle fingerprint in snapshot; tone id in provenance envelope |
| SeedParser + GenerationPipeline (2.1) | SeedBundle attachment point; injector invocation during stage traversal |
| CanonFactValidator (2.2) | ToneCompatibilityGate hook on accept path |
| `session.*` bus (1.1) | `session.tone_selected`, `session.tone_fallback_applied`, `session.palette_veto_applied` |

**Exports to Phase 2 closure and Phase 3+:**

| Export | Consumer |
|--------|----------|
| **ToneProfileBundle** schema + attachment contract | Execution track mirror; Half A catalog mint (`data/archetypes/` layout) |
| **ArchetypeRegistry** + **ProfileWeightManifest** namespaces | **2.1** stage executors; Phase 3 weather/NPC defaults |
| **ToneCompatibilityGate** rules | **2.2** CanonFactValidator |
| Profile id + fingerprint | Phase 3 living simulation; Phase 5 quest moral tone bias |

**Adjacent slices:**

- **2.1** owns pipeline orchestration; 2.3 supplies bundle attachment and injector manifests — **2.1** §Integration spine with 2.3 satisfied by this note.
- **2.2** owns canon lifecycle; 2.3 owns profile selection and compatibility rules — validator invokes gate, does not own bundle mint.

## Edge cases

- **No tone selected at session 0:** SeedParser blocks **SeedBundle** formation; DM sees explicit missing-field list (not silent Medium Fantasy at parse — fallback only for *unknown* ids post-selection).
- **Unknown community profile id:** **ToneFallbackResolver** → Medium Fantasy + `session.tone_fallback_applied`; DM-visible log entry.
- **Palette veto removes all weights in a namespace:** Stage uses archetype defaults for that namespace only; bundle id unchanged; veto recorded in provenance.
- **Tone change mid-campaign (structural):** Requires **SeedSnapshot** + full regen path per Phase 1.3 — partial stage replay deferred to execution track with explicit waiver.
- **Canon fact conflicts with profile:** **ToneCompatibilityGate** rejects or flags for DM — no silent accept (**2.2** ConflictArbiter may still surface if fact accepted under waiver policy).
- **Session 0 closes before Palette review:** Session policy may auto-accept pending vetoes as empty; logged on `session.*` bus.

## Open questions

- **Community archetype extension format:** JSON manifest vs. catalog row — locked on execution track / Half A catalog mint.
- **Per-namespace override granularity:** Table edits single weight key vs. archetype swap — DM workbench UX deferred.
- **Horizon M0 minimum weight subset:** Which namespaces required for first playable loop — operator attestation via factory catalog.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope — ToneProfileBundle, ArchetypeRegistry, injector manifests; 2.1/2.2 boundaries explicit |
| Behavior (actors, ordering) | pass | § Behavior — session 0 attachment flow; six-step selection → inject → gate |
| Interfaces (adjacent contracts) | pass | § Interfaces — Phase 1 + 2.1/2.2 adjacency; Phase 3+ profile id export |
| Edge cases | pass | § Edge cases — missing tone, unknown id fallback, Palette veto, mid-campaign change |
| Open questions | pass | § Open questions — community archetype format, namespace override deferred |
| Pseudo-code readiness | pass | § Pseudo-code readiness — bundle attachment traceable without API signatures |
| Integration spine (2.1 + 2.2) | pass | § Responsibilities — SeedParser + ToneCompatibilityGate closed |
| **`handoff_readiness` aggregate** | **80%** | factory feed gate reconcile `phase_2_secondary_tree` slice 2.3; **Phase 2 secondary tree complete** |

> Execution-deferred / advisory on conceptual track: `data/archetypes/` catalog layout, Godot profile loaders, HR rollup gates — resolved on execution track or factory harness (`1373c0c3408d`).

## Pseudo-code readiness

A reader can trace session 0 tone selection → bundle materialization → SeedBundle attachment → injector application at stage nodes → compatibility gate on canon accept → fallback on unknown id — without guessing profile ownership or seed attachment order. No API signatures on conceptual track; execution deepen mints typed contracts under `Roadmap/Execution/` mirror spine.

## Research integration

Builds on Phase 1 ToneProfileInjector cross-cutting model and PMG single-bundle mandate:

- PMG: one bundled profile per campaign consumed by world gen, weather, sim defaults, lore events, quest framing — [[genesis-mythos-master-goal]]
- Phase 1.2 cross-cutting injector vs. explicit DAG port — lean injector retained; weight namespaces named here for **2.1** stage executors
- Execution rollup / catalog archetype path gates are **execution-deferred / advisory** on conceptual track

## Responsibilities

- [x] Name ToneProfileBundle, ArchetypeRegistry, and Session0ToneSelector actors
- [x] ProfileWeightManifest namespaces and SeedBundle attachment contract
- [x] Integration spine with **2.1** SeedParser + ToneProfileInjector touchpoints
- [x] Integration spine with **2.2** ToneCompatibilityGate at CanonFactValidator
- [x] Tertiary 2.3.1: ProfileWeightManifest archetype tables — [[Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roadmap-2026-06-29-2115]] (minted 2026-06-29)

## Tasks

- [x] Mint 2.3 secondary with profile bundle on world seed contract
- [x] Tertiary 2.3.1: ProfileWeightManifest archetype tables — [[Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roadmap-2026-06-29-2115]] (minted 2026-06-29)
- [ ] Optional tertiary: Palette veto schema detail — **deferred** to refine pass (owner: 2.3 refine) — partial coverage in 2.3.1 PaletteVetoKey schema
- [x] Handoff closure with **2.1** + **2.2** integration spines — documented in §Interfaces

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
