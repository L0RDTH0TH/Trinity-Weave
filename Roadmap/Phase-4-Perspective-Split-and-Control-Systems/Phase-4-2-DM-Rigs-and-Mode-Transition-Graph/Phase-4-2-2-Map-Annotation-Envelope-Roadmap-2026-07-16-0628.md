---
title: Phase 4.2.2 — Map Annotation Envelope
roadmap-level: tertiary
phase-number: 4
subphase-index: 4.2.2
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feed_gate_status: green
factory_feed_gate_reason: ''
body_compact_status: complete
body_chars_cap: 1200
body_recompact_1200_at: 2026-07-16
body_recompact_1200_queue: followup-deepen-gmm-4-2-2-20260716T230307Z
body_recompact_1200_status: complete
created: 2026-07-16
tags:
- roadmap
- genesis-mythos-master
- phase-4
- dm-rigs
- map-annotation
- mapcam
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
- '[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-4-2-2-Map-Annotation-Envelope-Roll-up-2026-07-16]]'
rollup-detail: '[[Phase-4-2-2-Map-Annotation-Envelope-Roll-up-2026-07-16]]'
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 4.2.2 — Map Annotation Envelope

**MapAnnotationEnvelope** for MapCam: Presentation-local pins/marks; never WorldState. No Godot / factory/L5.

## Scope

**In:** `map-annotation-local`; fields (anchor, layer_tag, visibility_band, session_ttl); MapCamPolicy bind; canon-gate reject sim-mutating marks; 3.2 since-you-left overlays.

**Out:** DM rail chrome (`4.2.3`); guards (`4.2.1`); Camera3D; serializers; factory/L5; exec pins; 4.3 persistence.

## Behavior

MapCam active → annotate → envelope validates Presentation-local → map surface. WorldState-implying intent fails canon gate (1.1). Session-local default. Detail → [[Phase-4-2-2-Map-Annotation-Envelope-Roll-up-2026-07-16]].

## Interfaces

**In:** MapCamPolicy + ModeTransitionGraph; TransitionGuardRegistry (4.2.1); 3.2 hints; canon gate (1.1). **Out:** envelope vocab + `map-annotation-local` → 4.2/4.3.

## Handoff

**80%** nouns + non-sim boundary. Cap ≤1200. Siblings 4.1.1=1062 / 4.1.2=1177 / 4.1.3=1154 / 4.2.1=1139. Next DFS **4.2.3** (`body_over_cap`).
