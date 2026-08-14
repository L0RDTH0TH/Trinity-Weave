---
title: Phase 4.2.1 — TransitionGuardRegistry and DM Session Authority (Roll-up)
roadmap-level: roll-up
phase-number: 4
subphase-index: 4.2.1
project-id: genesis-mythos-master
status: active
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-4
- roll-up
- dm-rigs
- transition-guards
- dm-session-authority
para-type: Project
roadmap_track: conceptual
parent: '[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
body_compact_source_queue: followup-deepen-phase42-feedstock-20260716T085600Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 4.2.1 Roll-up — archive of pre-compact feedstock

Canonical compact tertiary: [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]. This roll-up preserves detail moved off the ≤1400 feedstock body on 2026-07-16 (`followup-deepen-phase42-feedstock-20260716T085600Z`) and the ≤1200 recompact on 2026-07-16 (`followup-deepen-gmm-4-2-1-20260716T222811Z`).

## Archived body (pre-compact)

## Phase 4.2.1 — TransitionGuardRegistry and DM Session Authority

This tertiary isolates the **guard stack contract** that governs when a DM rail transition may fire. It makes **DM session authority**, **freeze/veto compatibility**, and **SensoriumAttach safety** explicit without drifting into Godot runtime wiring or factory/L5 scope.

## Scope

**In:** `dm_session_authority`; `not_dmpause_frozen`; `narrative_veto_clear`; `overwrite_patch_compatible`; `attach_target_valid`; `not_dominate_active`; first-failing-guard semantics; blocked-reason UX receipt on `presentation.transition_blocked`; FP-entry / FP-return / inter-DM rail distinctions.

**Out:** Map annotation persistence details (future `4.2.2`); DM rail chrome / operator sequencing states (future `4.2.3`); `Camera3D` / `SubViewport`; typed serializers; factory/L5; execution pins.

## Behavior

Mode-switch intent enters **TransitionGuardRegistry** with the candidate `edge_id`. The registry evaluates the ordered guard stack and returns either:

1. **allow** with the passed guard list for `presentation.mode_changed`, or
2. **block** with the first failing `guard_id` for `presentation.transition_blocked`.

The conceptual split is:

- **FP -> DM entry** requires DM authority and freeze clearance.
- **Inter-DM observation** may keep moving during narrative freeze because those rigs remain read-only.
- **DM -> FP return** still requires veto / overwrite compatibility so the player is not dropped back into an invalid authored state.

## Interfaces

**Imports:** `ModeTransitionGraph` and rig nouns from **4.1**; `DMPauseGate` from **3.1**; `NarrativeDeltaVetoPolicy` and `OverwritePatchLayer` classes from **3.3**.

**Exports:** stable `guard_id` vocabulary for the parent **4.2** matrix and for **4.3** agency glue; canonical blocked-reason contract for `DMRailUXContract`.

## Edge cases

- **Missing DM token:** all DM-entry and DM-switch edges block at `dm_session_authority`; UX must explain the missing authority rather than silently noop.
- **Narrative freeze mid-rail:** FP entry / return edges hold on `not_dmpause_frozen`, but inter-DM observation remains legal because it does not mutate agency.
- **Overwrite hard-freeze:** `overwrite_patch_compatible` blocks DM exits unless `narrative_veto_clear` explicitly re-opens the return to FP.
- **Dominate active:** `not_dominate_active` blocks SensoriumAttach so observation never masquerades as agency possession.

## Open questions

- Should `dm_session_authority` be renewed on every edge or cached for a short PresentationShell lease window?
- Do inter-DM edges need a separate guard for stale projection snapshots, or is that an execution-track concern only?
- Should `presentation.transition_blocked` expose only the first failing guard or a full failed-guard list for operator diagnostics?

## Handoff

**80%** — the guard catalog is explicit enough for a junior implementer to wire the policy order without guessing the conceptual authority split. Execution-deferred: Godot signal signatures, typed guard payloads, and runtime projection freshness checks. Project harness **RED** after this recompact advances to Phase-4-2-2 tertiary `body_over_cap` (live DFS). Execution-deferred gates remain advisory on conceptual track.

## Recompact ≤1200 archive (2026-07-16)

Queue `followup-deepen-gmm-4-2-1-20260716T222811Z`. Pre-recompact body **1381→≤1200** moved residual prose here; live tertiary keeps nouns + rollup pointer.

### Pre-recompact body (1381)

## Phase 4.2.1 — TransitionGuardRegistry and DM Session Authority

Guard-stack for DM rail transitions: **DM session authority**, freeze/veto, **SensoriumAttach** safety. Conceptual — no Godot, no factory/L5.

## Scope

**In:** `dm_session_authority`; `not_dmpause_frozen`; `narrative_veto_clear`; `overwrite_patch_compatible`; `attach_target_valid`; `not_dominate_active`; first-failing-guard; `presentation.transition_blocked`; FP-entry/return/inter-DM.

**Out:** Map annotation (`4.2.2`); DM rail chrome (`4.2.3`); Camera3D; serializers; factory/L5; exec pins.

## Behavior

Intent → **TransitionGuardRegistry** → allow (`presentation.mode_changed`) or block (first `guard_id` → `presentation.transition_blocked`). FP→DM: authority+freeze; inter-DM OK under freeze (read-only); DM→FP: veto/overwrite clear. Detail → [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roll-up-2026-07-16]].

## Interfaces

**Imports:** ModeTransitionGraph (4.1); DMPauseGate (3.1); NarrativeDeltaVetoPolicy + OverwritePatchLayer (3.3). **Exports:** `guard_id` for 4.2/4.3; blocked-reason for DMRailUXContract.

## Roll-up

Edge cases + OQs → [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roll-up-2026-07-16]].

## Handoff

**80%** — guard catalog explicit. Exec-deferred — advisory. Harness **red**: `phase_4_tertiary_tree` incomplete; next **4.2.2** map annotation.

