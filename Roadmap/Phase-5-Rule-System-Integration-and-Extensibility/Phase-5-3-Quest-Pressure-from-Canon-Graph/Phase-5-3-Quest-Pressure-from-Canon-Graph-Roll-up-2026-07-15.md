---
title: Phase 5.3 — Quest Pressure from Canon Graph (Roll-up)
roadmap-level: rollup
phase-number: 5
subphase-index: '5.3'
project-id: genesis-mythos-master
status: complete
priority: high
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-5
- quest-pressure
- canon-graph
- rule-engine
- rollup
para-type: Project
roadmap_track: conceptual
rollup_of: '[[Phase-5-3-Quest-Pressure-from-Canon-Graph-Roadmap-2026-06-26-2142]]'
links:
- '[[Phase-5-3-Quest-Pressure-from-Canon-Graph-Roadmap-2026-06-26-2142]]'
- '[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
body_compact_source_queue: followup-deepen-phase53-20260715T235806Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 5.3 — Roll-up detail (factory feed-gate compact)

Canonical NL detail preserved from secondary body compact 2026-07-15 (queue followup-deepen-phase53-20260715T235806Z). Secondary keeps nouns + scope; this note holds tables, schemas, bands, edge cases, open questions, tasks, dataview.

## Phase 5.3 — Quest Pressure from Canon Graph

Quest-pressure rules derive narrative urgency from the **CanonRegistry** relationship graph — threads, entities, locations, and hook states — and route systemic effects through **RuleEngineCore** / **SeamRegistry** into **RuleEffectBus** without inventing fetch-loop quest templates. This slice owns **QuestPressureManifest**, **CanonGraphPressureIndex**, and **QuestPressureRulePlugin** registration patterns that compose with spell metadata (5.2) under shared **RuleConflictArbiter** priority conventions.

## Scope

**In scope:** **QuestPressureManifest** (per-quest or per-thread metadata block); **QuestPressureRegistry** (lookup by `quest_pressure_id` at rule evaluation); **CanonGraphPressureIndex** (read-only projection over **CanonRegistry** + **LoreHookRegistry** graph edges); **QuestPressureSignal** taxonomy (thread urgency, entity stake, location tension, hook decay); **QuestPressureRulePlugin** pattern (registers quest rules + manifest via **SeamRegistry** `rule` family); **RuleContextFrame.quest_pressure_snapshot** extension when trigger class is quest-bound; **RuleEffectBus** `quest_pressure` channel (world_event, canon_proposal, tone_bias, and optional cross-channel hints to `agency_transition` / `perspective_transition` when spell side-effects interact); **RuleConflictArbiter** priority bands for quest vs spell effects (extends 5.2 conventions); integration with **CanonFact** lifecycle `hooked` / `sim-active` promotion as pressure source events.

**Out of scope:** Individual quest narrative scripts and reward tables (game design content); execution-track quest UI widgets and Godot quest journal serialization (execution-deferred / advisory on conceptual track); new **CanonRegistry** write paths (5.3 reads graph + proposes via existing `append_canon_fact` / **IntentResolver** gate only); DM workbench quest editor UX (Half A catalog / execution track); spell agency/perspective metadata (Phase 5.2 — 5.3 consumes priority conventions only).

## Behavior

### CanonGraphPressureIndex

Read-only index assembled from **CanonRegistry** and **LoreHookRegistry** at rule-evaluation time (or refreshed on `canon.fact_*` bus events per session policy):

```
CanonGraphPressureIndex:
  thread_nodes: []ThreadPressureNode
  entity_nodes: []EntityPressureNode
  location_nodes: []LocationPressureNode
  hook_edges: []HookPressureEdge
  snapshot_epoch: int              # aligns with RegistrySnapshot epoch when available
  index_build_policy: eager | lazy_on_trigger
```

**ThreadPressureNode:**

| Field | Semantics |
|---|---|
| `thread_id` | Canon thread / narrative arc identifier |
| `lifecycle_state` | Aggregated min lifecycle across member facts (`accepted` \| `hooked` \| `sim-active`) |
| `open_hook_count` | Count of `hooked` facts not yet `sim-active` |
| `stake_entity_ids` | Entities with unresolved stakes on this thread |
| `urgency_score` | Normalized 0–100 derived from hook age, player proximity signals, tone weights |
| `decay_class` | `stable` \| `cooling` \| `escalating` — feeds quest rule conditions |

**EntityPressureNode** and **LocationPressureNode** mirror thread semantics at finer granularity — entity reputation edges, faction rivalry tags, location occupation flags — sourced from **CanonRegistry** indexes (2.2) and Phase 3 off-screen activity ripples (advisory inputs, not hard blockers on conceptual track).

