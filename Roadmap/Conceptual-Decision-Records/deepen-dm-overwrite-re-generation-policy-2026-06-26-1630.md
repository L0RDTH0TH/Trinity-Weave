---
title: "CDR — DM Overwrite vs Deliberate Re-Generation Policy (3.3)"
created: 2026-06-26
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-3]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T142331Z-phase3-3
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: reconciled
related_research: []
---

## Summary

Chose a **three-class DM authority model** (`live_patch`, `canon_touching_patch`, `structural_re_gen`) with **OverwritePatchLayer** for in-session mutations and **ReGenerationIntentQueue** for structural change. **SpeculativeDeltaReconciler** bridges **3.1** pause/speculative queue; **NarrativeDeltaVetoPolicy** bridges **3.2** `dm_queue` retroactive veto — completing Phase 3 conceptual breadth secondaries without collapsing sim authority into narrative packaging.

## PMG alignment

Honors **DM authority respected** and **cost/intent doctrine**: cheap dynamic flair (tokens, weather, whispers) stays live; terrain/biome/seed surgery requires deliberate re-generation with narrative cost copy — consistent with master goal living-world + collaborative canon pillars.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| All DM edits as direct **WorldState** mutation | Simple mental model | Structural edits corrupt replay; no cost signal for regen | Patch layer + structural detector preserves **1.3** replay |
| All structural-looking edits auto-regen without live band | Clear boundary | Blocks cheap faction/weather nudges at table | **LiveOverwriteRegistry** allowlist for low-cost flair |
| Merge veto into **SinceYouLeftCompiler** (3.2) | Fewer actors | Blurs surfacing vs authority; DM veto is policy not packaging | **3.3** owns **NarrativeDeltaVetoPolicy**; **3.2** compiles only |

## Validation evidence

- **3.1** exports **DMPauseGate** + speculative queue explicitly for **3.3**
- **3.2** exports **dm_queue** entries to **3.3** canon conflict resolution
- Archived Phase 3.2 DM overwrite slice (2026-03) informed policy matrix without flattening new numbering (3.3 on greenfield tree)
- Validator (first pass): [[.technical/Validator/roadmap-auto-validation-20260626T163000Z-godo-followup-20260626T142331Z-phase3-3]] — `primary_code: safety_unknown_gap`; `reason_codes: [safety_unknown_gap, missing_roll_up_gates]`; `consume_eligible_l1: true`; rollup/traceability gaps reconciled post-IRA; execution gates advisory on `conceptual_v1`

## Links

- Workflow log: 2026-06-26 16:30 deepen Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy
- Parent phase: [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]
- Prior slices: [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]], [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]
