---
title: Phase 6.2.8 — PlayerFeedbackChannel Feedback — Roll-up
project-id: genesis-mythos-master
roadmap_track: conceptual
rollup_of: Phase-6-2-8-PlayerFeedbackChannel-Feedback-Roadmap-2026-06-27-1021.md
created: '2026-07-17'
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.2.8 — PlayerFeedbackChannel Feedback — Roll-up

Overflow from manual chat recompact 2026-07-17 (pre-body 10043 chars → live ≤1200).

## Preserved source (pre-compact)

## Phase 6.2.8 — PlayerFeedbackChannel Feedback

Decomposes **beat 8 (Feedback)** of the eight-beat horizon demo loop from parent [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **PlayerFeedbackChannel** aggregates overwrite outcome, rule echo, and prior stage precursors into **HUDLayerStack** **Transient** toasts plus optional world chrome pulse, then publishes `demo.loop_complete` to close the **DemoLoopOrchestrator** v1 session. Nouns and ordering only — no new persistent HUD layers beyond **6.1.3**, no factory **KinestheticHonestyChecklist** sign-off substitution.

> **Parent boundary:** This slice begins after beat 7 overwrite outcome (`demo.overwrite_applied` or `demo.overwrite_vetoed` on `session.*` from [[Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roadmap-2026-06-27-1005]]) plus readable rule outcome from **RuleEffectBus** (`rule.demo_pass` / `rule.demo_fail` from [[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]). Beat 8 is the **terminal demo stage** for v1 strict ordering — it does not spawn new world state or re-run prior beats.

## Scope

**In scope:** **PlayerFeedbackChannel** lifecycle (awaiting_overwrite_outcome → aggregating → rendering → loop_closing → complete | blocked); beat 8 entry gate on overwrite stage completion (`demo.overwrite_applied` **or** `demo.overwrite_vetoed` per parent edge case); subscription fan-in to `rule.*`, `demo.*`, and `presentation.*` precursors (read-only — no re-emission of beat 5–7 buses); **HUDLayerStack** **Transient** layer toast composition (overwrite outcome, rule pass/fail echo, optional stage-failure recap); optional world chrome pulse (conceptual — atmosphere nudge visibility after DM return, execution-deferred); `demo.loop_complete` on `session.*`; **HorizonDemoManifest** session summary stub (stages passed, elapsed time, veto flag); **DemoLoopOrchestrator** beat 8 entry/exit gates and stage index closure at 8/8.

**Out of scope:** **SpawnBootstrapController** through **OverwriteDemonstrationSlot** (beats 1–7 re-execution); minting new **HUDLayerStack** persistent/chrome layers (6.1.3 authority); factory catalog attestation or **DevLeakageGuard** weakening; **RuleCheckProbe** re-evaluation; **OverwritePatchLayer** apply/revert; full playtest HR rollup or Godot toast widget implementation; `loop_repeat` debug re-entry (execution-only flag on manifest).

## Behavior

**Actors:** **PlayerFeedbackChannel** (beat 8 owner), **HUDLayerStack** Transient layer (6.1.3), **DemoLoopOrchestrator** (stage gate machine), **OverwriteDemonstrationSlot** (6.2.7 — upstream overwrite outcome), **RuleCheckProbe** (6.2.5 — upstream rule outcome on **RuleEffectBus**), prior beat `presentation.*` precursors (`presentation.overwrite_outcome`, `presentation.rule_outcome`, `presentation.dm_transition_blocked`).

**Ordering:** DemoLoopOrchestrator opens beat 8 gate on overwrite stage terminal state → **PlayerFeedbackChannel** aggregates rule + overwrite + optional precursors → render Transient toast(s) + optional chrome pulse → emit `demo.loop_complete` on `session.*` → DemoLoopOrchestrator marks session loop closed (v1 default: no auto `loop_repeat`).

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| awaiting_overwrite_outcome | DemoLoopOrchestrator beat 8 gate eligible | aggregating when `demo.overwrite_applied` or `demo.overwrite_vetoed` observed | blocked if beat 7 incomplete |
| aggregating | awaiting_overwrite_outcome exit | rendering when feedback payload composed | blocked if rule outcome unreadable on **RuleEffectBus** (`rule.demo_pass` / `rule.demo_fail`) — `presentation.rule_outcome` optional |
| rendering | aggregating exit | loop_closing when Transient toast queued | blocked if **HUDLayerStack** unavailable |
| loop_closing | rendering success | complete when `demo.loop_complete` emitted | blocked on orchestrator reject |
| complete | loop_closing success | terminal for beat 8; v1 session loop closed | — |
| blocked | precondition failure | terminal until operator reset | — |

### Entry gates (beat 8 eligibility)

| Guard | Source | Demo v1 contract |
|---|---|---|
| `overwrite_stage_terminal` | **6.2.7** on `session.*` | `demo.overwrite_applied` **or** `demo.overwrite_vetoed` |
| `rule_outcome_known` | **RuleEffectBus** (5.1) | `rule.demo_pass` or `rule.demo_fail` from beat 5 (read-only; **authoritative** — optional `presentation.rule_outcome` precursor from 6.2.5 is non-authoritative echo; absence does not block aggregating) |
| `strict_ordering` | **HorizonDemoManifest** | Feedback blocked before beat 7 terminal |
| `hud_transient_available` | **6.1.3** | Transient layer mounted — no new layer mint |

### Feedback payload composition (demo-truncated)

| Field | Source | Transient toast content |
|---|---|---|
| `overwrite_outcome` | `demo.overwrite_applied` / `demo.overwrite_vetoed` | Applied vs vetoed messaging (may reuse `presentation.overwrite_outcome` copy) |
| `rule_outcome` | `rule.demo_pass` / `rule.demo_fail` | Pass/fail echo — does not re-run **RuleEngineCore** |
| `veto_flag` | overwrite branch | When vetoed, summary still allows `demo.loop_complete` per parent edge case |
| `stages_passed` | **DemoLoopOrchestrator** | `1..8` fraction for summary stub |
| `session_elapsed` | demo session clock stub | Optional operator telemetry — execution owns timer |

Optional **world chrome pulse:** brief atmosphere highlight on stub facet `demo_shrine_mood` after DM return — visual echo of beat 7 patch; **not** required for conceptual loop closure.

### Bus conventions

> **IRA annotation (GAP-8 — bus namespace convention):** Beat 8 terminal signal `demo.loop_complete` routes on `session.*` **by DemoLoopOrchestrator convention** (same family as beats 1–7). **PlayerFeedbackChannel** **subscribes** to `rule.*` on **RuleEffectBus** and `presentation.*` / prior `demo.*` precursors — it does **not** re-publish beat 5–7 stage progress events. Toast rendering uses `presentation.feedback_*` family on **HUDLayerStack** **Transient** — execution-deferred registration.

| Signal | Bus | When |
|---|---|---|
| `demo.overwrite_applied` / `demo.overwrite_vetoed` | `session.*` | Upstream beat 7 terminal (entry eligibility) |
| `rule.demo_pass` / `rule.demo_fail` | **RuleEffectBus** (5.1) | Read-only aggregation from beat 5 |
| `presentation.overwrite_outcome` | `presentation.*` | Optional copy reuse from beat 7 precursor |
| `presentation.feedback_summary` | `presentation.*` | Composed loop summary toast (beat 8) |
| `demo.loop_complete` | `session.*` | Terminal beat 8 — v1 session loop closed |

### Beat 8 → post-loop handoff

- **Default exit:** `demo.loop_complete` → operator playtest telemetry; Phase **6.3** boundary glue may consume **HorizonDemoManifest** loop completion (non-factory attestation).
- **Veto path:** loop may complete with veto flag in summary — does not block `demo.loop_complete`.
- **Rule fail path:** if loop halted at beat 5 per manifest, beat 8 **not entered** — out of scope for this tertiary (orchestrator holds at stage 5).

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.2.8 consumes it |
|---|---|
| `demo.overwrite_applied` / `demo.overwrite_vetoed` (6.2.7) | Beat 8 eligibility + toast copy |
| `rule.demo_pass` / `rule.demo_fail` (6.2.5 via **RuleEffectBus**) | Rule echo in summary |
| **HUDLayerStack** Transient layer (6.1.3) | Toast render target — no new layers |
| Prior `presentation.*` precursors (beats 5–7) | Optional message reuse |
| **HorizonDemoManifest** `loop_progress` | Summary stub numerator/denominator |

**Exports to downstream:**

| Export | Consumer |
|---|---|
| `demo.loop_complete` on `session.*` | Operator telemetry; Phase 6.3 boundary glue; execution playtest scripts |
| `presentation.feedback_summary` | Operator UX |
| Session summary stub fields | Non-factory playtest sign-off (conceptual) |

**Explicit non-import:** Factory **KinestheticHonestyChecklist** operator sign-off (6.1), **PresentationShellManifest** catalog attestation, HR rollup gates, Godot UI widget types.

## Edge Cases

| Case | Handling |
|---|---|
| Overwrite vetoed but rule failed earlier | Valid if operator enabled `demo.continue_on_rule_fail` (execution debug) — beat 8 surfaces combined summary with flags |
| Standard v1 rule fail at beat 5 | Loop halts — beat 8 not entered (`continue_on_rule_fail: false`) |
| **HUDLayerStack** Transient unavailable | **blocked** — toast queue fails; no `demo.loop_complete` until recovered or operator reset |
| Duplicate toast from beat 7 precursor | **PlayerFeedbackChannel** dedupes or composes single summary — execution policy |
| Operator triggers feedback before overwrite terminal | **Rejected** per `strict_ordering: true` |
| `loop_repeat` debug enabled | Beat 8 completion may reset orchestrator — execution-only; conceptual v1 default is single pass |

## Open Questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.2.8-001 | Single composed toast vs stacked toasts per source? | **Single composed summary** default for v1 kiosk; stacked mode execution stretch |
| OQ-6.2.8-002 | World chrome pulse mandatory? | **Optional** — atmosphere echo after DM return; loop closure does not depend on pulse |
| OQ-6.2.8-003 | Session summary persisted across sessions? | **No** — ephemeral stub for demo session only; persistence execution-deferred |

## Pseudo-code readiness

Reader can sketch **PlayerFeedbackChannel** state machine (awaiting_overwrite_outcome → … → complete), subscription fan-in table, Transient toast composition, and `demo.loop_complete` emission without guessing **HUDLayerStack** layer ids from 6.1.3. Execution track owns typed feedback router interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.2.8 tertiary — PlayerFeedbackChannel feedback (depth-first backfill; beat 8 of 8-beat demo loop)
- [x] Post-loop: evaluate **6.2 branch closed** + Phase 6 advance-phase gate OR refine tertiaries — **Phase 6 complete** (advance-phase 2026-06-27)
