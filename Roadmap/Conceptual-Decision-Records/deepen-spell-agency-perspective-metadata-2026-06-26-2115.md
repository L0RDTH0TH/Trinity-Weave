---
title: CDR — Phase 5.2 Spell Agency and Perspective Metadata
cdr-type: deepen
phase-number: 5
subphase-index: "5.2"
project-id: genesis-mythos-master
queue_entry_id: godo-followup-20260626T211500Z-phase5-deepen-5-2
roadmap_track: conceptual
created: 2026-06-26
tags: [cdr, genesis-mythos-master, phase-5, spell-metadata]
validation_status: reconciled
master_goal: "[[genesis-mythos-master-goal]]"
parent_roadmap_note: "[[Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]"
---

## Summary

Minted Phase 5.2 secondary: **Spell Agency and Perspective Metadata** — spell-bound manifests route dominate/victim presentation through **RuleEffectBus** into **AgencyEnvelope** without new **PerspectiveEnvelope** legal modes.

## PMG alignment

Honors PMG dominate/victim branch: dominator receives **pilot_fp** via **PilotGraph**; victim uses reserved `passenger_fp_overlay` with **LiminalPresentationPolicy** (locked input, liminal UI) — presentation overlay outside legal perspective modes.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Victim as new `perspective_mode` (`passenger_fp` in envelope) | Simpler mode graph | Violates 4.1 contract; blurs agency vs observation | Rejected — 4.1 explicitly defers victim overlay to Phase 5 hook |
| Inline spell metadata only in rule bodies | Fewer registry artifacts | DM workbench cannot browse spells without loading rules | Central **SpellMetadataRegistry** preferred (OQ-5.2-001 lean) |
| Synchronous effect bus dispatch | Easier ordering reasoning | Breaks 5.1 async-by-default sim pause semantics | Retains async **RuleEffectBus** queues from 5.1 |

## Validation evidence

- Pattern: [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]] exports `agency_transition` channel for 5.2
- Pattern: [[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]] reserves `passenger_fp_overlay` hook
- Pattern: [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]] excludes victim overlay from legal modes
- **Rejected-alternative rationale (PMG victim policy):** Victim-as-`perspective_mode` alternative would violate PMG dominate/victim branch — victim must receive locked-input liminal presentation via overlay hook, not a legal **PerspectiveEnvelope** mode switch. Chosen path honors PMG [[genesis-mythos-master-goal]] victim branch (overlay + **LiminalPresentationPolicy** semantics) while dominator retains **pilot_fp** via **PilotGraph** dominate state.
- IRA post-validator (2026-06-26): dominate_release disambiguated to `modify_agency` `{agency_class: release_dominate}` vs 4.3 handoff state; absent_proxy_hint path documented; 4.3 `spell_id` extension + 5.1 spell trigger enum declared — [[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-godo-followup-20260626T211500Z-phase5-deepen-5-2.md]]

## Links

- workflow_state Log: 2026-06-26 21:15 | Phase-5-2-Spell-Agency-Perspective-Metadata
- queue_entry_id: godo-followup-20260626T211500Z-phase5-deepen-5-2
