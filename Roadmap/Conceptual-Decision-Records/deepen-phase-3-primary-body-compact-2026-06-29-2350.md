---
title: Deepen Phase 3 primary body compact
decision_id: deepen-phase-3-primary-body-compact-2026-06-29-2350
project-id: genesis-mythos-master
roadmap_track: conceptual
created: 2026-06-29
status: active
validation_status: validated
queue_entry_id: architect-rr-gmm-remi-1e58b84f
product_factory_run_id: 1373c0c3408d
goal_authority: gmm-remint-l5-20260627T231800Z
persona_id: half_a.conceptual_architect
---

## Decision

Factory feed gate **RED** (`conceptual_note_oversized`) on Phase 3 primary required body compact: move roll-up tables, handoff readiness, open questions, pseudo-code readiness, subphase index, and dataview to rollup child; preserve wikilinks 3.1/3.2/3.3 on compact primary.

## Evidence

- **Before:** body ~7979 chars (harness `body_over_cap:7977>2000`)
- **After:** body ≤2000 chars; rollup [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roll-up-2026-06-29]]
- **Harness:** `factory_feed_gate` authority; `mint_batch: pmg_phases`
- **Scope excluded:** factory/l5, User-Story/scopes/*/L5.md

## Outcome

`factory_feed_gate_status: green` at primary slice; project harness may remain **RED** on tertiary oversize (3.1.1–3.1.3) until subsequent compacts.
