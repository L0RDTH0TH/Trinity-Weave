---
title: Phase 6.2.5 — RuleCheckProbe Rule Check (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: 6.2.5
project-id: genesis-mythos-master
status: active
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- horizon-demo
- rule-check
- beat-5
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]'
body_compact_source_queue: followup-deepen-phase625-tertiary-20260716T054400Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.2.5 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-16 (`followup-deepen-phase625-tertiary-20260716T054400Z`).

## Archived body (pre-compact)

## Phase 6.2.5 — RuleCheckProbe Rule Check

Decomposes **beat 5 (Rule check)** of the eight-beat horizon demo loop from parent [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **RuleCheckProbe** builds a post-tick **RuleContextFrame** stub from **WorldEventLog** row `demo_interact_observed`, loads the **demo_ruleset** plugin manifest, runs **one** **RuleEngineCore** evaluation pass, and emits `rule.demo_pass` or `rule.demo_fail` on **RuleEffectBus** as the beat 5 exit gate. Nouns and ordering only — no full **RulesetPlugin** loader, no spell/quest priority bands, no Godot rule DSL.

> **Parent boundary:** This slice begins after `demo.sim_tick_committed` from [[Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]] with **WorldEventLog** row `demo_interact_observed` present. It completes beat 5 of the **DemoLoopOrchestrator** stage machine; beat 6 (**DMCamTransitionSlot**) awaits operator DM rail hotkey or scripted cue per **HorizonDemoManifest** `strict_ordering: true`.

## Scope

**In scope:** **RuleCheckProbe** lifecycle (awaiting_context → frame_built → evaluating → pass | fail | blocked); beat 5 entry gate on `demo.sim_tick_committed` plus **WorldEventLog** `demo_interact_observed`; post-tick **RuleContextFrame** stub assembly (5.1 authority — demo-truncated field set); **demo_ruleset** plugin manifest (one condition + one effect); **RuleEngineCore** single evaluation pass; **RuleEffectBus** emission of `rule.demo_pass` or `rule.demo_fail`; optional `presentation.rule_outcome` echo for **PlayerFeedbackChannel** (beat 8 precursor — execution wiring); **HorizonDemoManifest** `continue_on_rule_fail: false` default — loop halts at stage 5 on fail unless operator enables `demo.continue_on_rule_fail` (execution debug only); **DemoLoopOrchestrator** beat 5 entry/exit gates; demo priority band placeholder 50–99 (below spell 100–199 and quest 200–299 per 5.2/5.3).

**Out of scope:** **SpawnBootstrapController**, **FPExploreRigHost**, **IntentPipelineStub**, **SimTickStub** (beats 1–4); **DMCamTransitionSlot**, **OverwriteDemonstrationSlot**, **PlayerFeedbackChannel** (beats 6–8); full **PluginLoader** session-boundary hot-swap (5.1); **RuleConflictArbiter** multi-plugin merge (single plugin in v1); **CanonRegistry** read/write beyond stub no-op handle; spell/quest **RulesetPlugin** instances (5.2/5.3); factory catalog attestation (6.1); execution-track Godot rule evaluator, C# **RulePrimitive** types, or HR rollup gates.

## Behavior

**Actors:** **RuleCheckProbe** (beat 5 owner), **RuleEngineCore** (5.1 — single-pass evaluation), **RuleContextFrameBuilder** (5.1 — demo stub assembly), **demo_ruleset** **RulesetPlugin** stub (5.1 — one rule triple), **RuleEffectBus** (5.1 — effect routing), **WorldEventLogReader** (3.1 — condition input), **DemoLoopOrchestrator** (stage gate machine), **SimTickStub** (6.2.4 — upstream log producer).

**Ordering:** DemoLoopOrchestrator opens beat 5 gate on `demo.sim_tick_committed` → **RuleCheckProbe** validates **WorldEventLog** `demo_interact_observed` → build **RuleContextFrame** stub → load **demo_ruleset** → **RuleEngineCore** evaluates → **RuleEffectBus** emits `rule.demo_pass` or `rule.demo_fail` → DemoLoopOrchestrator advances to beat 6 or halts per **continue_on_rule_fail**.

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| awaiting_context | DemoLoopOrchestrator beat 5 gate open | frame_built when `demo.sim_tick_committed` + log row present | blocked if log row missing |
| frame_built | awaiting_context exit | evaluating when **RuleContextFrame** stub assembled | blocked if frame assembly fails |
| evaluating | frame_built exit | pass or fail when **RuleEngineCore** completes | blocked if plugin manifest invalid |
| pass | condition satisfied | DemoLoopOrchestrator stage 5 → 6 eligible; emit `rule.demo_pass` | — |
| fail | condition not satisfied | loop halt at stage 5 (v1 default); emit `rule.demo_fail` | — |
| blocked | precondition or evaluation failure | terminal for beat 5; DemoLoopOrchestrator holds | |

### RuleContextFrame stub (demo-truncated)

Per OQ-6.2.5-001 and parent 6.2 **RuleCheckProbe** section — minimal field set for v1:

| Field | Demo v1 value | Authority |
|---|---|---|
| `actor_entity_id` | player avatar stub id from 6.2.1 spawn | **UnifiedSceneGraph** (4.1 — stub) |
| `scene_context` | `demo_shrine_v1` facet id | Aligns with 6.2.1 stub world |
| `trigger_class` | `tick_phase_end` (post-sim-tick) | 5.1 trigger enum |
| `world_state_snapshot` | read-only stub after stand-in tick | 6.2.4 post-tick state |
| `canon_read_handle` | no-op read stub — no **CanonFact** proposals | 2.2 deferred |
| `agency_envelope_snapshot` | player agency default from 4.3 | FP explore beat |
| `perspective_envelope_snapshot` | `player_fp` from 6.2.2 | 4.1 |
| `tone_weights` | default bundle stub — no bias application | 2.3 deferred |
| `active_plugin_ids` | `["demo_ruleset"]` only | 5.1 |
| `event_log_refs` | `[demo_interact_observed]` | 6.2.4 **WorldEventLog** row |

Full **RuleContextFrame** field population remains **execution-deferred**; demo stub proves condition evaluation seam only.

### demo_ruleset plugin manifest

Conceptual single-rule triple per parent 6.2:

| Component | Demo v1 contract |
|---|---|
| Plugin id | `demo_ruleset` |
| Priority band | 50–99 (demo rules — below spell/quest per 5.2/5.3) |
| Condition | `state_is` primitive: event log contains `demo_interact_observed` (or equivalent **RulePrimitive** `trigger_event` read) |
| Effect (pass) | `trigger_event` → **RuleEffectBus** channel `rule.demo_pass`; optional `grant_demo_boon` stub effect to `presentation.*` (no canon mutation) |
| Effect (fail) | **RuleEffectBus** channel `rule.demo_fail` when condition not met |
| Trigger | `tick_phase_end` after sim stub commit |

**Teachable fail path:** Per OQ-6.2-002 and parent **HorizonDemoManifest**, rule may fail when condition unsatisfied (e.g. log row absent due to race — execution only). v1 default: loop **halts** at stage 5; operator may enable `demo.continue_on_rule_fail` for kiosk teaching builds (execution debug only).

### RuleEngineCore evaluation pass

- **Exactly one** evaluation pass per demo loop session — triggered by beat 5 gate, not by frame loop.
- **No** **RuleConflictArbiter** invocation — single plugin, single rule.
- Effects route through **RuleEffectBus** only — **does not** mutate **CanonRegistry** or apply **WorldStateCommitter** deltas beyond stub no-op.
- Pass/fail outcome published for **PlayerFeedbackChannel** (beat 8) and operator telemetry.

### `rule.demo_pass` / `rule.demo_fail` gates

Emitted on **RuleEffectBus** **once** when evaluation completes:

1. `demo.sim_tick_committed` already observed (beat 4 complete).
2. **WorldEventLog** row `demo_interact_observed` present.
3. **RuleEngineCore** evaluation finished.

On **pass:** **DemoLoopOrchestrator** records beat 5 progress; beat 6 (**DMCamTransitionSlot**) may open on operator DM hotkey per OQ-6.2-003 — rule pass is **not** auto-trigger for DM cam in v1 default.

On **fail:** **DemoLoopOrchestrator** holds at stage 5; `demo.stage_failed` with stage id `rule_check` unless `demo.continue_on_rule_fail` enabled.

### `demo.rule_check_complete` gate

Emitted on `session.*` **once** when evaluation completes (pass or fail):

1. **RuleEngineCore** evaluation finished.
2. **RuleEffectBus** has emitted `rule.demo_pass` or `rule.demo_fail`.

> **IRA annotation (GAP-5 — bus namespace convention):** `demo.rule_check_complete` routes through `session.*` **by DemoLoopOrchestrator convention** (same as `demo.spawn_complete`, `demo.fp_active`, `demo.intent_labeled`, `demo.sim_tick_committed`). Outcome detail (`rule.demo_pass` / `rule.demo_fail`) remains on **RuleEffectBus** per 5.1 authority — **DemoLoopOrchestrator** stage progress for beat 5→6 uses `demo.rule_check_complete` on `session.*`; **PlayerFeedbackChannel** and rule consumers subscribe to **RuleEffectBus** channels. Precedent: OQ-6.2.3-003, OQ-6.2.4-003 bus split.

### Beat 5 → beat 6 handoff

- **Default exit (pass):** `rule.demo_pass` → operator may invoke DM rail hotkey; **DMCamTransitionSlot** validates `play_region_mounted`, `demo_fp_active` guards per parent 6.2.
- **Fail exit:** loop halt — no DM cam until operator reset or debug flag.
- Beat 6 must **not** open before beat 5 evaluation completes under `strict_ordering: true`.

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.2.5 consumes it |
|---|---|
| `demo.sim_tick_committed` on `session.*` (6.2.4) | Beat 5 entry gate |
| **WorldEventLog** row `demo_interact_observed` (6.2.4) | Condition input |
| **RuleEngineCore** + **RuleContextFrame** (5.1) | Evaluation pass |
| **RuleEffectBus** (5.1) | Pass/fail emission |
| **RulePrimitive** `state_is` / `trigger_event` (5.1) | Condition atoms |

**Exports to downstream beats:**

| Export | Consumer |
|---|---|
| `rule.demo_pass` or `rule.demo_fail` on **RuleEffectBus** | **PlayerFeedbackChannel** (beat 8); rule outcome consumers |
| `demo.rule_check_complete` on `session.*` | **DemoLoopOrchestrator** progress (beat 5→6 eligibility) |
| Rule outcome stub | Operator telemetry; optional toast precursor |
| Post-rule session state | Beat 6 **DMCamTransitionSlot** guard inputs |

**Explicit non-import:** **PluginLoader** hot-swap, **RuleConflictArbiter**, spell/quest plugins (5.2/5.3), **CanonRegistry** writes, full **ToneProfileConsequenceWeights** application.

## Edge Cases

| Case | Handling |
|---|---|
| `demo.sim_tick_committed` never arrives | **RuleCheckProbe** stays `awaiting_context`; DemoLoopOrchestrator holds at beat 5 |
| Log row missing after sim commit (race) | Evaluation yields **fail**; `rule.demo_fail`; loop halts per v1 default |
| Double evaluation in same session | **DemoLoopOrchestrator** rejects duplicate — one pass per loop |
| Operator triggers DM cam before rule check | Rejected per `strict_ordering: true` — toast via **PlayerFeedbackChannel** (execution wiring) |
| Rule pass but operator never triggers DM cam | Valid terminal pause — loop complete only after beat 8; beat 6 optional until hotkey |
| `demo.continue_on_rule_fail` enabled | Loop may advance to beat 6 despite fail — execution debug only |

## Open Questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.2.5-001 | **RuleContextFrame** full fields vs demo stub subset? | **Demo stub subset** for v1 — full frame assembly execution-deferred |
| OQ-6.2.5-002 | Pass effect: silent vs `grant_demo_boon` presentation echo? | **Emit `rule.demo_pass` + optional presentation stub** — boon is cosmetic, no canon mutation |
| OQ-6.2.5-003 | Fail path: always halt vs teachable continue? | **Halt at stage 5 default** — aligns with parent OQ-6.2-002; `demo.continue_on_rule_fail` execution debug only |

## Pseudo-code readiness

Reader can sketch **RuleCheckProbe** state machine (awaiting_context → frame_built → evaluating → pass | fail | blocked), **demo_ruleset** single-rule manifest, **RuleContextFrame** stub field table, and beat 5/6 handoff without guessing full **RuleEngineCore** plugin loader APIs. Execution track owns typed rule interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.2.5 tertiary — RuleCheckProbe rule check (depth-first backfill; beat 5 of 8-beat demo loop)
- [x] Depth-first continue → 6.2.6 DMCamTransitionSlot (beat 6) — minted [[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]

