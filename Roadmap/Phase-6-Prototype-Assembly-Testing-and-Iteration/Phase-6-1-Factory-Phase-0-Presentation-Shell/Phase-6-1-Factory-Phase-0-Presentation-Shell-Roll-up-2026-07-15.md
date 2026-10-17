---
title: Phase 6.1 — Factory Phase 0 Presentation Shell (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: '6.1'
project-id: genesis-mythos-master
status: active
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- presentation-shell
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
body_compact_source_queue: followup-deepen-phase61-secondary-20260716T012010Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.1 Roll-up — archive of pre-compact feedstock

Canonical compact secondary: [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-15 (`followup-deepen-phase61-secondary-20260716T012010Z`).

## Archived body (pre-compact)

## Phase 6.1 — Factory Phase 0 Presentation Shell

First **factory catalog row** on the Half A spine: a player-facing **presentation shell** that proves factory law (operator-attested scopes, kinesthetic honesty, no dev-only leakage) before full proc-gen or horizon demo gameplay wiring. Flow: **launch → PlayRegion → HUD**.

> **Dual-track boundary:** This slice is **factory spine only**. It does **not** implement the horizon demo v1 gameplay loop (spawn → FP explore → intent stub → sim stub → rule check → DM cam → overwrite → feedback) — that is Phase **6.2**. Do not conflate factory Phase 0 catalog proof with playable demo assembly.

## Scope

**In scope:** **PresentationShellManifest** (catalog row contract for `ui_presentation_shell` or successor scope id); **LaunchFlowController** (cold start → session bootstrap gate → PlayRegion entry); **PlayRegionHost** (single active play viewport container; hosts world view + rig attachment points without owning sim/rule logic); **HUDLayerStack** (layered player/DM chrome: status, mode indicator, minimal action affordances); **KinestheticHonestyChecklist** (DM ortho + WorldCam/MapCam feel gates per PMG); **DevLeakageGuard** (no debug panels, editor-only overlays, or factory conductor UI in player build); integration hooks to Phase **1.1** Presentation layer and Phase **4.1** camera/perspective envelope (read-only attachment, not full rig wiring).

**Out of scope:** Horizon demo v1 gameplay loop and M0–M8 mint (Phase **6.2**); factory vs demo boundary glue policy (Phase **6.3**); full proc-gen pipeline, Azgaar/WebView, multiplayer (deferred post demo v1 per PMG); execution-track Godot scene graph, C# types, and rollup HR gates (execution-deferred / advisory on conceptual track); RuleEngine tick integration, spell/quest plugins (Phase 5.x consumers attach later on execution track).

## Behavior

### Launch → PlayRegion → HUD flow

Three-stage player-facing funnel — each stage is a **named factory scope boundary**, not a Godot scene name mandate:

| Stage | Actor | Input | Output | Ordering |
|---|---|---|---|---|
| **Launch** | Player / operator | App start, session profile selection (stub OK) | **LaunchFlowController** completes bootstrap checklist; emits `presentation.launch_complete` on `presentation.*` bus | Must complete before PlayRegion mount |
| **PlayRegion** | Presentation host | `launch_complete` + session context handle | **PlayRegionHost** mounts active viewport; exposes rig attachment sockets (FP baseline, DM WorldCam slot) without binding sim tick | Single active PlayRegion per session |
| **HUD** | Presentation chrome | PlayRegion mount + mode context from **PerspectiveEnvelope** read handle (4.1) | **HUDLayerStack** renders mode-appropriate layers (player chrome vs DM chrome); subscribes to mode transitions, does not drive them | Layers stack bottom→top: world chrome, status, mode badge, action strip |

**LaunchFlowController** responsibilities:

- Validate session bootstrap prerequisites (canon profile stub, ToneProfile selection stub, or explicit "demo bypass" flag for factory-only builds).
- Run **DevLeakageGuard** scan: reject build configs that expose factory conductor, queue debugger, or vault paths in player-facing UI.
- Hand off to **PlayRegionHost** with a **PresentationSessionHandle** (session id, active mode hint, attachment registry id).

**PlayRegionHost** responsibilities:

- Own the **single** active play viewport container (world rendering surface + camera rig mount points).
- Do **not** own simulation tick, rule evaluation, or intent parsing — those remain downstream stubs until horizon demo (6.2) or execution wiring.
- Publish **PlayRegionReady** event on `presentation.*` bus when mount completes (canonical bus string: `presentation.play_region_ready`; legacy alias **PlayRegionReady** retained in prose only).

**HUDLayerStack** responsibilities:

- Layer model: **Base** (persistent session chrome), **Mode** (player vs DM indicator), **Context** (minimal contextual actions — e.g. "Resume", "Settings stub"), **Transient** (toast/feedback slot).
- Mode layer visibility driven by read-only subscription to **PerspectiveEnvelope** / mode hint — HUD reflects mode, does not initiate **ModeTransitionGraph** edges (4.2 authority).
- **KinestheticHonestyChecklist** gates: DM ortho feel and WorldCam/MapCam transition readability must pass operator attestation before catalog row sign-off (execution track implements checklist UI; conceptual track declares criteria).

### Factory catalog row contract

**PresentationShellManifest** is the Half A catalog artifact this slice names:

| Field | Contract |
|---|---|
| `scope_id` | `ui_presentation_shell` (or successor id minted at catalog row creation) |
| `target_depth` | L5 presentation + L4 launch/region/HUD decomposition (execution track) |
| `attestation_gates` | KinestheticHonestyChecklist pass; DevLeakageGuard pass; launch→PlayRegion→HUD ordering invariant |
| `track_authority` | **Factory spine** — not horizon demo v1 |
| `downstream_consumers` | Phase 6.2 mounts gameplay stubs **into** PlayRegionHost sockets; Phase 6.3 documents boundary |

### DevLeakageGuard

Player-facing builds must not surface:

- Factory conductor / product-factory queue UI
- Vault paths, roadmap notes, or MCP debug panels
- Editor-only gizmo overlays or hot-reload indicators
- Unattributed "WIP" placeholders without **PresentationShellManifest** exception list entry

Violations block catalog row attestation until remediated or explicitly waived in operator scope sign-off (execution track).

### KinestheticHonestyChecklist

Operator attestation gate for factory Phase 0 catalog sign-off. Each criterion is **pass/fail** at conceptual depth; execution track may add automated screenshot diff (OQ-6.1-004 advisory only).

| Criterion ID | Check | Pass condition | Fail condition |
|---|---|---|---|
| **KH-6.1-001** | DM ortho feel | Operator reports tactical **WorldCam** viewport is stable at default zoom — no disorienting roll, no unintended perspective drift during 30s observation | Nausea, roll drift, or inability to maintain tactical read within 30s |
| **KH-6.1-002** | WorldCam ↔ MapCam transition readability | Rig switch completes with identifiable target rig within **3s**; **HUDLayerStack** **Mode** layer shows correct rig badge before interaction resumes | Ambiguous blend state, wrong mode badge, or operator cannot name active rig after transition |
| **KH-6.1-003** | FP → DM entry clarity | **LaunchFlowController** → **PlayRegionHost** → **HUDLayerStack** ordering is perceptible; first DM rail activation does not skip **PlayRegion** mount | Player-visible skip of launch/region stage or HUD renders before `presentation.play_region_ready` |
| **KH-6.1-004** | SensoriumAttach boundary (read-only) | When **SensoriumAttach** is blocked (e.g. dominate active per 4.2), operator receives explicit blocked-state messaging — no silent fallback to agency-bearing input | Silent attach or input routes to sim without guard messaging |

All four must pass for **PresentationShellManifest** `attestation_gates` kinesthetic row; failures keep scope `factory_staged` on execution track (conceptual slice may still be complete).

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.1 consumes it |
|---|---|
| **Presentation layer** + `presentation.*` bus (1.1) | Event channel for `launch_complete`, `presentation.play_region_ready`, `presentation.hud_active`, HUD layer updates |
| **InputIntent layer** (1.1) | Launch/settings affordances route through intent bus — stub handlers OK for factory Phase 0 |
| **PerspectiveEnvelope** + **CameraInterpolatorRegistry** (4.1) | Read-only mode hint + rig attachment socket definitions for PlayRegionHost |
| **ModeTransitionGraph** guard awareness (4.2) | HUD reflects mode; does not fire transitions |
| **SeamRegistry** presentation seam family (1.3) | PlayRegionHost registers as presentation seam consumer |

**Exports to downstream phases:**

| Export | Consumer |
|---|---|
| **PresentationShellManifest** | Half A catalog mint; execution track scope attestation |
| **PlayRegionHost** attachment sockets | Phase 6.2 horizon demo: FP explore, intent stub, sim stub mount points |
| **HUDLayerStack** layer ids | Phase 6.2 feedback toasts; Phase 4.x mode chrome extensions |
| **KinestheticHonestyChecklist** criteria | Operator attestation workflow; execution track checklist UI |
| **DevLeakageGuard** policy | CI/player-build gate on execution track |

**Explicit non-import (dual-track):** Phase 5.x **RuleEngineCore**, Phase 3.x **SimTickPipeline**, Phase 2.x proc-gen executors — **not** wired in 6.1. Factory Phase 0 proves presentation shell only.

## Edge Cases

| Case | Handling |
|---|---|
| Launch completes but PlayRegion mount fails (viewport init error) | **LaunchFlowController** rolls back to launch screen with `play_region_mount_failed` user message; no partial HUD render |
| Multiple PlayRegion mount requests in same session | **PlayRegionHost** rejects second mount; log `duplicate_play_region` on `presentation.*` bus; first mount wins |
| Mode hint unavailable at HUD init (4.1 stub not wired) | **HUDLayerStack** defaults to **Base** + **Mode: unknown** badge; does not block PlayRegion; flagged for 6.2 wiring |
| Factory build accidentally includes debug menu | **DevLeakageGuard** fails attestation gate; catalog row blocked until build profile corrected |
| Operator attestation fails kinesthetic checklist | Scope remains `factory_staged`; no execution-track sign-off; conceptual slice still complete — execution gap advisory |
| Session bootstrap bypass flag set (factory-only CI) | **LaunchFlowController** skips canon/ToneProfile stubs; must still run DevLeakageGuard |

## Open Questions

| ID | Question | Conceptual authority decision |
|---|---|---|
| OQ-6.1-001 | Catalog scope id: retain `ui_presentation_shell` from PMG or mint successor at catalog row creation? | **PMG default stands** (`ui_presentation_shell`); Half A catalog mint may rename with provenance link — execution track records id in **PresentationShellManifest** |
| OQ-6.1-002 | PlayRegion: single persistent viewport vs allow scene swap within host? | **Single active PlayRegion per session** for factory Phase 0; scene swap is execution-track optimization — conceptual contract locks one host |
| OQ-6.1-003 | HUD action strip: empty stub vs minimal "Settings / Quit" for factory attestation? | **Minimal affordances allowed** (Settings stub, Quit) — proves layer stack without gameplay actions; full action strip deferred to 6.2 |
| OQ-6.1-004 | Kinesthetic checklist: operator manual attestation vs automated screenshot diff? | **Operator manual attestation** for factory Phase 0; automated diff is execution-track CI enhancement — advisory only on conceptual track |

## Pseudo-code readiness

Reader can sketch launch controller state machine (idle → bootstrapping → launch_complete → failed), PlayRegion mount lifecycle, and HUD layer visibility rules without guessing core behavior. No pseudo-code blocks in this conceptual slice — execution track owns typed interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.1 secondary with factory Phase 0 presentation shell (launch → PlayRegion → HUD)
- [x] Dual-track boundary documented — factory spine NOT horizon demo v1 (Phase 6.2)
- [x] Handoff to 6.2 horizon demo v1 gameplay loop — breadth continue 1/3

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

## Consistency Reports

> [!note]
> Post-mint: execution rollup gates, REGISTRY-CI, HR closure artifacts, and Godot scene implementation are execution-deferred / advisory on conceptual track per conceptual_v1 contract. Factory Phase 0 catalog attestation is out of scope for conceptual completion — resolved on execution track / Half A operator sign-off.

Minted 2026-06-26 (godo-followup-20260626T185832Z-phase6-deepen-6-1); persona: half_a.conceptual_architect; product_factory_run_id: f35ff65cfb4f; pre_create_gate: skipped_conceptual_track; dual_track: factory_spine_not_horizon_demo; execution_gaps_advisory: true.

