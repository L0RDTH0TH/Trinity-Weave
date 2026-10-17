---
title: Slice brief — alpha0_townscaper_tutorial_s4_module_selection_r1
slice_id: alpha0_townscaper_tutorial_s4_module_selection_r1
ask_id: alpha0_townscaper_tutorial
series_id: alpha0_townscaper_tutorial_r1
umbrella_ask_id: alpha_architecture_half_b
tutorial_step: 4
created: 2026-10-02
updated: 2026-10-02
claim_class: staging
factory_greenlit: false
status: draft
template: Half-B-Weld-Brief-Template
depends_on: alpha0_townscaper_tutorial_s3_connector_modules_r1
next_in_chain: alpha0_townscaper_tutorial_s5_genesis_adapt_r1
launch_word: WELD
armed_packet: null
---

# Slice brief — `alpha0_townscaper_tutorial_s4_module_selection_r1`

**Draft only — greenlit false.** Tutorial step 4 — module selection rules (marching-style mask → module). Edges/corners look built, not pasted. Series: [[alpha0_townscaper_tutorial_r1]].

## 1. Header

| Field | Value |
|-------|--------|
| `slice_id` | `alpha0_townscaper_tutorial_s4_module_selection_r1` |
| Tutorial step | **4 of 6** |
| Scope | Selection rules so edges/corners read as built connectors, not pasted props |
| `factory_greenlit` | `false` |

## 5. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5:** Edges/corners look built, not pasted; selection follows dual corners; mass from step 3 preserved; Terrain3D out |

## 6. Refuse (series preload)

`prop_scatter_as_composition` · `bitmask_equals_townscaper` · `skip_dual_offset` · `procedural_only_as_success` · `terrain3d_in_scope` · `boil_the_ocean_df` · `verify_mcp_only` · `bundle_tutorial_steps`

## 7. Out of scope

Art Prefer (step 6 blocked until s3–s4 mass green), DF-depth, Terrain3D, Genesis palette pass (step 5).
