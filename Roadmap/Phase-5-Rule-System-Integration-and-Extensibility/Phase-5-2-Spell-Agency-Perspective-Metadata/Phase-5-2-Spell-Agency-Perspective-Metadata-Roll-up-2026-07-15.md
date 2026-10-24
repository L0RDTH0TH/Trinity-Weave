---
title: Phase 5.2 — Spell Agency and Perspective Metadata (Roll-up)
roadmap-level: rollup
phase-number: 5
subphase-index: '5.2'
project-id: genesis-mythos-master
status: complete
priority: high
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-5
- spell-metadata
- agency
- perspective
- rollup
para-type: Project
roadmap_track: conceptual
rollup_of: '[[Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
links:
- '[[Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
- '[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[genesis-mythos-master-goal]]'
body_compact_source_queue: followup-deepen-phase52-20260715T234512Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 5.2 — Roll-up detail (factory feed-gate compact)

Canonical NL detail preserved from secondary body compact 2026-07-15 (queue followup-deepen-phase52-20260715T234512Z). Secondary keeps nouns + scope; this note holds tables, bindings, policies, edge cases, open questions, tasks, dataview.

## Phase 5.2 — Spell Agency and Perspective Metadata

Spell-bound declarations that route dominate / victim presentation through **RuleEffectBus** into **AgencyEnvelope** (4.3) and **PerspectiveEnvelope** (4.1) without inventing new legal perspective modes. This slice owns **SpellAgencyPerspectiveManifest** — the metadata contract spells attach to rule plugins — plus **LiminalPresentationPolicy** for victim UX during dominate spells.

## Scope

**In scope:** **SpellAgencyPerspectiveManifest** (per-spell metadata block); **SpellMetadataRegistry** (lookup by `spell_id` at rule evaluation); **DominateSpellBinding** (dominator → `pilot_fp` via **PilotGraph** / **AgencyEnvelope**); **VictimPassengerOverlayBinding** (victim → `passenger_fp_overlay` hook on **AgencyEnvelope** — reserved slot, not a **PerspectiveEnvelope** mode); **LiminalPresentationPolicy** (locked input, liminal UI chrome, audio ducking hints per PMG victim policy); **RuleContextFrame.spell_metadata** extension when trigger class is spell-bound; **RulesetPlugin** spell plugin pattern (registers spell rules + manifest); **RuleEffectBus** `agency_transition` and `perspective_transition` channel wiring for spell-fired effects; integration with **RuleConflictArbiter** priority for spell vs quest effects (quest detail in 5.3).

**Out of scope:** Quest-pressure canon graph integration (Phase 5.3); execution-track typed spell DSL serialization and Godot UI widgets (execution-deferred / advisory on conceptual track); new **PerspectiveEnvelope** legal modes for victim POV (explicitly forbidden — overlay only); dominate session persistence format (4.3 **AgencyPersistenceLedger** — 5.2 consumes export hook only); individual spell balance tables and damage primitives (game design content, not architecture).

## Behavior

### SpellAgencyPerspectiveManifest

Each spell that affects agency or perspective declares a manifest block attached to its **RulesetPlugin**:

```
SpellAgencyPerspectiveManifest:
  spell_id: string                    # globally unique, matches plugin rule scope
  agency_profile: AgencyProfile       # dominate / none / proxy_hint
  perspective_profile: PerspectiveProfile
  liminal_policy_id: string | null    # references LiminalPresentationPolicy row
  rule_trigger_class: string          # e.g. spell_cast_complete, spell_tick_sustain
  effect_bus_channels: []string        # subset: agency_transition, perspective_transition
  priority_hint: int                  # feeds RuleConflictArbiter via plugin priority
  veto_classes: []string              # optional spell-level veto declarations
```

**AgencyProfile:**

| Field | Values | Semantics |
|---|---|---|
| `agency_class_request` | `dominate` \| `none` \| `absent_proxy_hint` | Requested **PilotGraph** transition class |
| `dominator_binding` | DominateSpellBinding \| null | Present when `agency_class_request = dominate` |
| `victim_binding` | VictimPassengerOverlayBinding \| null | Present when spell imposes victim overlay |
| `handoff_choreography` | `standard` \| `snap` \| `deferred_until_blend` | Passed to **PilotHandoffCoordinator** (4.3) |

**PerspectiveProfile:**

