---
title: Phase 4.2.2 — Map Annotation Envelope (Roll-up)
roadmap-level: rollup
phase-number: 4
subphase-index: 4.2.2
project-id: genesis-mythos-master
status: complete
created: 2026-07-16
tags:
- roadmap
- rollup
- genesis-mythos-master
- phase-4
- map-annotation
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-2-2-Map-Annotation-Envelope-Roadmap-2026-07-16-0628]]'
- '[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

# Phase 4.2.2 roll-up — Map Annotation Envelope

Canonical compact tertiary: [[Phase-4-2-2-Map-Annotation-Envelope-Roadmap-2026-07-16-0628]]. Detail preserved off the ≤1400 feedstock body (`followup-deepen-phase422-tertiary-20260716T102802Z`); body recompact ≤1200 (`followup-deepen-gmm-4-2-2-20260716T230307Z`, 1393→≤1200).

## Purpose

Isolate the **MapCam annotation contract**: pins and marks that live in Presentation, bind to MapCamPolicy, and must never mutate WorldState. Complements 4.2.1 guards (when edges fire) with what MapCam may accept as local operator ink.

## Scope (expanded)

**In:**

| Noun | Role |
|------|------|
| **MapAnnotationEnvelope** | Carrier for Presentation-local map marks |
| `anchor` | Map-space reference (region / faction / coord band — conceptual) |
| `layer_tag` | Overlay class (faction border hint, since-you-left, operator pin) |
| `visibility_band` | Which MapCam zoom / policy bands show the mark |
| `session_ttl` | Session-local lifetime default |
| `map-annotation-local` | Intent class eligible only under MapCamPolicy |

**Out:** DM rail chrome / operator sequencing (`4.2.3`); guard stack (`4.2.1`); Camera3D / SubViewport; typed serializers; factory/L5; execution pins; 4.3 persistence of rail logs.

## Behavior detail

1. MapCam active (post-guard edge from 4.2.1 / ModeTransitionGraph).
2. Operator issues annotation intent with `map-annotation-local`.
3. Envelope validates: Presentation-local only; no WorldState field writes.
4. Canon gate (1.1) rejects any annotation that implies sim mutation.
5. Projection surfaces mark; 3.2 since-you-left hints may co-layer as read-only overlays.

## Edge cases

- **Annotation while not on MapCam:** Reject — envelope only under MapCamPolicy active row.
- **Annotation implying faction ownership change:** Canon gate fail; not a Presentation pin.
- **Session end:** Default drop session-local marks; 4.3 may later export to DM session log (open Q).
- **Freeze / DMPauseGate:** Annotations remain Presentation-local ink; they do not bypass `not_dmpause_frozen` for FP-return edges.

## Open questions

- **Persistence:** Session-local only vs export to DM session log — lean session-local; 4.3 owns rail persistence.
- **Shared vs private pins:** Multi-operator shared map ink deferred to factory/L5 attestation.

## Handoff criteria

- [x] Envelope nouns named
- [x] Non-sim / Presentation-local boundary explicit
- [x] Binding to MapCamPolicy + canon gate stated
- [x] Next tertiary pointed (`4.2.3` DM rail chrome)

**80%** handoff_readiness — implementer can place map ink without guessing WorldState authority. Slice `factory_feed_gate_status: green` after recompact ≤1200. Project harness **red** sole live cause: Phase-4-2-3 `body_over_cap` (4.2.2 cleared).
