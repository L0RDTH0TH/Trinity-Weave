---
slice_id: alpha0_stalberg_dual_place_product_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: place_product
created: 2026-10-16
updated: 2026-10-16
composed_at: '2026-10-16T21:12:37Z'
prefer_authored_at: '2026-10-16T21:12:37Z'
prefer_thickened_at: '2026-10-16T22:08:18Z'
prior_recovery: alpha0_place_thrash_rollback_r1
supersedes_thrash: alpha0_stalberg_dual_piggyback_ghost_place_r1
claim_class: staging
factory_greenlit: false
live_weld_greenlit: false
live_weld_landed: false
prefer_concept_required: true
status: prefer_draft_awaiting_gate_a_b
template: Half-B-Weld-Brief-Template
keeps_brush_tri: alpha0_stalberg_dual_tri_cell_place_r1
keeps_brush_single_deck: alpha0_stalberg_dual_single_deck_emit_r1
keeps_brush_update_four: alpha0_stalberg_dual_update_four_recompute_r1
keeps_brush_coast_bits: alpha0_stalberg_dual_place_coast_r1
keeps_brush_strip_water: alpha0_stalberg_dual_coast_strip_water_r1
keeps_brush_coast_stage6_landed: alpha0_stalberg_dual_coast_stage6_emit_r1
prior_world_slice: alpha0_gen_biomes_r1
prior_world_disposition: staging_awaiting_f5_after_place_honest
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_place_product_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
ticket_map_id: PLACE-product
success_object: grey_ghost_lmb_permanent_opaque_full_plate
contract: C_place_product_ghost_to_opaque_full
operator_f5_confirmed: false
disposition: staging
map_fidelity_hostile_ok: false
do_not_arm_next: GEN-sites
next_world_armed: false
gen_biomes_pointer: alpha0_gen_biomes_r1
gen_biomes_note: Gate_B_plus_F5_after_place_product_honest
---

# Slice brief — `alpha0_stalberg_dual_place_product_r1`

**Prefer draft only — NOT greenlit · NOT welded.** One recovery **step** (not full world-builder fidelity). Meaning-minimal **place product**: on Enter Craft, grey ghost preview under cursor → LMB → **permanent opaque Full plate** on the **same seat**, with owned update-four + coast gate still running, and neighbor rebuild **not** deleting that Full. Not wording-minimal mechanics (SeatPolygon / stamp / Cull / piggyback-skip / `update_four=false` theater).

**Recovery context:** Place thrash rolled back to Trinity `2675d22` FlipOrganicCorner baseline ([[alpha0_place_thrash_rollback_r1.receipt]]). Piggyback [[alpha0_stalberg_dual_piggyback_ghost_place_r1.receipt]] SUPERSEDED / never KEEP. GEN-tone · PACK organic_seed · GEN-biomes assign/probe/pack **stay intact** and are **out of Success** — this ticket does **not** own GEN-biomes. GEN-biomes still **staging awaiting F5** but **after** place product is honest.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Map: `PLACE-product` in [[World-Builder-Mini-Game-Ticket-Map]]. Law: [[Prefer-Authorship-Host-Law]] § C.3 + Gate A/B. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]].

## Why (binding)

| Gate | Detail |
|------|--------|
| Place product | Grey ghost → LMB → permanent opaque Full on the **same seat** (stranger sentence) |
| Same seat | Ghost preview seat == committed Full seat after LMB |
| Owned gates | **Owned update-four and coast gate still run** on LMB place — required |
| Neighbor | Neighbor rebuild **must not delete** that Full |
| Intent/feel | Operator F5 validates intended behavior — not Prefer prose shape |
| Refuse wording-minimal | SeatPolygon-as-success · piggyback-as-success · piggyback-skip / `update_four=false` on LMB · CullMode-as-success · log-tag-as-success · `intent_collapsed_to_mechanics` |
| Brush KEEP | 2u/2w/2x/2y/2z KEEP-real · 2aa parked · do not reopen §0 as Success |
| World ladder | Biome assign/probe/pack stay; do **not** own GEN-biomes. Do **not** arm GEN-sites. GEN-biomes F5 **after** place honest |
| Claim | `claim_class: staging` until Gate B + operator F5 · **never KEEP in this draft** |

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_place_product_r1` |
| `ticket_map_id` | **`PLACE-product`** |
| `success_object` | **`grey_ghost_lmb_permanent_opaque_full_plate`** |
| Scope | Prefer compose fields for Gate A+B · staging until F5 · no weld this session |
| `claim_class` | staging |
| `factory_greenlit` | **false** (draft) |

## 2. Product job (Play path)

Enter Craft (empty amber). Hover primary vertex → **grey ghost** shows where Full will land. LMB → that **same seat** becomes a **permanent opaque Full plate** that remains after mouse leave / highlight restore / neighbor rebuild. **Owned update-four and coast gate still run** on that place. RMB clears. Create World Open / GEN-biomes assign·probe·pack / PACK paths stay intact and are **out** of this Prefer’s Success.

## 3. Factory path (required before any staging green)

1. Prefer compose with Gate A fields (`ticket_map_id`, `structural_success`, `success_object`, `do_not_waive`).
2. Gate A mechanical (`prefer_map_fidelity_check` when applicable).
3. Gate B₁ hostile VALIDATE `prefer_map_fidelity` → `map_fidelity_hostile_ok` (pending until run).
4. Operator greenlight only after A+B₁ — then weld LIVE.
5. Gate B₂ weld intent VALIDATE `prefer_weld_intent` → `weld_intent_hostile_ok` (after weld; smoke path; not run while unwelded).
6. Operator F5 for feel. **No KEEP** without F5 + stranger sentence + B₂.

## 4. Refuse

- `intent_collapsed_to_mechanics` · `hotkey_as_product_ux` · `verify_mcp_only`
- `piggyback_as_place_success` · `piggyback_skip_update_four` · `update_four_false_on_lmb_place`
- `seat_polygon_as_place_success` · `cull_mode_as_place_success`
- `neighbor_rebuild_deletes_full` · `ghost_seat_neq_commit_seat`
- `townscaper_done_as_parity_success` · GEN-fill as place Success · GEN-biomes as this ticket’s Success
- Arming GEN-sites · claiming GEN-biomes KEEP · claiming place KEEP in draft

## 5. Out of scope this Prefer

GEN-sites · GEN-biomes ownership / F5 · friends/roster · Terrain3D · MeshLibrary reauth as blocker · reopening brush §0 KEEP · piggyback v2 chat hotfix · full world-builder fidelity.