**HookPressureEdge** links a **LoreHookRegistry** record to pressure signals: `hook_id`, `source_fact_id`, `pressure_contribution`, `dangling` flag (2.2 orphan hook contract).

### QuestPressureSignal taxonomy

Named signal kinds emitted by **CanonGraphPressureIndex** evaluation and referenced by quest rule conditions:

| Signal kind | Source node field | Semantics |
|---|---|---|
| `thread_urgency` | `ThreadPressureNode.urgency_score` | Normalized 0–100 urgency on narrative thread |
| `entity_stake` | `EntityPressureNode.stake_entity_ids` + urgency | Unresolved entity stake on scoped threads |
| `location_tension` | `LocationPressureNode.urgency_score` | Location occupation / rivalry tension |
| `hook_decay` | `ThreadPressureNode.decay_class` | `stable` \| `cooling` \| `escalating` lifecycle pressure |

**QuestPressureSignal** values are read-only projections — rules consume them via `pressure_above` and `thread_decay_is` condition atoms; no separate mutable signal store.

### QuestPressureManifest

Each quest-pressure ruleset declares a manifest attached to its **QuestPressureRulePlugin**:

```
QuestPressureManifest:
  quest_pressure_id: string
  thread_scope: string | []string     # thread_ids monitored
  entity_scope: []entity_ref | null
  location_scope: []location_ref | null
  pressure_threshold: int             # urgency_score floor to fire rules
  rule_trigger_class: string         # e.g. quest_pressure_tick, canon_hook_promoted, thread_stake_changed
  effect_bus_channels: []string        # subset: quest_pressure, world_event, canon_proposal, tone_bias
  priority_hint: int                 # feeds RuleConflictArbiter (see Priority bands)
  veto_classes: []string
  spell_interaction_policy: defer_to_spell | co_fire | quest_wins_on_tie
```

**spell_interaction_policy** governs same-frame conflicts with **SpellAgencyPerspectiveManifest** (5.2) effects — default **`defer_to_spell`** for `agency_transition` / `perspective_transition` channels; quest effects on `world_event` / `canon_proposal` / `tone_bias` may **co_fire** unless arbiter veto applies.

### Quest pressure evaluation loop

1. **Trigger** arrives (`quest_pressure_tick` at **SimTickPipeline** boundary, or `canon_hook_promoted` on **CanonRegistry** bus event, or `thread_stake_changed` from Phase 3 ripple)
2. **RuleEngineCore** builds **RuleContextFrame** with `canon_read_handle` + **`quest_pressure_snapshot`** (selected index slice for manifest scopes)
3. **QuestPressureRegistry** lookup by `quest_pressure_id` for active plugins
4. Condition atoms evaluate: `canon_has`, `state_is`, `tone_weight_above`, plus quest-specific **`pressure_above`** (manifest threshold vs index urgency) and **`thread_decay_is`** (decay_class match)
5. Effect set dispatches via **RuleEffectBus**:
   - **`quest_pressure`** channel — posts structured pressure deltas to **WorldEventLog** and optional quest-journal adapter seam (execution-deferred)
   - **`world_event`** — narrative ripple entries for player-visible continuity (PMG world continuity goal)
   - **`canon_proposal`** — proposes follow-on **CanonFact** when pressure resolves a thread stake (routes through **IntentResolver** — no direct registry write)
   - **`tone_bias`** — optional urgency bias on **ToneProfileConsequenceWeights** (3.1) per campaign tone profile
6. **RuleConflictArbiter** resolves conflicts with spell plugins per priority bands below

### RuleEffectBus quest_pressure channel

New effect class registered on **RuleEffectBus** (5.1 extension, owned by 5.3 contract):

| Sub-route | Target | Semantics |
|---|---|---|
| `pressure_delta` | Quest journal adapter seam | Increment/decrement visible urgency on thread/entity (execution-deferred presentation) |
| `stake_surface` | **WorldEventLog** | Record stake change for chronicle / between-session continuity |
| `hook_nudge` | **HookMaterializer** advisory queue | Suggest hook promotion candidate — DM/table accept still required (2.2 lifecycle) |
| `cross_channel_hint` | **RuleEffectBus** internal | When `spell_interaction_policy` allows, hint `agency_transition` or `perspective_transition` — never bypasses 5.2 manifest gates |

**DMPauseGate** (3.1) holds `world_delta` only; `quest_pressure` and `world_event` sub-routes proceed unless **NarrativeDeltaVetoPolicy** (3.3) active on the affected thread.

### Priority bands (quest vs spell)

