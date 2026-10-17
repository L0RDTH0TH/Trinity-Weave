---
title: "CDR — HUDLayerStack + KinestheticHonestyChecklist tertiary (6.1.3)"
created: 2026-06-27
tags: [roadmap, cdr, genesis-mythos-master, phase-6, factory]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]"
decision_kind: deepen
queue_entry_id: godo-7632b96155f7
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
---

## Summary

Combined **HUDLayerStack** layer model and **KinestheticHonestyChecklist** **KH-6.1-001..004** into a single tertiary **6.1.3** to close the **6.1** depth-first branch (Launch → PlayRegion → HUD). HUD init is gated on `presentation.play_region_ready`; mode layer reflects **PerspectiveEnvelope** without initiating transitions; kinesthetic criteria remain operator attestation gates for factory catalog sign-off.

## PMG alignment

PMG requires player-facing factory Phase 0 proof: presentation shell with honest DM ortho feel and perceptible launch funnel. This slice names the HUD chrome contract and the attestation checklist that prevents catalog sign-off without kinesthetic honesty — directly supporting Half A factory spine before horizon demo gameplay (6.2).

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Split HUD and kinesthetic into **6.1.3** and **6.1.4** | Finer granularity | Extra queue round; kinesthetic criteria are inseparable from HUD **Mode** layer behavior | User guidance requested single tertiary; parent 6.1 planned three-child split (Launch, PlayRegion, HUD) |
| Embed checklist only in parent 6.1 secondary | Less duplication | Parent already oversized; triggered branch_split | Depth-first backfill requires dedicated tertiary |
| Defer kinesthetic to execution track only | Faster conceptual pass | Loses factory attestation contract at design authority | PMG + **PresentationShellManifest** require named attestation gates at conceptual depth |

## Validation evidence

- Pattern: industry HUD layer stacks (base chrome + mode indicator + transient feedback) aligned with parent 6.1 **Launch → PlayRegion → HUD** funnel.
- Bus contract: **6.1.3** exports `presentation.hud_active`; siblings export `presentation.launch_complete` (6.1.1) and `presentation.play_region_ready` (6.1.2) — no false sibling `hud_active` claims.
- Parent authority: [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]] **KinestheticHonestyChecklist** table preserved verbatim with slice ownership column added.
- Validator: [[.technical/Validator/roadmap-auto-validation-20260627T051948Z-godo-7632b96155f7]]
- Validator (second pass / L1 post-LV): [[.technical/Validator/validator-roadmap_handoff_auto-godot-godo-7632b96155f7-l1-20260627T053000Z]] — `primary_code: contradictions_detected` reconciled by repair `repair-handoff-audit-7cd4d8acc0aa`

## Links

- Parent: [[Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]
- Master goal: [[genesis-mythos-master-goal]]
- Workflow anchor: 2026-06-27 05:07 deepen Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist
