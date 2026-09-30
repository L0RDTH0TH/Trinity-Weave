---
title: Phase 4.1 — Roll-up & Perspective Envelope Detail
roadmap-level: rollup
phase-number: 4
subphase-index: '4.1'
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-secondary: '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-4
- rollup
- perspective
- player-fp
para-type: Project
queue_entry_id: followup-deepen-phase41-20260715T222400Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Actors

| Actor | Role |
|-------|------|
| **PerspectiveEnvelope** | Declares legal perspective modes (`player_fp`, `dm_world`, `dm_map`, `dm_sensorium_attach`) and which modes may emit **InputIntent** vs read-only observe; dominated-victim **passenger_fp** / spell-bound presentation is **not** an envelope mode — overlay deferred Phase 5 (PMG [[genesis-mythos-master-goal]]) |
| **UnifiedSceneGraph** | Single scene composition root; all rigs attach as **PerspectiveAnchor** nodes; no duplicate world mutation paths |
| **CameraInterpolatorRegistry** | Named interpolators (`ease_default`, `snap_cut`, `dm_orbit`) swappable per transition edge without rewiring graph |
| **PlayerFPRig** | Default FP anchor; binds local player avatar presentation; routes self-agency intents upward |
| **WorldCam** | DM tactical overview rig; read-only WorldState projection; no **InputIntent** except mode-switch envelopes |
| **MapCam** | Strategic map rig; read-only faction/terrain overlays from projected state |
| **SensoriumAttach** | Read-only bind to NPC/entity sensorium — **not** agency delegation (distinct from **PilotGraph** dominate) |
| **PilotGraph** | Agency delegation state machine: **self** → **dominate** (possess target envelope) → **absent-proxy** (NPC acts per policy while player away) |
| **ModeTransitionGraph** | Directed edges among rigs with guard predicates (DM session authority, **DMPauseGate** from 3.1, narrative veto from 3.3) |
| **PresentationShell** | Session-scoped composer child (1.1); owns rig activation and interpolator selection |

## Ordering (mode transition)

1. **ModeTransitionGraph** evaluates guard (DM authority, pause state, overwrite class from 3.3 if live patch active)
2. Source rig **deactivate** (flush pending interpolator)
3. **CameraInterpolatorRegistry** blend from source **PerspectiveAnchor** to target over `transition_ms` or snap
4. Target rig **activate**; **PerspectiveEnvelope** updates legal intent routes
5. **PilotGraph** reconciles agency: dominate transfers **InputIntent** router target; absent-proxy installs proxy policy without sim write from Presentation
6. Emit `presentation.mode_changed` on `presentation.*` bus (Phase 1.1)

## Inputs / outputs

- *Into 4.1:* **WorldState** projections (1.1); `sim.tick_committed` read-only (3.1); **DMPauseGate** + speculative queue awareness (3.1/3.3); **NarrativeDeltaVetoPolicy** may block transitions that contradict live narrative (3.3)
- *Out of 4.1:* **PerspectiveEnvelope** contract for 4.2 DM rigs deep-dive; **PilotGraph** export for 4.3 agency glue; stable rig IDs for factory catalog mint

## Interfaces

**Imports from Phase 1:**

| Phase 1 export | How 4.1 consumes it |
|----------------|----------------------|
| Presentation / InputIntent layers (1.1) | PresentationShell owns rigs; InputIntent router respects **PerspectiveEnvelope** |
| `presentation.*` bus category (1.1) | `presentation.mode_changed`, `presentation.rig_active` |
| Agency delegation envelopes (1.1) | **PilotGraph** specializes dominate + absent-proxy |

**Imports from Phase 3:**

| Phase 3 export | How 4.1 consumes it |
|----------------|----------------------|
| **DMPauseGate** (3.1) | Mode transitions may be frozen while DM holds narrative authority |
| **WorldEventLog** subscribe (3.1) | Presentation refreshes projections on `sim.tick_committed` — never blocks sim |
| **NarrativeDeltaVetoPolicy** (3.3) | Blocks mode edges that would surface contradictory live patches |

