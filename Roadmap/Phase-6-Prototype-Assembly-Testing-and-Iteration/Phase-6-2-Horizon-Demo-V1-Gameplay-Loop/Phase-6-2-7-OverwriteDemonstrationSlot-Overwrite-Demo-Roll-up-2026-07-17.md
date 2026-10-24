---
title: Phase 6.2.7 — OverwriteDemonstrationSlot Overwrite Demo — Roll-up
project-id: genesis-mythos-master
roadmap_track: conceptual
rollup_of: Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roadmap-2026-06-27-1005.md
created: '2026-07-17'
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.2.7 — OverwriteDemonstrationSlot Overwrite Demo — Roll-up

Overflow from manual chat recompact 2026-07-17 (pre-body 10937 chars → live ≤1200).

## Preserved source (pre-compact)

## Phase 6.2.7 — OverwriteDemonstrationSlot Overwrite Demo

Decomposes **beat 7 (Overwrite)** of the eight-beat horizon demo loop from parent [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **OverwriteDemonstrationSlot** applies a **DMOverwriteClass** `live_patch` demo delta on the stub world facet `demo_shrine_mood` via **OverwritePatchLayer**, evaluates **NarrativeDeltaVetoPolicy** before commit, and publishes overwrite outcome on the demo bus split. Nouns and ordering only — no Godot patch applicators, no **ReGenerationIntentQueue**, no **CanonRegistry** writes.

> **Parent boundary:** This slice begins after `demo.dm_cam_active` on `session.*` from [[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]] (beat 6 WorldCam session active). Beat 7 requires active DM observation context + facet selection (operator pick or default target per OQ-6.2.7-001). It completes beat 7 of the **DemoLoopOrchestrator** stage machine; beat 8 (**PlayerFeedbackChannel**) awaits overwrite outcome + rule echo.

## Scope

**In scope:** **OverwriteDemonstrationSlot** lifecycle (awaiting_dm_session → awaiting_facet → patch_preparing → veto_evaluating → applying → applied | vetoed | rolled_back | blocked); beat 7 entry gate on `demo.dm_cam_active` plus facet id resolved; **DMOverwriteClass** `live_patch` only (3.3 authority — demo excludes `canon_touching_patch` and `structural_re_gen`); **LiveOverwriteRegistry** demo-truncated token for `live_patch` mood nudge (single registry row — execution owns full registry); **OverwritePatchLayer** ordered patch apply on stub **WorldState** facet `demo_shrine_mood` (seeded in 6.2.1); demo patch payload table (mood/atmosphere nudge — conceptual, not terrain surgery); **NarrativeDeltaVetoPolicy** pre-commit evaluation (3.3 — demo-truncated: accept | veto | rollback); **RollbackWindow** on veto (patch not committed); `demo.overwrite_applied` or `demo.overwrite_vetoed` on `session.*`; `presentation.overwrite_outcome` echo on **HUDLayerStack** **Transient** layer (beat 8 precursor); **DemoLoopOrchestrator** beat 7 entry/exit gates; **HorizonDemoManifest** `strict_ordering: true` rejection of overwrite before DM cam.

**Out of scope:** **SpawnBootstrapController** through **DMCamTransitionSlot** (beats 1–6); **PlayerFeedbackChannel** full loop summary (beat 8); **ReGenerationIntentQueue** and **StructuralChangeDetector** (3.3 — not exercised in v1 loop); **CanonConflictArbiter** / **LoreHookRegistry** mutation (2.2 deferred); **SpeculativeDeltaReconciler** merge against 3.1 queue (no speculative queue in demo stub); factory catalog attestation (6.1); execution-track Godot patch serializers, C# **OverwritePatchLayer** types, or HR rollup gates.

## Behavior

**Actors:** **OverwriteDemonstrationSlot** (beat 7 owner), **OverwritePatchLayer** (3.3 — ordered patch apply), **NarrativeDeltaVetoPolicy** (3.3 — pre-commit veto), **LiveOverwriteRegistry** (3.3 — demo-truncated token for `live_patch`), **DemoLoopOrchestrator** (stage gate machine), **DMCamTransitionSlot** (6.2.6 — upstream DM session), **SpawnBootstrapController** stub facet authority (6.2.1 — `demo_shrine_v1` / `demo_shrine_mood`).

**Ordering:** DemoLoopOrchestrator opens beat 7 gate on `demo.dm_cam_active` → **OverwriteDemonstrationSlot** resolves facet id → build demo patch descriptor → **NarrativeDeltaVetoPolicy** evaluates → **OverwritePatchLayer** applies or rolls back → emit `demo.overwrite_applied` or `demo.overwrite_vetoed` on `session.*` → DemoLoopOrchestrator advances to beat 8 eligibility.

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| awaiting_dm_session | DemoLoopOrchestrator beat 7 gate eligible | awaiting_facet when `demo.dm_cam_active` observed | blocked if beat 6 incomplete |
| awaiting_facet | awaiting_dm_session exit | patch_preparing when facet id resolved | blocked if facet unknown |
| patch_preparing | facet selected | veto_evaluating when patch descriptor built | blocked if patch class ≠ `live_patch` |
| veto_evaluating | patch_preparing exit | applying when **NarrativeDeltaVetoPolicy** accepts | vetoed → rolled_back on veto |
| applying | veto_evaluating accept | applied when patch committed | blocked on apply failure |
| applied | applying success | DemoLoopOrchestrator stage 7 → 8 eligible; emit `demo.overwrite_applied` | — |
| vetoed | veto_evaluating reject | rolled_back; emit `demo.overwrite_vetoed` | — |
| rolled_back | veto or apply abort | terminal for beat 7 patch; loop may still advance per manifest | — |
| blocked | precondition failure | terminal until operator reset | — |

### Entry gates (beat 7 eligibility)

| Guard | Source | Demo v1 contract |
|---|---|---|
| `demo.dm_cam_active` | **6.2.6** on `session.*` | WorldCam DM session active |
| `facet_id_known` | Operator selection or default | Target `demo_shrine_mood` (6.2.1 stub facet) |
| `overwrite_class_live_patch` | Patch descriptor | Reject `structural_re_gen` / `canon_touching_patch` in v1 |
| `strict_ordering` | **HorizonDemoManifest** | Overwrite blocked before beat 6 complete |

### Demo patch descriptor (`live_patch` on `demo_shrine_mood`)

Per parent 6.2 **OverwriteDemonstrationSlot** and 3.3 taxonomy:

| Field | Demo v1 value |
|---|---|
| `overwrite_class` | `live_patch` |
| `facet_id` | `demo_shrine_mood` (child of `demo_shrine_v1` POI from 6.2.1) |
| `patch_kind` | `atmosphere_nudge` (conceptual — mood/atmosphere scalar shift) |
| `patch_payload` | e.g. `mood: contemplative → solemn` (display string + stub scalar — execution owns schema) |
| `provenance` | DM session id stub from beat 6 — **ProvenanceEnvelope** execution-deferred |
| `canon_touch` | `none` — no **CanonFact** proposals |

**ReGenerationIntentQueue** is **not** enqueued in v1 — structural re-gen remains 3.3 out-of-loop documentation only.

### NarrativeDeltaVetoPolicy (demo-truncated)

| Outcome | Beat 7 behavior |
|---|---|
| `accept` | **OverwritePatchLayer** commits patch; proceed to `applied` |
| `veto` | Patch discarded; **RollbackWindow** ensures no **WorldState** mutation; `demo.overwrite_vetoed`; loop may still reach beat 8 with veto flag per parent edge case |
| `retroactive_veto` | **Not exercised** in v1 — no 3.2 `dm_queue` backlog in demo stub |

Teachable veto path: operator may trigger demo patch that fails veto policy (execution script) to surface `presentation.overwrite_outcome` toast — conceptual only; default demo script uses accept path.

### Bus conventions

> **IRA annotation (GAP-7 — bus namespace convention):** Beat 7 stage signals use `demo.overwrite_applied` / `demo.overwrite_vetoed` on `session.*` **by DemoLoopOrchestrator convention** (same family as prior beats). Presentation echoes use `presentation.overwrite_outcome` on **HUDLayerStack** **Transient** layer — beat 8 **PlayerFeedbackChannel** may aggregate. Full bus registration remains **execution-deferred**.

| Signal | Bus | When |
|---|---|---|
| `demo.dm_cam_active` | `session.*` | Upstream beat 6 complete (entry eligibility) |
| `demo.overwrite_applied` | `session.*` | Patch committed successfully |
| `demo.overwrite_vetoed` | `session.*` | **NarrativeDeltaVetoPolicy** rejected patch |
| `presentation.overwrite_outcome` | `presentation.*` | Transient toast (applied / vetoed messaging) |
| `rule.demo_pass` / `rule.demo_fail` | **RuleEffectBus** (5.1) | Read-only context for beat 8 feedback — not re-emitted by beat 7 |

### Beat 7 → beat 8 handoff

- **Default exit:** `demo.overwrite_applied` → **PlayerFeedbackChannel** (beat 8) composes loop feedback from overwrite + rule outcome.
- **Veto exit:** `demo.overwrite_vetoed` → beat 8 still eligible per parent — toast explains veto; optional `demo.loop_complete` may carry veto flag.
- FP return / WorldCam teardown is **out of scope** for beat 7 completion — forward beat order through feedback.

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.2.7 consumes it |
|---|---|
| `demo.dm_cam_active` on `session.*` (6.2.6) | Beat 7 eligibility gate |
| `demo_shrine_mood` stub facet (6.2.1) | Patch target facet id |
| **DMOverwriteClass** + **OverwritePatchLayer** (3.3) | Patch taxonomy + apply seam |
| **NarrativeDeltaVetoPolicy** (3.3) | Pre-commit veto evaluation |
| **DMPauseGate** (3.1) | Apply at commit boundary while sim stub paused (6.2.4) |
| **HUDLayerStack** Transient layer (6.1.3) | Overwrite outcome toast precursor |

**Exports to downstream beats:**

| Export | Consumer |
|---|---|
| `demo.overwrite_applied` / `demo.overwrite_vetoed` on `session.*` | **DemoLoopOrchestrator** progress (beat 7→8); **PlayerFeedbackChannel** (beat 8) |
| `presentation.overwrite_outcome` | Operator UX; beat 8 aggregation |
| Patched stub facet state (conceptual) | Operator telemetry; execution replay tests |

**Explicit non-import:** **ReGenerationIntentQueue**, **StructuralChangeDetector**, **CanonRegistry** write path, **RuleCheckProbe** re-evaluation, factory **DevLeakageGuard** weakening.

## Edge Cases

| Case | Handling |
|---|---|
| Operator attempts overwrite before `demo.dm_cam_active` | **Rejected** per `strict_ordering: true` — blocked state |
| Facet id not in stub catalog | **blocked** — toast explains unknown facet |
| Patch classified as `structural_re_gen` | **Rejected** at `patch_preparing` — v1 demo allows `live_patch` only |
| **NarrativeDeltaVetoPolicy** vetoes patch | **rolled_back** — no **WorldState** mutation; `demo.overwrite_vetoed`; loop may continue |
| Apply failure after veto accept | **blocked** — operator retry; no partial commit |
| DM session lost mid-beat-7 | **blocked** — requires beat 6 re-entry (execution recovery) |
| Overwrite succeeds but rule was `demo_fail` | Valid — beat 7 independent of rule pass; beat 8 surfaces combined feedback |

## Open Questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.2.7-001 | Single default facet vs operator picker UI? | **Default `demo_shrine_mood`** for v1 kiosk; operator picker execution stretch |
| OQ-6.2.7-002 | Teachable veto script in demo? | **Optional execution profile** — default demo path uses accept; veto path documented for playtest |
| OQ-6.2.7-003 | Patch visible in FP before DM cam? | **No** — patch applies during DM session; FP sees outcome only after return (execution presentation) |

## Pseudo-code readiness

Reader can sketch **OverwriteDemonstrationSlot** state machine (awaiting_dm_session → … → applied | vetoed | rolled_back), `live_patch` descriptor table, **NarrativeDeltaVetoPolicy** outcomes, and beat 7/8 handoff without guessing **DMOverwriteClass** ids or facet naming from 6.2.1. Execution track owns typed patch interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.2.7 tertiary — OverwriteDemonstrationSlot overwrite demo (depth-first backfill; beat 7 of 8-beat demo loop)
- [x] Depth-first continue → 6.2.8 PlayerFeedbackChannel (beat 8) OR advance-phase gate evaluation
