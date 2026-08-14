---
title: Conceptual decision record — Phase 4.1.3 body recompact ≤1200
created: 2026-07-16
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-4, body-compact]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]"
decision_kind: deepen
queue_entry_id: followup-deepen-gmm-4-1-3-20260716T220407Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
roadmap_track: conceptual
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
validator_report: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-gmm-4-1-3-20260716T220407Z-20260716T221758Z.md]]"
ira_report: "[[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-gmm-4-1-3-20260716T220407Z.md]]"
---

# Conceptual decision record

## Summary

Recompacted Phase **4.1.3** tertiary feedstock body **1331→≤1200** under `factory_feed_gate` / Config `max_note_body_chars.tertiary: 1200`. Preserved WorldCam/MapCam/SensoriumAttach nouns + rollup pointer; dropped duplicate ## Roll-up; tightened Interfaces/Handoff. No factory/L5. Siblings 4.1.1=**1035** / 4.1.2=**1176** (post-scrub) ≤1200.

## PMG alignment

Keeps DM observation FOV nouns mintable for Half A `pmg_phases` without inventing Camera3D ownership or collapsing SensoriumAttach into PilotGraph dominate.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Leave body at 1331 | No churn | Feed gate RED `body_over_cap` | Forbidden (`harness_forbid_deepen_noop`) |
| Split into quaternary notes | Smaller slices | Tree already closed; overkill for ~180 chars | Cap reachable via compact |
| Deepen factory/L5 | Unrelated | Out of deepen scope | Explicit forbid |

**Chosen:** in-place body compact + roll-up retention; next DFS **4.2.1** `body_over_cap:1381>1200`.

## Validation evidence

- Queue: `followup-deepen-gmm-4-1-3-20260716T220407Z`
- Gate: `factory_feed_gate` / `conceptual_note_oversized` / tertiary cap 1200
- Body measured: **1153≤1200** (before 1331)
- Sibling consistency: 4.1.1=1035; 4.1.2=1176≤1200
- Pattern: Phase-4.1.1 / 4.1.2 body-recompact-1200 trail
- Artifact: `Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845.md`
- Validator first: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-gmm-4-1-3-20260716T220407Z-20260716T221758Z.md]] — `needs_work` / `state_hygiene_failure`
- IRA: [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-gmm-4-1-3-20260716T220407Z.md]]
- Validator second: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-gmm-4-1-3-20260716T220407Z-20260716T222502Z-second-pass.md]] — `needs_work` / compare_verdict: partial
- Snapshot: `.technical/backups/20260716-221441-followup-deepen-gmm-4-1-3-20260716T220407Z/`

## Links

- Parent: [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]
- Roll-up: [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roll-up-2026-07-16]]
- Prior CDR: [[Conceptual-Decision-Records/deepen-phase-4-1-3-worldcam-mapcam-sensorium-fov-2026-07-16-0845]]
- Sibling recompact: [[Conceptual-Decision-Records/deepen-phase-4-1-2-body-recompact-1200-2026-07-16-1750]]
