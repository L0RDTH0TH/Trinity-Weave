---
title: Phase 4.2 — Roll-up & DM Rigs / Transition Graph Detail
roadmap-level: rollup
phase-number: 4
subphase-index: '4.2'
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-secondary: '[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
created: 2026-07-15
tags:
- roadmap
- genesis-mythos-master
- phase-4
- rollup
- dm-rigs
- mode-transition
para-type: Project
queue_entry_id: followup-deepen-phase42-20260715T224500Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.2 — DM Rigs and Mode Transition Graph

Exhaust the **DM observation rig policy matrix** (WorldCam / MapCam / SensoriumAttach) and the **transition guard catalog** that refines **ModeTransitionGraph** from 4.1. This slice owns **which DM rig may activate under which session authority**, **read-only projection bindings**, and **edge predicates** that gate FP ↔ DM transitions — without Godot scene wiring (execution-deferred).

## Scope

**In scope:** **DMRigPolicyMatrix** (per-rig capability rows: projection sources, overlay classes, intent eligibility); **WorldCamPolicy**, **MapCamPolicy**, **SensoriumAttachPolicy** as named policy rows; **ModeTransitionGraph** edge catalog (source → target, guard stack, interpolator hint, veto hooks); **TransitionGuardRegistry** (composable predicates: DM authority, **DMPauseGate**, **NarrativeDeltaVetoPolicy**, live **OverwritePatchLayer** class from 3.3); **DMRailUXContract** (operator affordances for rig switch without sim mutation); **PresentationShell** activation handshake per 4.1.

**Out of scope:** **PlayerFPRig** and **PilotGraph** dominate/absent-proxy internals (4.1); cross-session agency persistence glue (4.3); Godot `Camera3D` / `SubViewport` implementation; execution-track typed rig interfaces and rollup HR gates (execution-deferred / advisory on conceptual track); tick commit and DM overwrite policy **definition** (Phase 3 — 4.2 consumes veto/pause seams only); spell-bound victim **passenger_fp** overlay (Phase 5).

## Behavior

**Actors:**

| Actor | Role |
|-------|------|
| **DMRigPolicyMatrix** | Authoritative table: rig_id → {projection_binding, overlay_set, intent_eligible, read_only} |
| **WorldCamPolicy** | Tactical overview: terrain + entity markers from **WorldState** projection; no faction write; intent_eligible = mode-switch only |
| **MapCamPolicy** | Strategic map: faction/terrain overlays from projected state; zoom bands; intent_eligible = mode-switch + map annotation envelopes (Presentation-local, non-sim) |
| **SensoriumAttachPolicy** | Read-only bind to target entity sensorium; **never** intent_eligible for locomotion/combat — observe + mode-switch only |
| **TransitionGuardRegistry** | Ordered predicate list evaluated before any edge fires |
| **ModeTransitionGraph** (refined) | Directed edges among `player_fp`, `dm_world`, `dm_map`, `dm_sensorium_attach` with per-edge guard stack + interpolator_id |
| **DMRailUXContract** | Hotkey / UI rail ordering: FP → WorldCam → MapCam → SensoriumAttach return paths; blocked-state messaging |
| **PresentationShell** | Delegates rig activation to matrix row; enforces single **active_rig_id** (4.1) |

**DMRigPolicyMatrix (conceptual rows):**

| rig_id | projection_binding | overlay_set | intent_eligible | read_only |
|--------|-------------------|-------------|-----------------|-----------|
| `player_fp` | local avatar + near field | combat HUD, interact prompts | locomotion, combat, interact, mode-switch | false (agency-bearing) |
| `dm_world` | tactical WorldState slice | entity markers, fog-of-war DM | mode-switch only | true |
| `dm_map` | strategic map projection | faction borders, since-you-left hints (3.2) | mode-switch, map-annotation-local | true |
| `dm_sensorium_attach` | target entity sensorium stream | NPC POV chrome, read-only HUD | mode-switch only | true |

**ModeTransitionGraph edge catalog (building on 4.1):**

| edge_id | source | target | guard_stack (ordered) | interpolator_hint |
|---------|--------|--------|----------------------|-------------------|
| `fp_to_world` | player_fp | dm_world | dm_session_authority, not_dmpause_frozen | ease_default |
| `world_to_fp` | dm_world | player_fp | dm_session_authority, narrative_veto_clear, overwrite_patch_compatible | ease_default |
| `world_to_map` | dm_world | dm_map | dm_session_authority, overwrite_patch_compatible | dm_orbit |
| `map_to_world` | dm_map | dm_world | dm_session_authority, overwrite_patch_compatible | dm_orbit |
| `world_to_sensorium` | dm_world | dm_sensorium_attach | dm_session_authority, attach_target_valid, not_dominate_active, overwrite_patch_compatible | snap_cut |
| `sensorium_to_world` | dm_sensorium_attach | dm_world | attach_target_valid, overwrite_patch_compatible | snap_cut |
| `fp_to_sensorium` | player_fp | dm_sensorium_attach | **rejected** — must route via world or dominate (4.1 PilotGraph) | — |
| `sensorium_to_fp` | dm_sensorium_attach | player_fp | narrative_veto_clear, not_dmpause_frozen, overwrite_patch_compatible | ease_default |

