---
title: Phase 6.2 — Horizon Demo v1 Gameplay Loop (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: '6.2'
project-id: genesis-mythos-master
status: active
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- horizon-demo
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
body_compact_source_queue: followup-deepen-phase62-20260716T204442Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.2 Roll-up — archive of pre-compact feedstock

Canonical compact secondary: [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-16 (`followup-deepen-phase62-20260716T204442Z`). Pre-compact body was **16718** chars.

## Archived body (pre-compact)

## Phase 6.2 — Horizon Demo v1 Gameplay Loop

Playable **horizon demo v1** assembly slice: a single-session vertical proof that PMG pillars (perspective split, living sim, DM overwrite, rule hooks) can be **felt** in one loop — without factory catalog attestation scope and without full proc-gen or multiplayer. Canonical loop: **spawn → FP explore → intent stub → sim stub → rule check → DM cam → overwrite → feedback**.

> **Dual-track boundary:** This slice is **horizon demo v1 only**. It **does not** implement factory Phase 0 presentation shell attestation (launch → PlayRegion → HUD catalog row) — that is Phase **6.1**. Demo mounts **into** **6.1** **PlayRegionHost** sockets; it does not replace factory spine law.

## Scope

**In scope:** **HorizonDemoManifest** (demo session contract + M0–M8 milestone labels as conceptual checkpoints, not factory catalog rows); **SpawnBootstrapController** (minimal world/session spawn into **PlayRegionHost**); **FPExploreRigHost** (first-person locomotion + look stub on **PlayerFPRig** attachment); **IntentPipelineStub** (InputIntent → labeled intent tokens on `input.*` bus; stage signals `demo.*` on `session.*` — no full IntentResolver); **SimTickStub** (single intent-triggered **SimTickPipeline** stand-in tick per loop; optional 1 Hz explore stretch execution-debug-only — emitting **WorldEventLog** append); **RuleCheckProbe** (one **RuleEngineCore** evaluation pass via **RuleContextFrame** stub + **RuleEffectBus** echo); **DMCamTransitionSlot** (player FP → **WorldCam** DM rail via **ModeTransitionGraph** guarded edge); **OverwriteDemonstrationSlot** (**DMOverwriteClass** `live_patch` demo on a named world facet); **PlayerFeedbackChannel** (**HUDLayerStack** **Transient** layer + `presentation.*` toast); **DemoLoopOrchestrator** (ordered stage gate machine for the eight named beats).

**Out of scope:** Factory **PresentationShellManifest** catalog attestation and **KinestheticHonestyChecklist** operator sign-off (Phase **6.1**); factory vs demo boundary glue policy (Phase **6.3**); full proc-gen DAG execution, Azgaar/WebView, multiplayer (deferred post demo v1 per PMG); dominate spell / quest pressure plugins (5.2/5.3 — optional stretch hooks only); execution-track Godot scenes, C# types, HR rollup gates (execution-deferred / advisory on conceptual track).

## Behavior

### Eight-beat demo loop (canonical ordering)

Each beat is a **named demo stage** with explicit entry/exit gates. Stages run **once per demo session** in order unless operator enables **loop_repeat** debug flag (execution track only).

| Beat | Stage actor | Input | Output | Upstream authority |
|---|---|---|---|---|
| **1. Spawn** | **SpawnBootstrapController** | Session start after **6.1** `presentation.launch_complete` | Player avatar + stub world facet spawned into **PlayRegionHost**; `demo.spawn_complete` on `session.*` | **6.1** PlayRegion mount must precede spawn |
| **2. FP explore** | **FPExploreRigHost** | `demo.spawn_complete` + **PlayerFPRig** attach | Locomotion + look input consumed; interact sample handoff; `demo.fp_active` on `session.*` | **4.1** **PerspectiveEnvelope** FP mode |
| **3. Intent stub** | **IntentPipelineStub** | `demo.fp_active` + interact sample (e.g. interact key) | Labeled intent token `intent.demo_interact` on `input.*` bus; `demo.intent_labeled` on `session.*` | **1.1** InputIntent layer contract |
| **4. Sim stub** | **SimTickStub** | `demo.intent_labeled` + `intent.demo_interact` on `input.*` | One **SimTickPipeline** tick; **WorldEventLog** row `demo_interact_observed`; `demo.sim_tick_committed` on `session.*` | **3.1** tick authority (stubbed depth) |
| **5. Rule check** | **RuleCheckProbe** | `demo.sim_tick_committed` on `session.*` + **WorldEventLog** `demo_interact_observed` (frame built internally) | **RuleEngineCore** evaluates demo ruleset; `demo.rule_check_complete` on `session.*`; **RuleEffectBus** emits `rule.demo_pass` or `rule.demo_fail` | **5.1** rule primitives |
| **6. DM cam** | **DMCamTransitionSlot** | `demo.rule_check_complete` on `session.*` + operator DM rail hotkey OR scripted demo cue | **ModeTransitionGraph** edge `fp_to_worldcam_demo` with **TransitionGuardRegistry** pass; `demo.dm_cam_active` on `session.*`; **HUDLayerStack** mode badge → DM on `presentation.mode_badge_dm` | **4.2** mode graph |
| **7. Overwrite** | **OverwriteDemonstrationSlot** | `demo.dm_cam_active` on `session.*` + facet id (`demo_shrine_mood` default) | **OverwritePatchLayer** `live_patch` apply or veto rollback; `demo.overwrite_applied` / `demo.overwrite_vetoed` on `session.*`; `presentation.overwrite_outcome` on Transient HUD (**NarrativeDeltaVetoPolicy** accept\|veto evaluation) | **3.3** overwrite taxonomy |
| **8. Feedback** | **PlayerFeedbackChannel** | `demo.overwrite_applied` or `demo.overwrite_vetoed` on `session.*` + `rule.demo_pass` or `rule.demo_fail` on **RuleEffectBus** | `presentation.feedback_summary` on **HUDLayerStack** **Transient** + optional world chrome pulse; `demo.loop_complete` on `session.*` | **6.1** HUD layers |

**DemoLoopOrchestrator** responsibilities:

- Maintain stage index `1..8`; reject out-of-order transitions unless `demo.debug_skip_gates` (execution only).
- On stage failure: emit `demo.stage_failed` with stage id; roll back to safe stage (spawn or FP explore) without corrupting **PlayRegionHost** mount.
- Publish **HorizonDemoManifest** `loop_progress` fraction for operator telemetry.

### SpawnBootstrapController

- Consumes **PresentationSessionHandle** from **6.1** **LaunchFlowController** — does **not** re-run launch UI.
- Spawns **stub world facet** (single POI + terrain placeholder — no full **CompiledWorldManifest** from Phase 2 proc-gen).
- Attaches **PlayerFPRig** to **PlayRegionHost** FP socket; does **not** wire full **UnifiedSceneGraph** load.
- Emits `demo.spawn_complete` only after `presentation.play_region_ready` (6.1.2/6.1.3 canonical bus string) observed.

### IntentPipelineStub vs full IntentResolver

- Maps discrete input events to **named intent tokens** — does **not** propose **CanonFact** or touch **CanonRegistry**.
- Sufficient to prove **InputIntent → sim-relevant signal** seam for demo; full **IntentResolver** path remains Phase 2.2 execution wiring.

### SimTickStub vs SimTickPipeline

- Runs **at most one** committed tick per demo loop — intent-triggered only per OQ-6.2.4-001; optional 1 Hz stretch is **execution-debug-only** (not default v1 conceptual path).
- Appends minimal **WorldEventLog** entry — no **OffScreenActivityWindow** or faction deltas.
- Respects **DMPauseGate** read-only: if DM cam active, sim stub pauses until return to FP (demo policy).

### RuleCheckProbe

- Loads **demo_ruleset** plugin manifest (conceptual): one condition (`demo_interact_observed`) + one effect (`grant_demo_boon` stub).
- Routes effects through **RuleEffectBus** to **presentation.*** feedback channel — does **not** mutate canon graph.
- Documents priority band placeholder (demo rules in band 50–99 — below spell/quest bands per 5.2/5.3).

### DMCamTransitionSlot

- Uses **ModeTransitionGraph** edge catalog from **4.2** — demo-specific edge id `fp_to_worldcam_demo` with guards: `play_region_mounted`, `demo_fp_active`, `demo_rule_check_complete`, `rule_outcome_allows_dm`, `not_dmpause_frozen`, `not_sensorium_blocked`.
- Entry eligibility requires `demo.rule_check_complete` on `session.*` (beat 5 complete); operator hotkey or scripted demo cue — not auto-triggered by `rule.demo_pass` alone (OQ-6.2-003).
- Emits `demo.dm_cam_active` on `session.*` after transition; mode badge on `presentation.mode_badge_dm` (**HUDLayerStack** persistent/chrome layer per 6.1.3).
- Does **not** implement full **DMRigPolicyMatrix** — demo uses **WorldCam** rail only.
- **SensoriumAttach** blocked during transition per **4.1** — guard failure surfaces `presentation.dm_transition_blocked` (toast precursor); beat 8 **PlayerFeedbackChannel** consumes downstream.

### OverwriteDemonstrationSlot

- Demonstrates **DMOverwriteClass** `live_patch` on a single named facet (e.g. `demo_shrine_mood`).
- Entry requires `demo.dm_cam_active` on `session.*` (beat 6) + facet id resolution (default `demo_shrine_mood` per OQ-6.2.7-001).
- **ReGenerationIntentQueue** not exercised in v1 loop — structural re-gen deferred.
- **NarrativeDeltaVetoPolicy** must pass before commit; veto surfaces `presentation.overwrite_outcome` toast and emits `demo.overwrite_vetoed`.
- Successful apply emits `demo.overwrite_applied` on `session.*`; **RollbackWindow** ensures no partial commit on veto.

### PlayerFeedbackChannel

- **Lifecycle (beat 8):** awaiting_overwrite_outcome → aggregating → rendering → loop_closing → complete | blocked — terminal stage for v1 strict ordering.
- Subscribes to `rule.*` on **RuleEffectBus**, prior `demo.*` stage signals, and `presentation.*` precursors (read-only fan-in — no re-emission of beats 5–7 progress).
- **Entry:** `demo.overwrite_applied` **or** `demo.overwrite_vetoed` on `session.*` (beat 7 terminal) plus **RuleEffectBus** `rule.demo_pass` / `rule.demo_fail` (authoritative; optional `presentation.rule_outcome` echo non-blocking).
- Renders **Transient** HUD toasts via `presentation.feedback_summary` — does **not** add new persistent HUD layers beyond **6.1** stack.
- **Veto-complete path:** loop may reach `demo.loop_complete` with veto flag in summary per parent edge case.
- On `demo.loop_complete`: optional session summary stub (stages passed, elapsed time, veto flag) — closes **DemoLoopOrchestrator** v1 session (default: no `loop_repeat`).

### HorizonDemoManifest

| Field | Contract |
|---|---|
| `demo_id` | `horizon_demo_v1` |
| `track_authority` | **Horizon demo** — not factory catalog row |
| `mount_target` | **6.1** **PlayRegionHost** sockets |
| `loop_beats` | spawn, fp_explore, intent_stub, sim_stub, rule_check, dm_cam, overwrite, feedback |
| `milestone_labels` | M0–M8 as conceptual checkpoints mapping to beats (documentation only in v1) |
| `attestation_gates` | Loop completes once per session; no factory **DevLeakageGuard** substitution |
| `continue_on_rule_fail` | `false` for v1 — loop halts at stage 5 on `rule.demo_fail` unless operator enables `demo.continue_on_rule_fail` (execution debug only) |
| `strict_ordering` | default `true` — **DemoLoopOrchestrator** rejects out-of-order transitions (e.g. DM cam before rule check) with toast; aligns with edge-case `demo.strict_ordering` |
| `loop_repeat` | `false` default — eight beats run once per session; execution debug flag enables repeat |

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.2 consumes it |
|---|---|
| **PlayRegionHost** + **HUDLayerStack** (6.1) | Mount target + feedback toasts |
| **PlayerFPRig** + **PerspectiveEnvelope** (4.1) | FP explore beat |
| **InputIntent** bus (1.1) | Intent stub routing |
| **SimTickPipeline** + **WorldEventLog** (3.1) | Sim stub tick + log append |
| **RuleEngineCore** + **RuleEffectBus** (5.1) | Rule check probe |
| **ModeTransitionGraph** + guards (4.2) | DM cam transition |
| **OverwritePatchLayer** + veto (3.3) | Overwrite demonstration |

**Exports to downstream phases:**

| Export | Consumer |
|---|---|
| **HorizonDemoManifest** | Phase 6.3 boundary glue; execution track demo build profile |
| **DemoLoopOrchestrator** stage ids | Execution wiring; playtest scripts |
| **demo_ruleset** plugin stub | Execution track **RulesetPlugin** implementation |
| **loop_complete** telemetry | Operator playtest sign-off (non-factory) |

**Explicit non-import (dual-track):** **PresentationShellManifest** catalog attestation, **KinestheticHonestyChecklist** factory gates, Half A **ui_presentation_shell** scope sign-off — **6.1** authority only.

## Edge Cases

| Case | Handling |
|---|---|
| **6.1** PlayRegion not mounted at spawn attempt | **SpawnBootstrapController** blocks; `demo.spawn_blocked_no_play_region` toast |
| Player triggers DM cam before rule check | **DemoLoopOrchestrator** rejects or queues per `demo.strict_ordering` (default: reject with toast) |
| Rule check fails | **Halt at stage 5** (v1 default) — **HorizonDemoManifest** locks **continue_on_rule_fail: false**; operator may enable `demo.continue_on_rule_fail` for execution-debug teachable continue only (not co-equal v1 path) |
| Overwrite vetoed | **OverwriteDemonstrationSlot** rolls back patch; feedback explains veto; loop may still complete with `demo.loop_complete` + veto flag |
| Factory debug UI visible during demo | **6.1** **DevLeakageGuard** remains authoritative — demo does not weaken factory leakage policy |
| Sim stub tick during DM cam | **DMPauseGate** pauses stub; resume on FP return |

## Open Questions

| ID | Question | Conceptual authority decision |
|---|---|---|
| OQ-6.2-001 | Demo world: single static facet vs minimal proc-gen seed? | **Static stub facet** for horizon demo v1 — proves loop without Phase 2 executor wiring |
| OQ-6.2-002 | Rule check: always pass vs teachable fail path? | **Teachable fail allowed** — stage 5 may fail; loop halts unless operator enables `demo.continue_on_rule_fail` (execution debug only) |
| OQ-6.2-003 | DM cam: operator-triggered vs scripted auto after rule pass? | **Operator-triggered default**; scripted auto-cue optional for kiosk builds (execution track) |
| OQ-6.2-004 | M0–M8 labels: bind to beats 1:1 or documentation-only? | **Documentation mapping table in manifest** — not separate roadmap tertiaries in v1 breadth-first pass |

## Pseudo-code readiness

Reader can sketch **DemoLoopOrchestrator** stage machine, bus event names, and guard conditions without guessing beat order. No pseudo-code blocks in this conceptual slice — execution track owns typed interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.2 secondary with horizon demo v1 eight-beat loop
- [x] Dual-track boundary documented — horizon demo NOT factory Phase 0 shell (Phase 6.1)
- [x] Handoff to 6.3 factory vs demo boundary glue — breadth complete 3/3
- [x] Beat 1 tertiary minted — [[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]] (6.2.1; depth-first backfill; IRA GAP-5 rollup; CDR validated)
- [x] Beat 2 tertiary minted — [[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]] (6.2.2; depth-first backfill; persona: half_a.conceptual_architect; CDR validated)
- [x] Beat 3 tertiary minted — [[Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]] (6.2.3; depth-first backfill; persona: half_a.conceptual_architect; CDR validated)
- [x] Beat 4 tertiary minted — [[Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]] (6.2.4; depth-first backfill; persona: half_a.conceptual_architect; CDR validated)
- [x] Beat 5 tertiary minted — [[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]] (6.2.5; depth-first backfill; persona: half_a.conceptual_architect; CDR: deepen-rule-check-probe-2026-06-27-0800; validated)
- [x] Beat 6 tertiary minted — [[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]] (6.2.6; depth-first backfill; persona: half_a.conceptual_architect; CDR: deepen-dm-cam-transition-slot-2026-06-27-0830; validated)
- [x] Beat 7 tertiary minted — [[Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roadmap-2026-06-27-1005]] (6.2.7; depth-first backfill; persona: half_a.conceptual_architect; CDR: deepen-overwrite-demonstration-slot-2026-06-27-1005; validated)
- [x] Beat 8 tertiary minted — [[Phase-6-2-8-PlayerFeedbackChannel-Feedback-Roadmap-2026-06-27-1021]] (6.2.8; depth-first backfill; persona: half_a.conceptual_architect; CDR: deepen-player-feedback-channel-2026-06-27-1021; **6.2 eight-beat loop closed**)

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

## Consistency Reports

> [!note]
> Post-mint: execution rollup gates, REGISTRY-CI, HR closure artifacts, Godot demo scene implementation, and playtest HR sign-off are execution-deferred / advisory on conceptual track per conceptual_v1 contract. Horizon demo v1 playable build attestation is out of scope for conceptual completion — resolved on execution track.

Minted 2026-06-26 (godo-followup-20260626T195100Z-phase6-deepen-6-2); persona: half_a.conceptual_architect; product_factory_run_id: f35ff65cfb4f; pre_create_gate: skipped_conceptual_track; dual_track: horizon_demo_not_factory_spine; execution_gaps_advisory: true.

