---
title: Phase 5.2 — Spell Agency and Perspective Metadata
roadmap-level: secondary
phase-number: 5
subphase-index: '5.2'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
breadth_mint_complete: true
secondary_feedstock_qualified: true
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-5
- spell-metadata
- agency
- perspective
para-type: Project
roadmap_track: conceptual
links:
- '[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[genesis-mythos-master-goal]]'
- '[[Phase-5-2-Spell-Agency-Perspective-Metadata-Roll-up-2026-07-15]]'
rollup-detail: '[[Phase-5-2-Spell-Agency-Perspective-Metadata-Roll-up-2026-07-15]]'
factory_feed_gate_status: green
body_compact_status: complete
body_compact_at: 2026-07-16
body_compact_queue: followup-deepen-phase52-20260716T195444Z
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 5.2 — Spell Agency and Perspective Metadata

**SpellAgencyPerspectiveManifest** + **SpellMetadataRegistry** + **DominateSpellBinding** + **VictimPassengerOverlayBinding** + **LiminalPresentationPolicy** + **AbsentProxyHintSpellBinding**. Routes via **RuleEffectBus** → **AgencyEnvelope** (4.3) / **PerspectiveEnvelope** (4.1). Victim overlay only. Conceptual — Godot DSL exec-deferred.

## Scope

**In:** SpellAgencyPerspectiveManifest; SpellMetadataRegistry; DominateSpellBinding; VictimPassengerOverlayBinding; LiminalPresentationPolicy; AbsentProxyHintSpellBinding; RuleContextFrame.spell_metadata; SpellRulesetPlugin. **Out:** Quest pressure (5.3); serializers/HR; factory/L5.

## Behavior

Spell → registry → `modify_agency` dominate/release or absent_proxy_hint → PilotHandoff / AbsentProxyPolicy → overlay + liminal. Priority 100–199. Detail → [[Phase-5-2-Spell-Agency-Perspective-Metadata-Roll-up-2026-07-15]].

## Interfaces

Imports: 5.1 RuleEngineCore/EffectBus/Arbiter; 4.3 AgencyEnvelope/PilotHandoff; 4.1 PerspectiveEnvelope; 4.2 ModeTransitionGraph. Exports: SpellMetadataRegistry + liminal → 5.3.

## Roll-up

Schemas, bindings, liminal policies, edge cases, OQs, tasks → [[Phase-5-2-Spell-Agency-Perspective-Metadata-Roll-up-2026-07-15]].

## Handoff

**80** — NL complete; secondary feedstock qualified; next DFS **5.3**. Exec-deferred: widgets, serializers — advisory.
