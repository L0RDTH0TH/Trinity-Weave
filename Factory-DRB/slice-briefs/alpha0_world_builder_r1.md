---
title: Series hub — alpha0_world_builder_r1
series_id: alpha0_world_builder_r1
created: 2026-10-15
updated: 2026-10-15
project-id: genesis-mythos-master
status: active
claim_class: staging
active_step: gen_terrain_product
active_slice: alpha0_gen_terrain_product_r1
active_disposition: live_weld_landed_staging_awaiting_f5
keeps_world_new: alpha0_world_new_r1
keeps_world_new_fidelity: KEEP-real
keeps_world_bounds: alpha0_world_bounds_r1
keeps_world_bounds_fidelity: KEEP-debt
keeps_world_propose: alpha0_world_propose_r1
keeps_world_propose_fidelity: KEEP-debt
keeps_world_s0_intents: alpha0_world_s0_intents_r1
keeps_world_s0_disposition: KEEP-debt_packaging
keeps_world_import: alpha0_world_import_r1
keeps_world_import_disposition: KEEP-debt_parked
keeps_world_empty_campaigns: alpha0_world_empty_campaigns_r1
keeps_world_empty_campaigns_fidelity: KEEP-real
keeps_world_parity: alpha0_world_parity_r1
keeps_world_parity_note: empty_craft_enter_KEEP-real_GEN_owns_fill
gen_terrain_2a: alpha0_gen_terrain_r1
gen_terrain_2a_status: INCOMPLETE_superseded_by_GEN-terrain-product
next_pointer: GEN-terrain-product
next_armed: false
ticket_map: World-Builder-Mini-Game-Ticket-Map
prior_brush_series: alpha0_stalberg_grid_kernel_r1
freeze_no_keep_product_success:
  - WORLD-bounds
  - WORLD-propose
  - WORLD-import
  - GEN-terrain
---

# Series hub — `alpha0_world_builder_r1`

World-builder mini-game Prefer ladder (§1+ of [[World-Builder-Mini-Game-Ticket-Map]]). Brush honesty lives on [[alpha0_stalberg_grid_kernel_r1]] and is **closed** at **2z KEEP-real** (VIS-zfight via **2w**; **2v** SUPERSEDED).

**Grok recovery 2026-10-15:** Map law + weld proofs. Active = **`GEN-terrain-product`** GREENLIGHT WELD LIVE landed · staging awaiting F5 on W1–W5. **No KEEP** until F5-green. **Do not arm GEN-biomes.**

| Step | Slice | Ticket | Status |
|------|-------|--------|--------|
| **1a** | [[alpha0_world_new_r1]] | `WORLD-new` | **KEEP-real** — shell, four biases, enter craft; bias stored, does not generate |
| **1b** | [[alpha0_world_bounds_r1]] | `WORLD-bounds` | **KEEP-debt** — dials must change generate (proof → W2); not product Success |
| **1c** | [[alpha0_world_propose_r1]] | `WORLD-propose` | **KEEP-debt** — menu-only ≠ Success |
| **1d** | [[alpha0_world_s0_intents_r1]] | `WORLD-s0-intents` | **KEEP-debt (packaging)** — off Create World critical path until GEN consumes; do not expand |
| **1e** | [[alpha0_world_import_r1]] | `WORLD-import` | **KEEP-debt / parked** — stub ≠ product; park until save/load |
| **1f** | [[alpha0_world_empty_campaigns_r1]] | `WORLD-empty-campaigns` | **KEEP-real** — zero campaigns lawful |
| **1g** | [[alpha0_world_parity_r1]] | `WORLD-parity` | **KEEP-real** — empty craft enter; GEN owns fill |
| **2a** | [[alpha0_gen_terrain_r1]] | `GEN-terrain` | **INCOMPLETE / superseded** — T-hotkey not product Success; keep callable |
| **active** | [[alpha0_gen_terrain_product_r1]] | `GEN-terrain-product` | **LIVE W1–W5 landed** · staging awaiting F5 · not KEEP · `next_armed: false` |

## Debt notes (binding)

- **1b:** Proof that dials change the world moves into `GEN-terrain-product` W2. Freeze: no new KEEP as product Success.
- **1c:** Accept/reject/revise must change a scaffold the generator or board uses. Menu chrome alone stays debt.
- **1d:** World seeds, not campaign copy. Optional; unread until a GEN row consumes them.
- **1e:** Real bundle in or not this ticket. No second stub weld.

**Active:** `GEN-terrain-product` [[alpha0_gen_terrain_product_r1]] — LIVE W1–W5 landed, `claim_class: staging`. After operator F5 on W1–W5 → next arm **`GEN-tone`** (not GEN-biomes). Pointer stays `GEN-terrain-product` / `next_armed: false` until that F5-green.