| Field | Values | Semantics |
|---|---|---|
| `perspective_request` | `retain_current` \| `dm_world_observe` \| `none` | Legal **PerspectiveEnvelope** mode requests only |
| `victim_overlay_only` | bool | When true, victim path uses **passenger_fp_overlay** — never `override_perspective` to a new envelope mode |
| `camera_interpolator_hint` | string \| null | Suggested **CameraInterpolatorRegistry** id for dominate entry/exit |

### DominateSpellBinding (dominator branch)

When a dominate spell resolves successfully:

1. **RuleEngineCore** evaluates spell rule; **RuleContextFrame** carries `spell_metadata` snapshot
2. Effect `modify_agency` routes via **RuleEffectBus** → `agency_transition` channel
3. **AgencyEnvelope** receives transition request: `{agency_class: dominate, target_entity_id, source_spell_id}`
4. **PilotMachineryGlue** (4.3) stages **PilotHandoffCoordinator**: `idle` → `dominate_pending` → `dominate_active`
5. **DominateSessionBinding** records `{target_entity_id, source_rig_id, envelope_snapshot, spell_id}` — dominator experiences **pilot_fp** (possessed target envelope) via **PilotGraph** `dominate` state
6. **InputIntent** router retargets to possessed entity per 4.1/4.3 contract
7. DM observation rails (**WorldCam**, etc.) remain legal — dominate does not block DM rigs (4.2/4.3)

**Dominate spell release:** Spell duration end, dispel, or **NarrativeDeltaVetoPolicy** (3.3) fires `modify_agency` effect with payload `{agency_class: release_dominate, target_entity_id, source_spell_id}` → **RuleEffectBus** `agency_transition` channel → **PilotHandoffCoordinator** state transition `dominate_active` → `dominate_release` (4.3 handoff state machine label — **not** a **RulePrimitive** effect atom) → **DominateSessionBinding** cleared → **PilotGraph** returns `self` or edge-specified mode.

### VictimPassengerOverlayBinding (victim branch)

Victim presentation during dominate spells uses the **AgencyEnvelope** reserved hook — **not** a **PerspectiveEnvelope** legal mode:

```
VictimPassengerOverlayBinding:
  overlay_hook: passenger_fp_overlay    # AgencyEnvelope reserved slot (4.3)
  victim_entity_id: entity_ref
  dominator_spell_id: string
  input_lock_class: full | partial | narrative_only
  liminal_policy_id: string
  presentation_shell_hint: liminal_victim_shell
```

**Routing rules:**

| Concern | Authority | 5.2 contract |
|---|---|---|
| Victim camera / sensory presentation | `passenger_fp_overlay` hook | Overlay compositor on **PresentationShell** — outside **PerspectiveEnvelope** mode table |
| Victim **InputIntent** | **LiminalPresentationPolicy** | Locked or narrative-only per PMG victim policy |
| Victim sim agency | Simulation / narrative | No **InputIntent** write from victim overlay — read-only or vetoed intents |
| Perspective mode enum | **PerspectiveEnvelope** (4.1) | **No** `player_fp` or `dm_*` mode switch for victim — overlay only |

### AbsentProxyHintSpellBinding (proxy-hint branch)

When `agency_class_request = absent_proxy_hint` (no dominate binding):

1. Spell rule evaluates; **RuleContextFrame** carries `spell_metadata` with `dominator_binding: null`
2. Effect `modify_agency` routes via **RuleEffectBus** → `agency_transition` with payload `{agency_class: absent_proxy_hint, target_entity_id, source_spell_id}`
3. **PilotMachineryGlue** (4.3) consults **AbsentProxyPolicyTable** — installs or refreshes absent-proxy session per D-4.3-002 static policy + DM token override
4. No **DominateSessionBinding** created; no **LiminalPresentationPolicy** row unless manifest also sets `victim_binding` (orthogonal paths)
5. Concurrent dominate spell: edge case table applies — dominate queues or rejects with `presentation.agency_busy` (4.3 single-flight)

Proxy-hint spells do **not** use **PilotHandoffCoordinator** dominate state machine; they use the absent-proxy install path only. See OQ-5.2-005 for spell trigger enum registration seam.

### LiminalPresentationPolicy

Named policy rows referenced by `liminal_policy_id`:

| policy_id | input_lock_class | ui_chrome | audio_hint | release_trigger |
|---|---|---|---|---|
| `liminal_dominate_victim_default` | full | liminal_border + desaturate | duck_ambient_70 | dominate_release OR spell_end |
| `liminal_dominate_victim_narrative` | narrative_only | vignette + subtitle_channel | mute_foley | narrative_veto OR dominate_release |
| `liminal_dominate_victim_partial` | partial | action_prompts_disabled | duck_music_50 | player_escape_minigame OR dominate_release |

