---
title: Slice brief — alpha0_chargen_seats_tricam_r1 (superseded)
slice_id: alpha0_chargen_seats_tricam_r1
ask_id: alpha0_pf1_chargen_seats_tricam
umbrella_ask_id: alpha_architecture_half_b
created: 2026-10-01
updated: 2026-10-01
claim_class: staging
factory_greenlit: false
status: superseded
template: Half-B-Weld-Brief-Template
superseded_by: alpha0_worldgen_dualgrid_sparky_r1
---

# Slice brief — `alpha0_chargen_seats_tricam_r1` (superseded)

**Not first-weld.** Status: `superseded`. Active first Half-B weld is now [[alpha0_worldgen_dualgrid_sparky_r1]] (`ask_id: alpha0_worldgen_dualgrid_sparky`).

Chargen / seats / tricam polish remain valid later umbrella work under [[alpha_architecture_half_b]] — do not treat this file as the active queue or Half-B driver.

---

Filled from [[Half-B-Weld-Brief-Template]]. Umbrella: [[alpha_architecture_half_b]]. Lock: [[FEEDSTOCK-SHAPE]].

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_pf1_chargen_seats_tricam` |
| `slice_id` | `alpha0_chargen_seats_tricam_r1` |
| Scope | Tutorial PF1 chargen at player seat + seat asymmetry + three functional cams + fantasy GUI chrome |
| `claim_class` | `staging` |
| `factory_greenlit` | `false` |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | generate / update as needed on LIVE slug |
| First-weld | **No** — superseded by [[alpha0_worldgen_dualgrid_sparky_r1]] |

## 2. Focus inspirations (this weld only)

| Source | Why in focus |
|--------|----------------|
| Baldur's Gate 3 | Seat agency; player-authored character; intent→sheet feel |
| Fantasy Grounds | Table/seat asymmetry; VTT resolve chrome peers |
| TaleSpire | Classic VTT ortho peer for `vtt_planar_ortho` |
| GUI chrome | [[GUI-Chrome-Direction-Fantasy-UI]] / `Ingest/fantasy_ui.jpg` |
| 3D bar (if meshes) | [[Visual-Factory-Direction-Stylized-Low-Poly]] / Astroneer stylized low poly |

Seasoning: rest of Inspiration INDEX when not in focus.

## 3. Load set

- [x] [[FEEDSTOCK-SHAPE]]
- [ ] Host-weld: `implementation_factory_loop` + `product_factory_pipeline`
- [ ] [[Godot-Implementation-Decision-Matrix]] — quote Prefer/Never for seats/cams/player as touched
- [ ] [[ENGINE-COMPILE-PACK-stock_godot_fps]] if FP/`anchored_actor` move/look
- [x] [[INSPIRATION-HALF-B-SHAPE]]
- [x] [[GUI-Chrome-Direction-Fantasy-UI]]
- [x] [[Camera-Mode-Taxonomy-Live]]
- [ ] [[Visual-Factory-Direction-Stylized-Low-Poly]] when meshes/env land

## 4. End flavor

BG3/FG-shaped **player-seat** PC authorship with a **tutorial-first Pathfinder 1e** flow (operator is D&D-experienced, has not played PF1 — bridge honest D&D vocabulary to **real PF1** steps/terms; not a 5e rules engine). Menus/panels land **fantasy UI chrome**. All three cameras work: `anchored_actor`, `vtt_planar_ortho`, `god_mode_sparky`. DM is not a PC.

## 5. Acceptance (staging)

| Field | Value |
|-------|--------|
| `done_when` | Operator can move through a non-laughable menu/seat path (GUI bar), complete **tutorial-guided** PF1 PC authorship at the **player** seat, and switch among all three cameras with correct mode behavior |
| Operator attest | F5 / play; walk+look caveat OK on Wayland; **ban** `verify_mcp_only` |
| `claim_class` | `staging` — not `ask_success`; not greenlit |

## 6. Refuse

Matrix **Never** + [[Ask-Fidelity-Exemplars]] + factory rejects:

`inspiration_shape_miss` · `fidelity_miss` · `engine_pattern_miss` · `gui_input_steal` · `seat_ok_feel_fail` · `verify_mcp_only` · `option_button_only` · `dropdown_only` · `DM_picks_PC` · `front_door_spine_only` · `table_chrome_only`

| Code | Note |
|------|------|
| `option_button_only` / `dropdown_only` | Not chargen Success |
| `DM_picks_PC` | Player seat owns PC authoring |
| Camera conflation | Ortho ≠ sparky ≠ anchored — [[Camera-Mode-Taxonomy-Live]] |
| 5e-as-engine | PF1 legal path; tutorial may *bridge* language only |

## 7. Out of scope

- Archived `horizon_demo_investor` Success
- Months of DF worldgen as mandatory (possible ≠ required)
- Paizo prose dump
- Full CRB dump / every PF1 option in weld #1 — guided tutorial subset that authors a legal-enough alpha PC
- Overnight `factory_greenlit`
- **Active first-weld driver** (see [[alpha0_townscaper_craft_core_r1]])

## 8. Receipt (required on Half-B completion)

1. `ask_id` / `slice_id`
2. Focus inspiration + GUI (and 3D if used) cites landed
3. Matrix Prefer quotes for touched rows
4. Tri-cam mode ids verified in receipt
5. `claim_class: staging` · `factory_greenlit: false`
6. Operator attest or explicit debt

## Related

- **Active craft chain:** [[alpha0_townscaper_craft_core_r1]] → visual → DF-depth (Terrain3D deferred; legacy [[alpha0_worldgen_dualgrid_sparky_r1]] scrapped this round)
- [[alpha_architecture_half_b]] · [[Half-B-Alpha-Mode]] · [[Half-B-Weld-Brief-Template]] · [[Ask-Fidelity-Exemplars]]
