---
title: Phase 6.2.4 — SimTickStub Sim Stub (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: 6.2.4
project-id: genesis-mythos-master
status: active
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- horizon-demo
- sim-stub
- beat-4
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]'
body_compact_source_queue: followup-deepen-phase624-tertiary-20260716T051200Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.2.4 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-16 (`followup-deepen-phase624-tertiary-20260716T051200Z`).

## Archived body (pre-compact)

## Phase 6.2.4 — SimTickStub Sim Stub

Decomposes **beat 4 (Sim stub)** of the eight-beat horizon demo loop from parent [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **SimTickStub** observes `intent.demo_interact` on `input.*`, commits **one** stand-in **SimTickPipeline** tick, appends a minimal **WorldEventLog** row `demo_interact_observed`, and emits `demo.sim_tick_committed` as the beat 4 exit gate. Nouns and ordering only — no full **SimClock** catch-up, no **OffScreenActivityWindow**, no Godot `_process` wiring.

> **Parent boundary:** This slice begins after `demo.intent_labeled` from [[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]] with `intent.demo_interact` visible on `input.*`. It completes beat 4 of the **DemoLoopOrchestrator** stage machine; beat 5 (**RuleCheckProbe**) opens on `demo.sim_tick_committed` and builds **RuleContextFrame** stub internally from **WorldEventLog** `demo_interact_observed`.

## Scope

**In scope:** **SimTickStub** lifecycle (awaiting_intent → tick_pending → committing → committed | paused | blocked); beat 4 entry gate on `demo.intent_labeled` plus `intent.demo_interact` on `input.*`; single committed tick via **SimTickPipeline** stand-in (3.1 authority — stubbed subsystem depth); **WorldEventLog** append with event id `demo_interact_observed`; `demo.sim_tick_committed` emission on `session.*` after log append; **DMPauseGate** read-only respect — no tick commit while DM cam active (demo policy); optional `sim.tick_committed` echo on `sim.*` per 3.1 bus convention (informational — execution wiring); **DemoLoopOrchestrator** beat 4 entry/exit gates.

**Out of scope:** **SpawnBootstrapController**, **FPExploreRigHost**, **IntentPipelineStub** (beats 1–3); **RuleCheckProbe**, **DMCamTransitionSlot**, **OverwriteDemonstrationSlot**, **PlayerFeedbackChannel** (beats 5–8); full **SimTickPipeline** subsystem registry (weather, NPC agendas, faction graph — 3.1 full depth); **ConsequenceResolver** merge of multiple **TickDelta** proposals; **OffScreenActivityWindow** and faction deltas (3.2); **ToneProfileConsequenceWeights** application beyond stub no-op delta; factory catalog attestation (6.1); execution-track Godot sim loop, C# tick types, or **CommittedTickRecord** serialization.

## Behavior

**Actors:** **SimTickStub** (beat 4 owner), **SimTickPipeline** stand-in (3.1 — single-tick commit path only), **WorldEventLogAppender** (3.1 — append contract), **DMPauseGate** (3.1 — read-only pause check), **DemoLoopOrchestrator** (stage gate machine), **IntentPipelineStub** (6.2.3 — intent trigger source).

**Ordering:** DemoLoopOrchestrator opens beat 4 gate on `demo.intent_labeled` → **SimTickStub** validates `intent.demo_interact` on `input.*` → **DMPauseGate** check → commit one stand-in tick → append **WorldEventLog** `demo_interact_observed` → emit `demo.sim_tick_committed` on `session.*` → DemoLoopOrchestrator advances to beat 5.

> **IRA annotation (GAP-4 — bus namespace convention):** `demo.sim_tick_committed` routes through `session.*` **by DemoLoopOrchestrator convention** (same as `demo.spawn_complete`, `demo.fp_active`, `demo.intent_labeled`). Optional `sim.tick_committed` on `sim.*` per 3.1 **SimTickPipeline** publish step is **execution-deferred** informational echo — DemoLoopOrchestrator progress uses `demo.*` on `session.*` only in v1 conceptual. Full `sim.*` bus registration remains **execution-deferred**.

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| awaiting_intent | DemoLoopOrchestrator beat 4 gate open | tick_pending when `demo.intent_labeled` + `intent.demo_interact` on `input.*` | blocked if intent token missing |
| tick_pending | awaiting_intent exit | committing when **DMPauseGate** not active | paused if DM cam active (hold until FP return) |
| committing | tick_pending exit | committed when stand-in tick + log append succeed | blocked if log append fails |
| committed | committing success | DemoLoopOrchestrator stage 4 → 5; emit `demo.sim_tick_committed` on `session.*` | — |
| paused | **DMPauseGate** active during tick_pending | resume to tick_pending on FP return | — |
| blocked | precondition or commit failure | terminal for beat 4; DemoLoopOrchestrator holds | |

### Single-tick commit (SimTickPipeline stand-in)

Per OQ-6.2.4-001 and parent 6.2 **SimTickStub vs SimTickPipeline**:

- **At most one** committed tick per demo loop session — triggered by `intent.demo_interact`, not by explore-phase frame loop.
- Stand-in tick **does not** run weather → NPC → faction subsystem passes — emits a single no-op or minimal **TickDelta** stub sufficient for log provenance.
- **SimClock** increments conceptual tick index `n` by 1; no catch-up spiral or multi-tick budget per session frame.
- Explore-phase 1 Hz stretch (`demo.sim_during_explore`) is **execution debug only** — not default v1 conceptual path.

### WorldEventLog append

Minimal row per OQ-6.2.4-002:

| Field | Demo v1 value | Authority |
|---|---|---|
| Event id | `demo_interact_observed` | **SimTickStub** |
| Trigger | `intent.demo_interact` consumption | 6.2.3 handoff |
| Tick index | `n` after stand-in commit | 3.1 **SimClock** |
| Facet hint | `demo_shrine_v1` (optional) | Aligns with 6.2.1 stub world |
| Provenance | `source: sim_tick_stub` | 1.3 append-only pattern |

No **OffScreenActivityWindow** rows, no faction graph deltas, no **CanonFact** proposals.

### DMPauseGate interaction

- If **DMPauseGate** active when beat 4 opens (should not occur under strict ordering before beat 6): **SimTickStub** enters `paused`; no tick commit.
- If DM cam activated mid-commit (race — execution only): abort commit; remain `tick_pending`.
- Resume on FP return per parent 6.2 edge case "Sim stub tick during DM cam".

### `demo.sim_tick_committed` gate

Emitted on `session.*` **once** when **all** preconditions satisfied:

1. `demo.intent_labeled` already observed (beat 3 complete).
2. `intent.demo_interact` consumed from `input.*`.
3. Stand-in tick committed and **WorldEventLog** row appended.

On emission: **DemoLoopOrchestrator** records beat 4 progress; **RuleCheckProbe** may open beat 5 gate immediately per **HorizonDemoManifest** `strict_ordering: true`.

### Beat 4 → beat 5 handoff

- **Default exit:** `demo.sim_tick_committed` → **RuleCheckProbe** builds post-tick **RuleContextFrame** stub with `demo_interact_observed` in context.
- **Debug exit:** operator `demo.advance_beat` (execution only) — does not weaken conceptual strict-ordering default.
- Beat 5 must **not** evaluate rules before log row exists.

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.2.4 consumes it |
|---|---|
| `demo.intent_labeled` on `session.*` (6.2.3) | Beat 4 entry gate |
| `intent.demo_interact` on `input.*` (6.2.3) | Tick trigger |
| **SimTickPipeline** + **WorldEventLog** append contract (3.1) | Stand-in tick + log row |
| **DMPauseGate** read (3.1 / 6.2 demo policy) | Pause tick commit while DM active |
| **SimClock** tick index (3.1) | Log `tick_index` field |

**Exports to downstream beats:**

| Export | Consumer |
|---|---|
| **WorldEventLog** row `demo_interact_observed` | Beat 5 **RuleCheckProbe** condition input |
| `demo.sim_tick_committed` on `session.*` | **DemoLoopOrchestrator** progress; operator telemetry |
| Post-tick sim state stub | **RuleContextFrame** stub (beat 5) |

**Explicit non-import:** **OffScreenActivityWindow**, **FactionGraphSubsystem**, **ConsequenceResolver** full merge, **ToneProfileConsequenceWeights**, **CompiledWorldManifest** proc-gen executor.

## Edge Cases

| Case | Handling |
|---|---|
| `demo.intent_labeled` never arrives | **SimTickStub** stays `awaiting_intent`; DemoLoopOrchestrator holds at beat 4 |
| Tick attempted before `intent.demo_interact` visible | Reject per strict ordering — remain `awaiting_intent` |
| Double tick commit in same session | **DemoLoopOrchestrator** rejects duplicate — one tick per loop per OQ-6.2.4-001 |
| Double `demo.sim_tick_committed` emission | Reject duplicate — emit once per session |
| **DMPauseGate** active at tick_pending | Enter `paused`; resume on FP return |
| Log append fails after tick | `blocked`; no stage advance; toast via **PlayerFeedbackChannel** (execution wiring) |

## Open Questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.2.4-001 | Single tick per loop vs explore-phase 1 Hz stretch? | **Single tick per loop for v1** — triggered by intent only; 1 Hz stretch execution debug only |
| OQ-6.2.4-002 | Minimal **WorldEventLog** row fields? | **`demo_interact_observed` + tick_index + trigger ref** — full **CommittedTickRecord** schema execution-deferred |
| OQ-6.2.4-003 | Publish `sim.tick_committed` on `sim.*` vs `demo.sim_tick_committed` on `session.*` only? | **`session.*` for stage signal; optional `sim.*` echo execution-deferred** — split per 3.1 vs orchestrator convention |

## Pseudo-code readiness

Reader can sketch **SimTickStub** state machine (awaiting_intent → tick_pending → committing → committed | paused | blocked), single-tick trigger contract, **WorldEventLog** append shape, and beat 4/5 handoff without guessing full **SimTickPipeline** subsystem APIs. Execution track owns typed sim interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.2.4 tertiary — SimTickStub sim stub (depth-first backfill; beat 4 of 8-beat demo loop)
- [x] Depth-first continue → 6.2.5 RuleCheckProbe (beat 5) — [[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]