Policies are declarative hints to **PresentationShell** — execution track chooses widget implementation. Conceptual track locks **semantics** (locked input, liminal chrome) per PMG [[genesis-mythos-master-goal]] victim branch.

### RuleContextFrame extension

When `trigger_class` is spell-bound (`spell_cast_complete`, `spell_tick_sustain`, `spell_dispel`):

| Added field | Source |
|---|---|
| `spell_metadata` | **SpellMetadataRegistry** lookup by `spell_id` from triggering event |
| `spell_caster_entity_id` | Triggering actor |
| `spell_target_entity_id` | Primary target (dominate victim) |
| `active_dominate_binding` | Read-only snapshot from **DominateSessionBinding** if dominate active |

Nil spell context: fields omitted; spell-specific conditions (`spell_targets_self`, etc.) return false — no exception.

### RuleEffectBus channel wiring (spell path)

| Channel | Spell effect | Guard stack |
|---|---|---|
| `agency_transition` | Dominate start/release; proxy hints | **AgencyTransitionGuardExtension** (4.3) + **RuleConflictArbiter** |
| `perspective_transition` | Legal envelope switches only (e.g. caster shifts to `dm_world_observe` during channel) | **ModeTransitionGraph** (4.2) — **blocked** when `victim_overlay_only: true` on manifest |

**Spell vs core rule priority:** Spell plugins declare `priority_hint` in manifest; merged into **PluginHookManifest.priority**. Spell agency/perspective plugins occupy **priority band 100–199** per [[Phase-5-3-Quest-Pressure-from-Canon-Graph-Roadmap-2026-06-26-2142]] band table — dominate spell effects typically `priority_hint` **120–140** (above ambient world rules 300+, below narrative veto / safety band 0–99). Pre-band numeric examples (20–40) retired in favor of band table. **RuleConflictArbiter** single-target rule: one `modify_agency` per entity per frame after veto pass.

### RulesetPlugin spell pattern

```
SpellRulesetPlugin extends RulesetPlugin:
  spell_manifests: []SpellAgencyPerspectiveManifest
  declare_hooks() → PluginHookManifest with:
    rules: spell condition/effect triples
    required_effect_atoms: [modify_agency, override_perspective]  # as needed
    tone_bias_subscriptions: []  # optional per-spell tone keys
```

Spell plugins register in **SeamRegistry** `rule` family alongside core rulesets (5.1). **PluginLoader** validates manifest atoms against **RulePrimitive** library.

## Interfaces

**Imports from Phase 5.1:**

| 5.1 export | How 5.2 consumes it |
|---|---|
| **RuleEngineCore** + **RulePrimitive** | Spell rules use same condition/effect atoms |
| **RuleEngineCore** `trigger_class` enum | 5.2 extends 5.1 base triggers with `spell_cast_complete`, `spell_tick_sustain`, `spell_dispel` — registered via **PluginHookManifest.trigger_classes** extension (see OQ-5.2-005) |
| **RuleEffectBus** `agency_transition` / `perspective_transition` | Primary dispatch path for spell agency/perspective effects |
| **RuleContextFrame** | Extended with `spell_metadata` on spell triggers |
| **RuleConflictArbiter** | Spell plugin priority + veto integration |

**Imports from Phase 4:**

| Phase export | How 5.2 consumes it |
|---|---|
| **PilotGraph** + **AgencyEnvelope** (4.3) | Dominate binding, `passenger_fp_overlay` hook, handoff choreography |
| **DominateSessionBinding** (4.3) | Base tuple `{target_entity_id, source_rig_id, envelope_snapshot}` — **5.2 extends** with `spell_id` for spell provenance (4.3 base unchanged; extension declared here) |
| **PilotHandoffCoordinator** (4.3) | Dominate pending/active/release state machine (`dominate_release` = handoff state label, not RulePrimitive) |
| **PerspectiveEnvelope** (4.1) | Legal mode requests only; victim overlay explicitly outside envelope |
| **PresentationShell** (4.1) | Liminal overlay compositor host |
| **ModeTransitionGraph** (4.2) | Gates `perspective_transition` for caster-only envelope switches |

**Exports to Phase 5.3:**

| Export | Consumer |
|---|---|
| **SpellMetadataRegistry** | Quest-pressure rules may reference spell side-effects |
| **RuleEffectBus** spell priority conventions | Quest plugins declare compatible priority bands |
| **LiminalPresentationPolicy** table | Quest narrative overrides may reference policy ids |

## Edge cases