**TransitionGuardRegistry predicates:**

| guard_id | Predicate (NL) | Blocks when |
|----------|----------------|-------------|
| `dm_session_authority` | Operator holds active DM session token | No DM token |
| `not_dmpause_frozen` | **DMPauseGate** (3.1) not holding narrative freeze | Pause active and edge not whitelisted for snap-complete. **Inter-DM edges** (`world_to_map`, `map_to_world`, `world_to_sensorium`, `sensorium_to_world`) **omit** this guard by design: DM observation rails stay navigable during narrative freeze (matrix `intent_eligible` = mode-switch only); only **FP-return** edges (`world_to_fp`, `sensorium_to_fp`) and **FP→DM entry** (`fp_to_world`) require freeze clearance |
| `narrative_veto_clear` | **NarrativeDeltaVetoPolicy** (3.3) approves transition | Live patch would contradict surfaced narrative |
| `attach_target_valid` | Sensorium target exists in projection | Target despawned or out of range |
| `not_dominate_active` | **PilotGraph** not in dominate state (4.1) | Dominate active — SensoriumAttach would conflate observe with agency |
| `overwrite_patch_compatible` | Active **OverwritePatchLayer** class permits mode change (3.3) | Patch class blocks DM exits; **exception:** snap-to-FP when `narrative_veto_clear` passes on `world_to_fp` / `sensorium_to_fp` |

**Ordering (transition attempt):**

1. **PresentationShell** receives mode-switch intent (DM rail or envelope)
2. **TransitionGuardRegistry** evaluates guard_stack for candidate edge — first failure → **DMRailUXContract** surfaces blocked reason (no silent noop)
3. On pass: source rig deactivate per 4.1; **CameraInterpolatorRegistry** blend per edge hint
4. **DMRigPolicyMatrix** row activates target rig projections + overlay_set
5. **PerspectiveEnvelope** (4.1) updates legal intent routes per matrix `intent_eligible`
6. Emit `presentation.mode_changed` with `edge_id` + `guard_stack_passed` audit on `presentation.*` bus

**Inputs / outputs:**

- *Into 4.2:* **ModeTransitionGraph** skeleton + rig IDs (4.1); **DMPauseGate** + speculative queue (3.1); **NarrativeDeltaVetoPolicy** + **OverwritePatchLayer** classes (3.3); **SinceYouLeftCompiler** map hints (3.2) for MapCam overlays
- *Out of 4.2:* Exhaustive policy matrix + edge catalog for 4.3 agency glue; stable `edge_id` / `guard_id` vocabulary for factory catalog mint

## Interfaces

**Imports from Phase 4.1:**

| 4.1 export | How 4.2 consumes it |
|------------|----------------------|
| **ModeTransitionGraph** (skeleton) | 4.2 refines edges + guard stacks; does not rename rig IDs |
| **PerspectiveEnvelope** | Matrix `intent_eligible` column aligns with envelope legal modes |
| **CameraInterpolatorRegistry** | Edge `interpolator_hint` references registry IDs |
| **PilotGraph** | `not_dominate_active` guard; no direct SensoriumAttach ↔ FP shortcut |

**Imports from Phase 3:**

| Phase 3 export | How 4.2 consumes it |
|----------------|----------------------|
| **DMPauseGate** (3.1) | `not_dmpause_frozen` guard; snap-complete whitelist for in-flight blends |
| **NarrativeDeltaVetoPolicy** (3.3) | `narrative_veto_clear` on return-to-FP and post-patch edges |
| **OverwritePatchLayer** classes (3.3) | `overwrite_patch_compatible` guard |

**Exports to Phase 4 siblings:**

| Export | Consumer |
|--------|----------|
| **DMRigPolicyMatrix** + **TransitionGuardRegistry** | 4.3 cross-session agency + rail persistence |
| **DMRailUXContract** | Factory catalog L5 UX rows; execution mirror |

**Adjacent slices:**

- **4.1** owns rig nouns + envelope; **4.2** owns exhaustive policy matrix and transition guard catalog.
- **4.3** owns session-spanning agency glue; **4.2** supplies guard vocabulary only.

## Edge cases

