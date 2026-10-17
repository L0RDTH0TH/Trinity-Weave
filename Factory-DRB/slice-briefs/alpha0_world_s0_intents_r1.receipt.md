---
title: Staging receipt — alpha0_world_s0_intents_r1
slice_id: alpha0_world_s0_intents_r1
ask_id: alpha0_world_s0_intents
series_id: alpha0_world_builder_r1
series_step: 1d
producer_run_id: sp-world-s0-intents-r1-greenlight-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: session0_intent_proposed_accepted_board
contract: C_world_s0_intents_collaborative
ticket_map: WORLD-s0-intents
completed: 2026-10-15T21:06:00Z
status: live_weld_landed_staging_awaiting_f5
prior_keep: alpha0_world_propose_r1
prior_disposition: KEEP_ask_success
selection_rationale: map_section_1_after_WORLD-propose_highest_priority_WORLD-s0-intents
partial_abort_check: no_world_s0_intents_prefer_or_live_partials_found
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
trinity_branch: project/genesis-mythos-master
trinity_project_sha: dbb14e9936ce2016e1d54b5f7daab1dd97dade54
trinity_live_weld_sha: 477a0b6ffd1c08dda62073e0f2a5615d08f9f7d9
trinity_prior_tip: d17f89786f800d1e64603d291f2afc8523f241ee
trinity_push: direct_export_project_push_force_with_lease
trinity_tip_note: tip_dbb14e9; weld_477a0b6; prior_d17f897; 1c_KEEP; 1d_WORLD-s0-intents
ui_layout_deferred_to_sibling: true
curator_snapshot: skipped_push_enabled_false_and_mass_cursor_rules_dirt
---

# Staging receipt — alpha0_world_s0_intents_r1

**GREENLIGHT WELD LIVE** after operator **1c WORLD-propose F5 SUCCESS** (KEEP/ask_success).

**Choice:** Map §1 next after WORLD-propose = **`WORLD-s0-intents`** (collaborative Session 0 intents proposed→accepted). Series step **1d**.

Brush §0 **closed** — **2z KEEP/ask_success**; **2w KEEP / 2v SUPERSEDED**; **2u/2x/2y-bits KEEP**; **2aa** coast emit KEEP LIVE parked. LaunchShell remains `main_scene`.

**UI layout:** WorldgenGui anchors/ScrollContainer/widescreen clipping **deferred to sibling** — this weld is product Prefer on Play path only.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_world_s0_intents_r1.prefer-result.json → ok · concept_prefer_ok: true |
| Law | Prefer-Authorship-Host-Law · Session 0 intents on LaunchShell Play path |
| Feedstock | dual-grid-nested-placetile-world-authorship · player may seed intents |

## LIVE code changed

| File | Change |
|------|--------|
| `Core/WorldGen/WorldSession0Intent.cs` | **new** — intent record proposed/accepted/rejected + seat |
| `Core/WorldGen/WorldSession0IntentBoard.cs` | **new** — collaborative seed bank · Accept/Reject · ≥1 gate |
| `Core/WorldGen/WorldPackage.cs` | schema v4 · Intents on package · slice 1d ids |
| `Core/WorldGen/WorldPackageSession.cs` | BindNew(+intents) · intent metas |
| `UI/WorldgenGui.cs` | Intents phase after Accept scaffold (**no** `.tscn` layout edits) |
| `LaunchShell.cs` | Bind intents; HUD s0 count |
| `Systems/DualGridCraftHost.cs` | **unchanged** — single-deck Full KEEP |

## MCP verify (not ask_success)

- Prefer topology: WorldSession0IntentBoard + WorldgenGui Intents phase + LaunchShell present
- DualGridCraftHost not mutated
- `dotnet build` ok

## KEEP

- **1a** WORLD-new · **1b** WORLD-bounds · **1c** WORLD-propose ask_success
- 2z strip-water · 2w single-deck · 2u/2x/2y-bits · 2aa coast emit LIVE parked

## Operator F5 bar (facts for Layer 0)

1. F5 / main lands on LaunchShell (Create World + Enter Craft + Controls)
2. Create World → bias → dials → Propose scaffold → Accept scaffold → **Session 0 intents** phase (player/DM/shared seeds)
3. Accept ≥1 intent (optionally Reject or Propose seed) → Open world → craft; HUD shows scaffold + s0=N + dials + world_id; campaigns empty
4. Owned Full still flat single-deck green (brush KEEP)
5. Fail: Open world with 0 accepted intents; GEN-fill as Success; DM-wizard-only sold as collaborative; MCP-only attest; ask_success without operator F5

## Trinity / Curator

| Item | Value |
|------|-------|
| Branch | `project/genesis-mythos-master` |
| Push | **ok** tip `dbb14e9` (weld `477a0b6`) force-with-lease (prior `d17f897`) |
| Curator | **skipped** — `git.push_enabled: false` + mass `.cursor/rules` dirt risk |
| Blockers | Operator F5 on WORLD-s0-intents only; WORLD-import / GEN-* / PACK-save deferred; UI layout sibling |
| Deferred UI | WorldgenGui layout/anchors/ScrollContainer left to sibling |

## Related

- Brief [[alpha0_world_s0_intents_r1]] · Prior KEEP [[alpha0_world_propose_r1]] · Series [[alpha0_world_builder_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]
