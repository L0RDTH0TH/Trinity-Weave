---
title: Staging receipt — alpha0_world_parity_r1
slice_id: alpha0_world_parity_r1
ask_id: alpha0_world_parity
series_id: alpha0_world_builder_r1
series_step: 1g
producer_run_id: sp-world-parity-r1-empty-craft-enter
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: procedural_manual_craft_peer_contract
contract: C_world_parity_authorship_peers
ticket_map: WORLD-parity
craft_enter_empty: true
gen_fill_as_craft_enter: barred
completed: 2026-10-15T22:13:48Z
status: live_weld_landed_staging_awaiting_f5
prior_keep: alpha0_world_empty_campaigns_r1
prior_disposition: KEEP_ask_success
selection_rationale: map_section_1_after_WORLD-empty-campaigns_WORLD-parity_closes_section_1
partial_abort_check: no_world_parity_prefer_or_live_partials_found
not_selected: GEN-terrain
selection_choice: WORLD-parity_1g_not_GEN-terrain_2a
empty_enter_fold: folded_into_1g_not_new_slice
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
trinity_branch: project/genesis-mythos-master
trinity_project_sha: 54fc84bbd5ee8a19a681536780b7fd68a02303fe
trinity_live_weld_sha: 815085ca971cbaec136eaceceb4eb6435c76250c
trinity_prior_tip: 70a0e7a91e447ad39558a03f4d3015ab875a7413
trinity_push: direct_export_project_push_force_with_lease
trinity_tip_note: tip_54fc84b; weld_815085c; prior tip_70a0e7a; empty-enter fold into 1g
curator_snapshot: skipped_push_enabled_false_and_mass_cursor_rules_dirt
dotnet_build: succeeded_0_errors
---

# Staging receipt — alpha0_world_parity_r1

**GREENLIGHT WELD LIVE** (amended) — peer law + **empty craft enter** folded into **1g** Success bar (not a new GEN slice; not `alpha0_world_craft_empty_enter_r1`).

**Choice:** Map §1 last after WORLD-empty-campaigns = **`WORLD-parity`** (procedural ↔ manual craft peers — feedstock). Series step **1g**. Closes §1 before **GEN-terrain** (§2a) — **not** selected this weld. GEN-* owns self-populate later.

Brush §0 **closed**. LaunchShell remains `main_scene`. Create World + Import + empty-campaigns KEEP (1a–1f).

## Root cause (pre-fill)

`DualGridCraftHost.BuildOrganicDualCornerOverlay` called `SeedDualVisualFamilyShowcase` before dual MeshLibrary arm — demo Full/edge/corner silhouettes on every craft enter. Secondary: `WorldgenCraft._Ready` auto-`ImportAttach` restored persist occupancy when present.

## Fix one-liner

Gate showcase seed + auto-import off craft enter; keep LMB place / I re-attach; document GEN fill ≠ craft-enter Success on 1g.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_world_parity_r1.prefer-result.json → ok · concept_prefer_ok: true |
| Law | Prefer-Authorship-Host-Law · procedural↔manual peers · empty craft enter |
| Feedstock | dual-grid-nested-placetile-world-authorship · full procedural and full manual are peers |
| Honesty | Not GEN-fill Done · GEN fill ≠ craft-enter Success · not Townscaper product Done |

## LIVE code changed

| File | Change |
|------|--------|
| `Core/WorldGen/WorldParityContract.cs` | peer law + `EmptyCraftEnterLaw` / gen-fill-as-enter barred |
| `LaunchShell.cs` | empty-enter Controls + subtitle |
| `Systems/DualGridCraftHost.cs` | remove showcase seed from overlay arm; opt-in method only |
| `Systems/WorldgenCraft.cs` | gate auto ImportAttach; I key KEEP |
| Docs | ticket map · brief · armed · this receipt |

## MCP / build (not ask_success)

- Prefer topology: WorldParityContract empty-enter + LaunchShell framing present
- Showcase seed not called from EnsureHost / BuildOrganicDualCornerOverlay
- `dotnet build` ok (0 errors)

## KEEP

- **1a–1e** world path · **1f** empty-campaigns **KEEP/ask_success**
- **1d** soft framing debt (do not expand)
- Place tools / FlipOrganicCorner / Full single-deck when painted
- Import explicit (I / menu) — not auto on enter
- 2z strip-water · 2w single-deck · 2u/2x/2y-bits · 2aa coast emit LIVE parked

## Operator F5 bar (facts for Layer 0)

1. F5 / main lands on LaunchShell — subtitle frames WORLD-parity peers + empty craft enter
2. Create World and Enter Craft share equal bronze peer chrome; Controls lists empty-enter + GEN later
3. Enter Craft or Create World→Open → **amber board only** (no pre-placed Fulls/coasts); LMB still paints
4. Import World peer stub / I re-attach KEEP; campaigns=0 lawful; Full still flat single-deck when painted
5. Fail: showcase/auto-import/GEN-fill sold as craft-enter or parity Success; Townscaper Done; MCP-only attest; ask_success without operator F5

## Trinity / Curator

| Item | Value |
|------|-------|
| Branch | `project/genesis-mythos-master` |
| Push | **ok** tip `54fc84b` (weld `815085c`) force-with-lease (prior `70a0e7a`) |
| Curator | **skipped** — `git.push_enabled: false` + mass `.cursor/rules` dirt risk |
| Blockers | Operator F5 on parity peers + empty enter; GEN-terrain / PACK-save / campaign attach deferred; 1d framing debt follow-up (not this weld) |

## Related

- Brief [[alpha0_world_parity_r1]] · Prior KEEP [[alpha0_world_empty_campaigns_r1]] · Series [[alpha0_world_builder_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]
