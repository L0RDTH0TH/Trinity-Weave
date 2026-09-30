---
title: Phase 3.1.1 — Roll-up & SimClock Policy Tables
roadmap-level: rollup
phase-number: 3
subphase-index: 3.1.1
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roadmap-2026-06-29-2205]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-3
- rollup
- sim-clock
- tick-scheduler
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Actors

| Actor | Role |
|-------|------|
| **SimClock** | Owns `t`, `n`, **StepMode**; exposes pause/resume; never blocks on Presentation |
| **SimClockPolicyRegistry** | Catalog of allowed step modes + session defaults |
| **TickScheduler** | Maps frame budget → tick count per session frame |
| **TickBudgetManifest** | Caps `max_ticks_per_frame`, `max_catchup_backlog`, deferral threshold |
| **CatchupDeferralPolicy** | When backlog exceeds ceiling → defer + `sim.catchup_deferred` |
| **SessionTimeSyncBinding** | Wall-clock session markers for absence windows (**3.2** consumes) |
| **DMPauseGate** | Halt tick advance; finish current atomic commit before pause holds |

## Step modes (conceptual v1)

| step_mode | Description | Default | Determinism |
|-----------|-------------|---------|-------------|
| `fixed` | Constant `Δt` per tick | **yes** | Full replay from seed + log |
| `variable_absence` | Larger `Δt` when sim backlog from long wall-clock absence | no | Replay records mode per tick in **CommittedTickRecord** |
| `paused` | No advance; speculative deltas may queue | — | N/A |

## Per-frame scheduling (algorithm sketch)

```
ticks_allowed = 0
if DMPauseGate.active: return 0
budget = TickBudgetManifest.from_presentation_signal()
backlog = SimClock.pending_tick_debt()
ticks_allowed = min(budget.max_ticks_per_frame, backlog)
if backlog > budget.max_catchup_backlog:
    emit sim.catchup_deferred
    ticks_allowed = min(ticks_allowed, budget.deferred_batch_cap)
return ticks_allowed
```

## Interface tables

### Imports

| Source | Consumption |
|--------|-------------|
| Parent 3.1 **DMPauseGate** | Pause-first; atomic commit before hold |
| Parent 3.1 **WorldStateCommitter** | Scheduler never partial-applies mid-tick |
| Phase 1 `sim.*` bus | `sim.tick_committed`, `sim.pause`, `sim.resume`, `sim.catchup_deferred` |
| Phase 1.3 **ProvenanceEnvelope** | Each committed tick records step mode + scheduler debt snapshot |
| Phase 2.1 **SimGraphSeed** | Initial `n=0`, `t=0` at session bootstrap |

### Exports

| Export | Consumer |
|--------|----------|
| **SimClockPolicyRegistry** | Sibling tertiaries + execution mirror |
| **TickBudgetManifest** defaults | **3.2** **AbsenceCatchupBridge** catch-up coordination |
| `sim.catchup_deferred` event schema | Presentation + DM notification path |

## Edge cases

- **Catch-up spiral:** Long absence → backlog exceeds ceiling; defer batch + notify DM; **3.2** may compile narrative from log without full catch-up replay.
- **Pause during commit:** **DMPauseGate** engaged mid-tick — finish **WorldStateCommitter** atomic apply, then hold clock; no partial state visible to Presentation.
- **Zero NPC/faction seed:** Valid — clock still advances; weather-only ticks commit (parent 3.1 edge case preserved).
- **Presentation frame drop:** Scheduler uses wall-clock debt, not frame count alone — avoids tying sim rate to render FPS.
- **Variable mode without log record:** Invalid — **CommittedTickRecord** must record `step_mode` for replay; block commit if missing (1.3 provenance).

## Open questions

- **Default `Δt` for first playable:** Coupled to Horizon M0 — operator attestation via factory catalog, not resolved on conceptual track.
- **Deferred batch priority vs live ticks:** When player returns mid-deferral — session policy toggle; DM table authority deferred to Phase 4+.
- **Maximum catch-up wall-clock span:** Factory catalog / Operator Loop 2 — not blocking conceptual feedstock.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope on parent tertiary |
| Behavior (actors, ordering) | pass | § Actors + scheduling sketch |
| Interfaces (adjacent contracts) | pass | § Interface tables |
| Edge cases | pass | § Edge cases |
| Open questions | pass | § Open questions |
| Pseudo-code readiness | pass | Scheduling sketch traceable |
| **`handoff_readiness` aggregate** | **79%** | first Phase 3 tertiary under factory feed gate |

> Execution-deferred / advisory on conceptual track: Godot scheduler wiring, typed budget structs, REGISTRY-CI — execution track or factory harness (`1373c0c3408d`).

## Research integration

Pattern alignment (no new pre-deepen research this run):

- Deterministic sim decoupled from render — Phase 1.1 Simulation/Presentation boundary
- Catch-up spiral guard — parent 3.1 § Edge cases
- Session replay provenance — Phase 1.3 **SeedSnapshot** + log hash contract

## Pseudo-code readiness

A reader can trace presentation budget → pause check → debt calculation → capped tick allowance → deferral event without guessing ownership between clock and pipeline. No API signatures on conceptual track.

## Responsibilities (rollup authority)

- [x] Document **StepMode** catalog and default `fixed`
- [x] Document **TickBudgetManifest** catch-up ceiling and deferral
- [x] Bind **SessionTimeSyncBinding** for **3.2** absence windows

## Tasks (rollup authority)

- [x] Mint 3.1.1 rollup with policy tables and scheduling sketch
- [ ] Refine variable_absence replay fields when execution mirror mints typed **CommittedTickRecord**
