---
title: Phase 6.2.6 — DMCamTransitionSlot DM Cam (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: 6.2.6
project-id: genesis-mythos-master
status: active
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- horizon-demo
- dm-cam
- beat-6
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]'
body_compact_source_queue: followup-deepen-phase626-tertiary-20260716T061100Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.2.6 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-16 (`followup-deepen-phase626-tertiary-20260716T061100Z`).

## Archived body (pre-compact)

## Phase 6.2.6 — DMCamTransitionSlot DM Cam

Decomposes **beat 6 (DM cam)** of the eight-beat horizon demo loop from parent [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **DMCamTransitionSlot** transitions the player from **player_fp** to **WorldCam** DM rail via **ModeTransitionGraph** edge `fp_to_worldcam_demo`, evaluates **TransitionGuardRegistry** predicates, respects **DMPauseGate** read-only during the transition window, and publishes mode + stage signals on the demo bus split. Nouns and ordering only — no Godot rig wiring, no full **DMRigPolicyMatrix**, no MapCam / SensoriumAttach paths in v1.

> **Parent boundary:** This slice begins after `demo.rule_check_complete` on `session.*` from [[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]] (beat 5 evaluation finished — pass or fail per **HorizonDemoManifest** policy). Beat 6 opens on **operator DM rail hotkey** or optional **scripted demo cue** — **not** auto-triggered by `rule.demo_pass` in v1 default per OQ-6.2-003. It completes beat 6 of the **DemoLoopOrchestrator** stage machine; beat 7 (**OverwriteDemonstrationSlot**) awaits active DM session + facet selection.

## Scope

**In scope:** **DMCamTransitionSlot** lifecycle (awaiting_eligibility → awaiting_trigger → guard_evaluating → transitioning → dm_active | blocked | rejected); beat 6 entry eligibility on `demo.rule_check_complete` plus guard preconditions (`play_region_mounted`, `demo_fp_active`, rule outcome per manifest); **operator DM rail hotkey** entry (primary) and optional **scripted demo cue** (kiosk — execution profile only); **ModeTransitionGraph** demo edge `fp_to_worldcam_demo` (4.2 authority — demo-specific id, not renaming 4.1 rig IDs); **TransitionGuardRegistry** guard stack evaluation; **DMPauseGate** read-only interaction during FP→DM entry (`not_dmpause_frozen` per 4.2); **WorldCamPolicy** row activation (demo-truncated — WorldCam rail only); **HUDLayerStack** mode badge → DM on `presentation.*`; `demo.dm_cam_active` emission on `session.*` after transition complete; **DemoLoopOrchestrator** beat 6 entry/exit gates; **HorizonDemoManifest** `strict_ordering: true` rejection of out-of-order DM cam attempts.

**Out of scope:** **SpawnBootstrapController**, **FPExploreRigHost**, **IntentPipelineStub**, **SimTickStub**, **RuleCheckProbe** (beats 1–5); **OverwriteDemonstrationSlot**, **PlayerFeedbackChannel** (beats 7–8); full **DMRigPolicyMatrix** (MapCam, SensoriumAttach policy rows — demo uses WorldCam only); **DominateSpellBinding** / agency hijack paths (5.2); sim tick commit during DM cam (**SimTickStub** paused via **DMPauseGate** — 6.2.4); factory catalog attestation (6.1); execution-track Godot camera rigs, C# transition interpolators, or HR rollup gates.

## Behavior

**Actors:** **DMCamTransitionSlot** (beat 6 owner), **DemoLoopOrchestrator** (stage gate machine), **TransitionGuardRegistry** (4.2 — composable predicates), **ModeTransitionGraph** (4.2 — edge catalog), **DMPauseGate** (3.1 — read-only freeze check), **WorldCamPolicy** (4.2 — demo-truncated matrix row), **DMRailUXContract** (4.2 — hotkey ordering + blocked messaging), **HUDLayerStack** (6.1.3 — mode badge layer), **PlayRegionHost** (6.1.2 — mount guard source), **FPExploreRigHost** (6.2.2 — `demo_fp_active` source), **RuleCheckProbe** (6.2.5 — upstream rule outcome).

**Ordering:** DemoLoopOrchestrator marks beat 6 **eligible** on `demo.rule_check_complete` → **DMCamTransitionSlot** waits for operator hotkey or scripted cue → guard stack evaluates → **ModeTransitionGraph** fires `fp_to_worldcam_demo` → WorldCam rail active → emit `demo.dm_cam_active` on `session.*` + `presentation.mode_badge_dm` on `presentation.*` → DemoLoopOrchestrator advances to beat 7 eligibility.

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| awaiting_eligibility | DemoLoopOrchestrator beat 6 gate eligible | awaiting_trigger when `demo.rule_check_complete` + manifest allows beat 6 | blocked if rule fail + `continue_on_rule_fail: false` |
| awaiting_trigger | awaiting_eligibility exit | guard_evaluating on operator hotkey or scripted cue | rejected if trigger before eligibility (strict_ordering) |
| guard_evaluating | trigger received | transitioning when guard stack passes | blocked on first guard failure |
| transitioning | guard_evaluating exit | dm_active when blend complete (conceptual — no interpolator API) | blocked if **DMPauseGate** engages mid-blend per 4.2 snap-complete policy |
| dm_active | transitioning success | DemoLoopOrchestrator stage 6 → 7 eligible; emit `demo.dm_cam_active` | — |
| blocked | guard or pause failure | terminal for beat 6 until operator reset or FP return | |
| rejected | out-of-order trigger | `presentation.dm_transition_blocked` on `presentation.*` (blocked-state toast per **DMRailUXContract**); no mode change | |

### Entry gates (beat 6 eligibility)

Per parent 6.2 **DMCamTransitionSlot** section and OQ-6.2-003:

| Guard | Source | Demo v1 contract |
|---|---|---|
| `play_region_mounted` | **6.1.2** **PlayRegionHost** mount lifecycle | `presentation.play_region_ready` observed; mount not torn down |
| `demo_fp_active` | **6.2.2** **FPExploreRigHost** | Player in **player_fp** perspective; FP rig attached |
| `demo.rule_check_complete` | **6.2.5** on `session.*` | Beat 5 evaluation finished — required for strict ordering |
| `rule_outcome_allows_dm` | **RuleEffectBus** + manifest | **Pass default:** eligible after `rule.demo_pass`. **Fail default:** beat 6 blocked unless `demo.continue_on_rule_fail` (execution debug only) |
| `not_dmpause_frozen` | **3.1** **DMPauseGate** | FP→DM entry requires freeze clearance per 4.2 **TransitionGuardRegistry** |

**Not auto-trigger:** `rule.demo_pass` alone does **not** invoke transition — operator hotkey or scripted cue required (OQ-6.2-003).

### Operator DM rail hotkey vs scripted cue

| Entry mode | Authority | Demo v1 default |
|---|---|---|
| Operator hotkey | **DMRailUXContract** (4.2) — FP → WorldCam rail ordering | **Primary** — player/operator initiates after beat 5 complete |
| Scripted demo cue | **HorizonDemoManifest** kiosk profile (execution only) | **Optional** — auto-fire hotkey equivalent after eligibility delay; not conceptual default |

Both paths converge on the same **DMCamTransitionSlot** `guard_evaluating` state — no separate auto-edge in v1 conceptual contract.

### ModeTransitionGraph edge `fp_to_worldcam_demo`

Demo-specific edge building on 4.2 `fp_to_world` pattern:

| Field | Demo v1 value |
|---|---|
| Edge id | `fp_to_worldcam_demo` |
| Source rig | `player_fp` |
| Target rig | `dm_world` (**WorldCam** rail — demo truncates matrix to WorldCam only; execution alias `dm_worldcam_slot` per 6.1.2 mount socket — conceptual bridge only) |
| Guard stack | `play_region_mounted`, `demo_fp_active`, `demo_rule_check_complete`, `rule_outcome_allows_dm`, `not_dmpause_frozen`, `not_sensorium_blocked` (4.1 **SensoriumAttach** blocked during FP explore — demo surfaces toast) |
| Interpolator hint | `fp_to_dm_blend` (conceptual — execution owns curve) |
| Veto hooks | **NarrativeDeltaVetoPolicy** not evaluated at beat 6 — overwrite is beat 7 |

Full **ModeTransitionGraph** edge catalog and **DMRigPolicyMatrix** rows remain 4.2 authority; demo edge is a named subset.

### DMPauseGate interaction

- **SimTickStub** (6.2.4): if DM cam becomes active, stand-in tick path stays **paused** — no tick commit during DM observation (parent 6.2 edge case).
- **FP→DM entry:** `not_dmpause_frozen` guard must pass before edge fires (4.2).
- **Mid-blend pause:** If **DMPauseGate** engages during transition, complete visual blend (4.1 policy) but block intent routes until freeze clears — matrix `intent_eligible` = mode-switch only for DM rigs.
- **DM-active beat 6:** Beat 6 **dm_active** does **not** itself set narrative freeze — freeze semantics remain 3.1 authority; demo documents read-only observation only.

### Bus conventions

> **IRA annotation (GAP-6 — bus namespace convention):** Stage progress for beat 6 uses `demo.dm_cam_active` on `session.*` **by DemoLoopOrchestrator convention** (same family as `demo.spawn_complete`, `demo.fp_active`, `demo.intent_labeled`, `demo.sim_tick_committed`, `demo.rule_check_complete`). Mode presentation echoes use `presentation.*` — e.g. `presentation.mode_badge_dm` on **HUDLayerStack** **persistent/chrome** layer per **OQ-6.2.6-002** and 6.1.3 **D-6.1.3-002** (mode badge authority — not Transient). Guard failure toasts route through `presentation.dm_transition_blocked` on `presentation.*` (blocked-state messaging per **DMRailUXContract**) — not `session.*`. Full bus registration remains **execution-deferred**.

| Signal | Bus | When |
|---|---|---|
| `demo.rule_check_complete` | `session.*` | Upstream beat 5 complete (entry eligibility) |
| `demo.dm_cam_active` | `session.*` | Beat 6 transition complete; WorldCam rail active |
| `presentation.mode_badge_dm` | `presentation.*` | HUD mode badge shows DM observation |
| `presentation.dm_transition_blocked` | `presentation.*` | Guard failure or strict_ordering rejection (toast precursor) |
| `rule.demo_pass` / `rule.demo_fail` | **RuleEffectBus** (5.1) | Read-only for `rule_outcome_allows_dm` — not re-emitted by beat 6 |

### Beat 6 → beat 7 handoff

- **Default exit:** `demo.dm_cam_active` → operator may select facet for **OverwriteDemonstrationSlot** (beat 7).
- Beat 7 requires active DM session — beat 6 must reach `dm_active` before overwrite slot opens under `strict_ordering: true`.
- FP return path (WorldCam → player_fp) is **out of scope** for beat 6 completion — documented as operator escape hatch via 4.2 `world_to_fp` edge (execution wiring); loop progress for v1 demo assumes forward beat order through overwrite.

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.2.6 consumes it |
|---|---|
| `demo.rule_check_complete` on `session.*` (6.2.5) | Beat 6 eligibility gate |
| `rule.demo_pass` / `rule.demo_fail` on **RuleEffectBus** (6.2.5) | `rule_outcome_allows_dm` guard input |
| `demo.fp_active` on `session.*` (6.2.2) | `demo_fp_active` guard |
| `presentation.play_region_ready` (6.1.2) | `play_region_mounted` guard |
| **ModeTransitionGraph** + **TransitionGuardRegistry** (4.2) | Edge + guard evaluation |
| **DMPauseGate** (3.1) | `not_dmpause_frozen` predicate |
| **HUDLayerStack** (6.1.3) | Mode badge presentation |

**Exports to downstream beats:**

| Export | Consumer |
|---|---|
| `demo.dm_cam_active` on `session.*` | **DemoLoopOrchestrator** progress (beat 6→7); **OverwriteDemonstrationSlot** (beat 7) |
| `presentation.mode_badge_dm` | Operator UX; **PlayerFeedbackChannel** (beat 8) |
| Active WorldCam session stub | Beat 7 facet selection + **OverwritePatchLayer** |
| DM observation context | Operator telemetry |

**Explicit non-import:** **OverwritePatchLayer** apply (beat 7), **MapCamPolicy** / **SensoriumAttachPolicy** rows, full **AgencyEnvelope** dominate paths, factory **DevLeakageGuard** weakening.

## Edge Cases

| Case | Handling |
|---|---|
| Operator triggers DM cam before `demo.rule_check_complete` | **Rejected** per `strict_ordering: true` — `presentation.dm_transition_blocked` toast |
| `rule.demo_fail` + default manifest | Beat 6 **not eligible** — **DMCamTransitionSlot** stays `awaiting_eligibility` or `blocked` |
| `demo.continue_on_rule_fail` enabled | Beat 6 may become eligible despite fail — execution debug only |
| Hotkey pressed but `play_region_mounted` false | Guard failure — blocked; toast explains missing mount |
| Hotkey pressed during sim stub tick (should not occur pre-beat-6) | **SimTickStub** should be committed; if race, guard may fail — operator retry |
| **DMPauseGate** active at hotkey | `not_dmpause_frozen` fails — blocked until freeze clears |
| Operator never triggers DM cam after rule pass | Valid pause — loop incomplete until beat 8; beat 6 optional until hotkey (6.2.5 precedent) |
| Scripted auto-cue in kiosk build | Equivalent to hotkey after eligibility — same guard stack |

## Open Questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.2.6-001 | WorldCam-only vs allow MapCam switch during beat 6? | **WorldCam only** for v1 — MapCam is post-demo or execution stretch |
| OQ-6.2.6-002 | Mode badge: persistent layer vs Transient toast? | **Mode badge on HUD persistent/chrome layer** via `presentation.mode_badge_dm` — aligns with 6.1.3 stack |
| OQ-6.2.6-003 | Scripted cue delay after rule pass? | **Execution kiosk profile only** — conceptual default remains operator hotkey; no fixed delay in manifest |

## Pseudo-code readiness

Reader can sketch **DMCamTransitionSlot** state machine (awaiting_eligibility → awaiting_trigger → guard_evaluating → transitioning → dm_active | blocked | rejected), guard stack table, bus split (`session.*` vs `presentation.*`), and beat 6/7 handoff without guessing **ModeTransitionGraph** edge ids or **DMPauseGate** interaction. Execution track owns typed transition interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.2.6 tertiary — DMCamTransitionSlot DM cam (depth-first backfill; beat 6 of 8-beat demo loop)
- [x] Depth-first continue → 6.2.7 OverwriteDemonstrationSlot (beat 7) — [[Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roadmap-2026-06-27-1005]]