**Exports to Phase 4 siblings:**

| Export | Consumer |
|--------|----------|
| **ModeTransitionGraph** + rig IDs | 4.2 DM rigs and transition policy refinement |
| **PilotGraph** dominate/absent-proxy states | 4.3 agency envelope + pilot machinery glue |
| **CameraInterpolatorRegistry** | Execution track mirror under `Roadmap/Execution/` parallel spine |

**Adjacent slices:**

- **4.2** owns exhaustive DM transition policy and rail UX; 4.1 owns rig nouns + envelope guards.
- **4.3** owns cross-session agency persistence; 4.1 defines **PilotGraph** states only.

## Edge cases

- **Transition during DMPauseGate:** Finish current interpolator blend or snap per policy — never half-active dual rigs writing intents; sim pause does not freeze Presentation blend completion if already committed visually.
- **Dominate vs SensoriumAttach confusion:** SensoriumAttach is **read-only** perception; dominate transfers **InputIntent** — **PerspectiveEnvelope** rejects dominate while SensoriumAttach active without explicit edge through **ModeTransitionGraph**.
- **Absent-proxy during off-screen sim (3.2):** Proxy policy reads **SinceYouLeftCompiler** surfacing hints but does not mutate **WorldState** — intents route to Simulation via 1.1 canon gate only.
- **Interpolator missing:** Fallback `snap_cut`; log `presentation.interpolator_fallback` — not silent ease default.
- **UnifiedSceneGraph anchor drift:** Two rigs claim same anchor — **PresentationShell** enforces single **active_rig_id**; secondary rig stays dormant.

## Open questions

