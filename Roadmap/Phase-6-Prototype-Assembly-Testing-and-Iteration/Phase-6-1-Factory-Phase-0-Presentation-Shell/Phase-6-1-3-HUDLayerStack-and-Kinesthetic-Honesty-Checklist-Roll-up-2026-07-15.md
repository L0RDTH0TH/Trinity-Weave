---
title: Phase 6.1.3 — HUDLayerStack and Kinesthetic Honesty Checklist (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: 6.1.3
project-id: genesis-mythos-master
status: active
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- hud
- kinesthetic-honesty
- presentation-shell
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]'
body_compact_source_queue: followup-deepen-phase613-tertiary-20260716T024134Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.1.3 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-15 (`followup-deepen-phase613-tertiary-20260716T024134Z`).

## Archived body (pre-compact)

## Phase 6.1.3 — HUDLayerStack and Kinesthetic Honesty Checklist

Decomposes the **HUD** stage and **KinestheticHonestyChecklist** attestation gate from parent [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]: **HUDLayerStack** layer model, mode-reflective chrome, prerequisite on `presentation.play_region_ready`, and operator **KH-6.1-001..004** pass/fail criteria for factory Phase 0 catalog sign-off. Nouns and ordering only — no Godot Control tree or C# types.

> **Parent boundary:** This slice begins after `presentation.play_region_ready` ([[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]) and completes the **6.1** depth-first tertiary triad (Launch → PlayRegion → HUD). Horizon demo eight-beat loop (**6.2**) consumes **Transient** layer slots — not redefined here.

## Scope

**In scope:** **HUDLayerStack** lifecycle (dormant → initializing → active | blocked); four-layer model (**Base**, **Mode**, **Context**, **Transient**); read-only subscription to **PerspectiveEnvelope** / mode hint (4.1); minimal action affordances (Settings stub, Quit per parent OQ-6.1-003); **KinestheticHonestyChecklist** criteria table **KH-6.1-001..004** with pass/fail semantics and factory attestation gate; integration with **PresentationShellManifest** `attestation_gates`; ordering invariant Launch → PlayRegion → HUD audited by **KH-6.1-003**.

**Out of scope:** **LaunchFlowController** and **DevLeakageGuard** (**6.1.1**); **PlayRegionHost** mount (**6.1.2**); demo loop beats and **PlayerFeedbackChannel** content (**6.2**); automated screenshot diff CI (**OQ-6.1-004** execution-deferred); execution-track Godot CanvasLayer ordering (execution-deferred / advisory).

## Behavior

**Actors:** **HUDLayerStack** (chrome owner), **PerspectiveEnvelope** read handle (4.1), **PlayRegionMountReceipt** (from 6.1.2), operator (kinesthetic attestation), **PresentationShellManifest** attestation registry.

**Ordering:** `presentation.play_region_ready` received → validate mount receipt → initialize layer stack bottom→top → emit `presentation.hud_active` on `presentation.*` bus → operator may run **KinestheticHonestyChecklist** before catalog sign-off.

| HUD state | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| dormant | Host init / pre-PlayRegion | initializing when `play_region_ready` + valid receipt | — |
| initializing | dormant exit + receipt valid | active when all four layers registered | blocked when PlayRegion not ready or receipt invalid |
| active | init success | persists until session teardown | — |
| blocked | init before `play_region_ready` or invalid receipt | terminal until PlayRegion recovers | no partial chrome above world viewport |

**Layer stack (bottom → top):**

| Layer id | Purpose | Visibility rule | Demo consumer (6.2) |
|---|---|---|---|
| **Base** | Persistent session chrome (session label, build profile badge) | Always when **active** | — |
| **Mode** | Player vs DM indicator; rig badge (FP / WorldCam / MapCam / unknown) | Driven by read-only **PerspectiveEnvelope** mode hint | **DMCamTransitionSlot** beat 6 |
| **Context** | Minimal contextual actions (Settings stub, Quit) | When **active**; no gameplay actions at factory Phase 0 | — |
| **Transient** | Toast / feedback slot (empty at factory attestation) | On-demand; stack does not auto-show | **PlayerFeedbackChannel** beat 8 |

**Mode layer contract:** HUD **reflects** mode — it does **not** initiate **ModeTransitionGraph** edges (4.2 authority). When mode hint is `unknown`, **Mode** layer shows explicit **unknown** badge; does not block **active** state (parent 6.1 edge case).

**KinestheticHonestyChecklist** (operator attestation — factory Phase 0 catalog gate):

| Criterion ID | Check | Pass condition | Fail condition | Owner slice |
|---|---|---|---|---|
| **KH-6.1-001** | DM ortho feel | Operator reports tactical **WorldCam** viewport stable at default zoom — no disorienting roll, no unintended perspective drift during 30s observation | Nausea, roll drift, or inability to maintain tactical read within 30s | 4.1 + PlayRegion **dm_worldcam_slot** |
| **KH-6.1-002** | WorldCam ↔ MapCam transition readability | Rig switch completes with identifiable target rig within **3s**; **Mode** layer shows correct rig badge before interaction resumes | Ambiguous blend state, wrong mode badge, or operator cannot name active rig after transition | 4.2 + **HUDLayerStack** **Mode** |
| **KH-6.1-003** | FP → DM entry clarity | **LaunchFlowController** → **PlayRegionHost** → **HUDLayerStack** ordering perceptible; first DM rail activation does not skip **PlayRegion** mount; HUD does not render **active** before `presentation.play_region_ready` | Player-visible skip of launch/region stage or HUD chrome before `presentation.play_region_ready` | 6.1.1 → 6.1.2 → **this slice** |
| **KH-6.1-004** | SensoriumAttach boundary (read-only) | When **SensoriumAttach** blocked (e.g. dominate active per 4.2), operator receives explicit blocked-state messaging — no silent fallback to agency-bearing input | Silent attach or input routes to sim without guard messaging | 4.2 guard registry |

All four must pass for **PresentationShellManifest** kinesthetic attestation row; any fail keeps scope `factory_staged` on execution track — conceptual slice may still be **complete** (execution gap advisory).

**Attestation workflow (conceptual):**

1. Factory build reaches **HUDLayerStack** **active** with **DevLeakageGuard** pass (6.1.1).
2. Operator exercises DM WorldCam + optional MapCam stub per **KH-6.1-001/002**.
3. Operator verifies launch funnel ordering per **KH-6.1-003**.
4. Operator triggers blocked attach scenario per **KH-6.1-004** (stub OK).
5. Pass/fail recorded on execution track; conceptual track declares criteria only.

## Interfaces

**Imports:** `presentation.play_region_ready` + **PlayRegionMountReceipt** (6.1.2; legacy prose alias **PlayRegionReady** = same bus string); **Presentation layer** + `presentation.*` bus (1.1); **PerspectiveEnvelope** read-only mode hint (4.1); **ModeTransitionGraph** guard awareness (4.2) for **KH-6.1-004** messaging contract.

**Exports:** `presentation.hud_active` event; **HUDLayerRegistry** snapshot (layer ids, visibility state); **KinestheticHonestyChecklist** criteria reference for **PresentationShellManifest**; failure codes `hud_init_blocked`, `hud_prerequisite_missing`.

**Downstream consumers:** Phase **6.2** **PlayerFeedbackChannel** mounts into **Transient** layer; **DemoLoopOrchestrator** assumes **Mode** badge reflects DM cam beat; Phase **6.3** **AttestationSeparationPolicy** separates factory kinesthetic sign-off from demo loop attestation.

## Edge cases

| Case | Handling |
|---|---|
| HUD init attempted before `play_region_ready` | **blocked** state; emit `hud_prerequisite_missing`; no partial layer render |
| Mode hint unavailable at init (4.1 stub) | **Mode** layer shows **unknown** badge; stack reaches **active** — flagged for 6.2 wiring |
| Operator attestation fails **KH-6.1-001** only | Scope `factory_staged`; other criteria may pass — remediation targets WorldCam rig / PlayRegion socket |
| Transient layer receives demo toast before factory attestation | Allowed for integrated demo builds (6.2); factory-only attestation build keeps **Transient** empty |
| **KH-6.1-003** fail (HUD visible before PlayRegion) | Critical ordering violation; blocks factory catalog sign-off; fix ordering in execution track mount sequence — fail when HUD **active** before `presentation.play_region_ready` |
| Session teardown while **active** | Stack transitions **dormant**; layers hide; remount requires fresh PlayRegion **ready** |

## Open questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.1.3-001 | Should **Context** layer include "Resume" stub for factory attestation? | **Optional** — Settings + Quit sufficient per parent OQ-6.1-003; Resume deferred to 6.2 session continuity |
| OQ-6.1.3-002 | Minimum **Mode** badge set at factory Phase 0? | **FP**, **WorldCam**, **unknown** required; **MapCam** optional unless **KH-6.1-002** needs it |
| OQ-6.1.3-003 | Checklist attestation: single operator session vs multi-session aggregate? | **Single attestation session** for factory Phase 0; re-run required after material HUD/rig changes |

## Pseudo-code readiness

Reader can sketch HUDLayerStack state table, four-layer visibility rules, prerequisite gate on PlayRegion receipt, mode-reflective **Mode** layer, and kinesthetic pass/fail checklist without API signatures. Execution track owns typed interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.1.3 tertiary — HUDLayerStack + KinestheticHonestyChecklist (depth-first backfill; closes 6.1 branch)
- [x] Parent 6.1 branch closed → depth-first 6.2 eight-beat tertiaries OR advance-phase gate (next queue step)

