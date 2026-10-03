---
title: Phase 6.2.1 — SpawnBootstrapController Session Bootstrap (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: 6.2.1
project-id: genesis-mythos-master
status: active
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- horizon-demo
- spawn-bootstrap
- beat-1
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]'
body_compact_source_queue: followup-deepen-phase621-tertiary-20260716T030605Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.2.1 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-15 (`followup-deepen-phase621-tertiary-20260716T030605Z`).

## Archived body (pre-compact)

## Phase 6.2.1 — SpawnBootstrapController Session Bootstrap

Decomposes **beat 1 (Spawn)** of the eight-beat horizon demo loop from parent [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]: **SpawnBootstrapController** session-handle consumption, stub world facet initialization, **PlayerFPRig** socket attachment, and `demo.spawn_complete` emission gate. Nouns and ordering only — no Godot Node types or C# spawn APIs.

> **Parent boundary:** This slice begins after `presentation.play_region_ready` from [[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]] and the **PresentationSessionHandle** handoff from [[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]. It completes beat 1 of the **DemoLoopOrchestrator** stage machine; beat 2 (**FPExploreRigHost**) awaits `demo.spawn_complete`.

## Scope

**In scope:** **SpawnBootstrapController** lifecycle (idle → bootstrapping → spawned | failed); **PresentationSessionHandle** consumption and validation from 6.1.1; stub world facet specification (single named POI + terrain placeholder — no Phase 2 **CompiledWorldManifest**); **PlayerFPRig** attachment to **PlayRegionHost** `fp_baseline_rig` socket (6.1.2); `demo.spawn_complete` emission gate on `presentation.play_region_ready` (canonical bus string — not bare `PlayRegionReady`); blocking behavior and `demo.spawn_blocked_no_play_region` toast; **DemoLoopOrchestrator** beat 1 entry/exit gate.

**Out of scope:** Full **UnifiedSceneGraph** load or **CompiledWorldManifest** from Phase 2 proc-gen; **PlayRegionHost** implementation (6.1.2); FP locomotion and look input (beat 2 — **FPExploreRigHost**); **IntentPipelineStub**, **SimTickStub**, **RuleCheckProbe**, **DMCamTransitionSlot**, **OverwriteDemonstrationSlot**, **PlayerFeedbackChannel** (beats 3–8); factory **PresentationShellManifest** catalog attestation (6.1); execution-track Godot Node tree, C# spawn APIs.

## Behavior

**Actors:** **SpawnBootstrapController** (beat 1 owner), **PlayRegionHost** (6.1.2 — FP socket provider), **PresentationSessionHandle** (6.1.1 export), **DemoLoopOrchestrator** (stage gate machine), **PlayerFPRig** (4.1 — rig attachment target).

**Ordering:** DemoLoopOrchestrator opens beat 1 gate → **SpawnBootstrapController** observes `presentation.play_region_ready` → validate **PresentationSessionHandle** → bootstrap stub world facet → attach **PlayerFPRig** to `fp_baseline_rig` socket → emit `demo.spawn_complete` on `session.*`.

> **IRA annotation (GAP-4 — bus namespace convention):** `demo.*` events (including `demo.spawn_complete`) are routed through the `session.*` bus **by DemoLoopOrchestrator convention** per the 6.2 secondary **HorizonDemoManifest** `loop_beats` contract. The `session.*` namespace is the orchestrator's inter-beat communication channel; `demo.*` is the event prefix identifying demo-loop stage signals within that namespace. The `session.*` bus namespace is **not** formally registered in any prior secondary; full bus namespace registration (namespacing policy, subscriber contracts, isolation from `presentation.*` and `input.*`) is **execution-deferred**. Conceptual validity: DemoLoopOrchestrator owns routing of `demo.*` stage events through `session.*`; execution track confirms namespace registration when wiring 6.2 beats. (IRA ira_reconciled; validator advisory GAP-4; 2026-06-27)

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| idle | DemoLoopOrchestrator beat 1 gate open | bootstrapping when `presentation.play_region_ready` observed + handle valid | — |
| bootstrapping | idle exit | spawned when stub facet committed + FPRig attached; emit `demo.spawn_complete` on `session.*` | failed on socket unavailable, handle invalid, or WorldEventLog init error |
| spawned | bootstrapping success | persists for demo session; DemoLoopOrchestrator advances to beat 2 | — |
| failed | bootstrapping error | terminal; emit `demo.spawn_blocked_no_play_region`; DemoLoopOrchestrator holds | |

### PresentationSessionHandle consumption

- **SpawnBootstrapController** receives the handle via the 6.1 launch-flow chain: **LaunchFlowController** (6.1.1) → **PlayRegionMountReceipt** (6.1.2) → session handle enriched with `play_region_socket_ref`.
- Required fields: `session_id`, `play_region_socket_ref` (pointing to `fp_baseline_rig`), `play_region_ready: true`.
- Controller validates `play_region_ready: true` before proceeding; stale or missing handle → `failed` state with `demo.spawn_blocked_no_play_region`.
- Does **not** re-run launch UI — handle is consumed, not re-created.

### Stub world facet

Minimal world payload sufficient for horizon demo v1 — no Phase 2 **CompiledWorldManifest** data:

| Facet field | Demo v1 value | Authority |
|---|---|---|
| Facet id | `demo_shrine_v1` | SpawnBootstrapController (conceptual stub) |
| Named sub-id | `demo_shrine_mood` | OverwriteDemonstrationSlot beat 7 — must match |
| Terrain | Flat placeholder — no heightfield tile load | Phase 2 exec-deferred |
| POI count | 1 (sufficient per OQ-6.2.1-002) | See OQ-6.2.1-002 |
| Entities | None at spawn; faction graph not initialized | 3.2 exec-deferred |
| WorldEventLog | Initialized empty; no SeedBundle pre-populate | 3.1 authority |

Stub world facet is committed to the **WorldEventLog** as a session-init record before `demo.spawn_complete` is emitted.

### PlayerFPRig attachment

- Attaches **PlayerFPRig** to `fp_baseline_rig` socket of **PlayRegionHost** (6.1.2 socket catalog).
- Does **not** activate **PerspectiveEnvelope** FP mode — that is beat 2 (**FPExploreRigHost**) responsibility (OQ-6.2.1-003 resolved: beat 2 owns mode activation).
- Does **not** initialize **UnifiedSceneGraph** or **CameraInterpolatorRegistry** (Phase 4.1 execution-deferred).
- FPRig state begins `inactive` post-attach; **FPExploreRigHost** drives `fp_active` on beat 2 entry.

### `demo.spawn_complete` gate

Emitted on `session.*` bus **only after all three preconditions satisfied:**
1. `presentation.play_region_ready` received from **PlayRegionHost** (canonical bus string per 6.1.2/6.1.3 — NOT bare `PlayRegionReady`).
2. Stub world facet committed to **WorldEventLog**.
3. **PlayerFPRig** attached to `fp_baseline_rig` socket.

On emission: **DemoLoopOrchestrator** advances stage index from 1 → 2 and opens beat 2 (**FPExploreRigHost**).

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.2.1 consumes it |
|---|---|
| `presentation.play_region_ready` bus signal + **PlayRegionMountReceipt** (6.1.2) | Prerequisite gate and socket reference for FPRig attach |
| **PresentationSessionHandle** (6.1.1 **LaunchFlowController** export) | Session validity gate; `play_region_socket_ref` field |
| PlayRegionHost `fp_baseline_rig` socket (6.1.2 socket catalog) | FPRig attachment target |
| **PlayerFPRig** (4.1 **PerspectiveEnvelope**) | Rig node attached to socket |
| **WorldEventLog** (3.1 tick core) | Stub world facet commit target |

**Exports to downstream beats:**

| Export | Consumer |
|---|---|
| `demo.spawn_complete` on `session.*` | **FPExploreRigHost** beat 2 entry gate |
| Stub world facet — facet id `demo_shrine_v1`, sub-id `demo_shrine_mood` | **OverwriteDemonstrationSlot** beat 7 target |
| **PlayerFPRig** attached-and-inactive state | **FPExploreRigHost** beat 2 owns mode activation |

**Explicit non-import:** Phase 2 **CompiledWorldManifest**, **SeedBundle**, **ToneProfileBundle** (execution-deferred for demo v1); factory **PresentationShellManifest** attestation (6.1 authority only).

> **IRA annotation (GAP-3 — execution-deferred field naming):** `play_region_socket_ref` is a **conceptual extension point** on the **PresentationSessionHandle** — it names the field that carries the `fp_baseline_rig` socket reference established in 6.1.1/6.1.2. Actual field name, type, and serialization format will be verified by the execution track when wiring 6.1.1 (**LaunchFlowController** export) to 6.1.2 (**PlayRegionMountReceipt** enrichment). Do not treat `play_region_socket_ref` as a finalized API identifier; it is a conceptual placeholder for the socket-reference slot on the handle. (IRA ira_reconciled; validator advisory GAP-3; 2026-06-27)

## Edge Cases

| Case | Handling |
|---|---|
| PlayRegion not mounted at spawn attempt | `failed` state; `demo.spawn_blocked_no_play_region` toast |
| PresentationSessionHandle expired or missing | `failed` state; DemoLoopOrchestrator holds at pre-beat-1 |
| `fp_baseline_rig` socket not available on PlayRegionHost | `failed` state; log; no partial rig attach |
| WorldEventLog init error | `failed` state; stub facet not committed; `demo.spawn_complete` withheld |
| Spawn attempted twice in same session | **DemoLoopOrchestrator** strict ordering rejects — no double-spawn; HorizonDemoManifest `strict_ordering: true` |
| `presentation.play_region_ready` arrives after FPRig already attached | Acceptable; gate check re-evaluates all three preconditions; emit once all pass |

## Open Questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.2.1-001 | Retry policy on `failed` state: single-attempt-per-session or retry on handle refresh? | **Single-attempt per session** for v1 — DemoLoopOrchestrator prevents retry without full session reset; retry semantics are execution-track concern |
| OQ-6.2.1-002 | Minimum POI count for stub world facet: one `demo_shrine_v1` sufficient? | **One POI sufficient** — `demo_shrine_v1` supports both beat 5 (rule check probe) and beat 7 (overwrite demonstration); second POI deferred to stretch |
| OQ-6.2.1-003 | FPRig attachment vs PerspectiveEnvelope FP mode: who activates? | **FPExploreRigHost (beat 2) owns mode activation** — SpawnBootstrapController attaches rig only; mode transition is beat 2 per 4.1 PerspectiveEnvelope authority |

## Pseudo-code readiness

Reader can sketch **SpawnBootstrapController** state machine (idle → bootstrapping → spawned | failed), session-handle consumption, stub world facet commit sequence, FPRig socket attachment, and `demo.spawn_complete` gate without guessing API signatures. Execution track owns typed Godot Node interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.2.1 tertiary — SpawnBootstrapController session bootstrap (depth-first backfill; beat 1 of 8-beat demo loop)
- [x] Depth-first continue → 6.2.2 FPExploreRigHost (beat 2) — minted [[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]

