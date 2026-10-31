---
title: Phase 6.1.1 — Launch Flow and DevLeakageGuard Session Bootstrap (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: 6.1.1
project-id: genesis-mythos-master
status: active
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- launch-flow
- dev-leakage
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
body_compact_source_queue: followup-deepen-phase611-tertiary-20260716T014300Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.1.1 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-15 (`followup-deepen-phase611-tertiary-20260716T014300Z`).

## Archived body (pre-compact)

## Phase 6.1.1 — Launch Flow and DevLeakageGuard Session Bootstrap

Decomposes the **Launch** stage from parent [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]: **LaunchFlowController** state machine, session bootstrap prerequisites, **DevLeakageGuard** scan policy, and **PresentationSessionHandle** handoff to **PlayRegionHost**. Nouns and ordering only — no Godot scene graph or C# types.

> **Parent boundary:** This slice ends at `presentation.launch_complete`. **PlayRegionHost** mount and **HUDLayerStack** init are sibling tertiaries (**6.1.2+**) — not redefined here.

## Scope

**In scope:** **LaunchFlowController** lifecycle states (idle → bootstrapping → launch_complete | failed); bootstrap prerequisite checklist (canon profile stub, ToneProfile selection stub, demo bypass flag semantics); **DevLeakageGuard** forbidden surface catalog and attestation fail path; **PresentationSessionHandle** fields emitted at handoff; `presentation.launch_complete` bus contract; rollback on bootstrap failure.

**Out of scope:** PlayRegion viewport mount (**6.1.2** territory); HUD layer stack (**6.1.3** territory); horizon demo spawn (**6.2**); factory vs demo glue (**6.3**); execution-track build pipeline CI wiring (execution-deferred / advisory).

## Behavior

**Actors:** Player/operator (start), **LaunchFlowController** (orchestrator), **DevLeakageGuard** (policy scanner), session profile stub (read-only), **PresentationSessionHandle** (immutable handoff token).

**Ordering:** App start → bootstrap checklist → **DevLeakageGuard** scan → on pass emit `presentation.launch_complete` + hand off **PresentationSessionHandle** → downstream **PlayRegionHost** may mount (parent 6.1).

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| idle | App start | bootstrapping when profile context available | — |
| bootstrapping | idle exit | launch_complete when checklist + guard pass | failed on guard fail or missing mandatory stub (unless bypass) |
| launch_complete | guard pass | terminal for this controller | — |
| failed | guard fail / bootstrap error | terminal; UI shows launch screen error | blocks PlayRegion |

**Bootstrap checklist (conceptual):**

| Check | Required when | Waived when |
|---|---|---|
| Session profile selected (stub OK) | default player build | `factory_phase0_only` CI profile may use fixed stub |
| Canon profile stub present | integrated builds | `demo_bypass` flag on factory-only attestation builds |
| ToneProfile selection stub | integrated builds | same bypass as canon |
| **DevLeakageGuard** scan | always | never waived for player-facing attestation builds |

**DevLeakageGuard** forbidden surfaces (non-exhaustive; parent 6.1 authority):

- Factory conductor / product-factory queue UI
- Vault paths, roadmap notes, MCP debug panels
- Editor gizmo overlays, hot-reload indicators
- Unattributed WIP placeholders outside **PresentationShellManifest** exception list

On violation: transition to **failed**; attestation gate blocks factory catalog sign-off until remediated or operator waiver recorded on execution track.

**PresentationSessionHandle** at handoff:

| Field | Contract |
|---|---|
| `session_id` | Stable for session lifetime |
| `active_mode_hint` | Read-only hint from **PerspectiveEnvelope** when wired; else `unknown` |
| `attachment_registry_id` | Registry slot for **PlayRegionHost** socket binding |
| `build_profile` | `factory_phase0_only` \| `horizon_demo_in_shell` \| `demo_debug` (conceptual; see 6.3) |

## Interfaces

**Imports:** `presentation.*` bus (1.1); **InputIntent** affordances for launch/settings stub (1.1); optional **PerspectiveEnvelope** read handle (4.1) for mode hint only.

**Exports:** `presentation.launch_complete` event; **PresentationSessionHandle**; **DevLeakageGuard** pass/fail attestation record (execution track persists); failure codes `play_region_mount_failed` reserved for downstream — launch stage emits `bootstrap_failed` / `dev_leakage_detected` only.

**Downstream consumers:** **PlayRegionHost** (parent 6.1) waits on `launch_complete`; Phase **6.2** **SpawnBootstrapController** consumes **PresentationSessionHandle** per **6.3** **MountContractGlue**.

## Edge cases

| Case | Handling |
|---|---|
| Bootstrap bypass flag set (factory-only CI) | Skip canon/ToneProfile stubs; **DevLeakageGuard** still runs |
| Guard pass but handoff handle allocation fails | **failed** state; no `launch_complete`; log `session_handle_alloc_failed` |
| Operator retries launch after failed guard | Full bootstrap + guard re-run from idle; no partial reuse of failed handle |
| Mode hint unavailable (4.1 stub) | **PresentationSessionHandle.active_mode_hint** = `unknown`; does not block launch_complete |
| Debug menu present in player build profile | **DevLeakageGuard** fails; factory attestation blocked |

## Open questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.1.1-001 | Should `demo_bypass` be a build-profile field only vs runtime launch flag? | **Build-profile authority** (6.3 **BuildProfileSelector**); runtime flag allowed only when profile explicitly enables it |
| OQ-6.1.1-002 | Minimum stub depth for canon/ToneProfile at factory Phase 0 attestation? | **Named stub ids sufficient** for conceptual completion; full resolver wiring execution-deferred |
| OQ-6.1.1-003 | Guard scan: static build manifest vs runtime UI tree walk? | **Static manifest required** for attestation; runtime walk is execution-track enhancement — advisory only |

## Pseudo-code readiness

Reader can sketch LaunchFlowController state table, bootstrap checklist gates, guard fail path, and session handle fields without API signatures. Execution track owns typed interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.1.1 tertiary — launch flow + DevLeakageGuard decomposition (depth-first backfill from oversized 6.1)
- [x] Mint 6.1.2 PlayRegionHost mount lifecycle tertiary — [[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]
- [x] Mint 6.1.3 HUDLayerStack + kinesthetic checklist tertiary — [[Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]
- [x] Parent 6.1 branch closed → depth-first 6.2 tertiaries or advance-phase gate (next queue step)

