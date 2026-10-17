---
slice_id: alpha0_world_import_r1
ask_id: alpha0_world_import
series_id: alpha0_world_builder_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 1e
created: 2026-10-15
updated: 2026-10-15
operator_f5_closed: '2026-10-15T21:49:00Z'
greenlit_at: '2026-10-15T21:42:00Z'
composed_at: '2026-10-15T21:42:00Z'
claim_class: ask_success
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: KEEP_ask_success
template: Half-B-Weld-Brief-Template
prior_keep_slice: alpha0_world_s0_intents_r1
prior_keep_step: 1d
prior_keep_disposition: KEEP_soft
keeps_world_new: alpha0_world_new_r1
keeps_world_bounds: alpha0_world_bounds_r1
keeps_world_propose: alpha0_world_propose_r1
keeps_world_s0_intents: alpha0_world_s0_intents_r1
keeps_brush_tri: alpha0_stalberg_dual_tri_cell_place_r1
keeps_brush_single_deck: alpha0_stalberg_dual_single_deck_emit_r1
keeps_brush_update_four: alpha0_stalberg_dual_update_four_recompute_r1
keeps_brush_coast_bits: alpha0_stalberg_dual_place_coast_r1
keeps_brush_strip_water: alpha0_stalberg_dual_coast_strip_water_r1
keeps_brush_coast_stage6_landed: alpha0_stalberg_dual_coast_stage6_emit_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_world_import_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map: WORLD-import
success_object: world_import_play_path_stub_entry
contract: C_world_import_power_user_stub
operator_f5_confirmed: true
disposition: KEEP_ask_success
selection_rationale: map_section_1_after_WORLD-s0-intents_next_is_WORLD-import
full_canon_ingest: barred_this_slice
---

# Slice brief — `alpha0_world_import_r1`

**KEEP/ask_success** (operator F5 — honest stub Success; full canon ingest still barred). Prior **1d** [[alpha0_world_s0_intents_r1]] **KEEP soft** (operator soft-success close; framing debt noted — do not expand s0). Brush §0 closed. Owned Full = flat single-deck green KEEP. `claim_class: ask_success` until operator F5 on **this** ticket only. **Not** full canon ingest Done.

**Choice:** After WORLD-s0-intents, map §1 next = **`WORLD-import`** (world or offline history canon bundle — PMG power-user path). Series step **1e**. Scaffolding thin ⇒ Prefer + LaunchShell **Import World** peer entry with honest F5 bar.

**Altitude:** Campaigns attach later — do **not** integrate campaign attach into Create World. Import is a **peer** menu entry, not nested in Create World / Session 0.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_world_builder_r1]]. Map: `WORLD-import` in [[World-Builder-Mini-Game-Ticket-Map]]. Feedstock: [[dual-grid-nested-placetile-world-authorship]].

## Why (binding)

| Gate | Detail |
|------|--------|
| WORLD-import | Power-user path to bring world / offline history canon bundle |
| Play path | LaunchShell **Import World** peer button (not inside Create World) |
| Honesty | Stub acknowledges path; **full canon ingest barred** this slice |
| KEEP | 1a–1d Create World path; Full single-deck; campaigns empty on new world |
| Out of scope | Full ingest Done · GEN-* · PACK-save · campaign attach · Terrain3D · Townscaper Done · expand s0 |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_world_import` |
| `slice_id` | `alpha0_world_import_r1` |
| `success_object` | **`world_import_play_path_stub_entry`** |
| Scope | Prefer + LaunchShell Import World stub; clear bar on full ingest |
| `claim_class` | `staging` until operator F5 |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Map ticket | `WORLD-import` |

## 2. Must / refuse

| Must | Refuse if |
|------|-----------|
| Visible **Import World** on LaunchShell (peer to Create World) | Docs-only / orphan UI off LaunchShell |
| Press → visible stub status (banner + metas); full ingest = false | Silent no-op sold as import |
| Honest scaffolding / barred full ingest messaging | Stub sold as full canon ingest Done |
| Create World path still works; campaigns empty | Campaign attach on Create World / Import |
| LaunchShell remains main_scene | main_scene WorldgenCraft regress |
| Owned Full stays single-deck flat green | MeshFit Full GLB · expand Session 0 |

## 3. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** LaunchShell shows Import World peer entry → press → visible WORLD-import stub (banner + status code barring full ingest) → Create World path still reachable; campaigns empty; Full single-deck KEEP. MCP alone ≠ Success. Full canon ingest Done = **out**. |
| Out | Full canon ingest Done · GEN-terrain Done · PACK-save · campaign attach · Terrain3D · Townscaper product Done · expand s0 |

## 4. Refuse (`do_not_waive`)

`full_canon_ingest_as_stub_success` · `import_nested_in_create_world` · `campaign_attach_on_world_create` · `silent_import_noop` · `expand_s0_as_import` · `gen_fill_as_import` · `orphan_import_off_play_path` · `full_glb_meshfit` · `y_bias_as_zfight_fix` · `verify_mcp_only` · `terrain3d_in_scope` · `townscaper_product_done`

## 5. LIVE weld (implementer)

- `Core/WorldGen/WorldCanonImportStub.cs` — **new** stub record + status codes
- `Core/WorldGen/WorldPackage.cs` · `WorldPackageSession.cs` — schema v5 · import metas · BindImportStub
- `LaunchShell.tscn` · `LaunchShell.cs` — **Import World** peer button + honest banner
- DualGridCraftHost **unchanged** (brush KEEP)
- Create World / WorldgenGui path **KEEP** (no s0 expand)

## 6. Operator F5 bar

Layer 0 owns the long tutorial. Compact: F5 → Import World visible → press → stub banner (full ingest barred) → Create World still works; Full still flat green.

## Related

- Prior KEEP soft [[alpha0_world_s0_intents_r1]] · [[alpha0_world_propose_r1]] · [[alpha0_world_bounds_r1]] · [[alpha0_world_new_r1]] · Map [[World-Builder-Mini-Game-Ticket-Map]] · Series [[alpha0_world_builder_r1]]
