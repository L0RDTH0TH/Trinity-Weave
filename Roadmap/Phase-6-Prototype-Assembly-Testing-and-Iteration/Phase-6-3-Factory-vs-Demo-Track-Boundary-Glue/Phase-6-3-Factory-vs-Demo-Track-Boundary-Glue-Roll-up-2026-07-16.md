---
title: Phase 6.3 — Factory vs Demo Track Boundary Glue (Roll-up)
roadmap-level: roll-up
phase-number: 6
subphase-index: '6.3'
project-id: genesis-mythos-master
status: active
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-6
- roll-up
- dual-track
- boundary-glue
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roadmap-2026-06-26-2031]]'
body_compact_source_queue: followup-deepen-phase63-20260716T210004Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 6.3 Roll-up — archive of pre-compact feedstock

Canonical compact secondary: [[Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roadmap-2026-06-26-2031]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-16 (`followup-deepen-phase63-20260716T210004Z`). Pre-compact body was **12333** chars.

## Archived body (pre-compact)

## Phase 6.3 — Factory vs Demo Track Boundary Glue

Conceptual **glue slice** that locks how Phase **6.1** (factory Phase 0 presentation shell) and Phase **6.2** (horizon demo v1 gameplay loop) coexist without authority bleed. Neither track subsumes the other: factory law governs catalog attestation and player-build leakage; horizon demo law governs playable loop proof. This note names the **contracts at the seam** — mount sockets, event namespaces, attestation separation, and failure routing — so execution wiring and Half A operator sign-off have a single boundary reference.

> **Dual-track boundary (authoritative):** **6.1** owns **PresentationShellManifest**, **DevLeakageGuard**, and **KinestheticHonestyChecklist** factory gates. **6.2** owns **HorizonDemoManifest**, **DemoLoopOrchestrator**, and eight-beat loop ordering. **6.3** does **not** add gameplay beats or factory catalog rows — it documents **how** demo mounts into factory sockets and **which** attestations apply to which track.

## Scope

**In scope:** **DualTrackBoundaryManifest** (single reference artifact listing track authorities, mount contracts, and forbidden cross-imports); **TrackAuthorityRegistry** (factory vs horizon_demo track ids + owning subphase); **MountContractGlue** (PlayRegionHost socket ids, HUDLayerStack layer ids demo may use vs factory-only layers); **AttestationSeparationPolicy** (which gates block factory catalog sign-off vs demo playtest sign-off); **CrossTrackEventFirewall** (allowed `presentation.*` / `session.*` / `demo.*` bus crossings); **FailureRoutingPolicy** (factory mount failure vs demo stage failure — who surfaces toast, who blocks attestation); **BuildProfileSelector** (conceptual: factory-only vs demo-in-factory-shell vs debug — no Godot project file names).

**Out of scope:** Re-minting **6.1** launch→PlayRegion→HUD behavior or **6.2** eight-beat loop internals; full proc-gen, Azgaar/WebView, multiplayer; execution-track Godot scenes, C# types, HR rollup gates (execution-deferred / advisory on conceptual track); tertiary decomposition of individual glue policies (breadth-first complete at secondary level).

## Behavior

### Track authority matrix

| Track id | Authority subphase | Owns | Must not own |
|---|---|---|---|
| `factory_spine` | **6.1** | **PresentationShellManifest**, **LaunchFlowController**, **PlayRegionHost**, **HUDLayerStack** (persistent layers), **DevLeakageGuard**, **KinestheticHonestyChecklist** | Demo loop stages, **HorizonDemoManifest**, **demo_ruleset**, sim/rule stub wiring |
| `horizon_demo` | **6.2** | **HorizonDemoManifest**, **DemoLoopOrchestrator**, spawn→feedback beats, **demo_ruleset** stub, `demo.*` bus events | Factory catalog row attestation, weakening **DevLeakageGuard**, replacing **PlayRegionHost** ownership |
| `dual_track_glue` | **6.3** | Boundary contracts below — read-only policy reference for both tracks | Runtime behavior in either track |

### MountContractGlue (6.2 into 6.1)

Demo **mounts into** factory sockets — it does **not** fork a parallel viewport or HUD root.

| Factory export (6.1) | Socket id (6.1.2 authority) | Demo consumer (6.2) | Glue rule |
|---|---|---|---|
| **PlayRegionHost** FP socket | `fp_baseline_rig` | **FPExploreRigHost** | Demo attaches after `presentation.launch_complete` + `presentation.play_region_ready`; demo must not call **LaunchFlowController** |
| **PlayRegionHost** DM socket | `dm_worldcam_slot` | **DMCamTransitionSlot** | Demo uses **WorldCam** rail only; full **DMRigPolicyMatrix** deferred |
| **PlayRegionHost** MapCam stub (optional) | `mapcam_slot` | (deferred) | Optional stub — FP + DM WorldCam required at factory Phase 0; MapCam execution-deferred unless **KH-6.1-002** needs it |
| **HUDLayerStack** **Transient** | **PlayerFeedbackChannel** | Demo toasts only — no new persistent layers |
| **HUDLayerStack** **Base** / **Mode** | read-only | Demo reflects mode; does not reconfigure layer stack |
| **PresentationSessionHandle** | **SpawnBootstrapController** | Session id continuity required across tracks |

**Forbidden mounts:** Demo spawning a second **PlayRegionHost**; demo adding **Context** layer actions that bypass factory **DevLeakageGuard**; demo substituting **KinestheticHonestyChecklist** pass for loop completion.

### AttestationSeparationPolicy

| Attestation | Track | Blocks if failed | Does not block |
|---|---|---|---|
| **DevLeakageGuard** | factory (6.1) | Factory **ui_presentation_shell** catalog sign-off | Horizon demo loop completion (demo still fails player-build policy if leakage present) |
| **KinestheticHonestyChecklist** | factory (6.1) | Factory catalog row `attestation_gates` | Demo `demo.loop_complete` telemetry |
| **demo.loop_complete** (all 8 beats) | horizon (6.2) | Demo playtest sign-off (execution) | Factory catalog attestation |
| **DualTrackBoundaryManifest** review | glue (6.3) | Execution handoff when boundary doc stale vs 6.1/6.2 exports | Conceptual breadth completion (this slice) |

Factory attestation and demo playtest are **independent** success criteria. Passing demo loop does **not** waive factory leakage or kinesthetic gates; passing factory Phase 0 does **not** prove playable overwrite/rule loop.

### CrossTrackEventFirewall

Allowed crossings (demo may emit/consume):

| Bus | Factory → Demo | Demo → Factory |
|---|---|---|
| `presentation.*` | `launch_complete`, `play_region_ready`, `hud_active` (6.1.3 export; see [[Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]) | `demo.spawn_complete` (factory HUD may show Transient toast only) |
| `session.*` | **PresentationSessionHandle** | `demo.loop_complete`, `demo.stage_failed` |
| `demo.*` | — (factory does not subscribe) | all demo stage events |
| `input.*` | intent bus shared per 1.1 | demo intent tokens |
| `rule.*` | — | **RuleCheckProbe** effects to **presentation.*** feedback |

**Forbidden crossings:** Demo emitting `presentation.launch_complete` (factory authority); factory emitting `demo.loop_complete`; demo bypassing **DevLeakageGuard** via debug bus; either track writing to the other's manifest attestation fields.

### FailureRoutingPolicy

| Failure class | Primary owner | User-visible surface | Cross-track effect |
|---|---|---|---|
| Launch / PlayRegion mount fail | **6.1** **LaunchFlowController** | Launch screen error | Demo spawn blocked (`demo.spawn_blocked_no_play_region`) |
| **DevLeakageGuard** fail | **6.1** | Build rejected for factory attestation | Demo cannot weaken policy — same build profile must pass guard for player builds |
| Demo stage fail / ordering violation | **6.2** **DemoLoopOrchestrator** | **Transient** HUD toast | Factory mount and HUD **Base**/**Mode** unchanged |
| Overwrite veto | **6.2** + **3.3** | Feedback toast | No factory attestation impact |
| Boundary contract violation (e.g. duplicate PlayRegion) | **6.3** policy → **6.1** enforcement | Factory error path first | Demo session abort |

### BuildProfileSelector (conceptual)

| Profile | Factory gates active | Demo loop active | Typical use |
|---|---|---|---|
| `factory_phase0_only` | yes | no | Half A catalog attestation, presentation shell proof |
| `horizon_demo_in_shell` | yes (leakage + mount) | yes | Default integrated player build after Phase 6 breadth |
| `demo_debug` | leakage yes; kinesthetic may waive | yes + debug flags | Execution-only; not factory sign-off |

**Glue rule:** `horizon_demo_in_shell` is the **default** integrated profile — demo runs inside attested factory shell, not as a forked scene tree.

### DualTrackBoundaryManifest

| Field | Contract |
|---|---|
| `boundary_id` | `factory_demo_v1_glue` |
| `factory_authority` | Phase **6.1** exports in **MountContractGlue** table |
| `demo_authority` | Phase **6.2** **HorizonDemoManifest** + **DemoLoopOrchestrator** |
| `attestation_matrix` | **AttestationSeparationPolicy** table |
| `event_firewall` | **CrossTrackEventFirewall** allowed set |
| `failure_routing` | **FailureRoutingPolicy** table |
| `default_build_profile` | `horizon_demo_in_shell` |
| `version_anchor` | Minted with 6.1 (`2026-06-26-1912`) + 6.2 (`2026-06-26-1951`) basenames |

## Interfaces

**Imports from prior phases:**

| Phase export | How 6.3 consumes it |
|---|---|
| **PresentationShellManifest** + sockets (6.1) | Mount contract source of truth |
| **HorizonDemoManifest** + stage ids (6.2) | Demo authority + beat ordering reference |
| **SeamRegistry** presentation seam (1.3) | Glue registers boundary as presentation seam metadata |
| **DevLeakageGuard** (6.1) | Non-negotiable cross-track policy |

**Exports to downstream:**

| Export | Consumer |
|---|---|
| **DualTrackBoundaryManifest** | Execution track integrated build wiring; playtest scripts; Half A operator boundary review |
| **TrackAuthorityRegistry** | CI policy: which tests gate which attestation |
| **BuildProfileSelector** | Execution build flavors; operator docs |

**Explicit non-import:** Re-defining **6.1** or **6.2** internal stage machines — glue references, does not duplicate.

## Edge Cases

| Case | Handling |
|---|---|
| Demo completes loop but factory kinesthetic checklist failed | Demo playtest may pass; factory catalog remains `factory_staged` — attestations independent |
| Factory attestation passes with demo loop never run | Valid for `factory_phase0_only` profile; integrated profile requires both per operator checklist |
| Demo debug flag skips beat ordering | Execution debug only; does not satisfy **HorizonDemoManifest** `strict_ordering` for playtest sign-off |
| Operator runs demo without launch_complete | **SpawnBootstrapController** blocks; glue cites **MountContractGlue** — factory ordering invariant |
| Third track proposed (e.g. multiplayer shell) | Out of scope Phase 6 — new boundary manifest version required; do not extend 6.3 ad hoc |

## Open Questions

| ID | Question | Conceptual authority decision |
|---|---|---|
| OQ-6.3-001 | Single player build vs separate factory-attestation build artifact? | **Default integrated profile** (`horizon_demo_in_shell`); separate factory-only artifact allowed for CI — execution packaging |
| OQ-6.3-002 | Demo telemetry stored in factory session log? | **session.*** bus may carry `demo.loop_complete` summary; factory **PresentationShellManifest** does not own demo analytics schema |
| OQ-6.3-003 | Can demo waive **DMPauseGate** for teaching? | **No** — **6.2** respects **3.1** read-only pause; glue does not grant waiver |
| OQ-6.3-004 | Boundary manifest versioning on 6.1/6.2 tertiary edits? | **Reconcile on secondary export change** — execution track diff; conceptual slice complete at breadth mint |

## Pseudo-code readiness

Reader can sketch **TrackAuthorityRegistry** lookup, mount precondition checks before `demo.spawn_*`, and attestation matrix queries without guessing which track owns a failure. No pseudo-code blocks in this conceptual slice — execution track owns typed interfaces per Half A execution tech lead persona.

## Tasks

- [x] Mint 6.3 secondary with factory vs demo track boundary glue
- [x] Document **MountContractGlue** — demo mounts into **6.1** sockets only
- [x] Document **AttestationSeparationPolicy** — independent factory vs demo sign-off
- [x] Phase 6 conceptual breadth secondaries complete (6.1–6.3)

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

## Consistency Reports

> [!note]
> Post-mint: execution rollup gates, REGISTRY-CI, HR closure artifacts, integrated Godot build profiles, and dual attestation CI jobs are execution-deferred / advisory on conceptual track per conceptual_v1 contract. Boundary enforcement in player builds is out of scope for conceptual completion — resolved on execution track.

Minted 2026-06-26 (godo-followup-20260626T203100Z-phase6-deepen-6-3); persona: half_a.conceptual_architect; product_factory_run_id: f35ff65cfb4f; pre_create_gate: skipped_conceptual_track; dual_track: factory_demo_boundary_glue; execution_gaps_advisory: true.

