---
lane_id: module
slice_id: row_ux_world_generation_r1_d6
producer_run_id: sp-sp-craft-2aae0f
ux_bullet_ids: ["UX-1", "UX-3", "UX-5", "UX-7"]
prefer_authorship_injected: true
---

# Lane Mission — module

## Mission
Deliver your lane contribution for `ux_world_generation` at depth 6.


## Prefer authorship contract (host law — durable; not one-off brief text)

- **Slice:** `row_ux_world_generation_r1_d6`
- **YT lock:** https://www.youtube.com/watch?v=Y19Mw5YsgjI
- **Vault cite:** `Ingest/Resources/Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md`
- **Craft** = Hot Wheels tile authorship only (Townscaper dual-grid)
- **Terrain3D** = real car / fed consumer under Sparky (or explicit feed)
- **No** craft-view Terrain3D blend / deform
- **No** camera recenter on place
- **No proxy override:** host_touch_budget / shell seats / bootstrap stubs cannot pass or waive these product Prefer seats

### Durable negative examples (fail closed)
- `craft_cam_recenter_on_place` — Craft place/remove recenters camera / orbit focus onto the new tile
- `craft_terrain_blend` — Craft view deforms checker/grid into Terrain3D heights (Hot Wheels≠car)
- `craft_phase_terrain3d_deform` — Craft phase authors via Terrain3D sculpt instead of tile map
- `unfed_terrain_under_sparky` — Sparky sees graybox-only; Terrain3D not fed as separate consumer layer
- `inspiration_shape_miss` — Prefer collapses Hot Wheels craft into Terrain3D under craft cam

## UX bullets you own
- **UX-1:** **Seat:** shared_table, dm_as_player, privileged_access · **Trigger:** enter `ux_worldgen_gui` · **Observable response:** Collaborative generation dialogue — propose scaffolds, choose/refine, preview, accept/regenerate a persistent living world (under DM can create (table can shape) a persistent living world). · **Refusal/guard:** out of contract / wrong seat · **Residue:** lasting readable state from this moment
- **UX-3:** **Seat:** shared_table, dm_as_player, privileged_access · **Trigger:** contract clause 2 · **Observable response:** players do not author the first world · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable
- **UX-5:** **Seat:** shared_table, dm_as_player, privileged_access · **Trigger:** contract clause 4 · **Observable response:** import/attach first-class · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable
- **UX-7:** `ux_worldgen_gui` — Collaborative generation dialogue — propose scaffolds, choose/refine, preview, accept/regenerate a persistent living world (under DM can create (table can shape

## Shape context
See SIB §2 — do not relitigate conceptual lock.

## Realization notes
See SIB §3 — crosswalk acceptance to your UX bullets.

## Done when
- Build passes
- Lane receipt cites UX bullet ids satisfied
- Prefer product seats met (no proxy override)

## Prefer craft-visual overlay (operator GREENLIGHT ticket 2)

- **half_b_overlay:** `alpha0_townscaper_craft_visual_r1`
- **ask_id:** `alpha0_townscaper_craft_visual`
- **armed packet:** `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_townscaper_craft_visual_r1.armed.yaml`
- **brief:** `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_townscaper_craft_visual_r1.md`
- **LIVE:** `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos`
- **Hard law:** Re-skin existing dual MeshLibrary variants (Full/Corner/Edge/Diagonal/InverseCorner+Empty); do not collapse to one cube; do not replace logic-point→corner-bitmask with raw-cell-only; small craft tile set only — no full biome atlas / DF depth; LMB/RMB under mouse + no cam yank regression; Terrain3D absent/hard-disabled under craft.
- **Receipt must:** cite Visual-Factory-Direction-Stylized-Low-Poly + prove dual variant ids still differ.
- **Lanes:** module-primary; ADC/TAC as drops only if needed.
- Ban `verify_mcp_only`. claim_class: staging.

## Prefer authorship contract (host law — durable; not one-off brief text)

- **Slice:** `alpha0_townscaper_craft_visual_r1`
- **YT lock:** https://www.youtube.com/watch?v=Y19Mw5YsgjI
- **Vault cite:** `Ingest/Resources/Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md`
- **Craft** = Hot Wheels tile authorship only (Townscaper dual-grid)
- **Terrain3D** = real car / fed consumer under Sparky (or explicit feed)
- **No** craft-view Terrain3D blend / deform
- **No** camera recenter on place
- **No proxy override:** host_touch_budget / shell seats / bootstrap stubs cannot pass or waive these product Prefer seats

### Durable negative examples (fail closed)
- `craft_cam_recenter_on_place` — Craft place/remove recenters camera / orbit focus onto the new tile
- `craft_terrain_blend` — Craft view deforms checker/grid into Terrain3D heights (Hot Wheels≠car)
- `craft_phase_terrain3d_deform` — Craft phase authors via Terrain3D sculpt instead of tile map
- `unfed_terrain_under_sparky` — Sparky sees graybox-only; Terrain3D not fed as separate consumer layer
- `inspiration_shape_miss` — Prefer collapses Hot Wheels craft into Terrain3D under craft cam

