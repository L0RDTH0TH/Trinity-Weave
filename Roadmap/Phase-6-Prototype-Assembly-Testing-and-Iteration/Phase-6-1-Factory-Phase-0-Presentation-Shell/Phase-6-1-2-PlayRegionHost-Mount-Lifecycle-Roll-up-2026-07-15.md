---
title: Phase 6.1.2 — PlayRegionHost Mount Lifecycle (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: 6.1.2
project-id: genesis-mythos-master
status: active
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- play-region
- presentation-shell
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
body_compact_source_queue: followup-deepen-phase612-tertiary-20260716T021200Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.1.2 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-15 (`followup-deepen-phase612-tertiary-20260716T021200Z`).

## Archived body (pre-compact)

## Phase 6.1.2 — PlayRegionHost Mount Lifecycle

Decomposes the **PlayRegion** stage from parent [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]: **PlayRegionHost** mount lifecycle, rig attachment socket registry, `presentation.play_region_ready` bus contract, and handoff prerequisites from [[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]. Nouns and ordering only — no Godot scene graph or C# types.

> **Parent boundary:** This slice begins after `presentation.launch_complete` and ends at `presentation.play_region_ready`. **HUDLayerStack** init is sibling tertiary **6.1.3** — not redefined here.

## Scope

**In scope:** **PlayRegionHost** lifecycle states (unmounted → mounting → ready | failed); prerequisite gate on **PresentationSessionHandle** + `presentation.launch_complete`; emit `presentation.play_region_ready` on `presentation.*` bus; rig attachment socket catalog (FP baseline, DM WorldCam slot); single-active-PlayRegion invariant; mount failure rollback to launch screen; **MountContractGlue** socket ids consumed by Phase **6.2** / **6.3**.

**Out of scope:** **LaunchFlowController** bootstrap and **DevLeakageGuard** (**6.1.1**); **HUDLayerStack** layer model (**6.1.3**); horizon demo eight-beat loop (**6.2**); sim tick, rule evaluation, intent parsing (downstream stubs); execution-track viewport init implementation (execution-deferred / advisory).

## Behavior

**Actors:** **PlayRegionHost** (viewport owner), **PresentationSessionHandle** (immutable input from launch), **SeamRegistry** presentation seam consumer (1.3), optional **PerspectiveEnvelope** read handle (4.1) for rig socket hints.

**Ordering:** `presentation.launch_complete` received → validate **PresentationSessionHandle** → mount active viewport → register rig sockets → emit `presentation.play_region_ready` → **HUDLayerStack** may init (**6.1.3**).

| State | Entry trigger | Exit / emit | Failure |
|---|---|---|---|
| unmounted | Host init / post-session teardown | mounting when `launch_complete` + valid handle | — |
| mounting | unmounted exit + handle valid | ready when viewport + socket registry complete | failed on viewport init error or invalid handle |
| ready | mount success | terminal for mount lifecycle (persists until session end) | — |
| failed | viewport init error / invalid handle / duplicate mount rejected | terminal; rollback signal to launch UI | blocks HUD init; no `presentation.play_region_ready` |

**Prerequisite gate (from 6.1.1):**

| Input | Required | Reject when |
|---|---|---|
| `presentation.launch_complete` event | always | absent or launch still **failed** |
| **PresentationSessionHandle** | always | missing, expired, or `session_handle_alloc_failed` lineage |
| `attachment_registry_id` | always | empty or unknown registry slot |
| `build_profile` | always | profile forbids PlayRegion (conceptual; see 6.3 **BuildProfileSelector**) |

**Rig attachment socket catalog (factory Phase 0):**

| Socket id | Purpose | Demo consumer (6.2 / 6.3) |
|---|---|---|
| `fp_baseline_rig` | First-person explore mount point | **FPExploreRigHost** |
| `dm_worldcam_slot` | DM WorldCam rail attachment | **DMCamTransitionSlot** |
| `mapcam_slot` | MapCam attachment (optional stub) | deferred to execution track |

Host publishes socket ids in mount receipt; **MountContractGlue** (6.3) is authoritative cross-track naming — this slice declares factory spine ids only.

**Single active PlayRegion invariant:** At most one **ready** mount per session. Second mount request while **ready** → reject with `duplicate_play_region` on `presentation.*` bus; first mount wins (parent 6.1 OQ-6.1-002 authority).

## Interfaces

**Imports:** `presentation.launch_complete` + **PresentationSessionHandle** (6.1.1); **Presentation layer** + `presentation.*` bus (1.1); **PerspectiveEnvelope** + **CameraInterpolatorRegistry** read-only rig hints (4.1); **SeamRegistry** presentation seam family registration (1.3).

**Exports:** `presentation.play_region_ready` event; **PlayRegionMountReceipt** (session id, socket registry snapshot, mount timestamp); failure codes `play_region_mount_failed`, `duplicate_play_region`, `play_region_prerequisite_missing`.

**Downstream consumers:** **HUDLayerStack** (6.1.3) waits on `presentation.play_region_ready`; Phase **6.2** **SpawnBootstrapController** mounts into sockets per **6.3** **MountContractGlue**; **KinestheticHonestyChecklist** **KH-6.1-003** audits Launch → PlayRegion → HUD ordering.

## Edge cases

| Case | Handling |
|---|---|
| Launch complete but viewport init fails | Transition **failed**; emit `play_region_mount_failed`; **LaunchFlowController** rollback to launch screen (parent 6.1); no partial HUD |
| Handle valid but `attachment_registry_id` mismatch | **failed**; log `play_region_prerequisite_missing`; no `presentation.play_region_ready` |
| Mode hint unavailable at mount (4.1 stub) | Mount proceeds; sockets register with default labels; **HUDLayerStack** may show **Mode: unknown** — does not block **ready** |
| Demo attempts mount before `launch_complete` | **SpawnBootstrapController** blocks per **MountContractGlue**; factory host stays **unmounted** |
| Session teardown while **ready** | Host transitions to **unmounted**; sockets deregister; demo stubs must detach before remount |
| Factory attestation build with debug viewport overlay | **DevLeakageGuard** (6.1.1) should have blocked at launch; if leak appears post-mount, attestation fails on execution track — conceptual documents ordering only |

## Open questions

| ID | Question | Conceptual authority |
|---|---|---|
| OQ-6.1.2-001 | Persist **ready** across scene swap within host vs remount? | **Single active PlayRegion per session** (parent OQ-6.1-002); internal scene swap is execution-track optimization — host state stays **ready** if socket registry preserved |
| OQ-6.1.2-002 | Minimum mount receipt fields for factory Phase 0 attestation? | **session_id + socket id list + mount timestamp** sufficient; screenshot diff execution-deferred |
| OQ-6.1.2-003 | MapCam socket mandatory at factory Phase 0? | **Optional stub** — FP + DM WorldCam slots required; MapCam deferred unless **KH-6.1-002** needs it for attestation |

## Research integration

External grounding from [[Ingest/Agent-Research/2026-06-27-influence-conceptual-deepen-gmm-040652Z]] (chain consumed, godo-509363bc2f08):

- **Launch handoff discipline:** No partial PlayRegion mount without **PresentationSessionHandle** — aligns with industry "no change_scene reset without full bootstrap" pattern cited for **LaunchFlowController** (research § LaunchFlowController bootstrap architecture).
- **Dual-track sockets:** Demo mounts into declared sockets only after factory ordering — **MountContractGlue** table in research § dual-track build profiles reinforces socket-bound demo attachment vs factory spine ownership.
- **Kinesthetic honesty:** **KH-6.1-003** requires perceptible Launch → PlayRegion → HUD ordering — this slice owns the PlayRegion stage visibility contract before HUD (**6.1.3**).

## Pseudo-code readiness

Reader can sketch PlayRegionHost state table, prerequisite gate, socket registry, duplicate-mount rejection, and rollback path without API signatures. Execution track owns typed interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.1.2 tertiary — PlayRegionHost mount lifecycle (depth-first backfill from oversized 6.1)
- [x] Mint 6.1.3 HUDLayerStack + kinesthetic checklist tertiary — [[Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]
- [x] Parent 6.1 branch closed → depth-first 6.2 tertiaries or advance-phase gate