- **Dominated-victim / passenger-FP presentation:** PMG requires spell-bound victim policy (e.g. `passenger_fp` with locked input, liminal UI) paired with dominator **pilot** — **deferred to Phase 5** spell metadata; 4.1 **PilotGraph** documents dominator possess branch only; victim presentation is out-of-envelope overlay, not a fifth legal mode in this slice.
- **Default transition_ms** per edge — operator attestation via factory catalog; not resolved on conceptual track.
- **Absent-proxy policy source:** ~~Static table vs **ToneProfileNarrativeWeights** (3.2)~~ **Superseded by D-4.3-002** — static **AbsentProxyPolicyTable** + DM session token override for `proxy_quest_steward` only; see [[decisions-log#Phase 4.3 open question anchors|decisions-log D-4.3-002]].
- **SubViewport vs single-camera stack:** Execution track chooses; conceptual track requires **UnifiedSceneGraph** single-authority invariant only.

## Pseudo-code readiness

A reader can trace session entry on **PlayerFPRig** → DM invokes WorldCam/MapCam/SensoriumAttach via **ModeTransitionGraph** → interpolator blend → **PilotGraph** dominate handoff → absent-proxy while away → Presentation subscribes to projections without sim mutation — without guessing rig ownership or read-only vs agency modes. No API signatures on conceptual track.

## Research integration

Pattern alignment (no new pre-deepen research this run):

- Single scene graph + camera rig swapping — common action-RPG / DM tool pattern; aligned with Phase 1.1 Presentation mode graph
- Agency delegation graphs — dominate/possess vs observe-only binds per 1.1 InputIntent table
- Read-only DM observation rigs — SensoriumAttach distinct from pilot per 1.1 edge-case callout

## Responsibilities

- [x] Name PlayerFPRig, WorldCam, MapCam, SensoriumAttach, UnifiedSceneGraph, CameraInterpolatorRegistry
- [x] Document PerspectiveEnvelope and ModeTransitionGraph guards
- [x] PilotGraph states for dominate + absent-proxy
- [x] Integration spine with Phase 1 Presentation/InputIntent and Phase 3 pause/veto seams

## Tasks

- [x] Mint 4.1 secondary with perspective envelope actor registry
- [ ] Optional tertiaries: interpolator curves, PilotGraph detail, per-rig FOV contracts — deferred breadth-first
- [x] Handoff to 4.2 DM rigs transition policy — [[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]

## Consistency

> [!note]
> Body compact 2026-07-15 (`followup-deepen-phase41-20260715T222400Z`): NL substance moved here for `factory_feed_gate` secondary `body_over_cap` 9659→≤1400. Execution Camera3D/SubViewport + typed serializers remain execution-deferred / advisory on conceptual track.

## Handoff readiness (feedstock qualify 2026-07-16)

**Score: 80** (factory feed gate floor ≥75; target feedstock 80). Reconciled from non-numeric `breadth_complete` after post-cleanup honest cursor (`cleanup-20260716`). Queue: `followup-deepen-phase627-tertiary-20260716T064200Z`.

### Criteria assessment

| Criterion | Weight | Status | Evidence |
|-----------|--------|--------|----------|
| Scope nouns + in/out boundaries | 20% | Pass | Secondary § Scope — PerspectiveEnvelope, UnifiedSceneGraph, PilotGraph; explicit outs (4.2 matrix, Camera3D) |
| Behavior narrative (mode → presentation) | 20% | Pass | Secondary § Behavior — ModeTransitionGraph → interpolator → PilotGraph → `presentation.mode_changed` |
| Interface imports/exports | 15% | Pass | Secondary § Interfaces — 1.1 InputIntent, 3.1 tick, 3.3 veto; exports to 4.2/4.3 |
| Roll-up NL completeness | 15% | Pass | This roll-up — actors, ordering, edge cases |
| Body compact + breadth mint | 15% | Pass | Secondary body ≤1400 post–feedstock compact; `breadth_mint_complete: true`; criteria tables live here |
| Cross-phase linkage | 10% | Pass | wikilinks 1.1, 3.1, 3.3; parent Phase 4 primary |
| Execution-deferred honesty | 5% | Pass | Typed rigs, Camera3D, SubViewport — advisory; no pseudo-code on conceptual track |

### Gaps (non-blocking on conceptual track)

| Gap | Severity | Owner track |
|-----|----------|-------------|
| Typed rig manifests (Camera3D paths) | Advisory | execution |
| Tertiary depth under 4.1 | Deferred | execution / factory |
| L5 catalog pins | Out of scope | factory (excluded this run) |

### Handoff contract

Feedstock **qualified** for `pmg_phases` mint batch at secondary **4.1**. Siblings **4.2** and **4.3** remain on `breadth_complete` until their feedstock reconcile runs. Exec-deferred items do not block conceptual completion.

## Roll-up gates (execution-deferred / advisory)

The following remain **execution-deferred / advisory** on conceptual track — **not** authoritative blockers for Phase 4.1 conceptual completion:

| Gate family | Phase 4.1 posture | Resolved on |
|---|---|---|
| Godot Camera3D / SubViewport / typed rig serializers | deferred | execution track parallel spine |
| HR ≥93 rollup closure artifacts | advisory | execution track + operator attestation |
| REGISTRY-CI / canon registry CI receipts | advisory | execution track |
| `catalog_signed_at` / `execution_pins` | deferred | Operator Loop 2 post-freeze |
| Factory catalog row attestation | out of scope | Half A after conceptual freeze |

**Contract:** Conceptual 4.1 is complete for feedstock when secondary NL + this roll-up are present; execution gaps do **not** block DFS to Phase-4-3 body compact under `factory_feed_gate`.

Compacted under persona `half_a.conceptual_architect`; `product_factory_run_id: 1373c0c3408d`; goal_authority `gmm-remint-l5-20260627T231800Z`; next DFS: Phase-5 primary body compact (7801>2000); Phase-5-3 cleared 17030→1382; Phase-5-1 cleared 13723→1400; Phase-4-2 cleared 11858→1375.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task" OR roadmap-level = "rollup"
SORT subphase-index ASC, file.name ASC
```
