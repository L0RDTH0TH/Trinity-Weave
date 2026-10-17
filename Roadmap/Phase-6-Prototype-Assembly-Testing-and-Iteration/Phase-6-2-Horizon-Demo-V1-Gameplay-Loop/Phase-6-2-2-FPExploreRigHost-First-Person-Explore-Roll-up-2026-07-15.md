---
title: Phase 6.2.2 — FPExploreRigHost First-Person Explore (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: 6.2.2
project-id: genesis-mythos-master
status: active
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- horizon-demo
- fp-explore
- beat-2
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]'
body_compact_source_queue: followup-deepen-phase622-tertiary-20260716T033640Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.2.2 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-15 (`followup-deepen-phase622-tertiary-20260716T033640Z`).

## Archived body (pre-compact)

## Phase 6.2.2 — FPExploreRigHost First-Person Explore

Decomposes **beat 2 (FP explore)** of the eight-beat horizon demo loop from parent [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **FPExploreRigHost** consumes `demo.spawn_complete`, activates **PerspectiveEnvelope** `player_fp` mode on the attached **PlayerFPRig**, routes locomotion and look input, and emits `demo.fp_active` as the beat 2 exit gate. Nouns and ordering only — no Godot CharacterBody3D APIs or input action map wiring.

> **Parent boundary:** This slice begins after `demo.spawn_complete` from [[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]] with **PlayerFPRig** attached-and-inactive on `fp_baseline_rig`. It completes beat 2 of the **DemoLoopOrchestrator** stage machine; beat 3 (**IntentPipelineStub**) awaits `demo.fp_active` plus an interact input sample.

## Scope

**In scope:** **FPExploreRigHost** lifecycle (awaiting_spawn → activating → exploring → beat_exit | blocked); **PerspectiveEnvelope** `player_fp` mode activation (4.1 authority — resolves OQ-6.2.1-003); locomotion input consumption (move vector on `input.*` bus); look input consumption (yaw/pitch on `input.*` bus); `demo.fp_active` emission on `session.*` after mode activation + first input frame acknowledged; beat 2 entry gate on `demo.spawn_complete`; beat 2 exit gate opening beat 3 on interact sample OR operator `demo.advance_beat` debug cue (execution only); **DMPauseGate** read-only respect — explore input suppressed while DM cam active (demo policy from 6.2 secondary).

**Out of scope:** **SpawnBootstrapController** stub world facet and FPRig socket attach (beat 1 — 6.2.1); **IntentPipelineStub** labeled intent tokens (beat 3); **SimTickStub**, **RuleCheckProbe**, **DMCamTransitionSlot**, **OverwriteDemonstrationSlot**, **PlayerFeedbackChannel** (beats 4–8); full **InputIntent** router and **CanonRegistry** path (Phase 1.2 / 2.2 execution wiring); **CameraInterpolatorRegistry** blend curves and **ModeTransitionGraph** edges beyond FP mode activation (4.1 / 4.2 execution-deferred); factory **KinestheticHonestyChecklist** sign-off (6.1); execution-track Godot input map, physics body, or camera rig implementation.

## Behavior

**Actors:** **FPExploreRigHost** (beat 2 owner), **PlayerFPRig** (4.1 — rig under explore), **PerspectiveEnvelope** (4.1 — legal mode `player_fp`), **DemoLoopOrchestrator** (stage gate machine), **PlayRegionHost** (6.1.2 — mount context, no mutation this beat).

**Ordering:** DemoLoopOrchestrator opens beat 2 gate on `demo.spawn_complete` → **FPExploreRigHost** validates FPRig attached-and-inactive → activate **PerspectiveEnvelope** `player_fp` → consume locomotion + look on `input.*` → emit `demo.fp_active` on `session.*` → hold explore until interact sample or debug advance → DemoLoopOrchestrator advances to beat 3.

> **IRA annotation (GAP-4 — bus namespace convention):** `demo.fp_active` (and other `demo.*` stage signals in beat 2) route through the `session.*` bus **by DemoLoopOrchestrator convention** per parent 6.2 **HorizonDemoManifest** `loop_beats` contract. Same namespace rules as 6.2.1 `demo.spawn_complete`. Full bus namespace registration remains **execution-deferred**; DemoLoopOrchestrator owns routing of `demo.*` through `session.*`. (IRA ira_reconciled; validator advisory GAP-4; 2026-06-27)

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| awaiting_spawn | DemoLoopOrchestrator beat 2 gate open | activating when `demo.spawn_complete` observed + FPRig attached | blocked if spawn incomplete or rig missing |
| activating | awaiting_spawn exit | exploring when `player_fp` mode active + first input frame ack | blocked if PerspectiveEnvelope rejects mode |
| exploring | activating success | beat_exit on interact sample OR `demo.advance_beat` debug; emit `demo.fp_active` once at exploring entry | blocked if DMPauseGate active (input suppressed, no false exit) |
| beat_exit | interact sample or debug advance | DemoLoopOrchestrator stage 2 → 3 | — |
| blocked | precondition or envelope failure | terminal for beat 2; DemoLoopOrchestrator holds; toast via **PlayerFeedbackChannel** (6.2 secondary — execution wiring) | |

### PerspectiveEnvelope `player_fp` activation

- **FPExploreRigHost** owns activation per OQ-6.2.1-003 — **SpawnBootstrapController** (6.2.1) attaches rig only.
- Requests legal mode `player_fp` on **PerspectiveEnvelope** (4.1 contract); rejects dominated-victim **passenger_fp** overlay paths (Phase 5 — not exercised in demo v1).
- Does **not** invoke **ModeTransitionGraph** DM edges — DM cam is beat 6.
- On success: FPRig state transitions `inactive` → `fp_active`; **InputIntent** router may accept self-agency locomotion/look intents per 4.1 envelope rules.

### Locomotion and look input

- **Locomotion:** move vector (conceptual WASD or stick equivalent) published on `input.*` bus; **FPExploreRigHost** consumes and applies to **PlayerFPRig** presentation anchor — no world mutation, no **SimTickPipeline** tick.
- **Look:** yaw/pitch deltas on `input.*`; clamp policy and sensitivity are **execution-deferred** (OQ-6.2.2-002).
- Input consumed only while state is `exploring` and **DMPauseGate** not active.
- Does **not** emit **CanonFact** or touch **IntentResolver** — full intent path is beat 3.

### `demo.fp_active` gate

Emitted on `session.*` bus **once** when **all** preconditions satisfied:

1. `demo.spawn_complete` already observed (beat 1 complete).
2. **PerspectiveEnvelope** reports `player_fp` active.
3. First locomotion or look input frame acknowledged (proves input path live).

On emission: **DemoLoopOrchestrator** records beat 2 progress; explore continues until beat 3 entry trigger (interact sample). Beat 3 may open immediately after `demo.fp_active` — ordering per **HorizonDemoManifest** `strict_ordering: true`.

### Beat 2 → beat 3 handoff

- **Default exit:** player issues interact input (e.g. interact key) while in `exploring` — **IntentPipelineStub** (beat 3) samples that event.
- **Debug exit:** operator `demo.advance_beat` (execution only) — does not weaken conceptual strict-ordering default.
- **DMPauseGate:** if DM cam becomes active mid-explore (should not occur before beat 6 under strict ordering), locomotion/look suppressed; beat 2 does not auto-advance.

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.2.2 consumes it |
|---|---|
| `demo.spawn_complete` on `session.*` (6.2.1) | Beat 2 entry gate |
| **PlayerFPRig** attached-and-inactive on `fp_baseline_rig` (6.2.1) | Rig activation target |
| **PerspectiveEnvelope** `player_fp` mode (4.1) | Legal FP mode activation |
| **PlayRegionHost** mount context (6.1.2) | Spatial anchor — no socket mutation |
| `input.*` bus (1.1 **InputIntent** layer) | Locomotion + look samples |
| **DMPauseGate** read (3.1 / 6.2 demo policy) | Suppress explore input when DM active |

**Exports to downstream beats:**

| Export | Consumer |
|---|---|
| `demo.fp_active` on `session.*` | Beat 3 **IntentPipelineStub** precondition; beat 6 **DMCamTransitionSlot** guard `demo_fp_active` |
| Active **PlayerFPRig** in `fp_active` state | **IntentPipelineStub** interact sample source |
| Explore input path proven | Operator telemetry; execution playtest scripts |

**Explicit non-import:** **SpawnBootstrapController** stub facet fields; **RuleEngineCore**; **ModeTransitionGraph** DM edges; factory catalog attestation (6.1).

## Edge Cases

| Case | Handling |
|---|---|
| `demo.spawn_complete` never arrives | **FPExploreRigHost** stays `awaiting_spawn`; DemoLoopOrchestrator holds at beat 2 |
| FPRig not attached at beat 2 open | `blocked`; no `demo.fp_active`; toast explains missing rig |
| PerspectiveEnvelope rejects `player_fp` | `blocked`; DemoLoopOrchestrator holds; no beat 3 advance |
| Interact before `demo.fp_active` emitted | Reject per strict ordering — interact ignored until FP mode live |
| DMPauseGate active during explore | Input suppressed; remain in `exploring`; no premature beat 3 |
| Zero input frames (AFK player) | `demo.fp_active` withheld until first input ack — prevents false "FP ready" telemetry |
| Double `demo.fp_active` emission | **DemoLoopOrchestrator** rejects duplicate — emit once per session |

## Open Questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.2.2-001 | Beat 2 exit: interact-only vs optional timer auto-advance? | **Interact-only default** for v1 — teaches intent stub beat; timer auto-advance execution debug only |
| OQ-6.2.2-002 | Look sensitivity and input deadzone? | **Execution-deferred** — conceptual beat proves input path exists; tuning on execution track |
| OQ-6.2.2-003 | `demo.fp_active` before or after first movement? | **After first locomotion or look frame** — proves input consumption, not merely mode flag |

## Pseudo-code readiness

Reader can sketch **FPExploreRigHost** state machine (awaiting_spawn → activating → exploring → beat_exit | blocked), **PerspectiveEnvelope** activation handshake, `input.*` consumption contract, and `demo.fp_active` gate without guessing Godot input APIs. Execution track owns typed rig interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.2.2 tertiary — FPExploreRigHost first-person explore (depth-first backfill; beat 2 of 8-beat demo loop)
- [x] Depth-first continue → 6.2.3 IntentPipelineStub (beat 3) minted [[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]