Extends 5.2 **RuleConflictArbiter** integration. Plugins declare `priority_hint` in manifest; **PluginHookManifest.priority** is authoritative at load. **Mapping note:** Phase 5.2 pre-band examples (e.g. dominate `priority_hint` 20–40) are **superseded** by this band table — spell plugins map to **100–199** with dominate typically at `priority_hint` 120–140 per [[Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]] cross-ref.

| Band | Priority range (lower = higher precedence) | Owner | Notes |
|---|---|---|---|
| **Safety / veto** | 0–99 | Core + table policy plugins | Veto pass always runs first (5.1) |
| **Spell agency/perspective** | 100–199 | Spell plugins (5.2) | `agency_transition`, `perspective_transition` |
| **Quest pressure core** | 200–299 | Quest plugins (5.3) | `quest_pressure`, `canon_proposal` on thread scope |
| **Ambient tone / world** | 300–399 | Tone + ambient rules | `tone_bias`, low-urgency `world_event` |
| **Deferred / background** | 400+ | Off-screen sim ripples | May be vetoed by higher bands |

**Same-frame spell + quest on same entity:** Arbiter applies 5.2 serialize rule (agency first, perspective second) then quest `world_event` / `quest_pressure` unless spell manifest `veto_classes` includes `quest_pressure`. Default: spell agency wins; quest logs `quest_pressure_deferred` to **WorldEventLog** for next tick.

**OQ-5.1-003 resolution (conceptual):** Static per-plugin `priority` remains default; 5.3 documents **priority bands** as convention for community quest modules — DM runtime priority stack override remains execution-deferred / Half A catalog seam.

### SeamRegistry integration

**QuestPressureRulePlugin** registers via **SeamRegistry** `rule` family (1.3) — same contract as **RulesetPlugin** (5.1):

- `declare_hooks()` returns **PluginHookManifest** with quest trigger classes
- `required_condition_atoms` may extend with `pressure_above`, `thread_decay_is` (registered as **RulePrimitive** extensions on quest seam)
- `required_effect_atoms` includes `quest_pressure` effect atom
- **PluginLoader** validates atoms at session init; duplicate `quest_pressure_id` rejected (first registered wins)

## Interfaces

**Imports from Phase 5.1 (RulePrimitive extensions):**

| Extension | Kind | Semantics |
|---|---|---|
| `pressure_above` | condition atom | `quest_pressure_snapshot` urgency ≥ manifest `pressure_threshold` |
| `thread_decay_is` | condition atom | `decay_class` matches manifest filter |
| `quest_pressure` | effect atom | Dispatches via **RuleEffectBus** `quest_pressure` channel |

Trigger class extensions (merged into session trigger registry per 5.2 OQ-5.2-005 pattern):

- `quest_pressure_tick`
- `canon_hook_promoted`
- `thread_stake_changed`
- `quest_resolution_complete`

**Imports from Phase 5 siblings:**

| Source | How 5.3 consumes it |
|---|---|
| **RuleEngineCore** + **RulePrimitive** library | Quest rules use same condition/effect evaluation loop |
| **RuleEffectBus** | Extends with `quest_pressure` channel; shares async dispatch + **DMPauseGate** hold rules |
| **RuleContextFrame** | Extended with `quest_pressure_snapshot` on quest triggers |
| **RuleConflictArbiter** | Priority bands + spell_interaction_policy |
| **SeamRegistry** `rule` family | Plugin registration seam |
| **SpellMetadataRegistry** (5.2) | Optional cross-reference when quest rules react to spell side-effects |
| **LiminalPresentationPolicy** (5.2) | Quest narrative overrides may reference policy ids for liminal quest states |

**Imports from Phase 2–3:**

| Source | How 5.3 consumes it |
|---|---|
| **CanonRegistry** + **CanonFact** lifecycle (2.2) | **CanonGraphPressureIndex** source; `canon_has` conditions; read-only handles |
| **LoreHookRegistry** (2.2) | Hook edges, dangling hook policy |
| **IntentResolver** (2.2) | `canon_proposal` effect routing — no direct registry mutation |
| **ToneProfileBundle** (2.3) | `tone_weight_above` conditions; urgency bias keys |
| **SimTickPipeline** + **WorldEventLog** (3.1) | `quest_pressure_tick` trigger; ripple logging |
| **OffScreenActivityWindow** (3.2) | Advisory stake signals into entity pressure nodes |
| **NarrativeDeltaVetoPolicy** (3.3) | May block quest pressure effects on vetoed threads |

**Exports to Phase 6 and execution track:**