- **Guard stack partial pass:** All guards must pass — no "best effort" edge fire; log `presentation.transition_blocked` with first failing `guard_id`.
- **SensoriumAttach target lost mid-attach:** Auto-edge to `dm_world` via `sensorium_to_world` with `attach_target_valid` failure recovery — not stranded black screen.
- **DMPauseGate during blend:** If pause engages mid-interpolator, complete visual blend (4.1) but block intent routes until `not_dmpause_frozen` — matrix `intent_eligible` already mode-switch-only for DM rigs.
- **Map annotation vs sim write:** MapCam `map-annotation-local` intents stay Presentation-local; canon gate (1.1) rejects any annotation that implies **WorldState** mutation.
- **Dominate active + DM rail WorldCam request:** Allowed — dominate does not block DM observation rigs; only blocks SensoriumAttach edge per `not_dominate_active`.
- **Overwrite patch class "hard freeze":** `overwrite_patch_compatible` blocks all DM rig exits except snap back to FP when veto clears.

## Open questions

- **Map annotation persistence:** Session-local only vs export to DM session log — lean session-local; 4.3 may persist rail state.
- **DM rail ordering operator override:** Default FP → World → Map → Sensorium — factory catalog attestation; not resolved on conceptual track.
- **Guard whitelist during pause:** In-flight blend snap-complete is a **runtime** PresentationShell behavior on active `edge_id` (4.1 mid-blend completion) — not a static catalog bypass of `not_dmpause_frozen`. **Inter-DM rail switches** intentionally omit `not_dmpause_frozen` (see registry row) so DM can reposition observation during freeze; FP-return edges retain the guard.
- **SensoriumAttach range model:** Projection-bound vs narrative-bound — lean projection-bound with 3.2 surfacing hints.

## Pseudo-code readiness

A reader can trace DM session open → **DMRailUXContract** selects WorldCam → guard stack `fp_to_world` passes → matrix row activates → MapCam switch via `world_to_map` → SensoriumAttach with `attach_target_valid` → blocked return to FP when **NarrativeDeltaVetoPolicy** fires — without guessing read-only vs intent routes or shortcut edges. No API signatures on conceptual track.

## Research integration

Pattern alignment (no new pre-deepen research this run):

- DM tool camera rails (world / map / possess observe) — aligned with 4.1 rig nouns; 4.2 adds policy matrix discipline
- Transition guard stacks — composable predicates pattern from 3.1 pause + 3.3 veto seams
- Read-only observation vs agency — SensoriumAttach matrix row enforces 4.1 distinction

## Responsibilities

- [x] Name DMRigPolicyMatrix with WorldCam / MapCam / SensoriumAttach policy rows
- [x] Document ModeTransitionGraph edge catalog with guard stacks
- [x] TransitionGuardRegistry composable predicates building on 4.1 + Phase 3 seams
- [x] DMRailUXContract operator affordances (conceptual)

## Tasks

- [x] Mint 4.2 secondary with DM rig policy matrix + transition graph
- [ ] Optional tertiaries: per-guard detail, map annotation envelope, rail UX states — deferred breadth-first
- [x] Handoff to 4.3 agency envelope + pilot machinery glue — [[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]

## Consistency

> [!note]
> Body compact 2026-07-15 (`followup-deepen-phase42-20260715T224500Z`): NL substance moved here for `factory_feed_gate` secondary `body_over_cap` 11858→≤1400. Execution Camera3D/SubViewport + typed serializers remain execution-deferred / advisory on conceptual track.

## Roll-up gates (execution-deferred / advisory)

The following remain **execution-deferred / advisory** on conceptual track — **not** authoritative blockers for Phase 4.2 conceptual completion:

| Gate family | Phase 4.2 posture | Resolved on |
|---|---|---|
| Godot Camera3D / SubViewport / typed rig serializers | deferred | execution track parallel spine |
| HR ≥93 rollup closure artifacts | advisory | execution track + operator attestation |
| REGISTRY-CI / canon registry CI receipts | advisory | execution track |
| `catalog_signed_at` / `execution_pins` | deferred | Operator Loop 2 post-freeze |
| Factory catalog row attestation | out of scope | Half A after conceptual freeze |

**Contract:** Conceptual 4.2 is complete for feedstock when secondary NL + this roll-up are present; execution gaps do **not** block DFS to Phase-4-3 body compact under `factory_feed_gate`.

Compacted under persona `half_a.conceptual_architect`; `product_factory_run_id: 1373c0c3408d`; goal_authority `gmm-remint-l5-20260627T231800Z`; next DFS: Phase-5 primary body compact (7801>2000); Phase-5-3 cleared 17030→1382; Phase-5-1 cleared 13723→1400.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task" OR roadmap-level = "rollup"
SORT subphase-index ASC, file.name ASC
```
