---
title: Staging receipt — alpha0_gen_terrain_r1
slice_id: alpha0_gen_terrain_r1
ask_id: alpha0_gen_terrain
series_id: alpha0_world_builder_r1
series_step: 2a
producer_run_id: sp-gen-terrain-r1-greenlight-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
live_weld_landed: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: gen_terrain_dualgrid_height_starter
contract: C_gen_terrain_explicit_populate
ticket_map: GEN-terrain
craft_enter_empty: kept_1g
gen_fill_as_craft_enter: barred
explicit_generate: Key.T
height_contract: stub_value_noise
completed: 2026-10-15T22:24:00Z
status: live_weld_landed_staging_awaiting_f5
prior_world: alpha0_world_parity_r1
prior_disposition: empty_enter_folded_KEEP
selection_rationale: map_section_2_first_GEN-terrain_after_1g_empty_enter_KEEP
not_selected: GEN-biomes_GEN-history
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
trinity_branch: project/genesis-mythos-master
trinity_project_sha: 53e5c32b00cbe6497103e92a99c429cb9183a7df
trinity_live_weld_sha: c8c92f331d4534a93122c24e319f6baa4a2905e2
trinity_prior_tip: 54fc84b
trinity_push: direct_export_project_push_force_with_lease
trinity_tip_note: tip_53e5c32 (receipt); live weld tip_c8c92f3; prior tip_54fc84b; GEN-terrain 2a after 1g empty-enter KEEP
curator_snapshot: skipped_push_enabled_false
dotnet_build: succeeded_0_errors
---

# Staging receipt — alpha0_gen_terrain_r1

**GREENLIGHT WELD LIVE** — Prefer concept + first **GEN-terrain** populate. Series step **2a**.

**1g note:** Empty craft enter folded into [[alpha0_world_parity_r1]] — **KEEP**; this weld does not undo that law. GEN self-populates only on explicit Generate (**T**).

**Honesty bar:** Land/water dual-grid paint from dials+bias + height contract stub + river corridors. Full noise→gradient→erosion stack / VIS-height / DF-hours = later. Not GEN-biomes/history. Not Townscaper Done.

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_gen_terrain_r1.prefer-result.json → ok · concept_prefer_ok: true |
| Law | Prefer-Authorship-Host-Law · explicit Generate · empty enter KEEP |
| Map | `GEN-terrain` in [[World-Builder-Mini-Game-Ticket-Map]] |

## LIVE code changed

| File | Change |
|------|--------|
| `Core/WorldGen/GenTerrainContract.cs` | **new** law |
| `Core/WorldGen/GenTerrainService.cs` | **new** compute (value noise land/water/height/rivers) |
| `Systems/DualGridCraftHost.cs` | `ApplyGenTerrainPass` (empty-enter arm KEEP; clears gen state only) |
| `Systems/WorldgenCraft.cs` | Key.T → RunGenTerrainGenerate |
| `Core/WorldGen/WorldPackage.cs` · `WorldPackageSession.cs` | schema v8 · gen metas |
| `LaunchShell.cs` · `UI/WorldgenCraftControls.cs` | chrome / hints empty→T→populate |

## MCP / build (not ask_success)

- Empty enter still logs `craft_enter_empty=true`; showcase not called from overlay arm
- `ApplyGenTerrainPass` only from WorldgenCraft Key.T
- `dotnet build` ok (0 errors)

## Operator F5 bar (facts for Layer 0)

1. Enter Craft / Create World→Open → **empty amber board** (1g KEEP)
2. Press **T** → dual-grid land/water populates from dials/bias; rivers carve; height stub logged
3. HUD/hint shows GEN applied counts; campaigns=0 lawful
4. Fail: silent fill on enter · DF-hours Done claim · Townscaper Done · MCP-only attest

## Trinity / Curator

| Item | Value |
|------|-------|
| Branch | `project/genesis-mythos-master` |
| Tip | `53e5c32b00cbe6497103e92a99c429cb9183a7df` (receipt; live `c8c92f3`) |
| Push | force-with-lease OK |
| Curator | skipped (`git.push_enabled: false`) |

## Related

- Prior [[alpha0_world_parity_r1]] · Series [[alpha0_world_builder_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]]
