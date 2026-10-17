---
title: Phase 6.2.3 — IntentPipelineStub Intent Stub (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: 6.2.3
project-id: genesis-mythos-master
status: active
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- horizon-demo
- intent-stub
- beat-3
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]'
body_compact_source_queue: followup-deepen-phase622-tertiary-20260716T033640Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.2.3 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-16 (`followup-deepen-phase622-tertiary-20260716T033640Z`).

## Archived body (pre-compact)


## Phase 6.2.3 — IntentPipelineStub Intent Stub

Decomposes **beat 3 (Intent stub)** of the eight-beat horizon demo loop from parent [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **IntentPipelineStub** samples the interact input from beat 2, maps it to a labeled intent token `intent.demo_interact` on the `input.*` bus, and emits `demo.intent_labeled` as the beat 3 exit gate. Nouns and ordering only — no **IntentResolver** canon proposals, no **CanonRegistry** writes, no Godot input action wiring.

> **Parent boundary:** This slice begins after `demo.fp_active` from [[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]] and the interact input sample that closed beat 2. It completes beat 3 of the **DemoLoopOrchestrator** stage machine; beat 4 (**SimTickStub**) awaits `intent.demo_interact` on `input.*`.

## Scope

**In scope:** **IntentPipelineStub** lifecycle (awaiting_fp → awaiting_interact → labeling → labeled | blocked); beat 3 entry gate on `demo.fp_active` plus interact sample handoff from **FPExploreRigHost**; discrete interact event capture (conceptual interact key / affordance — not locomotion/look); mapping to single labeled token **`intent.demo_interact`** on `input.*` bus per parent 6.2 beat table; `demo.intent_labeled` emission on `session.*` after token published; **InputIntent** layer envelope shape (1.1 — agency self, no dominate/absent-proxy paths in demo v1); rejection of canon-touching side effects; **DemoLoopOrchestrator** beat 3 entry/exit gates.

**Out of scope:** **SpawnBootstrapController** and **FPExploreRigHost** (beats 1–2); **SimTickStub** tick commit and **WorldEventLog** append (beat 4); full **IntentResolver** + **CanonRegistry** path (Phase 1.2 / 2.2 execution wiring); **RuleCheckProbe**, **DMCamTransitionSlot**, **OverwriteDemonstrationSlot**, **PlayerFeedbackChannel** (beats 5–8); multi-intent catalog or proc-gen intent DAG; factory catalog attestation (6.1); execution-track Godot InputMap, C# intent router types, or **CanonFact** serialization.

## Behavior

**Actors:** **IntentPipelineStub** (beat 3 owner), **InputIntent** router (1.1 — envelope validation only, no canon gate in stub), **DemoLoopOrchestrator** (stage gate machine), **FPExploreRigHost** (6.2.2 — interact sample source).

**Ordering:** DemoLoopOrchestrator opens beat 3 gate on `demo.fp_active` + interact sample → **IntentPipelineStub** validates FP explore preconditions → capture interact discrete event → publish `intent.demo_interact` on `input.*` → emit `demo.intent_labeled` on `session.*` → DemoLoopOrchestrator advances to beat 4.

> **IRA annotation (GAP-4 — bus namespace convention):** `demo.intent_labeled` routes through `session.*` **by DemoLoopOrchestrator convention** (same as `demo.spawn_complete`, `demo.fp_active`). Labeled intent token **`intent.demo_interact`** publishes on **`input.*`** per parent 6.2 beat table and **1.1 InputIntent** layer authority — not on `session.*`. Full bus namespace registration remains **execution-deferred**; DemoLoopOrchestrator owns `demo.*` stage signals on `session.*`; **InputIntent** layer owns labeled tokens on `input.*`.

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| awaiting_fp | DemoLoopOrchestrator beat 3 gate open | awaiting_interact when `demo.fp_active` observed | blocked if FP mode not active |
| awaiting_interact | awaiting_fp exit | labeling when interact sample received from beat 2 handoff | blocked if interact arrives before `demo.fp_active` (strict ordering) |
| labeling | interact sample present | labeled when `intent.demo_interact` published on `input.*`; emit `demo.intent_labeled` on `session.*` | blocked if envelope validation fails |
| labeled | labeling success | DemoLoopOrchestrator stage 3 → 4 | — |
| blocked | precondition or validation failure | terminal for beat 3; DemoLoopOrchestrator holds; toast via **PlayerFeedbackChannel** (6.2 secondary — execution wiring) | |

### Interact sample capture

- Consumes the **interact** discrete input event that closed beat 2 per OQ-6.2.2-001 (interact-only exit).
- Does **not** re-consume locomotion or look vectors — those remain **FPExploreRigHost** responsibility.
- Sample carries minimal envelope: `source: player_fp`, `affordance: demo_interact`, `timestamp: session_tick` (conceptual — execution track types deferred).
- Rejects interact samples while **DMPauseGate** active (demo policy — should not occur before beat 6 under strict ordering).

### `intent.demo_interact` token

Single demo v1 intent token per OQ-6.2.3-001:

| Field | Demo v1 value | Authority |
|---|---|---|
| Token id | `intent.demo_interact` | IntentPipelineStub |
| Bus | `input.*` | 1.1 InputIntent layer |
| Agency class | `self` | 4.1 **PerspectiveEnvelope** — no dominate/passenger paths |
| Canon touch | `none` | Stub — no **CanonFact** proposal |
| Target facet hint | `demo_shrine_v1` (optional) | Aligns with 6.2.1 stub world — informational only |

Token publication is **idempotent per session** — duplicate interact presses after labeling do not re-emit unless operator enables `demo.allow_intent_repeat` (execution debug only).

### IntentPipelineStub vs full IntentResolver

- Maps **one** discrete input affordance → **one** named token — does **not** invoke **IntentResolver** proposal pipeline or **CanonRegistry** writes.
- Proves **InputIntent → sim-relevant signal** seam for horizon demo v1; full resolver path remains Phase 2.2 execution wiring.
- **RuleContextFrame** and **SimTickStub** (beat 4) consume `intent.demo_interact` as tick trigger — no intermediate canon commit.

### `demo.intent_labeled` gate

Emitted on `session.*` **once** when **all** preconditions satisfied:

1. `demo.fp_active` already observed (beat 2 complete).
2. Interact sample captured and validated.
3. `intent.demo_interact` published on `input.*` and acknowledged by **InputIntent** router (stub ack — no canon gate).

On emission: **DemoLoopOrchestrator** records beat 3 progress; **SimTickStub** may open beat 4 gate immediately per **HorizonDemoManifest** `strict_ordering: true`.

### Beat 3 → beat 4 handoff

- **Default exit:** `demo.intent_labeled` → **SimTickStub** observes `intent.demo_interact` on `input.*` and commits one stub tick.
- **Debug exit:** operator `demo.advance_beat` (execution only) — does not weaken conceptual strict-ordering default.
- Beat 4 must **not** tick before `intent.demo_interact` is visible on `input.*`.

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.2.3 consumes it |
|---|---|
| `demo.fp_active` on `session.*` (6.2.2) | Beat 3 entry gate |
| Interact input sample from beat 2 handoff (6.2.2) | Labeling trigger |
| **InputIntent** layer + `input.*` bus (1.1) | Token publication target |
| **PerspectiveEnvelope** self-agency rules (4.1) | Envelope validation — reject dominate/passenger |
| **DMPauseGate** read (3.1 / 6.2 demo policy) | Block labeling while DM active |

**Exports to downstream beats:**

| Export | Consumer |
|---|---|
| `intent.demo_interact` on `input.*` | Beat 4 **SimTickStub** tick trigger; **RuleContextFrame** stub (beat 5) |
| `demo.intent_labeled` on `session.*` | **DemoLoopOrchestrator** progress; operator telemetry |
| Intent path proven (input → labeled token) | Execution playtest scripts; Half A execution tech lead wiring |

**Explicit non-import:** **CanonRegistry**, **IntentResolver** proposal queue, **CompiledWorldManifest**, factory **PresentationShellManifest** attestation.

## Edge Cases

| Case | Handling |
|---|---|
| `demo.fp_active` never arrives | **IntentPipelineStub** stays `awaiting_fp`; DemoLoopOrchestrator holds at beat 3 |
| Interact before `demo.fp_active` | Reject per strict ordering — sample discarded; remain `awaiting_fp` |
| Double interact before labeling completes | First sample wins; duplicates ignored until `labeled` state |
| Double `demo.intent_labeled` emission | **DemoLoopOrchestrator** rejects duplicate — emit once per session |
| Attempt to label during DMPauseGate | `blocked`; no token publication |
| Operator presses interact with no target POI in range | v1 still labels `intent.demo_interact` — spatial validation **execution-deferred** (OQ-6.2.3-002) |

## Open Questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.2.3-001 | Single `intent.demo_interact` vs small intent catalog for demo? | **Single token for v1** — proves seam; catalog expansion execution stretch only |
| OQ-6.2.3-002 | Require POI proximity before labeling? | **No proximity gate in v1 conceptual** — spatial raycast validation execution-deferred |
| OQ-6.2.3-003 | Publish intent on `input.*` only vs mirror on `session.*`? | **`input.*` for token; `session.*` for `demo.intent_labeled` stage signal** — split per 1.1 layer vs orchestrator convention |

## Pseudo-code readiness

Reader can sketch **IntentPipelineStub** state machine (awaiting_fp → awaiting_interact → labeling → labeled | blocked), interact sample envelope, `intent.demo_interact` publication contract, and beat 3/4 handoff without guessing **IntentResolver** APIs. Execution track owns typed intent interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.2.3 tertiary — IntentPipelineStub intent stub (depth-first backfill; beat 3 of 8-beat demo loop)
- [x] Depth-first continue → 6.2.4 SimTickStub (beat 4) minted [[Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]