| Export | Consumer |
|---|---|
| **QuestPressureManifest** + **QuestPressureRegistry** | Community quest modules; Half A catalog rows |
| **CanonGraphPressureIndex** contract | Execution mirror; sim-active hook consumers |
| **Priority band table** | Spell + quest plugin authoring guidelines |
| **RuleEffectBus** `quest_pressure` channel | Godot quest journal adapter (execution-deferred) |

## Edge cases

| Case | Handling |
|---|---|
| Thread urgency drops below threshold mid-tick | Rule body does not fire; `quest_pressure_cooled` optional **WorldEventLog** entry when decay_class = `cooling` |
| Conflicting quest plugins same `thread_scope` | **RuleConflictArbiter** priority pass; lower priority number wins; overflow guard per 5.1 |
| Spell dominate + quest stake change same entity | Spell `agency_transition` wins per band table; quest `stake_surface` deferred to next tick unless `spell_interaction_policy: quest_wins_on_tie` |
| `hook_nudge` on dangling hook (2.2) | Skipped; log `hook_nudge_skipped_dangling` |
| Canon fact demoted / rejected after pressure fired | Next index rebuild reflects lower urgency; no retroactive effect rollback — chronicle notes correction via `world_event` |
| Empty graph at session start | Valid — quest plugins with `pressure_above` conditions simply do not fire until hooks materialize |
| DM pause during quest_pressure_tick | **DMPauseGate** holds world_delta only; quest_pressure channel proceeds unless narrative veto |

## Open questions

| ID | Question | Conceptual authority decision |
|---|---|---|
| OQ-5.3-001 | **CanonGraphPressureIndex** rebuild: per-tick full vs incremental on `canon.fact_*` events? | **Incremental lean**: rebuild affected thread/entity slices on bus events; full rebuild at session boundary — execution track tunes performance |
| OQ-5.3-002 | Player proximity signal source for urgency_score? | **Advisory composite**: UnifiedSceneGraph distance + off-screen faction activity (3.2) — weight table execution-deferred; conceptual safety: `pressure_above` conditions clamp to index `urgency_score` 0–100 only — no unbounded threshold bypass |
| OQ-5.3-003 | Quest-pressure plugin coexists with procedural fetch-loop antipattern? | **Explicit non-goal**: manifests must declare `thread_scope` tied to canon graph — generic kill-10-rats templates rejected at **PluginLoader** schema validation (execution track) |
| OQ-5.3-004 | Cross-session quest pressure persistence? | **AgencyPersistenceLedger** pattern (4.3) analogous export hook for active pressure states — serialization execution-deferred |
| OQ-5.3-005 | DM override of priority band for narrative fiat? | **Out of scope conceptual** — table may veto outcomes via **NarrativeDeltaVetoPolicy** (3.3); runtime priority stack flagged for Half A extensibility seam |

## Pseudo-code readiness

A reader can trace `hooked` fact promotion → **CanonGraphPressureIndex** urgency update → `quest_pressure_tick` trigger → **QuestPressureRegistry** lookup → `pressure_above` condition → **RuleEffectBus** `quest_pressure` + `world_event` dispatch → optional `canon_proposal` through **IntentResolver** — and same-frame spell interaction deferral via priority bands — without inventing direct **CanonRegistry** writes or illegal **PerspectiveEnvelope** victim modes. No API signatures on conceptual track.

## Responsibilities

- [x] Name QuestPressureManifest, QuestPressureRegistry, CanonGraphPressureIndex, QuestPressureRulePlugin
- [x] Document **RuleEffectBus** `quest_pressure` channel and trigger class extensions
- [x] Wire **SeamRegistry** / **RuleEngineCore** quest plugin pattern
- [x] Declare priority bands integrating 5.2 spell metadata conventions
- [x] Anchor pressure sources to **CanonRegistry** graph + **LoreHookRegistry** hooks per PMG canon pipeline

## Tasks

- [x] Mint 5.3 secondary with quest pressure from canon graph
- [ ] Optional tertiaries: per-thread pressure curve detail, chronicle surfacing policy, registry serialization — deferred breadth-first
- [x] Phase 5 conceptual breadth secondaries complete (5.1–5.3)

## Consistency reports

> [!note]
> Post-mint: execution rollup gates, REGISTRY-CI, and HR closure artifacts are execution-deferred / advisory on conceptual track per conceptual_v1 contract.

Minted 2026-06-26 (godo-followup-20260626T214200Z-phase5-deepen-5-3); Phase 5 conceptual breadth secondaries complete (5.1–5.3); persona: half_a.conceptual_architect; product_factory_run_id: f35ff65cfb4f; pre_create_gate: skipped_conceptual_track; execution_gaps_advisory: true.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-3-Quest-Pressure-from-Canon-Graph"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
