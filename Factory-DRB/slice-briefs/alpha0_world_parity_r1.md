---
slice_id: alpha0_world_parity_r1
ask_id: alpha0_world_parity
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1g
created: 2026-10-15
updated: 2026-10-15
greenlit_at: '2026-10-15T22:03:00Z'
composed_at: '2026-10-15T22:03:00Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: live_weld_landed_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_keep_slice: alpha0_world_empty_campaigns_r1
prior_keep_step: 1f
prior_keep_disposition: KEEP_ask_success
keeps_world_new: alpha0_world_new_r1
keeps_world_bounds: alpha0_world_bounds_r1
keeps_world_propose: alpha0_world_propose_r1
keeps_world_s0_intents: alpha0_world_s0_intents_r1
keeps_world_import: alpha0_world_import_r1
keeps_world_empty_campaigns: alpha0_world_empty_campaigns_r1
keeps_brush_tri: alpha0_stalberg_dual_tri_cell_place_r1
keeps_brush_single_deck: alpha0_stalberg_dual_single_deck_emit_r1
keeps_brush_update_four: alpha0_stalberg_dual_update_four_recompute_r1
keeps_brush_coast_bits: alpha0_stalberg_dual_place_coast_r1
keeps_brush_strip_water: alpha0_stalberg_dual_coast_strip_water_r1
keeps_brush_coast_stage6_landed: alpha0_stalberg_dual_coast_stage6_emit_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_world_parity_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map: WORLD-parity
success_object: procedural_manual_craft_peer_contract
contract: C_world_parity_authorship_peers
operator_f5_confirmed: false
disposition: staging
selection_rationale: map_section_1_after_WORLD-empty-campaigns_next_is_WORLD-parity_closes_section_1
campaign_attach: deferred_not_world_create_success
gen_fill: barred_as_parity_success
townscaper_done: barred_as_parity_success
craft_enter_empty: true
gen_fill_as_craft_enter: barred
---

# Slice brief — `alpha0_world_parity_r1`

**GREENLIGHT WELD LIVE** — Prefer concept + **WORLD-parity** peer law on Play path + **empty craft enter**. Prior **1f** [[alpha0_world_empty_campaigns_r1]] **KEEP/ask_success**. Brush §0 closed. Owned Full = flat single-deck green KEEP (when operator paints). `claim_class: staging` until operator F5 on **this** ticket only.

**Choice:** After WORLD-empty-campaigns KEEP, map §1 last = **`WORLD-parity`** (full procedural and full manual craft are peers — feedstock). Series step **1g**. §1 not complete until this ticket; **not** jumping to GEN-terrain / §2a.

**Altitude:** Procedural = Create World propose/scaffold path (honest; GEN-* fill still later). Manual = Enter Craft dual-grid brush (honest; not Townscaper Done). Peers — neither demoted. **Both lanes open empty craft** (amber board; no pre-placed Fulls / coast stamps / showcase seed / auto-import fill). Place tools KEEP for manual paint. **GEN fill ≠ craft enter Success** — GEN-* owns self-populate later. Empty campaigns remain lawful (1f KEEP). No campaign attach on create.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `WORLD-parity` in [[World-Builder-Mini-Game-Ticket-Map]]. Feedstock: [[dual-grid-nested-placetile-world-authorship]].

## Why (binding)

| Gate | Detail |
|------|--------|
| WORLD-parity | Procedural and manual craft are first-class peers |
| Play path | Create World + Enter Craft equal chrome weight; HUD/parity metas |
| Empty craft enter | Amber board on Open/Enter — no showcase Fulls, no auto-import occupancy, no GEN self-fill |
| Honesty | Not GEN-fill Done · GEN fill ≠ craft-enter Success · not Townscaper product Done |
| KEEP | 1a–1f; Import stub (explicit I / menu); empty campaigns lawful; Full single-deck place; LaunchShell main |
| Out of scope | GEN-terrain Done · fake GEN-fill as Success · Townscaper Done · campaign attach · PACK-save |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_world_parity` |
| `slice_id` | `alpha0_world_parity_r1` |
| `success_object` | **`procedural_manual_craft_peer_contract`** |
| Scope | Prefer + parity peer law on package + Play-path chrome |
| `claim_class` | `staging` until operator F5 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Map ticket | `WORLD-parity` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Create World + Enter Craft framed as **peers** on LaunchShell | Manual demoted / procedural-only Success |
| Parity metas + HUD on Play path (both lanes) | Docs-only / silent meta-only |
| Craft opens **empty** (amber; place tools KEEP) | Showcase seed / auto-import Fulls / GEN self-fill on enter |
| Empty campaigns KEEP; no campaign attach on create | Campaign attach / empty-as-defect regress |
| Import stub KEEP (explicit); Full single-deck place KEEP | Regress Import or MeshFit Full GLB |
| LaunchShell remains main_scene | main_scene WorldgenCraft |
| Honest: GEN-fill / Townscaper Done barred as this Success | Fake GEN-fill or Townscaper Done as parity Success |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** LaunchShell shows WORLD-parity peer framing → Create World (procedural peer) and Enter Craft (manual peer) both first-class → **both open empty amber craft** (no pre-placed Fulls/coasts) → place tools still paint → HUD shows parity / lane → campaigns=0 lawful; Import KEEP (explicit); Full single-deck when painted. MCP alone ≠ Success. GEN-fill Done / GEN-fill-as-enter / Townscaper Done = **out**. |
| Out | GEN-terrain Done · fake GEN-fill as Success · GEN fill as craft-enter Success · Townscaper product Done · campaign attach · PACK-save · Terrain3D |

## 4. Refuse (`do_not_waive`)

`gen_fill_as_parity_success` · `gen_fill_as_craft_enter_success` · `showcase_seed_on_craft_enter` · `auto_import_fill_on_craft_enter` · `townscaper_done_as_parity_success` · `procedural_only_as_success` · `manual_demoted_as_toy` · `campaign_attach_as_world_create_success` · `empty_campaigns_as_defect` · `full_canon_ingest_as_stub_success` · `full_glb_meshfit` · `y_bias_as_zfight_fix` · `verify_mcp_only` · `terrain3d_in_scope`

## 5. LIVE weld (implementer)

- `Core/WorldGen/WorldParityContract.cs` — peer law + **empty craft enter** law
- `Core/WorldGen/WorldPackage.cs` · `WorldPackageSession.cs` — schema v7 · parity metas · BindParityPeers
- `LaunchShell.cs` — peer chrome · empty-enter Controls · Play path wiring · HUD parity hints
- `Systems/DualGridCraftHost.cs` — **remove showcase seed on overlay arm** (opt-in MCP only)
- `Systems/WorldgenCraft.cs` — **gate auto ImportAttach** on enter (I key KEEP)
- `WorldCanonImportStub.cs` — KEEP; parity summary on stub line
- `WorldEmptyCampaignsContract.cs` — KEEP binding (comment only)

## 6. Operator F5 bar

Layer 0 owns the long tutorial. Compact: F5 → LaunchShell parity framing → Create World and Enter Craft both peer chrome → **craft opens empty amber** → LMB still places Full → campaigns=0; Import KEEP via I/menu; no GEN-fill / Townscaper Done claim.

## Related

- Prior KEEP [[alpha0_world_empty_campaigns_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]]
