---
slice_id: alpha0_world_empty_campaigns_r1
ask_id: alpha0_world_empty_campaigns
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1f
created: 2026-10-15
updated: 2026-10-15
operator_f5_closed: '2026-10-15T22:00:00Z'
greenlit_at: '2026-10-15T22:00:00Z'
composed_at: '2026-10-15T22:00:00Z'
claim_class: ask_success
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: KEEP_ask_success
template: Half-B-Weld-Brief-Template
prior_keep_slice: alpha0_world_import_r1
prior_keep_step: 1e
prior_keep_disposition: KEEP_ask_success
keeps_world_new: alpha0_world_new_r1
keeps_world_bounds: alpha0_world_bounds_r1
keeps_world_propose: alpha0_world_propose_r1
keeps_world_s0_intents: alpha0_world_s0_intents_r1
keeps_world_import: alpha0_world_import_r1
keeps_brush_tri: alpha0_stalberg_dual_tri_cell_place_r1
keeps_brush_single_deck: alpha0_stalberg_dual_single_deck_emit_r1
keeps_brush_update_four: alpha0_stalberg_dual_update_four_recompute_r1
keeps_brush_coast_bits: alpha0_stalberg_dual_place_coast_r1
keeps_brush_strip_water: alpha0_stalberg_dual_coast_strip_water_r1
keeps_brush_coast_stage6_landed: alpha0_stalberg_dual_coast_stage6_emit_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_world_empty_campaigns_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map: WORLD-empty-campaigns
success_object: world_owns_self_campaigns_guest_contract
contract: C_world_empty_campaigns_guest
operator_f5_confirmed: true
disposition: KEEP_ask_success
selection_rationale: map_section_1_after_WORLD-import_next_is_WORLD-empty-campaigns
campaign_attach: deferred_not_world_create_success
---

# Slice brief — `alpha0_world_empty_campaigns_r1`

**KEEP/ask_success** (operator F5 SUCCESS — empty campaigns lawful; world owns itself; attach later). Prior **1e** [[alpha0_world_import_r1]] **KEEP/ask_success**. Brush §0 closed. Owned Full = flat single-deck green KEEP. Next §1 = [[alpha0_world_parity_r1]] WORLD-parity (1g).

**Choice (closed):** After WORLD-import, map §1 next was **`WORLD-empty-campaigns`**. Series step **1f**. WORLD-parity deferred to **1g**.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `WORLD-empty-campaigns` in [[World-Builder-Mini-Game-Ticket-Map]]. Feedstock: [[dual-grid-nested-placetile-world-authorship]].

## Why (binding)

| Gate | Detail |
|------|--------|
| WORLD-empty-campaigns | Zero campaigns is a lawful saved-world state |
| Ownership | World owns itself; campaigns are later guests |
| Play path | LaunchShell + Create World + HUD show empty-campaigns honesty |
| KEEP | 1a–1e; Import stub; Full single-deck; LaunchShell main |
| Out of scope | Campaign attach Done · ToneProfile campaign bind · GEN-* · PACK-save · Townscaper Done |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_world_empty_campaigns` |
| `slice_id` | `alpha0_world_empty_campaigns_r1` |
| `success_object` | **`world_owns_self_campaigns_guest_contract`** |
| Scope | Prefer + empty-campaigns guest law on package + Play-path chrome |
| `claim_class` | `ask_success` (operator F5) |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Map ticket | `WORLD-empty-campaigns` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Create World opens package with campaigns=0 as **lawful** | Empty treated as defect / missing campaign |
| Visible Play-path copy: attach later · world owns itself | Docs-only / silent meta-only |
| Campaign ownership meta = world_owns_self_campaigns_guest | Campaign owns world / attach on Create World |
| Import stub KEEP; Create World path KEEP | Regress Import peer or nest attach in Create World |
| LaunchShell remains main_scene; Full single-deck KEEP | main_scene WorldgenCraft · MeshFit Full GLB |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (ask_success):** LaunchShell empty-campaigns framing → Create World → campaigns=0 lawful → no campaign attach UI → Import stub KEEP; Full single-deck KEEP. **Operator confirmed SUCCESS.** |
| Out | Campaign attach Done · GEN-fill as Success · PACK-save · Townscaper product Done |

## 4. Refuse (`do_not_waive`)

`campaign_attach_as_world_create_success` · `campaign_owns_world` · `empty_campaigns_as_defect` · `tone_profile_campaign_bind_as_world_create` · `gen_fill_as_empty_campaigns` · `parity_as_empty_campaigns` · `full_canon_ingest_as_stub_success` · `full_glb_meshfit` · `y_bias_as_zfight_fix` · `verify_mcp_only` · `terrain3d_in_scope` · `townscaper_product_done`

## 5. LIVE weld (landed / KEEP)

- `Core/WorldGen/WorldEmptyCampaignsContract.cs` — guest/ownership law (**KEEP binding**)
- `Core/WorldGen/WorldPackage.cs` · `WorldPackageSession.cs` — empty-campaigns metas (superseded schema pointer → 1g)
- `LaunchShell.cs` — empty-campaigns framing (**KEEP**; active chrome advances to parity)
- DualGridCraftHost **unchanged** (brush KEEP)

## Related

- Next [[alpha0_world_parity_r1]] · Prior KEEP [[alpha0_world_import_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]]
