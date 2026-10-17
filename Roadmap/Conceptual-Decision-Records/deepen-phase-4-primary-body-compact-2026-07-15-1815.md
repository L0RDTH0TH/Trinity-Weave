---
title: Conceptual decision record — Phase 4 primary body compact under factory feed cap
created: 2026-07-15
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-4, body-compact]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase4-20260715T221000Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
---

# Conceptual decision record

## Summary

Compacted Phase **4** primary body **7319→1899** chars (≤2000 primary harness / feed cap) and preserved handoff table, roll-up gates, open questions, consistency, and dataview in rollup [[Phase-4-Perspective-Split-and-Control-Systems-Roll-up-2026-07-15]]. Clears `conceptual_note_oversized` for this path under `factory_feed_gate` mint_batch `pmg_phases`. Next DFS cursor: Phase-4-1 secondary (`9659>1400`).

## PMG alignment

Keeps perspective-split / control-systems feedstock factory-feedable without truncating design nouns — rollup retains handoff evidence and advisory gate contract that serve Phase 4→5 advance.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Leave oversized body | No rewrite risk | Blocks factory feed readiness | Gate RED; forbidden deepen_noop |
| Delete detail permanently | Fastest shrink | Loses handoff evidence | Violates NL preservation |
| Atomize new tertiaries this run | Smaller primary | Scope creep vs single compact | Deferred; DFS next = 4.1 secondary compact |

**Chosen path:** Body compact + new rollup child (same pattern as Phase 1 / Phase 3 primaries).

## Validation evidence

- Pattern: Phase 1 primary compact 6077→1968; Phase 3 primary 7979→1894
- Parent path: `Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914.md`
- Harness: `factory_feed_gate` reason `body_over_cap:7319>2000` → cleared for this slice; next cursor Phase-4-1 (`9659>1400`)
- Measured body raw **1899** ≤2000 (pre **7319**)
- Snapshot (local pre-compact): `1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/.snapshots/20260715-181405-Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914.md`
- Snapshot (Backup twin): `Backups/Per-Change/Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914--2b95cff3--20260715-181405.md.bak`

## Validator trace

- **validator_first:** `needs_work` — `primary_code: state_hygiene_failure` — `reason_codes: state_hygiene_failure,contradictions_detected,safety_unknown_gap,missing_roll_up_gates`
- **report:** [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase4-20260715T221000Z-20260715T221725Z.md]]
- **ira_call_index:** 1 — **ira_applied:** true — **validation_hygiene:** reconciled
- **ira_report:** [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-phase4-20260715T221000Z.md]]
- **execution_gaps_advisory:** true — `missing_roll_up_gates` / forward `safety_unknown_gap` remain conceptual-track advisory (no HR pins invented)
- **compare_verdict:** improved_vs_first_pass_ira_hygiene_repaired_core_eligible_log_only
- **second_pass:** [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase4-20260715T221000Z-20260715T222103Z-second-pass.md]]
- **validator_second:** log_only
- **primary_code_active:** safety_unknown_gap
- **validation_status:** pending_validator_second_pass

## Links

- Parent roadmap note: [[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-06-26-0914]]
- Rollup: [[Phase-4-Perspective-Split-and-Control-Systems-Roll-up-2026-07-15]]
- Queue: `followup-deepen-phase4-20260715T221000Z`