| Case | Handling |
|---|---|
| Dominate spell on entity already dominated | **RuleConflictArbiter** priority pass; higher-priority spell wins; lower spell logs `agency_transition_rejected` to **WorldEventLog** |
| Victim overlay + caster perspective switch in same frame | Serialize: agency_transition first, then perspective_transition; victim overlay unaffected by caster envelope switch |
| Spell end while **PilotHandoffCoordinator** mid-transition | Defer spell release effect until `handoff_complete` guard passes (4.3) — queue effect on **RuleEffectBus** |
| `override_perspective` effect on victim entity | **Rejected at bus** when manifest `victim_overlay_only: true` — log `perspective_transition_blocked_overlay_active` |
| Concurrent spell plugins same `spell_id` | **PluginLoader** duplicate rejection (5.1) — first registered wins |
| DM pause during dominate spell tick | **DMPauseGate** (3.1) holds `world_delta` only; `agency_transition` proceeds unless narrative veto (3.3) active |
| Absent-proxy active + dominate spell cast | **PilotMachineryGlue** single-flight — dominate request queues or rejects with `presentation.agency_busy` (4.3) |

## Open questions

| ID | Question | Conceptual authority decision |
|---|---|---|
| OQ-5.2-001 | Spell manifest storage: embedded in plugin manifest vs central **SpellMetadataRegistry** file? | **Central registry lean**: plugins register manifests into registry at load; supports DM workbench browse without loading all rule bodies — execution track chooses serialization |
| OQ-5.2-002 | Partial input lock (`liminal_dominate_victim_partial`) — which intent classes remain? | **Deferred to execution track** with narrative design input; conceptual contract names `partial` class only |
| OQ-5.2-003 | Dominate spell stacking (multiple casters, one victim)? | **Single binding per victim entity** — second dominate rejected unless first released; arbiter logs conflict |
| OQ-5.2-004 | Tone bias on spell cast for dominate spells? | **Optional** `tone_bias_subscriptions` on spell plugin; dominate spells may subscribe `domination_weight` key — wiring detail execution-deferred |
| OQ-5.2-005 | Spell trigger enum registration: extend 5.1 core enum vs spell-plugin-local trigger namespace? | **5.1 enum extension lean**: `spell_cast_complete`, `spell_tick_sustain`, `spell_dispel` registered on **PluginHookManifest.trigger_classes** at plugin load; **RuleEngineCore** merges into session trigger registry — single authority for valid `trigger_class` values |

## Pseudo-code readiness

A reader can trace spell cast → **SpellMetadataRegistry** lookup → `modify_agency` dominate start with `{agency_class: dominate, ...}` → **PilotHandoffCoordinator** staging → victim `passenger_fp_overlay` + **LiminalPresentationPolicy** application → dominate release via `modify_agency` `{agency_class: release_dominate, ...}` → handoff `dominate_release` state → binding clear — without conflating **RulePrimitive** effect atoms with 4.3 handoff state labels or inventing illegal **PerspectiveEnvelope** victim modes. No API signatures on conceptual track.

## Responsibilities

- [x] Name SpellAgencyPerspectiveManifest, SpellMetadataRegistry, DominateSpellBinding, VictimPassengerOverlayBinding, LiminalPresentationPolicy
- [x] Document dominate start/release via `modify_agency` (not phantom `dominate_release` effect atom)
- [x] Document absent_proxy_hint spell path via **PilotMachineryGlue** / **AbsentProxyPolicyTable**
- [x] Declare 4.3 **DominateSessionBinding** `spell_id` extension and 5.1 spell trigger enum extension
- [x] Victim routing through `passenger_fp_overlay` hook only — no legal perspective mode for victim

## Tasks

- [x] Mint 5.2 secondary with spell agency/perspective metadata
- [ ] Optional tertiaries: per-spell manifest schema detail, liminal widget mapping, registry serialization — deferred breadth-first
- [x] Phase 5 breadth 2/3 complete — next deepen 5.3 quest pressure from canon graph

## Consistency reports

> [!note]
> Post-mint: execution rollup gates, REGISTRY-CI, and HR closure artifacts are execution-deferred / advisory on conceptual track per conceptual_v1 contract.

Minted 2026-06-26 (godo-followup-20260626T211500Z-phase5-deepen-5-2); breadth-first Phase 5 continue → 5.3 quest pressure from canon graph; persona: half_a.conceptual_architect; product_factory_run_id: f35ff65cfb4f; pre_create_gate: skipped_conceptual_track; execution_gaps_advisory: true; Phase 5 breadth 2/3 complete.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
