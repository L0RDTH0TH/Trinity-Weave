---
title: Conceptual decision record — Release-plan Loop 2 migration
created: 2026-09-28
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, product-factory, release-plan]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[genesis-mythos-master-goal]]"
decision_kind: other
queue_entry_id: null
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: pattern_only
related_cdr: "[[Conceptual-Decision-Records/api-core-protection-boundary-2026-09-28]]"
---

# Conceptual decision record — Release-plan Loop 2 migration

## Summary

Replace Operator Loop 2’s **depth/budget splicer** (`target_depth` per catalog row + depth slicer → L4…L1 validate) with a **traditional release plan**: waves `alpha` → `beta` → `rc` → `ga`, packages of catalog rows with **fidelity** and **exit_criteria**, feeding Half B. L5 folds into Loop 2 for rows included in packages. CDP lane sequencing is renamed **`lane_batch`** (not “wave”).

This CDR is **independent** of [[Conceptual-Decision-Records/api-core-protection-boundary-2026-09-28]]. Release-plan / factory doctrine must **not** re-introduce “modules slot directly” / unprotected core reach — modules still extend only through versioned API ports.

Glossary: [[3-Resources/Second-Brain/Docs/Factory-Vocabulary]].

## PMG alignment

Serves System + Reference Exemplar delivery by making **what ships together** and **when a wave is done** operator-legible, instead of welding arbitrary depth rungs overnight.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ----------- | ------ | -------- | -------------- |
| Keep per-row `target_depth` budget | Existing harness | Operators plan releases with the wrong primitive | Rejected |
| Depth slicer remains Loop 2 gate | Auto L4–L1 files | Confuses L5 vision with release planning | Rejected as Loop 2 exit; transitional CLI only |
| Call CDP lane batches “waves” | Match old code | Collides with alpha/beta release waves | Rejected — rename to `lane_batch` |

**Chosen path:** `release-plan.yaml` + fidelity + wave-exit rule; harness cutover behind `release_plan_feed` after tests green.

## Binding rules (normative)

### Wave

A **wave** is a release channel: `alpha` → `beta` → `rc` → `ga` (ordered). Not a lane batch.

### Fidelity (one-liners)

| Value | Definition |
| ----- | ---------- |
| **`stub`** | Structure and contracts present; happy path may be incomplete or mocked; not demoable as a real player/DM session beat. |
| **`playable`** | An operator (or playtest) can complete the package’s named session beat(s) end-to-end without builder workarounds; failure modes are honest, not silent. |
| **`polish`** | Playable bar met **plus** UX/edge cases and presentation bar in the package `exit_criteria` (no “known broken but shippable” escapes). |

### Active-wave exit

**`active_wave_complete` / `factory_wave_satisfied` is true iff every package in the active wave:**

1. Has status complete / weld receipt recorded, **and**
2. Meets **all** of its own `exit_criteria[]`, **and**
3. Meets its declared **`fidelity`** target (definitions above).

Partial waves do **not** count. Completing some packages or some `lane_batches` inside a package does **not** satisfy the wave.

### L5 and pins

Loop 2 affirms **L5** (and resolved conceptual pins) for rows in packages being signed into the plan. Execution pins wire for the **next package** before Half B stage. Depth L4–L1 slicer is **not** a Loop 2 exit check.

### Depth-slicer retirement

`depth_slicer` CLI may remain **transitional** (optional, not Loop 2). **Remove** it after the **first successful alpha wave** under release-plan feed (`active_wave_complete` for `alpha` with real weld receipts).

### Compat flag

`release_plan_feed` defaults **false** until `test_release_plan.py` and Phase 2 Loop 2/3 tests are green; then default **true** and hard-off the budget/depth Loop 2 path. No dual-brain overnight once flipped.

## Consequences

- Artifact: `Roadmap/User-Story/release-plan.yaml` (replaces `slice-depth-budget.json` as planner).
- Half B overnight `done_when`: `active_wave_complete` (legacy budget tokens only in pre-flip window).
- Operator docs: [[Release-Plan-and-Catalog]], [[Roadmap-Factory-Pipeline]], [[Five-Factories-Trail]], [[Headless-Overnight-Session]].
- GMM seed: one alpha package mapping existing catalog rows; do not invent pins/L5.

## Validation evidence

- Operator + Grok plan refinements 2026-09-28 (fidelity defs; wave-exit rule; depth-slicer retirement; Phase 2 before Phase 3; test-before-flip; minimal seed; separate from API-core CDR)

## Links

- Master goal: [[genesis-mythos-master-goal]]
- Vocabulary: [[3-Resources/Second-Brain/Docs/Factory-Vocabulary]]
- Sibling (do not merge): [[Conceptual-Decision-Records/api-core-protection-boundary-2026-09-28]]
- Prior dual-goal: [[Conceptual-Decision-Records/reference-exemplar-dual-goal-2026-08-01]]
